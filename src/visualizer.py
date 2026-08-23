"""
Multi-Model Forecast Visualizer with Additive RGB Blending
Supports plotting 1, 2, or 3 forecast datasets simultaneously.
"""

import argparse
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


MODEL_THEMES = [
    {
        "name": "TrueTether",
        "color": (0.95, 0.25, 0.25),   # Red / Coral
        "edge_color": "#ff4d4d",
    },
    {
        "name": "RegimeEcho",
        "color": (0.25, 0.55, 0.95),   # Royal Blue
        "edge_color": "#4da6ff",
    },
    {
        "name": "TailWhip",
        "color": (0.20, 0.85, 0.45),   # Mint / Emerald
        "edge_color": "#33cc66",
    },
]


def load_dataset(file_path: str):
    df = pd.read_csv(file_path)
    df["Month_Date"] = pd.to_datetime(df["Month"])
    df = df.sort_values("Month_Date").reset_index(drop=True)
    return df


def plot_forecasts(csv_paths: list[str], output_path: str, actual_csv: str = None):
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)

    # Set medium-dark grey background for additive blending
    bg_color = "#202226"
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    # Styling grid & spines
    ax.grid(True, which="both", color="#383c44", linestyle="--", linewidth=0.7, alpha=0.7)
    for spine in ax.spines.values():
        spine.set_color("#555b66")

    all_dfs = [load_dataset(p) for p in csv_paths]
    x_dates = all_dfs[0]["Month_Date"]
    x_labels = all_dfs[0]["Month"]
    x_indices = np.arange(len(x_dates))

    # Iterate through models and plot transparent bands
    for i, df in enumerate(all_dfs):
        theme = MODEL_THEMES[i % len(MODEL_THEMES)]
        base_name = os.path.splitext(os.path.basename(csv_paths[i]))[0]
        label_name = theme["name"] if i < 3 else base_name
        r, g, b = theme["color"]

        # Outer tail bounds: p05 to p95
        ax.fill_between(
            x_indices,
            df["Low_p05"],
            df["High_p95"],
            color=(r, g, b, 0.15),
            label=f"{label_name} (5th-95th Tail)",
            zorder=2 + i,
        )

        # Core density bounds: p16 to p84
        ax.fill_between(
            x_indices,
            df["Low_p16"],
            df["High_p84"],
            color=(r, g, b, 0.28),
            label=f"{label_name} (16th-84th Core)",
            zorder=3 + i,
        )

        # Median High and Low Bounds
        ax.plot(
            x_indices,
            df["High_p50"],
            color=theme["edge_color"],
            linewidth=1.8,
            linestyle="-",
            label=f"{label_name} Median High",
            zorder=5 + i,
        )
        ax.plot(
            x_indices,
            df["Low_p50"],
            color=theme["edge_color"],
            linewidth=1.8,
            linestyle="--",
            label=f"{label_name} Median Low",
            zorder=5 + i,
        )

    # Optional: Plot actual realized price points if provided
    if actual_csv and os.path.exists(actual_csv):
        df_act = pd.read_csv(actual_csv)
        df_act["Month_Date"] = pd.to_datetime(df_act["Month"])
        merged = pd.merge(all_dfs[0][["Month"]], df_act, on="Month", how="left")
        act_idx = np.where(~merged["Actual_High"].isna())[0]
        if len(act_idx) > 0:
            ax.vlines(
                x_indices[act_idx],
                merged["Actual_Low"].iloc[act_idx],
                merged["Actual_High"].iloc[act_idx],
                color="#ffffff",
                linewidth=3.5,
                label="Realized Market Range",
                zorder=10,
            )

    # Formatting Axes
    ax.set_xticks(x_indices)
    ax.set_xticklabels(x_labels, rotation=45, ha="right", fontsize=10, color="#dcdcdc")
    ax.yaxis.set_major_formatter("${x:,.0f}")
    ax.tick_params(axis="y", colors="#dcdcdc", labelsize=10)
    ax.tick_params(axis="x", colors="#dcdcdc")

    ax.set_title(
        "Bitcoin 12-Month Monte Carlo Tournament Forecasts\nAdditive Density Bands (TrueTether, RegimeEcho, TailWhip)",
        fontsize=14,
        fontweight="bold",
        color="#ffffff",
        pad=18,
    )
    ax.set_ylabel("Reference Price ($ USD)", fontsize=11, fontweight="bold", color="#ffffff")

    # Clean multi-column legend
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(
        handles,
        labels,
        loc="upper left",
        facecolor="#181a1d",
        edgecolor="#444952",
        fontsize=8.5,
        labelcolor="#ffffff",
        framealpha=0.9,
        ncol=len(csv_paths),
    )

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"Visualization successfully saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Multi-Model Bitcoin Forecast Visualizer")
    parser.add_argument("files", nargs="+", help="Paths to 1, 2, or 3 monthly_forecast.csv files")
    parser.add_argument("--output", type=str, default="output/forecast_overlay.png", help="Path for rendered image")
    parser.add_argument("--actuals", type=str, default=None, help="Optional CSV containing realized monthly actuals")
    args = parser.parse_args()

    plot_forecasts(args.files, args.output, args.actuals)


if __name__ == "__main__":
    main()