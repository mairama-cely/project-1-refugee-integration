import json

notebook = {
    "cells": [
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["import os\n", "if 'notebooks' in os.getcwd():\n", "    os.chdir('..')\n", "print(f'Working directory: {os.getcwd()}')"]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["# 01_EDA — Exploratory Data Analysis"]
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
            "source": ["master = pd.read_parquet('data/processed/refugee_master_consolidated.parquet')\n", "print(f'Shape: {master.shape}')\n", "print(f'Columns: {len(master.columns)}')"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["print('Integration Index Distribution:')\n", "print(master['integration_index'].describe().round(2))"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["plt.figure(figsize=(10, 5))\n", "plt.hist(master['integration_index'], bins=30, edgecolor='black')\n", "plt.title('Distribution: Integration Index')\n", "plt.xlabel('Integration Index')\n", "plt.ylabel('Frequency')\n", "plt.grid(True, alpha=0.3)\n", "plt.show()"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["yearly_avg = master.groupby('Year')['integration_index'].mean()\n", "plt.figure(figsize=(12, 5))\n", "plt.plot(yearly_avg.index, yearly_avg.values, marker='o')\n", "plt.title('Trend: Integration Index by Year')\n", "plt.xlabel('Year')\n", "plt.ylabel('Avg Integration Index')\n", "plt.grid(True, alpha=0.3)\n", "plt.show()"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["components = ['employment_rate', 'housing_access', 'education_enrollment', 'income_stability', 'legal_rights_score', 'social_cohesion']\n", "corr = master[components].corr()\n", "plt.figure(figsize=(8, 6))\n", "sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, fmt='.2f')\n", "plt.title('Correlation: Components')\n", "plt.show()"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["print('Top 10 countries:')\n", "print(master.groupby('country_name')['integration_index'].mean().nlargest(10).round(2))"]
        }
    ],
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11.0"}
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open('notebooks/01_EDA.ipynb', 'w') as f:
    json.dump(notebook, f, indent=2)

print('✓ Created: 01_EDA.ipynb')