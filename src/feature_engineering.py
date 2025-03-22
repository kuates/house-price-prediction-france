import sys
import pandas as pd
import numpy as np
import os
from tqdm import tqdm  # Barre de progression

# Forcer l'encodage en UTF-8 pour éviter les erreurs d'affichage
sys.stdout.reconfigure(encoding='utf-8')

# Liste des années disponibles
YEARS = ["2019", "2020", "2021", "2022", "2023", "2024"]

# Répertoires des fichiers
RAW_DATA_DIR = "data/processed/"
PROCESSED_DATA_DIR = "data/feature_engineered/"

# Créer le répertoire pour les données transformées si nécessaire
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

# Liste des variables utiles
FEATURES = [
    "valeur_fonciere",  # Prix (cible)
    "surface_reelle_bati",
    "nombre_pieces_principales",
    "code_departement",
    "latitude",
    "longitude",
    "type_local"
]

for year in YEARS:
    """Charge, transforme et sauvegarde les données pour une année donnée."""
    input_file = os.path.join(RAW_DATA_DIR, year, "full_clean.csv.gz")

    if not os.path.exists(input_file):
        print(f"⚠️ Fichier {input_file} non trouvé. Passer {year}.")
        continue
    
    print(f"📥 Chargement des données de {year}...")
    
    # Charger le fichier CSV (gzip compressé)
    df = pd.read_csv(input_file, sep=",", dtype=str, low_memory=False)

    # Sélectionner les variables utiles
    df = df[FEATURES]
    
    # Conversion en numérique pour éviter les erreurs
    cols_to_convert = ["surface_reelle_bati", "latitude", "longitude", "valeur_fonciere"]
    for col in cols_to_convert:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Remplir les valeurs manquantes correctement
    df["surface_reelle_bati"] = df["surface_reelle_bati"].fillna(df["surface_reelle_bati"].median())
    df["latitude"] = df.groupby("code_departement")["latitude"].transform(lambda x: x.fillna(x.mean()))
    df["longitude"] = df.groupby("code_departement")["longitude"].transform(lambda x: x.fillna(x.mean()))

    # Supprimer les lignes restantes avec des NaN
    df.dropna(inplace=True)

    # Encodage One-Hot de type_local
    df = pd.get_dummies(df, columns=["type_local"], drop_first=True)

    # Transformation logarithmique
    df["valeur_fonciere_log"] = np.log1p(df["valeur_fonciere"])
    df["surface_log"] = np.log1p(df["surface_reelle_bati"])

    # Créer le répertoire pour l'année si nécessaire
    year_output_dir = os.path.join(PROCESSED_DATA_DIR, year)
    os.makedirs(year_output_dir, exist_ok=True)

    # Sauvegarder le fichier transformé
    output_file = os.path.join(year_output_dir, "feature_engineered.csv.gz")
    df.to_csv(output_file, index=False, compression="gzip")

    print(f"✅ Données de {year} préparées et sauvegardées dans {output_file}")

print("🎯 Feature Engineering terminé pour toutes les années !")

