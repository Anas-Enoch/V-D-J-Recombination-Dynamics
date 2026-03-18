# V(D)J Recombination Dynamics  
## VDJ-KTS and Clonal Attractor Susceptibility (CAS)

**Author:** Anas Enoch, MD  
**Affiliation:** Mohammed VI University of Health Sciences (UM6SS), Casablanca, Morocco  

---
# V-D-J-Recombination-Dynamics

This repository contains the computational assets used for a bounded stochastic analysis of V(D)J recombination dynamics, including data tables, plotting scripts, and figure-generation workflows for Clonal Attractor Score (CAS) analyses.

## Overview

The repository supports a finite-state stochastic modeling workflow for studying recombination dynamics under bounded insertion complexity and biologically interpretable perturbations. The main outputs are:

- CAS stability analyses across insertion bounds
- rare-event benchmarking versus Monte Carlo
- anchored cohort-level CAS comparisons
- ROC comparisons against classical clonality metrics
- mechanism sensitivity analyses under survival/checkpoint perturbation

## Repository structure

### `data/`
CSV tables used to generate manuscript figures.

Main files:
- `results_cas_stability.csv`
- `results_cohort_cas.csv`
- `results_mechanism_sensitivity.csv`
- `results_rare_event.csv`
- `results_roc.csv`

Notes:
- `results_mechanism_sensitivity.csv` is the canonical mechanism-sensitivity dataset.
- older duplicate files such as `results_mechanism_sensitivity1.csv` should not be used for final analyses.

### `figures/`
Generated manuscript figures.

Main files:
- `fig2_cas_stability.pdf`
- `fig3_rare_event.pdf`
- `fig4_cohort_cas_distribution.pdf`
- `fig5_roc_comparison.pdf`
- `fig6_mechanism_sensitivity_clean.png`
- optional PDF counterpart if exported

Notes:
- `fig6_mechanism_sensitivity_clean.*` is the current final mechanism-perturbation figure.
- older versions of Figure 6 should not be used in the final manuscript.

### `scripts/`
Python scripts used to generate CSVs and figures.

#### Figure-generation scripts
- `plot_fig2_cas_stability.py`
- `plot_fig3_rare_event.py`
- `plot_fig4_cohort_cas_distribution.py`
- `plot_fig5_roc_comparison.py`
- `plot_fig6_mechanism_sensitivity.py`
- `plot_fig7_mechanism_sensitivity.py` (legacy / optional)
- `plot_utils.py`

#### Data-generation scripts
- `make_results_cas_stability_csv.py`
- `make_results_cohort_cas_csv.py`
- `make_results_mechanism_sensitivity_csv.py`
- `make_results_rare_event_csv.py`
- `make_results_roc_csv.py`

Notes:
- `make_results_mechanism_sensitivity_csv.py` is the preferred script for the final mechanism-sensitivity dataset.
- obsolete or broken experimental scripts should be removed or clearly marked before publication.

## Final mechanism-sensitivity workflow

### 1. Generate the mechanism-sensitivity CSV
```bash
python scripts/make_results_mechanism_sensitivity_csv.py