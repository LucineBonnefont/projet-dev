import pooch

# Dossier cache pour stocker les données localement
DATA_DIR = pooch.os_cache("tam_cycle_data")

# Gestionnaire de fichiers avec leurs hachages MD5 et URLs
pooch_handler = pooch.create(
    path=DATA_DIR,
    base_url="",  
    registry={
        "MMM_MMM_GeolocCompteurs.csv": "md5:0a72d428a26dfcd9097942227999f068",
        "TAM_MMM_CoursesVelomagg.csv": "md5:c8287f1ed3ad9ea5db62537024b78813",
    },
    urls={
        "MMM_MMM_GeolocCompteurs.csv": "https://data.montpellier3m.fr/sites/default/files/MMM_MMM_GeolocCompteurs.csv",
        "TAM_MMM_CoursesVelomagg.csv": "https://data.montpellier3m.fr/sites/default/files/TAM_MMM_CoursesVelomagg.csv",
    },
)

def get_data(filename):
    """
    Télécharge un fichier s'il n'existe pas déjà ou vérifie son intégrité.
    
    Parameters:
        filename (str): Nom du fichier à télécharger.
    
    Returns:
        str: Chemin local vers le fichier téléchargé.
    """
    try:
        file_path = pooch_handler.fetch(filename)
        print(f"Fichier téléchargé ou trouvé localement : {file_path}")
        return file_path
    except pooch.DownloadError as e:
        print(f"Erreur lors du téléchargement de {filename}: {e}")
        return None

# test (exemple) d'utilisation
if __name__ == "__main__":
    # Télécharger les fichiers
    velomagg_path = get_data("TAM_MMM_CoursesVelomagg.csv")
    compteurs_path = get_data("MMM_MMM_GeolocCompteurs.csv")

    if velomagg_path and compteurs_path:
        print(f"Fichiers téléchargés :\n- {velomagg_path}\n- {compteurs_path}")
