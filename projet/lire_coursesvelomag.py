import pandas as pd

# Assurez-vous que le chemin est correct

# Lire le fichier CSV
df = pd.read_csv('./projet/TAM_MMM_CoursesVelomagg .csv')

# Afficher le DataFrame
print(df)

import pandas as pd
import tkinter as tk
from tkinter import ttk


# Créer une nouvelle fenêtre
root = tk.Tk()
root.title("Tableau de Données")

# Créer le tableau
tree = ttk.Treeview(root)

# Définir les colonnes
tree["columns"] = list(df.columns)
tree["show"] = "headings"  # Affiche uniquement les en-têtes

# Créer les en-têtes de colonnes
for column in df.columns:
    tree.heading(column, text=column)
    tree.column(column, anchor="center")  # Centrer le texte dans les colonnes

# Ajouter les données au tableau
for index, row in df.iterrows():
    tree.insert("", "end", values=list(row))

# Ajouter le tableau à la fenêtre
tree.pack(expand=True, fill="both")

# Lancer l'application
root.mainloop()
