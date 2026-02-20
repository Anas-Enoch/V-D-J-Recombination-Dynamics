# V(D)J Recombination Dynamics  
## VDJ-KTS and Clonal Attractor Susceptibility (CAS)

**Author:** Anas Enoch, MD  
**Affiliation:** Mohammed VI University of Health Sciences (UM6SS), Casablanca, Morocco  

---

## Overview

This repository contains the computational framework accompanying:

**VDJ-KTS: A Formal and Probabilistic Framework for Verifying V(D)J Recombination Dynamics and Clonal Attractor Susceptibility (CAS).**

VDJ-KTS models V(D)J recombination as a bounded finite-state Markov system and defines the Clonal Attractor Score (CAS) as an operator-level reachability functional:

CAS(s₀) = ⟨ δₛ₀ , (−Q_TT)⁻¹ Q_TA 1 ⟩

The framework enables:

- Exact reachability computation (no Monte Carlo bias)
- Stability analysis under junctional complexity bounds
- Sensitivity analysis under structured generator perturbations
- Evaluation of non-additive biological mechanism interactions

---

## Repository Structure
scripts/      # Python scripts for CSV generation and figure plotting
data/         # Structured CSV inputs
figures/      # Submission-ready PDF figures
paper/        # Manuscript PDF (optional)

---

## Environment Setup

Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install numpy pandas matplotlib scikit-learn

Reproducing Figures

Run CSV generators:
python scripts/make_results_cas_stability_csv.py
python scripts/make_results_rare_event_csv.py
python scripts/make_results_cohort_cas_csv.py
python scripts/make_results_roc_csv.py
python scripts/make_results_mechanism_sensitivity_csv.py

Then generate figures:
python scripts/plot_fig2_cas_stability.py
python scripts/plot_fig3_rare_event.py
python scripts/plot_fig4_cohort_cas_distribution.py
python scripts/plot_fig5_roc_comparison.py
python scripts/plot_fig6_mechanism_sensitivity.py