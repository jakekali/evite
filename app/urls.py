from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('myEvents/', views.myEvents, name='myEvents'),
    path('authenticate/', views.authenticate, name='authenticate'),
]