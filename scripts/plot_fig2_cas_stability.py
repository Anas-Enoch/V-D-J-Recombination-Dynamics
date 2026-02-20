# scripts/plot_fig2_cas_stability.py
from __future__ import annotations
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from plot_utils import save_pdf, panel_label

def main():
    df = pd.read_csv("data/results_cas_stability.csv")
    # Ensure sorted
    df = df.sort_values(["sample_id", "Lmax"])

    fig, ax = plt.subplots(figsize=(3.4, 2.4))

    # Plot a handful of samples (or all if small)
    sample_ids = df["sample_id"].unique()
    # If too many, subsample deterministically
    max_curves = 8
    if len(sample_ids) > max_curves:
        sample_ids = sample_ids[:max_curves]

    for sid in sample_ids:
        d = df[df["sample_id"] == sid]
        ax.plot(d["Lmax"], d["CAS"], marker="o", label=str(sid))

    ax.set_xlabel(r"Insertion bound $L_{\max}$")
    ax.set_ylabel(r"Clonal Attractor Score (CAS)")
    ax.set_yscale("log")  # almost always needed
    ax.grid(True, which="both", linewidth=0.3, alpha=0.4)

    # Optional legend if not too crowded
    if len(sample_ids) <= 6:
        ax.legend(frameon=False, ncol=2)

    panel_label(ax, "A")

    # Inset: |CAS_{L+1} - CAS_L|
    ax_in = ax.inset_axes([0.58, 0.12, 0.38, 0.38])
    diffs = []
    for sid in sample_ids:
        d = df[df["sample_id"] == sid].sort_values("Lmax")
        cas = d["CAS"].to_numpy()
        lmax = d["Lmax"].to_numpy()
        if len(cas) >= 2:
            diffs.append(pd.DataFrame({
                "sample_id": sid,
                "Lmax_mid": lmax[1:],
                "dCAS": np.abs(cas[1:] - cas[:-1]),
            }))
    if diffs:
        dd = pd.concat(diffs, ignore_index=True)
        # Plot median change per L step
        med = dd.groupby("Lmax_mid")["dCAS"].median().reset_index()
        ax_in.plot(med["Lmax_mid"], med["dCAS"], marker="o")
        ax_in.set_yscale("log")
        ax_in.set_title(r"$|\mathrm{CAS}_{L+1}-\mathrm{CAS}_L|$", pad=2)
        ax_in.set_xticks(sorted(med["Lmax_mid"].unique()))
        ax_in.grid(True, which="both", linewidth=0.3, alpha=0.4)

    save_pdf(fig, "figures/Fig2_CAS_vs_Lmax.pdf")

if __name__ == "__main__":
    main()
