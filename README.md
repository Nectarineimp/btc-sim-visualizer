# btc-sim-visualizer
Visualizer for price prediction models.

# Bitcoin Forecast Visualizer (`btc-sim-visualizer`)

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **High-Precision Multi-Model Stochastic Overlay & Tournament Tracker**

`btc-sim-visualizer` is a dedicated visualization and empirical performance tracker for Bitcoin price simulation engines. It ingests forward forecast distributions from one, two, or three independent models—**TrueTether**, **RegimeEcho**, and **TailWhip**—rendering additive RGB density corridors against a dark-slate canvas and tracking model accuracy against realized market actuals in real time.

---

## Visual Architecture & Additive Color Dynamics

The visualizer uses additive alpha-channel blending against a neutral dark-slate background (`#202226`):

- 🔴 **TrueTether (Coral/Red):** Mean-Reverting Residual Process (Ornstein-Uhlenbeck + Power-Law Drift)
- 🔵 **RegimeEcho (Royal Blue):** Non-Parametric Moving Block Bootstrap (Era 4 Resampling)
- 🟢 **TailWhip (Emerald/Mint):** Regime Jump-Diffusion SDE (Merton Process)

### Overlap & Consensus Density
When multiple models project overlapping confidence bands, their color channels blend:
- **Red + Blue $\to$ Magenta:** TrueTether & RegimeEcho consensus
- **Blue + Green $\to$ Cyan:** RegimeEcho & TailWhip consensus
- **Red + Green $\to$ Yellow:** TrueTether & TailWhip consensus
- **Red + Green + Blue $\to$ Bright White / Ivory:** Universal three-model agreement zone

### Uncertainty Layers
Each model is plotted across two distinct confidence layers:
1. **$2\sigma$ Tail Corridor ($p05 \leftrightarrow p95$):** Low-opacity outer bounding fill.
2. **$1\sigma$ Core Corridor ($p16 \leftrightarrow p84$):** Medium-opacity core density fill.
3. **Median Trajectory ($p50$ High & Low):** High-contrast structural bounding lines.

---

## Realized Market Tracker (Live Overlay)

The visualizer supports an optional `--actuals` CSV flag to plot real-world monthly High/Low trading ranges directly over the forecast bands, allowing visual performance grading and tournament tracking throughout the 12-month evaluation period.

### `actuals.csv` Format:
```csv
Month,Actual_Low,Actual_High
2026-05,67100,78200
2026-06,60150,71900
2026-07,62400,69800
