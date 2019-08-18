from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name="cardioadmin.home"),
    path('login', views.login, name="cardioadmin.login"),
    path('logout', views.deconnexion, name="cardioadmin.deconnexion"),
    path('forgot', views.forgot, name="cardioadmin.forgot"),
]
