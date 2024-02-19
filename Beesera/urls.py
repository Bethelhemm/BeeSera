
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.authentication import JWTAuthentication

urlpatterns = [
    path('admin/', admin.site.urls),
     path('api/auth/', include('authentication.urls')),
]
