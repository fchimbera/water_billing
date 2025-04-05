from django.urls import path
from .views import UserRegistrationAPIView, UserLoginAPIView, UserProfileAPIView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register-api'),
    path('login/', UserLoginAPIView.as_view(), name='login-api'),
    path('profile/', UserProfileAPIView.as_view(), name='profile-api'),
]