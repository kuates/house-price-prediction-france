import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap
from tqdm import tqdm  # Barre de progression

# Forcer l'encodage en UTF-8 pour éviter les erreurs d'affichage
sys.stdout.reconfigure(encoding='utf-8')

# Dossiers des données
CLEAN_DIR = "data/processed/"
DASHBOARD_DIR = "dashboard/"

# Liste des années à analyser
YEARS = ["2019", "2020", "2021", "2022", "2023", "2024"]

# Boucle pour analyser chaque année
for year in YEARS:
    file_path = os.path.join(CLEAN_DIR, year, "full_clean.csv.gz")
    dash_file = os.path.join(DASHBOARD_DIR, year, "full_clean.csv.gz")
    
    if not os.path.exists(file_path):
        print(f"❌ Fichier introuvable : {file_path}")
        continue  # Passe à l'année suivante

    print(f"📊 Analyse des données pour {year}...")
    
    # Assurer la création des dossiers nettoyés
    os.makedirs(os.path.dirname(dash_file), exist_ok=True)

    # Charger les données nettoyées
    df = pd.read_csv(file_path)

    # --- 📌 Statistiques générales ---
    print(df.info())
    print(df.describe())

    # --- 📌 Répartition des types de biens ---
    plt.figure(figsize=(8, 5))
    sns.countplot(y=df["type_local"], palette="pastel")
    plt.title(f"Répartition des types de biens ({year})")
    plt.savefig(f"{dash_file}type_biens_{year}.png")
    plt.show()

    # --- 📌 Relation surface/prix ---
    plt.figure(figsize=(8, 5))
    sns.scatterplot(x=df["surface_reelle_bati"], y=df["valeur_fonciere"], alpha=0.5)
    plt.xlabel("Surface (m²)")
    plt.ylabel("Prix (€)")
    plt.title(f"Relation entre la surface et le prix ({year})")
    plt.savefig(f"{dash_file}relation_surface_prix_{year}.png")
    plt.show()

    # --- 📌 Distribution des prix immobiliers ---
    plt.figure(figsize=(8, 5))
    sns.histplot(df["valeur_fonciere"], bins=50, kde=True, color="blue")
    plt.xlabel("Prix (€)")
    plt.title(f"Distribution des prix de l'immobilier ({year})")
    plt.savefig(f"{dash_file}distribution_prix_{year}.png")
    plt.show()

    # --- 📌 Top 10 des villes les plus chères ---
    top_villes = df.groupby("nom_commune")["valeur_fonciere"].mean().sort_values(ascending=False).head(10)

    plt.figure(figsize=(10, 5))
    sns.barplot(x=top_villes.values, y=top_villes.index, palette="coolwarm")
    plt.xlabel("Prix moyen (€)")
    plt.title(f"Top 10 des villes les plus chères ({year})")
    plt.savefig(f"{dash_file}top_villes_{year}.png")
    plt.show()

    # --- 📌 Heatmap des prix immobiliers ---
    df_map = df[["latitude", "longitude", "valeur_fonciere"]].dropna().sample(1000, random_state=42)

    map = folium.Map(location=[46.603354, 1.888334], zoom_start=6)
    heat_data = [[row["latitude"], row["longitude"], row["valeur_fonciere"]] for _, row in df_map.iterrows()]
    HeatMap(heat_data, radius=10).add_to(map)

    map.save(f"{dash_file}heatmap_{year}.html")

    print(f"✅ Analyse {year} terminée. Résultats enregistrés.")

print("📊 Toutes les analyses ont été générées avec succès !")