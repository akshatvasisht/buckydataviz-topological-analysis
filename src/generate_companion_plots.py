#!/usr/bin/env python3
"""
Generates static charts (radar, bar, scatter) to complement the TDA graph.
Useful for quick reference and reports.
"""

import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

# --- Constants ---

# Visual Style Configuration
SNS_STYLE = "whitegrid"
PALETTE = "husl"
RESOLUTIONS = 300  # DPI

# Colors
COLOR_HIGH_PERF = '#2ecc71'
COLOR_LOW_PERF = '#e74c3c'
COLOR_HEADER = '#3498db'

# Feature Sets
FEATURES = [
    'energy_score', 'aggression_score',
    'cliche_score', 'complexity_score'
]

# File Paths (Relative to repository root)
INPUT_PATH = 'data/processed_fight_songs.csv'
IMAGE_DIR = 'docs/images'

# Global Configuration
sns.set_style(SNS_STYLE)
sns.set_palette(PALETTE)


def create_win_rate_ranking(df: pd.DataFrame, output_path: str) -> None:
    """Creates a horizontal bar chart of schools ranked by win rate."""
    df_sorted = df.sort_values('win_perc', ascending=True)

    fig, ax = plt.subplots(figsize=(10, 8))
    colors = plt.cm.RdYlGn(df_sorted['win_perc'])
    ax.barh(
        df_sorted['school'], df_sorted['win_perc'],
        color=colors, edgecolor='black', linewidth=1
    )

    ax.set_xlabel('Historical Win Percentage', fontsize=12, fontweight='bold')
    ax.set_title(
        'Big Ten Schools Ranked by All-Time Win Percentage',
        fontsize=14, fontweight='bold', pad=20
    )

    for i, (_, row) in enumerate(df_sorted.iterrows()):
        ax.text(row['win_perc'] + 0.01, i, f"{row['win_perc']:.3f}", va='center')

    ax.set_xlim(0.4, 0.8)
    plt.tight_layout()
    plt.savefig(output_path, dpi=RESOLUTIONS, bbox_inches='tight')
    plt.close()


def create_feature_radar(df: pd.DataFrame, output_path: str) -> None:
    """Generates a radar chart comparing high vs. low performing schools."""
    median_win = df['win_perc'].median()
    high_perf = df[df['win_perc'] > median_win]
    low_perf = df[df['win_perc'] <= median_win]

    high_means = [high_perf[f].mean() for f in FEATURES]
    low_means = [low_perf[f].mean() for f in FEATURES]

    # Radar geometry
    num_vars = len(FEATURES)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    # Close the loop
    high_means += high_means[:1]
    low_means += low_means[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))

    ax.plot(angles, high_means, 'o-', linewidth=2, label='High Win Rate', color=COLOR_HIGH_PERF)
    ax.fill(angles, high_means, alpha=0.25, color=COLOR_HIGH_PERF)

    ax.plot(angles, low_means, 'o-', linewidth=2, label='Low Win Rate', color=COLOR_LOW_PERF)
    ax.fill(angles, low_means, alpha=0.25, color=COLOR_LOW_PERF)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([f.replace('_', '\n').title() for f in FEATURES])
    ax.set_ylim(0, 10)
    ax.set_title(
        'Fight Song Feature Profiles\nHigh vs. Low Performance',
        fontsize=14, fontweight='bold', pad=30
    )
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

    plt.tight_layout()
    plt.savefig(output_path, dpi=RESOLUTIONS, bbox_inches='tight')
    plt.close()


def create_scatter_matrix(df: pd.DataFrame, output_path: str) -> None:
    """Grid of scatter plots showing feature correlations with win rates."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    axes = axes.flatten()

    for idx, feature in enumerate(FEATURES):
        ax = axes[idx]
        x, y = df[feature].values, df['win_perc'].values

        ax.scatter(
            x, y, c=df['win_perc'], cmap='RdYlGn',
            s=120, edgecolor='black', linewidth=1.5, alpha=0.8
        )

        # Reg line
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        x_line = np.linspace(x.min(), x.max(), 100)
        ax.plot(x_line, p(x_line), "r--", alpha=0.8, linewidth=2.5, label='Linear fit')

        # Stats
        corr, p_val = pearsonr(x, y)
        ax.text(
            0.05, 0.95, f'r = {corr:.3f}\np = {p_val:.3f}',
            transform=ax.transAxes, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
            fontweight='bold'
        )

        ax.set_xlabel(feature.replace('_', ' ').title(), fontweight='bold')
        ax.set_ylabel('Win Percentage', fontweight='bold')
        ax.grid(True, alpha=0.3)

    fig.suptitle('Musical Features vs. Success (N=18)', fontsize=16, fontweight='bold', y=1.0)
    plt.tight_layout()
    plt.savefig(output_path, dpi=RESOLUTIONS, bbox_inches='tight')
    plt.close()


def create_summary_table(df: pd.DataFrame, output_path: str) -> None:
    """Exports a summary statistics table as an image."""
    stats_df = df[FEATURES + ['win_perc']].describe().T[['mean', 'std', 'min', 'max']]
    stats_df = stats_df.round(2)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('tight')
    ax.axis('off')

    data = [['Feature', 'Mean', 'Std Dev', 'Min', 'Max']]
    for feature, row in stats_df.iterrows():
        data.append([
            feature.replace('_', ' ').title(),
            f"{row['mean']:.2f}", f"{row['std']:.2f}",
            f"{row['min']:.2f}", f"{row['max']:.2f}"
        ])

    table = ax.table(cellText=data, cellLoc='center', loc='center', bbox=[0, 0, 1, 1])
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 1.5)

    # Style header
    for i in range(5):
        cell = table[(0, i)]
        cell.set_facecolor(COLOR_HEADER)
        cell.set_text_props(weight='bold', color='white')

    plt.title('Feature Summary Statistics (N=18 Big Ten Schools)', fontweight='bold', pad=20)
    plt.savefig(output_path, dpi=RESOLUTIONS, bbox_inches='tight')
    plt.close()


def main() -> None:
    """Generate the full companion plot suite."""
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(root_dir, INPUT_PATH)
    out_dir = os.path.join(root_dir, IMAGE_DIR)

    os.makedirs(out_dir, exist_ok=True)
    df = pd.read_csv(input_file)

    print(f"Generating companion artifacts in {IMAGE_DIR}/...")
    create_win_rate_ranking(df, os.path.join(out_dir, 'win_rate_ranking.png'))
    create_feature_radar(df, os.path.join(out_dir, 'feature_radar.png'))
    create_scatter_matrix(df, os.path.join(out_dir, 'feature_scatter_matrix.png'))
    create_summary_table(df, os.path.join(out_dir, 'summary_statistics.png'))


if __name__ == '__main__':
    main()
