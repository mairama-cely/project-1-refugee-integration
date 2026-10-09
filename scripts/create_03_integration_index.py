import json

notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["# 03_Integration_Index — Component Analysis & Decomposition"]
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
            "source": ["master = pd.read_parquet('data/processed/refugee_master_consolidated.parquet')\n", "print(f'Loaded: {master.shape}')\n", "print(f'Index range: {master[\"integration_index\"].min():.2f} - {master[\"integration_index\"].max():.2f}')"]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 1. Integration Index Formula & Weights"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["weights = {\n", "    'employment_rate': 0.20,\n", "    'housing_access': 0.15,\n", "    'education_enrollment': 0.20,\n", "    'income_stability': 0.15,\n", "    'legal_rights_score': 0.20,\n", "    'social_cohesion': 0.10\n", "}\n", "\n", "print('Integration Index Formula:')\n", "print('integration_index = (')\n", "for component, weight in weights.items():\n", "    print(f'    {component} × {weight} +')\n", "print(')')\n", "print(f'\\nTotal weight: {sum(weights.values())}')"]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 2. Component Distributions"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["components = list(weights.keys())\n", "stats = master[components].describe().round(2)\n", "print(stats)"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["fig, axes = plt.subplots(2, 3, figsize=(14, 8))\n", "axes = axes.ravel()\n", "\n", "for i, comp in enumerate(components):\n", "    axes[i].hist(master[comp], bins=30, color='steelblue', edgecolor='black')\n", "    axes[i].set_title(f'{comp}\\n(weight: {weights[comp]})', fontsize=10)\n", "    axes[i].set_xlabel('Score')\n", "    axes[i].set_ylabel('Frequency')\n", "\n", "plt.tight_layout()\n", "plt.savefig('output/03_component_distributions.png', dpi=300, bbox_inches='tight')\n", "plt.show()\n", "print('✓ Saved: 03_component_distributions.png')"]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 3. Weighted Contribution Analysis"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["# Calculate individual contributions\n", "contributions = pd.DataFrame()\n", "for comp, weight in weights.items():\n", "    contributions[comp] = master[comp] * weight\n", "\n", "contributions['total'] = contributions.sum(axis=1)\n", "print('Contribution stats (in final index points):')\n", "print(contributions.describe().round(2))"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["# Average contribution per component\n", "avg_contributions = contributions[components].mean().sort_values(ascending=False)\n", "fig, ax = plt.subplots(figsize=(10, 6))\n", "avg_contributions.plot(kind='barh', color='coral', ax=ax)\n", "ax.set_title('Average Contribution to Integration Index', fontsize=12, fontweight='bold')\n", "ax.set_xlabel('Average Points Contributed')\n", "plt.tight_layout()\n", "plt.savefig('output/03_contribution_analysis.png', dpi=300, bbox_inches='tight')\n", "plt.show()\n", "print('✓ Saved: 03_contribution_analysis.png')"]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 4. Index Tiers Classification"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["def classify_integration(score):\n", "    if score >= 70:\n", "        return 'High'\n", "    elif score >= 50:\n", "        return 'Medium'\n", "    else:\n", "        return 'Low'\n", "\n", "master['integration_tier'] = master['integration_index'].apply(classify_integration)\n", "\n", "tier_dist = master['integration_tier'].value_counts()\n", "print('Integration Tier Distribution:')\n", "for tier, count in tier_dist.items():\n", "    pct = count / len(master) * 100\n", "    print(f'  {tier}: {count} ({pct:.1f}%)')"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["fig, ax = plt.subplots(figsize=(8, 6))\n", "tier_dist.plot(kind='pie', autopct='%1.1f%%', colors=['#2ecc71', '#f39c12', '#e74c3c'], ax=ax)\n", "ax.set_ylabel('')\n", "ax.set_title('Integration Index Tiers', fontsize=12, fontweight='bold')\n", "plt.tight_layout()\n", "plt.savefig('output/03_integration_tiers.png', dpi=300, bbox_inches='tight')\n", "plt.show()\n", "print('✓ Saved: 03_integration_tiers.png')"]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 5. Summary Table"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["summary = pd.DataFrame({\n", "    'Component': components,\n", "    'Weight': [weights[c] for c in components],\n", "    'Mean Score': [master[c].mean() for c in components],\n", "    'Std Dev': [master[c].std() for c in components],\n", "    'Min': [master[c].min() for c in components],\n", "    'Max': [master[c].max() for c in components]\n", "})\n", "\n", "summary['Contribution (Mean)'] = summary['Mean Score'] * summary['Weight']\n", "summary = summary.round(2)\n", "print(summary.to_string(index=False))"]
        }
    ],
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11.0"}
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open('notebooks/03_Integration_Index.ipynb', 'w') as f:
    json.dump(notebook, f, indent=2)

print('✓ Created: 03_Integration_Index.ipynb')