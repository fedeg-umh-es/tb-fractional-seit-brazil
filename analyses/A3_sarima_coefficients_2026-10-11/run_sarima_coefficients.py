"""Step 3 (Plan A continuation): per-origin SARIMA coefficients and reproduction control.

Protocol: PROTOCOL.md in this folder (committed before this script was run).
Uses the same SARIMAX call as scripts/run_rolling_origin_forecast.py::fit_sarima.
"""

import json
import os
import sys
import warnings
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))
from tb_seit import rolling_origin as ro  # noqa: E402
from statsmodels.tsa.statespace.sarimax import SARIMAX  # noqa: E402
import statsmodels  # noqa: E402

OUT = Path(__file__).resolve().parent
S1 = REPO / "evidence_S1" / "TB_SEIT_EVIDENCE_FREEZE_2026-10-10"
TOL = 1e-6


def main() -> int:
    meta = json.loads((REPO / "outputs/forecasting/sarima_frozen_order.json").read_text())
    o, so = meta["selected_order"], meta["selected_seasonal_order"]
    archived = pd.read_csv(S1 / "phase2" / "rolling_origin_predictions.csv", parse_dates=["origin"])
    archived = archived[archived["model"] == "SARIMA"]
    assert len(archived) == 156

    rows, rel_errs, problems = [], [], []
    for origin in ro.ORIGINS:
        ts = ro.build_training_set(origin)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            m = SARIMAX(ts.train_cases, order=(o["p"], o["d"], o["q"]),
                        seasonal_order=(so["P"], so["D"], so["Q"], so["s"]),
                        enforce_stationarity=False, enforce_invertibility=False)
            fit = m.fit(disp=False)
        fc = np.asarray(fit.get_forecast(12).predicted_mean, dtype=float)
        conv = bool(fit.mle_retvals.get("converged", False))
        if not conv:
            problems.append(f"{origin:%Y-%m}: optimizer did not report convergence")
        if not np.all(np.isfinite(fc)) or not np.all(np.isfinite(fit.params)):
            problems.append(f"{origin:%Y-%m}: non-finite values")
        arch = archived[archived["origin"] == origin].sort_values("horizon")["predicted"].to_numpy()
        rel = np.abs(fc - arch) / np.abs(arch)
        rel_errs.append(rel)
        row = {"origin": f"{origin:%Y-%m-%d}", "n_train": ts.n_train}
        for name, val, se in zip(fit.param_names, fit.params, fit.bse):
            row[f"{name}"] = val
            row[f"{name}_se"] = se
        row.update(llf=float(fit.llf), aic=float(fit.aic), nobs=int(fit.nobs), converged=conv,
                   n_warnings=len(caught), max_rel_err_forecast=float(rel.max()))
        rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv(OUT / "sarima_coefficients_by_origin.csv", index=False, float_format="%.12g")
    max_rel = float(np.max(np.concatenate(rel_errs)))
    ctrl = {"statsmodels": statsmodels.__version__, "numpy": np.__version__,
            "order": o, "seasonal_order": so, "n_origins": len(rows),
            "n_forecasts_compared": int(sum(len(r) for r in rel_errs)),
            "max_relative_error": max_rel, "tolerance": TOL,
            "all_converged": bool(df["converged"].all()), "problems": problems,
            "pass": bool(max_rel <= TOL and not problems)}
    (OUT / "reproduction_control.json").write_text(json.dumps(ctrl, indent=2) + "\n")
    print(json.dumps(ctrl, indent=2))
    return 0 if ctrl["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
