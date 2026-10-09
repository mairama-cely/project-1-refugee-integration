-- Drop existing objects
DROP VIEW IF EXISTS vw_component_contribution;
DROP VIEW IF EXISTS vw_country_ranking;
DROP VIEW IF EXISTS vw_regional_summary;
DROP TABLE IF EXISTS fact_component_scores;
DROP TABLE IF EXISTS fact_refugee_integration;
DROP TABLE IF EXISTS dim_integration_tier;
DROP TABLE IF EXISTS dim_components;
DROP TABLE IF EXISTS dim_country;
DROP TABLE IF EXISTS dim_time;

-- Dimension: Time
CREATE TABLE dim_time (
    time_id INTEGER PRIMARY KEY,
    year INTEGER NOT NULL UNIQUE,
    decade TEXT,
    period_label TEXT
);

-- Dimension: Country
CREATE TABLE dim_country (
    country_id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_name TEXT NOT NULL UNIQUE,
    iso_a3 TEXT UNIQUE,
    continent TEXT,
    region_un TEXT
);

-- Dimension: Integration Components
CREATE TABLE dim_components (
    component_id INTEGER PRIMARY KEY AUTOINCREMENT,
    component_name TEXT NOT NULL UNIQUE,
    component_code TEXT UNIQUE,
    weight REAL,
    description TEXT
);

-- Fact Table: Refugee Statistics
CREATE TABLE fact_refugee_integration (
    fact_id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_id INTEGER NOT NULL,
    time_id INTEGER NOT NULL,
    refugees_unhcr INTEGER,
    asylum_seekers INTEGER,
    idps INTEGER,
    employment_rate REAL,
    housing_access REAL,
    education_enrollment REAL,
    income_stability REAL,
    legal_rights_score REAL,
    social_cohesion REAL,
    integration_index REAL,
    data_source TEXT,
    quality_flag TEXT,
    updated_date TEXT,
    FOREIGN KEY (country_id) REFERENCES dim_country(country_id),
    FOREIGN KEY (time_id) REFERENCES dim_time(time_id),
    UNIQUE (country_id, time_id)
);

-- Dimension: Integration Tiers
CREATE TABLE dim_integration_tier (
    tier_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tier_name TEXT NOT NULL UNIQUE,
    min_score REAL,
    max_score REAL,
    description TEXT
);

-- Bridge Table: Component Details (Denormalized for analytics)
CREATE TABLE fact_component_scores (
    component_score_id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_id INTEGER NOT NULL,
    time_id INTEGER NOT NULL,
    component_id INTEGER NOT NULL,
    score REAL,
    contribution REAL,
    FOREIGN KEY (country_id) REFERENCES dim_country(country_id),
    FOREIGN KEY (time_id) REFERENCES dim_time(time_id),
    FOREIGN KEY (component_id) REFERENCES dim_components(component_id)
);

-- Indexes for Performance
CREATE INDEX idx_fact_country ON fact_refugee_integration(country_id);
CREATE INDEX idx_fact_time ON fact_refugee_integration(time_id);
CREATE INDEX idx_fact_integration_index ON fact_refugee_integration(integration_index);
CREATE INDEX idx_fact_country_time ON fact_refugee_integration(country_id, time_id);
CREATE INDEX idx_component_scores_country ON fact_component_scores(country_id);
CREATE INDEX idx_component_scores_time ON fact_component_scores(time_id);

-- Views for Analytics
CREATE VIEW vw_regional_summary AS
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
GROUP BY c.region_un, t.year;

CREATE VIEW vw_country_ranking AS
SELECT 
    c.country_name,
    c.continent,
    c.region_un,
    ROUND(AVG(f.integration_index), 2) as avg_index,
    ROUND(STDDEV(f.integration_index), 2) as stddev_index,
    COUNT(DISTINCT f.time_id) as num_years,
    SUM(f.refugees_unhcr) as total_refugees
FROM fact_refugee_integration f
JOIN dim_country c ON f.country_id = c.country_id
GROUP BY f.country_id
ORDER BY avg_index DESC;

CREATE VIEW vw_component_contribution AS
SELECT 
    c.component_name,
    c.weight,
    ROUND(AVG(fc.score), 2) as avg_score,
    ROUND(AVG(fc.contribution), 2) as avg_contribution,
    COUNT(DISTINCT fc.country_id) as countries_covered
FROM fact_component_scores fc
JOIN dim_components c ON fc.component_id = c.component_id
GROUP BY fc.component_id
ORDER BY avg_contribution DESC;