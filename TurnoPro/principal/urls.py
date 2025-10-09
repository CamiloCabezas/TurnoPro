from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from .views import get_movimientos, CustomTokenObtainPairView, set_rol, CustomRefreshTokenView,delete_user, logout, is_authenticated, register


urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomRefreshTokenView.as_view(), name='token_refresh'),
    path('movimientos/', get_movimientos),
    path('set_rol/<int:id>/',set_rol),
    path('logout/',logout),
    path('isAuthenticated/', is_authenticated),
    path('register/', register), 
    path('delete/<int:id>/', delete_user)
]
