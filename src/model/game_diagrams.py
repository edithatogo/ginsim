#!/usr/bin/env python3
"""
Game diagram generation functions.

Creates visual representations of the 6 game-theoretic modules:
- Module A: Behavior/Deterrence
- Module C: Insurance Equilibrium
- Module D: Proxy Substitution
- Module E: Pass-Through
- Module F: Data Quality
- Enforcement: Compliance
"""

from __future__ import annotations

from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import Rectangle, Circle, ArrowStyle
from matplotlib.lines import Line2D


@dataclass
class DiagramConfig:
    """Configuration for diagram styling."""
    figsize: Tuple[int, int] = (10, 8)
    dpi: int = 150
    font_size: int = 10
    node_color: str = '#3498db'
    node_edge_color: str = '#2c3e50'
    edge_color: str = '#7f8c8d'
    highlight_color: str = '#e74c3c'
    success_color: str = '#2ecc71'
    warning_color: str = '#f39c12'
    background_color: str = '#ecf0f1'


def create_module_a_diagram(
    params: Optional[Dict[str, float]] = None,
    config: Optional[DiagramConfig] = None,
    save_path: Optional[Path] = None,
) -> plt.Figure:
    """
    Create Module A: Behavior/Deterrence game diagram.
    
    Shows the decision tree for genetic testing participation based on
    perceived discrimination risk and policy regime.
    
    Args:
        params: Optional parameters to visualize (baseline_uptake, deterrence_elasticity)
        config: Diagram configuration
        save_path: Optional path to save figure
        
    Returns:
        Matplotlib figure object
    """
    if config is None:
        config = DiagramConfig()
    
    fig, ax = plt.subplots(figsize=config.figsize, dpi=config.dpi)
    ax.set_facecolor(config.background_color)
    
    # Title
    ax.set_title(
        "Module A: Behavior / Deterrence Game",
        fontsize=14, fontweight='bold', pad=20
    )
    
    # Create decision tree structure
    # Nodes: Individual → Information Set → Decision → Outcome
    
    # Position definitions
    start_x, start_y = 1, 4
    info_x, info_y = 4, 4
    decision_x, decision_y = 7, 4
    outcome_test_x, outcome_test_y = 10, 5.5
    outcome_no_test_x, outcome_no_test_y = 10, 2.5
    
    # Draw nodes
    # Start node (Individual)
    start_circle = Circle((start_x, start_y), 0.4, fill=True, 
                          color=config.node_color, ec=config.node_edge_color, lw=2)
    ax.add_patch(start_circle)
    ax.text(start_x, start_y, "Individual\nDecides", ha='center', va='center', 
            fontsize=config.font_size, fontweight='bold', color='white')
    
    # Information set (Perceived Risk)
    info_rect = Rectangle((info_x - 0.6, info_y - 0.5), 1.2, 1.0, 
                          fill=True, color=config.warning_color, ec=config.node_edge_color, lw=2)
    ax.add_patch(info_rect)
    ax.text(info_x, info_y, "Perceived\nDiscrimination\nRisk", ha='center', va='center',
            fontsize=config.font_size - 1, fontweight='bold')
    
    # Decision node
    decision_circle = Circle((decision_x, decision_y), 0.4, fill=True,
                             color=config.node_color, ec=config.node_edge_color, lw=2)
    ax.add_patch(decision_circle)
    ax.text(decision_x, decision_y, "Test?\nDecision", ha='center', va='center',
            fontsize=config.font_size, fontweight='bold', color='white')
    
    # Outcome: Test
    test_rect = Rectangle((outcome_test_x - 0.7, outcome_test_y - 0.5), 1.4, 1.0,
                          fill=True, color=config.success_color, ec=config.node_edge_color, lw=2)
    ax.add_patch(test_rect)
    ax.text(outcome_test_x, outcome_test_y, "Take Test\n✓", ha='center', va='center',
            fontsize=config.font_size, fontweight='bold')
    
    # Outcome: No Test
    no_test_rect = Rectangle((outcome_no_test_x - 0.7, outcome_no_test_y - 0.5), 1.4, 1.0,
                             fill=True, color=config.highlight_color, ec=config.node_edge_color, lw=2)
    ax.add_patch(no_test_rect)
    ax.text(outcome_no_test_x, outcome_no_test_y, "Decline Test\n✗", ha='center', va='center',
            fontsize=config.font_size, fontweight='bold')
    
    # Draw edges (arrows)
    ax.annotate("", xy=(info_x - 0.6, info_y), xytext=(start_x + 0.4, start_y),
                arrowprops=dict(arrowstyle='->', color=config.node_edge_color, lw=2))
    
    ax.annotate("", xy=(decision_x - 0.4, decision_y), xytext=(info_x + 0.6, info_y),
                arrowprops=dict(arrowstyle='->', color=config.node_edge_color, lw=2))
    
    ax.annotate("", xy=(outcome_test_x - 0.7, outcome_test_y), 
                xytext=(decision_x + 0.4, decision_y + 0.3),
                arrowprops=dict(arrowstyle='->', color=config.success_color, lw=2))
    ax.text(8.5, 5.2, "If perceived risk low", fontsize=config.font_size - 1, 
            style='italic', color=config.success_color)
    
    ax.annotate("", xy=(outcome_no_test_x - 0.7, outcome_no_test_y),
                xytext=(decision_x + 0.4, decision_y - 0.3),
                arrowprops=dict(arrowstyle='->', color=config.highlight_color, lw=2))
    ax.text(8.5, 3.0, "If perceived risk high", fontsize=config.font_size - 1,
            style='italic', color=config.highlight_color)
    
    # Policy influence arrow
    ax.annotate("", xy=(decision_x, decision_y + 1.5), xytext=(decision_x, decision_y + 0.5),
                arrowprops=dict(arrowstyle='->', color=config.highlight_color, lw=3,
                               linestyle='--'))
    ax.text(decision_x, decision_y + 1.8, "Policy Regime\n(Ban/Moratorium)",
            ha='center', va='bottom', fontsize=config.font_size - 1,
            color=config.highlight_color, fontweight='bold')
    
    # Add parameters if provided
    if params:
        param_text = "Parameters:\n"
        for key, value in params.items():
            param_text += f"  {key}: {value:.3f}\n"
        ax.text(0.05, 0.95, param_text, transform=ax.transAxes,
                fontsize=config.font_size - 2, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Set limits
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=config.dpi, bbox_inches='tight')
    
    return fig


