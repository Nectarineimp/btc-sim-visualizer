#!/usr/bin/env bash
set -e

# Default to running all models if none specified
SELECTED_MODELS="all"

# Parse CLI arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --model)
      SELECTED_MODELS="$2"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1"
      exit 1
      ;;
  esac
done

# Convert selected models list to lowercase for robust matching
SELECTED_MODELS=$(echo ",${SELECTED_MODELS}," | tr '[:upper:]' '[:lower:]')

should_run() {
  local model_name="$1"
  if [[ "$SELECTED_MODELS" == *",all,"* ]] || [[ "$SELECTED_MODELS" == *",${model_name},"* ]]; then
    return 0
  else
    return 1
  fi
}

cd ~/projects/btc-data-hub
echo "Building actuals..."
poetry run python src/build_actuals.py

cd ~/projects/btc-sim-visualizer/

# Get current date in YYYYMMDD format
DATE=$(date +%Y%m%d)

echo "Starting visualizations..."

# 1. TrueTether Solo Render with Actuals
if should_run "truetether"; then
  echo "Rendering TrueTether..."
  poetry run python src/visualizer.py \
    ~/projects/btc-sim-truetether/output/monthly_forecast.csv \
    --actuals data/actuals.csv \
    --output "output/truetether_${DATE}.png"
fi

# 2. RegimeEcho Solo Render with Actuals
if should_run "regimeecho"; then
  echo "Rendering RegimeEcho..."
  poetry run python src/visualizer.py \
    ~/projects/btc-sim-regimeecho/output/monthly_forecast.csv \
    --actuals data/actuals.csv \
    --output "output/regimeecho_${DATE}.png"
fi

# 3. TailWhip Solo Render with Actuals
if should_run "tailwhip"; then
  echo "Rendering TailWhip..."
  poetry run python src/visualizer.py \
    ~/projects/btc-sim-tailwhip/output/monthly_forecast.csv \
    --actuals data/actuals.csv \
    --output "output/tailwhip_${DATE}.png"
fi

# 4. Chamberlain Solo Render with Actuals
if should_run "chamberlain"; then
  echo "Rendering Chamberlain..."
  poetry run python src/visualizer.py \
    ~/projects/btc-sim-chamberlain/output/monthly_forecast.csv \
    --actuals data/actuals.csv \
    --output "output/chamberlain_${DATE}.png"
fi

# 5. Gatekeeper Solo Render with Actuals
if should_run "gatekeeper"; then
  echo "Rendering Gatekeeper..."
  poetry run python src/visualizer.py \
    ~/projects/btc-sim-gatekeeper/output/monthly_forecast.csv \
    --actuals data/actuals.csv \
    --output "output/gatekeeper_${DATE}.png"
fi

# 6. EchoPhase Solo Render with Actuals
if should_run "echophase"; then
  echo "Rendering EchoPhase..."
  poetry run python src/visualizer.py \
    ~/projects/btc-sim-echophase/output/monthly_forecast.csv \
    --actuals data/actuals.csv \
    --output "output/echophase_${DATE}.png"
fi

echo "Visualizations completed."