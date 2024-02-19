from django.urls import path
from .views import UserRegistrationView, UserLoginView
from rest_framework_simplejwt.authentication import JWTAuthentication

app_name = 'authentication'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
]