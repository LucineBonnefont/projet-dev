import uuid
import requests
import pandas as pd
import osmnx as ox

def get_bike_data(analysis_date):
    """
    Fonction pour récupérer les données des stations de vélo et filtrer les trajets 
    pour une date spécifique.
    
    Paramètres :
    - analysis_date (str) : La date souhaitée au format 'AAAA-MM-JJ'
    
    Retourne :
    - stations (dict) : Un dictionnaire des coordonnées des stations
    - filtered_data (DataFrame) : Un DataFrame filtré pour la date spécifiée
    """

    # Récupérer les données de l'API bikestation
    url = 'https://portail-api-data.montpellier3m.fr/bikestation?limit=1000'
    response = requests.get(url)
    if response.status_code == 200:
        stations_data = response.json() 
    else:
        print(f"Erreur lors de la récupération des données : {response.status_code}")
        return None, None

    # Extraire les informations de localisation des stations
    stations = {}
    for station in stations_data:
        name = station['id'].split(':')[-1]  # Code de la station (001)
        lon = station['location']['value']['coordinates'][0]
        lat = station['location']['value']['coordinates'][1]
        stations[name] = (lon, lat)

    # Charger le fichier CSV
    data = pd.read_csv('data/TAM_MMM_CoursesVelomagg.csv', low_memory=False)

    # Convertir les colonnes de date au format datetime
    data['Departure'] = pd.to_datetime(data['Departure'])
    data['Return'] = pd.to_datetime(data['Return'])

    # Filtrer pour la date d'analyse spécifiée
    analysis_date = pd.to_datetime(analysis_date).date()
    filtered_data = data[(data['Departure'].dt.date == analysis_date) |
                         (data['Return'].dt.date == analysis_date)]
    
    return stations, filtered_data

def get_bike_routes(stations, paths):
    """
    Fonction pour récupérer les routes empruntées pour chaque trajet de vélo.
    
    Paramètres :
    - stations : Liste des stations de vélos avec leurs coordonnées GPS
    - paths : Liste des trajets des vélos
    
    Retourne :
    - bikes_routes (dict) : Un dictionnaire des routes empruntées par les vélos pour chaque trajet
    """

    # Charger le graphe de Montpellier pour les trajets à vélo
    G = ox.graph_from_place('Montpellier, France', network_type='bike')

    bikes_routes = []

    for _, path in paths.iterrows():
        
        # Extraire le code des stations de départ et de retour pour le trajet.
        departure_station = path['Departure station'][:3] if isinstance(path['Departure station'], str) else path['Departure station']
        return_station = path['Return station'][:3] if isinstance(path['Return station'], str) else path['Return station']

        # Obtenir les points des stations de départ et de retour.
        if not pd.isna(departure_station) and not pd.isna(return_station) :
            origin_node = ox.nearest_nodes(G, *stations[departure_station]) if departure_station in stations else None
            destination_node = ox.nearest_nodes(G, *stations[return_station]) if return_station in stations else None

        # Calculer le trajet complet et définir les étapes intermédiaires
        if origin_node and destination_node and  origin_node != destination_node :
            route = ox.shortest_path(G, origin_node, destination_node) or []
        else :
            route =  []

        departure_time = path['Departure']
        return_time = path['Return']
        
        # Stocker les informations pour chaque vélo
        bikes_routes.append({
            'id': uuid.uuid4(),
            'departure_time': departure_time,
            'return_time': return_time,
            'route': [(G.nodes[node]['x'], G.nodes[node]['y']) for node in route],
        })

    return bikes_routes
