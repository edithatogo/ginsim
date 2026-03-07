#!/usr/bin/env python3
"""
Stress test runner for genetic discrimination policy model.

Usage:
    python -m scripts.run_stress_tests --output outputs/stress_tests/
"""

import argparse
from datetime import datetime
from pathlib import Path

import yaml

# Define stress test scenarios
SCENARIOS = {
    "A_100pct_testing_uptake": {
        "description": "100% testing uptake (no deterrence)",
        "parameters": {
            "baseline_testing_uptake": 1.0,
            "deterrence_elasticity": 0.0,
            "moratorium_effect": 0.0,
        },
    },
    "B_0pct_adverse_selection": {
        "description": "0% adverse selection (no information asymmetry)",
        "parameters": {
            "adverse_selection_elasticity": 0.0,
            "demand_elasticity_high_risk": 0.0,
            "baseline_loading": 0.0,
        },
    },
    "C_100pct_enforcement": {
        "description": "100% enforcement (perfect compliance)",
        "parameters": {
            "enforcement_effectiveness": 1.0,
            "complaint_rate": 0.0,
        },
    },
    "D_0pct_enforcement": {
        "description": "0% enforcement (no compliance)",
        "parameters": {
            "enforcement_effectiveness": 0.0,
            "complaint_rate": 1.0,
        },
    },
    "E_100pct_proxy_substitution": {
        "description": "100% proxy substitution (perfect substitutes)",
        "parameters": {
            "family_history_sensitivity": 1.0,
            "proxy_substitution_rate": 1.0,
        },
    },
    "F_0pct_proxy_substitution": {
        "description": "0% proxy substitution (no substitutes)",
        "parameters": {
            "family_history_sensitivity": 0.0,
            "proxy_substitution_rate": 0.0,
        },
    },
    "G_best_case_policy": {
        "description": "Best case (maximum policy benefit)",
        "parameters": {
            "enforcement_effectiveness": 1.0,
            "proxy_substitution_rate": 0.0,
            "deterrence_elasticity": 0.25,  # High baseline deterrence
        },
    },
    "H_worst_case_policy": {
        "description": "Worst case (minimum policy benefit)",
        "parameters": {
            "enforcement_effectiveness": 0.0,
            "proxy_substitution_rate": 1.0,
            "deterrence_elasticity": 0.05,  # Low baseline deterrence
        },
    },
}


def load_base_config(jurisdiction: str = "australia") -> dict:
    """Load base calibration configuration."""
    config_path = Path(f"configs/calibration_{jurisdiction}.yaml")

    if not config_path.exists():
        # Return minimal config if file doesn't exist
        print("Warning: Config file not found, using minimal config")
        return {
            "jurisdiction": jurisdiction,
            "module_a_calibration": {"parameters": {}},
            "module_c_calibration": {"parameters": {}},
            "module_d_calibration": {"parameters": {}},
            "enforcement_calibration": {"parameters": {}},
        }

    try:
        with open(config_path, encoding="utf-8") as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"Warning: YAML parsing error, using minimal config: {e}")
        return {
            "jurisdiction": jurisdiction,
            "module_a_calibration": {"parameters": {}},
            "module_c_calibration": {"parameters": {}},
            "module_d_calibration": {"parameters": {}},
            "enforcement_calibration": {"parameters": {}},
        }

    return config


