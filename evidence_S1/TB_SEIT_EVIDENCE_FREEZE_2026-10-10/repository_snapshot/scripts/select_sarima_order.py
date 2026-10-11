"""Execute the SARIMA order-selection procedure frozen in docs/SARIMA_BASELINE_CONTRACT.md,
using ONLY 2001-01..2020-12 (canonical calibration data). Never inspects 2021-2022.

Writes outputs/forecasting/sarima_frozen_order.json (selected order + full AIC grid table).
"""

from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from tb_seit import data  # noqa: E402

OUT_PATH = REPO_ROOT / "outputs/forecasting/sarima_frozen_order.json"

D_FIXED = 1
SEASONAL_D_FIXED = 1
S = 12
P_GRID = [0, 1, 2]
Q_GRID = [0, 1, 2]
SEASONAL_P_GRID = [0, 1]
SEASONAL_Q_GRID = [0, 1]


def main() -> None:
    from statsmodels.tsa.statespace.sarimax import SARIMAX

    dataset = data.load_canonical_dataset()
    series = dataset.calibration["cases"].to_numpy(dtype=float)  # 2001-01..2020-12 ONLY

    results = []
    for p in P_GRID:
        for q in Q_GRID:
            for sp in SEASONAL_P_GRID:
                for sq in SEASONAL_Q_GRID:
                    order = (p, D_FIXED, q)
                    seasonal_order = (sp, SEASONAL_D_FIXED, sq, S)
                    try:
                        with warnings.catch_warnings():
                            warnings.simplefilter("ignore")
                            model = SARIMAX(
                                series, order=order, seasonal_order=seasonal_order,
                                enforce_stationarity=False, enforce_invertibility=False,
                            )
                            fit = model.fit(disp=False)
                        aic = float(fit.aic)
                        converged = bool(fit.mle_retvals.get("converged", True)) if hasattr(fit, "mle_retvals") else True
                    except Exception as exc:  # noqa: BLE001
                        aic = float("inf")
                        converged = False
                    results.append(
                        {
                            "p": p, "d": D_FIXED, "q": q,
                            "P": sp, "D": SEASONAL_D_FIXED, "Q": sq, "s": S,
                            "aic": aic, "converged": converged,
                            "n_params": p + q + sp + sq,
                        }
                    )
                    print(f"order=({p},{D_FIXED},{q}) seasonal=({sp},{SEASONAL_D_FIXED},{sq},{S}) "
                          f"AIC={aic:.3f} converged={converged}")

    finite = [r for r in results if np_isfinite(r["aic"])]
    finite.sort(key=lambda r: (r["aic"], r["n_params"], r["p"]))
    best = finite[0]

    payload = {
        "grid_policy": "docs/SARIMA_BASELINE_CONTRACT.md",
        "selection_data": "2001-01 to 2020-12 (canonical calibration only)",
        "selected_order": {"p": best["p"], "d": best["d"], "q": best["q"]},
        "selected_seasonal_order": {
            "P": best["P"], "D": best["D"], "Q": best["Q"], "s": best["s"]
        },
        "selected_aic": best["aic"],
        "full_grid": results,
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(payload, indent=2))
    print(f"\nWrote {OUT_PATH.relative_to(REPO_ROOT)}")
    print(f"FROZEN ORDER: SARIMA({best['p']},{best['d']},{best['q']})"
          f"({best['P']},{best['D']},{best['Q']},{best['s']})  AIC={best['aic']:.3f}")


def np_isfinite(x: float) -> bool:
    import math

    return math.isfinite(x)


if __name__ == "__main__":
    main()
