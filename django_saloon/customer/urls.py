"""customer urls module.
"""
from django.urls import path

from .views import Register, Profile, ReservationsListView

urlpatterns = [
    path('register/', Register.as_view(), name='customer_register'),
    path('profile/', Profile.as_view(), name='customer_profile'),
    path('myreservations/', ReservationsListView.as_view(),
         name='customer_reservations')
]
