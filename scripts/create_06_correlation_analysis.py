import json

notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["# 06_Correlation_Analysis — Relationships & Dependencies"]
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
            "source": ["import pandas as pd\n", "import numpy as np\n", "import matplotlib.pyplot as plt\n", "import seaborn as sns\n", "from scipy.stats import pearsonr, spearmanr\n", "sns.set_style('whitegrid')\n", "print('✓ Libraries loaded')"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["master = pd.read_parquet('data/processed/refugee_master_consolidated.parquet')\n", "print(f'Data shape: {master.shape}')"]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 1. Component Correlation Matrix"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["components = ['employment_rate', 'housing_access', 'education_enrollment', 'income_stability', 'legal_rights_score', 'social_cohesion', 'integration_index']\n", "\n", "corr_matrix = master[components].corr(method='pearson')\n", "print('Pearson Correlation Matrix:')\n", "print(corr_matrix.round(3))"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["fig, ax = plt.subplots(figsize=(10, 8))\n", "sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0, \n", "            square=True, linewidths=1, cbar_kws={\"shrink\": 0.8}, ax=ax, vmin=-1, vmax=1)\n", "ax.set_title('Component Correlation Matrix', fontsize=12, fontweight='bold')\n", "plt.tight_layout()\n", "plt.savefig('output/06_correlation_matrix.png', dpi=300, bbox_inches='tight')\n", "plt.show()\n", "print('✓ Saved: 06_correlation_matrix.png')"]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 2. Correlation with Integration Index"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["component_list = ['employment_rate', 'housing_access', 'education_enrollment', 'income_stability', 'legal_rights_score', 'social_cohesion']\n", "\n", "correlations = []\n", "for comp in component_list:\n", "    pearson_corr, p_value = pearsonr(master[comp], master['integration_index'])\n", "    correlations.append({\n", "        'Component': comp,\n", "        'Pearson r': pearson_corr,\n", "        'P-value': p_value,\n", "        'Significant': 'Yes' if p_value < 0.05 else 'No'\n", "    })\n", "\n", "corr_df = pd.DataFrame(correlations).sort_values('Pearson r', ascending=False)\n", "print(corr_df.to_string(index=False))"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["fig, ax = plt.subplots(figsize=(10, 6))\n", "corr_df_sorted = corr_df.sort_values('Pearson r')\n", "colors = ['#2ecc71' if x >= 0 else '#e74c3c' for x in corr_df_sorted['Pearson r']]\n", "ax.barh(corr_df_sorted['Component'], corr_df_sorted['Pearson r'], color=colors, alpha=0.7)\n", "ax.set_xlabel('Correlation with Integration Index')\n", "ax.set_title('Component Correlation Strength', fontsize=12, fontweight='bold')\n", "ax.axvline(x=0, color='black', linestyle='-', linewidth=0.8)\n", "plt.tight_layout()\n", "plt.savefig('output/06_component_correlations.png', dpi=300, bbox_inches='tight')\n", "plt.show()\n", "print('✓ Saved: 06_component_correlations.png')"]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 3. Pairwise Component Relationships"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["# Employment vs Housing\n", "fig, axes = plt.subplots(2, 3, figsize=(15, 10))\n", "axes = axes.ravel()\n", "\n", "pairs = [\n", "    ('employment_rate', 'housing_access'),\n", "    ('employment_rate', 'education_enrollment'),\n", "    ('income_stability', 'legal_rights_score'),\n", "    ('housing_access', 'social_cohesion'),\n", "    ('education_enrollment', 'income_stability'),\n", "    ('legal_rights_score', 'social_cohesion')\n", "]\n", "\n", "for i, (x, y) in enumerate(pairs):\n", "    axes[i].scatter(master[x], master[y], alpha=0.5, s=30)\n", "    r, _ = pearsonr(master[x], master[y])\n", "    axes[i].set_title(f'{x.replace(\"_\", \" \").title()} vs\\n{y.replace(\"_\", \" \").title()}\\n(r={r:.2f})', fontsize=9)\n", "    axes[i].set_xlabel(x.replace('_', ' '))\n", "    axes[i].set_ylabel(y.replace('_', ' '))\n", "    axes[i].grid(True, alpha=0.3)\n", "\n", "plt.tight_layout()\n", "plt.savefig('output/06_pairwise_relationships.png', dpi=300, bbox_inches='tight')\n", "plt.show()\n", "print('✓ Saved: 06_pairwise_relationships.png')"]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 4. Refugee Volume Correlations"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["# Does higher refugee volume correlate with lower integration?\n", "r_refugees, p_refugees = pearsonr(master['Refugees under UNHCR\\'s mandate'], master['integration_index'])\n", "r_asylum, p_asylum = pearsonr(master['Asylum-seekers'], master['integration_index'])\n", "\n", "print(f'Refugees vs Integration Index: r={r_refugees:.3f}, p={p_refugees:.4f}')\n", "print(f'Asylum-seekers vs Integration Index: r={r_asylum:.3f}, p={p_asylum:.4f}')"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))\n", "\n", "ax1.scatter(master['Refugees under UNHCR\\'s mandate'] / 1000, master['integration_index'], alpha=0.5, s=30)\n", "ax1.set_xlabel('Refugees (thousands)')\n", "ax1.set_ylabel('Integration Index')\n", "ax1.set_title(f'Refugee Volume vs Integration (r={r_refugees:.3f})', fontsize=11, fontweight='bold')\n", "ax1.grid(True, alpha=0.3)\n", "\n", "ax2.scatter(master['Asylum-seekers'] / 1000, master['integration_index'], alpha=0.5, s=30, color='orange')\n", "ax2.set_xlabel('Asylum-seekers (thousands)')\n", "ax2.set_ylabel('Integration Index')\n", "ax2.set_title(f'Asylum-seekers vs Integration (r={r_asylum:.3f})', fontsize=11, fontweight='bold')\n", "ax2.grid(True, alpha=0.3)\n", "\n", "plt.tight_layout()\n", "plt.savefig('output/06_volume_correlations.png', dpi=300, bbox_inches='tight')\n", "plt.show()\n", "print('✓ Saved: 06_volume_correlations.png')"]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 5. Summary Statistics Table"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["summary = pd.DataFrame({\n", "    'Relationship': ['Refugees vs Index', 'Asylum-seekers vs Index'],\n", "    'Pearson r': [r_refugees, r_asylum],\n", "    'P-value': [p_refugees, p_asylum],\n", "    'Significant': ['Yes' if p_refugees < 0.05 else 'No', 'Yes' if p_asylum < 0.05 else 'No'],\n", "    'Interpretation': [\n", "        'Weak positive' if r_refugees > 0 else 'Weak negative',\n", "        'Weak positive' if r_asylum > 0 else 'Weak negative'\n", "    ]\n", "})\n", "print(summary.round(4).to_string(index=False))"]
        }
    ],
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11.0"}
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open('notebooks/06_Correlation_Analysis.ipynb', 'w') as f:
    json.dump(notebook, f, indent=2)

print('✓ Created: 06_Correlation_Analysis.ipynb')