def create_module_c_diagram(
    params: Optional[Dict[str, float]] = None,
    config: Optional[DiagramConfig] = None,
    save_path: Optional[Path] = None,
) -> plt.Figure:
    """
    Create Module C: Insurance Equilibrium diagram.
    
    Shows the separating vs pooling equilibrium in insurance markets
    under asymmetric information.
    
    Args:
        params: Optional parameters (risk_premium_high, risk_premium_low)
        config: Diagram configuration
        save_path: Optional path to save figure
        
    Returns:
        Matplotlib figure object
    """
    if config is None:
        config = DiagramConfig()
    
    fig, ax = plt.subplots(figsize=config.figsize, dpi=config.dpi)
    ax.set_facecolor(config.background_color)
    
    ax.set_title(
        "Module C: Insurance Equilibrium (Asymmetric Information)",
        fontsize=14, fontweight='bold', pad=20
    )
    
    # Create equilibrium diagram
    # Two pools: High Risk and Low Risk individuals
    
    # High risk pool
    high_risk_x, high_risk_y = 3, 5
    high_risk_rect = Rectangle((high_risk_x - 1.5, high_risk_y - 1.5), 3, 3,
                                fill=True, color=config.highlight_color, 
                                ec=config.node_edge_color, lw=2, alpha=0.7)
    ax.add_patch(high_risk_rect)
    ax.text(high_risk_x, high_risk_y + 1.8, "High Risk Individuals",
            ha='center', va='bottom', fontsize=config.font_size, fontweight='bold',
            color=config.highlight_color)
    ax.text(high_risk_x, high_risk_y, "Premium:\n$P_H", ha='center', va='center',
            fontsize=config.font_size + 2, fontweight='bold')
    
    # Low risk pool
    low_risk_x, low_risk_y = 9, 5
    low_risk_rect = Rectangle((low_risk_x - 1.5, low_risk_y - 1.5), 3, 3,
                               fill=True, color=config.success_color,
                               ec=config.node_edge_color, lw=2, alpha=0.7)
    ax.add_patch(low_risk_rect)
    ax.text(low_risk_x, low_risk_y + 1.8, "Low Risk Individuals",
            ha='center', va='bottom', fontsize=config.font_size, fontweight='bold',
            color=config.success_color)
    ax.text(low_risk_x, low_risk_y, "Premium:\n$P_L", ha='center', va='center',
            fontsize=config.font_size + 2, fontweight='bold')
    
    # Insurer in the middle
    insurer_x, insurer_y = 6, 5
    insurer_circle = Circle((insurer_x, insurer_y), 0.8, fill=True,
                            color=config.node_color, ec=config.node_edge_color, lw=2)
    ax.add_patch(insurer_circle)
    ax.text(insurer_x, insurer_y, "Insurer\n(Sets\nPremiums)",
            ha='center', va='center', fontsize=config.font_size - 1, fontweight='bold',
            color='white')
    
    # Arrows from pools to insurer
    ax.annotate("", xy=(insurer_x - 0.8, insurer_y), xytext=(high_risk_x + 1.5, insurer_y),
                arrowprops=dict(arrowstyle='->', color=config.node_edge_color, lw=2))
    ax.annotate("", xy=(insurer_x + 0.8, insurer_y), xytext=(low_risk_x - 1.5, insurer_y),
                arrowprops=dict(arrowstyle='->', color=config.node_edge_color, lw=2))
    
    # Information asymmetry indicator
    ax.annotate("", xy=(insurer_x, insurer_y - 2), xytext=(insurer_x, insurer_y - 0.9),
                arrowprops=dict(arrowstyle='->', color=config.warning_color, lw=3,
                               linestyle='--'))
    ax.text(insurer_x, insurer_y - 2.5, "Cannot observe\nindividual risk type\n(Asymmetric Information)",
            ha='center', va='top', fontsize=config.font_size - 1,
            color=config.warning_color, fontweight='bold')
    
    # Policy impact arrow (from top)
    ax.annotate("", xy=(insurer_x, insurer_y + 0.9), xytext=(insurer_x, insurer_y + 2),
                arrowprops=dict(arrowstyle='->', color=config.highlight_color, lw=3,
                               linestyle='--'))
    ax.text(insurer_x, insurer_y + 2.3, "Policy: Genetic Testing Ban\n→ Reduces information asymmetry",
            ha='center', va='bottom', fontsize=config.font_size - 1,
            color=config.highlight_color)
    
    # Equilibrium outcomes at bottom
    eq_text = (
        "Equilibrium Outcomes:\n"
        "• Separating: High-risk pay P_H, Low-risk pay P_L\n"
        "• Pooling: Single premium P_avg (adverse selection)\n"
        "• Policy impact: Shifts equilibrium type"
    )
    ax.text(0.5, 0.05, eq_text, transform=ax.transAxes,
            fontsize=config.font_size - 1, verticalalignment='bottom',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
    
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=config.dpi, bbox_inches='tight')
    
    return fig


