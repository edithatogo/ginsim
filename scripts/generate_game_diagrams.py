#!/usr/bin/env python3
"""
Generate game structure diagrams for all 6 game-theoretic modules.

Usage:
    python -m scripts.generate_game_diagrams --output outputs/figures/games --formats png svg
"""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches

# Colorblind-safe palette (Okabe-Ito)
COLORS = {
    "orange": "#E69F00",
    "sky_blue": "#56B4E9",
    "bluish_green": "#009E73",
    "yellow": "#F0E442",
    "blue": "#0072B2",
    "vermilion": "#D55E00",
    "reddish_purple": "#CC79A7",
    "black": "#000000",
    "gray": "#999999",
}


def save_figure(fig, output_path: Path, dpi: int = 1200, formats: list = None):
    """Save figure in multiple formats."""
    if formats is None:
        formats = ["png", "svg"]

    for fmt in formats:
        if fmt == "png":
            path = output_path.with_suffix(".png")
            fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor="white")
            print(f"  ✓ Saved {path.name} ({dpi}dpi)")
        elif fmt == "svg":
            path = output_path.with_suffix(".svg")
            fig.savefig(path, bbox_inches="tight", facecolor="white")
            print(f"  ✓ Saved {path.name}")

    plt.close(fig)


def generate_module_a_diagram(output_dir: Path, dpi: int, formats: list):
    """Generate Module A: Behavior/Deterrence game structure diagram."""
    print("Generating Module A: Behavior/Deterrence diagram...")

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.set_axis_off()

    # Title
    ax.text(
        6,
        9.5,
        "Module A: Behavior/Deterrence Game",
        fontsize=16,
        fontweight="bold",
        ha="center",
        va="top",
    )

    # Players
    players = [
        (1, 7, "Individuals", COLORS["blue"], "Testing decision"),
        (6, 7, "Insurers", COLORS["vermilion"], "Premium setting"),
        (11, 7, "Policymakers", COLORS["bluish_green"], "Policy regime"),
    ]

    for x, y, name, color, role in players:
        rect = patches.Rectangle(
            (x - 1.2, y - 0.8),
            2.4,
            1.6,
            linewidth=2,
            edgecolor=color,
            facecolor=color,
            alpha=0.2,
        )
        ax.add_patch(rect)
        ax.text(x, y, name, fontsize=12, fontweight="bold", ha="center", va="center", color=color)
        ax.text(x, y - 0.5, role, fontsize=9, ha="center", va="center", style="italic")

    # Game sequence arrows
    arrow_props = dict(arrowstyle="->", color=COLORS["black"], linewidth=2)

    # Policy → Individual
    ax.annotate(
        "",
        xy=(10, 7),
        xytext=(2, 7),
        arrowprops=dict(arrowstyle="->", color=COLORS["bluish_green"], linewidth=2.5),
    )
    ax.text(6, 7.3, "1. Sets policy regime", fontsize=10, ha="center", va="bottom")

    # Individual → Insurer
    ax.annotate(
        "",
        xy=(5, 7),
        xytext=(3, 7),
        arrowprops=dict(arrowstyle="->", color=COLORS["blue"], linewidth=2.5),
    )
    ax.text(4, 6.6, "2. Testing decision", fontsize=10, ha="center", va="top")

    # Insurer → Payoffs
    ax.annotate(
        "",
        xy=(8, 7),
        xytext=(7, 7),
        arrowprops=dict(arrowstyle="->", color=COLORS["vermilion"], linewidth=2.5),
    )
    ax.text(7.5, 7.3, "3. Sets premiums", fontsize=10, ha="center", va="bottom")

    # Equilibrium box
    rect = patches.Rectangle(
        (4, 2.5),
        4,
        3,
        linewidth=2,
        edgecolor=COLORS["black"],
        facecolor="white",
        linestyle="--",
    )
    ax.add_patch(rect)
    ax.text(
        6,
        4.5,
        "Equilibrium:\nTesting uptake = f(policy, penalty)",
        fontsize=11,
        ha="center",
        va="center",
    )

    # Utility function
    ax.text(
        6,
        1.5,
        r"$U_i = \text{health\_benefit} - \text{perceived\_penalty}(\text{policy})$",
        fontsize=12,
        ha="center",
        va="center",
        family="monospace",
    )

    save_figure(fig, output_dir / "module_a_behavior", dpi, formats)


