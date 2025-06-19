from django.urls import path, include
from .views import connexion_view, inscription_view, bienvenue_view
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [

    #Afficher la page d'acceuil par defaut

    path('', bienvenue_view, name="bienvenue"), 
    path('connexion/', views.connexion_view, name='connexion'),
    path('inscription/', views.inscription_view, name='inscription'),
    path('page_utilisateur/', views.page_utilisateur_view, name='page_utilisateur'),

    #url pour les publications,trajets et les messages privés

    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
    path('profil/', views.profil_view, name='profil'),

]