from typing import Any
from django.contrib import admin
from qr_codes.models import QRGroup, QRZipLink, NFCTag


@admin.register(QRGroup)
class QRGroupAdmin(admin.ModelAdmin):
    model = QRGroup
    list_display = ['name', 'prod', 'nfc_tags', 'prefix', 'suffix']

    def prod(self, obj):
        return obj.product.name if obj.product else ''
    
    def nfc_tags(self, obj):
        return obj.nfc_tags.count()


@admin.register(NFCTag)
class NFCTagAdmin(admin.ModelAdmin):
    model = NFCTag
    list_display = ('hw_id', 'identifier', 'product')

    def get_queryset(self, request):
        return NFCTag.objects.all().select_related('qr_group')

    def identifier(self, obj):
        prefix = obj.qr_group.prefix
        id = f'{"0"* (obj.qr_group.zeros - len(str(obj.serial_num)))}{obj.serial_num}' 
        suffix = obj.qr_group.suffix
        return f'{prefix} {id} {suffix}'.strip()

    def product(self, obj):
        return obj.qr_group.product.name

@admin.register(QRZipLink)
class QRZipLinksAdmin(admin.ModelAdmin):
    model = QRZipLink
