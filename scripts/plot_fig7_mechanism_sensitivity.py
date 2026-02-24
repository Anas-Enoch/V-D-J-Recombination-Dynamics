#!/usr/bin/env python3
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# If you have your plot_utils.py (you used it for previous figures), we’ll try to use it.
# If import fails, we fall back to vanilla matplotlib.
try:
    import plot_utils  # noqa: F401
    _HAS_PLOT_UTILS = True
except Exception:
    _HAS_PLOT_UTILS = False

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]   # project root
IN_CSV = str(ROOT / "data" / "results_mechanism_sensitivity.csv")
OUT_PDF = str(ROOT / "fig6_mechanism_sensitivity.pdf")  # or fig7 if you want

def _infer_columns(df: pd.DataFrame):
    """
    Tries to infer the column names in your CSV.
    We need:
      - survival parameter (x-axis)
      - checkpoint parameter (y-axis)
      - CAS value (heat value)
    """
    cols = {c.lower(): c for c in df.columns}

    # likely names
    cas_candidates  = ["cas", "cas_value", "value", "score"]
    surv_candidates = ["survival", "survival_scale", "p_survive", "survival_mult", "surv",
                       "theta_survival", "theta_survive"]
    chk_candidates  = ["checkpoint", "checkpoint_scale", "checkpoint_mult", "chk", "qc",
                       "theta_checkpoint", "theta_chk", "theta_qc"]

    cas_col  = next((cols[c] for c in cas_candidates if c in cols), None)
    surv_col = next((cols[c] for c in surv_candidates if c in cols), None)
    chk_col  = next((cols[c] for c in chk_candidates if c in cols), None)

    if cas_col is None:
        # last resort: pick the only float-like column that isn't obviously a parameter id
        float_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
        # Prefer something named with 'cas' in it
        cas_like = [c for c in float_cols if "cas" in c.lower()]
        cas_col = cas_like[0] if cas_like else (float_cols[-1] if float_cols else None)

    if cas_col is None or surv_col is None or chk_col is None:
        raise ValueError(
            f"Could not infer columns automatically.\n"
            f"Found columns: {list(df.columns)}\n"
            f"Rename your CSV columns to: survival, checkpoint, CAS "
            f"(or edit _infer_columns() candidates)."
        )

    return surv_col, chk_col, cas_col


def main():
    if not os.path.exists(IN_CSV):
        raise FileNotFoundError(f"Missing input CSV: {IN_CSV}")

    df = pd.read_csv(IN_CSV)

    # Optional: if your generator wrote different names, this will still work if inferable.
    surv_col, chk_col, cas_col = _infer_columns(df)

    # Keep only relevant columns, drop NaNs
    df = df[[surv_col, chk_col, cas_col]].dropna()

    # Ensure numeric types
    df[surv_col] = pd.to_numeric(df[surv_col], errors="coerce")
    df[chk_col] = pd.to_numeric(df[chk_col], errors="coerce")
    df[cas_col] = pd.to_numeric(df[cas_col], errors="coerce")
    df = df.dropna()

    # Pivot to grid
    surv_vals = np.sort(df[surv_col].unique())
    chk_vals = np.sort(df[chk_col].unique())

    grid = df.pivot_table(index=chk_col, columns=surv_col, values=cas_col, aggfunc="mean")
    # Reindex in case pivot produced unsorted axes
    grid = grid.reindex(index=chk_vals, columns=surv_vals)

    # If CAS spans orders of magnitude, log10 helps readability.
    Z = grid.values.astype(float)
    # Add tiny epsilon to avoid log10(0)
    eps = 1e-300
    Zlog = np.log10(Z + eps)

    plt.figure(figsize=(7.2, 5.6))

    # imshow expects matrix; use origin='lower' so low checkpoint appears bottom.
    # extent maps matrix coords to actual parameter values.
    im = plt.imshow(
        Zlog,
        origin="lower",
        aspect="auto",
        extent=[surv_vals.min(), surv_vals.max(), chk_vals.min(), chk_vals.max()],
        interpolation="nearest",
    )

    plt.xlabel(surv_col)
    plt.ylabel(chk_col)
    plt.title("Mechanism perturbation phase diagram (log10 CAS)")
    cbar = plt.colorbar(im)
    cbar.set_label("log10(CAS)")

    # Ticks: show all if small, else a reasonable subset
    if len(surv_vals) <= 10:
        plt.xticks(surv_vals)
    if len(chk_vals) <= 10:
        plt.yticks(chk_vals)

    plt.tight_layout()
    plt.savefig(OUT_PDF)
    plt.close()

    print(f"Wrote: {OUT_PDF}")
    print(f"Used columns: {surv_col} (x), {chk_col} (y), {cas_col} (heat)")


if __name__ == "__main__":
    main()
