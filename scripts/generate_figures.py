#!/usr/bin/env python3
"""
Generate reporting figures from run outputs.

Usage:
    python -m scripts.generate_figures --meta_dir outputs/runs/meta_pipeline/20260306T010203Z
    python -m scripts.generate_figures --run_dir outputs/runs/full_uncertainty/australia_20260306T010203Z
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import TYPE_CHECKING

import matplotlib as mpl
import numpy as np

from scripts.reporting_common import build_reporting_bundle

if TYPE_CHECKING:
    import pandas as pd

mpl.use("Agg")
import matplotlib.pyplot as plt

# Colorblind-safe palettes
OKABE_ITO = {
    "orange": "#E69F00",
    "sky_blue": "#56B4E9",
    "bluish_green": "#009E73",
    "yellow": "#F0E442",
    "blue": "#0072B2",
    "vermilion": "#D55E00",
    "reddish_purple": "#CC79A7",
    "black": "#000000",
}


def save_figure(fig: plt.Figure, output_path: Path, dpi: int, formats: list[str]) -> None:
    """Save a figure in one or more formats."""
    for fmt in formats:
        path = output_path.with_suffix(f".{fmt}")
        if fmt == "png":
            fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor="white")
        else:
            fig.savefig(path, bbox_inches="tight", facecolor="white")
        print(f"  ✓ Saved {path.name}")
    plt.close(fig)


def _write_caption(output_dir: Path, stem: str, caption: str) -> None:
    """Write a plain-text caption alongside generated figure files."""
    caption_path = output_dir / f"{stem}_caption.md"
    caption_path.write_text(caption.strip() + "\n", encoding="utf-8")
    print(f"  ✓ Saved {caption_path.name}")


def plot_policy_bars(
    summary_df: pd.DataFrame,
    jurisdiction: str,
    output_dir: Path,
    dpi: int,
    formats: list[str],
) -> None:
    """Plot policy net benefit means with 90% intervals for one jurisdiction."""
    df = (
        summary_df.loc[summary_df["jurisdiction"] == jurisdiction]
        .drop(columns=["jurisdiction"])
        .sort_values("nb_mean", ascending=False)
    )
    if df.empty:
        return

    x_positions = np.arange(df.shape[0])
    means = df["nb_mean"].to_numpy()
    error_bars = np.vstack([means - df["nb_p05"].to_numpy(), df["nb_p95"].to_numpy() - means])

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(
        x_positions,
        means,
        yerr=error_bars,
        capsize=4,
        color=OKABE_ITO["blue"],
        alpha=0.85,
    )
    ax.set_xticks(x_positions)
    ax.set_xticklabels(df["policy"].to_list(), rotation=30, ha="right")
    ax.set_ylabel("Net benefit")
    ax.set_title(
        f"{jurisdiction.replace('_', ' ').title()}: net benefit by policy (mean and 90% interval)",
        fontweight="bold",
    )
    ax.grid(True, axis="y", alpha=0.3)

    save_figure(fig, output_dir / f"{jurisdiction}_net_benefit", dpi, formats)
    _write_caption(
        output_dir,
        f"{jurisdiction}_net_benefit",
        (
            f"Figure: {jurisdiction.replace('_', ' ').title()} policy ranking by mean long-run net benefit. "
            "Bars show posterior means and whiskers show the 90% interval from uncertainty draws."
        ),
    )


def plot_evppi(
    evppi_df: pd.DataFrame,
    jurisdiction: str,
    output_dir: Path,
    dpi: int,
    formats: list[str],
) -> None:
    """Plot EVPPI by parameter group for one jurisdiction."""
    df = (
        evppi_df.loc[evppi_df["jurisdiction"] == jurisdiction]
        .drop(columns=["jurisdiction"])
        .sort_values("evppi", ascending=False)
    )
    if df.empty:
        return

    x_positions = np.arange(df.shape[0])
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(x_positions, df["evppi"].to_numpy(), color=OKABE_ITO["sky_blue"])
    ax.set_xticks(x_positions)
    ax.set_xticklabels(df["group"].to_list(), rotation=30, ha="right")
    ax.set_ylabel("EVPPI")
    ax.set_title(
        f"{jurisdiction.replace('_', ' ').title()}: EVPPI by parameter group",
        fontweight="bold",
    )
    ax.grid(True, axis="y", alpha=0.3)

    save_figure(fig, output_dir / f"{jurisdiction}_evppi", dpi, formats)
    _write_caption(
        output_dir,
        f"{jurisdiction}_evppi",
        (
            f"Figure: {jurisdiction.replace('_', ' ').title()} expected value of partial perfect information by parameter group. "
            "Higher bars indicate uncertainty groups with greater decision value for additional evidence collection."
        ),
    )


def plot_uncertainty_decomposition(
    decomposition_df: pd.DataFrame,
    jurisdiction: str,
    output_dir: Path,
    dpi: int,
    formats: list[str],
) -> None:
    """Plot total-order uncertainty contributions for one jurisdiction."""
    df = (
        decomposition_df.loc[decomposition_df["jurisdiction"] == jurisdiction]
        .drop(columns=["jurisdiction"])
        .sort_values("ST_optimal_NB", ascending=False)
    )
    if df.empty:
        return

    x_positions = np.arange(df.shape[0])
    width = 0.38
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.bar(
        x_positions - width / 2,
        df["S1_optimal_NB"].to_numpy(),
        width=width,
        color=OKABE_ITO["bluish_green"],
        label="First-order",
    )
    ax.bar(
        x_positions + width / 2,
        df["ST_optimal_NB"].to_numpy(),
        width=width,
        color=OKABE_ITO["vermilion"],
        label="Total-order",
    )
    ax.set_xticks(x_positions)
    ax.set_xticklabels(df["group"].to_list(), rotation=30, ha="right")
    ax.set_ylabel("Sensitivity index")
    ax.set_title(
        f"{jurisdiction.replace('_', ' ').title()}: uncertainty decomposition for optimal net benefit",
        fontweight="bold",
    )
    ax.legend(frameon=False)
    ax.grid(True, axis="y", alpha=0.3)

    save_figure(fig, output_dir / f"{jurisdiction}_uncertainty_decomposition", dpi, formats)
    _write_caption(
        output_dir,
        f"{jurisdiction}_uncertainty_decomposition",
        (
            f"Figure: {jurisdiction.replace('_', ' ').title()} first-order and total-order uncertainty decomposition for optimal net benefit. "
            "Total-order indices capture main effects plus interactions, while first-order indices isolate direct contributions."
        ),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate reporting figures from model outputs")
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "--meta_dir",
        type=str,
        help="Meta-pipeline directory containing full_uncertainty jurisdiction run directories",
    )
    input_group.add_argument(
        "--run_dir",
        type=str,
        help="Single-jurisdiction full uncertainty run directory",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="",
        help="Output directory for figures (default: <meta_dir>/figures or <run_dir>/figures)",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="Resolution for PNG output",
    )
    parser.add_argument(
        "--formats",
        type=str,
        nargs="+",
        default=["png", "svg"],
        help="Output formats",
    )
    args = parser.parse_args()

    meta_dir = Path(args.meta_dir) if args.meta_dir else None
    run_dir = Path(args.run_dir) if args.run_dir else None
    output_dir = (
        Path(args.output)
        if args.output
        else (meta_dir / "figures" if meta_dir is not None else run_dir / "figures")
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("FIGURE GENERATION")
    print("=" * 60)

    bundle = build_reporting_bundle(meta_dir=meta_dir, run_dir=run_dir)
    jurisdictions = sorted(bundle["run_dirs"])

    for jurisdiction in jurisdictions:
        plot_policy_bars(bundle["policy_summary"], jurisdiction, output_dir, args.dpi, args.formats)
        plot_evppi(bundle["evppi_by_group"], jurisdiction, output_dir, args.dpi, args.formats)
        plot_uncertainty_decomposition(
            bundle["uncertainty_decomposition"],
            jurisdiction,
            output_dir,
            args.dpi,
            args.formats,
        )

    print(f"Source runs: {', '.join(jurisdictions)}")
    print("=" * 60)
    print(f"✓ Reporting figures generated in {output_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()
