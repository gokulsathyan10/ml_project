# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .   # installs the src package as editable
```

The project is packaged via `setup.py` and installed as `mlproject`. The `-e .` line in `requirements.txt` is currently commented out; uncomment it to auto-install on `pip install -r`.

## Running the Training Pipeline

```bash
python src/components/model_trainer.py
```

This triggers the full pipeline (ingestion → transformation → training) via the `__main__` block at the bottom of `model_trainer.py`. Outputs land in `artifacts/`.

## Architecture

The pipeline is composed of three sequential components in `src/components/`:

1. **`data_ingestion.py`** — Reads `notebooks/data/stud.csv`, splits into train/test (80/20), and writes `artifacts/data.csv`, `artifacts/train.csv`, `artifacts/test.csv`. Supports CSV, Parquet, Excel, and JSON inputs via `_load_dataframe`.

2. **`data_transformation.py`** — Builds a `sklearn` `ColumnTransformer` with separate pipelines for numerical (`writing_score`, `reading_score`) and categorical features. Saves the fitted preprocessor to `artifacts/proprocessor.pkl` (note the typo in the filename).

3. **`model_trainer.py`** — Runs `GridSearchCV` across 7 regressors (Linear Regression, Decision Tree, Random Forest, Gradient Boosting, XGBoost, CatBoost, AdaBoost). Picks the best by test R², requires R² ≥ 0.6, and saves the winning model to `artifacts/model.pkl`.

**Target variable**: `math_score`

**Cross-cutting utilities** in `src/`:
- `utils.py` — `save_object` / `load_object` (pickle), `evaluate_models` (GridSearchCV loop returning test R² per model)
- `logger.py` — Configures `logging` to write timestamped `.log` files under `logs/<timestamp>/`
- `exception.py` — `CustomException` wraps any exception with script name and line number

`src/pipeline/train_pipeline.py` and `predict_pipeline.py` exist but are currently empty stubs.

## Artifacts

All generated files go to `artifacts/` (git-ignored):
- `data.csv` — raw copy of input
- `train.csv` / `test.csv` — split data
- `proprocessor.pkl` — fitted sklearn preprocessor (typo in name is intentional per existing code)
- `model.pkl` — best trained model

## Notebooks

- `notebooks/EDA.ipynb` — exploratory data analysis on `stud.csv`
- `notebooks/Model_Train.ipynb` — model training experiments
