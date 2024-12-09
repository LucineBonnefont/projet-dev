import folium
from collections import defaultdict

def create_density_map(bike_routes, location=[43.6119, 3.8772], zoom_start=15, return_frequency=False):
    """
    Crée une carte interactive des routes empruntées par les vélos, avec des couleurs
    indiquant la densité de trafic.

    Paramètres :
    - bike_routes : Liste des trajets contenant des coordonnées GPS
    - location : Coordonnées pour centrer la carte (par défaut Montpellier, France)
    - zoom_start : Niveau de zoom initial de la carte
    
    Retourne :
    - density_map : Objet de carte Folium
    """
    
    # Dictionnaire pour compter la fréquence de chaque segment de route
    segment_frequency = defaultdict(int)

    # Compter la fréquence des segments
    for route in bike_routes:
        for i in range(len(route['route']) - 1):
            # Inverser les coordonnées pour chaque point
            start = (route['route'][i][1], route['route'][i][0])  # (latitude, longitude)
            end = (route['route'][i + 1][1], route['route'][i + 1][0])  # (latitude, longitude)
            segment = (start, end)
            segment_frequency[segment] += 1

    if return_frequency:
        return segment_frequency

    return generate_map(segment_frequency, location=[43.6119, 3.8772], zoom_start=15)

def generate_map(segment_frequency, location=[43.6119, 3.8772], zoom_start=15):
    
    # Initialisation de la carte
    density_map = folium.Map(location=location, zoom_start=zoom_start)

    # Déterminer la fréquence maximale pour normaliser les couleurs
    max_frequency = max(segment_frequency.values())
    # Définir les seuils pour les couleurs
    seuils = {
        25: max_frequency * 0.25,
        50: max_frequency * 0.5,
        75: max_frequency * 0.75,
        90: max_frequency * 0.90,
    }

    # Ajouter chaque segment à la carte avec une couleur selon sa fréquence
    for segment, frequency in segment_frequency.items():
        start, end = segment

        # Attribuer une couleur en fonction des seuils
        if frequency > seuils[90]:
            color = "black"
        elif frequency > seuils[75]:
            color = "red"
        elif frequency > seuils[50]:
            color = "orange"
        elif frequency > seuils[25]:
            color = "yellow"
        else:
            color = "green"

        # Ajouter le segment à la carte
        folium.PolyLine(
            locations=[start, end],
            color=color,
            weight=5,  # épaisseur du trait
            opacity=0.7
        ).add_to(density_map)

    return density_map
