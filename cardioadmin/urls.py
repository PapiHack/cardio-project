from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name="cardioadmin.home"),
    path('login', views.connexion, name="cardioadmin.connexion"),
    path('logout', views.deconnexion, name="cardioadmin.deconnexion"),
    path('forgot', views.forgot, name="cardioadmin.forgot"),
    path('gestion_admin', views.gestion_admin, name="cardioadmin.gestion_admin"),
    path('gestion_user', views.gestion_user, name="cardioadmin.gestion_user"),
    path('sup_user/<int:id>', views.supprimer_user, name="cardioadmin.supprimer_user"),
    path('edit_user/<int:id>', views.edit_user, name="cardioadmin.edit_user"),
    path('update_user/<int:id>', views.update_user, name="cardioadmin.update_user"),
    path('ajout_user/<str:user>', views.ajout_user, name="cardioadmin.ajout_user"),
    path('add_user/', views.add_user, name="cardioadmin.add_user"),
    path('mon_profil/', views.profil, name="cardioadmin.profil"),
]
