import json

notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["# 07_Country_Profiles — Detailed Performance Snapshots"]
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
            "source": ["import pandas as pd\n", "import numpy as np\n", "import matplotlib.pyplot as plt\n", "import seaborn as sns\n", "sns.set_style('whitegrid')\n", "print('✓ Libraries loaded')"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["master = pd.read_parquet('data/processed/refugee_master_consolidated.parquet')\n", "latest_year = master['Year'].max()\n", "latest = master[master['Year'] == latest_year]\n", "print(f'Latest year: {latest_year}')\n", "print(f'Countries in snapshot: {latest[\"Country of asylum\"].nunique()}')"]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 1. Top 5 Countries Deep Dive"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["top_5 = latest.nlargest(5, 'integration_index')[['Country of asylum', 'integration_index', 'employment_rate', 'housing_access', 'education_enrollment', 'income_stability', 'legal_rights_score', 'social_cohesion', 'Refugees under UNHCR\\'s mandate']]\n", "print('\\n=== TOP 5 COUNTRIES ===')\n", "for idx, row in top_5.iterrows():\n", "    print(f\"\\n{row['Country of asylum']}\")\n", "    print(f\"  Integration Index: {row['integration_index']:.2f}\")\n", "    print(f\"  Employment: {row['employment_rate']:.1f} | Housing: {row['housing_access']:.1f} | Education: {row['education_enrollment']:.1f}\")\n", "    print(f\"  Income Stability: {row['income_stability']:.1f} | Legal Rights: {row['legal_rights_score']:.1f} | Social Cohesion: {row['social_cohesion']:.1f}\")\n", "    print(f\"  Refugee Population: {row['Refugees under UNHCR\\'s mandate']:,.0f}\")"]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 2. Component Radar Chart - Top 3 Countries"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["from math import pi\n", "\n", "top_3_countries = latest.nlargest(3, 'integration_index')['Country of asylum'].tolist()\n", "categories = ['Employment', 'Housing', 'Education', 'Income', 'Legal Rights', 'Social Cohesion']\n", "components = ['employment_rate', 'housing_access', 'education_enrollment', 'income_stability', 'legal_rights_score', 'social_cohesion']\n", "\n", "fig, axes = plt.subplots(1, 3, figsize=(15, 5), subplot_kw=dict(projection='polar'))\n", "axes = axes.ravel()\n", "\n", "angles = [n / len(categories) * 2 * pi for n in range(len(categories))]\n", "angles += angles[:1]\n", "\n", "for i, country in enumerate(top_3_countries):\n", "    country_data = latest[latest['Country of asylum'] == country][components].values[0].tolist()\n", "    country_data += country_data[:1]\n", "    \n", "    axes[i].plot(angles, country_data, 'o-', linewidth=2)\n", "    axes[i].fill(angles, country_data, alpha=0.25)\n", "    axes[i].set_xticks(angles[:-1])\n", "    axes[i].set_xticklabels(categories, size=9)\n", "    axes[i].set_ylim(0, 100)\n", "    axes[i].set_title(country, fontsize=11, fontweight='bold')\n", "\n", "plt.tight_layout()\n", "plt.savefig('output/07_top3_radar_charts.png', dpi=300, bbox_inches='tight')\n", "plt.show()\n", "print('✓ Saved: 07_top3_radar_charts.png')"]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 3. Weakest 5 Countries Analysis"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["bottom_5 = latest.nsmallest(5, 'integration_index')[['Country of asylum', 'integration_index', 'employment_rate', 'housing_access', 'education_enrollment', 'income_stability', 'legal_rights_score', 'social_cohesion']]\n", "print('\\n=== BOTTOM 5 COUNTRIES ===')\n", "for idx, row in bottom_5.iterrows():\n", "    print(f\"\\n{row['Country of asylum']}\")\n", "    print(f\"  Integration Index: {row['integration_index']:.2f}\")\n", "    print(f\"  Employment: {row['employment_rate']:.1f} | Housing: {row['housing_access']:.1f} | Education: {row['education_enrollment']:.1f}\")\n", "    print(f\"  Income Stability: {row['income_stability']:.1f} | Legal Rights: {row['legal_rights_score']:.1f} | Social Cohesion: {row['social_cohesion']:.1f}\")"]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 4. Country Trajectories (Last 10 Years)"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["recent_years = master[master['Year'] >= 2014].groupby(['Country of asylum', 'Year'])['integration_index'].mean().unstack()\n", "\n", "# Select top 10 improving countries\n", "improvement = recent_years.iloc[:, -1] - recent_years.iloc[:, 0]\n", "top_improvers = improvement.nlargest(5)\n", "\n", "fig, ax = plt.subplots(figsize=(12, 6))\n", "for country in top_improvers.index:\n", "    if country in recent_years.index:\n", "        ax.plot(recent_years.columns, recent_years.loc[country], marker='o', linewidth=2, label=country)\n", "\n", "ax.set_xlabel('Year')\n", "ax.set_ylabel('Integration Index')\n", "ax.set_title('Top 5 Most Improving Countries (2014-2023)', fontsize=12, fontweight='bold')\n", "ax.legend()\n", "ax.grid(True, alpha=0.3)\n", "plt.tight_layout()\n", "plt.savefig('output/07_improving_countries.png', dpi=300, bbox_inches='tight')\n", "plt.show()\n", "print('✓ Saved: 07_improving_countries.png')"]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 5. Regional Country Rankings"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["regional_rankings = latest.groupby('region_un')[['Country of asylum', 'integration_index']].apply(lambda x: x.nlargest(3, 'integration_index')).reset_index(drop=True)\n", "print('\\n=== TOP 3 COUNTRIES PER REGION ===')\n", "for region in latest['region_un'].unique():\n", "    if pd.notna(region):\n", "        region_data = latest[latest['region_un'] == region].nlargest(3, 'integration_index')\n", "        print(f\"\\n{region}:\")\n", "        for idx, row in region_data.iterrows():\n", "            print(f\"  {row['Country of asylum']}: {row['integration_index']:.2f}\")"]
        }
    ],
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11.0"}
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open('notebooks/07_Country_Profiles.ipynb', 'w') as f:
    json.dump(notebook, f, indent=2)

print('✓ Created: 07_Country_Profiles.ipynb')