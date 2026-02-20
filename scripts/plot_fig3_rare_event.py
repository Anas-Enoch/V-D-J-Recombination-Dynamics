# scripts/plot_fig3_rare_event.py
import os, sys
sys.path.append(os.path.dirname(__file__))
from plot_utils import save_pdf, panel_label

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("data/results_rare_event.csv").sort_values("M")

fig = plt.figure(figsize=(7.2, 3.6))
gs = fig.add_gridspec(1, 2, width_ratios=[1.15, 1.0], wspace=0.35)

# Panel A: Monte Carlo estimate vs M (will sit at 0)
ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(df["M"], df["mc_hat"], marker="o")
ax1.set_xscale("log")
ax1.set_yscale("log")  # will warn if zeros; handle by clipping
ax1.set_title("Monte Carlo estimate")
ax1.set_xlabel("Trajectories M")
ax1.set_ylabel(r"$\hat{p}_{MC}$")

# Avoid log(0) issues: show zeros as a floor
y_floor = df["cas_solver"].iloc[0] / 50.0
ax1.cla()
ax1.plot(df["M"], np.maximum(df["mc_hat"].to_numpy(), y_floor), marker="o")
ax1.axhline(df["cas_solver"].iloc[0], linestyle="--")
ax1.set_xscale("log")
ax1.set_yscale("log")
ax1.set_title("Monte Carlo vs rare-event floor")
ax1.set_xlabel("Trajectories M")
ax1.set_ylabel(r"$\hat{p}_{MC}$ (floored for log scale)")
panel_label(ax1, "A")

# Panel B: Solver CAS (constant)
ax2 = fig.add_subplot(gs[0, 1])
ax2.plot(df["M"], df["cas_solver"], marker="o")
ax2.set_xscale("log")
ax2.set_yscale("log")
ax2.set_title("Linear-solver CAS")
ax2.set_xlabel("Trajectories M (for reference)")
ax2.set_ylabel(r"$\mathrm{CAS}$")
panel_label(ax2, "B")

outpath = "figures/fig3_rare_event.pdf"
save_pdf(fig, outpath)
print(f"Saved: {os.path.abspath(outpath)}")
