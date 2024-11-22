import pandas as pd
from collections import Counter

# Chemin vers le fichier CSV (remplace par le bon chemin)
data_path = "projet/TAM_MMM_CoursesVelomagg .csv"

# Charger les données
df = pd.read_csv(data_path)

# Filtrer les colonnes dont nous avons besoin
df_filtered = df[['Departure station', 'Return station']]

# Créer une liste des trajets (station de départ, station de retour)
trip_list = list(zip(df_filtered['Departure station'], df_filtered['Return station']))

# Compter la fréquence des trajets
counter = Counter(trip_list)

# Obtenir les 5 trajets les plus fréquents
top_5_trips = counter.most_common(5)

# Créer un DataFrame avec les résultats
top_5_df = pd.DataFrame(top_5_trips, columns=['Trip', 'Frequency'])

# Séparer les tuples en deux colonnes (Departure station et Return station)
top_5_df[['Departure station', 'Return station']] = pd.DataFrame(top_5_df['Trip'].to_list(), index=top_5_df.index)

# Supprimer la colonne Trip qui contient les tuples
top_5_df = top_5_df.drop(columns=['Trip'])

# Ajouter une colonne pour le classement (de 1 à 5)
top_5_df['Rank'] = range(1, 6)

# Réorganiser les colonnes pour que "Rank" soit en premier
top_5_df = top_5_df[['Rank', 'Departure station', 'Return station', 'Frequency']]


# Générer le tableau HTML et l'enregistrer dans le dossier docs
top_trajets_html = top_5_df.to_html(index=False)
output_path = "docs/flux_velo_montpellier.html"
with open(output_path, "w") as file:
    file.write(top_trajets_html)

print(f"Tableau HTML généré dans {output_path}")
