import pandas as pd
import geopandas as gpd
from fuzzywuzzy import process
import numpy as np
import os
from datetime import datetime

print("=" * 70)
print("ÉTAPE 6: MERGE & VALIDATION")
print("=" * 70)

# Load all data
print("\n[1/6] Chargement données...")
df_unhcr = pd.read_csv('data/raw/unhcr_1951_2023.csv')
df_recent = pd.read_csv('data/raw/refugee_asylum_2019_2024.csv')
df_synthetic = pd.read_csv('data/interim/synthetic_integration_indicators.csv')
world = gpd.read_file('data/raw/countries_geo.geojson')

print(f"  ✓ UNHCR: {len(df_unhcr)} lignes, {len(df_unhcr.columns)} colonnes")
print(f"  ✓ Recent: {len(df_recent)} lignes, {len(df_recent.columns)} colonnes")
print(f"  ✓ Synthetic: {len(df_synthetic)} lignes, {len(df_synthetic.columns)} colonnes")
print(f"  ✓ Geo: {len(world)} pays")

# Normalize country names & add ISO codes
print("\n[2/6] Normalisation noms pays...")
iso_mapping = dict(zip(world['NAME'], world['ISO_A3']))

def find_iso_code(country_name):
    if pd.isna(country_name):
        return None
    if country_name in iso_mapping:
        return iso_mapping[country_name]
    # Fuzzy match
    matches = process.extractOne(country_name, iso_mapping.keys(), score_cutoff=80)
    return iso_mapping[matches[0]] if matches else None

# Map ISO codes
df_unhcr['iso_a3'] = df_unhcr['Country of asylum'].apply(find_iso_code)
df_synthetic['iso_a3'] = df_synthetic['country'].apply(find_iso_code)

print(f"  ✓ UNHCR mapped: {df_unhcr['iso_a3'].notna().sum()} / {len(df_unhcr)}")
print(f"  ✓ Synthetic mapped: {df_synthetic['iso_a3'].notna().sum()} / {len(df_synthetic)}")

# Filter to countries with ISO codes
df_unhcr_clean = df_unhcr[df_unhcr['iso_a3'].notna()].copy()
df_synthetic_clean = df_synthetic[df_synthetic['iso_a3'].notna()].copy()

print(f"  ✓ UNHCR after filtering: {len(df_unhcr_clean)} lignes")
print(f"  ✓ Synthetic after filtering: {len(df_synthetic_clean)} lignes")

# Merge UNHCR + Synthetic on iso_a3 + year
print("\n[3/6] Merge principal (UNHCR + Synthetic)...")
master = df_unhcr_clean.merge(
    df_synthetic_clean[['iso_a3', 'year', 'employment_rate', 'housing_access', 
                        'education_enrollment', 'income_stability', 'legal_rights_score', 
                        'social_cohesion', 'integration_index']],
    left_on=['iso_a3', 'Year'],
    right_on=['iso_a3', 'year'],
    how='inner',
    suffixes=('_unhcr', '_synthetic')
)

print(f"  ✓ Merged rows: {len(master)}")
print(f"  ✓ Countries: {master['iso_a3'].nunique()}")
print(f"  ✓ Years: {master['Year'].min()} - {master['Year'].max()}")

# Enrich with geography
print("\n[4/6] Enrichissement géographie...")
# Extract properties from GeoJSON
# Extract properties from GeoJSON
geo_data = []
for idx, row in world.iterrows():
    geo_data.append({
        'iso_a3': row['ISO_A3'],
        'country_name': row['NAME'],
        'continent': row.get('CONTINENT', None),
        'region_un': row.get('REGION_UN', None),
    })

df_geo = pd.DataFrame(geo_data)

master = master.merge(df_geo, on='iso_a3', how='left')

print(f"  ✓ Enrichies: {master['country_name'].notna().sum()} lignes avec géo")

# Quality validation
print("\n[5/6] Validation qualité...")
null_check = master.isnull().sum()
print(f"\n  Nulls par colonne (top 10):")
null_check_sorted = null_check[null_check > 0].sort_values(ascending=False).head(10)
for col, count in null_check_sorted.items():
    pct = count / len(master) * 100
    print(f"    {col}: {count} ({pct:.1f}%)")

# Add data quality metadata
master['data_source'] = 'UNHCR + Synthetic'
master['quality_flag'] = master['iso_a3'].apply(lambda x: 'clean' if pd.notna(x) else 'missing')
master['updated_date'] = datetime.now()

# Save outputs
print("\n[6/6] Sauvegarde outputs...")
master.to_parquet('data/processed/refugee_master_consolidated.parquet', index=False)
master.to_csv('data/processed/refugee_master_consolidated.csv', index=False)

print(f"\n  ✓ Parquet: data/processed/refugee_master_consolidated.parquet ({len(master)} lignes)")
print(f"  ✓ CSV: data/processed/refugee_master_consolidated.csv")

# Summary statistics
print("\n" + "=" * 70)
print("ÉTAPE 6 ✓ COMPLÉTÉE")
print("=" * 70)

print(f"\nFinal Master Table:")
print(f"  Shape: {master.shape}")
print(f"  Countries: {master['iso_a3'].nunique()}")
print(f"  Years: {master['Year'].min()} - {master['Year'].max()}")
print(f"  Integration index: {master['integration_index'].min():.2f} - {master['integration_index'].max():.2f}")
print(f"  Memory: {master.memory_usage(deep=True).sum() / (1024*1024):.2f} MB")

print(f"\nTop 5 countries by avg integration index:")
top_integration = master.groupby('country_name')['integration_index'].mean().nlargest(5)
for country, score in top_integration.items():
    print(f"  {country}: {score:.2f}")

print(f"\nBottom 5 countries by avg integration index:")
bottom_integration = master.groupby('country_name')['integration_index'].mean().nsmallest(5)
for country, score in bottom_integration.items():
    print(f"  {country}: {score:.2f}")

print(f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")