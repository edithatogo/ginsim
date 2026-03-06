"""
Output formatter for policy evaluation results.

Generates tables, figures, and reports.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tabulate import tabulate


def format_policy_table(results: dict[str, Any]) -> str:
    """
    Format policy evaluation results as table.

    Args:
        results: Dictionary of policy results

    Returns:
        Formatted table string
    """
    headers = ["Policy", "Testing Uptake", "Avg Premium", "Welfare", "Compliance"]

    rows = []
    for policy_name, result in results.items():
        rows.append(
            [
                policy_name,
                f"{result.get('testing_uptake', 0):.1%}",
                f"{result.get('avg_premium', 0):.3f}",
                f"${result.get('welfare_impact', 0):,.0f}",
                f"{result.get('compliance_rate', 0):.1%}",
            ]
        )

    return tabulate(rows, headers=headers, tablefmt="grid")


def format_comparison_table(
    comparisons: dict[str, dict[str, float]], baseline: str = "status_quo"
) -> str:
    """
    Format policy comparisons as table.

    Args:
        comparisons: Dictionary of comparison metrics
        baseline: Baseline policy name

    Returns:
        Formatted table string
    """
    headers = ["Policy", "Δ Uptake", "Δ Premium", "Δ Welfare", "Δ Compliance"]

    rows = []
    for policy_name, metrics in comparisons.items():
        rows.append(
            [
                policy_name,
                f"{metrics.get('testing_uptake_change', 0):+.1%}",
                f"{metrics.get('premium_change', 0):+.3f}",
                f"${metrics.get('welfare_change', 0):,+,.0f}",
                f"{metrics.get('compliance_change', 0):+.1%}",
            ]
        )

    return tabulate(rows, headers=headers, tablefmt="grid")


def save_results_json(results: dict[str, Any], output_path: str | Path) -> None:
    """
    Save results to JSON file.

    Args:
        results: Results dictionary
        output_path: Output file path
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Convert arrays to lists for JSON serialization
    serializable = {}
    for policy_name, result in results.items():
        serializable[policy_name] = {}
        for key, value in result.items():
            if hasattr(value, "tolist"):
                serializable[policy_name][key] = value.tolist()
            elif hasattr(value, "item"):
                serializable[policy_name][key] = float(value)
            else:
                serializable[policy_name][key] = value

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=2)


def generate_policy_brief(
    results: dict[str, Any],
    comparisons: dict[str, dict[str, float]],
    output_path: str | Path,
) -> None:
    """
    Generate policy brief document.

    Args:
        results: Policy evaluation results
        comparisons: Policy comparisons
        output_path: Output file path
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Policy Brief: Genetic Discrimination Policy Evaluation",
        "",
        "## Executive Summary",
        "",
        "This brief summarizes the evaluation of three policy regimes for genetic discrimination in life insurance:",
        "",
        "1. **Status Quo**: No restrictions on genetic information use",
        "2. **Moratorium**: Industry self-regulation with financial caps",
        "3. **Statutory Ban**: Legislative prohibition with penalties",
        "",
        "## Key Findings",
        "",
        "### Testing Uptake",
        "",
    ]

    # Add testing uptake findings
    for policy_name, result in results.items():
        uptake = result.get("testing_uptake", 0)
        lines.append(f"- **{policy_name.title()}**: {uptake:.1%} testing uptake")

    lines.extend(
        [
            "",
            "### Welfare Impacts",
            "",
        ]
    )

    # Add welfare findings
    for policy_name, metrics in comparisons.items():
        welfare = metrics.get("welfare_change", 0)
        lines.append(f"- **{policy_name.title()}**: ${welfare:,+,.0f} vs status quo")

    lines.extend(
        [
            "",
            "## Policy Comparison",
            "",
            "```",
            format_comparison_table(comparisons),
            "```",
            "",
            "## Recommendations",
            "",
            "Based on the evaluation:",
            "",
            "1. **For maximizing testing uptake**: [Recommendation based on results]",
            "2. **For maximizing welfare**: [Recommendation based on results]",
            "3. **For minimizing adverse selection**: [Recommendation based on results]",
            "",
            "## Uncertainty and Limitations",
            "",
            "- Results reflect model assumptions and parameter uncertainty",
            "- Evidence base is limited (particularly for New Zealand)",
            "- Value of Information analysis recommended for research prioritization",
            "",
            "---",
            "",
            "*Generated from genetic discrimination policy model*",
        ]
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def generate_results_summary(results: dict[str, Any]) -> str:
    """
    Generate results summary string.

    Args:
        results: Policy evaluation results

    Returns:
        Summary string
    """
    lines = [
        "=" * 80,
        "POLICY EVALUATION RESULTS SUMMARY",
        "=" * 80,
        "",
    ]

    for policy_name, result in results.items():
        lines.append(f"Policy: {policy_name}")
        lines.append("-" * 40)

        if "testing_uptake" in result:
            lines.append(f"  Testing Uptake: {result['testing_uptake']:.1%}")
        if "avg_premium" in result:
            lines.append(f"  Average Premium: {result['avg_premium']:.3f}")
        if "welfare_impact" in result:
            lines.append(f"  Net Welfare: ${result['welfare_impact']:,.0f}")
        if "compliance_rate" in result:
            lines.append(f"  Compliance Rate: {result['compliance_rate']:.1%}")

        lines.append("")

    lines.append("=" * 80)

    return "\n".join(lines)
