
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logOut, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('room/<str:pk>/', views.room, name='room'),
    path('profile/<str:pk>', views.userProfile, name='user-profile'),
    path('create-room', views.create_room, name='create-room'),
    path('update-room/<str:pk>/', views.update_room, name='update-room'),
    path('delete-room/<str:pk>/', views.delete_room, name='delete-room'),
    path('delete-message/<str:pk>/', views.deleteMessage, name='delete-message')
]