def create_module_d_diagram(
    params: Optional[Dict[str, float]] = None,
    config: Optional[DiagramConfig] = None,
    save_path: Optional[Path] = None,
) -> plt.Figure:
    """
    Create Module D: Proxy Substitution diagram.
    
    Shows how insurers use family history and other proxies when
    genetic information is restricted.
    
    Args:
        params: Optional parameters (proxy_accuracy, substitution_rate)
        config: Diagram configuration
        save_path: Optional path to save figure
        
    Returns:
        Matplotlib figure object
    """
    if config is None:
        config = DiagramConfig()
    
    fig, ax = plt.subplots(figsize=config.figsize, dpi=config.dpi)
    ax.set_facecolor(config.background_color)
    
    ax.set_title(
        "Module D: Proxy Substitution (Information Leakage)",
        fontsize=14, fontweight='bold', pad=20
    )
    
    # Create proxy substitution flow diagram
    
    # Genetic information (blocked by policy)
    genetic_x, genetic_y = 2, 6
    genetic_rect = Rectangle((genetic_x - 1, genetic_y - 0.7), 2, 1.4,
                             fill=True, color=config.highlight_color,
                             ec=config.node_edge_color, lw=2, alpha=0.5)
    ax.add_patch(genetic_rect)
    ax.text(genetic_x, genetic_y, "Genetic Test\nResults", ha='center', va='center',
            fontsize=config.font_size, fontweight='bold')
    
    # Blocked arrow (policy restriction)
    ax.annotate("", xy=(4, genetic_y), xytext=(genetic_x + 1, genetic_y),
                arrowprops=dict(arrowstyle='->', color='red', lw=3, linestyle='--'))
    ax.text(4, genetic_y + 0.5, "BLOCKED\nby Policy", ha='center', va='bottom',
            fontsize=config.font_size - 1, color='red', fontweight='bold')
    
    # Alternative proxies
    proxy_positions = [
        (6, 2, "Family\nHistory"),
        (8, 2, "Medical\nRecords"),
        (10, 2, "Lifestyle\nFactors"),
    ]
    
    for px, py, label in proxy_positions:
        proxy_circle = Circle((px, py), 0.6, fill=True,
                              color=config.warning_color,
                              ec=config.node_edge_color, lw=2)
        ax.add_patch(proxy_circle)
        ax.text(px, py, label, ha='center', va='center',
                fontsize=config.font_size - 1, fontweight='bold')
    
    # Arrows from blocked path to proxies
    for px, py, _ in proxy_positions:
        ax.annotate("", xy=(px, py + 0.5), xytext=(4.5, genetic_y - 0.5),
                    arrowprops=dict(arrowstyle='->', color=config.warning_color, lw=2))
    
    # Insurer inference
    insurer_x, insurer_y = 8, 5
    insurer_rect = Rectangle((insurer_x - 1, insurer_y - 0.7), 2, 1.4,
                             fill=True, color=config.node_color,
                             ec=config.node_edge_color, lw=2)
    ax.add_patch(insurer_rect)
    ax.text(insurer_x, insurer_y, "Insurer\nInference", ha='center', va='center',
            fontsize=config.font_size, fontweight='bold', color='white')
    
    # Arrows from proxies to insurer
    for px, py, _ in proxy_positions:
        ax.annotate("", xy=(insurer_x - 1, insurer_y), xytext=(px + 0.6, py),
                    arrowprops=dict(arrowstyle='->', color=config.node_edge_color, lw=2))
    
    # Information leakage indicator
    leakage_text = (
        "Information Leakage:\n"
        "Even with genetic ban, insurers\n"
        "reconstruct risk via proxies\n"
        "→ Reduces policy effectiveness"
    )
    ax.text(0.5, 0.05, leakage_text, transform=ax.transAxes,
            fontsize=config.font_size - 1, verticalalignment='bottom',
            bbox=dict(boxstyle='round', facecolor=config.warning_color, alpha=0.3))
    
    # Reconstruction accuracy metric
    if params and 'proxy_accuracy' in params:
        acc = params['proxy_accuracy']
        acc_text = f"Reconstruction Accuracy: {acc:.1%}"
        ax.text(0.95, 0.95, acc_text, transform=ax.transAxes,
                fontsize=config.font_size, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.9),
                ha='right')
    
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=config.dpi, bbox_inches='tight')
    
    return fig


