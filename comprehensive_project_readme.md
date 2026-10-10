# Bitcoin Forecast Visualizer (`btc-sim-visualizer`)

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Matplotlib](https://img.shields.io/badge/Render-Matplotlib%20DPI300-brightgreen.svg)](https://matplotlib.org/)

> **High-Precision Multi-Model Stochastic Overlay & 12-Month Tournament Tracker**

`btc-sim-visualizer` is an analytical visualization engine and empirical validation framework for forward Bitcoin price simulations. Designed to ingest prospective Monte Carlo trajectories, non-parametric bootstraps, and jump-diffusion stochastic differential equation (SDE) distributions, it renders additive alpha-blended probability corridors against real-world market outcomes.

---

## Table of Contents
- [The 12-Month Stochastic Tournament](#the-12-month-stochastic-tournament)
  - [Rationale and Purpose](#rationale-and-purpose)
  - [Evaluation Criteria & Scoring](#evaluation-criteria--scoring)
- [Competing Quantitative Paradigms](#competing-quantitative-paradigms)
- [Visual Architecture & Color Dynamics](#visual-architecture--color-dynamics)
- [Data Specifications & Schemas](#data-specifications--schemas)
  - [Forecast Distribution Schema](#forecast-distribution-schema-monthly_forecastcsv)
  - [Realized Actuals Schema](#realized-actuals-schema-actualscsv)
- [Installation & Quickstart](#installation--quickstart)
- [CLI Reference & Usage Modes](#cli-reference--usage-modes)
- [Extensibility](#extensibility)

---

## The 12-Month Stochastic Tournament

### Rationale and Purpose

Quantitative financial models frequently suffer from in-sample over-parameterization: models tuned on historical Bitcoin price action often capture regime-specific noise rather than enduring price formation mechanics. The **12-Month Stochastic Tournament** is a rigorous, out-of-sample forward evaluation arena established to benchmark fundamentally distinct quantitative paradigms against future reality without hindsight bias.

1. **Capturing Medium-Horizon Structural Drift:**  
   A 12-month horizon tests whether models can separate macro structural trend (such as long-term power-law adoption drifts) from cyclic volatility and institutional liquidity rebalancing. Shorter horizons (e.g., 30 days) are dominated by microstructure noise, whereas multi-year horizons suffer excessive compounding variance.
2. **Post-Halving & Liquidity Cycle Traversal:**  
   Bitcoin's 4-year cycle typically experiences distinct quarterly phase shifts—from accumulation and parabolic expansion to severe drawdowns and distribution. A full 1-year test forces each engine to endure multiple macro regimes.
3. **Distributional Calibration vs. Point Prediction:**  
   Financial markets are non-stationary and non-Gaussian. Rather than judging models on fragile single-line price targets, the tournament scores engines on their **probabilistic coverage**—evaluating whether market actuals inhabit the $1\sigma$ (68%) and $2\sigma$ (90%) corridors with the expected statistical frequency.
4. **Tail-Risk & Black-Swan Stress Testing:**  
   Bitcoin displays significant excess kurtosis (fat tails) and negative skewness during liquidation cascades. The 12-month duration provides sufficient surface area to assess whether jump-diffusion, mean-reversion, or bootstrap models adequately anticipate extreme market shocks.

### Evaluation Criteria & Scoring

Each participating model is tracked monthly against the realized market high/low price range:

| Metric | Target | Evaluation Mechanism |
| :--- | :--- | :--- |
| **$1\sigma$ Core Coverage** | $\approx 68\%$ | Percentage of months where the realized range intersects $[p16_{\text{Low}}, p84_{\text{High}}]$. |
| **$2\sigma$ Tail Bounding** | $\approx 90\%$ | Percentage of realized monthly ranges completely contained within $[p05_{\text{Low}}, p95_{\text{High}}]$. |
| **Median Drift Error (MAE)** | Minimize | Absolute divergence of realized mid-prices from the modeled $p50$ center line. |
| **Band Efficiency** | Maximize | Ratio of coverage hit-rate to total corridor bandwidth (penalizes trivial, excessively wide bands). |

---

## Competing Quantitative Paradigms

The visualizer includes built-in styling and detection presets for the tournament's primary competing simulation archetypes:

| Model Flag | Engine Name | Mathematical Framework | Hypothesis |
| :--- | :--- | :--- | :--- |
| `truetether` | **TrueTether** | Ornstein-Uhlenbeck (OU) Mean-Reversion + Power-Law Drift | Price is tethered to a macro power-law trajectory; short-term deviations revert to equilibrium over time. |
| `regimeecho` | **RegimeEcho** | Era 4 Moving Block Bootstrap | Non-parametric resampling of modern institutional-era returns preserving empirical autocorrelation and kurtosis. |
| `tailwhip` | **TailWhip** | Merton Jump-Diffusion SDE | Combines continuous Brownian motion with Poisson-distributed discontinuous jump processes to capture flash crashes. |
| `chamberlain`| **Chamberlain** | Coupled Heston Stochastic Volatility + Power Law | Treats volatility as a mean-reverting stochastic process correlated with price returns. |
| `gatekeeper` | **GateKeeper** | Macro-Liquidity Gated SDE | Couples global macro liquidity metrics with explicit institutional rebalancing intervals. |
| `echophase`  | **EchoPhase** | Harmonic-Weighted Empirical Block Bootstrap | Cyclically weighted bootstrap emphasizing phase-matched epochs from prior Bitcoin cycles. |

---

## Visual Architecture & Color Dynamics

The visualizer employs additive alpha blending across a high-contrast dark-slate canvas (`#1a1c20`), allowing viewers to diagnose model consensus instantly:

```
              ┌──────────────────────────────────────────────┐
              │           Visual Output Canvas               │
              │                                              │
              │   🔴 TrueTether (Red)                        │
              │         ↘                                    │
              │           🟪 Consensus Zone (Magenta)        │
              │         ↗                                    │
              │   🔵 RegimeEcho (Blue)                       │
              │         ↘                                    │
              │           ⬜ 3-Model Consensus (White/Ivory) │
              │         ↗                                    │
              │   🟢 TailWhip (Green)                        │
              │                                              │
              │   ══ Realized Market Actuals (White Bars)    │
              └──────────────────────────────────────────────┘
```

- **Confidence Bands:**
  - **Outer $2\sigma$ Tail Corridor ($p05 \leftrightarrow p95$):** Low-opacity bounded envelope representing extreme tail coverage.
  - **Inner $1\sigma$ Core Corridor ($p16 \leftrightarrow p84$):** High-density central corridor representing the model's highest probability domain.
- **Trajectory Lines:**
  - Solid ($p50$ High) and dashed ($p50$ Low) lines represent median boundary expectations.
- **Realized Actuals:**
  - High-contrast white vertical range bars with capped terminal ticks depicting the realized intra-month low and high prices.

---

## Data Specifications & Schemas

### Forecast Distribution Schema (`monthly_forecast.csv`)

Each simulation run must emit a CSV with forward 12-month projections structured as follows:

```csv
Month,Low_p05,Low_p16,Low_p50,High_p50,High_p84,High_p95
2026-05,58200.50,62400.00,68100.00,74200.00,81500.00,88300.00
2026-06,56100.00,60800.00,67300.00,75900.00,84100.00,92400.00
2026-07,59400.00,64200.00,71500.00,80100.00,89700.00,98500.00
```

- **`Month`:** `YYYY-MM` string representing the forward monthly period.
- **`Low_p05` / `High_p95`:** 5th percentile monthly low and 95th percentile monthly high (90% envelope).
- **`Low_p16` / `High_p84`:** 16th percentile monthly low and 84th percentile monthly high (68% envelope).
- **`Low_p50` / `High_p50`:** Median projected low and median projected high.

### Realized Actuals Schema (`actuals.csv`)

Realized market data can be updated monthly as the tournament progresses:

```csv
Month,Actual_Low,Actual_High
2026-05,62100.00,76850.00
2026-06,59800.00,72400.00
2026-07,,
```
*(Leave future or uncompleted months empty or unlisted).*

---

## Installation & Quickstart

### Prerequisites
- Python 3.10 or higher
- `pandas`, `numpy`, `matplotlib`

```bash
git clone https://github.com/your-username/btc-sim-visualizer.git
cd btc-sim-visualizer
pip install -r requirements.txt
```

*(Or install dependencies directly: `pip install matplotlib numpy pandas`)*

---

## CLI Reference & Usage Modes

### 1. Single-Model Deep Dive
Plot a single model's 12-month forecast distribution with rich alpha envelopes:
```bash
python visualizer.py forecasts/truetether_forecast.csv --output output/truetether.png
```

### 2. Dual-Model Comparative Overlay
Compare two opposing mathematical approaches (e.g., parametric mean-reversion vs. non-parametric bootstrap):
```bash
python visualizer.py \
  forecasts/truetether_forecast.csv \
  forecasts/regimeecho_forecast.csv \
  --output output/head_to_head.png
```

### 3. Full Tournament Overlay with Realized Actuals
Overlay three competing engines alongside real-world market ranges:
```bash
python visualizer.py \
  forecasts/truetether_forecast.csv \
  forecasts/regimeecho_forecast.csv \
  forecasts/tailwhip_forecast.csv \
  --actuals data/actuals.csv \
  --output output/tournament_leaderboard.png
```

---

## Extensibility

To add a new forecasting engine to the tournament visualizer, register a new entry in `MODEL_PRESETS` inside `visualizer.py`:

```python
MODEL_PRESETS["quantumdrift"] = {
    "name": "QuantumDrift",
    "color": (0.80, 0.30, 0.90),      # RGB tuple for density fills
    "edge_color": "#cc4dff",           # Hex color for median lines
    "desc": "Fractional Brownian Motion + Order Book Imbalance SDE",
}
```
The visualizer automatically maps CSV filenames containing the key (`quantumdrift`) to the corresponding aesthetic preset and legend descriptor.