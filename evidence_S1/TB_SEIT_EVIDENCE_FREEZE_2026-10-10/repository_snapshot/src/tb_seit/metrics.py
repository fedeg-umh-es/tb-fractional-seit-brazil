"""RMSE / MAE / bias, per docs/MODEL_CONTRACT.md Section 3 (A25, A30-A32). No AIC here."""

from __future__ import annotations

import numpy as np


def rmse(observed: np.ndarray, predicted: np.ndarray) -> float:
    observed = np.asarray(observed, dtype=float)
    predicted = np.asarray(predicted, dtype=float)
    return float(np.sqrt(np.mean((observed - predicted) ** 2)))


def mae(observed: np.ndarray, predicted: np.ndarray) -> float:
    observed = np.asarray(observed, dtype=float)
    predicted = np.asarray(predicted, dtype=float)
    return float(np.mean(np.abs(observed - predicted)))


def bias(observed: np.ndarray, predicted: np.ndarray) -> float:
    """bias = mean(predicted - observed), per docs/MODEL_CONTRACT.md A32."""
    observed = np.asarray(observed, dtype=float)
    predicted = np.asarray(predicted, dtype=float)
    return float(np.mean(predicted - observed))
