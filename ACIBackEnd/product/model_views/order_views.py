from rest_framework.response import Response
from rest_framework import status

from django.http import Http404
from django.db.models import Sum, F, Q, Subquery, OuterRef

from django.db import transaction


from product.model_serializers.order_serializers import OrderCreateForAdminSerializer, OrderCreateForUserSerializer, OrderFilterSerializer, OrderListSerializer
from shared.views import ACICreateAPIView, ACIListAPIView, ACIListCreateAPIView
from product.models import Order, Product, OrderProduct
from shared.constants import *
from product.utils import check_if_user_is_admin, \
get_the_last_part_of_date_key, parse_string_to_date, get_keys_that_contains_date, SQL_FOR_ORDER_TRANSACTION_PRICE

from datetime import datetime




class OrderListFromManagerAPIView(ACIListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    filter_map = {
        'name': 'name',
        'email': 'email',
        'address': 'address',
        'phone_number': 'phone_number',
         
    }
    filter_serializer_class = OrderFilterSerializer

    def get_queryset(self, ):
        list_of_transaction_keys = get_keys_that_contains_date(self.request.query_params.keys())
        query_set = super().get_queryset()
        queryset = self.prepare_queryset_for_date(query_set, list_of_transaction_keys)
        query_set = self.prepare_queryset_for_total_sum(query_set)
        return query_set 
        
    def prepare_queryset_for_total_sum(self, query_set):
        max_price = self.request.query_params.get('max_price')
        min_price = self.request.query_params.get('min_price')
        order_products = OrderProduct.objects.values('order').annotate(total_sum_req=Sum('total_price'))
        args = []
        if max_price:
            order_products = order_products.filter(total_sum_req__lte=float(max_price))
            args.append(self.prepare_args(order_products))
        if min_price:
            order_products = order_products.filter(total_sum_req__gte=float(min_price))
            args.append(self.prepare_args(order_products))
        query_set = query_set.filter(*args)
        return query_set 

    def prepare_args(self, order_products):
        return Q(id__in=order_products.values_list('order_id', flat=True))
    
    def prepare_queryset_for_date(self, query_set, list_of_transaction_keys):
        for element in list_of_transaction_keys:
            last_part = get_the_last_part_of_date_key(element)
            transaction_date = parse_string_to_date(self.request.query_params.get(element))
            data = {
                'transaction_time__' + last_part: transaction_date 
            }
            query_set = query_set.filter(Q(**data))
        return query_set
    
    
    
    
            

class OrderCreateAPIView(ACICreateAPIView):
    queryset = Order.objects.all()
    
    def get_serializer_class(self):
        if check_if_user_is_admin(request=self.request):
            OrderCreateForAdminSerializer
        return OrderCreateForUserSerializer
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if (serializer.data.get('printed_receipt')):
            pass
        return Response({MESSAGE: 'Kerkesa U be Me Sukses!'}, status=status.HTTP_201_CREATED)
            

