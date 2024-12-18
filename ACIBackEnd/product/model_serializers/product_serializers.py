from rest_framework import serializers

from product.models import Product, Brand, Category, ProductCategory, ProductImage
from shared.utils import check_ids_part_of_db
from shared.exception import ACIValidationError


class BrandSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Brand
        fields = ('id', 'name', 'country', 'description')
        extra_kwargs = {
                    'id': {'read_only': True},
                }
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'description')
        extra_kwargs = {
                'id': {'read_only': True}
                }

class ProductCreateSerializer(serializers.ModelSerializer):
    category = serializers.ListField(child=serializers.IntegerField())
    images = serializers.ListField(child=serializers.ImageField(), required=False)
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())

    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'sku_code', 'buy_price', 'sell_price',
                  'description', 'brand', 'stock', 'discount', 'main_image', 'images')
        extra_kwargs = {
                    'id': {'read_only': True},
                    'buy_price': {'required': True}
                }


    def validate(self, data):
        list_of_category_ids = data.get('category')
        if not check_ids_part_of_db(list_of_category_ids, Category):
            raise ACIValidationError("Kategorite e dhena nuk gjenden!")
        return data

    def create(self, validated_data):
        images = []
        if validated_data.get('images'):
            images = validated_data.pop('images')
        category_ids = validated_data.pop('category')
        product = Product.objects.create(**validated_data)
        for category_id in category_ids:
            ProductCategory.objects.create(product=product, category_id=category_id)
        for image in images:
            ProductImage.objects.create(product=product, image=image)
        return product

class ProductUpdateSerializer(ProductCreateSerializer):
    category = serializers.ListField(child=serializers.IntegerField(), required=False)
    images = serializers.ListField(child=serializers.ImageField(), required=False)
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all(), required=False)
    class Meta(ProductCreateSerializer.Meta):
        extra_kwargs = {
            'name': {'required': False},
            'sku_code': {'required': False},
            'buy_price': {'required': False},
            'sell_price': {'required': False},
            'description': {'required': False},
            'stock': {'required': False},
            'discount': {'required': False},
            'main_image': {'required': False}
        }
    
            
    def update(self, instance: Product, validated_data):
        instance.name = validated_data.get('name', instance.name)
        if categories := validated_data.get('category'):
            self.create_product_categories(instance, categories)
        instance.sku_code = validated_data.get('sku_code', instance.sku_code)
        instance.sell_price = validated_data.get('sell_price', instance.sell_price)
        instance.buy_price = validated_data.get('buy_price', instance.buy_price)
        instance.description = validated_data.get('description', instance.description)
        instance.brand = validated_data.get('brand', instance.brand)
        instance.stock = validated_data.get('stock', instance.stock)
        instance.discount = validated_data.get('discount', instance.discount)
        instance.main_image = validated_data.get('main_image', instance.main_image)
        if images := validated_data.get('images'):
            self.create_product_images(instance, images)
        return instance
        
            
    def create_product_categories(self, product, categories):
        categories = Category.objects.filter(id__in=categories)
        product_categories = product.product_categories
        product_categories.delete()
        for element in categories:
            ProductCategory.objects.create(category=element, product=product)
           
           
    def create_product_images(self, product, images):
        product_images = ProductImage.objects.filter(product=product)
        product_images.delete()
        for image in images:
            ProductImage.objects.create(product=product, image=image)





class ProductListSerializer(serializers.ModelSerializer):
    
    total_discount = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    brand = serializers.CharField(source='brand.name')
    category = serializers.SerializerMethodField()
    product_images = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'sku_code', 'buy_price', 'sell_price', 'has_discount', 'brand', 'discount', 'main_image', 'total_discount', 'product_images')
        
        
    
    def get_total_discount(self, obj):
        return obj.sell_price - (obj.discount * obj.sell_price)
    
    def get_discount(self, obj):
        return obj.discount * 100
    
    def get_category(self, obj):
        queryset_category_id = obj.product_categories.all().values_list('category_id', flat=True)
        categories = Category.objects.filter(id__in=queryset_category_id)
        serializer = CategorySerializer(categories, many=True)
        return serializer.data
    
    def get_product_images(self, obj):
        queryset = ProductImage.objects.filter(product_id=obj.pk).values_list('image', flat=True)
        return list(queryset)

class ProductInsertDiscountSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True)
    discount = serializers.FloatField()



