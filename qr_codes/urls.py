from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QRGroupViewSet, NFCTagViewSet, QRZipViewSet


app_name = 'qrs'

router = DefaultRouter()
router.register(r'qr_groups', QRGroupViewSet, basename='qr_groups')
router.register(r'tags', NFCTagViewSet, basename='tags')
router.register(r'zips', QRZipViewSet, basename='download_zip')

urlpatterns = [
    path('', include(router.urls)),
]