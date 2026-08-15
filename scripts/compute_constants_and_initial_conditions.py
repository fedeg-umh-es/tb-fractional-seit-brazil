"""Write outputs/model_constants.json and outputs/initial_conditions.json.

mu, Lambda per docs/EXTERNAL_PARAMETER_CONTRACT.md Section 2/4.
Initial conditions per docs/MODEL_CONTRACT.md Section 5. Uses only the FIRST calibration month's
observed cases as flow0 -- no free/estimated initial-condition parameters. The E0/I0 values
recorded here use a fixed reference parameter vector (bounds midpoint) purely for illustration/
auditability; during actual calibration, E0/I0 are recomputed per DE-candidate, per contract.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from tb_seit import constants, data, model  # noqa: E402

OUTPUT_CONSTANTS = REPO_ROOT / "outputs" / "model_constants.json"
OUTPUT_INITIAL = REPO_ROOT / "outputs" / "initial_conditions.json"

# Bounds midpoint reference vector -- used ONLY to illustrate the initial-condition
# construction here; NOT a calibration result. See docs/MODEL_CONTRACT.md Section 3/4.
REFERENCE_PARAMS = model.SeitParameters(
    beta=(0.01 + 1.00) / 2,
    sigma=(0.01 + 0.50) / 2,
    gamma=(0.05 + 0.30) / 2,
    d=(0.0001 + 0.05) / 2,
    alpha=(0.50 + 1.00) / 2,
)


def main() -> None:
    dataset = data.load_canonical_dataset()
    mc = constants.compute_model_constants(dataset.calibration["population"])

    constants_payload = {
        "mu": {
            "value": mc.mu,
            "formula": "1 / (life_expectancy_years * 12)",
            "life_expectancy_years": mc.life_expectancy_years,
            "source": "docs/EXTERNAL_PARAMETER_CONTRACT.md, mu row; METHOD_DECISION_LOG.md D015",
        },
        "lambda": {
            "value": mc.lambda_,
            "formula": "mu * mean(N_dataset over 2001-01..2020-12)",
            "mean_training_population": mc.mean_training_population,
            "source": "docs/EXTERNAL_PARAMETER_CONTRACT.md Section 2/4",
        },
    }
    OUTPUT_CONSTANTS.write_text(json.dumps(constants_payload, indent=2))
    print(f"Wrote {OUTPUT_CONSTANTS.relative_to(REPO_ROOT)}")

    N0 = float(dataset.calibration["population"].iloc[0])
    flow0 = float(dataset.calibration["cases"].iloc[0])
    t0_date = str(dataset.calibration["date"].iloc[0].date())

    y0 = model.initial_conditions(REFERENCE_PARAMS, mc.mu, N0, flow0)

    initial_payload = {
        "t0_date": t0_date,
        "N0": N0,
        "flow0_observed_cases": flow0,
        "construction": {
            "E0": "flow0 / sigma",
            "I0": "sigma * E0 / (gamma + mu + d)",
            "T0": "0 (fixed; T decoupled from S/E/I)",
            "S0": "N0 - E0 - I0 - T0",
            "C0": "0 (accumulator origin)",
        },
        "reference_parameter_vector_note": (
            "S0/E0/I0/T0 values below use the bounds-midpoint reference parameter vector for "
            "illustration only; during calibration these are recomputed per DE-candidate "
            "(sigma, gamma, d), never treated as free parameters."
        ),
        "reference_parameters": {
            "beta": REFERENCE_PARAMS.beta,
            "sigma": REFERENCE_PARAMS.sigma,
            "gamma": REFERENCE_PARAMS.gamma,
            "d": REFERENCE_PARAMS.d,
            "alpha": REFERENCE_PARAMS.alpha,
        },
        "reference_initial_state": {
            "S0": y0[0],
            "E0": y0[1],
            "I0": y0[2],
            "T0": y0[3],
            "C0": y0[4],
        },
    }
    OUTPUT_INITIAL.write_text(json.dumps(initial_payload, indent=2))
    print(f"Wrote {OUTPUT_INITIAL.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
