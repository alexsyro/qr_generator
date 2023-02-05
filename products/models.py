from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=100, null=False)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Product category'
        verbose_name_plural = 'Product categories'


class Product(models.Model):
    name = models.CharField(max_length=100, null=False)
    category = models.ForeignKey(to=ProductCategory, related_name='products', null=True, on_delete=models.DO_NOTHING)
    info = models.TextField(null=False)

    def __str__(self) -> str:
        return f'{self.category.name} - {self.name}'

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
