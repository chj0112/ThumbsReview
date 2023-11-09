"""
URL configuration for django_review project.

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
from django.urls import path

from search import views

urlpatterns = [
    path('', views.main),
    path('base', views.base),
    path('list', views.list, name='list'),
    path('info', views.info),
    path('test', views.test),
    path('kakao', views.kakao),
    path('<int:store_id>', views.store),
    path('model-test', views.model_test, name='model_test')
]
