import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INP = os.path.join(ROOT, "data", "results_cohort_cas.csv")
OUT = os.path.join(ROOT, "figures", "fig4_cohort_cas_distribution.pdf")

def panel_label(ax, label):
    ax.text(
        0.01, 0.98, label,
        transform=ax.transAxes,
        va="top", ha="left",
        fontsize=12, fontweight="bold"
    )

def save_pdf(fig, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)

df = pd.read_csv(INP)

# enforce order + clean labels
order = ["pSS_no_lymphoma", "pSS_MALT"]
label_map = {
    "pSS_no_lymphoma": "pSS (no lymphoma)",
    "pSS_MALT": "pSS + MALT",
}
df = df[df["group"].isin(order)].copy()
df["group"] = pd.Categorical(df["group"], categories=order, ordered=True)

# basic sanity
if df.empty:
    raise ValueError("results_cohort_cas.csv is empty or groups are mislabeled.")

groups = [df[df["group"] == g]["CAS"].to_numpy() for g in order]

fig, ax = plt.subplots(figsize=(6.2, 4.2))

# Boxplot
bp = ax.boxplot(
    groups,
    labels=[label_map[g] for g in order],
    showfliers=False,
    widths=0.55,
)

# Overlay points with jitter
rng = np.random.default_rng(0)
for i, g in enumerate(order, start=1):
    y = df[df["group"] == g]["CAS"].to_numpy()
    x = i + rng.normal(0, 0.06, size=len(y))
    ax.scatter(x, y, s=22, alpha=0.85)

ax.set_yscale("log")
ax.set_ylabel("Clonal Attractor Score (CAS)")
ax.set_title("Cohort distribution of CAS")
ax.grid(True, which="both", axis="y", alpha=0.25)

panel_label(ax, "A")

save_pdf(fig, OUT)
print(f"Saved: {OUT}")
