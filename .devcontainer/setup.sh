#!/bin/bash
set -e

echo "==> Generating synthetic data..."
python scripts/generate_data.py

echo "==> Copying CSVs to dbt seeds directory..."
cp data/raw/*.csv dbt/seeds/

echo "==> Setting up dbt profiles..."
mkdir -p ~/.dbt
cp dbt/profiles.yml ~/.dbt/profiles.yml

echo "==> Moving to dbt project..."
cd dbt

echo "==> Cleaning stale build artifacts..."
rm -f dbt_case_study.duckdb
rm -rf target/

echo "==> Installing dbt packages..."
dbt deps

echo "==> Seeding data + building models..."
dbt build

echo ""
echo "✅ Setup complete! The dbt project is ready."
echo "   cd dbt && dbt build"
