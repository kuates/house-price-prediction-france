import sys
import os
import requests
from tqdm import tqdm  # Barre de progression

# Forcer l'encodage en UTF-8 pour éviter les erreurs d'affichage
sys.stdout.reconfigure(encoding='utf-8')

# URL des fichiers DVF
DVF_URL = "https://files.data.gouv.fr/geo-dvf/latest/csv/"

# Répertoire pour sauvegarder les fichiers
DATA_DIR = "data/raw/"
os.makedirs(DATA_DIR, exist_ok=True)

# Liste des années à télécharger (modifie si besoin)
YEARS = ["2019", "2020", "2021", "2022", "2023", "2024"]
FILE_NAME = "full.csv.gz"

def download_dvf():
    """Télécharge les fichiers DVF pour chaque année et les enregistre dans data/raw/{année}/"""
    for year in YEARS:
        file_url = f"{DVF_URL}{year}/{FILE_NAME}"  # URL complète du fichier
        file_path = os.path.join(DATA_DIR, year, FILE_NAME)  # Chemin local du fichier
        
        # ✅ Assurer que le dossier de l'année existe
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        if not os.path.exists(file_path):
            print(f"📥 Téléchargement de {year}/{FILE_NAME} en cours...")
            response = requests.get(file_url, stream=True)

            if response.status_code == 200:  # Vérifier si l'URL est correcte
                with open(file_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                print(f"✅ {year}/{FILE_NAME} téléchargé avec succès !")
            else:
                print(f"❌ Erreur {response.status_code} : Impossible de télécharger {year}/{FILE_NAME}")
        else:
            print(f"✔️ {year}/{FILE_NAME} déjà présent.")

if __name__ == "__main__":
    download_dvf()
