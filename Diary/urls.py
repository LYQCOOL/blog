"""Diary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from app import views
#定制url,通过url到views中匹配相应函数，并返回相应html，呈现
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('register/', views.register),
    path('diaries/',views.diary),
    path('add/',views.add),
    path('show/',views.show),
    path('edit/',views.edit),
    path('change/',views.change),
]
