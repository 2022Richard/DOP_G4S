from django.urls import path
from . import views


app_name = 'DOP_G4S'

urlpatterns = [

    # Accueil
    path('', views.accueil, name='accueil'), 

    # Alarme
    path('choix_carte', views.alarme, name='alarme'),

    # Declen. All
    path('all', views.declenchement_all, name='declenchement_all'), 

    # Situation réelle
    path('alarme', views.situation_reelle, name='situation_reelle'), 

    # Type de Client
    path('Type_client', views.type_client, name='type_client'), 

    # all_tranche_deux_heures
    path('all_tranche_deux_heures', views.all_tranche_deux_heures, name='all_tranche_deux_heures'), 

    # all_tranche_deux_heures_2
    path('all_tranche_2', views.all_tranche_deux_heures_2, name='all_tranche_deux_heures_2'), 

    # Contact 
    path('contact', views.contact, name='contact'), 

     ]