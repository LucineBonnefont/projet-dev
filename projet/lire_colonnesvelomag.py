import pandas as pd
import tkinter as tk
from tkinter import ttk

# Charger le fichier CSV
df = pd.read_csv('./projet/TAM_MMM_CoursesVelomagg .csv')

# Extraire les noms des colonnes
columns = list(df.columns)

# Créer une nouvelle fenêtre
root = tk.Tk()
root.title("Noms des Colonnes")

# Créer un tableau dans l'interface Tkinter qui n'affiche que les noms de colonnes
tree = ttk.Treeview(root)

# Définir les colonnes avec une seule colonne nommée "Noms des Colonnes"
tree["columns"] = ("Column Names",)
tree["show"] = "headings"  # Affiche uniquement les en-têtes

# Créer un en-tête pour les noms des colonnes
tree.heading("Column Names", text="Noms des Colonnes")
tree.column("Column Names", anchor="center")  # Centrer le texte

# Insérer les noms des colonnes dans le tableau
for column_name in columns:
    tree.insert("", "end", values=(column_name,))

# Ajouter le tableau à la fenêtre
tree.pack(expand=True, fill="both")

# Lancer l'application
root.mainloop()

import pandas as pd

import pandas as pd


# Afficher les noms des colonnes
print("Noms des colonnes :")
print(df.columns.tolist())
