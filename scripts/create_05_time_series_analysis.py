import json

notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["# 05_Time_Series_Analysis — Trends Over Time (2000-2023)"]
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
            "source": ["import pandas as pd\n", "import numpy as np\n", "import matplotlib.pyplot as plt\n", "import seaborn as sns\n", "from scipy import stats\n", "sns.set_style('whitegrid')\n", "print('✓ Libraries loaded')"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["master = pd.read_parquet('data/processed/refugee_master_consolidated.parquet')\n", "print(f'Time range: {master[\"Year\"].min()} - {master[\"Year\"].max()}')\n", "print(f'Total records: {len(master)}')"]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 1. Global Integration Index Trend"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["global_trend = master.groupby('Year')['integration_index'].agg(['mean', 'std', 'min', 'max'])\n", "print(global_trend.round(2))"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["fig, ax = plt.subplots(figsize=(12, 6))\n", "ax.plot(global_trend.index, global_trend['mean'], linewidth=2.5, color='#2c3e50', label='Mean')\n", "ax.fill_between(global_trend.index, global_trend['min'], global_trend['max'], alpha=0.2, color='steelblue', label='Min-Max Range')\n", "ax.set_xlabel('Year')\n", "ax.set_ylabel('Integration Index')\n", "ax.set_title('Global Integration Index Trend (2000-2023)', fontsize=12, fontweight='bold')\n", "ax.legend()\n", "ax.grid(True, alpha=0.3)\n", "plt.tight_layout()\n", "plt.savefig('output/05_global_trend.png', dpi=300, bbox_inches='tight')\n", "plt.show()\n", "print('✓ Saved: 05_global_trend.png')"]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 2. Component Trends"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["components = ['employment_rate', 'housing_access', 'education_enrollment', 'income_stability', 'legal_rights_score', 'social_cohesion']\n", "\n", "fig, axes = plt.subplots(2, 3, figsize=(15, 10))\n", "axes = axes.ravel()\n", "\n", "for i, comp in enumerate(components):\n", "    trend = master.groupby('Year')[comp].mean()\n", "    axes[i].plot(trend.index, trend.values, linewidth=2, marker='o')\n", "    axes[i].set_title(f'{comp}', fontsize=10, fontweight='bold')\n", "    axes[i].set_xlabel('Year')\n", "    axes[i].set_ylabel('Score')\n", "    axes[i].grid(True, alpha=0.3)\n", "\n", "plt.tight_layout()\n", "plt.savefig('output/05_component_trends.png', dpi=300, bbox_inches='tight')\n", "plt.show()\n", "print('✓ Saved: 05_component_trends.png')"]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 3. Regional Trend Comparison"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["fig, ax = plt.subplots(figsize=(13, 7))\n", "\n", "for region in master['region_un'].unique():\n", "    if pd.notna(region):\n", "        regional_data = master[master['region_un'] == region].groupby('Year')['integration_index'].mean()\n", "        ax.plot(regional_data.index, regional_data.values, linewidth=2, marker='o', label=region)\n", "\n", "ax.set_xlabel('Year')\n", "ax.set_ylabel('Integration Index')\n", "ax.set_title('Integration Index by Region Over Time', fontsize=12, fontweight='bold')\n", "ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')\n", "ax.grid(True, alpha=0.3)\n", "plt.tight_layout()\n", "plt.savefig('output/05_regional_trends.png', dpi=300, bbox_inches='tight')\n", "plt.show()\n", "print('✓ Saved: 05_regional_trends.png')"]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 4. Refugee Volume Trends"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["volume_trend = master.groupby('Year')[['Refugees under UNHCR\\'s mandate', 'Asylum-seekers']].sum()\n", "\n", "fig, ax = plt.subplots(figsize=(12, 6))\n", "ax.plot(volume_trend.index, volume_trend['Refugees under UNHCR\\'s mandate'] / 1e6, linewidth=2.5, marker='o', label='Refugees (UNHCR)')\n", "ax.plot(volume_trend.index, volume_trend['Asylum-seekers'] / 1e6, linewidth=2.5, marker='s', label='Asylum-seekers')\n", "ax.set_xlabel('Year')\n", "ax.set_ylabel('Population (millions)')\n", "ax.set_title('Refugee & Asylum-Seeker Trends (2000-2023)', fontsize=12, fontweight='bold')\n", "ax.legend()\n", "ax.grid(True, alpha=0.3)\n", "plt.tight_layout()\n", "plt.savefig('output/05_volume_trends.png', dpi=300, bbox_inches='tight')\n", "plt.show()\n", "print('✓ Saved: 05_volume_trends.png')"]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 5. Year-over-Year Change Analysis"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["annual_mean = master.groupby('Year')['integration_index'].mean()\n", "yoy_change = annual_mean.pct_change() * 100\n", "\n", "print('Year-over-Year % Change:')\n", "print(yoy_change.round(2))"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["fig, ax = plt.subplots(figsize=(12, 6))\n", "colors = ['#2ecc71' if x >= 0 else '#e74c3c' for x in yoy_change]\n", "ax.bar(yoy_change.index, yoy_change.values, color=colors, alpha=0.7)\n", "ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)\n", "ax.set_xlabel('Year')\n", "ax.set_ylabel('% Change')\n", "ax.set_title('Year-over-Year Change in Integration Index', fontsize=12, fontweight='bold')\n", "ax.grid(True, alpha=0.3, axis='y')\n", "plt.tight_layout()\n", "plt.savefig('output/05_yoy_change.png', dpi=300, bbox_inches='tight')\n", "plt.show()\n", "print('✓ Saved: 05_yoy_change.png')"]
        }
    ],
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11.0"}
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open('notebooks/05_Time_Series_Analysis.ipynb', 'w') as f:
    json.dump(notebook, f, indent=2)

print('✓ Created: 05_Time_Series_Analysis.ipynb')