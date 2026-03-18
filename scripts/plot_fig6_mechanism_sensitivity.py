#!/usr/bin/env python3

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
FIG_DIR = ROOT / "figures"
FIG_DIR.mkdir(exist_ok=True)

CANDIDATE_CSVS = [
    DATA_DIR / "results_mechanism_sensitivity.csv",
    DATA_DIR / "results_mechanism_sensitivity1.csv",
]

OUT_PDF = FIG_DIR / "fig6_mechanism_sensitivity_clean.pdf"
OUT_PNG = FIG_DIR / "fig6_mechanism_sensitivity_clean.png"


def find_input_csv() -> Path:
    for p in CANDIDATE_CSVS:
        if p.exists():
            return p
    raise FileNotFoundError(
        "No mechanism sensitivity CSV found.\n"
        + "\n".join(str(p) for p in CANDIDATE_CSVS)
    )


def choose_column(df: pd.DataFrame, candidates: list[str], label: str) -> str:
    cols_lower = {c.lower(): c for c in df.columns}
    for cand in candidates:
        if cand.lower() in cols_lower:
            return cols_lower[cand.lower()]
    raise KeyError(
        f"Could not find a column for {label}.\n"
        f"Available columns: {list(df.columns)}"
    )


def build_grid(df: pd.DataFrame, x_col: str, y_col: str, z_col: str):
    x_vals = np.sort(df[x_col].dropna().unique())
    y_vals = np.sort(df[y_col].dropna().unique())
    pivot = df.pivot_table(index=y_col, columns=x_col, values=z_col, aggfunc="mean")
    pivot = pivot.reindex(index=y_vals, columns=x_vals)
    Z = pivot.to_numpy(dtype=float)
    return x_vals, y_vals, Z


def nearest_index(values: np.ndarray, target: float) -> int:
    return int(np.argmin(np.abs(values - target)))


def main():
    csv_path = find_input_csv()
    print(f"Using input CSV: {csv_path}")

    df = pd.read_csv(csv_path)

    surv_col = choose_column(
        df,
        ["theta_survival", "survival", "survival_scale", "alpha", "theta_s"],
        "survival parameter",
    )
    chk_col = choose_column(
        df,
        ["theta_checkpoint", "checkpoint", "checkpoint_scale", "beta", "theta_c"],
        "checkpoint parameter",
    )
    cas_col = choose_column(
        df,
        ["CAS", "cas", "cas_value"],
        "CAS",
    )

    df = df[[surv_col, chk_col, cas_col]].copy()
    df[surv_col] = pd.to_numeric(df[surv_col], errors="coerce")
    df[chk_col] = pd.to_numeric(df[chk_col], errors="coerce")
    df[cas_col] = pd.to_numeric(df[cas_col], errors="coerce")
    df = df.dropna()

    theta_s, theta_c, CAS_grid = build_grid(df, surv_col, chk_col, cas_col)

    if np.isnan(CAS_grid).any():
        raise ValueError(
            "CAS grid contains NaNs after pivoting. "
            "Your CSV is missing some parameter combinations."
        )

    eps = 1e-20
    log_CAS = np.log10(CAS_grid + eps)

    T_c, T_s = np.meshgrid(theta_c, theta_s)

    # Raw additive residual
    i_ref = nearest_index(theta_s, 1.0)
    j_ref = nearest_index(theta_c, 1.0)

    CAS_s_only = CAS_grid[:, j_ref]
    CAS_c_only = CAS_grid[i_ref, :]
    CAS_ref = CAS_grid[i_ref, j_ref]

    CAS_additive = CAS_s_only[:, None] + CAS_c_only[None, :] - CAS_ref
    delta = CAS_grid - CAS_additive

    delta_max = np.max(np.abs(delta))
    if delta_max == 0:
        delta_max = 1e-12

    fig, axes = plt.subplots(1, 2, figsize=(12, 5.2))

    # Panel A
    im1 = axes[0].pcolormesh(
        T_c,
        T_s,
        log_CAS,
        shading="gouraud",
        cmap="viridis",
    )
    contours1 = axes[0].contour(
        T_c,
        T_s,
        log_CAS,
        levels=10,
        colors="black",
        linewidths=0.5,
        alpha=0.6,
    )
    axes[0].clabel(contours1, inline=True, fontsize=7)
    axes[0].set_title("A. log10(CAS)")
    axes[0].set_xlabel(r"Checkpoint scaling $\theta_{\mathrm{checkpoint}}$")
    axes[0].set_ylabel(r"Survival scaling $\theta_{\mathrm{survival}}$")
    cbar1 = fig.colorbar(im1, ax=axes[0])
    cbar1.set_label(r"$\log_{10}(\mathrm{CAS})$")

    # Panel B
    im2 = axes[1].pcolormesh(
        T_c,
        T_s,
        delta,
        shading="gouraud",
        cmap="coolwarm",
        vmin=-delta_max,
        vmax=delta_max,
    )
    contours2 = axes[1].contour(
        T_c,
        T_s,
        delta,
        levels=10,
        colors="black",
        linewidths=0.5,
        alpha=0.6,
    )
    axes[1].clabel(contours2, inline=True, fontsize=7)
    axes[1].set_title(r"B. Raw interaction residual $\Delta$")
    axes[1].set_xlabel(r"Checkpoint scaling $\theta_{\mathrm{checkpoint}}$")
    axes[1].set_ylabel(r"Survival scaling $\theta_{\mathrm{survival}}$")
    cbar2 = fig.colorbar(im2, ax=axes[1])
    cbar2.set_label(r"$\Delta$")

    plt.tight_layout()
    plt.savefig(OUT_PDF, dpi=300, bbox_inches="tight")
    plt.savefig(OUT_PNG, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Wrote: {OUT_PDF}")
    print(f"Wrote: {OUT_PNG}")
    print(
        f"Reference point used for additive baseline: "
        f"theta_survival={theta_s[i_ref]:.3f}, theta_checkpoint={theta_c[j_ref]:.3f}"
    )


if __name__ == "__main__":
    main()
