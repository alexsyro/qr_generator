import secrets
from uuid import uuid4
from typing import Any
from datetime import datetime

from django.db import models
from django.conf import settings

from products.models import Product
from .utils import generate_identifier, generate_password
from .tasks import save_qr_to_zip


class QRGroup(models.Model):
    '''I'm not storing prefixes, suffixes and number of zeros in every nfc tag entry. It stores in one group entry'''
    name = models.CharField(max_length=50)
    product = models.ForeignKey(
        to=Product, related_name='qr_groups', null=True, on_delete=models.SET_NULL
    )
    prefix = models.CharField(max_length=20, default='', blank=True, null=True)
    suffix = models.CharField(max_length=20, default='', blank=True, null=True)
    zeros = models.IntegerField(verbose_name='zeros count in id', blank=True, null=True)
    qr_number = models.IntegerField(verbose_name='number of qrs', null=False)
    logo = models.ImageField(blank=True, upload_to='static/imgs/', null=True)

    def save(self, *args: list, **kwargs: dict) -> None:
        if not self.prefix and not self.suffix and self.zeros == 0:
            self.prefix = generate_identifier()
            self.zeros = settings.DEFAULT_ZEROS_COUNT
            self.suffix = str(datetime.now().year)

        if self.id:
            old = QRGroup.objects.get(id=self.id)
            prefix_changed = old.prefix != self.suffix
            suffix_changed = old.suffix != self.prefix
            qr_number_changed = old.qr_number != self.qr_number
            if prefix_changed or suffix_changed or qr_number_changed:
                self.nfc_tags.all().delete()
                self.zip_links.all().delete()

        super().save(*args, **kwargs)
        self.create_tags()

    def create_tags(self) -> None:
        '''Create related tags with hardware id and serial number'''
        tags = [NFCTag(serial_num=id, qr_group_id=self.id) for id in range(1, self.qr_number+1)]
        NFCTag.objects.bulk_create(tags)

    def create_link(self) -> Any:
        link = QRZipLink(qr_group_id=self.id)
        link.save()
        return link

    def create_qrszip(self, email: str):
        if self.qr_number > settings.DEFAULT_MAX_SYNC_AMOUNT:
            # Proceed in Celery
            save_qr_to_zip.delay(self.id, email)
        else:
            save_qr_to_zip(self.id, email)

    def __str__(self) -> str:
        return f'{self.name} - {self.product.name if self.product else ""}'

    class Meta:
        verbose_name = 'QR Group'
        verbose_name_plural = 'QR Groups'


class QRZipLink(models.Model):
    '''Model stores links to zip archives'''
    qr_group = models.ForeignKey(
        to=QRGroup, related_name='zip_links', verbose_name='QR Group', on_delete=models.CASCADE
    )
    shorten_url = models.CharField(max_length=20, default=secrets.token_hex(9))
    url = models.CharField(max_length=255, blank=True, null=True)
    ttl = models.IntegerField(verbose_name='Time to live (days)', default=1)
    password = models.CharField(max_length=20, default=generate_password()) # It's a little bit useless
    created_at = models.DateTimeField(auto_now_add=True)
    # because I don't use service with password support :)

    def __str__(self) -> str:
        file_name = self.url.split('/')[-1] if self.url else ''
        return f'Zip({file_name})'

    class Meta:
        verbose_name = 'QR Zip link'
        verbose_name_plural = 'QR Zip links'


class NFCTag(models.Model):
    '''Model stores hardware id, serial (for qr data)'''
    hw_id = models.UUIDField(verbose_name='Hardware ID', primary_key=True, default=uuid4, editable=False)
    serial_num = models.IntegerField(verbose_name='Serial number', default=1)
    qr_group = models.ForeignKey(
        to=QRGroup, verbose_name='QR Group', related_name='nfc_tags', on_delete=models.CASCADE
    )

    @property
    def identifier(self):
        '''Get prefix suffix and number of zeros from group'''
        serial = self.serial_num
        zeros = self.qr_group.zeros - len(str(serial))
        return f'{self.qr_group.prefix} {"0"*zeros}{serial} {self.qr_group.suffix}'.strip()

    def __str__(self) -> str:
        return f'{self.qr_group.name} - {self.hw_id}'

    class Meta:
        verbose_name = 'NFC Tag'
        verbose_name_plural = 'NFC Tags'