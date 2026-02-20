import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# so "from plot_utils import ..." works when script is run from repo root
sys.path.append(os.path.join(os.path.dirname(__file__)))

from plot_utils import save_pdf, panel_label


def auc_trapz(fpr, tpr):
    """AUC by trapezoidal rule (NumPy 2.x compatible)."""
    fpr = np.asarray(fpr, dtype=float)
    tpr = np.asarray(tpr, dtype=float)

    # sort by FPR to ensure proper integration and clean curve
    order = np.argsort(fpr)
    fpr_s = fpr[order]
    tpr_s = tpr[order]

    return float(np.trapezoid(tpr_s, fpr_s))


def main():
    in_csv = os.path.join("data", "results_roc.csv")
    if not os.path.exists(in_csv):
        raise FileNotFoundError(f"Missing input CSV: {in_csv}")

    df = pd.read_csv(in_csv)

    required = {"fpr", "tpr_A", "tpr_B"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"results_roc.csv missing columns: {sorted(missing)}")

    fpr = df["fpr"].to_numpy(dtype=float)
    tprA = df["tpr_A"].to_numpy(dtype=float)
    tprB = df["tpr_B"].to_numpy(dtype=float)

    # sort once for plotting + AUC
    order = np.argsort(fpr)
    fpr = fpr[order]
    tprA = tprA[order]
    tprB = tprB[order]

    aucA = auc_trapz(fpr, tprA)
    aucB = auc_trapz(fpr, tprB)

    fig, ax = plt.subplots(figsize=(6.2, 4.8))

    ax.plot(fpr, tprA, linewidth=2.0, label=f"Model A (clonality only), AUC={aucA:.3f}")
    ax.plot(fpr, tprB, linewidth=2.0, label=f"Model B (+CAS), AUC={aucB:.3f}")

    # chance line
    ax.plot([0, 1], [0, 1], linestyle="--", linewidth=1.5, label="Chance")

    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC: clonality-only vs +CAS")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.legend(frameon=False, loc="lower right")
    panel_label(ax, "A")

    os.makedirs("figures", exist_ok=True)
    out = os.path.join("figures", "fig5_roc_comparison.pdf")
    save_pdf(fig, out)
    print(f"Saved: {os.path.abspath(out)}")


if __name__ == "__main__":
    main()
