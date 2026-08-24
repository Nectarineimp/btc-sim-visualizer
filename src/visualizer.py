"""
btc-sim-visualizer: High-Precision Stochastic Simulation Overlay
Supports dynamic single-model, dual-model, and full 3-model tournament overlays with actuals.
"""

import argparse
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


MODEL_PRESETS = {
    "truetether": {
        "name": "TrueTether",
        "color": (0.95, 0.28, 0.28),   # Coral / Crimson
        "edge_color": "#ff4d4d",
        "desc": "OU Mean-Reversion + Power-Law Drift",
    },
    "regimeecho": {
        "name": "RegimeEcho",
        "color": (0.25, 0.55, 0.95),   # Royal Blue
        "edge_color": "#4da6ff",
        "desc": "Era 4 Moving Block Bootstrap",
    },
    "tailwhip": {
        "name": "TailWhip",
        "color": (0.20, 0.85, 0.45),   # Emerald / Mint
        "edge_color": "#33cc66",
        "desc": "Merton Jump-Diffusion SDE",
    },
}


def identify_model(file_path: str, index: int):
    """Identify model name and palette from filename or fallback to index."""
    fname = os.path.basename(file_path).lower()
    for key, val in MODEL_PRESETS.items():
        if key in fname or key in file_path.lower():
            return val
    keys = list(MODEL_PRESETS.keys())
    return MODEL_PRESETS[keys[index % len(keys)]]


def load_dataset(file_path: str):
    df = pd.read_csv(file_path)
    df["Month_Date"] = pd.to_datetime(df["Month"])
    df = df.sort_values("Month_Date").reset_index(drop=True)
    return df


def plot_forecasts(csv_paths: list[str], output_path: str, actual_csv: str = None):
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)

    # Dark-slate background for contrast and additive alpha blending
    bg_color = "#1a1c20"
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    # Grid styling
    ax.grid(True, which="both", color="#2e323b", linestyle="--", linewidth=0.7, alpha=0.8)
    for spine in ax.spines.values():
        spine.set_color("#474d59")

    all_dfs = [load_dataset(p) for p in csv_paths]
    x_dates = all_dfs[0]["Month_Date"]
    x_labels = all_dfs[0]["Month"]
    x_indices = np.arange(len(x_dates))

    num_models = len(csv_paths)

    for i, (df, path) in enumerate(zip(all_dfs, csv_paths)):
        preset = identify_model(path, i)
        label_name = preset["name"]
        r, g, b = preset["color"]

        # If rendering single model, use richer alpha; for multi-model, use lighter alpha
        tail_alpha = 0.18 if num_models == 1 else 0.12
        core_alpha = 0.35 if num_models == 1 else 0.22

        # Outer 2-sigma tail band: p05 to p95
        ax.fill_between(
            x_indices,
            df["Low_p05"],
            df["High_p95"],
            color=(r, g, b, tail_alpha),
            label=f"{label_name} 2σ Tail (5th–95th)",
            zorder=2 + i,
        )

        # Core 1-sigma density band: p16 to p84
        ax.fill_between(
            x_indices,
            df["Low_p16"],
            df["High_p84"],
            color=(r, g, b, core_alpha),
            label=f"{label_name} 1σ Core (16th–84th)",
            zorder=3 + i,
        )

        # Median High and Low lines
        ax.plot(
            x_indices,
            df["High_p50"],
            color=preset["edge_color"],
            linewidth=2.0,
            linestyle="-",
            label=f"{label_name} Median High (p50)",
            zorder=5 + i,
        )
        ax.plot(
            x_indices,
            df["Low_p50"],
            color=preset["edge_color"],
            linewidth=2.0,
            linestyle="--",
            label=f"{label_name} Median Low (p50)",
            zorder=5 + i,
        )

    # Plot Realized Market Actuals (High-Contrast White Candlesticks/Bars)
    if actual_csv and os.path.exists(actual_csv):
        df_act = pd.read_csv(actual_csv)
        merged = pd.merge(all_dfs[0][["Month"]], df_act, on="Month", how="left")
        act_idx = np.where(~merged["Actual_High"].isna())[0]

        if len(act_idx) > 0:
            for idx in act_idx:
                low_val = merged["Actual_Low"].iloc[idx]
                high_val = merged["Actual_High"].iloc[idx]
                
                # Vertical range bar
                ax.vlines(
                    x_indices[idx],
                    low_val,
                    high_val,
                    color="#ffffff",
                    linewidth=4.0,
                    zorder=12,
                )
                # Cap markers at high and low
                ax.plot(
                    x_indices[idx],
                    high_val,
                    marker="_",
                    markersize=12,
                    markeredgewidth=3.0,
                    color="#ffffff",
                    zorder=13,
                )
                ax.plot(
                    x_indices[idx],
                    low_val,
                    marker="_",
                    markersize=12,
                    markeredgewidth=3.0,
                    color="#ffffff",
                    zorder=13,
                )

            # Single legend entry for actuals
            ax.plot([], [], color="#ffffff", linewidth=3.5, label="Realized Market Range (Actuals)")

    # Dynamic Title Generation
    if num_models == 1:
        preset = identify_model(csv_paths[0], 0)
        title_text = f"{preset['name']} Forward 12-Month Stochastic Forecast\n{preset['desc']}"
    else:
        title_text = "Bitcoin 12-Month Monte Carlo Tournament Forecasts\nAdditive Density Bands (TrueTether, RegimeEcho, TailWhip)"

    ax.set_title(title_text, fontsize=14, fontweight="bold", color="#ffffff", pad=16)

    # Formatting Axes
    ax.set_xticks(x_indices)
    ax.set_xticklabels(x_labels, rotation=45, ha="right", fontsize=10, color="#dcdcdc")
    ax.yaxis.set_major_formatter("${x:,.0f}")
    ax.tick_params(axis="y", colors="#dcdcdc", labelsize=10)
    ax.tick_params(axis="x", colors="#dcdcdc")
    ax.set_ylabel("Reference Price ($ USD)", fontsize=11, fontweight="bold", color="#ffffff")

    # Legend formatting
    handles, labels = ax.get_legend_handles_labels()
    ncol = 1 if num_models == 1 else min(num_models, 3)
    ax.legend(
        handles,
        labels,
        loc="upper left",
        facecolor="#121417",
        edgecolor="#3d424d",
        fontsize=9,
        labelcolor="#ffffff",
        framealpha=0.92,
        ncol=ncol,
    )

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"Render complete: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Multi-Model Bitcoin Forecast Visualizer")
    parser.add_argument("files", nargs="+", help="Paths to 1, 2, or 3 monthly_forecast.csv files")
    parser.add_argument("--output", type=str, default="output/forecast_overlay.png", help="Path for rendered PNG")
    parser.add_argument("--actuals", type=str, default=None, help="Optional CSV containing realized actuals")
    args = parser.parse_args()

    plot_forecasts(args.files, args.output, args.actuals)


if __name__ == "__main__":
    main()