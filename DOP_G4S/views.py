from django.shortcuts import render
import folium
from folium import plugins
import pandas as pd
from folium.plugins import MarkerCluster, Draw
import pandas as pd
import os

# Create your views here.



def accueil(request): 
    return render(request, 'accueil.html', {'etat':'accueil'})

def contact(request): 
    return render(request, 'contact.html', {'etat':'contact'})

def alarme(request): 
    #df = pd.read_excel("Carte_Alarme_new.xlsx")
    return render(request, 'alarme.html', {'etat':'Alarme'})

def declenchement_all(request): 
    
    carte_garde = "Carte_Alarme_new.xlsx"
    # m = folium.Map((5.37309, -3.99117), tooltip = "G4S Siege" , zoom_start=7)
    
    df = pd.read_excel(carte_garde)

    # Je construis la carte des sites : 

    map = folium.Map((5.37309, -3.99117), tooltip = "G4S Siege" , zoom_start=7)

    heure_decl = ["Boston", "Detroit", "Malibu", "Monaco", "Orleans", "Sydney"  ]
    #print(len(df))
    Boston = MarkerCluster(name = "Boston").add_to(map)
    Detroit = MarkerCluster(name = "Detroit").add_to(map)
    Malibu = MarkerCluster(name = "Malibu").add_to(map)
    Monaco = MarkerCluster(name = "Monaco").add_to(map)
    Orleans = MarkerCluster(name = "Orleans").add_to(map)
    Sydney = MarkerCluster(name = "Sydney").add_to(map)

    #couleur =    ["orange", "red",   "gray",   "purple", "blue", "green"]  
    #couleur =    ["orange", "red",   "gray",   "purple", "blue", "green"]

    cpt, = 0,

    for i in heure_decl :
        df_map = (df.loc[df['ZONE'] == i])
        # Selection des coordonnées pour la carte
        df_map_2 = df_map[['Latitude', 'Longitude']]

        # Convertir les colonnes en numerique
        df_map_2 = df_map_2.astype({'Latitude':'float','Longitude':'float'})

        liste = df_map_2.values.tolist()
        liste_taille = len(liste)

        #map = folium.Map(location=[lat_fixe, long_fixe], zoom_start=4)
        for point in range(0, liste_taille) :
            marker = folium.Marker(liste[point], tooltip = df_map.iloc[point, 2], icon  = folium.Icon(icon = "cloud"))

            if i == "Boston" : Boston.add_child(marker)
            elif i == "Detroit" : Detroit.add_child(marker)
            elif i == "Malibu" : Malibu.add_child(marker)
            elif i == "Monaco" : Monaco.add_child(marker)
            elif i == "Orleans" : Orleans.add_child(marker)
            elif i == "Sydney" : Sydney.add_child(marker)

    cpt += 1

    #folium.TileLayer('mapquestopen').add_to(m)
    folium.LayerControl().add_to(map)
    #plugins.Geocoder().add_to(map)
    
    folium.plugins.Fullscreen(
        position="topright",
        title="Expand me",
        title_cancel="Exit me",
        force_separate_button=True,
    ).add_to(map)
    
    Draw(export=True).add_to(map)

    return render(request, 'declenchement_all.html', {'etat':'garde', 'map' : map._repr_html_(), 'etat':'Garde'})


