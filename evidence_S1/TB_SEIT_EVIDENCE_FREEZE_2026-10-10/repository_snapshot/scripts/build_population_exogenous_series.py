"""Build outputs/audits/population_exogenous_series.csv, per docs/EXTERNAL_PARAMETER_CONTRACT.md.

Does not perform any model calibration; purely a deterministic data-preparation step.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from tb_seit import data, population  # noqa: E402

OUTPUT_CSV = REPO_ROOT / "outputs" / "audits" / "population_exogenous_series.csv"
OUTPUT_META = REPO_ROOT / "outputs" / "audits" / "population_exogenous_series_trend.json"


def main() -> None:
    dataset = data.load_canonical_dataset()
    series, trend = population.build_population_exogenous_series(dataset)

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    series.to_csv(OUTPUT_CSV, index=False)

    meta = {
        "equation": "ln(N(t)) = intercept + slope * t_months, t_months = months since 2001-01",
        "intercept": trend.intercept,
        "slope": trend.slope,
        "fit_window": "2001-01 to 2020-12 (calibration only)",
        "method": "numpy.polyfit(deg=1) on ln(population) vs month index",
        "validation_rule": (
            "2021-01 to 2022-12 N_model_input = exp(intercept + slope*t_months); "
            "N_dataset for those months is recorded for audit only and is never used as "
            "model input (source_type=TRAIN_ONLY_EXTRAPOLATION)."
        ),
    }
    OUTPUT_META.write_text(json.dumps(meta, indent=2))

    print(f"Wrote {OUTPUT_CSV.relative_to(REPO_ROOT)}")
    print(f"Wrote {OUTPUT_META.relative_to(REPO_ROOT)}")
    print(trend.equation_string())


if __name__ == "__main__":
    main()
