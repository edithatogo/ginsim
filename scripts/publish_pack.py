from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from scripts.generate_figures import plot_evppi, plot_policy_bars
from scripts.reporting_common import build_reporting_bundle, write_reporting_tables

try:
    from docx import Document
    from docx.shared import Inches
except Exception:  # pragma: no cover - optional dependency surface
    Document = None
    Inches = None

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.pdfgen import canvas
except Exception:  # pragma: no cover - optional dependency surface
    letter = None
    inch = None
    canvas = None


def _write_docx(
    out_docx: Path,
    title: str,
    sections: list[tuple[str, str]],
    tables: list[tuple[str, pd.DataFrame]],
    figures: list[tuple[str, Path]],
) -> Path:
    if Document is None or Inches is None:
        message = "DOCX output requires python-docx to be installed."
        raise RuntimeError(message)

    doc = Document()
    doc.add_heading(title, level=0)

    for heading, body in sections:
        doc.add_heading(heading, level=1)
        for paragraph in body.split("\n"):
            if paragraph.strip():
                doc.add_paragraph(paragraph.strip())

    for table_title, df in tables:
        doc.add_heading(table_title, level=2)
        table = doc.add_table(rows=1, cols=df.shape[1])
        header_cells = table.rows[0].cells
        for index, column in enumerate(df.columns):
            header_cells[index].text = str(column)
        for _, row in df.iterrows():
            cells = table.add_row().cells
            for index, column in enumerate(df.columns):
                value = row[column]
                cells[index].text = "" if pd.isna(value) else f"{value}"
        doc.add_paragraph()

    for figure_title, figure_path in figures:
        if figure_path.exists():
            doc.add_heading(figure_title, level=2)
            doc.add_picture(str(figure_path), width=Inches(6.5))
            doc.add_paragraph()

    out_docx.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out_docx))
    return out_docx


def _write_pdf(
    out_pdf: Path,
    title: str,
    sections: list[tuple[str, str]],
    figures: list[tuple[str, Path]],
) -> Path:
    if letter is None or inch is None or canvas is None:
        message = "PDF output requires reportlab to be installed."
        raise RuntimeError(message)

    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(out_pdf), pagesize=letter)
    width, height = letter

    y_position = height - 0.8 * inch
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(0.75 * inch, y_position, title)
    y_position -= 0.5 * inch
    pdf.setFont("Helvetica", 10)

    for heading, body in sections:
        if y_position < 1.5 * inch:
            pdf.showPage()
            y_position = height - 0.8 * inch
            pdf.setFont("Helvetica", 10)

        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(0.75 * inch, y_position, heading)
        y_position -= 0.25 * inch
        pdf.setFont("Helvetica", 10)

        for line in body.split("\n"):
            if not line.strip():
                y_position -= 0.12 * inch
                continue
            if y_position < 1.0 * inch:
                pdf.showPage()
                y_position = height - 0.8 * inch
                pdf.setFont("Helvetica", 10)
            pdf.drawString(0.75 * inch, y_position, line[:120])
            y_position -= 0.14 * inch
        y_position -= 0.1 * inch

    for figure_title, figure_path in figures:
        if not figure_path.exists():
            continue
        pdf.showPage()
        y_position = height - 0.8 * inch
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(0.75 * inch, y_position, figure_title)
        y_position -= 0.3 * inch
        pdf.drawImage(
            str(figure_path),
            0.75 * inch,
            0.75 * inch,
            width=width - 1.5 * inch,
            height=height - 1.8 * inch,
            preserveAspectRatio=True,
            anchor="c",
        )

    pdf.save()
    return out_pdf


