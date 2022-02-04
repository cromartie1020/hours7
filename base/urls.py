from django.urls import path
from . import views
urlpatterns = [
    path('', views.room, name='room'),
    path('<int:pk>/', views.room_detail, name='detail'),
    path('create/', views.createRoom, name='create'),
    path('update/<int:pk>/', views.updateRoom, name='update'),
    path('delete/<int:pk>/', views.deleteRoom, name='delete'),
    path('confirm/<int:pk>/', views.deleteConfirm, name='confirm'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),




]
