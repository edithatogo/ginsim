#!/usr/bin/env python3
"""
Generate game structure diagrams for all 6 game-theoretic modules.

Usage:
    python -m scripts.generate_game_diagrams --output outputs/figures/games --formats png svg
"""

import argparse
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Colorblind-safe palette (Okabe-Ito)
COLORS = {
    'orange': '#E69F00',
    'sky_blue': '#56B4E9',
    'bluish_green': '#009E73',
    'yellow': '#F0E442',
    'blue': '#0072B2',
    'vermilion': '#D55E00',
    'reddish_purple': '#CC79A7',
    'black': '#000000',
    'gray': '#999999',
}


def save_figure(fig, output_path: Path, dpi: int = 1200, formats: list = None):
    """Save figure in multiple formats."""
    if formats is None:
        formats = ['png', 'svg']
    
    for fmt in formats:
        if fmt == 'png':
            path = output_path.with_suffix('.png')
            fig.savefig(path, dpi=dpi, bbox_inches='tight', facecolor='white')
            print(f"  ✓ Saved {path.name} ({dpi}dpi)")
        elif fmt == 'svg':
            path = output_path.with_suffix('.svg')
            fig.savefig(path, bbox_inches='tight', facecolor='white')
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
    ax.text(6, 9.5, 'Module A: Behavior/Deterrence Game', 
            fontsize=16, fontweight='bold', ha='center', va='top')
    
    # Players
    players = [
        (1, 7, 'Individuals', COLORS['blue'], 'Testing decision'),
        (6, 7, 'Insurers', COLORS['vermilion'], 'Premium setting'),
        (11, 7, 'Policymakers', COLORS['bluish_green'], 'Policy regime'),
    ]
    
    for x, y, name, color, role in players:
        rect = patches.Rectangle((x-1.2, y-0.8), 2.4, 1.6, linewidth=2, 
                                  edgecolor=color, facecolor=color, alpha=0.2)
        ax.add_patch(rect)
        ax.text(x, y, name, fontsize=12, fontweight='bold', ha='center', va='center', color=color)
        ax.text(x, y-0.5, role, fontsize=9, ha='center', va='center', style='italic')
    
    # Game sequence arrows
    arrow_props = dict(arrowstyle='->', color=COLORS['black'], linewidth=2)
    
    # Policy → Individual
    ax.annotate('', xy=(10, 7), xytext=(2, 7),
                arrowprops=dict(arrowstyle='->', color=COLORS['bluish_green'], linewidth=2.5))
    ax.text(6, 7.3, '1. Sets policy regime', fontsize=10, ha='center', va='bottom')
    
    # Individual → Insurer
    ax.annotate('', xy=(5, 7), xytext=(3, 7),
                arrowprops=dict(arrowstyle='->', color=COLORS['blue'], linewidth=2.5))
    ax.text(4, 6.6, '2. Testing decision', fontsize=10, ha='center', va='top')
    
    # Insurer → Payoffs
    ax.annotate('', xy=(8, 7), xytext=(7, 7),
                arrowprops=dict(arrowstyle='->', color=COLORS['vermilion'], linewidth=2.5))
    ax.text(7.5, 7.3, '3. Sets premiums', fontsize=10, ha='center', va='bottom')
    
    # Equilibrium box
    rect = patches.Rectangle((4, 2.5), 4, 3, linewidth=2, edgecolor=COLORS['black'], 
                              facecolor='white', linestyle='--')
    ax.add_patch(rect)
    ax.text(6, 4.5, 'Equilibrium:\nTesting uptake = f(policy, penalty)', 
            fontsize=11, ha='center', va='center')
    
    # Utility function
    ax.text(6, 1.5, r'$U_i = \text{health\_benefit} - \text{perceived\_penalty}(\text{policy})$',
            fontsize=12, ha='center', va='center', family='monospace')
    
    save_figure(fig, output_dir / 'module_a_behavior', dpi, formats)


