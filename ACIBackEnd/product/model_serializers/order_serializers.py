from functools import reduce
from rest_framework import serializers

from product.models import Product, OrderProduct, Order
from shared.exception import ACIValidationError

from django.db.models import Sum


class OrderSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = Order
        fields = ('id', 'client_secret', 'printed_receipt',
                  'name', 'email', 'address', 'is_admin', 'is_paid_online')
        extra_kwargs = {
                    'id': {'read_only': True},
                    'is_paid_online': {'read_only': True}
                }


class OrderProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OrderProduct
        fields = ('id', 'order', 'product', 'product_count', 'sell_price', 'discount', 'total_price')
        extra_kwargs = {
            'id': {'read_only': True},
            'order': {'read_only': True},
        }
    
        
class OrderProductSerializerUser(OrderProductSerializer):
    
    class Meta(OrderProductSerializer.Meta):
        extra_kwargs = {
            'sell_price': {'required': False},
            'discount': {'required': False},
            **OrderProductSerializer.Meta.extra_kwargs
        }
        
    
        

class OrderCreateForAdminSerializer(serializers.ModelSerializer):
   
    order_products = OrderProductSerializer(many=True)
    class Meta:
        model = Order
        fields = (
            'id', 'transaction_time', 'client_secret', 'is_paid_online', 'printed_recipt', 'name', 'email', 'address', 'order_products', 'paid')
        extra_kwargs = {
            'id': {'read_only': True},
            'transaction_time': {'read_only': True}
        }
        
    def create(self, validated_data):
        order_products = validated_data.pop('order_products')
        validated_data['is_admin'] = True
        order = Order.objects.create(**validated_data)
        for element in order_products:
            OrderProduct.objects.create(order=order, **element)
        return order
        
class OrderCreateForUserSerializer(serializers.ModelSerializer):
    order_products = OrderProductSerializerUser(many=True)
    class Meta:
        model = Order
        fields = ('id', 'client_secret', 'is_paid_online', 'printed_recipt', 'name', 'email', 'address', 'is_admin', 'order_products', 'paid')
        extra_kwargs = {
            'name': {'required': True},
            'email': {'required': True}
        }
        
    def create(self, validated_data):
        order_product = validated_data.pop('order_products')
        if validated_data.get('client_secret', False):
            validated_data['is_paid_online'] = True
            validated_data['paid'] = True
        order = Order.objects.create(**validated_data)
        for element in order_product:
            keys = list(filter(lambda x: x in ["sell_price", "buy_price", "discount"], element.keys()))
            for key in keys:
                element.pop(key)
        for element in order_product:
            OrderProduct.objects.create(order=order, **element)
        return order
        
        
class OrderListSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField() 
    class Meta:
        model = Order
        fields = ('id', 'name', 'email', 'phone_number', 'address', 'paid', 'transaction_time', 'is_paid_online', 
                  'total_price')
        
    def get_total_price(self, obj):
        return OrderProduct.objects.filter(order=obj).aggregate(total_price=Sum('total_price')).get('total_price')
        
class OrderFilterSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    address = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