def situation_reelle(request): 
    # Situation réelle  
    carte_alarme = "Carte_Alarme_new.xlsx"

    # m = folium.Map((5.37309, -3.99117), tooltip = "G4S Siege" , zoom_start=7)
    
    df = pd.read_excel(carte_alarme)

    # Je construis la carte des sites : 

    map = folium.Map((5.37309, -3.99117), tooltip = "G4S Siege" , zoom_start=7)

    heure_decl = ["Bancaire", "Non Bancaire"]
        
    cpt, var, groupe = 0, "group", list()
    for i in (heure_decl) :
        cpt = cpt + 1
        groupe.append(var+str(cpt))

    cpt, = 0,
    couleur =    ["red", "blue"]

    for i in heure_decl :
        groupe[cpt] = folium.FeatureGroup(i).add_to(map)
        df_map = (df.loc[df['Situation reelle'] == i])

        # Selection des coordonnées pour la carte
        df_map_2 = df_map[['Latitude', 'Longitude']]

        # Convertir les colonnes en numerique
        df_map_2 = df_map_2.astype({'Latitude':'float','Longitude':'float'})

        liste = df_map_2.values.tolist()
        liste_taille = len(liste)

        #map = folium.Map(location=[lat_fixe, long_fixe], zoom_start=4)

        for point in range(0, liste_taille) :
            folium.Marker(liste[point], tooltip = df_map.iloc[point, 2], icon  = folium.Icon(icon = "cloud",color = couleur[cpt])).add_to(groupe[cpt])

        cpt += 1

    #folium.TileLayer('mapquestopen').add_to(m)
    folium.LayerControl().add_to(map)
    #plugins.Geocoder().add_to(map)
    
    folium.plugins.Fullscreen(
        position="topright",
        title="Expand me",
        title_cancel="Exit me",
        force_separate_button=True,
    ).add_to(map)
    
    Draw(export=True).add_to(map)
   
    #print(df)
    return render(request, 'situation_reelle.html', {'etat':'Alarme', 'map' : map._repr_html_(), })
    #return render(request, 'alarme.html', {'etat':'Alarme'})

""""
def secteur_activite(request): 

    carte_alarme = "Carte_Alarme.xlsx"

    # m = folium.Map((5.37309, -3.99117), tooltip = "G4S Siege" , zoom_start=7)
    
    df = pd.read_excel(carte_alarme)

    # Je construis la carte des sites : 

    map = folium.Map((5.37309, -3.99117), tooltip = "G4S Siege" , zoom_start=7)

    heure_decl = ["Bancaire", "Autre secteur"]
        
    cpt, var, groupe = 0, "group", list()
    for i in (heure_decl) :
        cpt = cpt + 1
        groupe.append(var+str(cpt))

    cpt, = 0,
    couleur =    ["red", "blue"]

    for i in heure_decl :
        groupe[cpt] = folium.FeatureGroup(i).add_to(map)
        df_map = (df.loc[df['Secteur'] == i])

        # Selection des coordonnées pour la carte
        df_map_2 = df_map[['Latitude', 'Longitude']]

        # Convertir les colonnes en numerique
        df_map_2 = df_map_2.astype({'Latitude':'float','Longitude':'float'})

        liste = df_map_2.values.tolist()
        liste_taille = len(liste)

        #map = folium.Map(location=[lat_fixe, long_fixe], zoom_start=4)

        for point in range(0, liste_taille) :
            folium.Marker(liste[point], tooltip = df_map.iloc[point, 1], icon  = folium.Icon(icon = "cloud",color = couleur[cpt])).add_to(groupe[cpt])

        cpt += 1

    #folium.TileLayer('mapquestopen').add_to(m)
    folium.LayerControl().add_to(map)
    #plugins.Geocoder().add_to(map)
    
    folium.plugins.Fullscreen(
        position="topright",
        title="Expand me",
        title_cancel="Exit me",
        force_separate_button=True,
    ).add_to(map)
    
    Draw(export=True).add_to(map)
   
    #print(df)
    return render(request, 'secteur_activite.html', {'etat':'Alarme', 'map' : map._repr_html_(), })
"""