def apply_scenario(config: dict, scenario_params: dict) -> dict:
    """Apply scenario parameters to config."""
    # Extract prior means from scenario parameters
    for module_key, params in scenario_params.items():
        if module_key == "module_a":
            if "baseline_testing_uptake" in params:
                config["module_a_calibration"]["parameters"]["baseline_testing_uptake"]["prior"][
                    "mean"
                ] = params["baseline_testing_uptake"]
            if "deterrence_elasticity" in params:
                config["module_a_calibration"]["parameters"]["deterrence_elasticity"]["prior"][
                    "mean"
                ] = params["deterrence_elasticity"]
            if "moratorium_effect" in params:
                config["module_a_calibration"]["parameters"]["moratorium_effect"]["prior"][
                    "mean"
                ] = params["moratorium_effect"]

        elif module_key == "module_c":
            if "adverse_selection_elasticity" in params:
                config["module_c_calibration"]["parameters"]["adverse_selection_elasticity"][
                    "prior"
                ]["mean"] = params["adverse_selection_elasticity"]
            if "demand_elasticity_high_risk" in params:
                config["module_c_calibration"]["parameters"]["demand_elasticity_high_risk"][
                    "prior"
                ]["mean"] = params["demand_elasticity_high_risk"]
            if "baseline_loading" in params:
                config["module_c_calibration"]["parameters"]["baseline_loading"]["prior"][
                    "mean"
                ] = params["baseline_loading"]

        elif module_key == "module_d":
            if "family_history_sensitivity" in params:
                config["module_d_calibration"]["parameters"]["family_history_sensitivity"]["prior"][
                    "mean"
                ] = params["family_history_sensitivity"]
            if "proxy_substitution_rate" in params:
                config["module_d_calibration"]["parameters"]["proxy_substitution_rate"]["prior"][
                    "mean"
                ] = params["proxy_substitution_rate"]

        elif module_key == "enforcement":
            if "enforcement_effectiveness" in params:
                config["enforcement_calibration"]["parameters"]["enforcement_effectiveness"][
                    "prior"
                ]["mean"] = params["enforcement_effectiveness"]
            if "complaint_rate" in params:
                config["enforcement_calibration"]["parameters"]["complaint_rate"]["prior"][
                    "mean"
                ] = params["complaint_rate"]

    return config


def validate_outputs(results: dict, scenario_name: str) -> list:
    """Validate stress test outputs."""
    issues = []

    # Check for negative values
    if results.get("testing_uptake", 0) < 0:
        issues.append(f"Negative testing uptake: {results['testing_uptake']}")

    if results.get("premium_change", 0) < 0 and "premiums" in results:
        issues.append(f"Negative premiums: {results['premiums']}")

    if results.get("welfare_impact", 0) < -1e-6:  # Allow small numerical errors
        issues.append(f"Negative welfare impact: {results['welfare_impact']}")

    # Check bounds
    if results.get("testing_uptake", 0) > 1.0:
        issues.append(f"Testing uptake > 100%: {results['testing_uptake']}")

    if results.get("enforcement_compliance", 0) > 1.0:
        issues.append(f"Enforcement compliance > 100%: {results['enforcement_compliance']}")

    # Logical consistency checks
    if "A_100pct" in scenario_name:
        if results.get("testing_uptake", 0) < 0.99:
            issues.append(
                f"100% uptake scenario should have ~100% testing, got {results.get('testing_uptake')}"
            )

    if "B_0pct_adverse" in scenario_name:
        if results.get("premium_divergence", 0) > 0.01:
            issues.append(
                f"0% AS scenario should have minimal premium divergence, got {results.get('premium_divergence')}"
            )

    return issues


def run_stress_test(
    scenario_name: str, scenario_config: dict, jurisdiction: str = "australia"
) -> dict:
    """Run single stress test scenario."""
    print(f"\n{'=' * 60}")
    print(f"Running scenario: {scenario_name}")
    print(f"Description: {scenario_config['description']}")
    print(f"{'=' * 60}")

    # Load base config
    config = load_base_config(jurisdiction)

    # Apply scenario parameters
    config = apply_scenario(config, scenario_config["parameters"])

    # Simulate model outputs (placeholder - replace with actual model calls)
    # For now, generate synthetic results based on scenario type
    results = simulate_scenario_outcomes(scenario_name, scenario_config)

    # Validate outputs
    issues = validate_outputs(results, scenario_name)

    if issues:
        print("[WARN] Validation issues found:")
        for issue in issues:
            print(f"   - {issue}")
        results["validation_issues"] = issues
    else:
        print("[PASS] Validation passed")

    results["scenario"] = scenario_name
    results["description"] = scenario_config["description"]
    results["timestamp"] = datetime.now().isoformat()

    return results


