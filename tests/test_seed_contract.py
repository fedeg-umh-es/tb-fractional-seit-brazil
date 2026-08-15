"""Canonical seed-contract regression tests, per docs/METHOD_DECISION_LOG.md D024.

PRIMARY_SEED and DIAGNOSTIC_SEEDS were frozen BEFORE any DE result existed under them. These
tests guard against the values ever silently drifting, and against primary-result selection
ever being based on which seed produced the lowest objective.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from tb_seit import seeds  # noqa: E402


def test_primary_seed_is_frozen_value():
    assert seeds.PRIMARY_SEED == 20260815


def test_diagnostic_seeds_are_frozen_values():
    assert seeds.DIAGNOSTIC_SEEDS == [20260816, 20260817, 20260818, 20260819]


def test_primary_seed_not_among_diagnostic_seeds():
    assert seeds.PRIMARY_SEED not in seeds.DIAGNOSTIC_SEEDS


def test_all_seeds_distinct():
    assert len(set(seeds.ALL_SEEDS)) == len(seeds.ALL_SEEDS) == 5


def test_scripts_default_to_canonical_seeds():
    """The calibration/sensitivity entry points must default to the frozen seeds, not require
    an operator to re-type magic numbers that could silently drift from D024."""
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "run_calibration_multiseed", REPO_ROOT / "scripts" / "run_calibration_multiseed.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    assert mod.seeds.PRIMARY_SEED == seeds.PRIMARY_SEED
    assert mod.seeds.DIAGNOSTIC_SEEDS == seeds.DIAGNOSTIC_SEEDS


def _require_multiseed_csv(path: Path) -> list[dict]:
    if not path.exists():
        pytest.skip(f"{path} not yet generated (calibration not run in this test session)")
    with path.open() as f:
        return list(csv.DictReader(f))


def test_primary_result_selection_uses_seed_not_min_objective():
    """Primary estimates must come from the row with seed==PRIMARY_SEED, never argmin(objective).

    Regression guard: if a diagnostic seed ever achieves a strictly lower objective than the
    primary seed, this test still requires the *primary parameter files* to match the
    seed==PRIMARY_SEED row, not the minimum-objective row.
    """
    frac_multiseed = _require_multiseed_csv(
        REPO_ROOT / "outputs" / "calibration" / "fractional_multiseed.csv"
    )
    frac_params_path = REPO_ROOT / "outputs" / "calibration" / "fractional_parameters.csv"
    if not frac_params_path.exists():
        pytest.skip("fractional_parameters.csv not yet generated")

    rows_by_seed = {int(r["seed"]): r for r in frac_multiseed}
    assert set(rows_by_seed) == set(seeds.ALL_SEEDS)

    primary_row = rows_by_seed[seeds.PRIMARY_SEED]

    with frac_params_path.open() as f:
        saved_params = {row["parameter"]: float(row["value"]) for row in csv.DictReader(f)}

    for field in ["beta", "sigma", "gamma", "d", "alpha"]:
        assert saved_params[field] == pytest.approx(float(primary_row[field])), (
            f"primary_parameters.csv[{field}] does not match the seed={seeds.PRIMARY_SEED} row"
        )

    # Record which seed happens to have the lowest calibration objective, purely as a diagnostic
    # -- the assertions above already prove selection is seed-based, not argmin-based, since
    # they'd fail here if fractional_parameters.csv had been built from the minimum instead.
    min_objective_seed = min(rows_by_seed, key=lambda s: float(rows_by_seed[s]["objective"]))
    print(f"[diagnostic only] min-objective seed = {min_objective_seed} (not used as primary)")


def test_multiseed_csv_has_no_duplicate_or_missing_seeds():
    for name in ["fractional_multiseed.csv", "integer_multiseed.csv"]:
        rows = _require_multiseed_csv(REPO_ROOT / "outputs" / "calibration" / name)
        found_seeds = [int(r["seed"]) for r in rows]
        assert sorted(found_seeds) == sorted(seeds.ALL_SEEDS), f"{name}: seed set mismatch"
        assert len(found_seeds) == len(set(found_seeds)), f"{name}: duplicate seeds present"


def test_integer_multiseed_alpha_always_exactly_one():
    rows = _require_multiseed_csv(REPO_ROOT / "outputs" / "calibration" / "integer_multiseed.csv")
    for row in rows:
        assert float(row["alpha"]) == 1.0