def _build_markdown_brief(
    title: str,
    author: str,
    meta_dir: Path,
    bundle: dict[str, object],
) -> str:
    policy_summary = bundle["policy_summary"]
    evppi_by_group = bundle["evppi_by_group"]
    uncertainty_decomposition = bundle["uncertainty_decomposition"]
    manifests = bundle["manifests"]

    lines = [f"# {title}", ""]
    if author:
        lines.append(f"**Author:** {author}")
        lines.append("")
    lines.append(f"**Source:** {meta_dir}")
    lines.append("")
    lines.append("## Executive summary")
    lines.append("")
    lines.append(
        "- This pack summarises the latest meta pipeline outputs for Australia and New Zealand."
    )
    lines.append(
        "- Policies are ranked by mean net benefit with 90% intervals computed from uncertainty draws."
    )
    if not evppi_by_group.empty:
        lines.append(
            "- Uncertainty drivers are summarised with EVPPI and Sobol-style decompositions when theta matrices are available."
        )
    lines.append("")

    for jurisdiction in sorted(bundle["run_dirs"]):
        title_case = jurisdiction.replace("_", " ").title()
        jurisdiction_summary = policy_summary.loc[
            policy_summary["jurisdiction"] == jurisdiction
        ].drop(columns=["jurisdiction"])
        lines.append(f"## {title_case} results")
        lines.append("")
        lines.append(jurisdiction_summary.head(3).to_markdown(index=False))
        lines.append("")

        jurisdiction_evppi = evppi_by_group.loc[
            evppi_by_group["jurisdiction"] == jurisdiction
        ].drop(columns=["jurisdiction"])
        if not jurisdiction_evppi.empty:
            lines.append(f"### {title_case}: EVPPI by group")
            lines.append("")
            lines.append(jurisdiction_evppi.to_markdown(index=False))
            lines.append("")

        jurisdiction_decomposition = uncertainty_decomposition.loc[
            uncertainty_decomposition["jurisdiction"] == jurisdiction
        ].drop(columns=["jurisdiction"])
        if not jurisdiction_decomposition.empty:
            lines.append(f"### {title_case}: uncertainty decomposition")
            lines.append("")
            lines.append(jurisdiction_decomposition.to_markdown(index=False))
            lines.append("")

    lines.append("## Reproducibility")
    lines.append("")
    lines.append(
        "This analysis is configuration-driven and each run directory carries a manifest plus deterministic reporting outputs."
    )
    lines.append("")

    for jurisdiction, manifest in manifests.items():
        if not manifest:
            continue
        lines.append(f"### {jurisdiction.replace('_', ' ').title()} run manifest (excerpt)")
        lines.append("")
        for key in [
            "created_utc",
            "repo_tree_hash",
            "policies_file",
            "policies_file_sha256",
            "base_config_file_sha256",
        ]:
            value = manifest.get(key)
            if value is not None:
                lines.append(f"- {key}: {value}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--meta_dir",
        required=True,
        help="Path to outputs/runs/meta_pipeline/<timestamp>",
    )
    parser.add_argument(
        "--title",
        default="Policy brief: genetic discrimination protections (Australia and New Zealand)",
    )
    parser.add_argument("--author", default="")
    parser.add_argument(
        "--out",
        default="",
        help="Output folder (default: <meta_dir>/publish_pack)",
    )
    args = parser.parse_args()

    meta_dir = Path(args.meta_dir)
    if not meta_dir.exists():
        raise FileNotFoundError(meta_dir)

    out_dir = Path(args.out) if args.out else (meta_dir / "publish_pack")
    out_dir.mkdir(parents=True, exist_ok=True)

    bundle = build_reporting_bundle(meta_dir=meta_dir)
    generated_tables = write_reporting_tables(out_dir, bundle)

    figures_dir = out_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    for jurisdiction in sorted(bundle["run_dirs"]):
        plot_policy_bars(bundle["policy_summary"], jurisdiction, figures_dir, 200, ["png"])
        plot_evppi(bundle["evppi_by_group"], jurisdiction, figures_dir, 200, ["png"])

    policy_summary = bundle["policy_summary"]
    evppi_by_group = bundle["evppi_by_group"]
    uncertainty_decomposition = bundle["uncertainty_decomposition"]

    (out_dir / "POLICY_BRIEF.md").write_text(
        _build_markdown_brief(args.title, args.author, meta_dir, bundle),
        encoding="utf-8",
    )

    sections = [
        (
            "Executive summary",
            "This pack summarises the latest meta pipeline outputs for Australia and New Zealand.\n"
            "Policies are ranked by mean net benefit with 90% intervals computed from uncertainty draws.\n"
            "Reporting tables and figures are generated directly from the run directories.",
        ),
        ("Australia - top policies", "See the jurisdiction-specific summary table and figure."),
        ("New Zealand - top policies", "See the jurisdiction-specific summary table and figure."),
        (
            "Reproducibility",
            "Each generated artifact records its source run directory in reporting_manifest.json.",
        ),
    ]

    tables: list[tuple[str, pd.DataFrame]] = []
    figures: list[tuple[str, Path]] = []
    for jurisdiction in sorted(bundle["run_dirs"]):
        label = jurisdiction.replace("_", " ").title()
        jurisdiction_summary = policy_summary.loc[
            policy_summary["jurisdiction"] == jurisdiction
        ].drop(columns=["jurisdiction"])
        tables.append((f"{label} policy summary", jurisdiction_summary))

        jurisdiction_evppi = evppi_by_group.loc[
            evppi_by_group["jurisdiction"] == jurisdiction
        ].drop(columns=["jurisdiction"])
        if not jurisdiction_evppi.empty:
            tables.append((f"{label} EVPPI by group", jurisdiction_evppi))

        jurisdiction_decomposition = uncertainty_decomposition.loc[
            uncertainty_decomposition["jurisdiction"] == jurisdiction
        ].drop(columns=["jurisdiction"])
        if not jurisdiction_decomposition.empty:
            tables.append((f"{label} uncertainty decomposition", jurisdiction_decomposition))

        figures.append(
            (
                f"{label}: net benefit by policy",
                figures_dir / f"{jurisdiction}_net_benefit.png",
            )
        )
        figures.append(
            (
                f"{label}: EVPPI by group",
                figures_dir / f"{jurisdiction}_evppi.png",
            )
        )

    generated_docx = _write_docx(
        out_dir / "POLICY_BRIEF.docx", args.title, sections, tables, figures
    )
    generated_pdf = _write_pdf(out_dir / "POLICY_BRIEF.pdf", args.title, sections, figures)

    if not generated_docx.exists() or not generated_pdf.exists():
        message = "Publish pack did not produce the expected DOCX/PDF artifacts."
        raise RuntimeError(message)

    print("Wrote publish pack to:", out_dir)
    print("Generated tables:", ", ".join(sorted(generated_tables)))
    print("Generated documents:", generated_docx.name, generated_pdf.name)


if __name__ == "__main__":
    main()
