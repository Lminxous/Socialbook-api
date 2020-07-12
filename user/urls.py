from django.urls import path
from . import views


urlpatterns = [
    path('user/login/', views.register, name='user-login'),
    path('user/register/', views.register, name='user-register'),
]

