import pandas as pd
import sqlite3
from datetime import datetime
import os
import sys

# Configuration
DB_PATH = 'database/refugee_integration.db'
PARQUET_PATH = 'data/processed/refugee_master_consolidated.parquet'

def init_db():
    """Initialiser la base de données"""
    os.makedirs('database', exist_ok=True)
    
    # Supprimer ancienne base si elle existe
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print('  ▸ Removed old database')
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Charger le schéma
    with open('database/schema.sql', 'r') as f:
        schema_sql = f.read()
    
    # Exécuter sans vues d'abord
    cursor.executescript(schema_sql)
    conn.commit()
    conn.close()
    print('  ▸ Schema created')

def load_data():
    """Charger et valider les données"""
    print('\n📦 Loading Data...')
    
    # Lire parquet
    print('  ▸ Reading parquet...')
    master = pd.read_parquet(PARQUET_PATH)
    print(f'    Raw records: {len(master):,}')
    
    # Agréger par (Country of asylum, Year)
    print('  ▸ Aggregating by (Country, Year)...')
    master = master.groupby(['Country of asylum', 'Year']).agg({
        'iso_a3': 'first',
        'continent': 'first',
        'region_un': 'first',
        'Refugees under UNHCR\'s mandate': 'sum',
        'Asylum-seekers': 'sum',
        'employment_rate': 'mean',
        'housing_access': 'mean',
        'education_enrollment': 'mean',
        'income_stability': 'mean',
        'legal_rights_score': 'mean',
        'social_cohesion': 'mean',
        'integration_index': 'mean',
        'data_source': 'first',
        'quality_flag': 'first'
    }).reset_index()
    print(f'    After aggregation: {len(master):,}')
    
    # Valider colonnes essentielles
    required_cols = [
        'Country of asylum', 'Year', 'iso_a3', 'continent', 'region_un',
        'Refugees under UNHCR\'s mandate', 'Asylum-seekers',
        'employment_rate', 'housing_access', 'education_enrollment',
        'income_stability', 'legal_rights_score', 'social_cohesion',
        'integration_index', 'data_source', 'quality_flag'
    ]
    
    missing = [col for col in required_cols if col not in master.columns]
    if missing:
        print(f'  ✗ Missing columns: {missing}')
        sys.exit(1)
    
    print(f'  ✓ All required columns present')
    return master

def insert_dimensions(conn, master):
    """Insérer les dimensions"""
    print('\n📊 Loading Dimensions...')
    cursor = conn.cursor()
    
    try:
        # dim_time
        print('  ▸ dim_time...')
        years = sorted(master['Year'].unique())
        
        for i, year in enumerate(years, 1):
            year_int = int(year) if pd.notna(year) else None
            if year_int is None:
                print(f'    ⚠ Skipping null year at index {i}')
                continue
            
            decade = f"{(year_int // 10) * 10}s"
            cursor.execute(
                "INSERT INTO dim_time (time_id, year, decade, period_label) VALUES (?, ?, ?, ?)",
                (i, year_int, decade, decade)
            )
        
        print(f'    Inserted {len(years)} years')
        conn.commit()
        
        # dim_country
        print('  ▸ dim_country...')
        countries = master[['Country of asylum', 'iso_a3', 'continent', 'region_un']].drop_duplicates(
            subset=['Country of asylum'],
            keep='first'
        )
        
        # Vérifier doublons iso_a3
        duplicates = countries[countries['iso_a3'].duplicated(keep=False)]
        if len(duplicates) > 0:
            print(f'    ⚠ Found {len(duplicates)} duplicate iso_a3 codes')
            countries = countries.drop_duplicates(subset=['iso_a3'], keep='first')
        
        inserted_countries = 0
        for idx, (_, row) in enumerate(countries.iterrows(), 1):
            try:
                cursor.execute(
                    "INSERT INTO dim_country (country_id, country_name, iso_a3, continent, region_un) VALUES (?, ?, ?, ?, ?)",
                    (idx, row['Country of asylum'], row['iso_a3'], row['continent'], row['region_un'])
                )
                inserted_countries += 1
            except sqlite3.IntegrityError as e:
                print(f'    ✗ Skipping {row["Country of asylum"]}: {e}')
                continue
        
        print(f'    Inserted {inserted_countries} countries')
        conn.commit()
        
        # dim_components
        print('  ▸ dim_components...')
        components = [
            ('employment_rate', 'EMP', 0.20, 'Employment rate'),
            ('housing_access', 'HSG', 0.15, 'Housing access'),
            ('education_enrollment', 'EDU', 0.20, 'Education enrollment'),
            ('income_stability', 'INC', 0.15, 'Income stability'),
            ('legal_rights_score', 'LGL', 0.20, 'Legal rights'),
            ('social_cohesion', 'SOC', 0.10, 'Social cohesion')
        ]
        for i, (name, code, weight, desc) in enumerate(components, 1):
            cursor.execute(
                "INSERT INTO dim_components (component_id, component_name, component_code, weight, description) VALUES (?, ?, ?, ?, ?)",
                (i, name, code, weight, desc)
            )
        print(f'    Inserted {len(components)} components')
        conn.commit()
        
        # dim_integration_tier
        print('  ▸ dim_integration_tier...')
        tiers = [
            ('High', 70, 100, 'Strong integration'),
            ('Medium', 50, 69, 'Moderate integration'),
            ('Low', 0, 49, 'Low integration')
        ]
        for i, (name, min_s, max_s, desc) in enumerate(tiers, 1):
            cursor.execute(
                "INSERT INTO dim_integration_tier (tier_id, tier_name, min_score, max_score, description) VALUES (?, ?, ?, ?, ?)",
                (i, name, min_s, max_s, desc)
            )
        print(f'    Inserted {len(tiers)} tiers')
        conn.commit()
        
    except Exception as e:
        print(f'  ❌ Error in insert_dimensions: {type(e).__name__}: {e}')
        import traceback
        traceback.print_exc()
        raise

