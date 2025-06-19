from django.urls import path
from . import views

app_name = 'covoiturage'

urlpatterns = [

    path('trajets/', views.liste_trajets_view, name='liste_trajets'),
    path('trajets/creer/', views.creer_trajet, name='creer_trajet'),
    path('trajets/<int:trajet_id>/reserver/', views.reserver_trajet, name='reserver_trajet'),
    path('confirmation/<int:reservation_id>/', views.confirmation_reservation, name='confirmation_reservation'),
    path('publication/creer/', views.creer_publication, name='creer_publication'),
    path('messages/envoyer/<int:destinataire_id>/', views.envoyer_message, name='envoyer_message'),
    path('messages/reception/', views.boite_reception, name='boite_reception'),
    path('trajets/supprimer/<int:trajet_id>/', views.supprimer_trajet, name='supprimer_trajet'),
    path('publication/supprimer/<int:publication_id>/', views.supprimer_publication, name='supprimer_publication'),
    path('messages/nouveau/', views.nouveau_message, name='nouveau_message'),


]