import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Chargement du Fichier CSV
data2 = pd.read_csv('data/MMM_MMM_GeolocCompteurs.csv')

# Conversion des Colonnes de Latitude et Longitude au Format Numérique
data2['Latitude'] = pd.to_numeric(data2['Latitude'], errors='coerce')
data2['Longitude'] = pd.to_numeric(data2['Longitude'], errors='coerce')

# Création de la figure Plotly
fig = go.Figure()

# Ajout des points sur le graphique avec des infobulles
fig.add_trace(go.Scatter(
    x=data2['Longitude'],
    y=data2['Latitude'],
    text=data2.apply(lambda row: f"{row['Nom du com']} ({row['N° Série']} vélos)", axis=1),
    mode='markers',
    marker=dict(
        size=8,
        color=np.linspace(0, 1, len(data2)),  # Utilisation de linspace pour générer des couleurs différentes
        colorscale='Rainbow',
        showscale=True
    )
))

# Mise en page du graphique
fig.update_layout(
    title='Localisation des Compteurs de Vélo à Montpellier',
    xaxis_title='Longitude',
    yaxis_title='Latitude',
    annotations=[
        dict(
            x=0.5,
            y=-0.1,
            xref='paper',
            yref='paper',
            text="Les points représentent les compteurs de vélo et leurs positions exactes tout au long de Montpellier.",
            showarrow=False,
            font=dict(size=12)
        )
    ]
)

# Sauvegarder la figure dans un fichier HTML
html_file = "OCP.html"
fig.write_html(html_file)

def get_bike_data(date):
    """
    Récupère les données de vélo pour une date donnée.

    Cette fonction retourne l'ensemble des données de localisation des compteurs de vélos
    pour la date spécifiée. Actuellement, elle retourne simplement le jeu de données
    complet, mais elle peut être modifiée pour filtrer les données par date.

    Args:
        date (str): La date pour laquelle récupérer les données (format attendu : 'YYYY-MM-DD').

    Returns:
        pd.DataFrame: Les données des compteurs de vélos sous forme de DataFrame.
    """
    return data2


def plot_bike_data(data2):
    """
    Fonction d'exemple pour tracer les données des compteurs de vélos.

    Cette fonction affiche un message indiquant que les données des compteurs de vélos
    pour une date spécifique sont prêtes à être tracées. Elle peut être modifiée
    pour effectuer un tracé réel si nécessaire.

    Args:
        data2 (pd.DataFrame): Les données à tracer, sous forme de DataFrame.
    """
    print(f"Tracé des données de vélo pour la date : {data2}")


# Exemple de test pour récupérer et tracer des données supplémentaires (si définie)
data2 = get_bike_data('2024-01-01') # Recuperation des données pour la date '2024-01-01'
plot_bike_data(data2)    #Tracer lees données de vélo

