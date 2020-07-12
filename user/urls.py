from django.urls import path
from . import views


urlpatterns = [
    path('user/login/', views.register, name='user-login'),
    path('user/register/', views.register, name='user-register'),
    path('user/<int:id>/follow', views.follow, name='user-follow'),
    path('user/<int:id>/unfollow', views.unfollow, name='user-unfollow'),
]

