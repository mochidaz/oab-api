"""
URL configuration for oab_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from users.urls import cms_urlpatterns as user_cms_urls, public_urlpatterns as user_public_urls
from auth.urls import urlpatterns as auth_urls

urlpatterns = [
    path('api', include([
        path('/cms', include([
            path('/users', include(user_cms_urls))
        ])),

        path('/public', include([
            path('/users', include(user_public_urls))
        ])),

        path('/auth', include(auth_urls))
    ])),

]
