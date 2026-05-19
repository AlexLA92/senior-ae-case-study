#!/bin/bash
set -e

echo "==> Generating synthetic data..."
python scripts/generate_data.py

echo "==> Copying CSVs to dbt seeds directory..."
cp data/raw/*.csv pairing_funnel/seeds/

echo "==> Setting up dbt profiles..."
cp pairing_funnel/profiles.yml ~/.dbt/profiles.yml

echo "==> Installing dbt packages..."
cd pairing_funnel
dbt deps

echo "==> Seeding data + building models..."
dbt build

echo ""
echo "✅ Setup complete! The dbt project is ready."
echo "   cd pairing_funnel && dbt build"
