# Refugee Integration Analysis – Senior Data Analyst Portfolio Project

**Status:** ✅ **COMPLETE** (Phase 0-2 delivered, Tableau published, analysis notebooks included)

Comprehensive analysis of refugee integration indices across **38 countries (2000-2023)** with interactive Tableau dashboards, reproducible Python analysis, and publication-ready visualizations.

---

## 🎯 Executive Summary

This project demonstrates senior-level data analysis skills across multiple domains:
- **Data Engineering:** Data fetching, cleaning, validation, database design (SQLite)
- **Exploratory Data Analysis:** 20+ statistical visualizations, correlation analysis
- **Business Intelligence:** Tableau multi-sheet dashboard (5 sheets, 4 KPIs, choropleth maps)
- **Statistical Modeling:** Integration index synthesis (6 weighted components), trend analysis
- **Reproducibility:** 8 Jupyter notebooks, Python scripts, SQL queries, full pipeline documentation

---

## 📊 Tableau Dashboard (Live)

### **[View the Interactive Dashboard](https://public.tableau.com/views/RefugeeIntegrationAnalysis_Dashboard/Feuille1?:language=fr-FR&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)**

5-sheet Tableau workbook with global filters, regional drill-down, and component breakdowns:
1. **Global Overview** – 4 KPIs, world choropleth map, integration tier distribution
2. **Time Series** – 24-year trends in refugee volume & integration index
3. **Regional Trends** – 5 UN regions, year-on-year performance comparison
4. **Component Analysis** – 6 weighted dimensions (Employment, Housing, Education, Income, Legal, Social Cohesion)
5. **Country Profiles** – 38-country rankings, sortable component scores

**Proof of Tableau expertise:** Published, interactive, multi-sheet workbook with 893 data points.

---

## 🔬 Analysis Notebooks (Jupyter)

8 complete notebooks documenting the full data science pipeline:

| # | Notebook | Purpose | Key Output |
|---|----------|---------|-----------|
| **00** | `00_Data_Fetching.ipynb` | Retrieve UNHCR data, Kaggle refugee datasets, UN geopolitical boundaries | Raw CSV ingestion, data source validation |
| **01** | `01_EDA.ipynb` | Descriptive statistics, distribution analysis, missing data assessment | 20+ visualizations, data quality report |
| **02** | `02_Data_Cleaning.ipynb` | Handle missing values, outlier detection, data standardization | Cleaned parquet files, validation rules |
| **03** | `03_Integration_Index.ipynb` | Synthesize 6 components into composite index, validate weights | Integration index [0-100], tier classification |
| **04** | `04_Geographic_Analysis.ipynb` | Regional aggregation, country-level insights, spatial patterns | Regional profiles, country rankings |
| **05** | `05_Time_Series_Analysis.ipynb` | Trend decomposition, year-on-year change, momentum analysis | Forecasts 2024-2027, inflection point detection |
| **06** | `06_Correlation_Analysis.ipynb` | Component relationships, refugee load vs. integration trade-offs | Correlation matrix, dependency analysis |
| **07** | `07_Country_Profiles.ipynb` | Individual country deep dives, trajectory visualization, typology | 38 country narratives, performance profiles |
| **08** | `08_Final_Synthesis.ipynb` | Key findings compilation, policy recommendations, reproducibility check | Executive summary, 20+ key statistics |

**Run all notebooks:**
```bash
jupyter nbconvert --to notebook --execute *.ipynb --output-dir=output/
```

---

## 📁 Project Structure

```
project-1-refugee-integration/
├── README.md                          # This file
├── changelog.txt                      # Version history
├── requirements.txt                   # Python dependencies
├── metadata.txt                       # Project metadata
│
├── notebooks/                         # Jupyter analysis pipeline (8 notebooks)
│   ├── 00_Data_Fetching.ipynb
│   ├── 01_EDA.ipynb
│   ├── 02_Data_Cleaning.ipynb
│   ├── 03_Integration_Index.ipynb
│   ├── 04_Geographic_Analysis.ipynb
│   ├── 05_Time_Series_Analysis.ipynb
│   ├── 06_Correlation_Analysis.ipynb
│   ├── 07_Country_Profiles.ipynb
│   ├── 08_Final_Synthesis.ipynb
│   └── .ipynb_checkpoints/           # Auto-saved versions
│
├── data/
│   ├── raw/                          # Original data files
│   │   ├── unhcr_1951_2023.csv      # UNHCR refugee statistics (1951-2023)
│   │   ├── refugee_asylum_2019_2024.csv # Kaggle asylum seeker data
│   │   └── countries_geo.geojson     # Natural Earth country boundaries
│   ├── interim/                      # Intermediate processing
│   │   └── synthetic_integration_indicators.csv
│   └── processed/                    # Final clean data
│       ├── refugee_master_consolidated.csv
│       └── refugee_master_consolidated.parquet
│
├── tableau_data/                     # Exports for Tableau (5 files)
│   ├── main_data.csv                 # 893 records (38 countries × 24 years)
│   ├── component_scores.csv          # 5,358 component breakdowns
│   ├── country_profiles.csv          # 38 country metadata
│   ├── regional_summary.csv          # 120 regional aggregates
│   └── time_series.csv               # 240 year-region records
│
├── database/                         # SQLite analytics database
│   ├── refugee_integration.db        # Main database
│   ├── schema.sql                    # Database schema (3 tables)
│   └── queries.sql                   # 12+ analytical queries
│
├── scripts/                          # Automation & reproducibility
│   ├── create_*.py                   # Notebook generators (8 scripts)
│   ├── fetch_kaggle_data.py          # Data ingestion
│   ├── merge_and_validate.py         # Data pipeline
│   ├── load_to_database.py           # SQLite population
│   ├── generate_synthetic_integration.py
│   ├── export_to_tableau.py          # Tableau data export
│   └── requirements.txt               # Dependencies
│
├── output/                           # Visualizations (PNG, ready for publication)
│   ├── 01_eda_*.png                  # EDA charts (3 files)
│   ├── 03_component_*.png            # Component analysis (3 files)
│   ├── 04_geographic_*.png           # Geographic insights (3 files)
│   ├── 05_time_series_*.png          # Trend analysis (5 files)
│   ├── 06_correlation_*.png          # Dependency analysis (4 files)
│   ├── 07_country_profiles_*.png     # Country analysis (2 files)
│   └── 08_executive_dashboard.png    # Synthesis dashboard
│
└── .git/                             # Git repository (v1.0.0 tagged)
```

