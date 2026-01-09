#!/usr/bin/env python3
"""Tests for statistical validation and deterministic RNG."""

import os
import sys
import pytest
import numpy as np
import pandas as pd
from scipy.stats import pearsonr

# Path hack to import from src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from statistical_validation import (
    bootstrap_correlation,
    permutation_test,
    cohens_d,
    calculate_correlation_matrix
)

RANDOM_SEED = 42

# --- Correlation Logic ---

def test_bootstrap_perfect_correlation():
    """Check bootstrap CI with identical linear data."""
    x = np.array([1, 2, 3, 4, 5], dtype=float)
    y = x * 2.0

    corr, low, upp = bootstrap_correlation(x, y, n_bootstrap=1000)

    assert corr == pytest.approx(1.0)
    assert low == pytest.approx(1.0)
    assert upp == pytest.approx(1.0)


def test_bootstrap_no_correlation():
    """CI should overlap zero for random noise."""
    rng = np.random.default_rng(RANDOM_SEED)
    x = rng.standard_normal(50)
    y = rng.standard_normal(50)

    corr, low, upp = bootstrap_correlation(x, y, n_bootstrap=1000)

    assert abs(corr) < 0.3
    assert low < 0 < upp


def test_permutation_test_significance():
    """Check if permutation test catches highly correlated data."""
    x = np.arange(20, dtype=float)
    y = x + np.random.default_rng(RANDOM_SEED).standard_normal(20) * 0.1

    corr, p_val = permutation_test(x, y, n_permutations=1000)

    assert corr > 0.9
    assert p_val < 0.05


# --- Effect Sizes ---

def test_cohens_d_identical_groups():
    """Effect size should be zero for same distributions."""
    g1 = np.array([1, 2, 3, 4, 5], dtype=float)
    g2 = np.array([1, 2, 3, 4, 5], dtype=float)

    assert cohens_d(g1, g2) == pytest.approx(0.0)


def test_cohens_d_large_effect():
    """Should detect significant separation in means."""
    g1 = np.array([10, 11, 12, 10, 12], dtype=float)
    g2 = np.array([1, 0, 2, 1, 1], dtype=float)

    d = cohens_d(g1, g2)
    assert d > 2.0


# --- Data Structure ---

def test_correlation_matrix_properties():
    """Check mathematical sanity of the correlation matrix."""
    df = pd.DataFrame({
        'feat_a': [1, 2, 3, 4, 5],
        'feat_b': [5, 4, 3, 2, 1],
        'target': [2, 4, 6, 8, 10]
    })
    
    cols = ['feat_a', 'feat_b', 'target']
    matrix = calculate_correlation_matrix(df, cols)

    assert matrix.shape == (3, 3)
    # Diagonals should be 1.0
    for col in cols:
        assert matrix.loc[col, col] == pytest.approx(1.0)
    # A vs B is inverse (-1.0)
    assert matrix.loc['feat_a', 'feat_b'] == pytest.approx(-1.0)


def test_statistical_determinism():
    """Check that stochastic tests give same results with fixed seed."""
    x = np.array([1, 2, 3, 4, 5, 6, 7, 8], dtype=float)
    y = np.array([1, 3, 2, 4, 5, 7, 6, 8], dtype=float)

    # First run
    c1, l1, u1 = bootstrap_correlation(x, y, n_bootstrap=100)
    _, p1 = permutation_test(x, y, n_permutations=100)

    # Second run
    c2, l2, u2 = bootstrap_correlation(x, y, n_bootstrap=100)
    _, p2 = permutation_test(x, y, n_permutations=100)

    assert c1 == c2
    assert l1 == l2
    assert u1 == u2
    assert p1 == p2
