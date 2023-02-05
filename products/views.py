from rest_framework import viewsets
from rest_framework.response import Response
from .models import Product, ProductCategory
from products.serializers import ProductCategorySerializer, ProductSerializer


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

    def list(self, request, *args, **kwargs):
        category_id = request.GET.get('categoryid')
        if category_id:
            qrs = self.queryset.filter(category_id=category_id)
            serializer = self.serializer_class(qrs, many=True)
            data = serializer.data
            return Response(data=data)
        return super().list(request, *args, **kwargs)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
