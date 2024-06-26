# Generated by Django 4.1.5 on 2023-02-04 18:22

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QRGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('prefix', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('suffix', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('zeros', models.IntegerField(blank=True, null=True, verbose_name='zeros count in id')),
                ('qr_number', models.IntegerField(verbose_name='number of qrs')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='static/imgs/')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='qr_groups', to='products.product')),
            ],
            options={
                'verbose_name': 'QR Group',
                'verbose_name_plural': 'QR Groups',
            },
        ),
        migrations.CreateModel(
            name='QRZipLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shorten_url', models.CharField(default='c8cf9c0d3acd4b1a33', max_length=20)),
                ('url', models.CharField(blank=True, max_length=255, null=True)),
                ('ttl', models.IntegerField(default=1, verbose_name='Time to live (days)')),
                ('password', models.CharField(default='D6R2x6KyAt6RqmFWL6XF', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('qr_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='zip_links', to='qr_codes.qrgroup', verbose_name='QR Group')),
            ],
            options={
                'verbose_name': 'QR Zip link',
                'verbose_name_plural': 'QR Zip links',
            },
        ),
        migrations.CreateModel(
            name='NFCTag',
            fields=[
                ('hw_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Hardware ID')),
                ('serial_num', models.IntegerField(default=1, verbose_name='Serial number')),
                ('qr_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nfc_tags', to='qr_codes.qrgroup', verbose_name='QR Group')),
            ],
            options={
                'verbose_name': 'NFC Tag',
                'verbose_name_plural': 'NFC Tags',
            },
        ),
    ]
