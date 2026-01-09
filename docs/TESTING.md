# Testing Guidelines

## Strategy

This project utilizes **pytest** for deterministic verification of the analytical pipeline. Our testing philosophy prioritizes **Reproducibility and Data Integrity**.

Given the stochastic nature of topological data analysis, we do not write tests for visual layout metrics. Instead, we focus strictly on the deterministic preprocessing algorithms and the statistical validation methods that underpin the final report.

### Test Types
* **Unit Tests (`tests/test_preprocess.py`)**: Validates feature normalization and Big Ten realignment logic.
* **Statistical Tests (`tests/test_statistical_validation.py`)**: Verifies correctness of bootstrap, permutation, and effect size calculations.
* **Regression Suite**: Validates that pipeline updates preserve analytical integrity and artifact localization.

## Running Tests

### Automated Suite
Run the full suite using the project virtual environment:
```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run with coverage report
pytest --cov=src --cov-report=term-missing
```

## Core Regression Scenarios

All changes to the `src/` logic must pass the following core verification points:

| ID | Scenario | Purpose |
|---|---|---|
| **RT001** | Feature Normalization | Verifies that all features are scaled strictly between 1.0 and 10.0. |
| **RT002** | Conference Expansion | Verifies that USC, UCLA, Oregon, and Washington are correctly mapped to 'Big Ten'. |
| **RT003** | Deterministic Mapping | Verifies that the mapper graph produces the same node count across identical runs (Seed 42). |
| **RT004** | Statistical Integrity | Verifies that the Pearson correlation coefficient matches known benchmarks for the baseline dataset. |
| **RT005** | Image Localization | Verifies that all plots are generated in `docs/images/` without manual path creation. |

## Writing New Tests
* **No Network Dependency**: Tests must be isolated and rely only on local files in the `data/` directory.
* **Deterministic Seeds**: Use `random_state=42` in all stochastic mocks to maintain reproducibility.
* **Environment Isolation**: Tests must rely strictly on `data/` artifacts; never attempt network I/O or external API calls.
* **Coverage Expectation**: Aim for >90% coverage on `src/` logic to ensure analytical robustness.