def generate_module_c_diagram(output_dir: Path, dpi: int, formats: list):
    """Generate Module C: Insurance Equilibrium (Rothschild-Stiglitz) diagram."""
    print("Generating Module C: Insurance Equilibrium diagram...")
    
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.set_axis_off()
    
    # Title
    ax.text(6, 9.5, 'Module C: Insurance Equilibrium (Rothschild-Stiglitz)', 
            fontsize=16, fontweight='bold', ha='center', va='top')
    
    # Information asymmetry
    ax.text(6, 8.5, 'Information Asymmetry: Applicants know risk, Insurers don\'t',
            fontsize=11, ha='center', va='center', style='italic',
            bbox=dict(boxstyle='round', facecolor=COLORS['yellow'], alpha=0.3))
    
    # Players
    applicants_box = patches.Rectangle((1, 5.5), 4, 2, linewidth=2, 
                                        edgecolor=COLORS['blue'], facecolor=COLORS['blue'], alpha=0.2)
    ax.add_patch(applicants_box)
    ax.text(3, 6.5, 'Applicants\n(Informed)', fontsize=12, fontweight='bold', 
            ha='center', va='center', color=COLORS['blue'])
    
    insurer_box = patches.Rectangle((7, 5.5), 4, 2, linewidth=2, 
                                     edgecolor=COLORS['vermilion'], facecolor=COLORS['vermilion'], alpha=0.2)
    ax.add_patch(insurer_box)
    ax.text(9, 6.5, 'Insurers\n(Uninformed)', fontsize=12, fontweight='bold', 
            ha='center', va='center', color=COLORS['vermilion'])
    
    # Equilibrium types
    sep_box = patches.Rectangle((2, 2.5), 3.5, 2, linewidth=2, edgecolor=COLORS['bluish_green'],
                                 facecolor='white', linestyle='-')
    ax.add_patch(sep_box)
    ax.text(3.75, 3.5, 'Separating\nEquilibrium\n(Different premiums)', 
            fontsize=10, ha='center', va='center')
    
    pool_box = patches.Rectangle((6.5, 2.5), 3.5, 2, linewidth=2, edgecolor=COLORS['orange'],
                                  facecolor='white', linestyle='-')
    ax.add_patch(pool_box)
    ax.text(8.25, 3.5, 'Pooling\nEquilibrium\n(Same premium)', 
            fontsize=10, ha='center', va='center')
    
    # Policy constraint
    ax.text(6, 1, 'Policy Constraint:\nMoratorium/Ban restricts information use',
            fontsize=10, ha='center', va='center',
            bbox=dict(boxstyle='round', facecolor=COLORS['gray'], alpha=0.2))
    
    save_figure(fig, output_dir / 'module_c_insurance_eq', dpi, formats)


def generate_module_d_diagram(output_dir: Path, dpi: int, formats: list):
    """Generate Module D: Proxy Substitution diagram."""
    print("Generating Module D: Proxy Substitution diagram...")
    
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.set_axis_off()
    
    # Title
    ax.text(6, 9.5, 'Module D: Proxy Substitution Game', 
            fontsize=16, fontweight='bold', ha='center', va='top')
    
    # Constraint box
    constraint = patches.Rectangle((1, 7), 10, 1.5, linewidth=2, edgecolor=COLORS['vermilion'],
                                    facecolor=COLORS['vermilion'], alpha=0.1, linestyle='--')
    ax.add_patch(constraint)
    ax.text(6, 7.75, 'Constraint: Cannot use genetic test results directly',
            fontsize=11, ha='center', va='center', color=COLORS['vermilion'], fontweight='bold')
    
    # Proxies
    proxies = ['Family History', 'Age', 'Gender', 'Lifestyle', 'Medical History']
    for i, proxy in enumerate(proxies):
        x = 1.5 + i * 2
        rect = patches.Rectangle((x-0.8, 5), 1.6, 1.2, linewidth=2, 
                                  edgecolor=COLORS['sky_blue'], facecolor=COLORS['sky_blue'], alpha=0.3)
        ax.add_patch(rect)
        ax.text(x, 5.6, proxy, fontsize=9, ha='center', va='center', rotation=45)
    
    # Arrow to risk score
    ax.annotate('', xy=(10, 5.6), xytext=(9.5, 5.6),
                arrowprops=dict(arrowstyle='->', color=COLORS['black'], linewidth=2))
    
    # Risk score
    risk_box = patches.Rectangle((9, 4.5), 2.5, 2, linewidth=2, 
                                  edgecolor=COLORS['blue'], facecolor=COLORS['blue'], alpha=0.2)
    ax.add_patch(risk_box)
    ax.text(10.25, 5.5, 'Risk Score', fontsize=11, fontweight='bold', 
            ha='center', va='center', color=COLORS['blue'])
    
    # Formula
    ax.text(10.25, 4.8, r'$\sum w_i \cdot x_i$', fontsize=14, 
            ha='center', va='center', family='monospace')
    
    # Accuracy metrics
    ax.text(6, 2.5, 'Accuracy Metrics:\nSensitivity: 0.68\nSpecificity: 0.75',
            fontsize=10, ha='center', va='center',
            bbox=dict(boxstyle='round', facecolor=COLORS['yellow'], alpha=0.3))
    
    save_figure(fig, output_dir / 'module_d_proxy', dpi, formats)


