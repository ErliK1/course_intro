from rest_framework import serializers

from product.models import Product, Brand, Category, ProductCategory

class ProductListFilterSerializer(serializers.Serializer):
    category = serializers.ListField(child=serializers.IntegerField(),
                                     allow_null=True, required=False)
    brand = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    name = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    discount = serializers.BooleanField(allow_null=True, required=False)

class BrandProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'name')

class CategoryProductListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='category.id')
    name = serializers.CharField(source='category.name')

    class Meta:
        model = ProductCategory
        fields = ('id', 'name')