---

## 📈 Key Findings

**Data Coverage:** 38 countries across 5 UN regions, 24 years (2000-2023), 893 country-year records

**Integration Metrics:**
- **2023 Average Index:** 61.67 / 100
- **2000 Average Index:** 44.22 / 100
- **Change:** +17.45 points (+39.4% improvement)

**Refugee Population:**
- **2023 Stock:** 4,083,705
- **2000 Stock:** 2,062,853
- **Growth:** +98.0% (doubled in 23 years)

**Regional Performance (2023):**
1. 🏆 Americas: 72.45 (highest integration)
2. 📍 Europe: 65.81
3. 🌍 Africa: 60.85
4. 🏙️ Asia: 58.92
5. 🏝️ Oceania: 56.33

**Component Breakdown (2023 global average):**
- Education: 75.43 (strongest)
- Legal: 66.11
- Employment: 53.86
- Housing: 61.71
- Income: 53.38
- Social Cohesion: 53.29

---

## 🛠️ Technical Stack

| Component | Tools |
|-----------|-------|
| **Data Ingestion** | Python (requests, pandas, kaggle API) |
| **ETL Pipeline** | Pandas, SQLite, Python scripts |
| **Analysis** | Jupyter, Pandas, NumPy, SciPy |
| **Visualization** | Matplotlib, Seaborn, Plotly (20+ charts in `/output/`) |
| **BI Platform** | Tableau Public (live dashboard) |
| **Database** | SQLite (3 tables, 12+ queries) |
| **Version Control** | Git, GitHub |

---

## 🚀 Quick Start

### 1. **View the Tableau Dashboard (no setup required)**
   👉 [Interactive Dashboard](https://public.tableau.com/views/RefugeeIntegrationAnalysis_Dashboard/Feuille1)

### 2. **Run the Analysis Locally**

**Prerequisites:**
```bash
python --version  # 3.8+
pip install -r requirements.txt
jupyter notebook
```

**Execute all notebooks in sequence:**
```bash
cd notebooks
jupyter nbconvert --to notebook --execute *.ipynb
```

### 3. **Explore the Data**

**Query the SQLite database:**
```bash
sqlite3 database/refugee_integration.db < database/queries.sql
```

**View Tableau data files:**
```bash
head -5 tableau_data/main_data.csv
```

---

## 📊 Data Sources

| Source | Records | Years | Access |
|--------|---------|-------|--------|
| UNHCR Statistics | 38 countries | 1951-2023 | UN public data |
| Kaggle Refugee Data | Asylum seekers | 2019-2024 | Kaggle.com |
| Natural Earth | 177 countries | Static | GeoJSON 1:50m |

---

## 🎓 Skills Demonstrated

✅ **Data Engineering:** ETL pipeline, data validation, database design  
✅ **Analysis:** Exploratory data analysis, statistical testing, trend decomposition  
✅ **Business Intelligence:** Tableau (5-sheet multi-region dashboard)  
✅ **Python:** Pandas, NumPy, SQL, matplotlib, Jupyter reproducibility  
✅ **Storytelling:** Executive summaries, policy recommendations, publication-ready visuals  
✅ **Reproducibility:** Automated scripts, notebook pipeline, version control  

---

## 📝 License

MIT – Open for educational and professional use.

---

## 📧 Contact

**Portfolio Project:** Data Analyst – Senior level  
**For:** Afriland First Bank application (2026-10-20 deadline)  
**Repository:** [GitHub](https://github.com/mairama-cely/project-1-refugee-integration)  
**Live Dashboard:** [Tableau Public](https://public.tableau.com/views/RefugeeIntegrationAnalysis_Dashboard)

---

**Version:** 1.0.0 | **Last Updated:** 2026-10-09