def generate_module_e_diagram(output_dir: Path, dpi: int, formats: list):
    """Generate Module E: Pass-Through diagram."""
    print("Generating Module E: Pass-Through diagram...")
    
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.set_axis_off()
    
    # Title
    ax.text(6, 9.5, 'Module E: Pass-Through / Market Structure Game', 
            fontsize=16, fontweight='bold', ha='center', va='top')
    
    # Market structure spectrum
    ax.text(6, 8.5, 'Market Structure → Pass-Through Rate',
            fontsize=12, ha='center', va='center', fontweight='bold')
    
    # Spectrum
    structures = [
        (2, 'Monopoly', 'Low\n(30-50%)', COLORS['vermilion']),
        (6, 'Oligopoly', 'Medium\n(50-70%)', COLORS['orange']),
        (10, 'Competitive', 'High\n(70-90%)', COLORS['bluish_green']),
    ]
    
    for x, structure, rate, color in structures:
        rect = patches.Rectangle((x-1.5, 5.5), 3, 2.5, linewidth=2, 
                                  edgecolor=color, facecolor=color, alpha=0.2)
        ax.add_patch(rect)
        ax.text(x, 6.5, structure, fontsize=11, fontweight='bold', 
                ha='center', va='center', color=color)
        ax.text(x, 5.8, rate, fontsize=10, ha='center', va='center')
    
    # Pass-through formula
    ax.text(6, 3.5, r'Pass-Through Rate: $\tau \in [0.3, 0.9]$',
            fontsize=13, ha='center', va='center', family='monospace',
            bbox=dict(boxstyle='round', facecolor=COLORS['yellow'], alpha=0.3))
    
    ax.text(6, 2.5, r'Premium Change = $\tau \times$ Cost Shock',
            fontsize=12, ha='center', va='center', family='monospace')
    
    save_figure(fig, output_dir / 'module_e_passthrough', dpi, formats)


def generate_module_f_diagram(output_dir: Path, dpi: int, formats: list):
    """Generate Module F: Data Quality Externality diagram."""
    print("Generating Module F: Data Quality Externality diagram...")
    
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.set_axis_off()
    
    # Title
    ax.text(6, 9.5, 'Module F: Data Quality Externality Game', 
            fontsize=16, fontweight='bold', ha='center', va='top')
    
    # Public good structure
    ax.text(6, 8.5, 'Participation as Public Good',
            fontsize=12, ha='center', va='center', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor=COLORS['bluish_green'], alpha=0.2))
    
    # Players
    individuals = patches.Circle((3, 5.5), 1.5, linewidth=2, 
                                  edgecolor=COLORS['blue'], facecolor=COLORS['blue'], alpha=0.2)
    ax.add_patch(individuals)
    ax.text(3, 5.5, 'Individuals\n(Privacy cost\nvs. Social benefit)',
            fontsize=9, ha='center', va='center', color=COLORS['blue'])
    
    researchers = patches.Circle((9, 5.5), 1.5, linewidth=2, 
                                  edgecolor=COLORS['vermilion'], facecolor=COLORS['vermilion'], alpha=0.2)
    ax.add_patch(researchers)
    ax.text(9, 5.5, 'Researchers\n(Data quality\n→ Research value)',
            fontsize=9, ha='center', va='center', color=COLORS['vermilion'])
    
    # Externality arrow
    ax.annotate('', xy=(7.5, 5.5), xytext=(4.5, 5.5),
                arrowprops=dict(arrowstyle='->', color=COLORS['bluish_green'], linewidth=3))
    ax.text(6, 5.8, 'Positive Externality', fontsize=10, ha='center', va='bottom',
            color=COLORS['bluish_green'], fontweight='bold')
    
    # Participation function
    ax.text(6, 3, r'Participation Rate: $p = f(\text{policy}, \text{privacy\_concern})$',
            fontsize=12, ha='center', va='center', family='monospace',
            bbox=dict(boxstyle='round', facecolor=COLORS['yellow'], alpha=0.3))
    
    ax.text(6, 2, r'Elasticity: -0.10 (negative policy effect)',
            fontsize=10, ha='center', va='center', style='italic')
    
    save_figure(fig, output_dir / 'module_f_data_quality', dpi, formats)


