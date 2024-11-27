import pandas as pd

# Charger le fichier CSV directement
data2 = pd.read_csv('MMM_MMM_GeolocCompteurs 2.csv')

# Afficher les premières lignes du dataframe pour vérifier le contenu
print(data2.head())

# Filtrer les données pour ne garder que les compteurs de vélo
filtered_data2 = data2[data2['Nom du com'].str.contains('Vélo')]

# Afficher les premières lignes des données filtrées
print(filtered_data2.head())

# Extraire les informations de localisation des compteurs de vélo
compteurs_velo = {}
for index, row in filtered_data2.iterrows():
    name = row['Nom du com']
    lat = row['Latitude']
    lon = row['Longitude']
    compteurs_velo[name] = (lat, lon)

print(compteurs_velo)
