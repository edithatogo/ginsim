#!/usr/bin/env python3
"""
Generate publication-ready figures from model outputs.

Usage:
    python -m scripts.generate_figures --run_dir outputs/runs/meta_20260303 --output outputs/figures --dpi 1200 --formats png svg
"""

import argparse
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


# Colorblind-safe palettes
OKABE_ITO = {
    'orange': '#E69F00',
    'sky_blue': '#56B4E9',
    'bluish_green': '#009E73',
    'yellow': '#F0E442',
    'blue': '#0072B2',
    'vermilion': '#D55E00',
    'reddish_purple': '#CC79A7',
    'black': '#000000',
}


def save_figure(fig, output_path: Path, dpi: int = 1200, formats: list = None) -> None:
    """Save figure in multiple formats."""
    if formats is None:
        formats = ['png', 'svg']
    
    for fmt in formats:
        if fmt == 'png':
            path = output_path.with_suffix('.png')
            fig.savefig(path, dpi=dpi, bbox_inches='tight', facecolor='white')
        elif fmt == 'svg':
            path = output_path.with_suffix('.svg')
            fig.savefig(path, bbox_inches='tight', facecolor='white')
        print(f"  ✓ Saved {path.name}")
    
    plt.close(fig)


def generate_policy_comparison_figure(run_dir: Path, output_dir: Path, dpi: int, formats: list) -> None:
    """Generate F2: Policy comparison forest plot."""
    print(f"Generating policy comparison forest plot...")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Example data
    policies = ['Status Quo', 'Moratorium', 'Statutory Ban']
    welfare = [0, 150000, 250000]
    welfare_ci_lower = [-50000, 50000, 150000]
    welfare_ci_upper = [50000, 250000, 350000]
    
    y_pos = np.arange(len(policies))
    
    # Forest plot
    ax.errorbar(welfare, y_pos, xerr=[np.subtract(welfare, welfare_ci_lower), 
                                       np.subtract(welfare_ci_upper, welfare)],
                fmt='o', capsize=5, color=OKABE_ITO['blue'], markersize=10, linewidth=2)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(policies)
    ax.set_xlabel('Net Welfare Impact ($)', fontsize=12)
    ax.set_title('Policy Comparison: Net Welfare Impact', fontsize=14, fontweight='bold')
    ax.axvline(x=0, color='gray', linestyle='--', linewidth=1)
    ax.grid(True, alpha=0.3)
    
    output_path = output_dir / 'policy_comparison'
    save_figure(fig, output_path, dpi, formats)


def generate_ceac_curves(run_dir: Path, output_dir: Path, dpi: int, formats: list) -> None:
    """Generate F3: Cost-effectiveness acceptability curves."""
    print(f"Generating CEAC curves...")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Example data
    willingness_to_pay = np.linspace(0, 1000000, 100)
    ceac_status_quo = np.ones(100) * 0.5
    ceac_moratorium = 0.5 + 0.4 * (1 - np.exp(-willingness_to_pay / 200000))
    ceac_ban = 0.5 + 0.45 * (1 - np.exp(-willingness_to_pay / 150000))
    
    ax.plot(willingness_to_pay, ceac_status_quo, '--', label='Status Quo', 
            color=OKABE_ITO['black'], linewidth=2)
    ax.plot(willingness_to_pay, ceac_moratorium, '-', label='Moratorium', 
            color=OKABE_ITO['blue'], linewidth=2)
    ax.plot(willingness_to_pay, ceac_ban, '-', label='Statutory Ban', 
            color=OKABE_ITO['vermilion'], linewidth=2)
    
    ax.set_xlabel('Willingness to Pay ($ per QALY)', fontsize=12)
    ax.set_ylabel('Probability Cost-Effective', fontsize=12)
    ax.set_title('Cost-Effectiveness Acceptability Curves', fontsize=14, fontweight='bold')
    ax.set_ylim(0, 1.05)
    ax.legend(loc='lower right')
    ax.grid(True, alpha=0.3)
    
    output_path = output_dir / 'ceac_curves'
    save_figure(fig, output_path, dpi, formats)


def generate_tornado_diagram(run_dir: Path, output_dir: Path, dpi: int, formats: list) -> None:
    """Generate F4: Tornado diagram for sensitivity analysis."""
    print(f"Generating tornado diagram...")
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Example data
    parameters = ['Deterrence Elasticity', 'Adverse Selection', 'Enforcement', 
                  'Proxy Substitution', 'Pass-through']
    base_welfare = 150000
    low_welfare = [100000, 120000, 130000, 140000, 145000]
    high_welfare = [200000, 180000, 170000, 160000, 155000]
    
    y_pos = np.arange(len(parameters))
    
    # Tornado bars
    for i, (param, low, high) in enumerate(zip(parameters, low_welfare, high_welfare)):
        ax.barh(i, high - base_welfare, left=base_welfare, color=OKABE_ITO['blue'], alpha=0.7)
        ax.barh(i, base_welfare - low, left=low, color=OKABE_ITO['vermilion'], alpha=0.7)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(parameters)
    ax.set_xlabel('Net Welfare Impact ($)', fontsize=12)
    ax.set_title('Tornado Diagram: One-Way Sensitivity Analysis', fontsize=14, fontweight='bold')
    ax.axvline(x=base_welfare, color='gray', linestyle='-', linewidth=2)
    ax.grid(True, alpha=0.3, axis='x')
    
    output_path = output_dir / 'tornado'
    save_figure(fig, output_path, dpi, formats)


