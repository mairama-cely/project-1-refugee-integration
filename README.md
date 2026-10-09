# Refugee Integration Analysis — Project 1

## Overview
Entry-level portfolio project: Analyzing refugee data from Kaggle (UNHCR 1951-2023 + Recent 2019-2024) combined with synthetically-generated integration indicators (employment, housing, education, income, legal rights, social cohesion).

**Output:** Composite integration index (0-100) by country & year.

## Data Sources
- **UNHCR Historical:** `avtnshm/united-nations-refugee-data-unhcr` (1951-2023, 70 years)
- **Recent Asylum:** `nafayunnoor/global-refugee-and-asylum-seeker-data-2019-2024` (2019-2024)
- **Synthetic Integration:** Generated locally (employment rate, housing access, education enrollment, income stability, legal rights, social cohesion)
- **Geography:** GeoPandas Natural Earth (countries, centroids, regions)

## Project Structure

project-1-refugee-integration/
├── data/
│ ├── raw/ # Kaggle downloads
│ ├── processed/ # Final merged tables
│ └── final/ # Outputs for analysis
├── scripts/
│ ├── fetch_kaggle_data.py
│ ├── generate_synthetic_integration.py
│ └── merge_and_validate.py
├── notebooks/
│ └── 00_Data_Fetching.ipynb
├── database/
├── docs/
├── output/
├── tests/
├── venv/
├── requirements.txt
├── README.md
├── METADATA.md
└── CHANGELOG.md


## Setup

```bash
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure Kaggle (put kaggle.json in ~/.kaggle/)
# Download from: https://www.kaggle.com/settings/account

# 4. Run pipeline
python scripts/fetch_kaggle_data.py
python scripts/generate_synthetic_integration.py
python scripts/merge_and_validate.py
```

## Phase Timeline
- **Phase 2 (Weeks 3-5):** Data fetching, EDA, cleaning
- **Phase 3 (Weeks 6-8):** Dashboard (Tableau/Power BI)
- **Phase 4 (Weeks 9-12):** Medium article, website, GitHub release

## Key Metrics
- Integration Index = 0.20×employment + 0.15×housing + 0.20×education + 0.15×income + 0.20×rights + 0.10×cohesion
- Coverage: 50 countries × 24 years = 1,200 records
- Temporal: 2000-2023

## Career Level
Entry-level portfolio: Focus on project structure, EDA, visualization, storytelling.

