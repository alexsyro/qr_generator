from io import BytesIO
from django.conf import settings
from rest_framework import serializers
from qr_codes.models import QRGroup, QRZipLink, NFCTag
from qr_codes.utils import generate_qr


class QRGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = QRGroup
        fields = ('id', 'name', 'product_id', 'qr_number', 'prefix', 'suffix', 'zeros', 'logo')

class QRGroupListSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField(read_only=True)

    def get_product_name(self, obj):
        
        return obj.product.name if obj.product else ''

    class Meta:
        model = QRGroup
        fields = ('id', 'name', 'product_name', 'qr_number', 'prefix', 'suffix', 'zeros', 'logo')


class NFCTagSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='qr_group.product.name')
    category = serializers.CharField(source='qr_group.product.category.name')
    qr_group = serializers.CharField(source='qr_group.name')

    class Meta:
        model = NFCTag
        fields = ('hw_id', 'identifier', 'qr_group', 'product_name', 'category', 'qr_group')


class QRsSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    def get_url(self, obj):
        return f'{settings.SITE_URL}/api/qrs/tags/{obj.hw_id}/'

    class Meta:
        model = NFCTag
        fields = ('hw_id', 'url', 'serial_num')

class QRsImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    qr_image = serializers.SerializerMethodField(read_only=True)

    def get_url(self, obj):
        return f'{settings.SITE_URL}/api/qrs/tags/{obj.hw_id}/'

    def get_qr_image(self, obj):
        qr_group = obj.qr_group
        text = f'{settings.SITE_URL}/api/qrs/tags/{obj.hw_id}/'
        zeros = qr_group.zeros - len(str(obj.serial_num))
        img_name = f'{obj.qr_group.prefix} {"0"*zeros}{str(obj.serial_num)} {qr_group.suffix}.png'

        img = generate_qr(text, qr_group.logo)
        img_buffer = BytesIO()
        img.save(img_buffer, format='PNG')
        return {'qr_image': img_buffer, 'img_name': img_name}

    class Meta:
        model = NFCTag
        fields = ('qr_image', 'url')


class QRZipSerializer(serializers.ModelSerializer):
    full_url = serializers.SerializerMethodField(read_only=True)

    def get_full_url(self, obj):
        return f'{settings.SITE_URL}/api/qrs/zips/{obj.shorten_url}/'

    class Meta:
        model = QRZipLink
        fields = ('id', 'full_url', 'shorten_url', 'created_at')