def generate_module_c_diagram(output_dir: Path, dpi: int, formats: list):
    """Generate Module C: Insurance Equilibrium (Rothschild-Stiglitz) diagram."""
    print("Generating Module C: Insurance Equilibrium diagram...")

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.set_axis_off()

    # Title
    ax.text(
        6,
        9.5,
        "Module C: Insurance Equilibrium (Rothschild-Stiglitz)",
        fontsize=16,
        fontweight="bold",
        ha="center",
        va="top",
    )

    # Information asymmetry
    ax.text(
        6,
        8.5,
        "Information Asymmetry: Applicants know risk, Insurers don't",
        fontsize=11,
        ha="center",
        va="center",
        style="italic",
        bbox=dict(boxstyle="round", facecolor=COLORS["yellow"], alpha=0.3),
    )

    # Players
    applicants_box = patches.Rectangle(
        (1, 5.5),
        4,
        2,
        linewidth=2,
        edgecolor=COLORS["blue"],
        facecolor=COLORS["blue"],
        alpha=0.2,
    )
    ax.add_patch(applicants_box)
    ax.text(
        3,
        6.5,
        "Applicants\n(Informed)",
        fontsize=12,
        fontweight="bold",
        ha="center",
        va="center",
        color=COLORS["blue"],
    )

    insurer_box = patches.Rectangle(
        (7, 5.5),
        4,
        2,
        linewidth=2,
        edgecolor=COLORS["vermilion"],
        facecolor=COLORS["vermilion"],
        alpha=0.2,
    )
    ax.add_patch(insurer_box)
    ax.text(
        9,
        6.5,
        "Insurers\n(Uninformed)",
        fontsize=12,
        fontweight="bold",
        ha="center",
        va="center",
        color=COLORS["vermilion"],
    )

    # Equilibrium types
    sep_box = patches.Rectangle(
        (2, 2.5),
        3.5,
        2,
        linewidth=2,
        edgecolor=COLORS["bluish_green"],
        facecolor="white",
        linestyle="-",
    )
    ax.add_patch(sep_box)
    ax.text(
        3.75,
        3.5,
        "Separating\nEquilibrium\n(Different premiums)",
        fontsize=10,
        ha="center",
        va="center",
    )

    pool_box = patches.Rectangle(
        (6.5, 2.5),
        3.5,
        2,
        linewidth=2,
        edgecolor=COLORS["orange"],
        facecolor="white",
        linestyle="-",
    )
    ax.add_patch(pool_box)
    ax.text(
        8.25,
        3.5,
        "Pooling\nEquilibrium\n(Same premium)",
        fontsize=10,
        ha="center",
        va="center",
    )

    # Policy constraint
    ax.text(
        6,
        1,
        "Policy Constraint:\nMoratorium/Ban restricts information use",
        fontsize=10,
        ha="center",
        va="center",
        bbox=dict(boxstyle="round", facecolor=COLORS["gray"], alpha=0.2),
    )

    save_figure(fig, output_dir / "module_c_insurance_eq", dpi, formats)


