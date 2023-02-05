import base64
import io
from datetime import datetime
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from qr_codes.models import QRZipLink, QRGroup, NFCTag
from qr_codes.serializers import (
    QRGroupSerializer, QRGroupListSerializer, NFCTagSerializer, QRZipSerializer, QRsImageSerializer
)

class QRGroupViewSet(viewsets.ModelViewSet):
    queryset = QRGroup.objects.all()
    serializer_class = QRGroupSerializer

    def create(self, request, *args, **kwargs):
        logo = request.data.get('logo')
        image_file = None
        data = {
            'name': request.data.get('name'),
            'product_id': request.data.get('product_id'),
            'prefix': request.data.get('prefix'),
            'suffix': request.data.get('suffix'),
            'zeros': request.data.get('zeros', 0),
            'qr_number': request.data.get('qr_number'),
        }
        if QRGroup.objects.filter(name=data['name']):
            data['name'] = data['name'] + str(datetime.now())
        serializer = self.serializer_class(data=data)
        if logo:
            file_name = logo['name']
            file = logo['file'].split(',')[1]
            decoded = base64.b64decode(file)
            image_file = ContentFile(io.BytesIO(decoded).getvalue(), name=file_name)
            data.update({'logo': image_file})
        if serializer.is_valid():
            qr_group = serializer.save()
            qr_group.product_id = data['product_id']
            qr_group.save()
            qr_group.create_tags()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        qrs = QRGroup.objects.all().select_related('product')
        serializer = QRGroupListSerializer(qrs, many=True)
        return Response(serializer.data)


class NFCTagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NFCTag.objects.select_related('qr_group__product__category').all()
    serializer_class = NFCTagSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 12

    def retrieve(self, request, pk=None):
        tag = self.get_object()
        serializer = NFCTagSerializer(tag)
        data = serializer.data
        return Response(data)

    def list(self, request, *args, **kwargs):
        qr_group_id = self.request.GET.get('qrgroupid')
        qrs = NFCTag.objects.filter(qr_group_id=qr_group_id)
        page = self.paginate_queryset(qrs)
        if page is not None:
            serializer = QRsImageSerializer(page, many=True)
            response_data = serializer.data
            for data in response_data:
                data['img_name'] = data['qr_image']['img_name']
                data['qr_image'] = base64.b64encode(data['qr_image']['qr_image'].getvalue()).decode()
            return self.get_paginated_response(serializer.data)

        serializer = QRsImageSerializer(qrs, many=True)
        return Response(response_data)


class QRZipViewSet(viewsets.ViewSet):
    queryset = QRZipLink.objects.all()
    serializer_class = QRZipSerializer
    lookup_field = 'shorten_url'

    def create(self, request, *args, **kwargs):
        qr_group_id = self.request.GET.get('qrgroupid')
        email = self.request.GET.get('email')
        group = QRGroup.objects.filter(id=qr_group_id).first()
        if not group:
            return Response(data={'error': f'No group with ID {qr_group_id}'}, status=404)
        if not group.zip_links.filter(url__isnull=True).exists():
            group.create_qrszip(email=email)
            return Response(status=201)
        return Response(data={'error': 'Zip is creating'}, status=425)

    def list(self, request, *args, **kwargs):
        qr_group_id = self.request.GET.get('qrgroupid')
        qrs = QRZipLink.objects.filter(qr_group_id=qr_group_id)
        serializer = QRZipSerializer(qrs, many=True)
        return Response(serializer.data)

    def retrieve(self, request, shorten_url=None):
        zip = get_object_or_404(QRZipLink, shorten_url=shorten_url)
        if not zip.url:
            return Response(
                'The trolls are still drawing your QR codes. Please be patient. \
                    Check this: https://www.youtube.com/@kurzgesagt/videos'
            )
        return HttpResponseRedirect(zip.url)

    def delete(self, request, shorten_url=None):
        zip = get_object_or_404(QRZipLink, shorten_url=shorten_url)
        zip.delete()
        return Response(status=200)
