"""Deterministic scientific figures for the rolling-origin forecasting evaluation. Underlying
values all exist in CSV (metrics_by_horizon.csv, skill_by_horizon.csv,
rolling_origin_predictions.csv) -- these plots are visualizations only, not new evidence.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

OUT_DIR = REPO_ROOT / "outputs/figures/forecasting"
MODELS = ["fractional", "integer", "persistence", "seasonal_naive_12", "SARIMA"]
COLORS = {
    "fractional": "tab:blue", "integer": "tab:orange", "persistence": "tab:gray",
    "seasonal_naive_12": "tab:green", "SARIMA": "tab:purple",
}


def plot_metric_vs_horizon(metrics_df: pd.DataFrame, metric: str, out_name: str) -> None:
    fig, ax = plt.subplots(figsize=(6, 4))
    for model_label in MODELS:
        sub = metrics_df[metrics_df["model"] == model_label].sort_values("horizon")
        if len(sub) == 0:
            continue
        ax.plot(sub["horizon"], sub[metric], marker="o", label=model_label, color=COLORS[model_label])
    ax.set_xlabel("horizon (months)")
    ax.set_ylabel(metric)
    ax.set_title(f"{metric} vs horizon (rolling-origin, 13 origins)")
    ax.legend(fontsize=8)
    ax.set_xticks(range(1, 13))
    fig.tight_layout()
    path = OUT_DIR / out_name
    fig.savefig(path, dpi=120)
    plt.close(fig)
    print(f"Wrote {path.relative_to(REPO_ROOT)}")


def plot_skill_vs_horizon(skill_df: pd.DataFrame) -> None:
    for metric in ["RMSE", "MAE"]:
        fig, ax = plt.subplots(figsize=(6, 4))
        for baseline in ["persistence", "seasonal_naive_12", "SARIMA"]:
            sub = skill_df[
                (skill_df["model"] == "fractional")
                & (skill_df["baseline"] == baseline)
                & (skill_df["metric"] == metric)
            ].sort_values("horizon")
            if len(sub) == 0:
                continue
            ax.plot(sub["horizon"], sub["skill"], marker="o", label=f"vs {baseline}")
        ax.axhline(0.0, color="black", linewidth=0.8, linestyle="--")
        ax.set_xlabel("horizon (months)")
        ax.set_ylabel(f"Skill_{metric}")
        ax.set_title(f"Fractional model {metric} skill vs baselines")
        ax.legend(fontsize=8)
        ax.set_xticks(range(1, 13))
        fig.tight_layout()
        path = OUT_DIR / f"skill_{metric.lower()}_vs_horizon.png"
        fig.savefig(path, dpi=120)
        plt.close(fig)
        print(f"Wrote {path.relative_to(REPO_ROOT)}")


def plot_origin_horizon_error_map(predictions_df: pd.DataFrame) -> None:
    sub = predictions_df[predictions_df["model"] == "fractional"].copy()
    sub["abs_error"] = (sub["predicted"] - sub["observed"]).abs()
    pivot = sub.pivot(index="origin", columns="horizon", values="abs_error")
    fig, ax = plt.subplots(figsize=(7, 5))
    im = ax.imshow(pivot.to_numpy(), aspect="auto", cmap="viridis")
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels(pivot.columns)
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index)
    ax.set_xlabel("horizon (months)")
    ax.set_ylabel("origin")
    ax.set_title("Fractional model: absolute error by origin x horizon")
    fig.colorbar(im, ax=ax, label="|error|")
    fig.tight_layout()
    path = OUT_DIR / "origin_horizon_error_map_fractional.png"
    fig.savefig(path, dpi=120)
    plt.close(fig)
    print(f"Wrote {path.relative_to(REPO_ROOT)}")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    metrics_df = pd.read_csv(REPO_ROOT / "outputs/forecasting/metrics_by_horizon.csv")
    skill_df = pd.read_csv(REPO_ROOT / "outputs/forecasting/skill_by_horizon.csv")
    predictions_df = pd.read_csv(REPO_ROOT / "outputs/forecasting/rolling_origin_predictions.csv")

    plot_metric_vs_horizon(metrics_df, "RMSE", "rmse_vs_horizon.png")
    plot_metric_vs_horizon(metrics_df, "MAE", "mae_vs_horizon.png")
    plot_metric_vs_horizon(metrics_df, "bias", "bias_vs_horizon.png")
    plot_skill_vs_horizon(skill_df)
    plot_origin_horizon_error_map(predictions_df)


if __name__ == "__main__":
    main()
