"""Canonical dataset loading and temporal split, per PROJECT_CANON.md.

Calibration: 2001-01 to 2020-12 (N=240). Validation: 2021-01 to 2022-12 (N=24).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
RAW_PATH = REPO_ROOT / "data" / "raw" / "tb_mes.xlsx"

CALIBRATION_START = pd.Timestamp("2001-01-01")
CALIBRATION_END = pd.Timestamp("2020-12-01")
VALIDATION_START = pd.Timestamp("2021-01-01")
VALIDATION_END = pd.Timestamp("2022-12-01")

CANONICAL_TOTAL = 264
CANONICAL_CALIBRATION = 240
CANONICAL_VALIDATION = 24


@dataclass(frozen=True)
class CanonicalDataset:
    full: pd.DataFrame
    calibration: pd.DataFrame
    validation: pd.DataFrame


def load_canonical_dataset(raw_path: Path = RAW_PATH) -> CanonicalDataset:
    df = pd.read_excel(raw_path)
    df = df[["data", "casos", "populacao"]].rename(
        columns={"data": "date", "casos": "cases", "populacao": "population"}
    )
    df = df.sort_values("date").reset_index(drop=True)

    if len(df) != CANONICAL_TOTAL:
        raise ValueError(
            f"expected {CANONICAL_TOTAL} monthly observations, found {len(df)}"
        )

    calibration = df[
        (df["date"] >= CALIBRATION_START) & (df["date"] <= CALIBRATION_END)
    ].reset_index(drop=True)
    validation = df[
        (df["date"] >= VALIDATION_START) & (df["date"] <= VALIDATION_END)
    ].reset_index(drop=True)

    if len(calibration) != CANONICAL_CALIBRATION:
        raise ValueError(
            f"expected {CANONICAL_CALIBRATION} calibration observations, "
            f"found {len(calibration)}"
        )
    if len(validation) != CANONICAL_VALIDATION:
        raise ValueError(
            f"expected {CANONICAL_VALIDATION} validation observations, "
            f"found {len(validation)}"
        )

    calibration_dates = set(calibration["date"])
    validation_dates = set(validation["date"])
    if calibration_dates & validation_dates:
        raise ValueError("calibration and validation date sets overlap")

    return CanonicalDataset(full=df, calibration=calibration, validation=validation)


def month_index(dates: pd.Series, origin: pd.Timestamp = CALIBRATION_START) -> pd.Series:
    """Integer month offset from the calibration origin (2001-01 -> 0)."""
    return (
        (dates.dt.year - origin.year) * 12 + (dates.dt.month - origin.month)
    ).astype(int)
