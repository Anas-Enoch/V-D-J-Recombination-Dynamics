# scripts/plot_utils.py
from __future__ import annotations
from pathlib import Path
import matplotlib.pyplot as plt

def save_pdf(fig: plt.Figure, outpath: str | Path, dpi: int = 300) -> None:
    outpath = Path(outpath)
    outpath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(outpath, format="pdf", bbox_inches="tight", dpi=dpi)
    plt.close(fig)

def panel_label(ax, label: str, x: float = 0.02, y: float = 0.98) -> None:
    ax.text(
        x, y, label,
        transform=ax.transAxes,
        ha="left", va="top",
        fontsize=12, fontweight="bold"
    )
