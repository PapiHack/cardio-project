from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name="cardioadmin.home"),
    path('login', views.connexion, name="cardioadmin.connexion"),
    path('logout', views.deconnexion, name="cardioadmin.deconnexion"),
    path('forgot', views.forgot, name="cardioadmin.forgot"),
]
