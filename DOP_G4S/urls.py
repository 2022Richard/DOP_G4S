from django.urls import path
from . import views


app_name = 'DOP_G4S'

urlpatterns = [

    # all_tranche_deux_heures_2
   # path('all_tranche_2', views.all_tranche_deux_heures_2, name='all_tranche_deux_heures_2'), 


######################## URLS CORRECTES ########################    
 # Accueil
    path('', views.accueil, name='accueil'), 

    # Alarme --- Choix de la carte à afficher
    path('choix_carte', views.alarme, name='alarme'),
    # Contact 
    path('contact', views.contact, name='contact'), 

    # Gestion de tous les declenchements par zone
    path('carte_all', views.carte_all, name='carte_all'), 
    path('carte_all_htmx/<str:pk>', views.carte_all_htmx, name='carte_all_htmx'), 

    # Gestion de tous les declenchements par le Type de client
    path('Type_client', views.type_client, name='type_client'), 
    path('Type_client_htmx/<str:pk>', views.Type_client_htmx, name='Type_client_htmx'), 

    # Gestion de tous les declenchements dont les interventions sont justifiées
    path('inter_justifie', views.inter_justifie, name='inter_justifie'), 
    path('inter_justifie_htmx/<str:pk>', views.inter_justifie_htmx, name='inter_justifie_htmx'), 

    # Gestion de tous les declenchements avec les tranches de deux heures
    path('all_tranche_deux_heures', views.all_tranche_deux_heures, name='all_tranche_deux_heures'), 
    path('all_tranche_deux_heures_htmx/<str:pk>', views.all_tranche_deux_heures_htmx, name='all_tranche_deux_heures_htmx'), 
     

######################## URLS CORRECTES ########################  

     ]