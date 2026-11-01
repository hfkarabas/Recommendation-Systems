# Recommendation Systems Algorithms Project (Öneri Algoritmaları Projesi)

A comprehensive term project for developing, evaluating, and comparing recommendation system algorithms on the MovieLens 32M benchmark dataset.

## Directory Structure

```
C:\OneriAlgoritmalariProjesi
├── .venv/                         # Dedicated Python virtual environment
├── notebooks/                     # Jupyter notebooks for development & evaluation
│   └── 00_environment_check.ipynb # Environment and dataset accessibility validation
├── src/                           # Source code (modular recommendation algorithms & utilities)
├── scripts/                       # Automation and utility scripts
│   └── verify_dataset.py          # Read-only MovieLens 32M integrity verification script
├── results/                       # Evaluation benchmarks, figures, and exported metrics
├── documentation/                 # Technical documentation, reports, and methodology
├── config.yaml                    # Global project configuration & external dataset paths
├── requirements.txt               # Pinned project dependencies
├── .gitignore                     # Git exclusion rules
└── README.md                      # Project overview and documentation
```

## Dataset

This project uses the official **MovieLens 32M** dataset, maintained outside the repository at:
```
C:\ml-32m
```
The dataset directory contains:
- `ratings.csv` (32,000,204 ratings)
- `movies.csv` (87,585 movies)
- `tags.csv` (2,000,072 tag applications)
- `links.csv` (IMDb and TMDb identifiers)

## Environment Setup

1. **Virtual Environment:** `.venv` is located at `C:\OneriAlgoritmalariProjesi\.venv`
2. **Jupyter Kernel:** Registered as `Recommendation Systems - Project` (`recommendation-systems-project`)
3. **Dependencies:** Install dependencies via:
   ```bash
   .\.venv\Scripts\pip install -r requirements.txt
   ```
