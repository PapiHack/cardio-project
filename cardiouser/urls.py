from django.urls import path
from . import views

urlpatterns = [
    path('login', views.connexion, name="cardiouser.connexion"),
    path('home', views.home, name="cardiouser.home"),
    path('logout', views.deconnexion, name="cardiouser.deconnexion"),
    path('forgot', views.forgot, name="cardiouser.forgot"),
    path('register', views.register, name="cardiouser.register"),
    path('mon_profil', views.profil, name="cardiouser.profil"),
    path('update_user/<int:id>', views.update_user, name="cardiouser.update_user"),
    path('input_data', views.input_data, name="cardiouser.input_data"),
    path('analyze_data', views.upload_and_analyze, name="cardiouser.upload_and_analyze"),
]
