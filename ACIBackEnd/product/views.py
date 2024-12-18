from django.shortcuts import render


from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView

from shared.views import ACIListAPIView


from product.models import Product, OrderProduct
from product.serializers import ProductListFilterSerializer

from product.model_serializers.product_serializers import ProductListSerializer
# Create your views here.

from functools import reduce


class ProductListAPIView(ACIListAPIView):
    serializer_class = ProductListSerializer 
    filter_map = {
            'category': 'product_categories__category__id',
            'brand': 'brand__id',
            'name': 'name',
            'discount': 'has_discount',
        }
    sort_map = {
        'popularity': 'product_popularities__count',
        'name': 'name',
        }
    filter_serializer_class = ProductListFilterSerializer


    def get_queryset(self, ):     
        if self.request.query_params.get('price') and self.request.query_params.get('price').is_numeric():
            price = float(self.request.query_params.get('price'))
            popularity_queryset = Product.objects.filter(sell_price__lte=price, deleted=False)
        else:
            popularity_queryset = Product.objects.filter(deleted=False)
        return popularity_queryset


