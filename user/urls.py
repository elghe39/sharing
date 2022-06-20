from django.urls import path, include
from .views import MyObtainTokenPairView, RegisterView, ChangePasswordView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='user_register'),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='user_change_password'),
    path('password_reset/', include('django_rest_passwordreset.urls'), name='user_reset_password'),
]