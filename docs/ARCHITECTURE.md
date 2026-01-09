# Project Architecture

This system implements a centralized pipeline for the exploratory topological analysis of fight song data, generating interactive visualizations and statistical reports for the Bucky's Data Viz Challenge submission.

## Glossary

- **Cluster:** A group of connected schools in the topological graph exhibiting similar song characteristics and performance metrics.
- **Performance Cluster:** A connected region of schools exhibiting high performance metrics and similar song features.
- **Outlier Nodes:** Isolated regions in the mapper graph associated with significantly different win rates or musical metrics.
- **Mapper Graph:** A network representation used to visualize the topological relationships of high-dimensional data.

## System Design

```
DataViz/
├── src/           # Analytical logic and visualization enhancement
├── data/          # Raw and processed datasets
├── docs/          # Static reports and interactive output
├── scripts/       # Pipeline orchestration
└── requirements.txt
```

## Data Flow

1. **Input:** FiveThirtyEight dataset (`fight-songs.csv`) and historical conference records.
2. **Preprocessing:** `preprocess.py` engineers features (Energy, Aggression, Cliche, Complexity) on a standardized 1-10 scale.
3. **Topological Mapping:** `visualize.py` applies dimensionality reduction (t-SNE) and constructs a mapper graph (DBSCAN) using KeplerMapper.
4. **Enhancement:** `enhance_visualization.py` injects institutional branding and contextual headers for the contest submission.
5. **Output:** Standalone HTML (`docs/index.html`) optimized for static deployment.

## Technical Stack

- **Core:** Python (Data Processing)
- **TDA:** KeplerMapper, scikit-learn
- **Visualization:** HTML/JS (KeplerMapper Standalone)
- **Deployment:** Static Hosting (GitHub Pages optimized)

## Design Constraints

- **Static Output:** Prioritizes reproducibility and simplified submission review via standalone HTML.
- **Mathematical Engineering:** Features derive from raw data via deterministic, documented transformations.
- **Reproducibility:** Fixed random seeds ensure identical results across different evaluation environments.
