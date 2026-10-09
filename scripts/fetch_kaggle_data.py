import kagglehub
import pandas as pd
import geopandas as gpd
import os
from datetime import datetime

print("=" * 70)
print("ÉTAPE 4: TÉLÉCHARGEMENT KAGGLE DATASETS")
print("=" * 70)

# Create directories
os.makedirs('data/raw', exist_ok=True)
os.makedirs('data/interim', exist_ok=True)
os.makedirs('data/processed', exist_ok=True)

# Dataset 1: UNHCR Historical (1951-2023)
print("\n[1/3] Téléchargeant: avtnshm/united-nations-refugee-data-unhcr")
try:
    path_unhcr = kagglehub.dataset_download("avtnshm/united-nations-refugee-data-unhcr")
    print(f"✓ Téléchargé: {path_unhcr}")
    
    # Find CSV file
    unhcr_files = [f for f in os.listdir(path_unhcr) if f.endswith('.csv')]
    if unhcr_files:
        unhcr_file = os.path.join(path_unhcr, unhcr_files[0])
        df_unhcr = pd.read_csv(unhcr_file)
        df_unhcr.to_csv('data/raw/unhcr_1951_2023.csv', index=False)
        print(f"✓ Sauvegardé: data/raw/unhcr_1951_2023.csv ({len(df_unhcr)} lignes, {len(df_unhcr.columns)} colonnes)")
        print(f"  Colonnes: {list(df_unhcr.columns)[:5]}...")
    else:
        print("✗ Pas de fichier CSV trouvé")
except Exception as e:
    print(f"✗ Erreur: {str(e)}")

# Dataset 2: Recent Asylum (2019-2024)
print("\n[2/3] Téléchargeant: nafayunnoor/global-refugee-and-asylum-seeker-data-2019-2024")
try:
    path_recent = kagglehub.dataset_download("nafayunnoor/global-refugee-and-asylum-seeker-data-2019-2024")
    print(f"✓ Téléchargé: {path_recent}")
    
    # Find CSV file
    recent_files = [f for f in os.listdir(path_recent) if f.endswith('.csv')]
    if recent_files:
        recent_file = os.path.join(path_recent, recent_files[0])
        df_recent = pd.read_csv(recent_file)
        df_recent.to_csv('data/raw/refugee_asylum_2019_2024.csv', index=False)
        print(f"✓ Sauvegardé: data/raw/refugee_asylum_2019_2024.csv ({len(df_recent)} lignes, {len(df_recent.columns)} colonnes)")
        print(f"  Colonnes: {list(df_recent.columns)[:5]}...")
    else:
        print("✗ Pas de fichier CSV trouvé")
except Exception as e:
    print(f"✗ Erreur: {str(e)}")

# Geo reference: Download from Natural Earth directly
print("\n[3/3] Chargeant référence géographique (Natural Earth)...")
try:
    # Download from Natural Earth URL directly
    url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
    import tempfile
    import zipfile
    
    with tempfile.TemporaryDirectory() as tmpdir:
        import urllib.request
        zip_path = os.path.join(tmpdir, "countries.zip")
        urllib.request.urlretrieve(url, zip_path)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(tmpdir)
        
        shp_file = os.path.join(tmpdir, "ne_110m_admin_0_countries.shp")
        world = gpd.read_file(shp_file)
        world.to_file('data/raw/countries_geo.geojson', driver='GeoJSON')
        print(f"✓ Sauvegardé: data/raw/countries_geo.geojson ({len(world)} pays)")
except Exception as e:
    print(f"✗ Erreur geo: {str(e)}")

print("\n" + "=" * 70)
print("ÉTAPE 4 ✓ COMPLÉTÉE")
print("=" * 70)

# Summary
print("\nRésumé fichiers créés:")
try:
    print(f"  ✓ data/raw/unhcr_1951_2023.csv ({os.path.getsize('data/raw/unhcr_1951_2023.csv') / (1024*1024):.2f} MB)")
except:
    print(f"  ✗ data/raw/unhcr_1951_2023.csv (non trouvé)")

try:
    print(f"  ✓ data/raw/refugee_asylum_2019_2024.csv ({os.path.getsize('data/raw/refugee_asylum_2019_2024.csv') / (1024*1024):.2f} MB)")
except:
    print(f"  ✗ data/raw/refugee_asylum_2019_2024.csv (non trouvé)")

try:
    print(f"  ✓ data/raw/countries_geo.geojson ({os.path.getsize('data/raw/countries_geo.geojson') / (1024):.2f} KB)")
except:
    print(f"  ✗ data/raw/countries_geo.geojson (non trouvé)")

print(f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")