def generate_module_d_diagram(output_dir: Path, dpi: int, formats: list):
    """Generate Module D: Proxy Substitution diagram."""
    print("Generating Module D: Proxy Substitution diagram...")

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.set_axis_off()

    # Title
    ax.text(
        6,
        9.5,
        "Module D: Proxy Substitution Game",
        fontsize=16,
        fontweight="bold",
        ha="center",
        va="top",
    )

    # Constraint box
    constraint = patches.Rectangle(
        (1, 7),
        10,
        1.5,
        linewidth=2,
        edgecolor=COLORS["vermilion"],
        facecolor=COLORS["vermilion"],
        alpha=0.1,
        linestyle="--",
    )
    ax.add_patch(constraint)
    ax.text(
        6,
        7.75,
        "Constraint: Cannot use genetic test results directly",
        fontsize=11,
        ha="center",
        va="center",
        color=COLORS["vermilion"],
        fontweight="bold",
    )

    # Proxies
    proxies = ["Family History", "Age", "Gender", "Lifestyle", "Medical History"]
    for i, proxy in enumerate(proxies):
        x = 1.5 + i * 2
        rect = patches.Rectangle(
            (x - 0.8, 5),
            1.6,
            1.2,
            linewidth=2,
            edgecolor=COLORS["sky_blue"],
            facecolor=COLORS["sky_blue"],
            alpha=0.3,
        )
        ax.add_patch(rect)
        ax.text(x, 5.6, proxy, fontsize=9, ha="center", va="center", rotation=45)

    # Arrow to risk score
    ax.annotate(
        "",
        xy=(10, 5.6),
        xytext=(9.5, 5.6),
        arrowprops=dict(arrowstyle="->", color=COLORS["black"], linewidth=2),
    )

    # Risk score
    risk_box = patches.Rectangle(
        (9, 4.5),
        2.5,
        2,
        linewidth=2,
        edgecolor=COLORS["blue"],
        facecolor=COLORS["blue"],
        alpha=0.2,
    )
    ax.add_patch(risk_box)
    ax.text(
        10.25,
        5.5,
        "Risk Score",
        fontsize=11,
        fontweight="bold",
        ha="center",
        va="center",
        color=COLORS["blue"],
    )

    # Formula
    ax.text(
        10.25,
        4.8,
        r"$\sum w_i \cdot x_i$",
        fontsize=14,
        ha="center",
        va="center",
        family="monospace",
    )

    # Accuracy metrics
    ax.text(
        6,
        2.5,
        "Accuracy Metrics:\nSensitivity: 0.68\nSpecificity: 0.75",
        fontsize=10,
        ha="center",
        va="center",
        bbox=dict(boxstyle="round", facecolor=COLORS["yellow"], alpha=0.3),
    )

    save_figure(fig, output_dir / "module_d_proxy", dpi, formats)


def generate_module_e_diagram(output_dir: Path, dpi: int, formats: list):
    """Generate Module E: Pass-Through diagram."""
    print("Generating Module E: Pass-Through diagram...")

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.set_axis_off()

    # Title
    ax.text(
        6,
        9.5,
        "Module E: Pass-Through / Market Structure Game",
        fontsize=16,
        fontweight="bold",
        ha="center",
        va="top",
    )

    # Market structure spectrum
    ax.text(
        6,
        8.5,
        "Market Structure → Pass-Through Rate",
        fontsize=12,
        ha="center",
        va="center",
        fontweight="bold",
    )

    # Spectrum
    structures = [
        (2, "Monopoly", "Low\n(30-50%)", COLORS["vermilion"]),
        (6, "Oligopoly", "Medium\n(50-70%)", COLORS["orange"]),
        (10, "Competitive", "High\n(70-90%)", COLORS["bluish_green"]),
    ]

    for x, structure, rate, color in structures:
        rect = patches.Rectangle(
            (x - 1.5, 5.5),
            3,
            2.5,
            linewidth=2,
            edgecolor=color,
            facecolor=color,
            alpha=0.2,
        )
        ax.add_patch(rect)
        ax.text(
            x,
            6.5,
            structure,
            fontsize=11,
            fontweight="bold",
            ha="center",
            va="center",
            color=color,
        )
        ax.text(x, 5.8, rate, fontsize=10, ha="center", va="center")

    # Pass-through formula
    ax.text(
        6,
        3.5,
        r"Pass-Through Rate: $\tau \in [0.3, 0.9]$",
        fontsize=13,
        ha="center",
        va="center",
        family="monospace",
        bbox=dict(boxstyle="round", facecolor=COLORS["yellow"], alpha=0.3),
    )

    ax.text(
        6,
        2.5,
        r"Premium Change = $\tau \times$ Cost Shock",
        fontsize=12,
        ha="center",
        va="center",
        family="monospace",
    )

    save_figure(fig, output_dir / "module_e_passthrough", dpi, formats)


