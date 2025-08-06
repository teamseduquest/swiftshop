from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
  path('login/', views.user_login, name='login-user'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    
      path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/user/', views.user_dashboard, name='user_dashboard'),
    path('create-admin/', views.create_superuser),
]
