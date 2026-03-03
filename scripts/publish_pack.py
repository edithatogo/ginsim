from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json

import numpy as np
import pandas as pd

def _latest_run_dir(full_uncertainty_dir: Path, prefix: str) -> Optional[Path]:
    if not full_uncertainty_dir.exists():
        return None
    cands = [p for p in full_uncertainty_dir.iterdir() if p.is_dir() and p.name.startswith(prefix)]
    if not cands:
        return None
    cands.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return cands[0]

def _load_draws_summary(run_dir: Path) -> pd.DataFrame:
    draws_path = run_dir / "full_uncertainty_draws.csv"
    if not draws_path.exists():
        raise FileNotFoundError(draws_path)
    df = pd.read_csv(draws_path)
    # required columns: policy, nb, net_qalys, avg_premium
    for col in ["policy", "nb"]:
        if col not in df.columns:
            raise ValueError(f"Expected column '{col}' in {draws_path}")
    # fill missing optional cols
    if "net_qalys" not in df.columns:
        df["net_qalys"] = np.nan
    if "avg_premium" not in df.columns:
        df["avg_premium"] = np.nan

    def q(x, p): 
        return float(np.quantile(x.dropna(), p)) if x.dropna().shape[0] else np.nan

    out = (
        df.groupby("policy")
          .agg(
              nb_mean=("nb","mean"),
              nb_p05=("nb", lambda x: q(x, 0.05)),
              nb_p95=("nb", lambda x: q(x, 0.95)),
              qaly_mean=("net_qalys","mean"),
              qaly_p05=("net_qalys", lambda x: q(x, 0.05)),
              qaly_p95=("net_qalys", lambda x: q(x, 0.95)),
              prem_mean=("avg_premium","mean"),
              prem_p05=("avg_premium", lambda x: q(x, 0.05)),
              prem_p95=("avg_premium", lambda x: q(x, 0.95)),
          )
          .reset_index()
          .sort_values("nb_mean", ascending=False)
    )
    return out

def _maybe_load_manifest(run_dir: Path) -> Dict:
    p = run_dir / "run_manifest.json"
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {}

