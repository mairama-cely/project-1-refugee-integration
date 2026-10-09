import pandas as pd
import numpy as np
from faker import Faker
import os
from datetime import datetime

fake = Faker()
Faker.seed(42)  # Reproductibilité
np.random.seed(42)

print("=" * 70)
print("ÉTAPE 5: GÉNÉRATION DONNÉES SYNTHÉTIQUES INTÉGRATION")
print("=" * 70)

# Charger UNHCR pour avoir liste pays + années
print("\n[1/5] Chargement UNHCR source...")
df_unhcr = pd.read_csv('data/raw/unhcr_1951_2023.csv')

# Extraire pays uniques et années (focus 2000-2023 pour cohérence)
countries = sorted(df_unhcr['Country of asylum'].unique())[:50]  # Top 50 pays
years = range(2000, 2024)  # Focus 2000-2023

print(f"✓ Chargé: {len(df_unhcr)} lignes")
print(f"\nGénérant synthétique pour: {len(countries)} pays, {len(years)} années")
print(f"Total combinaisons: {len(countries) * len(years)}")

# Créer master table synthétique
print("\n[2/5] Génération indicateurs d'intégration...")
synthetic_data = []

for idx, country in enumerate(countries):
    if (idx + 1) % 10 == 0:
        print(f"  {idx + 1}/{len(countries)} pays traités...")
    
    for year in years:
        # Indicateurs d'intégration (0-100 scale)
        # Distribution réaliste: moins intégration en début, plus à la fin
        year_factor = (year - 2000) / 23  # 0 en 2000, 1 en 2023
        
        employment_rate = np.random.normal(35 + year_factor * 20, 18)
        housing_access = np.random.normal(45 + year_factor * 15, 16)
        education_enrollment = np.random.normal(60 + year_factor * 15, 12)
        income_stability = np.random.normal(30 + year_factor * 25, 22)
        legal_rights_score = np.random.normal(50 + year_factor * 15, 14)
        social_cohesion = np.random.normal(40 + year_factor * 15, 18)
        
        # Clamp to 0-100
        employment_rate = np.clip(employment_rate, 0, 100)
        housing_access = np.clip(housing_access, 0, 100)
        education_enrollment = np.clip(education_enrollment, 0, 100)
        income_stability = np.clip(income_stability, 0, 100)
        legal_rights_score = np.clip(legal_rights_score, 0, 100)
        social_cohesion = np.clip(social_cohesion, 0, 100)
        
        # Composite index (weighted average)
        integration_index = (
            employment_rate * 0.20 +
            housing_access * 0.15 +
            education_enrollment * 0.20 +
            income_stability * 0.15 +
            legal_rights_score * 0.20 +
            social_cohesion * 0.10
        )
        
        synthetic_data.append({
            'country': country,
            'year': year,
            'employment_rate': round(employment_rate, 2),
            'housing_access': round(housing_access, 2),
            'education_enrollment': round(education_enrollment, 2),
            'income_stability': round(income_stability, 2),
            'legal_rights_score': round(legal_rights_score, 2),
            'social_cohesion': round(social_cohesion, 2),
            'integration_index': round(integration_index, 2),
        })

df_synthetic = pd.DataFrame(synthetic_data)

print(f"✓ Synthétique généré: {len(df_synthetic)} lignes")

# Validation
print("\n[3/5] Validation synthétique...")
print(f"  Pays: {df_synthetic['country'].nunique()}")
print(f"  Années: {df_synthetic['year'].min()}-{df_synthetic['year'].max()}")
print(f"  Integration index range: {df_synthetic['integration_index'].min():.2f}-{df_synthetic['integration_index'].max():.2f}")
print(f"  Nulls: {df_synthetic.isnull().sum().sum()}")

# Statistiques
print("\n[4/5] Statistiques synthétique:")
stats = df_synthetic[['employment_rate', 'housing_access', 'education_enrollment', 
                       'income_stability', 'legal_rights_score', 'social_cohesion', 
                       'integration_index']].describe()
print(stats.round(2))

# Sauvegarde
print("\n[5/5] Sauvegarde...")
df_synthetic.to_csv('data/interim/synthetic_integration_indicators.csv', index=False)
print(f"✓ Sauvegardé: data/interim/synthetic_integration_indicators.csv ({os.path.getsize('data/interim/synthetic_integration_indicators.csv') / (1024):.2f} KB)")

# Échantillon
print("\n[SAMPLE] Premiers 10 records:")
print(df_synthetic.head(10).to_string())

print("\n" + "=" * 70)
print("ÉTAPE 5 ✓ COMPLÉTÉE")
print("=" * 70)
print(f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")