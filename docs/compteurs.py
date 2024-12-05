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
print(f"Graphique statique sauvegardé sous {html_file}")

# Exemple de fonction pour récupérer et tracer des données supplémentaires (si définie)
def get_bike_data(date):
    return data2

def plot_bike_data(data):
    print(f"Tracé des données de vélo pour la date : {data}")

data2 = get_bike_data('2023-01-01')
plot_bike_data(data2)
"""
Ce code crée  un graphe OCP qui localise tous les compteurs de vélo de
la ville de Montpellier pour une date spécifique.
"""
