from django.urls import path
from django.urls import include
from .views import ProductCategoryViewSet, ProductViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = 'products'

router = DefaultRouter()
router.register(r'categories', ProductCategoryViewSet, basename='categories')
router.register('', ProductViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls)),
]