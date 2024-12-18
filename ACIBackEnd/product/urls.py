from django.urls import path
from django.urls import include

from product.model_views.order_views import OrderCreateAPIView, OrderListFromManagerAPIView
from product.model_views.product_views import ProductCreateAPIView, CategoryCreateListAPIView, BrandCreateListAPIView, ProductUpdateAPIView, ProductInsertDiscountView
from product.url_constans import *
from product.views import ProductListAPIView

urlpatterns = [
    path('list/', ProductListAPIView.as_view(), name=PRODUCT_LIST),
    path('create/', ProductCreateAPIView.as_view(), name=PRODUCT_CREATE),
    path('update/', ProductUpdateAPIView.as_view(), name=PRODUCT_UPDATE),
    path('category/list/create/', CategoryCreateListAPIView.as_view(), name=CATEGORY_LIST_CREATE),
    path('brand/list/create/', BrandCreateListAPIView.as_view(), name=BRAND_LIST_CREATE),
    path('order/create/', OrderCreateAPIView.as_view(), name=ORDER_CREATE),
    path('order/list/', OrderListFromManagerAPIView.as_view(), name=ORDER_LIST),
    path('discount/set/', ProductInsertDiscountView.as_view())
    
] 