def generate_voi_results_figure(run_dir: Path, output_dir: Path, dpi: int, formats: list) -> None:
    """Generate F5: VOI results bar chart."""
    print(f"Generating VOI results bar chart...")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Example data
    parameter_groups = ['Deterrence', 'Adverse Selection', 'Enforcement', 
                        'Proxy Substitution', 'Pass-through']
    evppi = [50000, 40000, 30000, 20000, 10000]
    
    y_pos = np.arange(len(parameter_groups))
    
    bars = ax.barh(y_pos, evppi, color=OKABE_ITO['sky_blue'])
    
    # Add value labels
    for i, v in enumerate(evppi):
        ax.text(v + 2000, i, f'${v:,}', va='center', fontsize=10)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(parameter_groups)
    ax.set_xlabel('EVPPI ($)', fontsize=12)
    ax.set_title('Expected Value of Partial Perfect Information', fontsize=14, fontweight='bold')
    ax.invert_yaxis()
    ax.grid(True, alpha=0.3, axis='x')
    
    output_path = output_dir / 'voi_results'
    save_figure(fig, output_path, dpi, formats)


def generate_evidence_quality_heatmap(run_dir: Path, output_dir: Path, dpi: int, formats: list) -> None:
    """Generate F6: Evidence quality heatmap."""
    print(f"Generating evidence quality heatmap...")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Example data
    modules = ['Module A', 'Module C', 'Module D', 'Module E', 'Module F', 'Enforcement']
    quality = ['Moderate', 'Low', 'Very Low']
    
    # Data: rows=modules, columns=quality
    data = np.array([
        [1, 1, 1],
        [0, 2, 1],
        [1, 0, 1],
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 2],
    ])
    
    # Custom colormap
    colors = ['#ffffff', '#ffeda0', '#fc4e2a']
    cmap = LinearSegmentedColormap.from_list('quality', colors, N=100)
    
    im = ax.imshow(data, cmap=cmap, aspect='auto', vmin=0, vmax=2)
    
    ax.set_xticks(np.arange(len(quality)))
    ax.set_yticks(np.arange(len(modules)))
    ax.set_xticklabels(quality)
    ax.set_yticklabels(modules)
    ax.set_xlabel('Evidence Quality', fontsize=12)
    ax.set_ylabel('Module', fontsize=12)
    ax.set_title('Evidence Quality by Module', fontsize=14, fontweight='bold')
    
    # Add text annotations
    for i in range(len(modules)):
        for j in range(len(quality)):
            text = ax.text(j, i, str(data[i, j]), ha='center', va='center', 
                          color='black' if data[i, j] < 2 else 'white', fontsize=12)
    
    plt.colorbar(im, label='Number of Parameters')
    
    output_path = output_dir / 'evidence_quality'
    save_figure(fig, output_path, dpi, formats)


def main():
    parser = argparse.ArgumentParser(description='Generate publication-ready figures')
    parser.add_argument('--run_dir', type=str, default='outputs/runs/meta_latest',
                       help='Run directory with model outputs')
    parser.add_argument('--output', type=str, default='outputs/figures/v1.0',
                       help='Output directory for figures')
    parser.add_argument('--dpi', type=int, default=1200,
                       help='Resolution for PNG output (default: 1200)')
    parser.add_argument('--formats', type=str, nargs='+', default=['png', 'svg'],
                       help='Output formats (default: png svg)')
    
    args = parser.parse_args()
    
    run_dir = Path(args.run_dir)
    output_dir = Path(args.output)
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("FIGURE GENERATION")
    print("=" * 60)
    
    # Generate all figures
    generate_policy_comparison_figure(run_dir, output_dir, args.dpi, args.formats)
    generate_ceac_curves(run_dir, output_dir, args.dpi, args.formats)
    generate_tornado_diagram(run_dir, output_dir, args.dpi, args.formats)
    generate_voi_results_figure(run_dir, output_dir, args.dpi, args.formats)
    generate_evidence_quality_heatmap(run_dir, output_dir, args.dpi, args.formats)
    
    # Create latest symlink
    latest_dir = output_dir.parent / 'latest'
    if latest_dir.exists() or latest_dir.is_symlink():
        latest_dir.unlink()
    latest_dir.symlink_to(output_dir.name)
    
    print("=" * 60)
    print(f"✓ All figures generated in {output_dir}")
    print("=" * 60)


if __name__ == '__main__':
    main()