def generate_module_f_diagram(output_dir: Path, dpi: int, formats: list):
    """Generate Module F: Data Quality Externality diagram."""
    print("Generating Module F: Data Quality Externality diagram...")

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.set_axis_off()

    # Title
    ax.text(
        6,
        9.5,
        "Module F: Data Quality Externality Game",
        fontsize=16,
        fontweight="bold",
        ha="center",
        va="top",
    )

    # Public good structure
    ax.text(
        6,
        8.5,
        "Participation as Public Good",
        fontsize=12,
        ha="center",
        va="center",
        fontweight="bold",
        bbox=dict(boxstyle="round", facecolor=COLORS["bluish_green"], alpha=0.2),
    )

    # Players
    individuals = patches.Circle(
        (3, 5.5),
        1.5,
        linewidth=2,
        edgecolor=COLORS["blue"],
        facecolor=COLORS["blue"],
        alpha=0.2,
    )
    ax.add_patch(individuals)
    ax.text(
        3,
        5.5,
        "Individuals\n(Privacy cost\nvs. Social benefit)",
        fontsize=9,
        ha="center",
        va="center",
        color=COLORS["blue"],
    )

    researchers = patches.Circle(
        (9, 5.5),
        1.5,
        linewidth=2,
        edgecolor=COLORS["vermilion"],
        facecolor=COLORS["vermilion"],
        alpha=0.2,
    )
    ax.add_patch(researchers)
    ax.text(
        9,
        5.5,
        "Researchers\n(Data quality\n→ Research value)",
        fontsize=9,
        ha="center",
        va="center",
        color=COLORS["vermilion"],
    )

    # Externality arrow
    ax.annotate(
        "",
        xy=(7.5, 5.5),
        xytext=(4.5, 5.5),
        arrowprops=dict(arrowstyle="->", color=COLORS["bluish_green"], linewidth=3),
    )
    ax.text(
        6,
        5.8,
        "Positive Externality",
        fontsize=10,
        ha="center",
        va="bottom",
        color=COLORS["bluish_green"],
        fontweight="bold",
    )

    # Participation function
    ax.text(
        6,
        3,
        r"Participation Rate: $p = f(\text{policy}, \text{privacy\_concern})$",
        fontsize=12,
        ha="center",
        va="center",
        family="monospace",
        bbox=dict(boxstyle="round", facecolor=COLORS["yellow"], alpha=0.3),
    )

    ax.text(
        6,
        2,
        r"Elasticity: -0.10 (negative policy effect)",
        fontsize=10,
        ha="center",
        va="center",
        style="italic",
    )

    save_figure(fig, output_dir / "module_f_data_quality", dpi, formats)


def generate_enforcement_diagram(output_dir: Path, dpi: int, formats: list):
    """Generate Enforcement: Compliance Game diagram."""
    print("Generating Enforcement: Compliance Game diagram...")

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.set_axis_off()

    # Title
    ax.text(
        6,
        9.5,
        "Enforcement: Compliance Game",
        fontsize=16,
        fontweight="bold",
        ha="center",
        va="top",
    )

    # Mixed strategy
    ax.text(
        6,
        8.5,
        "Mixed Strategy Nash Equilibrium",
        fontsize=12,
        ha="center",
        va="center",
        fontweight="bold",
        bbox=dict(boxstyle="round", facecolor=COLORS["orange"], alpha=0.2),
    )

    # Insurer decision
    insurer_box = patches.Rectangle(
        (1, 5),
        4,
        3,
        linewidth=2,
        edgecolor=COLORS["vermilion"],
        facecolor=COLORS["vermilion"],
        alpha=0.2,
    )
    ax.add_patch(insurer_box)
    ax.text(
        3,
        6.5,
        "Insurers",
        fontsize=12,
        fontweight="bold",
        ha="center",
        va="center",
        color=COLORS["vermilion"],
    )
    ax.text(3, 5.8, "Strategy:\nComply vs. Violate", fontsize=9, ha="center", va="center")

    # Regulator decision
    regulator_box = patches.Rectangle(
        (7, 5),
        4,
        3,
        linewidth=2,
        edgecolor=COLORS["blue"],
        facecolor=COLORS["blue"],
        alpha=0.2,
    )
    ax.add_patch(regulator_box)
    ax.text(
        9,
        6.5,
        "Regulator",
        fontsize=12,
        fontweight="bold",
        ha="center",
        va="center",
        color=COLORS["blue"],
    )
    ax.text(9, 5.8, "Strategy:\nMonitor vs. Ignore", fontsize=9, ha="center", va="center")

    # Expected penalty
    ax.annotate(
        "",
        xy=(7, 6.5),
        xytext=(5, 6.5),
        arrowprops=dict(arrowstyle="->", color=COLORS["black"], linewidth=2),
    )

    ax.text(6, 7, "Expected Penalty", fontsize=10, ha="center", va="bottom")

    # Formula
    ax.text(
        6,
        3,
        r"Expected Penalty = $p_{detect} \times \text{penalty\_max} \times \text{enforcement\_strength}$",
        fontsize=11,
        ha="center",
        va="center",
        family="monospace",
        bbox=dict(boxstyle="round", facecolor=COLORS["yellow"], alpha=0.3),
    )

    # Complaint rate
    ax.text(
        6,
        2,
        r"Complaint Rate: 0.02 (95% CI: 0.01-0.03)",
        fontsize=10,
        ha="center",
        va="center",
        style="italic",
    )

    save_figure(fig, output_dir / "enforcement_compliance", dpi, formats)


