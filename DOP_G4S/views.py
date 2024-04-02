from django.shortcuts import render
import folium
from folium import plugins
import pandas as pd
from folium.plugins import MarkerCluster, Draw
import pandas as pd
import os
from django.http import Http404, HttpResponse
import leafmap

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


##############################" DEBUT : GESTION DES DECLENCHEMENT AVEC INTERVENTIONS JUSTIFIEES" ##############################
def inter_justifie(request): 
    # Situation réelle  
    carte_alarme = "Carte_Alarme_new.xlsx"

    df = pd.read_excel(carte_alarme)

    # Je construis la carte des sites : 
    map = folium.Map((5.37309, -3.99117), tooltip = "G4S Siege" , zoom_start=7)

    situation_reelle = ["Bancaire", "Non Bancaire"] 

    df = df[df['Situation reelle'].isin(situation_reelle)] 

    # Je construis la carte ici : 
    cluster = MarkerCluster(name = "Donnees").add_to(map) 

    # Selection des coordonnées pour la carte
    df_map_2 = df[['Latitude', 'Longitude']]

    # Convertir les colonnes en numerique
    df_map_2 = df_map_2.astype({'Latitude':'float','Longitude':'float'})

    liste = df_map_2.values.tolist()
    liste_taille = len(liste)

    #map = folium.Map(location=[lat_fixe, long_fixe], zoom_start=4)
    for point in range(0, liste_taille) :  
        html = '''
                <b> Type declench : </b> {} <br>
                <b> Date : </b> {} <br>
                <b> Heure : </b>{} <br>
                <b> Code Alarme : </b>{} <br>
                <b> Type Client : </b>{}
            '''.format(df.iloc[point, 0], df.iloc[point, 1],df.iloc[point, 2], df.iloc[point, 3],df.iloc[point, 13] )
        popup = folium.Popup(html, max_width=1000)
        marker = folium.Marker(liste[point], popup = popup, tooltip = df.iloc[point, 6], icon  = folium.Icon(icon = "cloud"))
        marker.add_to(cluster)

    #return render(request, 'carte_all.html',{'map': map._repr_html_()} )
    return render(request, 'inter_justifie.html', {'map' : map._repr_html_(), })


def inter_justifie_htmx(request, pk): 
     
    df = pd.read_excel("Carte_Alarme_new.xlsx")
    #texte = " Je suis là"

    situation_reelle = ["Bancaire", "Non Bancaire"] 
    df = df[df['Situation reelle'].isin(situation_reelle)] 

    zone = {"0": "Bancaire", "1": "Non Bancaire"}
    map = folium.Map((5.37309, -3.99117), tooltip = "G4S Siege" , zoom_start=5)

    # Je recupère les choix de l'utilisateur
    choix = pk.strip()
    if choix == "aucun" :
        #map = folium.Map((5.327098119322325, -3.94640170570424), tooltip = "G4S Siege" , zoom_start=7)
        return HttpResponse(f'{map._repr_html_()}')  
        #print(choix)
    else :
        #df_choix = df
        zone_choisie = []
        for ch in choix : 
        # ch = int(ch)
            zone_choisie.append(zone[ch])
            #print(zone_choisie)
            #print(zone[ch])
            #print(type(ch))

        df_choix = df[df['Situation reelle'].isin(zone_choisie)]     

        cluster = MarkerCluster(name = "Donnees").add_to(map) 

        # Selection des coordonnées pour la carte
        df_map_2 = df_choix[['Latitude', 'Longitude']]

        # Convertir les colonnes en numerique
        df_map_2 = df_map_2.astype({'Latitude':'float','Longitude':'float'})

        liste = df_map_2.values.tolist()
        liste_taille = len(liste)

            #map = folium.Map(location=[lat_fixe, long_fixe], zoom_start=4) 
        for point in range(0, liste_taille) :
            html = '''
                <b> Type declench : </b> {} <br>
                <b> Date : </b> {} <br>
                <b> Heure : </b>{} <br>
                <b> Code Alarme : </b>{} <br>
                <b> Type Client : </b>{}
                    '''.format(df_choix.iloc[point, 0], df_choix.iloc[point, 1],df_choix.iloc[point, 2], df_choix.iloc[point, 3],df_choix.iloc[point, 13] )
            popup = folium.Popup(html, max_width=1000)
            marker = folium.Marker(liste[point], popup=popup,tooltip = df_choix.iloc[point, 6], icon  = folium.Icon(icon = "cloud"))
            marker.add_to(cluster)
        
        #return render(request, 'exemple.html',{'texte':texte} )
        return HttpResponse(f'{map._repr_html_()}') 

