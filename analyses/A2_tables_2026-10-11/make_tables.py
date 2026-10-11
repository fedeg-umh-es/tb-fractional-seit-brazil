"""Step 2 (Plan A continuation): full metric tables from the frozen S1 rolling-origin predictions.

Arithmetic only: no model is fitted or simulated. Inputs are read-only.

Outputs (written next to this script):
  metrics_full_by_horizon.csv       RMSE, MAE, bias, MASE per method and horizon
  table_{MAE,bias,MASE}.csv/.tex    manuscript-ready wide tables (methods x h = 1..12)
  mase_scale_by_origin.csv          in-sample seasonal-naive MAE (m = 12) per origin
  h12_persistence_vs_snaive_check.json
  rmse_reconciliation.json          comparison against phase2/metrics_by_horizon.csv
"""

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
S1 = REPO / "evidence_S1" / "TB_SEIT_EVIDENCE_FREEZE_2026-10-10"
OUT = Path(__file__).resolve().parent
M = 12  # seasonal period for the MASE scale
RMSE_TOL = 1e-9

METHODS = ["fractional", "integer", "persistence", "seasonal_naive_12", "SARIMA"]
LABELS = {
    "fractional": "Fractional SEIT",
    "integer": "Integer SEIT",
    "persistence": "Persistence",
    "seasonal_naive_12": "Seasonal naive (12)",
    "SARIMA": "SARIMA",
}


def load_series() -> pd.Series:
    df = pd.read_excel(REPO / "data" / "raw" / "tb_mes.xlsx")
    s = pd.Series(df["casos"].to_numpy(dtype=float), index=pd.to_datetime(df["data"]))
    assert len(s) == 264 and s.index.is_monotonic_increasing
    return s


def mase_scale(y: pd.Series, origin: pd.Timestamp) -> float:
    """In-sample MAE of the seasonal naive (m = 12) on the training window 2001-01 .. origin."""
    train = y.loc[:origin].to_numpy()
    return float(np.mean(np.abs(train[M:] - train[:-M])))


def to_latex(wide: pd.DataFrame, caption: str, label: str, fmt: str) -> str:
    cols = "l" + "r" * wide.shape[1]
    lines = [r"\begin{table}[ht]", r"\centering", r"\small",
             rf"\caption{{{caption}}}", rf"\label{{{label}}}",
             rf"\begin{{tabular}}{{{cols}}}", r"\hline",
             "Method & " + " & ".join(f"$h={h}$" for h in wide.columns) + r" \\", r"\hline"]
    for m, row in wide.iterrows():
        lines.append(LABELS[m] + " & " + " & ".join(format(v, fmt) for v in row) + r" \\")
    lines += [r"\hline", r"\end{tabular}", r"\end{table}", ""]
    return "\n".join(lines)


def main() -> int:
    y = load_series()
    pred = pd.read_csv(S1 / "phase2" / "rolling_origin_predictions.csv",
                       parse_dates=["origin", "target_date"])
    assert len(pred) == 780 and set(pred["model"]) == set(METHODS)
    assert pred["origin"].nunique() == 13 and sorted(pred["horizon"].unique()) == list(range(1, 13))

    # observed values in the predictions file must equal the canonical series
    obs_check = np.abs(pred["observed"].to_numpy() - y.reindex(pred["target_date"]).to_numpy()).max()
    assert obs_check == 0.0, f"observed mismatch vs data/raw/tb_mes.xlsx: {obs_check}"

    scale = {o: mase_scale(y, o) for o in sorted(pred["origin"].unique())}
    pred["error"] = pred["predicted"] - pred["observed"]
    pred["abs_error"] = pred["error"].abs()
    pred["scaled_abs_error"] = pred["abs_error"] / pred["origin"].map(scale)

    g = pred.groupby(["model", "horizon"])
    full = pd.DataFrame({
        "n_forecasts": g.size(),
        "RMSE": g["error"].apply(lambda e: float(np.sqrt(np.mean(e**2)))),
        "MAE": g["abs_error"].mean(),
        "bias": g["error"].mean(),
        "MASE": g["scaled_abs_error"].mean(),
    }).reset_index()
    full["model"] = pd.Categorical(full["model"], METHODS, ordered=True)
    full = full.sort_values(["model", "horizon"]).reset_index(drop=True)
    full["model"] = full["model"].astype(str)
    full.to_csv(OUT / "metrics_full_by_horizon.csv", index=False, float_format="%.12g")

    pd.DataFrame({"origin": [o.strftime("%Y-%m-%d") for o in scale],
                  "n_train": [len(y.loc[:o]) for o in scale],
                  "mase_scale_snaive12_insample_mae": list(scale.values())}
                 ).to_csv(OUT / "mase_scale_by_origin.csv", index=False, float_format="%.12g")

    # 1. reconciliation against the frozen RMSE table
    frozen = pd.read_csv(S1 / "phase2" / "metrics_by_horizon.csv")
    merged = full.merge(frozen, on=["model", "horizon"], suffixes=("", "_frozen"))
    assert len(merged) == 60
    diffs = {k: float((merged[k] - merged[f"{k}_frozen"]).abs().max()) for k in ["RMSE", "MAE", "bias"]}
    rec = {"max_abs_difference": diffs, "tolerance_RMSE": RMSE_TOL, "n_rows": len(merged),
           "pass": diffs["RMSE"] < RMSE_TOL}
    (OUT / "rmse_reconciliation.json").write_text(json.dumps(rec, indent=2) + "\n")
    if not rec["pass"]:
        print("STOP: RMSE does not reproduce phase2/metrics_by_horizon.csv", rec, file=sys.stderr)
        return 1

    # 2. persistence vs seasonal naive at h = 12
    h12 = pred[pred["horizon"] == 12].pivot(index="origin", columns="model", values="predicted")
    d = (h12["persistence"] - h12["seasonal_naive_12"]).abs()
    chk = {"n_origins": int(len(d)), "max_abs_difference": float(d.max()),
           "identical_in_all_origins": bool((d == 0).all()),
           "rmse_h12_persistence": float(full.query("model=='persistence' and horizon==12")["RMSE"].iloc[0]),
           "rmse_h12_seasonal_naive_12": float(full.query("model=='seasonal_naive_12' and horizon==12")["RMSE"].iloc[0])}
    (OUT / "h12_persistence_vs_snaive_check.json").write_text(json.dumps(chk, indent=2) + "\n")

    # 3. wide tables
    specs = {"MAE": ("%.1f", ".1f", "Mean absolute error (cases per month) by method and horizon, rolling origin (13 origins).", "tab:mae_h"),
             "bias": ("%.1f", ".1f", "Mean bias, mean(predicted $-$ observed) (cases per month), by method and horizon.", "tab:bias_h"),
             "MASE": ("%.3f", ".3f", "Mean absolute scaled error by method and horizon. Scale: in-sample MAE of the seasonal naive ($m=12$) on each origin's training window.", "tab:mase_h")}
    for metric, (csvfmt, texfmt, cap, lab) in specs.items():
        wide = full.pivot(index="model", columns="horizon", values=metric).loc[METHODS]
        wide.to_csv(OUT / f"table_{metric}.csv", float_format=csvfmt)
        (OUT / f"table_{metric}.tex").write_text(to_latex(wide, cap, lab, texfmt))

    print(json.dumps({"rmse_reconciliation": rec, "h12_check": chk}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
