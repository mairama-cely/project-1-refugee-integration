import json

notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["# 04_Geographic_Analysis — Spatial Patterns & Regional Comparison"]
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
            "source": ["import pandas as pd\n", "import numpy as np\n", "import matplotlib.pyplot as plt\n", "import seaborn as sns\n", "import geopandas as gpd\n", "sns.set_style('whitegrid')\n", "print('✓ Libraries loaded')"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["master = pd.read_parquet('data/processed/refugee_master_consolidated.parquet')\n", "print(f'Data shape: {master.shape}')\n", "print(f'Unique countries: {master[\"Country of asylum\"].nunique()}')"]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 1. Regional Statistics"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["# Latest year only\n", "latest = master[master['Year'] == master['Year'].max()]\n", "\n", "regional = latest.groupby('region_un').agg({\n", "    'integration_index': ['mean', 'std', 'min', 'max'],\n", "    'Country of asylum': 'nunique',\n", "    'Refugees under UNHCR\\'s mandate': 'sum'\n", "}).round(2)\n", "\n", "regional.columns = ['Mean Index', 'Std Dev', 'Min', 'Max', 'Countries', 'Total Refugees']\n", "regional = regional.sort_values('Mean Index', ascending=False)\n", "print(regional)"]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 2. Continental Breakdown"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["continental = latest.groupby('continent').agg({\n", "    'integration_index': ['mean', 'std'],\n", "    'Country of asylum': 'nunique',\n", "    'Asylum-seekers': 'sum'\n", "}).round(2)\n", "\n", "continental.columns = ['Mean Index', 'Std Dev', 'Countries', 'Total Asylum-Seekers']\n", "continental = continental.sort_values('Mean Index', ascending=False)\n", "print(continental)"]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 3. Regional Boxplot"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["fig, ax = plt.subplots(figsize=(14, 6))\n", "sns.boxplot(data=latest, x='region_un', y='integration_index', palette='Set2', ax=ax)\n", "ax.set_title('Integration Index by Region (Latest Year)', fontsize=12, fontweight='bold')\n", "ax.set_xlabel('UN Region')\n", "ax.set_ylabel('Integration Index')\n", "plt.xticks(rotation=45, ha='right')\n", "plt.tight_layout()\n", "plt.savefig('output/04_regional_boxplot.png', dpi=300, bbox_inches='tight')\n", "plt.show()\n", "print('✓ Saved: 04_regional_boxplot.png')"]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 4. Top & Bottom Countries"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["country_avg = latest.groupby('Country of asylum')['integration_index'].mean().sort_values()\n", "\n", "print('\\n=== TOP 10 COUNTRIES ===')\n", "for country, index in country_avg.tail(10).items():\n", "    print(f'  {country}: {index:.2f}')\n", "\n", "print('\\n=== BOTTOM 10 COUNTRIES ===')\n", "for country, index in country_avg.head(10).items():\n", "    print(f'  {country}: {index:.2f}')"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 8))\n", "\n", "country_avg.tail(10).plot(kind='barh', color='#2ecc71', ax=ax1)\n", "ax1.set_title('Top 10 Countries by Integration Index', fontsize=11, fontweight='bold')\n", "ax1.set_xlabel('Integration Index')\n", "\n", "country_avg.head(10).plot(kind='barh', color='#e74c3c', ax=ax2)\n", "ax2.set_title('Bottom 10 Countries by Integration Index', fontsize=11, fontweight='bold')\n", "ax2.set_xlabel('Integration Index')\n", "\n", "plt.tight_layout()\n", "plt.savefig('output/04_country_rankings.png', dpi=300, bbox_inches='tight')\n", "plt.show()\n", "print('✓ Saved: 04_country_rankings.png')"]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 5. Refugee Load vs Integration Index"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["fig, ax = plt.subplots(figsize=(12, 7))\n", "scatter = ax.scatter(\n", "    latest['Refugees under UNHCR\\'s mandate'],\n", "    latest['integration_index'],\n", "    s=100,\n", "    alpha=0.6,\n", "    c=latest['integration_index'],\n", "    cmap='RdYlGn'\n", ")\n", "ax.set_xlabel('Number of Refugees')\n", "ax.set_ylabel('Integration Index')\n", "ax.set_title('Refugee Population vs Integration Performance', fontsize=12, fontweight='bold')\n", "plt.colorbar(scatter, label='Integration Index')\n", "\n", "# Add correlation\n", "corr = latest['Refugees under UNHCR\\'s mandate'].corr(latest['integration_index'])\n", "ax.text(0.05, 0.95, f'Correlation: {corr:.3f}', transform=ax.transAxes,\n", "        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))\n", "\n", "plt.tight_layout()\n", "plt.savefig('output/04_refugee_load_vs_index.png', dpi=300, bbox_inches='tight')\n", "plt.show()\n", "print('✓ Saved: 04_refugee_load_vs_index.png')"]
        }
    ],
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11.0"}
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open('notebooks/04_Geographic_Analysis.ipynb', 'w') as f:
    json.dump(notebook, f, indent=2)

print('✓ Created: 04_Geographic_Analysis.ipynb')