############################## FIN : GESTION DES DECLENCHEMENTS AVEC INTERVENTONS JUSTIFEES #################################
  
############################## DEBUT : GESTION DES DECLENCHEMENTS PAR LE TYPE DE CLIENT ##################################
def type_client(request): 

    carte_alarme = "Carte_Alarme_new.xlsx"

    # m = folium.Map((5.37309, -3.99117), tooltip = "G4S Siege" , zoom_start=7)
    
    df = pd.read_excel(carte_alarme)

    type_client = ["sensible", "Non sensible"]

    df = df[df['Client Sensible'].isin(type_client)] 

    # Je construis la carte ici : 
    map = folium.Map((5.37309, -3.99117), tooltip = "G4S Siege" , zoom_start=5)

    cluster = MarkerCluster(name = "Donnees").add_to(map) 

    # Selection des coordonnées pour la carte
    df_map_2 = df[['Latitude', 'Longitude']]

    # Convertir les colonnes en numerique
    df_map_2 = df_map_2.astype({'Latitude':'float','Longitude':'float'})

    liste = df_map_2.values.tolist()
    liste_taille = len(liste)

    #map = folium.Map(location=[lat_fixe, long_fixe], zoom_start=4)
    for point in range(0, liste_taille) :  
        html = '''
                <b> Type declench : </b> {} <br>
                <b> Date : </b> {} <br>
                <b> Heure : </b>{} <br>
                <b> Code Alarme : </b>{} <br>
                <b> Type Client : </b>{}
            '''.format(df.iloc[point, 0], df.iloc[point, 1],df.iloc[point, 2], df.iloc[point, 3],df.iloc[point, 13] )
        popup = folium.Popup(html, max_width=1000)
        marker = folium.Marker(liste[point], popup = popup, tooltip = df.iloc[point, 6], icon  = folium.Icon(icon = "cloud"))
        marker.add_to(cluster)

    #return render(request, 'carte_all.html',{'map': map._repr_html_()} )
    return render(request, 'type_client.html', {'map' : map._repr_html_(), })


def Type_client_htmx(request, pk): 
     
    df = pd.read_excel("Carte_Alarme_new.xlsx")
    #texte = " Je suis là"
    type_client = ["sensible", "Non sensible"]
    df = df[df['Client Sensible'].isin(type_client)] 

    zone = {"0": "sensible", "1": "Non sensible"}
    map = folium.Map((5.37309, -3.99117), tooltip = "G4S Siege" , zoom_start=5)

    # Je recupère les choix de l'utilisateur
    choix = pk.strip()
    if choix == "aucun" :
        #map = folium.Map((5.327098119322325, -3.94640170570424), tooltip = "G4S Siege" , zoom_start=7)
        return HttpResponse(f'{map._repr_html_()}')  
        #print(choix)
    else :
        #df_choix = df
        zone_choisie = []
        for ch in choix : 
        # ch = int(ch)
            zone_choisie.append(zone[ch])
            #print(zone_choisie)
            #print(zone[ch])
            #print(type(ch))

        df_choix = df[df['Client Sensible'].isin(zone_choisie)]     

        cluster = MarkerCluster(name = "Donnees").add_to(map) 

        # Selection des coordonnées pour la carte
        df_map_2 = df_choix[['Latitude', 'Longitude']]

        # Convertir les colonnes en numerique
        df_map_2 = df_map_2.astype({'Latitude':'float','Longitude':'float'})

        liste = df_map_2.values.tolist()
        liste_taille = len(liste)

            #map = folium.Map(location=[lat_fixe, long_fixe], zoom_start=4) 
        for point in range(0, liste_taille) :
            html = '''
                <b> Type declench : </b> {} <br>
                <b> Date : </b> {} <br>
                <b> Heure : </b>{} <br>
                <b> Code Alarme : </b>{} <br>
                <b> Type Client : </b>{}
                    '''.format(df_choix.iloc[point, 0], df_choix.iloc[point, 1],df_choix.iloc[point, 2], df_choix.iloc[point, 3],df_choix.iloc[point, 13] )
            popup = folium.Popup(html, max_width=1000)
            marker = folium.Marker(liste[point], popup=popup,tooltip = df_choix.iloc[point, 6], icon  = folium.Icon(icon = "cloud"))
            marker.add_to(cluster)
        
        #return render(request, 'exemple.html',{'texte':texte} )
        return HttpResponse(f'{map._repr_html_()}') 

  
############################## FIN : GESTION DES DECLENCHEMENTS PAR LE TYPE DE CLIENT ##################################


