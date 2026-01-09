# Big Ten Fight Song Topological Analysis

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg?logo=python&logoColor=white)
![TDA](https://img.shields.io/badge/TDA-KeplerMapper-red)
![Computing](https://img.shields.io/badge/SciPy-Ecosystem-blue?logo=scipy&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Event](https://img.shields.io/badge/Submission-Bucky's%20Data%20Viz%20Challenge%202026-FFD700)

**Big Ten Fight Song Topological Analysis** utilizes topological data analysis (TDA) to explore structural patterns in collegiate fight songs. This project was developed for Bucky's Data Viz Challenge to investigate potential relationships between musical characteristics and historical athletic success in an exploratory context. This project integrates the [FiveThirtyEight Fight Song Dataset](https://github.com/fivethirtyeight/data/tree/master/fight-songs) with all-time Big Ten Conference records from [Wikipedia](https://en.wikipedia.org/wiki/Big_Ten_Conference#All-time_school_records).

## How It Works

1. **Preprocessing**: The pipeline maps 18 schools (including 2024 expansions) to 5 engineered musical features: *Energy, Aggression, Cliche, and Complexity*.
2. **Topological Mapping**: High-dimensional features are projected via t-SNE and clustered using DBSCAN via **KeplerMapper** to identify topological manifolds.
3. **Statistical Validation**: A Pearson correlation suite with bootstrap confidence intervals validates the structural findings against historical win percentages.
4. **Visualization**: An interactive HTML network graph surfaces the relationship between song features and team success tiers.

## Quick Start

```bash
# Setup environment
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Execute full pipeline (Preprocessing → Visualization → Analysis)
bash scripts/run_full_pipeline.sh

# View the interactive result
open docs/index.html
```

## Performance & Impact

- **Analytical Insight**: Complexity (song duration) demonstrated a statistically significant moderate positive correlation ($p=0.048$) within this specific sample size (N=18).
- **Topological Clusters**: Identified a performance-related cluster where high-energy programs group in topological space.
- **Reproducibility**: All random seeds are fixed (`random_state=42`) for deterministic results across varying environments.

## Documentation

- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** — Core algorithms, data flow, and system design decisions.
- **[FINDINGS.md](docs/FINDINGS.md)** — Complete statistical report and topological interpretation.
- **[TESTING.md](docs/TESTING.md)** — Testing strategy, execution guides, and regression scenarios.
- **[STYLE.md](docs/STYLE.md)** — Architectural invariants, coding standards, and audit checklists.

## License

See **[LICENSE](LICENSE)** file for details.
