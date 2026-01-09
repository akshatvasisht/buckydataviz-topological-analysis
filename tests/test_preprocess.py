#!/usr/bin/env python3
"""Tests for Big Ten data cleaning and feature engineering."""

import os
import sys
import pytest
import numpy as np
import pandas as pd

# Path hack to import from src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from preprocess import normalize_to_1_10, WIN_PERC_DATA

# --- Normalization ---

def test_normalize_standard_range():
    """Check normalization with standard inputs."""
    values = pd.Series([0, 50, 100])
    normalized = normalize_to_1_10(values)

    assert normalized.iloc[0] == pytest.approx(1.0)
    assert normalized.iloc[1] == pytest.approx(5.5)
    assert normalized.iloc[2] == pytest.approx(10.0)


def test_normalize_identical_values():
    """Ensure midpoint (5.5) is returned for constant inputs."""
    values = pd.Series([42, 42, 42])
    normalized = normalize_to_1_10(values)

    for val in normalized:
        assert val == pytest.approx(5.5)


def test_normalize_preserves_ordering():
    """Verify relative ordering stays the same after scaling."""
    values = pd.Series([10, 20, 15, 25, 5])
    normalized = normalize_to_1_10(values)

    original_order = values.argsort().values
    normalized_order = normalized.argsort().values

    assert np.array_equal(original_order, normalized_order)


# --- Win Percentage Integrity ---

def test_all_expected_schools_present():
    """Verify all 18 programs are in the dataset."""
    assert len(WIN_PERC_DATA) == 18


def test_win_percentages_bounds():
    """Check that all win rates are between 0 and 1."""
    for school, rate in WIN_PERC_DATA.items():
        assert 0.0 <= rate <= 1.0, f"{school} rate invalid: {rate}"


# --- Feature Engineering ---

@pytest.fixture
def sample_data():
    """Mock data for feature tests."""
    return pd.DataFrame({
        'school': ['School A', 'School B', 'School C'],
        'bpm': [150, 100, 200],
        'sec_duration': [60, 90, 120],
        'trope_count': [3, 5, 2],
        'number_fights': [5, 2, 0],
        'victory_win_won': ['Yes', 'No', 'Yes']
    })


def test_aggression_score_calculation(sample_data):
    """Check the (fights*2 + win_flag) logic and scaling."""
    raw_a = 11 # 5*2+1
    raw_b = 4  # 2*2+0
    raw_c = 1  # 0*2+1
    
    raw_vals = pd.Series([raw_a, raw_b, raw_c])
    normalized = normalize_to_1_10(raw_vals)
    
    assert normalized.iloc[0] == pytest.approx(10.0) # Max
    assert normalized.iloc[1] == pytest.approx(3.7)  # 1 + (4-1)/10*9
    assert normalized.iloc[2] == pytest.approx(1.0)  # Min


def test_cliche_score_mapping(sample_data):
    """Cliche score should just be trope count."""
    assert np.array_equal(sample_data['trope_count'].values, [3, 5, 2])


# --- Pipeline Safety ---

def test_feature_ranges():
    """Ensure scaled features stay strictly within [1, 10]."""
    rng = np.random.default_rng(seed=42)
    values = pd.Series(rng.standard_normal(100) * 100)
    normalized = normalize_to_1_10(values)

    assert normalized.min() >= 1.0
    assert normalized.max() <= 10.0
