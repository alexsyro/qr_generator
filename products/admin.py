from django.contrib import admin
from products.models import ProductCategory, Product


@admin.register(ProductCategory)
class ProdCategoryAdmin(admin.ModelAdmin):
    model = ProductCategory
    list_display = ['id', 'name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ['id', 'name']

