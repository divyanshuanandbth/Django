from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('users/', views.users_list_view, name='users_list'),  # Users List Page
    path('user/<int:pk>/', views.user_detail_view, name='user_detail'),  # User Detail Page
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),  # Logout route
]