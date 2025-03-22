import sys
import os
import pandas as pd
from tqdm import tqdm  # Barre de progression

# Forcer l'encodage en UTF-8 pour éviter les erreurs d'affichage
sys.stdout.reconfigure(encoding='utf-8')

# Répertoires des fichiers bruts et nettoyés
RAW_DIR = "data/raw/"
CLEAN_DIR = "data/processed/"

# Liste des années disponibles
YEARS = ["2019", "2020", "2021", "2022", "2023", "2024"]

# Colonnes utiles à conserver (modifiable selon les besoins)
COLS_TO_KEEP = ["valeur_fonciere", "surface_reelle_bati", "nombre_pieces_principales",
        "code_postal", "nom_commune", "type_local", "longitude", "latitude"]

def clean_dvf():
    """Charge, nettoie et sauvegarde les fichiers DVF par année"""
    for year in YEARS:
        raw_file = os.path.join(RAW_DIR, year, "full.csv.gz")
        clean_file = os.path.join(CLEAN_DIR, year, "full_clean.csv.gz")

        # Vérifier si le fichier brut existe
        if not os.path.exists(raw_file):
            print(f"⚠️ Fichier manquant : {raw_file}")
            continue  # Passe à l'année suivante

        print(f"🧹 Nettoyage du fichier {year}...")

        # Assurer la création des dossiers nettoyés
        os.makedirs(os.path.dirname(clean_file), exist_ok=True)

        # Charger le fichier CSV (gzip compressé)
        df = pd.read_csv(raw_file, sep=",", dtype=str, low_memory=False)

        # Supprimer les lignes vides et valeurs manquantes critiques
        df.dropna(subset=["valeur_fonciere", "surface_reelle_bati"], inplace=True)

        # Convertir les types de données
        df["valeur_fonciere"] = pd.to_numeric(df["valeur_fonciere"], errors="coerce")
        df["surface_reelle_bati"] = pd.to_numeric(df["surface_reelle_bati"], errors="coerce")
        df["date_mutation"] = pd.to_datetime(df["date_mutation"], errors="coerce")

        # Filtrer les prix aberrants (ex: valeur_fonciere < 1000€ ou > 10M€)
        df = df[(df["valeur_fonciere"] >= 1000) & (df["valeur_fonciere"] <= 10_000_000)]

        # Filtrer les surfaces aberrantes (ex: surface < 5m² ou > 1000m²)
        df = df[(df["surface_reelle_bati"] >= 5) & (df["surface_reelle_bati"] <= 1000)]

        # Garder uniquement les colonnes utiles
        df = df[COLS_TO_KEEP]

        # Enregistrer le fichier nettoyé
        df.to_csv(clean_file, sep=",", index=False, compression="gzip")

        print(f"✅ Fichier nettoyé sauvegardé : {clean_file}")

if __name__ == "__main__":
    clean_dvf()

