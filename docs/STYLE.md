# Coding & Style Standards (Audit Guide)

This document outlines the coding conventions, stylistic choices, and architectural rules for the Big Ten Fight Song TDA project.

## 1. Architectural Integrity

* **Deterministic Preprocessing**: All feature engineering MUST use fixed random seeds (`random_state=42`) to ensure reproducibility of the topological mapper.
* **Data Immutability**: The `data/fight-songs.csv` file is treated as a read-only source. All modifications must be written to `data/processed_*.csv`.
* **Separation of Concerns**: Data ingestion and cleaning (`preprocess.py`) are strictly separated from visualization logic (`visualize.py`) and statistical validation (`statistical_validation.py`).

## 2. Python Standards (PEP 8+)

* **Type Annotations**: All function signatures must include type hints for parameters and return values.
* **Docstrings**: Use Google-style docstrings for all public functions to explain purpose, arguments, and return types.
* **Asynchronous Logic**: Use `subprocess` or `asyncio` only when necessary for pipeline orchestration; otherwise, prioritize synchronous, readable data flows.
* **Error Handling**: Implement specific exceptions for data validation (e.g., `ValueError` for missing win percentages) rather than catching generic exceptions.

### Stylistic Guidelines
* **Indentation**: 4 spaces per indentation level.
* **Variable Naming**: `snake_case` for variables and functions, `PascalCase` for classes, `UPPER_SNAKE_CASE` for global constants.
* **Line Length**: Max 88 characters (Black standard).

## 3. Data Flow & Reproducibility

* **Artifact Localization**: All generated plots MUST be saved to `docs/images/`. Statistical artifacts (CSV) must be saved to `data/`.
* **Fixed Seeds**: Every step involving stochastic processing (t-SNE in KeplerMapper, bootstrapping in statistical validation) must use the project-standard seed of `42`.

## 4. Testing Conventions

* **Framework**: `pytest`.
* **Isolation**: Tests must not modify the `data/` directory. Use temporary directories or mocks for file I/O where possible.
* **Focus**: Prioritize testing the deterministic feature engineering over visual check-ins of the mapper logic.

## 5. Audit Checklist

When reviewing the codebase, ensure the following are met:
1. Missing `random_state=42` in any stochastic function call.
2. Hardcoded absolute paths (all paths MUST be relative to the repository root).
3. Missing JSDoc-style docstrings or type hints on new functions.
4. Redundant horizontal rules or non-ASCII characters in documentation.
5. "Magic strings" in column mapping that should be defined as constants.