############################## DEBUT : GESTION DES DECLENCHEMENTS PAR DES TRANCHES DE DEUX HEURES ##################################  
def all_tranche_deux_heures(request): 

    carte_alarme = "Carte_Alarme_new.xlsx"

    # m = folium.Map((5.37309, -3.99117), tooltip = "G4S Siege" , zoom_start=7)
    
    df = pd.read_excel(carte_alarme)

    # Je construis la carte des sites : 

    map = folium.Map((5.37309, -3.99117), tooltip = "G4S Siege" , zoom_start=5)

    
    cluster = MarkerCluster(name = "Donnees").add_to(map) 

    # Selection des coordonnées pour la carte
    df_map_2 = df[['Latitude', 'Longitude']]

    # Convertir les colonnes en numerique
    df_map_2 = df_map_2.astype({'Latitude':'float','Longitude':'float'})

    liste = df_map_2.values.tolist()
    liste_taille = len(liste)

    #map = folium.Map(location=[lat_fixe, long_fixe], zoom_start=4)
    for point in range(0, liste_taille) :  
        html = '''
                <b> Type declench : </b> {} <br>
                <b> Date : </b> {} <br>
                <b> Heure : </b>{} <br>
                <b> Code Alarme : </b>{} <br>
                <b> Type Client : </b>{}
            '''.format(df.iloc[point, 0], df.iloc[point, 1],df.iloc[point, 2], df.iloc[point, 3],df.iloc[point, 13] )
        popup = folium.Popup(html, max_width=1000)
        marker = folium.Marker(liste[point], popup = popup, tooltip = df.iloc[point, 6], icon  = folium.Icon(icon = "cloud"))
        marker.add_to(cluster)

    return render(request, 'tranche_deux_heures.html',{'map': map._repr_html_()} )


def all_tranche_deux_heures_htmx(request, pk): 
     
    df = pd.read_excel("Carte_Alarme_new.xlsx")
    #texte = " Je suis là"

    zone = {"1":"00H - 02H", "2":"02H - 04H", "3":"04H - 06H", "4":"06H - 08H", "5":"08H - 10H", "6":"10H - 12H", "7":"12H - 14H", "8":"14H - 16H", "9":"16H - 18H", "10":"18H - 20H", "11":"20H - 22H", "12":"22H - 00H"} 

    #zone = {"0": "Boston", "1": "Detroit", "2": "Malibu", "3": "Monaco", "4": "Orleans", "5": "Sydney", }
    map = folium.Map((5.37309, -3.99117), tooltip = "G4S Siege" , zoom_start=5)

    # Je recupère les choix de l'utilisateur
    choix = pk.strip()
    print(choix)
    if choix == "aucun" :
        #map = folium.Map((5.327098119322325, -3.94640170570424), tooltip = "G4S Siege" , zoom_start=7)
        return HttpResponse(f'{map._repr_html_()}')  
        #print(choix)
    else :
        #Je recupère le(s) heure(s) renseignée(es) par l'utilisateur
        zone_choisie = []
        for ch in choix : 
        # ch = int(ch)
            zone_choisie.append(zone[ch])
            #print(zone_choisie)
            #print(zone[ch])
            #print(type(ch))

        df_choix = df[df['Heure Decl'].isin(zone_choisie)]     

        cluster = MarkerCluster(name = "Donnees").add_to(map) 

        # Selection des coordonnées pour la carte
        df_map_2 = df_choix[['Latitude', 'Longitude']]

        # Convertir les colonnes en numerique
        df_map_2 = df_map_2.astype({'Latitude':'float','Longitude':'float'})

        liste = df_map_2.values.tolist()
        liste_taille = len(liste)

            #map = folium.Map(location=[lat_fixe, long_fixe], zoom_start=4) 
        for point in range(0, liste_taille) :
            html = '''
                <b> Type declench : </b> {} <br>
                <b> Date : </b> {} <br>
                <b> Heure : </b>{} <br>
                <b> Code Alarme : </b>{} <br>
                <b> Type Client : </b>{}
                    '''.format(df_choix.iloc[point, 0], df_choix.iloc[point, 1],df_choix.iloc[point, 2], df_choix.iloc[point, 3],df_choix.iloc[point, 13] )
            popup = folium.Popup(html, max_width=1000)
            marker = folium.Marker(liste[point], popup=popup,tooltip = df_choix.iloc[point, 6], icon  = folium.Icon(icon = "cloud"))
            marker.add_to(cluster)
        
        #return render(request, 'exemple.html',{'texte':texte} )
        return HttpResponse(f'{map._repr_html_()}')  