def create_module_e_diagram(
    params: Optional[Dict[str, float]] = None,
    config: Optional[DiagramConfig] = None,
    save_path: Optional[Path] = None,
) -> plt.Figure:
    """
    Create Module E: Pass-Through diagram.
    
    Shows how costs/benefits pass through the market structure
    from insurers to consumers.
    
    Args:
        params: Optional parameters (pass_through_rate)
        config: Diagram configuration
        save_path: Optional path to save figure
        
    Returns:
        Matplotlib figure object
    """
    if config is None:
        config = DiagramConfig()
    
    fig, ax = plt.subplots(figsize=config.figsize, dpi=config.dpi)
    ax.set_facecolor(config.background_color)
    
    ax.set_title(
        "Module E: Pass-Through Mechanism",
        fontsize=14, fontweight='bold', pad=20
    )
    
    # Create pass-through flow diagram
    
    # Market structure layers
    layers = [
        (2, 6, "Insurers", "Set premiums based on\nrisk expectations"),
        (6, 6, "Intermediaries", "Brokers/Agents\nMarket frictions"),
        (10, 6, "Consumers", "Face final premiums\nand coverage terms"),
    ]
    
    for lx, ly, label, desc in layers:
        # Box
        layer_rect = Rectangle((lx - 1.2, ly - 1), 2.4, 2,
                               fill=True, color=config.node_color,
                               ec=config.node_edge_color, lw=2, alpha=0.7)
        ax.add_patch(layer_rect)
        ax.text(lx, ly + 0.5, label, ha='center', va='center',
                fontsize=config.font_size + 1, fontweight='bold', color='white')
        ax.text(lx, ly - 0.5, desc, ha='center', va='center',
                fontsize=config.font_size - 1, color='white')
    
    # Arrows between layers
    ax.annotate("", xy=(4.8, 6), xytext=(3.2, 6),
                arrowprops=dict(arrowstyle='->', color=config.node_edge_color, lw=3))
    ax.annotate("", xy=(8.8, 6), xytext=(7.2, 6),
                arrowprops=dict(arrowstyle='->', color=config.node_edge_color, lw=3))
    
    # Policy impact (vertical arrow)
    ax.annotate("", xy=(6, 7.5), xytext=(6, 6.8),
                arrowprops=dict(arrowstyle='->', color=config.highlight_color, lw=3,
                               linestyle='--'))
    ax.text(6, 7.8, "Policy Intervention\n( Genetic Ban )",
            ha='center', va='bottom', fontsize=config.font_size,
            color=config.highlight_color, fontweight='bold')
    
    # Pass-through rate indicator
    pass_through_y = 3
    ax.text(6, pass_through_y + 0.8, "Pass-Through Rate",
            ha='center', va='bottom', fontsize=config.font_size, fontweight='bold')
    
    # Pass-through visualization (gauge-like)
    gauge_x = np.linspace(0, 1, 100)
    gauge_y = np.zeros_like(gauge_x)
    
    if params and 'pass_through_rate' in params:
        ptr = params['pass_through_rate']
        # Color gradient based on pass-through
        colors = plt.cm.RdYlGn(gauge_x * ptr)
        for i in range(len(gauge_x) - 1):
            ax.axvspan(2 + gauge_x[i] * 8, 2 + gauge_x[i+1] * 8, 
                      ymin=pass_through_y - 0.1, ymax=pass_through_y + 0.1,
                      color=colors[i], alpha=0.5)
        
        # Marker
        ax.axvline(2 + ptr * 8, pass_through_y - 0.2, pass_through_y + 0.2,
                  color='red', lw=3, linestyle='--')
        ax.text(2 + ptr * 8, pass_through_y - 0.4, f"{ptr:.1%}",
                ha='center', va='top', fontsize=config.font_size, fontweight='bold')
    
    # Labels
    ax.text(2, pass_through_y - 0.4, "0%", ha='center', va='top',
            fontsize=config.font_size - 1)
    ax.text(10, pass_through_y - 0.4, "100%", ha='center', va='top',
            fontsize=config.font_size - 1)
    
    # Outcome text
    outcome_text = (
        "Pass-Through Outcomes:\n"
        "• High competition → High pass-through to consumers\n"
        "• Market frictions → Incomplete pass-through\n"
        "• Policy effectiveness depends on market structure"
    )
    ax.text(0.5, 0.05, outcome_text, transform=ax.transAxes,
            fontsize=config.font_size - 1, verticalalignment='bottom',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
    
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=config.dpi, bbox_inches='tight')
    
    return fig