def generate_equilibrium_concepts_diagram(output_dir: Path, dpi: int, formats: list):
    """Generate comprehensive equilibrium concepts diagram."""
    print("Generating Equilibrium Concepts diagram...")

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Equilibrium Concepts Across Games", fontsize=16, fontweight="bold")

    # Module A: Nash Equilibrium
    ax = axes[0, 0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_title("Module A: Nash Equilibrium", fontsize=12, fontweight="bold")

    # Best response curves
    x = np.linspace(0, 10, 100)
    br1 = 8 - 0.6 * x  # Individual BR
    br2 = 6 - 0.4 * x  # Insurer BR

    ax.plot(x, br1, "-", color=COLORS["blue"], linewidth=2, label="Individual BR")
    ax.plot(x, br2, "--", color=COLORS["vermilion"], linewidth=2, label="Insurer BR")
    ax.fill_between(x, 0, br1, alpha=0.2, color=COLORS["blue"])
    ax.fill_between(x, 0, br2, alpha=0.2, color=COLORS["vermilion"])

    # Equilibrium point
    eq_x, eq_y = 5, 5
    ax.plot(eq_x, eq_y, "o", color=COLORS["black"], markersize=12, label="Nash Equilibrium")
    ax.annotate(
        f"NE\n({eq_x:.1f}, {eq_y:.1f})",
        xy=(eq_x, eq_y),
        xytext=(eq_x + 0.5, eq_y + 0.5),
        fontsize=10,
        fontweight="bold",
    )

    ax.set_xlabel("Testing Uptake", fontsize=10)
    ax.set_ylabel("Premium Level", fontsize=10)
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(True, alpha=0.3)

    # Module C: Separating vs Pooling
    ax = axes[0, 1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_title("Module C: Separating vs Pooling Equilibrium", fontsize=12, fontweight="bold")

    # Separating equilibrium
    sep_rect = patches.Rectangle(
        (1, 5.5),
        3.5,
        3,
        linewidth=2,
        edgecolor=COLORS["bluish_green"],
        facecolor=COLORS["bluish_green"],
        alpha=0.2,
    )
    ax.add_patch(sep_rect)
    ax.text(
        2.75,
        7,
        "Separating",
        fontsize=11,
        fontweight="bold",
        ha="center",
        color=COLORS["bluish_green"],
    )
    ax.text(2.75, 6.3, "Full Information", fontsize=9, ha="center")
    ax.text(2.75, 5.8, "Different Premiums", fontsize=9, ha="center")

    # Pooling equilibrium
    pool_rect = patches.Rectangle(
        (5.5, 5.5),
        3.5,
        3,
        linewidth=2,
        edgecolor=COLORS["orange"],
        facecolor=COLORS["orange"],
        alpha=0.2,
    )
    ax.add_patch(pool_rect)
    ax.text(7.25, 7, "Pooling", fontsize=11, fontweight="bold", ha="center", color=COLORS["orange"])
    ax.text(7.25, 6.3, "No Information", fontsize=9, ha="center")
    ax.text(7.25, 5.8, "Same Premium", fontsize=9, ha="center")

    # Policy constraint arrow
    ax.annotate(
        "",
        xy=(7.25, 4.5),
        xytext=(2.75, 4.5),
        arrowprops=dict(arrowstyle="->", color=COLORS["black"], linewidth=2),
    )
    ax.text(5, 4.8, "Policy Constraint", fontsize=10, ha="center", va="bottom")

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_axis_off()

    # Module D: Constrained Optimization
    ax = axes[1, 0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_title("Module D: Constrained Proxy Optimization", fontsize=12, fontweight="bold")

    # Feasible region
    feasible = patches.Polygon(
        [[2, 2], [8, 2], [8, 6], [4, 8], [2, 6]],
        closed=True,
        linewidth=2,
        edgecolor=COLORS["blue"],
        facecolor=COLORS["blue"],
        alpha=0.2,
    )
    ax.add_patch(feasible)

    # Constraint boundary
    ax.plot(
        [2, 4, 8],
        [6, 8, 6],
        "--",
        color=COLORS["vermilion"],
        linewidth=2,
        label="Information Constraint",
    )

    # Optimal point
    ax.plot(6, 5, "o", color=COLORS["vermilion"], markersize=12, label="Optimal Proxy Mix")
    ax.annotate("Optimal", xy=(6, 5), xytext=(6.5, 5.5), fontsize=10, fontweight="bold")

    ax.set_xlabel("Proxy 1 Weight", fontsize=10)
    ax.set_ylabel("Proxy 2 Weight", fontsize=10)
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(True, alpha=0.3)

    # Module F: Public Good Equilibrium
    ax = axes[1, 1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_title("Module F: Public Good Participation Equilibrium", fontsize=12, fontweight="bold")

    # Participation curve
    x = np.linspace(0, 10, 100)
    participation = 8 * (1 - np.exp(-0.5 * x))  # Concave participation function
    ax.plot(
        x,
        participation,
        "-",
        color=COLORS["bluish_green"],
        linewidth=2,
        label="Participation Rate",
    )

    # Social optimum
    ax.plot(7, 6.5, "o", color=COLORS["orange"], markersize=12, label="Social Optimum")
    ax.annotate("Social Optimum", xy=(7, 6.5), xytext=(7.5, 7), fontsize=10, fontweight="bold")

    # Private equilibrium
    ax.plot(4, 4.5, "o", color=COLORS["vermilion"], markersize=12, label="Private Equilibrium")
    ax.annotate("Private NE", xy=(4, 4.5), xytext=(4.5, 5), fontsize=10, fontweight="bold")

    # Externality gap
    ax.annotate(
        "",
        xy=(7, 6.5),
        xytext=(4, 4.5),
        arrowprops=dict(arrowstyle="<->", color=COLORS["black"], linewidth=2),
    )
    ax.text(5.8, 5.7, "Externality", fontsize=10, ha="center", va="bottom", style="italic")

    ax.set_xlabel("Policy Strength", fontsize=10)
    ax.set_ylabel("Participation Rate", fontsize=10)
    ax.legend(loc="lower right", fontsize=9)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    save_figure(fig, output_dir / "equilibrium_concepts", dpi, formats)


def generate_payoff_matrices_diagram(output_dir: Path, dpi: int, formats: list):
    """Generate payoff matrices for games where applicable."""
    print("Generating Payoff Matrices diagram...")

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Payoff Matrices", fontsize=16, fontweight="bold")

    # Module A: Testing Decision Payoff Matrix
    ax = axes[0, 0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_axis_off()
    ax.set_title("Module A: Testing Decision (Simplified)", fontsize=12, fontweight="bold")

    # 2x2 matrix
    matrix_data = [
        ["Test", "No Test"],
        ["High Benefit\n-Low Penalty", "Status Quo"],
        ["Low Benefit\n-High Penalty", "No Change"],
    ]

    table = ax.table(
        cellText=matrix_data,
        colLabels=["Strategy", "Payoff"],
        cellLoc="center",
        loc="center",
        colWidths=[0.3, 0.6],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.5)

    # Color cells
    table[(0, 0)].set_facecolor(COLORS["blue"])
    table[(0, 1)].set_facecolor(COLORS["blue"])
    table[(1, 0)].set_facecolor(COLORS["bluish_green"])
    table[(1, 1)].set_facecolor(COLORS["gray"])
    table[(2, 0)].set_facecolor(COLORS["vermilion"])
    table[(2, 1)].set_facecolor(COLORS["gray"])

    # Enforcement: Compliance Payoff Matrix
    ax = axes[0, 1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_axis_off()
    ax.set_title("Enforcement: Compliance Game", fontsize=12, fontweight="bold")

    # 2x2 compliance matrix
    matrix_data = [
        ["", "Regulator: Monitor", "Regulator: Ignore"],
        ["Insurer: Comply", "0, -C", "0, 0"],
        ["Insurer: Violate", "-P, R-C", "B, -D"],
    ]

    table = ax.table(
        cellText=matrix_data,
        colLabels=["", "Monitor", "Ignore"],
        cellLoc="center",
        loc="center",
        colWidths=[0.25, 0.35, 0.35],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.5)

    # Color cells
    for i in range(3):
        table[(i, 0)].set_facecolor(COLORS["vermilion"])
        table[(i, 1)].set_facecolor(COLORS["blue"])
        table[(i, 2)].set_facecolor(COLORS["blue"])

    # Add parameter explanations
    ax.text(
        5,
        -0.5,
        "C=Monitoring Cost, P=Penalty, R=Reputation, B=Violation Benefit, D=Damage",
        fontsize=8,
        ha="center",
        va="top",
        style="italic",
    )

    # Module C: Information Regimes
    ax = axes[1, 0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_axis_off()
    ax.set_title("Module C: Information Regimes & Equilibrium Type", fontsize=12, fontweight="bold")

    regimes_data = [
        ["Regime", "Information", "Equilibrium"],
        ["Status Quo", "Full", "Separating"],
        ["Moratorium", "Partial", "Mixed"],
        ["Ban", "None", "Pooling"],
    ]

    table = ax.table(
        cellText=regimes_data,
        colLabels=["Policy", "Available", "Type"],
        cellLoc="center",
        loc="center",
        colWidths=[0.3, 0.3, 0.3],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.5)

    # Color by regime
    table[(0, 0)].set_facecolor(COLORS["blue"])
    table[(0, 1)].set_facecolor(COLORS["blue"])
    table[(0, 2)].set_facecolor(COLORS["blue"])
    table[(1, 0)].set_facecolor(COLORS["orange"])
    table[(1, 1)].set_facecolor(COLORS["orange"])
    table[(1, 2)].set_facecolor(COLORS["orange"])
    table[(2, 0)].set_facecolor(COLORS["vermilion"])
    table[(2, 1)].set_facecolor(COLORS["vermilion"])
    table[(2, 2)].set_facecolor(COLORS["vermilion"])

    # Module D: Proxy Accuracy
    ax = axes[1, 1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_axis_off()
    ax.set_title("Module D: Proxy Substitution Accuracy", fontsize=12, fontweight="bold")

    # ROC-style curve
    x = np.linspace(0, 1, 100)
    tpr = 0.68 + 0.25 * (1 - np.exp(-3 * x))  # Sensitivity curve
    fpr = x

    ax.plot(fpr, tpr, "-", color=COLORS["blue"], linewidth=2, label=f"Proxy ROC (AUC={0.72:.2f})")
    ax.plot([0, 1], [0, 1], "--", color=COLORS["gray"], linewidth=1, label="Random")

    # Operating point
    ax.plot(0.25, 0.68, "o", color=COLORS["vermilion"], markersize=12, label="Operating Point")
    ax.annotate(
        f"Sensitivity: 0.68\nSpecificity: {1 - 0.25:.2f}",
        xy=(0.25, 0.68),
        xytext=(0.35, 0.55),
        fontsize=9,
        arrowprops=dict(arrowstyle="->", color=COLORS["black"]),
    )

    ax.set_xlabel("False Positive Rate (1-Specificity)", fontsize=10)
    ax.set_ylabel("True Positive Rate (Sensitivity)", fontsize=10)
    ax.legend(loc="lower right", fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    plt.tight_layout()
    save_figure(fig, output_dir / "payoff_matrices", dpi, formats)


def main():
    parser = argparse.ArgumentParser(description="Generate game structure diagrams")
    parser.add_argument(
        "--output",
        type=str,
        default="outputs/figures/games",
        help="Output directory for diagrams",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=1200,
        help="Resolution for PNG output (default: 1200)",
    )
    parser.add_argument(
        "--formats",
        type=str,
        nargs="+",
        default=["png", "svg"],
        help="Output formats (default: png svg)",
    )

    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("GAME STRUCTURE DIAGRAM GENERATION")
    print("=" * 60)

    # Generate all diagrams
    generate_module_a_diagram(output_dir, args.dpi, args.formats)
    generate_module_c_diagram(output_dir, args.dpi, args.formats)
    generate_module_d_diagram(output_dir, args.dpi, args.formats)
    generate_module_e_diagram(output_dir, args.dpi, args.formats)
    generate_module_f_diagram(output_dir, args.dpi, args.formats)
    generate_enforcement_diagram(output_dir, args.dpi, args.formats)
    generate_equilibrium_concepts_diagram(output_dir, args.dpi, args.formats)
    generate_payoff_matrices_diagram(output_dir, args.dpi, args.formats)

    print("=" * 60)
    print(f"✓ All 8 game diagrams generated in {output_dir}")
    print("  - 6 game structure diagrams")
    print("  - 1 equilibrium concepts diagram")
    print("  - 1 payoff matrices diagram")
    print("=" * 60)


if __name__ == "__main__":
    main()
