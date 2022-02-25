from django.conf.urls import include, url
from django.urls import path
from django.contrib import admin
from . import views
urlpatterns = [
    path('base', views.base, name='base'),
    path('index', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('account', views.account, name='account'),
]