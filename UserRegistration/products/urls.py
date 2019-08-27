from django.urls import path, include
from rest_framework import routers

from .views import ProductsViewSet

app_name = 'products'
router = routers.DefaultRouter()
router.register(r'products', ProductsViewSet)
urlpatterns = [
    path(r'', include(router.urls)),
]

