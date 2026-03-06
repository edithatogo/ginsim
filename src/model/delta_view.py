#!/usr/bin/env python3
"""
Comparative Delta View Module

Calculate and visualize policy deltas with automatic Net Welfare Gain calculations.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from operator import itemgetter
from pathlib import Path
from typing import Any


@dataclass
class DeltaMetrics:
    """Delta metrics between two policies."""

    policy_name: str
    baseline_name: str
    testing_uptake_delta: float
    welfare_delta: float
    qalys_delta: float
    compliance_delta: float
    net_welfare_gain: float
    cost_benefit_ratio: float


@dataclass
class ComparativeAnalysis:
    """Complete comparative analysis results."""

    baseline_policy: str
    comparison_policies: list[str]
    delta_metrics: list[DeltaMetrics]
    ranking_by_welfare: list[str]
    ranking_by_uptake: list[str]
    summary: dict[str, Any]


def calculate_net_welfare_gain(
    welfare_delta: float,
    implementation_cost: float,
    administrative_cost: float,
    time_horizon: int = 10,
    discount_rate: float = 0.03,
) -> float:
    """
    Calculate net welfare gain from policy change.

    Args:
        welfare_delta: Change in welfare from policy
        implementation_cost: One-time implementation cost
        administrative_cost: Annual administrative cost
        time_horizon: Time horizon in years
        discount_rate: Discount rate for NPV calculation

    Returns:
        Net present value of welfare gain
    """
    # Calculate present value of administrative costs
    pv_admin_costs = 0.0
    for t in range(1, time_horizon + 1):
        pv_admin_costs += administrative_cost / ((1 + discount_rate) ** t)

    # Net welfare gain = welfare delta - implementation cost - PV of admin costs
    net_welfare = welfare_delta - implementation_cost - pv_admin_costs

    return net_welfare


def calculate_cost_benefit_ratio(
    benefits: float,
    costs: float,
) -> float:
    """
    Calculate cost-benefit ratio.

    Args:
        benefits: Total benefits (welfare gains)
        costs: Total costs

    Returns:
        Cost-benefit ratio (benefits per dollar spent)
    """
    if costs <= 0:
        return float("inf")

    return benefits / costs


def comparative_delta_analysis(
    baseline_result: dict[str, float],
    policy_results: dict[str, dict[str, float]],
    cost_params: dict[str, float] | None = None,
) -> ComparativeAnalysis:
    """
    Perform comprehensive comparative delta analysis.

    Args:
        baseline_result: Baseline policy results
        policy_results: Dictionary of policy results to compare
        cost_params: Cost parameters for net welfare calculation

    Returns:
        ComparativeAnalysis with all delta metrics
    """
    if cost_params is None:
        cost_params = {
            "implementation_cost": 1000000,  # $1M default
            "administrative_cost": 100000,  # $100k/year default
            "time_horizon": 10,
            "discount_rate": 0.03,
        }

    delta_metrics = []
    welfare_rankings = []
    uptake_rankings = []

    for policy_name, result in policy_results.items():
        # Calculate deltas
        testing_uptake_delta = result.get("testing_uptake", 0) - baseline_result.get(
            "testing_uptake", 0
        )
        welfare_delta = result.get("welfare_impact", 0) - baseline_result.get("welfare_impact", 0)
        qalys_delta = result.get("qalys_gained", 0) - baseline_result.get("qalys_gained", 0)
        compliance_delta = result.get("compliance_rate", 0) - baseline_result.get(
            "compliance_rate", 0
        )

        # Calculate net welfare gain
        net_welfare_gain = calculate_net_welfare_gain(
            welfare_delta=abs(welfare_delta),  # Use absolute value for gain calculation
            implementation_cost=cost_params.get("implementation_cost", 1000000),
            administrative_cost=cost_params.get("administrative_cost", 100000),
            time_horizon=int(cost_params.get("time_horizon", 10)),
            discount_rate=cost_params.get("discount_rate", 0.03),
        )

        # Adjust sign based on welfare delta direction
        if welfare_delta < 0:
            net_welfare_gain = -abs(net_welfare_gain)

        # Calculate cost-benefit ratio
        total_costs = cost_params.get("implementation_cost", 1000000) + cost_params.get(
            "administrative_cost", 100000
        ) * cost_params.get("time_horizon", 10)
        cost_benefit_ratio = calculate_cost_benefit_ratio(abs(welfare_delta), total_costs)

        metrics = DeltaMetrics(
            policy_name=policy_name,
            baseline_name="baseline",
            testing_uptake_delta=testing_uptake_delta,
            welfare_delta=welfare_delta,
            qalys_delta=qalys_delta,
            compliance_delta=compliance_delta,
            net_welfare_gain=net_welfare_gain,
            cost_benefit_ratio=cost_benefit_ratio,
        )

        delta_metrics.append(metrics)
        welfare_rankings.append((policy_name, welfare_delta))
        uptake_rankings.append((policy_name, testing_uptake_delta))

    # Sort rankings
    welfare_rankings.sort(key=itemgetter(1), reverse=True)
    uptake_rankings.sort(key=itemgetter(1), reverse=True)

    ranking_by_welfare = [name for name, _ in welfare_rankings]
    ranking_by_uptake = [name for name, _ in uptake_rankings]

    # Generate summary
    best_welfare = ranking_by_welfare[0] if ranking_by_welfare else None
    best_uptake = ranking_by_uptake[0] if ranking_by_uptake else None

    summary = {
        "best_welfare_policy": best_welfare,
        "best_uptake_policy": best_uptake,
        "total_policies_compared": len(policy_results),
        "policies_with_positive_welfare": sum(1 for m in delta_metrics if m.welfare_delta > 0),
        "policies_with_positive_uptake": sum(
            1 for m in delta_metrics if m.testing_uptake_delta > 0
        ),
    }

    return ComparativeAnalysis(
        baseline_policy="baseline",
        comparison_policies=list(policy_results.keys()),
        delta_metrics=delta_metrics,
        ranking_by_welfare=ranking_by_welfare,
        ranking_by_uptake=ranking_by_uptake,
        summary=summary,
    )


def format_delta_table(analysis: ComparativeAnalysis) -> str:
    """
    Format delta analysis as markdown table.

    Args:
        analysis: ComparativeAnalysis object

    Returns:
        Markdown table string
    """
    lines = []

    # Header
    lines.append(
        "| Policy | Δ Uptake | Δ Welfare | Δ QALYs | Δ Compliance | Net Welfare Gain | C/B Ratio |"
    )
    lines.append(
        "|--------|----------|-----------|---------|--------------|------------------|-----------|"
    )

    # Rows
    for metrics in analysis.delta_metrics:
        lines.append(
            f"| {metrics.policy_name} | "
            f"{metrics.testing_uptake_delta:+.1%} | "
            f"${metrics.welfare_delta:+,.0f} | "
            f"{metrics.qalys_delta:+.2f} | "
            f"{metrics.compliance_delta:+.1%} | "
            f"${metrics.net_welfare_gain:+,.0f} | "
            f"{metrics.cost_benefit_ratio:.2f} |",
        )

    # Summary
    lines.append("\n**Summary:**")
    lines.append(f"- Best policy by welfare: {analysis.summary.get('best_welfare_policy', 'N/A')}")
    lines.append(f"- Best policy by uptake: {analysis.summary.get('best_uptake_policy', 'N/A')}")
    lines.append(
        f"- Policies with positive welfare impact: {analysis.summary.get('policies_with_positive_welfare', 0)}/{analysis.summary.get('total_policies_compared', 0)}"
    )

    return "\n".join(lines)


def save_delta_analysis(
    analysis: ComparativeAnalysis,
    output_path: Path | str,
) -> None:
    """
    Save delta analysis to JSON file.

    Args:
        analysis: ComparativeAnalysis object
        output_path: Output file path
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Convert to serializable format
    data = {
        "baseline_policy": analysis.baseline_policy,
        "comparison_policies": analysis.comparison_policies,
        "delta_metrics": [
            {
                "policy_name": m.policy_name,
                "baseline_name": m.baseline_name,
                "testing_uptake_delta": m.testing_uptake_delta,
                "welfare_delta": m.welfare_delta,
                "qalys_delta": m.qalys_delta,
                "compliance_delta": m.compliance_delta,
                "net_welfare_gain": m.net_welfare_gain,
                "cost_benefit_ratio": m.cost_benefit_ratio,
            }
            for m in analysis.delta_metrics
        ],
        "ranking_by_welfare": analysis.ranking_by_welfare,
        "ranking_by_uptake": analysis.ranking_by_uptake,
        "summary": analysis.summary,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
