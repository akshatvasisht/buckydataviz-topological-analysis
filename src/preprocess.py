#!/usr/bin/env python3
"""
Clean 538 fight songs data and add Big Ten conference/win percentage info.

Steps:
1. Map 2024 expansion schools to Big Ten.
2. Filter for Big Ten schools only.
3. Attach historical win percentages.
4. Scale features (Energy, Aggression, etc.) for TDA.
"""

import os
from typing import Dict

import numpy as np
import pandas as pd

# --- Constants ---

# Historical win percentage data (all-time records)
# Source: https://en.wikipedia.org/wiki/Big_Ten_Conference#All-time_school_records
WIN_PERC_DATA: Dict[str, float] = {
    'Ohio State': 0.735, 'Michigan': 0.732, 'USC': 0.694, 'Penn State': 0.691,
    'Nebraska': 0.677, 'Washington': 0.620, 'Michigan State': 0.596,
    'Wisconsin': 0.584, 'UCLA': 0.586, 'Oregon': 0.582, 'Minnesota': 0.573,
    'Iowa': 0.546, 'Maryland': 0.520, 'Purdue': 0.513, 'Illinois': 0.507,
    'Rutgers': 0.491, 'Northwestern': 0.448, 'Indiana': 0.421
}

# Conference expansion mapping (2024 realignment)
EXPANSION_SCHOOLS = ['USC', 'UCLA', 'Oregon', 'Washington']
TARGET_CONFERENCE = 'Big Ten'

# Feature normalization bounds
NORM_MIN = 1.0
NORM_MAX = 10.0
NORM_MID = 5.5

# File paths (Relative to repository root)
DATA_PATH = 'data/fight-songs.csv'
OUTPUT_PATH = 'data/processed_fight_songs.csv'


def normalize_to_1_10(values: pd.Series) -> pd.Series:
    """
    Min-max scale a series to 1-10.

    Keeping features on the same scale prevents one (like BPM) from 
    dominating distance calculations in higher dimensions.
    """
    min_val = values.min()
    max_val = values.max()

    # Handle identical values to avoid division by zero
    if max_val == min_val:
        return pd.Series([NORM_MID] * len(values), index=values.index)

    normalized = NORM_MIN + ((values - min_val) / (max_val - min_val)) * (NORM_MAX - NORM_MIN)
    return normalized


def main() -> None:
    """Run the preprocessing pipeline."""
    # Get absolute directory of project root
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(root_dir, DATA_PATH)
    output_file = os.path.join(root_dir, OUTPUT_PATH)

    print(f"Loading {DATA_PATH}...")
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found at {input_file}")

    df = pd.read_csv(input_file)

    # 2024 realignment
    print("Applying 2024 realignment...")
    df.loc[
        df['school'].isin(EXPANSION_SCHOOLS) & (df['conference'] == 'Pac-12'),
        'conference'
    ] = TARGET_CONFERENCE

    # Filter to target conference
    df_big10 = df[df['conference'] == TARGET_CONFERENCE].copy()
    print(f"Identified {len(df_big10)} {TARGET_CONFERENCE} programs.")

    # Add historical performance data
    print("Mapping historical win percentages...")
    df_big10['win_perc'] = df_big10['school'].map(WIN_PERC_DATA)

    # Check for missing data
    missing = df_big10[df_big10['win_perc'].isna()]
    if not missing.empty:
        print(f"Warning: Missing data for schools: {missing['school'].tolist()}")

    # Feature Engineering
    print("Scaling and engineering TDA features...")

    # Cliche Score (Trope Count)
    df_big10['cliche_score'] = df_big10['trope_count']

    # Aggression Score (Weighting fights and victory language)
    df_big10['aggression_score'] = (df_big10['number_fights'] * 2) + \
        df_big10['victory_win_won'].map({'Yes': 1, 'No': 0})
    df_big10['aggression_score'] = normalize_to_1_10(df_big10['aggression_score'])

    # Complexity Score (Duration)
    df_big10['complexity_score'] = normalize_to_1_10(df_big10['sec_duration'])

    # Energy Score (Tempo)
    df_big10['energy_score'] = normalize_to_1_10(df_big10['bpm'])

    # Save processed artifact
    print(f"Saving artifacts to {OUTPUT_PATH}...")
    df_big10.to_csv(output_file, index=False)

    print("\nProcessing complete. Included Programs:")
    for school in sorted(df_big10['school'].unique()):
        print(f"  - {school}")


if __name__ == '__main__':
    main()
