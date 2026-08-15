"""Canonical Differential Evolution seed contract, per docs/METHOD_DECISION_LOG.md D024.

Frozen 2026-08-15, BEFORE any DE result was observed under these seeds. They carry no
scientific or epidemiological meaning -- purely deterministic-reproduction/robustness fixtures.

PRIMARY_SEED is PERMANENTLY the primary scientific estimate for both the fractional model and
the integer comparator. It must never be replaced by a result from DIAGNOSTIC_SEEDS for any
reason (lower RMSE, more convenient alpha, closer agreement with historical manuscript values,
better validation, or any other post hoc criterion).
"""

from __future__ import annotations

PRIMARY_SEED: int = 20260815

DIAGNOSTIC_SEEDS: list[int] = [20260816, 20260817, 20260818, 20260819]

ALL_SEEDS: list[int] = [PRIMARY_SEED, *DIAGNOSTIC_SEEDS]