def create_module_f_diagram(
    params: Optional[Dict[str, float]] = None,
    config: Optional[DiagramConfig] = None,
    save_path: Optional[Path] = None,
) -> plt.Figure:
    """
    Create Module F: Data Quality diagram.
    
    Shows how genetic discrimination policies affect research
    participation and data quality externalities.
    
    Args:
        params: Optional parameters (research_participation_rate)
        config: Diagram configuration
        save_path: Optional path to save figure
        
    Returns:
        Matplotlib figure object
    """
    if config is None:
        config = DiagramConfig()
    
    fig, ax = plt.subplots(figsize=config.figsize, dpi=config.dpi)
    ax.set_facecolor(config.background_color)
    
    ax.set_title(
        "Module F: Data Quality Externality",
        fontsize=14, fontweight='bold', pad=20
    )
    
    # Create data quality feedback loop diagram
    
    # Policy at top
    policy_x, policy_y = 6, 7
    policy_rect = Rectangle((policy_x - 1.5, policy_y - 0.7), 3, 1.4,
                            fill=True, color=config.highlight_color,
                            ec=config.node_edge_color, lw=2)
    ax.add_patch(policy_rect)
    ax.text(policy_x, policy_y, "Genetic\nDiscrimination Policy",
            ha='center', va='center', fontsize=config.font_size, fontweight='bold')
    
    # Trust node
    trust_x, trust_y = 6, 5
    trust_circle = Circle((trust_x, trust_y), 0.6, fill=True,
                          color=config.success_color,
                          ec=config.node_edge_color, lw=2)
    ax.add_patch(trust_circle)
    ax.text(trust_x, trust_y, "Public\nTrust", ha='center', va='center',
            fontsize=config.font_size, fontweight='bold', color='white')
    
    # Arrow from policy to trust
    ax.annotate("", xy=(trust_x, trust_y + 0.6), xytext=(trust_x, policy_y - 0.7),
                arrowprops=dict(arrowstyle='->', color=config.node_edge_color, lw=2))
    ax.text(trust_x + 0.3, trust_y + 0.3, "Strong protections\n→ ↑ Trust",
            fontsize=config.font_size - 1, color=config.success_color)
    
    # Research participation
    participation_x, participation_y = 6, 3
    participation_rect = Rectangle((participation_x - 1.2, participation_y - 0.7), 2.4, 1.4,
                                   fill=True, color=config.node_color,
                                   ec=config.node_edge_color, lw=2)
    ax.add_patch(participation_rect)
    ax.text(participation_x, participation_y, "Research\nParticipation",
            ha='center', va='center', fontsize=config.font_size, fontweight='bold',
            color='white')
    
    # Arrow from trust to participation
    ax.annotate("", xy=(participation_x, participation_y + 0.7), 
                xytext=(participation_x, trust_y - 0.6),
                arrowprops=dict(arrowstyle='->', color=config.node_edge_color, lw=2))
    
    # Data quality
    quality_x, quality_y = 6, 1
    quality_circle = Circle((quality_x, quality_y), 0.6, fill=True,
                            color=config.warning_color,
                            ec=config.node_edge_color, lw=2)
    ax.add_patch(quality_circle)
    ax.text(quality_x, quality_y, "Data\nQuality", ha='center', va='center',
            fontsize=config.font_size, fontweight='bold')
    
    # Arrow from participation to quality
    ax.annotate("", xy=(quality_x, quality_y + 0.6), 
                xytext=(quality_x, participation_y - 0.7),
                arrowprops=dict(arrowstyle='->', color=config.node_edge_color, lw=2))
    
    # Feedback loop (curved arrow)
    feedback_arrow = plt.annotate("", xy=(policy_x - 1.5, policy_y),
                                   xytext=(quality_x - 0.6, quality_y),
                                   arrowprops=dict(arrowstyle='->', 
                                                  color=config.success_color, 
                                                  lw=2, 
                                                  connectionstyle="arc3,rad=-0.5"))
    
    # Feedback label
    ax.text(3, 2.5, "Better data\n→ Better\npolicy design",
            fontsize=config.font_size - 2, color=config.success_color,
            style='italic')
    
    # Participation rate indicator
    if params and 'research_participation_rate' in params:
        rate = params['research_participation_rate']
        rate_text = f"Participation Rate: {rate:.1%}"
        ax.text(0.95, 0.95, rate_text, transform=ax.transAxes,
                fontsize=config.font_size, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.9),
                ha='right')
    
    # Externality note
    externality_text = (
        "Positive Externality:\n"
        "Genetic discrimination protections\n"
        "→ ↑ Trust → ↑ Research participation\n"
        "→ ↑ Data quality → ↑ Policy effectiveness"
    )
    ax.text(0.05, 0.05, externality_text, transform=ax.transAxes,
            fontsize=config.font_size - 1, verticalalignment='bottom',
            bbox=dict(boxstyle='round', facecolor=config.success_color, alpha=0.2))
    
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=config.dpi, bbox_inches='tight')
    
    return fig


