import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from plot_utils import save_pdf, panel_label


def main():

    df = pd.read_csv("data/results_mechanism_sensitivity.csv")

    alphas = np.sort(df["alpha"].unique())
    betas  = np.sort(df["beta"].unique())

    A, B = np.meshgrid(alphas, betas, indexing="ij")

    CAS = np.zeros_like(A)

    for i, a in enumerate(alphas):
        for j, b in enumerate(betas):
            CAS[i, j] = df[(df.alpha == a) & (df.beta == b)]["CAS"].values[0]

    # ---- Non-additivity residual ----
    base = df[(df.alpha == 1.0) & (df.beta == 1.0)]["CAS"].values[0]

    residual = np.zeros_like(CAS)

    for i, a in enumerate(alphas):
        for j, b in enumerate(betas):
            cas_ab = CAS[i, j]
            cas_a0 = df[(df.alpha == a) & (df.beta == 1.0)]["CAS"].values[0]
            cas_0b = df[(df.alpha == 1.0) & (df.beta == b)]["CAS"].values[0]
            residual[i, j] = cas_ab - cas_a0 - cas_0b + base

    # ---- Plot ----
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))

    # Panel A — CAS heatmap
    im0 = axes[0].imshow(
        CAS,
        origin="lower",
        aspect="auto",
        extent=[betas.min(), betas.max(), alphas.min(), alphas.max()]
    )
    axes[0].set_xlabel("Checkpoint scaling (β)")
    axes[0].set_ylabel("Survival scaling (α)")
    axes[0].set_title("CAS(α, β)")
    fig.colorbar(im0, ax=axes[0])
    panel_label(axes[0], "A")

    # Panel B — Interaction residual
    im1 = axes[1].imshow(
        residual,
        origin="lower",
        aspect="auto",
        extent=[betas.min(), betas.max(), alphas.min(), alphas.max()]
    )
    axes[1].set_xlabel("Checkpoint scaling (β)")
    axes[1].set_ylabel("Survival scaling (α)")
    axes[1].set_title("Non-additivity residual Δ")
    fig.colorbar(im1, ax=axes[1])
    panel_label(axes[1], "B")

    save_pdf(fig, "figures/fig6_mechanism_sensitivity.pdf")
    print("Saved: figures/fig6_mechanism_sensitivity.pdf")


if __name__ == "__main__":
    main()
