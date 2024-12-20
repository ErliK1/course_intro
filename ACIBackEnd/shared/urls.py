from rest_framework_simplejwt import views as jwt_views

from django.urls import path
from django.urls import include

from shared.views import CreateACiAdminAPIView


urlpatterns = [
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', CreateACiAdminAPIView.as_view(), name='signup'),
]