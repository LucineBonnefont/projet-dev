#%%
def calculate_bike_availability(filtered_data):
    """
    Calcule la disponibilité des vélos pour chaque heure de la journée.
    
    Paramètres :
    - filtered_data (DataFrame) : Les données des trajets filtrés.
    
    Retourne :
    - hourly_availability (DataFrame) : Un DataFrame avec la disponibilité horaire des vélos.
    """
    # Extraire l'heure de départ et de retour
    filtered_data['hour'] = filtered_data['Departure'].dt.hour
    
    # Calculer le nombre de vélos en circulation pour chaque heure
    hourly_counts = filtered_data.groupby('hour').size().reset_index(name='available_bikes')
    
    # Compléter avec les heures manquantes (pour afficher toute la journée)
    all_hours = pd.DataFrame({'hour': range(0, 24)})
    hourly_availability = pd.merge(all_hours, hourly_counts, on='hour', how='left').fillna(0)
    
    return hourly_availability

import matplotlib.pyplot as plt
import osmnx as ox

def plot_bike_availability(hourly_availability):
    """
    Crée un graphique de la disponibilité des vélos par heure.
    
    Paramètres :
    - hourly_availability (DataFrame) : Un DataFrame avec la disponibilité horaire des vélos.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(hourly_availability['hour'], hourly_availability['available_bikes'], marker='o', linestyle='-', color='blue')
    plt.title("Disponibilité des vélos en fonction de l'heure", fontsize=14)
    plt.xlabel("Heure de la journée", fontsize=12)
    plt.ylabel("Nombre de vélos disponibles", fontsize=12)
    plt.xticks(range(0, 24))
    plt.grid()
    plt.tight_layout()
    plt.show()

from bike_data import get_bike_data

if __name__ == "__main__":
    # Étape 1 : Définir une date d'analyse
    analysis_date = "2023-11-15"
    
    # Étape 2 : Charger les données
    stations, filtered_data = get_bike_data(analysis_date)
    
    if filtered_data is not None:
        # Étape 3 : Calculer la disponibilité horaire
        hourly_availability = calculate_bike_availability(filtered_data)
        
        # Étape 4 : Tracer le graphique
        plot_bike_availability(hourly_availability)

# %%