def insert_facts(conn, master):
    """Insérer les tables de faits"""
    print('\n📈 Loading Facts...')
    cursor = conn.cursor()
    
    # Créer les mappings
    year_map = {}
    cursor.execute("SELECT time_id, year FROM dim_time")
    for time_id, year in cursor.fetchall():
        year_map[int(year)] = time_id
    
    country_map = {}
    cursor.execute("SELECT country_id, country_name FROM dim_country")
    for country_id, country_name in cursor.fetchall():
        country_map[country_name] = country_id
    
    component_map = {
        'employment_rate': 1,
        'housing_access': 2,
        'education_enrollment': 3,
        'income_stability': 4,
        'legal_rights_score': 5,
        'social_cohesion': 6
    }
    weights = {1: 0.20, 2: 0.15, 3: 0.20, 4: 0.15, 5: 0.20, 6: 0.10}
    
    # fact_refugee_integration
    print('  ▸ fact_refugee_integration...')
    updated_date = datetime.now().strftime('%Y-%m-%d')
    fact_inserted = 0
    
    for idx, row in master.iterrows():
        country_id = country_map.get(row['Country of asylum'])
        time_id = year_map.get(int(row['Year']))
        
        if not country_id or not time_id:
            continue
        
        try:
            cursor.execute(
                """
                INSERT INTO fact_refugee_integration 
                (country_id, time_id, refugees_unhcr, asylum_seekers, idps,
                 employment_rate, housing_access, education_enrollment, income_stability,
                 legal_rights_score, social_cohesion, integration_index, 
                 data_source, quality_flag, updated_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    country_id, time_id,
                    int(row['Refugees under UNHCR\'s mandate']) if pd.notna(row['Refugees under UNHCR\'s mandate']) else 0,
                    int(row['Asylum-seekers']) if pd.notna(row['Asylum-seekers']) else 0,
                    0,  # IDPs not in source
                    float(row['employment_rate']) if pd.notna(row['employment_rate']) else 0,
                    float(row['housing_access']) if pd.notna(row['housing_access']) else 0,
                    float(row['education_enrollment']) if pd.notna(row['education_enrollment']) else 0,
                    float(row['income_stability']) if pd.notna(row['income_stability']) else 0,
                    float(row['legal_rights_score']) if pd.notna(row['legal_rights_score']) else 0,
                    float(row['social_cohesion']) if pd.notna(row['social_cohesion']) else 0,
                    float(row['integration_index']) if pd.notna(row['integration_index']) else 0,
                    row['data_source'] if pd.notna(row['data_source']) else 'synthetic',
                    row['quality_flag'] if pd.notna(row['quality_flag']) else 'validated',
                    updated_date
                )
            )
            fact_inserted += 1
        except sqlite3.IntegrityError as e:
            print(f'    ✗ Error at row {idx}: {e}')
            continue
    
    conn.commit()
    print(f'    Inserted {fact_inserted:,} records')
    
    # fact_component_scores
    print('  ▸ fact_component_scores...')
    score_count = 0
    
    for idx, row in master.iterrows():
        country_id = country_map.get(row['Country of asylum'])
        time_id = year_map.get(int(row['Year']))
        
        if not country_id or not time_id:
            continue
        
        for comp_name, comp_id in component_map.items():
            score = row[comp_name] if pd.notna(row[comp_name]) else 0
            contribution = score * weights[comp_id]
            
            try:
                cursor.execute(
                    """
                    INSERT INTO fact_component_scores 
                    (country_id, time_id, component_id, score, contribution)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (country_id, time_id, comp_id, float(score), contribution)
                )
                score_count += 1
            except sqlite3.IntegrityError:
                continue
    
    conn.commit()
    print(f'    Inserted {score_count:,} component scores')

def validate_db(conn):
    """Valider la base de données"""
    print('\n✅ Validation...')
    cursor = conn.cursor()
    
    queries = {
        'fact_refugee_integration': "SELECT COUNT(*) FROM fact_refugee_integration",
        'dim_country': "SELECT COUNT(*) FROM dim_country",
        'dim_time': "SELECT COUNT(*) FROM dim_time",
        'dim_components': "SELECT COUNT(*) FROM dim_components",
        'fact_component_scores': "SELECT COUNT(*) FROM fact_component_scores"
    }
    
    for table, query in queries.items():
        cursor.execute(query)
        count = cursor.fetchone()[0]
        print(f'  {table}: {count:,}')
    
    print(f'\n🎯 Database ready: {DB_PATH}')

def main():
    """Pipeline principal"""
    print('=' * 60)
    print('SQL PIPELINE — Refugee Integration')
    print('=' * 60)
    
    try:
        # Étape 1: Initialiser DB
        print('\n🔧 Initializing Database...')
        init_db()
        
        # Étape 2: Charger données
        master = load_data()
        
        # Étape 3: Connecter et insérer
        conn = sqlite3.connect(DB_PATH)
        
        # Étape 4: Insérer dimensions
        insert_dimensions(conn, master)
        
        # Étape 5: Insérer faits
        insert_facts(conn, master)
        
        # Étape 6: Valider
        validate_db(conn)
        
        conn.close()
        
        print('\n' + '=' * 60)
        print('✅ PIPELINE COMPLETE')
        print('=' * 60)
        
    except Exception as e:
        print(f'\n❌ Error: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()