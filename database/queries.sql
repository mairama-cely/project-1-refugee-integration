-- 1. Regional Performance Summary
SELECT 
    region_un,
    year,
    ROUND(AVG(integration_index), 2) as avg_index,
    COUNT(DISTINCT country_id) as countries
FROM fact_refugee_integration f
JOIN dim_country c ON f.country_id = c.country_id
GROUP BY region_un, year
ORDER BY year DESC, avg_index DESC;

-- 2. Top 10 Countries (All Time)
SELECT 
    c.country_name,
    c.continent,
    ROUND(AVG(f.integration_index), 2) as avg_index,
    SUM(f.refugees_unhcr) as total_refugees,
    COUNT(DISTINCT f.time_id) as years_covered
FROM fact_refugee_integration f
JOIN dim_country c ON f.country_id = c.country_id
GROUP BY f.country_id
ORDER BY avg_index DESC
LIMIT 10;

-- 3. Component Performance (Latest Year)
SELECT 
    c.component_name,
    ROUND(AVG(fc.score), 2) as avg_score,
    ROUND(AVG(fc.contribution), 2) as avg_contribution,
    COUNT(DISTINCT fc.country_id) as countries
FROM fact_component_scores fc
JOIN dim_components c ON fc.component_id = c.component_id
JOIN dim_time t ON fc.time_id = t.time_id
WHERE t.year = (SELECT MAX(year) FROM dim_time)
GROUP BY fc.component_id
ORDER BY avg_contribution DESC;

-- 4. Trend Analysis (2000 vs Latest)
WITH yearly_stats AS (
    SELECT 
        t.year,
        ROUND(AVG(f.integration_index), 2) as avg_index
    FROM fact_refugee_integration f
    JOIN dim_time t ON f.time_id = t.time_id
    GROUP BY t.year
)
SELECT 
    'Global' as metric,
    (SELECT avg_index FROM yearly_stats WHERE year = 2000) as year_2000,
    (SELECT avg_index FROM yearly_stats WHERE year = (SELECT MAX(year) FROM yearly_stats)) as latest,
    ROUND(((SELECT avg_index FROM yearly_stats WHERE year = (SELECT MAX(year) FROM yearly_stats)) - 
           (SELECT avg_index FROM yearly_stats WHERE year = 2000)), 2) as change;

-- 5. Countries by Integration Tier (Latest Year)
SELECT 
    dt.tier_name,
    COUNT(DISTINCT f.country_id) as count,
    GROUP_CONCAT(c.country_name, ', ') as countries
FROM fact_refugee_integration f
JOIN dim_country c ON f.country_id = c.country_id
JOIN dim_time t ON f.time_id = t.time_id
JOIN dim_integration_tier dt ON f.integration_index BETWEEN dt.min_score AND dt.max_score
WHERE t.year = (SELECT MAX(year) FROM dim_time)
GROUP BY dt.tier_name
ORDER BY dt.max_score DESC;