############################## FIN : GESTION DES DECLENCHEMENTS PAR DES TRANCHES DE DEUX HEURES ##################################
'''
def all_tranche_deux_heures_2(request): 
    
    carte_garde = "Carte_Alarme_new.xlsx"
    # m = folium.Map((5.37309, -3.99117), tooltip = "G4S Siege" , zoom_start=7)
    
    df = pd.read_excel(carte_garde)

    # Je construis la carte des sites : 

    map = folium.Map((5.37309, -3.99117), tooltip = "G4S Siege" , zoom_start=3)

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
'''
################################## DEBUT : Gestion de tous les declenchements par zone  #########################################
def carte_all(request): 
     
    df = pd.read_excel("Carte_Alarme_new.xlsx")

    map = folium.Map((5.327098119322325, -3.94640170570424), tooltip = "G4S Siege" , zoom_start=5) 

    cluster = MarkerCluster(name = "Donnees").add_to(map) 

        # Selection des coordonnées pour la carte
    df_map_2 = df[['Latitude', 'Longitude']]

    # Convertir les colonnes en numerique
    df_map_2 = df_map_2.astype({'Latitude':'float','Longitude':'float'})

    liste = df_map_2.values.tolist()
    liste_taille = len(liste)

            #map = folium.Map(location=[lat_fixe, long_fixe], zoom_start=4)
    for point in range(0, liste_taille) :  
        html = '''
                <b> Type declench : </b> {} <br>
                <b> Date : </b> {} <br>
                <b> Heure : </b>{} <br>
                <b> Code Alarme : </b>{} <br>
                <b> Type Client : </b>{}
            '''.format(df.iloc[point, 0], df.iloc[point, 1],df.iloc[point, 2], df.iloc[point, 3],df.iloc[point, 13] )
        popup = folium.Popup(html, max_width=1000)
        marker = folium.Marker(liste[point], popup = popup, tooltip = df.iloc[point, 6], icon  = folium.Icon(icon = "cloud"))
        marker.add_to(cluster)

    return render(request, 'carte_all.html',{'map': map._repr_html_()} )


def carte_all_htmx(request, pk): 
     
    df = pd.read_excel("Carte_Alarme_new.xlsx")
    #texte = " Je suis là"

    zone = {"0": "Boston", "1": "Detroit", "2": "Malibu", "3": "Monaco", "4": "Orleans", "5": "Sydney", }
    map = folium.Map((5.37309, -3.99117), tooltip = "G4S Siege" , zoom_start=5)

    # Je recupère les choix de l'utilisateur
    choix = pk.strip()
    if choix == "aucun" :
        #map = folium.Map((5.327098119322325, -3.94640170570424), tooltip = "G4S Siege" , zoom_start=7)
        return HttpResponse(f'{map._repr_html_()}')  
        #print(choix)
    else :
        #df_choix = df
        zone_choisie = []
        for ch in choix : 
        # ch = int(ch)
            zone_choisie.append(zone[ch])
            #print(zone_choisie)
            #print(zone[ch])
            #print(type(ch))

        df_choix = df[df['ZONE'].isin(zone_choisie)]     

        cluster = MarkerCluster(name = "Donnees").add_to(map) 

        # Selection des coordonnées pour la carte
        df_map_2 = df_choix[['Latitude', 'Longitude']]

        # Convertir les colonnes en numerique
        df_map_2 = df_map_2.astype({'Latitude':'float','Longitude':'float'})

        liste = df_map_2.values.tolist()
        liste_taille = len(liste)

            #map = folium.Map(location=[lat_fixe, long_fixe], zoom_start=4) 
        for point in range(0, liste_taille) :
            html = '''
                <b> Type declench : </b> {} <br>
                <b> Date : </b> {} <br>
                <b> Heure : </b>{} <br>
                <b> Code Alarme : </b>{} <br>
                <b> Type Client : </b>{}
                    '''.format(df_choix.iloc[point, 0], df_choix.iloc[point, 1],df_choix.iloc[point, 2], df_choix.iloc[point, 3],df_choix.iloc[point, 13] )
            popup = folium.Popup(html, max_width=1000)
            marker = folium.Marker(liste[point], popup=popup,tooltip = df_choix.iloc[point, 6], icon  = folium.Icon(icon = "cloud"))
            marker.add_to(cluster)
        
        #return render(request, 'exemple.html',{'texte':texte} )
        return HttpResponse(f'{map._repr_html_()}')  

############################## FIN : Gestion de tous les declenchements par zone  #########################################