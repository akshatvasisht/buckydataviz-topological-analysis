#!/usr/bin/env python3
"""
Statistical validation for Big Ten fight songs.

Analyzes the relationship between song features and team performance. 
Given N=18, we prioritize bootstrap CIs and effect sizes over raw p-values.
"""

import os
import warnings
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import pearsonr, spearmanr

# --- Constants ---

# Global random seed for reproducibility
RANDOM_STATE = 42

# Analytical Parameters
N_BOOTSTRAP = 10000
N_PERMUTATIONS = 10000
CONFIDENCE_LEVEL = 0.95

# Feature and Target Columns
FEATURE_COLS = [
    'energy_score', 'aggression_score',
    'cliche_score', 'complexity_score'
]
TARGET_COL = 'win_perc'

# File Paths (Relative to repository root)
INPUT_PATH = 'data/processed_fight_songs.csv'
REPORT_CSV = 'data/correlation_analysis.csv'
DOCS_DIR = 'docs'
IMAGE_DIR = 'docs/images'

# Plotting Configuration
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
warnings.filterwarnings('ignore')  # Suppress small-N warnings


def calculate_correlation_matrix(df: pd.DataFrame, features: List[str]) -> pd.DataFrame:
    """Simple Pearson correlation matrix."""
    return df[features].corr(method='pearson')


def bootstrap_correlation(
    x: np.ndarray,
    y: np.ndarray,
    n_bootstrap: int = N_BOOTSTRAP,
    confidence_level: float = CONFIDENCE_LEVEL
) -> Tuple[float, float, float]:
    """
    Run bootstrap to get CIs for Pearson r.

    Helpful for N=18 where standard p-values are noisy.
    """
    # Ensure reproducibility with local RNG
    rng = np.random.default_rng(RANDOM_STATE)
    n = len(x)
    correlations = []

    for _ in range(n_bootstrap):
        # Sample with replacement
        indices = rng.choice(n, size=n, replace=True)
        boot_x, boot_y = x[indices], y[indices]
        # Ignore p-value for bootstrap samples
        corr, _ = pearsonr(boot_x, boot_y)
        if not np.isnan(corr):
            correlations.append(corr)

    if not correlations:
        return observed_corr, np.nan, np.nan

    correlations = np.array(correlations)
    observed_corr, _ = pearsonr(x, y)

    alpha = 1 - confidence_level
    lower_ci = np.percentile(correlations, 100 * (alpha / 2))
    upper_ci = np.percentile(correlations, 100 * (1 - alpha / 2))

    return observed_corr, lower_ci, upper_ci


def permutation_test(
    x: np.ndarray,
    y: np.ndarray,
    n_permutations: int = N_PERMUTATIONS
) -> Tuple[float, float]:
    """
    Non-parametric permutation test for r-value significance.
    """
    # Ensure reproducibility with local RNG
    rng = np.random.default_rng(RANDOM_STATE)
    observed_corr, _ = pearsonr(x, y)

    permuted_corrs = []
    for _ in range(n_permutations):
        # Shuffle target variable
        permuted_y = rng.permutation(y)
        perm_corr, _ = pearsonr(x, permuted_y)
        permuted_corrs.append(perm_corr)

    permuted_corrs = np.array(permuted_corrs)
    # Calculate two-tailed p-value
    p_value = np.mean(np.abs(permuted_corrs) >= np.abs(observed_corr))

    return observed_corr, p_value


def cohens_d(group1: np.ndarray, group2: np.ndarray) -> float:
    """Standard Cohen's d for effect size."""
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    # Pooled standard deviation
    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    return (np.mean(group1) - np.mean(group2)) / pooled_std


def analyze_feature_correlations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform a comprehensive correlation suite between features and performance.

    Args:
        df: Processed fight song DataFrame.

    Returns:
        pd.DataFrame: Analysis results including CI and p-values.
    """
    results = []

    for feature in FEATURE_COLS:
        x_vals, y_vals = df[feature].values, df[TARGET_COL].values

        # Deterministic bootstrap and permutation
        corr, low_ci, upp_ci = bootstrap_correlation(x_vals, y_vals)
        _, p_val = permutation_test(x_vals, y_vals)
        rho, _ = spearmanr(x_vals, y_vals)

        results.append({
            'Feature': feature,
            'Pearson_r': corr,
            'CI_lower': low_ci,
            'CI_upper': upp_ci,
            'p_value': p_val,
            'Spearman_rho': rho,
            'Significant': 'Yes' if p_val < 0.05 else 'No'
        })

    return pd.DataFrame(results)


def plot_correlation_heatmap(corr_matrix: pd.DataFrame, output_path: str) -> None:
    """Export a publication-quality correlation heatmap."""
    plt.figure(figsize=(10, 8))
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    sns.heatmap(
        corr_matrix, mask=mask, annot=True, fmt='.2f',
        cmap='coolwarm', center=0, square=True, linewidths=1,
        cbar_kws={'label': 'Pearson Correlation'}
    )
    plt.title('Feature Correlation Matrix\nBig Ten Fight Songs (N=18)', pad=20)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()


def generate_statistical_report(df: pd.DataFrame, root_dir: str) -> None:
    """Print results and export summary plots."""
    print("=" * 80)
    print("STATISTICAL VALIDATION REPORT")
    print("=" * 80)
    print(f"\nAnalysis Sample: N = {len(df)}")
    print("\n[NOTE] Exploratory analysis. Results are hypothesis-generating.\n")

    # 1. Correlation Suite
    print("-" * 80)
    print("Feature Correlations vs. Win Percentage")
    print("-" * 80)
    corr_results = analyze_feature_correlations(df)
    print(corr_results.to_string(index=False))

    # 2. Manifold Comparison
    print(f"\n{'-' * 80}")
    print("Group Comparison: High vs. Low Energy Manifolds (Median Split)")
    print("-" * 80)
    median_energy = df['energy_score'].median()
    high_e = df[df['energy_score'] > median_energy][TARGET_COL].values
    low_e = df[df['energy_score'] <= median_energy][TARGET_COL].values

    u_stat, p_val = stats.mannwhitneyu(high_e, low_e, alternative='two-sided')
    d_val = cohens_d(high_e, low_e)

    print(f"High Energy Mean Win: {np.mean(high_e):.3f}")
    print(f"Low Energy Mean Win: {np.mean(low_e):.3f}")
    print(f"Difference: {np.mean(high_e) - np.mean(low_e):.3f}")
    print(f"Effect Size (Cohen's d): {d_val:.3f}")
    print(f"Mann-Whitney U P-Value: {p_val:.4f}")

    # 3. Visualizations
    img_dir = os.path.join(root_dir, IMAGE_DIR)
    os.makedirs(img_dir, exist_ok=True)

    matrix = calculate_correlation_matrix(df, FEATURE_COLS + [TARGET_COL])
    plot_correlation_heatmap(matrix, os.path.join(img_dir, 'correlation_heatmap.png'))
    print(f"\nArtifacts exported to {IMAGE_DIR}/")


def main() -> None:
    """Execute the full validation pipeline."""
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(root_dir, INPUT_PATH)
    output_csv = os.path.join(root_dir, REPORT_CSV)

    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Missing processed data: {INPUT_PATH}")

    df = pd.read_csv(input_file)
    generate_statistical_report(df, root_dir)

    # Save artifact
    analyze_feature_correlations(df).to_csv(output_csv, index=False)
    print(f"Statistical report saved to {REPORT_CSV}")


if __name__ == '__main__':
    main()
