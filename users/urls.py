from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('list/', views.users_list, name='list'),
    path('<int:user_id>/', views.user_profile, name='profile'),
    path('<int:user_id>/edit/', views.edit_profile, name='edit_profile'),
    path('<int:user_id>/change-password/',
         views.change_password, name='change_password'),
]
