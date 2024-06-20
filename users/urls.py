from django.urls import path

from .views import UserViewSet, PublicUserViewSet

public_urlpatterns = [
    path('', PublicUserViewSet.as_view({'get': 'list'})),
]

cms_urlpatterns = [
    path('', UserViewSet.as_view({'get': 'list', 'post': 'create', 'patch': 'partial_update', 'delete': 'destroy'})),
]