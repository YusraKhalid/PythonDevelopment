"""django_saloon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('customer/', include('customer.urls')),
    path('shop/', include('shop.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', core_views.LogoutView.as_view(), name='logout'),
    path('register/', core_views.UserRegisterView.as_view(), name='register'),

    path('api/login/', core_views.UserLoginApiView.as_view(), name='api_login'),
    path('api/register/', core_views.UserRegisterationApiView.as_view(),
         name='api_register'),
    path('api/logout/', core_views.UserLogoutApiView.as_view(), name='api_logout'),

    url(r'^', TemplateView.as_view(template_name="index.html")),

]