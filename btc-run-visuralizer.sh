#!/usr/bin/env bash

cd ~/projects/btc-data-hub
echo "Building actuals..."
poetry run python src/build_actuals.py

cd ~/projects/btc-sim-visualizer/

# Get current date in YYYYMMDD format
DATE=$(date +%Y%m%d)

echo "Starting visualizations..."

# 1. TrueTether Solo Render with Actuals
poetry run python src/visualizer.py \
  ~/projects/btc-sim-truetether/output/monthly_forecast.csv \
  --actuals data/actuals.csv \
  --output "output/truetether_${DATE}.png"

# 2. RegimeEcho Solo Render with Actuals
poetry run python src/visualizer.py \
  ~/projects/btc-sim-regimeecho/output/monthly_forecast.csv \
  --actuals data/actuals.csv \
  --output "output/regimeecho_${DATE}.png"

# 3. TailWhip Solo Render with Actuals
poetry run python src/visualizer.py \
  ~/projects/btc-sim-tailwhip/output/monthly_forecast.csv \
  --actuals data/actuals.csv \
  --output "output/tailwhip_${DATE}.png"

# 4. TrueTetherChamberlain Solo Render with Actuals
poetry run python src/visualizer.py \
  ~/projects/btc-sim-truetetherchamperlain/output/monthly_forecast.csv \
  --actuals data/actuals.csv \
  --output "output/truetether_${DATE}.png"

echo "Visualizations completed."
