from django.urls import path, include
from .views import RegisterView, ChangePasswordView, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='user_login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='user_register'),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='user_change_password'),
    path('reset_password/', include('django_rest_passwordreset.urls'), name='user_reset_password'),
    path('logout/', LogoutView.as_view(), name='user_logout'),
]