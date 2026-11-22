#!/usr/bin/env python3
"""
Stress test runner for the genetic discrimination policy model.

Usage:
    python -m scripts.run_stress_tests --output outputs/stress_tests/
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger

from src.model.module_a_behavior import get_standard_policies
from src.model.parameters import (
    ModelParameters,
    get_default_parameters,
    load_jurisdiction_parameters,
)
from src.model.pipeline import evaluate_single_policy
from src.utils.logging_config import setup_logging

setup_logging(level="INFO")

SCENARIOS = {
    "A_100pct_testing_uptake": {
        "description": "Maximum feasible testing uptake under a fully protected setting",
        "policy": "ban",
        "parameters": {
            "adverse_selection_elasticity": 0.0,
            "baseline_loading": 0.0,
            "enforcement_effectiveness": 1.0,
            "moratorium_effect": 0.25,
        },
    },
    "B_0pct_adverse_selection": {
        "description": "No adverse selection or high-risk demand distortion",
        "policy": "status_quo",
        "parameters": {
            "adverse_selection_elasticity": 0.0,
            "demand_elasticity_high_risk": 0.0,
            "baseline_loading": 0.0,
        },
    },
    "C_100pct_enforcement": {
        "description": "Perfect policy enforcement",
        "policy": "ban",
        "parameters": {
            "enforcement_effectiveness": 1.0,
            "complaint_rate": 0.0,
        },
    },
    "D_0pct_enforcement": {
        "description": "No enforcement response",
        "policy": "moratorium",
        "parameters": {
            "enforcement_effectiveness": 0.0,
            "complaint_rate": 1.0,
        },
    },
    "E_100pct_proxy_substitution": {
        "description": "Proxy channels recover almost all restricted information",
        "policy": "ban",
        "parameters": {
            "family_history_sensitivity": 1.0,
            "proxy_substitution_rate": 1.0,
        },
    },
    "F_0pct_proxy_substitution": {
        "description": "Proxy channels recover none of the restricted information",
        "policy": "ban",
        "parameters": {
            "family_history_sensitivity": 0.0,
            "proxy_substitution_rate": 0.0,
        },
    },
    "G_best_case_policy": {
        "description": "Strongest plausible reform setting",
        "policy": "ban",
        "parameters": {
            "enforcement_effectiveness": 1.0,
            "proxy_substitution_rate": 0.0,
            "research_participation_elasticity": -0.02,
            "complaint_rate": 0.0,
        },
    },
    "H_worst_case_policy": {
        "description": "Weak enforcement with strong proxy recovery",
        "policy": "moratorium",
        "parameters": {
            "enforcement_effectiveness": 0.0,
            "proxy_substitution_rate": 1.0,
            "research_participation_elasticity": -0.20,
            "complaint_rate": 1.0,
        },
    },
}


def build_base_params(jurisdiction: str) -> ModelParameters:
    """Construct a validated base parameter set for the chosen jurisdiction."""
    # load_jurisdiction_parameters is safer than direct ModelParameters init
    # as it ensures all fields (like calibration_date) are present.
    try:
        return load_jurisdiction_parameters(jurisdiction)
    except:
        return get_default_parameters()


def validate_outputs(results: dict[str, Any], scenario_name: str) -> list[str]:
    """Validate stress test outputs from the active pipeline."""
    issues: list[str] = []

    testing_uptake = float(results.get("testing_uptake", 0.0))
    uninsured_rate = float(results.get("insurance_uninsured_rate", 0.0))
    compliance_rate = float(results.get("enforcement_compliance", 0.0))
    avg_premium = float(results.get("avg_premium", 0.0))
    proxy_rate = float(results.get("proxy_substitution_rate", 0.0))

    if not 0.0 <= testing_uptake <= 1.0:
        issues.append(f"Testing uptake outside [0,1]: {testing_uptake}")
    if not 0.0 <= uninsured_rate <= 1.0:
        issues.append(f"Uninsured rate outside [0,1]: {uninsured_rate}")
    if not 0.0 <= compliance_rate <= 1.0:
        issues.append(f"Compliance rate outside [0,1]: {compliance_rate}")
    if avg_premium < 0.0:
        issues.append(f"Negative average premium: {avg_premium}")
    if not 0.0 <= proxy_rate <= 1.0:
        issues.append(f"Proxy substitution rate outside [0,1]: {proxy_rate}")

    if scenario_name == "C_100pct_enforcement" and compliance_rate < 0.95:
        issues.append(
            f"Perfect enforcement scenario should have near-total compliance, got {compliance_rate:.3f}"
        )
    if scenario_name == "D_0pct_enforcement" and compliance_rate > 0.60:
        issues.append(
            "Zero enforcement scenario should materially reduce compliance under the implemented model, "
            f"got {compliance_rate:.3f}"
        )
    if scenario_name == "E_100pct_proxy_substitution" and proxy_rate < 0.95:
        issues.append(f"Full proxy substitution scenario should approach 1.0, got {proxy_rate:.3f}")
    if scenario_name == "F_0pct_proxy_substitution" and proxy_rate > 0.05:
        issues.append(f"Zero proxy substitution scenario should approach 0.0, got {proxy_rate:.3f}")

    return issues


def run_stress_test(
    scenario_name: str, scenario_config: dict[str, Any], jurisdiction: str = "australia"
) -> dict[str, Any]:
    """Run a single stress-test scenario through the active policy pipeline."""
    logger.info("-" * 60)
    logger.info(f"Running scenario: {scenario_name}")
    logger.info(f"Description: {scenario_config['description']}")
    logger.info("-" * 60)

    base_params = build_base_params(jurisdiction)
    params = base_params.model_copy(update=scenario_config["parameters"])
    policy = get_standard_policies()[scenario_config["policy"]]
    result = evaluate_single_policy(params, policy)

    output = {
        "scenario": scenario_name,
        "description": scenario_config["description"],
        "policy": policy.name,
        "timestamp": datetime.now().isoformat(),
        "testing_uptake": float(result.testing_uptake),
        "avg_premium": float(result.insurance_premiums.get("avg_premium", 0.0)),
        "premium_change": float(result.insurance_premiums.get("risk_rating", 0.0)),
        "insurance_uninsured_rate": float(result.insurance_premiums.get("uninsured_rate", 0.0)),
        "welfare_impact": float(result.welfare_impact),
        "policy_effect": float(result.all_metrics["welfare"].get("net_welfare", 0.0)),
        "enforcement_compliance": float(result.compliance_rate),
        "proxy_substitution_rate": float(
            result.all_metrics["proxy"].get("proxy_substitution_rate", 0.0)
        ),
        "research_participation": float(result.research_participation),
    }

    issues = validate_outputs(output, scenario_name)
    if issues:
        logger.warning("Validation issues found:")
        for issue in issues:
            logger.warning(f"   - {issue}")
        output["validation_issues"] = issues
    else:
        logger.success("Validation passed")

    return output


def generate_summary(all_results: dict[str, dict[str, Any]]) -> str:
    """Generate summary markdown report."""
    lines = [
        "# Stress Test Results Summary",
        "",
        f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## Overview",
        "",
        f"Total scenarios tested: {len(all_results)}",
        "",
        "## Results by Scenario",
        "",
    ]

    lines.append("| Scenario | Testing Uptake | Avg Premium | Welfare Impact | Validation |")
    lines.append("|----------|---------------|-------------|----------------|------------|")

    for name, results in all_results.items():
        testing = f"{results.get('testing_uptake', 0):.1%}"
        premium = f"${results.get('avg_premium', 0):,.2f}"
        welfare = f"{results.get('welfare_impact', 0):.1f}"
        validation = "PASS" if not results.get("validation_issues") else "ISSUES"
        lines.append(f"| {name} | {testing} | {premium} | {welfare} | {validation} |")

    lines.append("")
    lines.append("## Detailed Results")
    lines.append("")

    for name, results in all_results.items():
        lines.append(f"### {name}: {results.get('description', 'N/A')}")
        lines.append("")
        lines.append(f"- **Policy Surface:** {results.get('policy', 'N/A')}")
        lines.append(f"- **Testing Uptake:** {results.get('testing_uptake', 0):.1%}")
        lines.append(f"- **Average Premium:** ${results.get('avg_premium', 0):,.2f}")
        lines.append(f"- **Risk Rating Spread:** {results.get('premium_change', 0):+.3f}")
        lines.append(f"- **Welfare Impact:** {results.get('welfare_impact', 0):.1f}")
        lines.append(f"- **Compliance:** {results.get('enforcement_compliance', 0):.1%}")
        lines.append(
            f"- **Research Participation:** {results.get('research_participation', 0):.1%}"
        )

        if results.get("validation_issues"):
            lines.append("")
            lines.append("**Validation Issues:**")
            for issue in results["validation_issues"]:
                lines.append(f"- {issue}")

        lines.append("")

    lines.append("## Conclusion")
    lines.append("")
    passed = sum(1 for r in all_results.values() if not r.get("validation_issues"))
    total = len(all_results)

    if passed == total:
        lines.append(f"[PASS] All {total} stress tests passed validation.")
    else:
        lines.append(
            f"[WARN] {passed}/{total} stress tests passed. {total - passed} scenarios had validation issues."
        )

    lines.append("")
    lines.append("## Next Steps")
    lines.append("")
    lines.append("1. Review validation issues (if any)")
    lines.append("2. Investigate model behavior where edge scenarios violate expectations")
    lines.append("3. Re-run stress tests after any parameterization changes")
    lines.append("4. Fold validated stress-test outputs into the validation report")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run stress tests for the genetic discrimination policy model"
    )
    parser.add_argument(
        "--jurisdiction",
        default="australia",
        choices=["australia", "new_zealand"],
        help="Jurisdiction to test (default: australia)",
    )
    parser.add_argument(
        "--output", default="outputs/stress_tests", help="Output directory for results"
    )

    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info("=" * 60)
    logger.info("STRESS TEST RUNNER")
    logger.info("=" * 60)
    logger.info(f"Jurisdiction: {args.jurisdiction}")
    logger.info(f"Output directory: {output_dir}")
    logger.info(f"Scenarios to test: {len(SCENARIOS)}")

    all_results: dict[str, dict[str, Any]] = {}

    for name, config in SCENARIOS.items():
        results = run_stress_test(name, config, args.jurisdiction)
        all_results[name] = results

        output_file = output_dir / f"{name}.yaml"
        with output_file.open("w", encoding="utf-8") as handle:
            yaml.dump(results, handle, default_flow_style=False)

    summary = generate_summary(all_results)
    summary_file = output_dir / "SUMMARY.md"
    summary_file.write_text(summary, encoding="utf-8")

    logger.info("-" * 60)
    logger.success("Stress tests complete!")
    logger.info(f"Results saved to: {output_dir}")
    logger.info(f"Summary: {summary_file}")
    logger.info("-" * 60)


if __name__ == "__main__":
    main()