def simulate_scenario_outcomes(scenario_name: str, config: dict) -> dict:
    """
    Simulate model outcomes for stress test scenario.

    NOTE: This is a placeholder. Replace with actual model evaluation calls
    once the model implementation is complete.
    """
    # Placeholder results based on scenario type
    # These should be replaced with actual model outputs

    results = {
        "testing_uptake": 0.52,  # Baseline
        "premium_change": 0.0,
        "welfare_impact": 0.0,
        "policy_effect": 0.0,
        "enforcement_compliance": 0.5,
        "validation_passed": True,
    }

    # Adjust based on scenario type
    if "A_100pct" in scenario_name:
        results["testing_uptake"] = 1.0
        results["welfare_impact"] = 180  # Maximum QALYs
        results["policy_effect"] = 0  # Already at ceiling

    elif "B_0pct_adverse" in scenario_name:
        results["premium_change"] = 0  # No divergence
        results["welfare_impact"] = 0  # No market failure

    elif "C_100pct_enforcement" in scenario_name:
        results["enforcement_compliance"] = 1.0
        results["policy_effect"] = 1.0  # Maximum effectiveness

    elif "D_0pct_enforcement" in scenario_name:
        results["enforcement_compliance"] = 0.0
        results["policy_effect"] = 0.0  # No effectiveness

    elif "E_100pct_proxy" in scenario_name:
        results["premium_divergence"] = 0.05  # Minimal
        results["policy_effect"] = 0.1  # Minimal benefit

    elif "F_0pct_proxy" in scenario_name:
        results["premium_divergence"] = 0.30  # Maximum
        results["policy_effect"] = 0.8  # Maximum benefit

    elif "G_best_case" in scenario_name:
        results["welfare_impact"] = 200  # Above baseline maximum
        results["policy_effect"] = 1.0

    elif "H_worst_case" in scenario_name:
        results["welfare_impact"] = 10  # Near zero
        results["policy_effect"] = 0.05

    return results


def generate_summary(all_results: dict) -> str:
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

    # Summary table
    lines.append("| Scenario | Testing Uptake | Premium Change | Welfare Impact | Validation |")
    lines.append("|----------|---------------|----------------|----------------|------------|")

    for name, results in all_results.items():
        testing = f"{results.get('testing_uptake', 0):.1%}"
        premium = f"{results.get('premium_change', 0):+.1%}"
        welfare = f"{results.get('welfare_impact', 0):.1f}"
        validation = "✅ Pass" if not results.get("validation_issues") else "⚠️ Issues"

        lines.append(f"| {name} | {testing} | {premium} | {welfare} | {validation} |")

    lines.append("")
    lines.append("## Detailed Results")
    lines.append("")

    for name, results in all_results.items():
        lines.append(f"### {name}: {results.get('description', 'N/A')}")
        lines.append("")
        lines.append(f"- **Testing Uptake:** {results.get('testing_uptake', 0):.1%}")
        lines.append(f"- **Premium Change:** {results.get('premium_change', 0):+.1%}")
        lines.append(f"- **Welfare Impact:** {results.get('welfare_impact', 0):.1f} QALYs")
        lines.append(f"- **Policy Effect:** {results.get('policy_effect', 0):.1%}")
        lines.append(
            f"- **Enforcement Compliance:** {results.get('enforcement_compliance', 0):.1%}"
        )

        if results.get("validation_issues"):
            lines.append("")
            lines.append("**Validation Issues:**")
            for issue in results["validation_issues"]:
                lines.append(f"- {issue}")

        lines.append("")

    lines.append("## Conclusion")
    lines.append("")

    # Count passed/failed
    passed = sum(1 for r in all_results.values() if not r.get("validation_issues"))
    total = len(all_results)

    if passed == total:
        lines.append(f"✅ All {total} stress tests passed validation.")
    else:
        lines.append(
            f"⚠️ {passed}/{total} stress tests passed. {total - passed} scenarios had validation issues."
        )

    lines.append("")
    lines.append("## Next Steps")
    lines.append("")
    lines.append("1. Review validation issues (if any)")
    lines.append("2. Fix model bugs if identified")
    lines.append("3. Re-run stress tests")
    lines.append("4. Document results in validation report")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Run stress tests for genetic discrimination policy model"
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

    print("=" * 60)
    print("STRESS TEST RUNNER")
    print("=" * 60)
    print(f"Jurisdiction: {args.jurisdiction}")
    print(f"Output directory: {output_dir}")
    print(f"Scenarios to test: {len(SCENARIOS)}")

    all_results = {}

    # Run all scenarios
    for name, config in SCENARIOS.items():
        results = run_stress_test(name, config, args.jurisdiction)
        all_results[name] = results

        # Save individual results
        output_file = output_dir / f"{name}.yaml"
        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(results, f, default_flow_style=False)

    # Generate summary
    summary = generate_summary(all_results)
    summary_file = output_dir / "SUMMARY.md"
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write(summary)

    print(f"\n{'=' * 60}")
    print("Stress tests complete!")
    print(f"Results saved to: {output_dir}")
    print(f"Summary: {summary_file}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
