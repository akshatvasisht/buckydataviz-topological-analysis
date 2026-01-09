#!/usr/bin/env python3
"""
Generate TDA visualization for Big Ten fight songs.

Uses KeplerMapper to build a graph-based representation of schools in 
high-dimensional feature space, surfaced in an interactive HTML dashboard.
"""

import os

import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
import kmapper as km
from kmapper import Cover

# --- Constants ---

# Global random seed for reproducibility
RANDOM_STATE = 42

# TDA Projection Parameters
TSNE_PERPLEXITY = 5  # Optimized for small-N datasets (N=18)

# Clustering Parameters (Mapper)
CLUSTER_EPS = 2.0  # Neighborhood radius for DBSCAN
CLUSTER_MIN_SAMPLES = 1  # Ensure all points are included in connectivity analysis
COVER_CUBES = 2
COVER_OVERLAP = 0.5

# Feature Columns
FEATURE_COLS = [
    'energy_score', 'win_perc', 'aggression_score',
    'cliche_score', 'complexity_score'
]

# File Paths (Relative to repository root)
INPUT_PATH = 'data/processed_fight_songs.csv'
OUTPUT_HTML = 'docs/index.html'


def main() -> None:
    """Build and export the TDA mapper graph."""
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(root_dir, INPUT_PATH)
    output_file = os.path.join(root_dir, OUTPUT_HTML)

    print(f"Loading data from {INPUT_PATH}...")
    df = pd.read_csv(input_file)

    # Prepare feature matrix
    x_data = df[FEATURE_COLS].values

    # HTML Tooltips
    tooltips = []
    for _, row in df.iterrows():
        tooltip = (
            f"<b>{row['school']}</b><br><i>{row['song_name']}</i><br><hr>"
            f"Win Rate: {row['win_perc']}<br>Aggression: {row['aggression_score']}/10"
        )
        tooltips.append(tooltip)
    tooltips = np.array(tooltips)

    print("Executing feature scaling and TDA projection...")
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x_data)

    # Initialize Lens via t-SNE (Deterministic)
    tsne = TSNE(
        n_components=2,
        perplexity=TSNE_PERPLEXITY,
        random_state=RANDOM_STATE
    )
    lens = tsne.fit_transform(x_scaled)

    # Initialize KeplerMapper
    mapper = km.KeplerMapper(verbose=1)

    print("Constructing mapper topological graph...")
    graph = mapper.map(
        lens,
        X=x_scaled,
        clusterer=DBSCAN(eps=CLUSTER_EPS, min_samples=CLUSTER_MIN_SAMPLES),
        cover=Cover(n_cubes=COVER_CUBES, perc_overlap=COVER_OVERLAP)
    )

    # Export Visualization
    print(f"Exporting interactive visualization to {OUTPUT_HTML}...")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    mapper.visualize(
        graph,
        path_html=output_file,
        title="Big Ten Fight Song Topology",
        custom_tooltips=tooltips,
        color_values=df['win_perc'],
        color_function_name="Win Percentage",
        node_color_function=["mean", "max", "min"],
        custom_meta={
            "Insight": "Yellow manifold connects programs with high energy and win rates.",
            "Dead Zones": "Isolated nodes represent generic musical structures.",
            "Methodology": "TDA Mapper using t-SNE and DBSCAN clusters."
        }
    )

    # Cleanup KeplerMapper logo/branding for a cleaner look
    with open(output_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    html_content = html_content.replace('href="http://i.imgur.com/axOG6GJ.jpg"', '')
    html_content = html_content.replace(
        '<div class="wrap-logo">',
        '<div class="wrap-logo" style="display:none;">'
    )

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    num_nodes = len(graph['nodes'])
    num_edges = sum(len(edges) for edges in graph['links'].values()) // 2
    print(f"\nFinal Graph: {num_nodes} nodes, {num_edges} edges.")


if __name__ == '__main__':
    main()