def type_client(request): 

    carte_alarme = "Carte_Alarme_new.xlsx"

    # m = folium.Map((5.37309, -3.99117), tooltip = "G4S Siege" , zoom_start=7)
    
    df = pd.read_excel(carte_alarme)

    # Je construis la carte des sites : 

    map = folium.Map((5.37309, -3.99117), tooltip = "G4S Siege" , zoom_start=7)

    heure_decl = ["sensible", "Non sensible"]
        
    cpt, var, groupe = 0, "group", list()
    for i in (heure_decl) :
        cpt = cpt + 1
        groupe.append(var+str(cpt))

    cpt, = 0,
    couleur =    ["red", "blue"]

    for i in heure_decl :
        groupe[cpt] = folium.FeatureGroup(i).add_to(map)
        df_map = (df.loc[df['Client Sensible'] == i])

        # Selection des coordonnées pour la carte
        df_map_2 = df_map[['Latitude', 'Longitude']]

        # Convertir les colonnes en numerique
        df_map_2 = df_map_2.astype({'Latitude':'float','Longitude':'float'})

        liste = df_map_2.values.tolist()
        liste_taille = len(liste)

        #map = folium.Map(location=[lat_fixe, long_fixe], zoom_start=4)

        for point in range(0, liste_taille) :
            folium.Marker(liste[point], tooltip = df_map.iloc[point, 2], icon  = folium.Icon(icon = "cloud",color = couleur[cpt])).add_to(groupe[cpt])

        cpt += 1

    #folium.TileLayer('mapquestopen').add_to(m)
    folium.LayerControl().add_to(map)
    #plugins.Geocoder().add_to(map)
    
    folium.plugins.Fullscreen(
        position="topright",
        title="Expand me",
        title_cancel="Exit me",
        force_separate_button=True,
    ).add_to(map)
    
    Draw(export=True).add_to(map)
   
    #print(df)
    return render(request, 'type_client.html', {'etat':'Alarme', 'map' : map._repr_html_(), })



def all_tranche_deux_heures(request): 

    carte_alarme = "Carte_Alarme_new.xlsx"

    # m = folium.Map((5.37309, -3.99117), tooltip = "G4S Siege" , zoom_start=7)
    
    df = pd.read_excel(carte_alarme)

    # Je construis la carte des sites : 

    map = folium.Map((5.37309, -3.99117), tooltip = "G4S Siege" , zoom_start=7)

    heure_decl = ["00H - 02H","02H - 04H", "04H - 06H", "06H - 08H", "08H - 10H", "10H - 12H", "12H - 14H", "14H - 16H", "16H - 18H", "18H - 20H", "20H - 22H", "22H - 00H"]
        
    cpt, var, groupe = 0, "group", list()
    for i in (heure_decl) :
        cpt = cpt + 1
        groupe.append(var+str(cpt))

    cpt, = 0,
    #couleur =    ["red", "blue"]

    for i in heure_decl :
        groupe[cpt] = folium.FeatureGroup(i).add_to(map)
        df_map = (df.loc[df['Heure Decl'] == i])

        # Selection des coordonnées pour la carte
        df_map_2 = df_map[['Latitude', 'Longitude']]

        # Convertir les colonnes en numerique
        df_map_2 = df_map_2.astype({'Latitude':'float','Longitude':'float'})

        liste = df_map_2.values.tolist()
        liste_taille = len(liste)

        #map = folium.Map(location=[lat_fixe, long_fixe], zoom_start=4)

        for point in range(0, liste_taille) :
            folium.Marker(liste[point], tooltip = df_map.iloc[point, 2], icon  = folium.Icon(icon = "cloud",color = "blue")).add_to(groupe[cpt])

        cpt += 1

    folium.LayerControl().add_to(map)
    #plugins.Geocoder().add_to(map)
    
    folium.plugins.Fullscreen(
        position="topright",
        title="Expand me",
        title_cancel="Exit me",
        force_separate_button=True,
    ).add_to(map)
    
    Draw(export=True).add_to(map)
   
    #print(df)
    return render(request, 'tranche_deux_heures.html', {'etat':'Alarme', 'map' : map._repr_html_(), })


