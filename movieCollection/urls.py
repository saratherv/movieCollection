"""movieCollection URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url
from core.views import *



urlpatterns = [
    url(r'^register', UserLoginView.as_view(), name="register"),
    url(r'^movies', MoviesAPIView.as_view()),
    url(r'^collection/(?P<pk>[0-9A-Fa-f-]+)$', CollectionView.as_view()),
    url(r'^collection/$', CollectionListView.as_view(), name="collectionList"),
    url(r'^request-count', RequestCounterView.as_view()),
    url(r'^request-count/reset', RequestCounterView.as_view()),
    
]
