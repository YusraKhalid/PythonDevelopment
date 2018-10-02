from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'user'

urlpatterns = [
    path('', views.IndexDetailView.as_view(), name='index'),
    path('login/', auth_views.LoginView.as_view(
        redirect_authenticated_user=True,
        template_name='user/registration/login.html'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.UserFormView.as_view(), name='register'),
    path('update/profile/', views.ProfileUpdate.as_view(), name='edit_profile'),
    path('update/user/', views.UserUpdate.as_view(), name='edit_basic_info'),
    path('update/user/complete', views.update_profile, name='edit_all_info'),
]
