from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name="cardiouser.login"),
    path('home', views.home, name="cardiouser.home"),
    path('logout', views.deconnexion, name="cardiouser.deconnexion"),
    path('forgot', views.forgot, name="cardiouser.forgot"),
    path('register', views.register, name="cardiouser.register"),
]
