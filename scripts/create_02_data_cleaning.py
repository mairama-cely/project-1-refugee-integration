import json

notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["# 02_Data_Cleaning — Data Quality & Validation"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["import os\n", "if 'notebooks' in os.getcwd():\n", "    os.chdir('..')\n", "print(f'Working directory: {os.getcwd()}')"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["import pandas as pd\n", "import numpy as np\n", "import matplotlib.pyplot as plt\n", "import seaborn as sns\n", "print('✓ Libraries loaded')"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["master = pd.read_parquet('data/processed/refugee_master_consolidated.parquet')\n", "print(f'Shape: {master.shape}')\n", "print(f'Memory: {master.memory_usage(deep=True).sum() / (1024*1024):.2f} MB')"]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 1. Null Values Analysis"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["nulls = master.isnull().sum()\n", "nulls = nulls[nulls > 0].sort_values(ascending=False)\n", "print('Nulls by column:')\n", "for col, count in nulls.items():\n", "    pct = count / len(master) * 100\n", "    print(f'  {col}: {count} ({pct:.2f}%)')\n", "\n", "if len(nulls) == 0:\n", "    print('  ✓ No nulls found')"]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 2. Outlier Detection"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["components = ['employment_rate', 'housing_access', 'education_enrollment', 'income_stability', 'legal_rights_score', 'social_cohesion']\n", "\n", "print('Outliers (IQR method):')\n", "for col in components:\n", "    Q1 = master[col].quantile(0.25)\n", "    Q3 = master[col].quantile(0.75)\n", "    IQR = Q3 - Q1\n", "    outliers = master[(master[col] < Q1 - 1.5 * IQR) | (master[col] > Q3 + 1.5 * IQR)]\n", "    print(f'  {col}: {len(outliers)} ({len(outliers)/len(master)*100:.2f}%)')"]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 3. Integration Index Validation"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["print('Integration Index Stats:')\n", "print(master['integration_index'].describe().round(2))\n", "\n", "out_of_bounds = master[(master['integration_index'] < 0) | (master['integration_index'] > 100)]\n", "print(f'\\nOut of bounds (0-100): {len(out_of_bounds)}')\n", "print(f'NaN values: {master[\"integration_index\"].isna().sum()}')"]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 4. Completeness Summary"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["completeness = (1 - master.isnull().sum() / len(master)) * 100\n", "print('Data Completeness:')\n", "for col, pct in completeness[completeness < 100].sort_values().items():\n", "    print(f'  {col}: {pct:.1f}%')\n", "\n", "print(f'\\nOverall: {completeness.mean():.1f}%')"]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 5. Final Checklist"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["checks = {\n", "    'No nulls (core)': master[['iso_a3', 'Year', 'integration_index']].isnull().sum().sum() == 0,\n", "    'Index in range': ((master['integration_index'] >= 0) & (master['integration_index'] <= 100)).all(),\n", "    'All countries mapped': master['iso_a3'].notna().all(),\n", "    'Years 2000-2023': ((master['Year'] >= 2000) & (master['Year'] <= 2023)).all(),\n", "    'No duplicates': master.duplicated().sum() == 0\n", "}\n", "\n", "print('Quality Checklist:')\n", "for check, result in checks.items():\n", "    print(f'  {\"✓\" if result else \"✗\"} {check}')\n", "\n", "print(f'\\n{\"✓ ALL PASSED\" if all(checks.values()) else \"✗ ISSUES FOUND\"}')"]
        }
    ],
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11.0"}
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open('notebooks/02_Data_Cleaning.ipynb', 'w') as f:
    json.dump(notebook, f, indent=2)

print('✓ Created: 02_Data_Cleaning.ipynb')