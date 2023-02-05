from rest_framework import serializers
from products.models import ProductCategory, Product


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ('__all__')


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.StringRelatedField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'info', 'category_name', 'category_id')



