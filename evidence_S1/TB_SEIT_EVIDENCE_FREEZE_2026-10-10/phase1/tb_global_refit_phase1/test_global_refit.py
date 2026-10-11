"""Unit tests for the ordinary observation postprocessor only.

These do not replace the mandatory real-data preflight of run_global_refit.py.
"""
from types import SimpleNamespace

import numpy as np

from run_global_refit import ordinary_monthly_flow


def fake_solver(e):
    states = np.zeros((len(e), 5), dtype=float)
    states[:, 1] = e
    return SimpleNamespace(status="ok", y=states)


def test_constant_flow():
    assert np.allclose(ordinary_monthly_flow(fake_solver(np.ones(4) * 12), 2.0, 3, 1.0), [24,24,24])


def test_linear_flow_monthly():
    # E(t)=t+1 and sigma=2: exact integrals are 3 and 5.
    assert np.allclose(ordinary_monthly_flow(fake_solver(np.array([1.,2.,3.])), 2.0, 2, 1.0), [3.,5.])


def test_linear_flow_submonthly():
    assert np.allclose(ordinary_monthly_flow(fake_solver(np.array([1.,1.5,2.,2.5,3.])), 2.0, 2, 0.5), [3.,5.])


def test_invalid_grid_rejected():
    import pytest
    with pytest.raises(ValueError):
        ordinary_monthly_flow(fake_solver(np.array([1.,2.,3.])), 2.0, 2, 0.3)