def create_enforcement_diagram(
    params: Optional[Dict[str, float]] = None,
    config: Optional[DiagramConfig] = None,
    save_path: Optional[Path] = None,
) -> plt.Figure:
    """
    Create Enforcement: Compliance game diagram.
    
    Shows the compliance dynamics between insurers and regulators.
    
    Args:
        params: Optional parameters (enforcement_strength, penalty_rate)
        config: Diagram configuration
        save_path: Optional path to save figure
        
    Returns:
        Matplotlib figure object
    """
    if config is None:
        config = DiagramConfig()
    
    fig, ax = plt.subplots(figsize=config.figsize, dpi=config.dpi)
    ax.set_facecolor(config.background_color)
    
    ax.set_title(
        "Enforcement: Compliance Game",
        fontsize=14, fontweight='bold', pad=20
    )
    
    # Create compliance game diagram
    
    # Regulator
    regulator_x, regulator_y = 2, 5
    regulator_circle = Circle((regulator_x, regulator_y), 0.7, fill=True,
                               color=config.node_color,
                               ec=config.node_edge_color, lw=2)
    ax.add_patch(regulator_circle)
    ax.text(regulator_x, regulator_y + 0.2, "Regulator", ha='center', va='center',
            fontsize=config.font_size, fontweight='bold', color='white')
    ax.text(regulator_x, regulator_y - 0.3, "(Sets Rules)", ha='center', va='top',
            fontsize=config.font_size - 1, color='white')
    
    # Enforcement mechanism
    enforcement_x, enforcement_y = 6, 5
    enforcement_rect = Rectangle((enforcement_x - 1.2, enforcement_y - 1), 2.4, 2,
                                  fill=True, color=config.warning_color,
                                  ec=config.node_edge_color, lw=2)
    ax.add_patch(enforcement_rect)
    ax.text(enforcement_x, enforcement_y + 0.3, "Enforcement", ha='center', va='center',
            fontsize=config.font_size, fontweight='bold')
    ax.text(enforcement_x, enforcement_y - 0.3, "Monitoring &", ha='center', va='top',
            fontsize=config.font_size - 1)
    ax.text(enforcement_x, enforcement_y - 0.6, "Penalties", ha='center', va='top',
            fontsize=config.font_size - 1)
    
    # Arrow from regulator to enforcement
    ax.annotate("", xy=(enforcement_x - 1.2, enforcement_y),
                xytext=(regulator_x + 0.7, enforcement_y),
                arrowprops=dict(arrowstyle='->', color=config.node_edge_color, lw=2))
    
    # Insurer
    insurer_x, insurer_y = 10, 5
    insurer_circle = Circle((insurer_x, insurer_y), 0.7, fill=True,
                            color=config.highlight_color,
                            ec=config.node_edge_color, lw=2)
    ax.add_patch(insurer_circle)
    ax.text(insurer_x, insurer_y + 0.2, "Insurer", ha='center', va='center',
            fontsize=config.font_size, fontweight='bold', color='white')
    ax.text(insurer_x, insurer_y - 0.3, "(Decides to", ha='center', va='top',
            fontsize=config.font_size - 1, color='white')
    ax.text(insurer_x, insurer_y - 0.6, "Comply)", ha='center', va='top',
            fontsize=config.font_size - 1, color='white')
    
    # Arrow from enforcement to insurer
    ax.annotate("", xy=(insurer_x - 0.7, insurer_y),
                xytext=(enforcement_x + 1.2, enforcement_y),
                arrowprops=dict(arrowstyle='->', color=config.node_edge_color, lw=2))
    
    # Compliance decision branches
    comply_x, comply_y = 10, 2
    comply_rect = Rectangle((comply_x - 1, comply_y - 0.5), 2, 1,
                            fill=True, color=config.success_color,
                            ec=config.node_edge_color, lw=2)
    ax.add_patch(comply_rect)
    ax.text(comply_x, comply_y, "Comply\n✓", ha='center', va='center',
            fontsize=config.font_size, fontweight='bold')
    
    violate_x, violate_y = 10, 7
    violate_rect = Rectangle((violate_x - 1, violate_y - 0.5), 2, 1,
                             fill=True, color=config.highlight_color,
                             ec=config.node_edge_color, lw=2)
    ax.add_patch(violate_rect)
    ax.text(violate_x, violate_y, "Violate\n✗", ha='center', va='center',
            fontsize=config.font_size, fontweight='bold')
    
    # Arrows from insurer to decisions
    ax.annotate("", xy=(insurer_x - 0.5, comply_y),
                xytext=(insurer_x, insurer_y - 0.7),
                arrowprops=dict(arrowstyle='->', color=config.success_color, lw=2))
    ax.annotate("", xy=(insurer_x - 0.5, violate_y),
                xytext=(insurer_x, insurer_y + 0.7),
                arrowprops=dict(arrowstyle='->', color=config.highlight_color, lw=2))
    
    # Penalty arrow (from enforcement to violate)
    ax.annotate("", xy=(violate_x - 1, violate_y),
                xytext=(enforcement_x + 1.2, violate_y),
                arrowprops=dict(arrowstyle='->', color='red', lw=3, linestyle='--'))
    ax.text(8.5, violate_y + 0.2, "Penalty if\ndetected", ha='center', va='bottom',
            fontsize=config.font_size - 1, color='red', fontweight='bold')
    
    # Parameters
    if params:
        param_text = "Enforcement Parameters:\n"
        for key, value in params.items():
            param_text += f"  {key}: {value:.3f}\n"
        ax.text(0.05, 0.95, param_text, transform=ax.transAxes,
                fontsize=config.font_size - 2, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Equilibrium note
    eq_text = (
        "Compliance Equilibrium:\n"
        "• Strong enforcement → High compliance\n"
        "• Weak enforcement → Strategic violations\n"
        "• Optimal policy: Balance enforcement cost vs compliance"
    )
    ax.text(0.5, 0.05, eq_text, transform=ax.transAxes,
            fontsize=config.font_size - 1, verticalalignment='bottom',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
    
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=config.dpi, bbox_inches='tight')
    
    return fig


def export_diagram(
    fig: plt.Figure,
    save_path: Path,
    formats: List[str] = ['png', 'svg'],
) -> List[Path]:
    """
    Export diagram to multiple formats.
    
    Args:
        fig: Matplotlib figure
        save_path: Base path (without extension)
        formats: List of formats to export
        
    Returns:
        List of saved file paths
    """
    saved_paths = []
    
    for fmt in formats:
        output_path = save_path.with_suffix(f'.{fmt}')
        fig.savefig(output_path, dpi=150 if fmt == 'png' else None,
                   bbox_inches='tight')
        saved_paths.append(output_path)
    
    return saved_paths


# Convenience function to generate all diagrams
def generate_all_game_diagrams(
    output_dir: Path,
    params: Optional[Dict[str, Dict[str, float]]] = None,
) -> Dict[str, List[Path]]:
    """
    Generate all 6 game diagrams.
    
    Args:
        output_dir: Directory to save diagrams
        params: Optional parameters for each diagram
        
    Returns:
        Dictionary mapping diagram names to saved file paths
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    diagrams = {
        'module_a_behavior': create_module_a_diagram,
        'module_c_insurance_eq': create_module_c_diagram,
        'module_d_proxy': create_module_d_diagram,
        'module_e_passthrough': create_module_e_diagram,
        'module_f_data_quality': create_module_f_diagram,
        'enforcement_compliance': create_enforcement_diagram,
    }
    
    results = {}
    
    for name, func in diagrams.items():
        print(f"Generating {name} diagram...")
        
        diagram_params = params.get(name) if params else None
        save_path = output_dir / f"{name}_diagram"
        
        fig = func(params=diagram_params, save_path=None)
        paths = export_diagram(fig, save_path, formats=['png', 'svg'])
        plt.close(fig)
        
        results[name] = paths
        print(f"  Saved: {', '.join(map(str, paths))}")
    
    return results


if __name__ == "__main__":
    # Example usage: generate all diagrams
    output_directory = Path(__file__).parent.parent / "outputs" / "diagrams"
    
    example_params = {
        'module_a_behavior': {
            'baseline_uptake': 0.52,
            'deterrence_elasticity': 0.18,
        },
        'module_d_proxy': {
            'proxy_accuracy': 0.65,
        },
        'module_e_passthrough': {
            'pass_through_rate': 0.75,
        },
        'module_f_data_quality': {
            'research_participation_rate': 0.45,
        },
    }
    
    saved_files = generate_all_game_diagrams(output_directory, example_params)
    print(f"\nGenerated {len(saved_files)} diagrams:")
    for name, paths in saved_files.items():
        print(f"  {name}: {len(paths)} files")
