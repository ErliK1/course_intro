from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from main.views.visitor_views import RegisterVisitorAPIView, VisitorRetrieveAPIView, \
                    VisitorListAPIView
from main.views.manager_views import ManagerRegisterAPIView, ManagerRetrieveAPIView


urlpatterns = [
        path('api/token/', TokenObtainPairView.as_view(), name='token-access'),
        path('api/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
        path('visitor/register/', RegisterVisitorAPIView.as_view(), name="register-visitor"),
        path('manager/register/', ManagerRegisterAPIView.as_view(), name='register-manager'),
        path('manager/retrieve/', ManagerRetrieveAPIView.as_view(), name='manager-retrieve'),
        path('visitor/retrieve/<int:pk>/', VisitorRetrieveAPIView.as_view(), name='visitor-retrieve'),
        path('visitor/list/', VisitorListAPIView.as_view(), name='visitor-list'),

    ]