def _compute_uncertainty_tables(run_dir: Path, seed: int = 20260302) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Compute EVPPI by group and (S1, ST) tables if theta matrices exist."""
    try:
        import jax
        import jax.numpy as jnp
        from src.model.evppi_rff import evppi_rff
        from src.model.voi import evpi
        from src.model.sensitivity import sobol_first_order_rff
        from src.model.sensitivity_total import total_order_sobol_rff
    except Exception:
        # If JAX not installed in environment running publish_pack, skip.
        return (pd.DataFrame(columns=["group","evppi"]), pd.DataFrame(columns=["group","S1_optimal_NB","ST_optimal_NB"]))

    nb_path = run_dir / "net_benefit_matrix.npy"
    if not nb_path.exists():
        return (pd.DataFrame(columns=["group","evppi"]), pd.DataFrame(columns=["group","S1_optimal_NB","ST_optimal_NB"]))

    nb = np.load(nb_path)
    nb_j = jnp.array(nb)
    nb_opt = jnp.max(nb_j, axis=1)

    groups = ["mapping","behavior","clinical","insurance","passthrough","data_quality"]
    theta = {}
    for g in groups:
        p = run_dir / f"theta_{g}.npy"
        if p.exists():
            theta[g] = jnp.array(np.load(p))

    key = jax.random.PRNGKey(seed)

    # EVPPI by group
    evpi_val = float(evpi(nb_j))
    evppi_rows = []
    for g, th in theta.items():
        k = jax.random.fold_in(key, hash(g) & 0xFFFFFFFF)
        v = float(evppi_rff(nb_j, th, k, n_features=256, lengthscale=1.0, l2=1e-2))
        evppi_rows.append({"group": g, "evppi": v})
    evppi_df = pd.DataFrame(evppi_rows).sort_values("evppi", ascending=False) if evppi_rows else pd.DataFrame(columns=["group","evppi"])
    evppi_df["evpi"] = evpi_val

    # S1 + ST for decision output (optimal NB) and avg policy NB
    def _concat_complement(exclude: str):
        mats = []
        for gg, mat in theta.items():
            if gg == exclude:
                continue
            mats.append(mat)
        if not mats:
            return None
        return jnp.concatenate(mats, axis=1)

    decomp_rows = []
    for g, th in theta.items():
        comp = _concat_complement(g)
        if comp is None:
            continue
        k1 = jax.random.fold_in(key, (hash(g) + 1) & 0xFFFFFFFF)
        s1_opt = float(sobol_first_order_rff(nb_opt, th, k1))
        k2 = jax.random.fold_in(key, (hash(g) + 2) & 0xFFFFFFFF)
        st_opt = float(total_order_sobol_rff(nb_opt, comp, k2))

        k3 = jax.random.fold_in(key, (hash(g) + 3) & 0xFFFFFFFF)
        s1_pol = sobol_first_order_rff(nb_j, th, k3)
        s1_avg = float(jnp.mean(s1_pol))

        k4 = jax.random.fold_in(key, (hash(g) + 4) & 0xFFFFFFFF)
        st_pol = total_order_sobol_rff(nb_j, comp, k4)
        st_avg = float(jnp.mean(st_pol))

        decomp_rows.append({
            "group": g,
            "S1_optimal_NB": s1_opt,
            "ST_optimal_NB": st_opt,
            "S1_avg_policy_NB": s1_avg,
            "ST_avg_policy_NB": st_avg,
        })

    decomp_df = pd.DataFrame(decomp_rows).sort_values("ST_optimal_NB", ascending=False) if decomp_rows else pd.DataFrame(columns=["group","S1_optimal_NB","ST_optimal_NB","S1_avg_policy_NB","ST_avg_policy_NB"])
    return evppi_df, decomp_df

def _plot_policy_bars(df: pd.DataFrame, out_png: Path, title: str, metric: str = "nb_mean"):
    try:
        import matplotlib.pyplot as plt
    except Exception:
        return

    # Sort
    df = df.sort_values(metric, ascending=False)
    x = np.arange(df.shape[0])
    y = df[metric].values
    yerr = None
    if metric == "nb_mean" and {"nb_p05","nb_p95"}.issubset(df.columns):
        yerr = np.vstack([y - df["nb_p05"].values, df["nb_p95"].values - y])

    plt.figure(figsize=(10, 5))
    if yerr is None:
        plt.bar(x, y)
    else:
        plt.bar(x, y, yerr=yerr, capsize=4)
    plt.xticks(x, df["policy"].values, rotation=30, ha="right")
    plt.title(title)
    plt.tight_layout()
    out_png.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_png, dpi=200)
    plt.close()

def _plot_evppi(evppi_df: pd.DataFrame, out_png: Path, title: str):
    try:
        import matplotlib.pyplot as plt
    except Exception:
        return
    if evppi_df.empty:
        return
    df = evppi_df.sort_values("evppi", ascending=False)
    x = np.arange(df.shape[0])
    y = df["evppi"].values

    plt.figure(figsize=(8, 4))
    plt.bar(x, y)
    plt.xticks(x, df["group"].values, rotation=30, ha="right")
    plt.title(title)
    plt.tight_layout()
    out_png.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_png, dpi=200)
    plt.close()

def _write_docx(out_docx: Path, title: str, sections: List[Tuple[str, str]], tables: List[Tuple[str, pd.DataFrame]], figures: List[Tuple[str, Path]]):
    try:
        from docx import Document
        from docx.shared import Inches
    except Exception:
        return

    doc = Document()
    doc.add_heading(title, level=0)

    for heading, body in sections:
        doc.add_heading(heading, level=1)
        for para in body.split("\n"):
            if para.strip():
                doc.add_paragraph(para.strip())

    for ttitle, df in tables:
        doc.add_heading(ttitle, level=2)
        # add table
        table = doc.add_table(rows=1, cols=df.shape[1])
        hdr = table.rows[0].cells
        for j, col in enumerate(df.columns):
            hdr[j].text = str(col)
        for _, row in df.iterrows():
            cells = table.add_row().cells
            for j, col in enumerate(df.columns):
                v = row[col]
                cells[j].text = "" if pd.isna(v) else f"{v}"
        doc.add_paragraph()

    for ftitle, fpath in figures:
        if fpath.exists():
            doc.add_heading(ftitle, level=2)
            doc.add_picture(str(fpath), width=Inches(6.5))
            doc.add_paragraph()

    out_docx.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out_docx))

def _write_pdf(out_pdf: Path, title: str, sections: List[Tuple[str, str]], figures: List[Tuple[str, Path]]):
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import inch
    except Exception:
        return

    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(out_pdf), pagesize=letter)
    width, height = letter

    y = height - 0.8*inch
    c.setFont("Helvetica-Bold", 16)
    c.drawString(0.75*inch, y, title)
    y -= 0.5*inch

    c.setFont("Helvetica", 10)

    for heading, body in sections:
        if y < 1.5*inch:
            c.showPage()
            y = height - 0.8*inch
            c.setFont("Helvetica", 10)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(0.75*inch, y, heading)
        y -= 0.25*inch
        c.setFont("Helvetica", 10)
        for line in body.split("\n"):
            if not line.strip():
                y -= 0.12*inch
                continue
            if y < 1.0*inch:
                c.showPage()
                y = height - 0.8*inch
                c.setFont("Helvetica", 10)
            c.drawString(0.75*inch, y, line[:120])
            y -= 0.14*inch
        y -= 0.1*inch

    # Figures
    for ftitle, fpath in figures:
        if not fpath.exists():
            continue
        c.showPage()
        y = height - 0.8*inch
        c.setFont("Helvetica-Bold", 12)
        c.drawString(0.75*inch, y, ftitle)
        y -= 0.3*inch
        # Fit image into page box
        img_w = width - 1.5*inch
        img_h = height - 1.8*inch
        c.drawImage(str(fpath), 0.75*inch, 0.75*inch, width=img_w, height=img_h, preserveAspectRatio=True, anchor='c')

    c.save()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--meta_dir", required=True, help="Path to outputs/runs/meta_pipeline/<timestamp>")
    parser.add_argument("--title", default="Policy brief: genetic discrimination protections (Australia and New Zealand)")
    parser.add_argument("--author", default="")
    parser.add_argument("--out", default="", help="Output folder (default: <meta_dir>/publish_pack)")
    args = parser.parse_args()

    meta_dir = Path(args.meta_dir)
    if not meta_dir.exists():
        raise FileNotFoundError(meta_dir)

    out_dir = Path(args.out) if args.out else (meta_dir / "publish_pack")
    out_dir.mkdir(parents=True, exist_ok=True)

    full_unc = meta_dir / "full_uncertainty"
    au_run = _latest_run_dir(full_unc, "australia_")
    nz_run = _latest_run_dir(full_unc, "new_zealand_")

    if au_run is None or nz_run is None:
        raise FileNotFoundError("Could not locate australia_*/new_zealand_* run dirs under meta_dir/full_uncertainty")

    # Build summary tables
    au_summary = _load_draws_summary(au_run)
    nz_summary = _load_draws_summary(nz_run)

    # Compute uncertainty driver tables (EVPPI + S1/ST) from theta matrices
    au_evppi, au_decomp = _compute_uncertainty_tables(au_run)
    nz_evppi, nz_decomp = _compute_uncertainty_tables(nz_run)

    # Save as CSV for portability
    au_summary.to_csv(out_dir / "australia_policy_summary.csv", index=False)
    nz_summary.to_csv(out_dir / "new_zealand_policy_summary.csv", index=False)
    au_evppi.to_csv(out_dir / "australia_evppi_by_group.csv", index=False)
    nz_evppi.to_csv(out_dir / "new_zealand_evppi_by_group.csv", index=False)
    au_decomp.to_csv(out_dir / "australia_uncertainty_decomposition.csv", index=False)
    nz_decomp.to_csv(out_dir / "new_zealand_uncertainty_decomposition.csv", index=False)

    # Figures
    figs_dir = out_dir / "figures"
    _plot_policy_bars(au_summary, figs_dir / "australia_net_benefit.png", "Australia: net benefit by policy (mean and 90% interval)")
    _plot_policy_bars(nz_summary, figs_dir / "new_zealand_net_benefit.png", "New Zealand: net benefit by policy (mean and 90% interval)")
    _plot_evppi(au_evppi, figs_dir / "australia_evppi.png", "Australia: EVPPI by parameter group (surrogate)")
    _plot_evppi(nz_evppi, figs_dir / "new_zealand_evppi.png", "New Zealand: EVPPI by parameter group (surrogate)")

    # Manifest snippets
    au_manifest = _maybe_load_manifest(au_run)
    nz_manifest = _maybe_load_manifest(nz_run)

    # Policy brief markdown
    def top3(df):
        return df.head(3)[["policy","nb_mean","nb_p05","nb_p95","qaly_mean","prem_mean"]]

    exec_lines = []
    exec_lines.append("This pack summarises the latest meta pipeline outputs for Australia and New Zealand.")
    exec_lines.append("Top policies are ranked by mean net benefit (DCBA ledger) with 90% intervals (5th to 95th percentile).")
    exec_lines.append("Uncertainty drivers are summarised using EVPPI and (approximate) Sobol indices when theta matrices are available.")

    md = []
    md.append(f"# {args.title}\n")
    if args.author:
        md.append(f"**Author:** {args.author}\n")
    md.append(f"**Source:** {meta_dir}\n")

    md.append("## Executive summary\n")
    md.extend([f"- {x}" for x in exec_lines])
    md.append("")

    md.append("## Australia results\n")
    md.append(top3(au_summary).to_markdown(index=False))
    md.append("")
    if not au_evppi.empty:
        md.append("### Australia: EVPPI by group\n")
        md.append(au_evppi[["group","evppi"]].to_markdown(index=False))
        md.append("")
    if not au_decomp.empty:
        md.append("### Australia: uncertainty decomposition (S1/ST)\n")
        md.append(au_decomp.to_markdown(index=False))
        md.append("")

    md.append("## New Zealand results\n")
    md.append(top3(nz_summary).to_markdown(index=False))
    md.append("")
    if not nz_evppi.empty:
        md.append("### New Zealand: EVPPI by group\n")
        md.append(nz_evppi[["group","evppi"]].to_markdown(index=False))
        md.append("")
    if not nz_decomp.empty:
        md.append("### New Zealand: uncertainty decomposition (S1/ST)\n")
        md.append(nz_decomp.to_markdown(index=False))
        md.append("")

    md.append("## Reproducibility\n")
    md.append("This analysis is configuration-driven and each run writes `run_manifest.json` with file hashes.")
    if au_manifest:
        md.append("\n### Australia run manifest (excerpt)\n")
        for k in ["created_utc","repo_tree_hash","policies_file","policies_file_sha256","base_config_file_sha256"]:
            if k in au_manifest:
                md.append(f"- {k}: {au_manifest[k]}")
    if nz_manifest:
        md.append("\n### New Zealand run manifest (excerpt)\n")
        for k in ["created_utc","repo_tree_hash","policies_file","policies_file_sha256","base_config_file_sha256"]:
            if k in nz_manifest:
                md.append(f"- {k}: {nz_manifest[k]}")

    (out_dir / "POLICY_BRIEF.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    # Write DOCX and PDF
    sections = [
        ("Executive summary", "\n".join(exec_lines)),
        ("Australia - top policies", "See table and figures."),
        ("New Zealand - top policies", "See table and figures."),
        ("Reproducibility", "Run manifests are included in each run directory."),
    ]
    tables = [
        ("Australia policy summary", au_summary),
        ("New Zealand policy summary", nz_summary),
    ]
    if not au_evppi.empty:
        tables.append(("Australia EVPPI by group", au_evppi[["group","evppi"]]))
    if not nz_evppi.empty:
        tables.append(("New Zealand EVPPI by group", nz_evppi[["group","evppi"]]))
    if not au_decomp.empty:
        tables.append(("Australia uncertainty decomposition", au_decomp))
    if not nz_decomp.empty:
        tables.append(("New Zealand uncertainty decomposition", nz_decomp))

    figures = [
        ("Australia: net benefit by policy", figs_dir / "australia_net_benefit.png"),
        ("New Zealand: net benefit by policy", figs_dir / "new_zealand_net_benefit.png"),
        ("Australia: EVPPI by group", figs_dir / "australia_evppi.png"),
        ("New Zealand: EVPPI by group", figs_dir / "new_zealand_evppi.png"),
    ]

    _write_docx(out_dir / "POLICY_BRIEF.docx", args.title, sections, tables, figures)
    _write_pdf(out_dir / "POLICY_BRIEF.pdf", args.title, sections, figures)

    print("Wrote publish pack to:", out_dir)

if __name__ == "__main__":
    main()
