# MOSEP Analysis

Analysis of LiDAR and radar point cloud data under varying weather and precipitation conditions, collected from the MOSEP (Modular Hardware and Software System for Multi-Sensor Environment Perception) measurement setup.

## Overview

This repository contains Jupyter notebooks, visualization tools, and analysis scripts to evaluate the impact of precipitation (rain, snow, hail) on LiDAR and radar sensor performance. It works with ROS2 bag files containing point cloud and weather station data, processed via the companion library [`moseplib`](packages/moseplib/).

Key capabilities:

- **Target analysis** — Statistical evaluation of reflectance targets at varying distances, split by material/color (white/grey/black) and weather conditions.
- **Noise ring analysis** — Identification and characterization of noise artifacts in point cloud data during precipitation.
- **Time series analysis** — Correlation of point cloud statistics (point count, intensity) with weather parameters (precipitation rate, type, wind).
- **3D visualization** — Interactive Plotly/Dash-based 3D point cloud exploration with selectable regions and overlay of exclusion zones.
- **Batch processing** — Parameterized notebook execution via [papermill](https://papermill.readthedocs.io/) across multiple measurement sessions.

## Installation

Requires Python ≥ 3.10 and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

This installs all dependencies including the local `moseplib` workspace package.

## Project Structure

```
├── data/
│   ├── 0external/              <- Data from third-party sources
│   ├── 1raw/                   <- Original, immutable data dumps (ROS2 bag files)
│   ├── 2interim/               <- Intermediate transformed data (parquet, pickle)
│   └── 3processed/             <- Final canonical datasets (CSV, resampled data)
├── develop/                    <- Development and test scripts
├── notebooks/
│   ├── exploratory/            <- Data exploration notebooks
│   ├── papermill/              <- Batch execution of parameterized notebooks
│   ├── target_analysis/        <- Per-bag target analysis notebooks (generated)
│   └── exported_figures/       <- Figures exported from notebooks
├── packages/
│   └── moseplib/               <- Core data processing library (workspace package)
├── presentations/              <- PowerPoint files for deliverables
├── references/                 <- Data dictionaries, manuals, papers
├── reports/
│   └── figures/                <- Figures for LaTeX reports
└── src/
    └── mosep_analysis/         <- Project-specific analysis code
        ├── data/               <- Configuration, paths, target definitions, caching
        ├── features/           <- Feature engineering (placeholder)
        ├── models/             <- Model training/prediction (placeholder)
        ├── tools/              <- Converters (LaTeX, pictures, PowerPoint)
        └── visualization/      <- Plotting: 3D point clouds, time series, Dash apps
```

## Notebooks

| Notebook | Description |
|---|---|
| `1.0_cg_target_definition_BA.ipynb` | Target definition for test site analysis |
| `1.1_cg_target_definition_ViF.ipynb` | Target definition for ViF Graz analysis |
| `1.1_cg_noise_ring_analysis.ipynb` | Analysis of noise ring artifacts |
| `1.2_cg_noise_ring_analysis.ipynb` | Extended noise ring analysis |
| `1.1_cg_model_intensity_reduction.ipynb` | Modeling of intensity reduction under precipitation |
| `target_analysis/1.1_cg_target_analysis_*.ipynb` | Per-bag target analysis (generated via papermill) |

## Configuration

Project-wide paths, target bounding boxes, and bag file mappings are defined in [`src/mosep_analysis/data/config.py`](src/mosep_analysis/data/config.py).