def all_tranche_deux_heures_2(request): 
    
    carte_garde = "Carte_Alarme_new.xlsx"
    # m = folium.Map((5.37309, -3.99117), tooltip = "G4S Siege" , zoom_start=7)
    
    df = pd.read_excel(carte_garde)

    # Je construis la carte des sites : 

    map = folium.Map((5.37309, -3.99117), tooltip = "G4S Siege" , zoom_start=7)

    heure_decl = ["00H - 02H","02H - 04H", "04H - 06H", "06H - 08H", "08H - 10H", "10H - 12H", "12H - 14H", "14H - 16H", "16H - 18H", "18H - 20H", "20H - 22H", "22H - 00H"]
     
    #print(len(df))
    Boston = MarkerCluster(name = "00H - 02H").add_to(map)
    Detroit = MarkerCluster(name = "02H - 04H").add_to(map)
    Malibu = MarkerCluster(name = "04H - 06H").add_to(map)
    Monaco = MarkerCluster(name = "06H - 08H").add_to(map)
    Orleans = MarkerCluster(name = "08H - 10H").add_to(map)
    Sydney = MarkerCluster(name = "10H - 12H").add_to(map)
    Boston_2 = MarkerCluster(name = "12H - 14H").add_to(map)
    Detroit_2 = MarkerCluster(name = "14H - 16H").add_to(map)
    Malibu_2 = MarkerCluster(name = "16H - 18H").add_to(map)
    Monaco_2 = MarkerCluster(name = "18H - 20H").add_to(map)
    Orleans_2 = MarkerCluster(name = "20H - 22H").add_to(map)
    Sydney_2 = MarkerCluster(name = "22H - 00H").add_to(map)

    #couleur =    ["orange", "red",   "gray",   "purple", "blue", "green"]  
    #couleur =    ["orange", "red",   "gray",   "purple", "blue", "green"]

    cpt, = 0,

    for i in heure_decl :
        df_map = (df.loc[df['Heure Decl'] == i])
        # Selection des coordonnées pour la carte
        df_map_2 = df_map[['Latitude', 'Longitude']]

        # Convertir les colonnes en numerique
        df_map_2 = df_map_2.astype({'Latitude':'float','Longitude':'float'})

        liste = df_map_2.values.tolist()
        liste_taille = len(liste)

        #map = folium.Map(location=[lat_fixe, long_fixe], zoom_start=4)
        for point in range(0, liste_taille) :
            marker = folium.Marker(liste[point], tooltip = df_map.iloc[point, 2], icon  = folium.Icon(icon = "cloud"))

            if i == "00H - 02H" : Boston.add_child(marker)
            elif i == "02H - 04H" : Detroit.add_child(marker)
            elif i == "04H - 06H" : Malibu.add_child(marker)
            elif i == "06H - 08H" : Monaco.add_child(marker)
            elif i == "08H - 10H" : Orleans.add_child(marker)
            elif i == "10H - 12H" : Sydney.add_child(marker)
            if i == "12H - 14H" : Boston_2.add_child(marker)
            elif i == "14H - 16H" : Detroit_2.add_child(marker)
            elif i == "16H - 18H" : Malibu_2.add_child(marker)
            elif i == "18H - 20H" : Monaco_2.add_child(marker)
            elif i == "20H - 22H" : Orleans_2.add_child(marker)
            elif i == "22H - 00H" : Sydney_2.add_child(marker)

    cpt += 1

    #folium.TileLayer('mapquestopen').add_to(m)
    folium.LayerControl().add_to(map)
    #plugins.Geocoder().add_to(map)
    
    folium.plugins.Fullscreen(
        position="topright",
        title="Expand me",
        title_cancel="Exit me",
        force_separate_button=True,
    ).add_to(map)
    
    Draw(export=True).add_to(map)

    return render(request, 'tranche_deux_heures_2.html', {'etat':'garde', 'map' : map._repr_html_(), 'etat':'Garde'})
