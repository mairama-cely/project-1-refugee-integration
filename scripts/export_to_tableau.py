import sqlite3
import pandas as pd
import os

DB_PATH = 'database/refugee_integration.db'
EXPORT_DIR = 'tableau_data'

os.makedirs(EXPORT_DIR, exist_ok=True)

print('📊 Exporting data for Tableau...\n')

conn = sqlite3.connect(DB_PATH)

# Query 1: Main Fact Table + Dimensions
query_main = """
SELECT 
    f.fact_id,
    c.country_name,
    c.iso_a3,
    c.continent,
    c.region_un,
    t.year,
    f.refugees_unhcr,
    f.asylum_seekers,
    f.employment_rate,
    f.housing_access,
    f.education_enrollment,
    f.income_stability,
    f.legal_rights_score,
    f.social_cohesion,
    ROUND(f.integration_index, 2) as integration_index,
    CASE 
        WHEN f.integration_index >= 70 THEN 'High'
        WHEN f.integration_index >= 50 THEN 'Medium'
        ELSE 'Low'
    END as integration_tier,
    f.data_source,
    f.quality_flag,
    f.updated_date
FROM fact_refugee_integration f
JOIN dim_country c ON f.country_id = c.country_id
JOIN dim_time t ON f.time_id = t.time_id
ORDER BY t.year DESC, c.country_name
"""

print('  ▸ Exporting main_data...')
df_main = pd.read_sql_query(query_main, conn)
df_main.to_csv(f'{EXPORT_DIR}/main_data.csv', index=False)
print(f'    → {len(df_main):,} rows')

# Query 2: Regional Summary
query_regional = """
SELECT 
    c.region_un,
    t.year,
    COUNT(DISTINCT f.country_id) as num_countries,
    ROUND(AVG(f.integration_index), 2) as avg_integration_index,
    ROUND(MIN(f.integration_index), 2) as min_index,
    ROUND(MAX(f.integration_index), 2) as max_index,
    SUM(f.refugees_unhcr) as total_refugees,
    SUM(f.asylum_seekers) as total_asylum_seekers
FROM fact_refugee_integration f
JOIN dim_country c ON f.country_id = c.country_id
JOIN dim_time t ON f.time_id = t.time_id
GROUP BY c.region_un, t.year
ORDER BY t.year DESC, avg_integration_index DESC
"""

print('  ▣ Exporting regional_summary...')
df_regional = pd.read_sql_query(query_regional, conn)
df_regional.to_csv(f'{EXPORT_DIR}/regional_summary.csv', index=False)
print(f'    → {len(df_regional):,} rows')

# Query 3: Component Scores (Tidy Format)
query_components = """
SELECT 
    c.country_name,
    c.region_un,
    t.year,
    comp.component_name,
    ROUND(fc.score, 2) as score,
    ROUND(fc.contribution, 2) as contribution
FROM fact_component_scores fc
JOIN dim_country c ON fc.country_id = c.country_id
JOIN dim_time t ON fc.time_id = t.time_id
JOIN dim_components comp ON fc.component_id = comp.component_id
ORDER BY t.year DESC, c.country_name, comp.component_id
"""

print('  ▣ Exporting component_scores...')
df_components = pd.read_sql_query(query_components, conn)
df_components.to_csv(f'{EXPORT_DIR}/component_scores.csv', index=False)
print(f'    → {len(df_components):,} rows')

# Query 4: Country Profiles
query_profiles = """
SELECT 
    c.country_name,
    c.iso_a3,
    c.continent,
    c.region_un,
    COUNT(DISTINCT f.time_id) as years_covered,
    ROUND(AVG(f.integration_index), 2) as avg_integration_index,
    ROUND(MIN(f.integration_index), 2) as min_index,
    ROUND(MAX(f.integration_index), 2) as max_index,
    ROUND(AVG(f.employment_rate), 2) as avg_employment,
    ROUND(AVG(f.housing_access), 2) as avg_housing,
    ROUND(AVG(f.education_enrollment), 2) as avg_education,
    ROUND(AVG(f.income_stability), 2) as avg_income,
    ROUND(AVG(f.legal_rights_score), 2) as avg_legal_rights,
    ROUND(AVG(f.social_cohesion), 2) as avg_social_cohesion,
    SUM(f.refugees_unhcr) as total_refugees
FROM fact_refugee_integration f
JOIN dim_country c ON f.country_id = c.country_id
GROUP BY f.country_id
ORDER BY avg_integration_index DESC
"""

print('  ▣ Exporting country_profiles...')
df_profiles = pd.read_sql_query(query_profiles, conn)
df_profiles.to_csv(f'{EXPORT_DIR}/country_profiles.csv', index=False)
print(f'    → {len(df_profiles):,} rows')

# Query 5: Time Series
query_timeseries = """
SELECT 
    t.year,
    ROUND(AVG(f.integration_index), 2) as global_avg_index,
    ROUND(AVG(f.employment_rate), 2) as avg_employment,
    ROUND(AVG(f.housing_access), 2) as avg_housing,
    ROUND(AVG(f.education_enrollment), 2) as avg_education,
    ROUND(AVG(f.income_stability), 2) as avg_income,
    ROUND(AVG(f.legal_rights_score), 2) as avg_legal_rights,
    ROUND(AVG(f.social_cohesion), 2) as avg_social_cohesion,
    SUM(f.refugees_unhcr) as total_refugees,
    SUM(f.asylum_seekers) as total_asylum_seekers,
    COUNT(DISTINCT f.country_id) as countries_covered
FROM fact_refugee_integration f
JOIN dim_time t ON f.time_id = t.time_id
GROUP BY t.year
ORDER BY t.year ASC
"""

print('  ▣ Exporting time_series...')
df_timeseries = pd.read_sql_query(query_timeseries, conn)
df_timeseries.to_csv(f'{EXPORT_DIR}/time_series.csv', index=False)
print(f'    → {len(df_timeseries):,} rows')

conn.close()

print(f'\n✅ Export Complete')
print(f'Location: {os.path.abspath(EXPORT_DIR)}')
print(f'\nFiles ready for Tableau:')
print(f'  • main_data.csv')
print(f'  • regional_summary.csv')
print(f'  • component_scores.csv')
print(f'  • country_profiles.csv')
print(f'  • time_series.csv')
print(f'\n✓ Integration Index normalized (0-100)')