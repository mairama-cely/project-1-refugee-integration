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
            "source": ["# 00_Data_Fetching — Refugee Integration Analysis\n", "\n", "**Objectif:** Load & validate master table"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["import pandas as pd\n", "import numpy as np\n", "import matplotlib.pyplot as plt\n", "import seaborn as sns\n", "from datetime import datetime\n", "print('✓ Libraries loaded')"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["# Load master table\n", "master = pd.read_parquet('data/processed/refugee_master_consolidated.parquet')\n", "print(f'✓ Loaded: {master.shape}')\n", "print(master.head())"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["# Summary\n", "print(f'Countries: {master[\"iso_a3\"].nunique()}')\n", "print(f'Years: {master[\"Year\"].min()}-{master[\"Year\"].max()}')\n", "print(f'Integration index: {master[\"integration_index\"].min():.2f}-{master[\"integration_index\"].max():.2f}')"]
        }
    ],
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11.0"}
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open('notebooks/00_Data_Fetching.ipynb', 'w') as f:
    json.dump(notebook, f, indent=2)

print('✓ Created: 00_Data_Fetching.ipynb')