def generate_enforcement_diagram(output_dir: Path, dpi: int, formats: list):
    """Generate Enforcement: Compliance Game diagram."""
    print("Generating Enforcement: Compliance Game diagram...")
    
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.set_axis_off()
    
    # Title
    ax.text(6, 9.5, 'Enforcement: Compliance Game', 
            fontsize=16, fontweight='bold', ha='center', va='top')
    
    # Mixed strategy
    ax.text(6, 8.5, 'Mixed Strategy Nash Equilibrium',
            fontsize=12, ha='center', va='center', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor=COLORS['orange'], alpha=0.2))
    
    # Insurer decision
    insurer_box = patches.Rectangle((1, 5), 4, 3, linewidth=2, 
                                     edgecolor=COLORS['vermilion'], facecolor=COLORS['vermilion'], alpha=0.2)
    ax.add_patch(insurer_box)
    ax.text(3, 6.5, 'Insurers', fontsize=12, fontweight='bold', 
            ha='center', va='center', color=COLORS['vermilion'])
    ax.text(3, 5.8, 'Strategy:\nComply vs. Violate', fontsize=9, 
            ha='center', va='center')
    
    # Regulator decision
    regulator_box = patches.Rectangle((7, 5), 4, 3, linewidth=2, 
                                       edgecolor=COLORS['blue'], facecolor=COLORS['blue'], alpha=0.2)
    ax.add_patch(regulator_box)
    ax.text(9, 6.5, 'Regulator', fontsize=12, fontweight='bold', 
            ha='center', va='center', color=COLORS['blue'])
    ax.text(9, 5.8, 'Strategy:\nMonitor vs. Ignore', fontsize=9, 
            ha='center', va='center')
    
    # Expected penalty
    ax.annotate('', xy=(7, 6.5), xytext=(5, 6.5),
                arrowprops=dict(arrowstyle='->', color=COLORS['black'], linewidth=2))
    
    ax.text(6, 7, 'Expected Penalty', fontsize=10, ha='center', va='bottom')
    
    # Formula
    ax.text(6, 3, r'Expected Penalty = $p_{detect} \times \text{penalty\_max} \times \text{enforcement\_strength}$',
            fontsize=11, ha='center', va='center', family='monospace',
            bbox=dict(boxstyle='round', facecolor=COLORS['yellow'], alpha=0.3))
    
    # Complaint rate
    ax.text(6, 2, r'Complaint Rate: 0.02 (95% CI: 0.01-0.03)',
            fontsize=10, ha='center', va='center', style='italic')
    
    save_figure(fig, output_dir / 'enforcement_compliance', dpi, formats)


def main():
    parser = argparse.ArgumentParser(description='Generate game structure diagrams')
    parser.add_argument('--output', type=str, default='outputs/figures/games',
                       help='Output directory for diagrams')
    parser.add_argument('--dpi', type=int, default=1200,
                       help='Resolution for PNG output (default: 1200)')
    parser.add_argument('--formats', type=str, nargs='+', default=['png', 'svg'],
                       help='Output formats (default: png svg)')
    
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
    
    print("=" * 60)
    print(f"✓ All 6 game structure diagrams generated in {output_dir}")
    print("=" * 60)


if __name__ == '__main__':
    main()
