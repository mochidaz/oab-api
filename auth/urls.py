from django.urls import path

from .views import JwtObtain, RefreshToken

urlpatterns = [
    path('/login', JwtObtain.as_view(), name='login'),
    path('/refresh-token', RefreshToken.as_view(), name='refresh-token'),
]