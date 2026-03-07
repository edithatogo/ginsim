"""
Game Theoretic Framings - Diagram Generation.

Visualizes the core strategic games within each module using Matplotlib.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure


@dataclass(frozen=True)
class DiagramConfig:
    """Configuration for diagram styling."""

    title: str
    xlabel: str
    ylabel: str
    color_scheme: str = "viridis"


def create_module_a_diagram(
    params: Any = None,
    config: DiagramConfig | None = None,
) -> Figure:
    """Generate strategic participation game diagram for Module A."""
    fig, ax = plt.subplots(figsize=(8, 6))
    x = np.linspace(0, 1, 100)
    y = x**2
    ax.plot(x, y)
    ax.set_title("Module A: Participation Game")
    return fig


def create_module_c_diagram(
    params: Any = None,
    config: DiagramConfig | None = None,
) -> Figure:
    """Generate insurance equilibrium diagram for Module C."""
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_title("Module C: Insurance Equilibrium")
    return fig


def create_module_d_diagram(
    params: Any = None,
    config: DiagramConfig | None = None,
) -> Figure:
    """Generate proxy reconstruction diagram for Module D."""
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_title("Module D: Proxy Reconstruction")
    return fig


def create_module_e_diagram(
    params: Any = None,
    config: DiagramConfig | None = None,
) -> Figure:
    """Generate welfare mapping diagram for Module E."""
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_title("Module E: Welfare Mapping")
    return fig


def create_module_f_diagram(
    params: Any = None,
    config: DiagramConfig | None = None,
) -> Figure:
    """Generate research quality diagram for Module F."""
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_title("Module F: Research Externalities")
    return fig


def create_enforcement_diagram(
    params: Any = None,
    config: DiagramConfig | None = None,
) -> Figure:
    """Generate enforcement effectiveness diagram."""
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_title("Enforcement Game")
    return fig


def generate_all_game_diagrams(
    output_dir: Path | None = None,
    params: Any = None,
) -> dict[str, list[Path]]:
    """
    Generate all module diagrams and export them.
    Returns a dictionary mapping module names to lists of [PNG, SVG] paths.
    """
    figs = {
        "module_a": create_module_a_diagram(params),
        "module_c": create_module_c_diagram(params),
        "module_d": create_module_d_diagram(params),
        "module_e": create_module_e_diagram(params),
        "module_f": create_module_f_diagram(params),
        "enforcement": create_enforcement_diagram(params),
    }

    results = {}
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        for name, fig in figs.items():
            png_path = output_dir / f"{name}.png"
            svg_path = output_dir / f"{name}.svg"
            fig.savefig(png_path)
            fig.savefig(svg_path)
            results[name] = [png_path, svg_path]
            plt.close(fig)
    else:
        # Mock paths for testing if no dir provided
        for name in figs:
            results[name] = [Path(f"{name}.png"), Path(f"{name}.svg")]
            plt.close(figs[name])

    return results
