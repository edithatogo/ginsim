#!/usr/bin/env python3
"""
Posterior predictive check runner for genetic discrimination policy model.

Usage:
    python -m scripts.run_posterior_predictive --n_draws 2000 --output outputs/ppc/
"""

import argparse
from datetime import datetime
from pathlib import Path

import numpy as np
from scipy.stats import beta, norm

# Prior definitions from calibration configs
PRIORS = {
    "baseline_testing_uptake": {"dist": "beta", "alpha": 462, "beta": 426},
    "deterrence_elasticity": {"dist": "beta", "alpha": 22.5, "beta": 102.5},
    "moratorium_effect": {"dist": "beta", "alpha": 12, "beta": 68},
    "adverse_selection_elasticity": {
        "dist": "normal",
        "mean": 0.08,
        "sd": 0.04,
        "trunc": (0, None),
    },
    "demand_elasticity_high_risk": {
        "dist": "normal",
        "mean": -0.22,
        "sd": 0.08,
        "trunc": (None, 0),
    },
    "baseline_loading": {"dist": "normal", "mean": 0.15, "sd": 0.06, "trunc": (0, None)},
    "family_history_sensitivity": {"dist": "beta", "alpha": 357, "beta": 168},
    "proxy_substitution_rate": {"dist": "beta", "alpha": 20, "beta": 30},
    "pass_through_rate": {"dist": "beta", "alpha": 60, "beta": 20},
    "research_participation_elasticity": {
        "dist": "normal",
        "mean": -0.10,
        "sd": 0.03,
        "trunc": (None, 0),
    },
    "enforcement_effectiveness": {"dist": "beta", "alpha": 10, "beta": 10},
    "complaint_rate": {"dist": "beta", "alpha": 2, "beta": 98},
}

# Empirical targets for comparison
EMPIRICAL_TARGETS = {
    "testing_uptake": {
        "value": 0.52,
        "ci_lower": 0.48,
        "ci_upper": 0.56,
        "source": "Ettema et al. 2021",
    },
    "premium_divergence": {
        "value": 0.08,
        "ci_lower": 0.03,
        "ci_upper": 0.15,
        "source": "Hersch & Viscusi 2019",
    },
    "deterrence_rate": {
        "value": 0.18,
        "ci_lower": 0.11,
        "ci_upper": 0.25,
        "source": "McGuire et al. 2019",
    },
}


def draw_from_prior(prior_name: str, n_draws: int, seed: int = None) -> np.ndarray:
    """Draw samples from a prior distribution."""
    if seed is not None:
        np.random.seed(seed)

    prior = PRIORS[prior_name]

    if prior["dist"] == "beta":
        return beta.rvs(prior["alpha"], prior["beta"], size=n_draws)

    if prior["dist"] == "normal":
        draws = norm.rvs(prior["mean"], prior["sd"], size=n_draws)

        # Apply truncation
        trunc = prior.get("trunc", (None, None))
        if trunc[0] is not None:
            draws = np.maximum(draws, trunc[0])
        if trunc[1] is not None:
            draws = np.minimum(draws, trunc[1])

        return draws

    raise ValueError(f"Unknown distribution: {prior['dist']}")


def simulate_model_outputs(draws: dict, n_draws: int) -> dict:
    """
    Simulate model outputs from prior draws.

    NOTE: This is a placeholder. Replace with actual model evaluation.
    """
    # Simplified simulation based on prior draws
    testing_uptake = draws["baseline_testing_uptake"] * (1 - draws["deterrence_elasticity"])

    premium_divergence = (
        draws["adverse_selection_elasticity"]
        * (1 - draws["proxy_substitution_rate"])
        * (1 - draws["enforcement_effectiveness"])
    )

    welfare_impact = (
        testing_uptake * 200  # QALYs from testing
        + premium_divergence * -50  # Welfare loss from adverse selection
    )

    return {
        "testing_uptake": testing_uptake,
        "premium_divergence": premium_divergence,
        "welfare_impact": welfare_impact,
        "deterrence_rate": draws["deterrence_elasticity"],
    }


def compare_to_targets(simulations: dict, targets: dict) -> dict:
    """Compare simulated outputs to empirical targets."""
    comparisons = {}

    for outcome, target in targets.items():
        if outcome not in simulations:
            continue

        sim_values = simulations[outcome]

        # Calculate coverage
        within_ci = np.sum(
            (sim_values >= target["ci_lower"]) & (sim_values <= target["ci_upper"])
        ) / len(sim_values)

        # Calculate bias
        sim_mean = np.mean(sim_values)
        bias = (sim_mean - target["value"]) / target["value"]

        comparisons[outcome] = {
            "target_value": target["value"],
            "target_ci": [target["ci_lower"], target["ci_upper"]],
            "sim_mean": sim_mean,
            "sim_sd": np.std(sim_values),
            "sim_ci": [np.percentile(sim_values, 2.5), np.percentile(sim_values, 97.5)],
            "coverage": within_ci,
            "bias": bias,
            "source": target["source"],
        }

    return comparisons


def generate_plots_data(simulations: dict, targets: dict, output_dir: Path):
    """Generate data for posterior predictive plots."""
    import json

    plot_data = {}

    for outcome in simulations:
        plot_data[outcome] = {
            "values": simulations[outcome].tolist()[:100],  # First 100 for visualization
            "mean": float(np.mean(simulations[outcome])),
            "ci": [
                float(np.percentile(simulations[outcome], 2.5)),
                float(np.percentile(simulations[outcome], 97.5)),
            ],
        }

        if outcome in targets:
            plot_data[outcome]["target"] = targets[outcome]["value"]
            plot_data[outcome]["target_ci"] = [
                targets[outcome]["ci_lower"],
                targets[outcome]["ci_upper"],
            ]

    with open(output_dir / "plot_data.json", "w") as f:
        json.dump(plot_data, f, indent=2)


def generate_report(comparisons: dict, n_draws: int, output_dir: Path):
    """Generate markdown report."""
    lines = [
        "# Posterior Predictive Check Report",
        "",
        f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Prior draws:** {n_draws}",
        "",
        "## Overview",
        "",
        "Posterior predictive checks compare model outputs (generated from prior draws) to empirical targets.",
        "Good calibration is indicated by:",
        "- High coverage (simulated values within empirical CI)",
        "- Low bias (< 20%)",
        "",
        "## Results by Outcome",
        "",
    ]

    overall_pass = True

    for outcome, comp in comparisons.items():
        coverage_status = "✅" if comp["coverage"] > 0.5 else "⚠️"
        bias_status = "✅" if abs(comp["bias"]) < 0.2 else "⚠️"

        lines.append(f"### {outcome.replace('_', ' ').title()}")
        lines.append("")
        lines.append(
            f"**Empirical Target:** {comp['target_value']:.2f} (95% CI: {comp['target_ci'][0]:.2f}-{comp['target_ci'][1]:.2f})"
        )
        lines.append(f"**Source:** {comp['source']}")
        lines.append("")
        lines.append(
            f"**Simulated:** {comp['sim_mean']:.2f} (95% CI: {comp['sim_ci'][0]:.2f}-{comp['sim_ci'][1]:.2f})"
        )
        lines.append("")
        lines.append(f"- Coverage: {comp['coverage']:.1%} {coverage_status}")
        lines.append(f"- Bias: {comp['bias']:+.1%} {bias_status}")
        lines.append("")

        if comp["coverage"] < 0.5 or abs(comp["bias"]) > 0.2:
            overall_pass = False
            lines.append("**⚠️ Note:** Poor calibration. Consider adjusting priors.")
            lines.append("")

    lines.append("## Overall Assessment")
    lines.append("")

    if overall_pass:
        lines.append(
            "✅ **All outcomes well-calibrated.** Priors are consistent with empirical evidence."
        )
    else:
        lines.append("⚠️ **Some outcomes poorly calibrated.** Consider prior adjustments:")
        lines.append("")
        for outcome, comp in comparisons.items():
            if comp["coverage"] < 0.5 or abs(comp["bias"]) > 0.2:
                lines.append(
                    f"- **{outcome}**: Bias {comp['bias']:+.1%}, Coverage {comp['coverage']:.1%}"
                )

    lines.append("")
    lines.append("## Next Steps")
    lines.append("")
    lines.append("1. Review poorly calibrated outcomes")
    lines.append("2. Adjust prior means or variances as needed")
    lines.append("3. Re-run posterior predictive checks")
    lines.append("4. Document prior adjustments in decision log")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Run posterior predictive checks")
    parser.add_argument(
        "--n_draws", type=int, default=2000, help="Number of prior draws (default: 2000)"
    )
    parser.add_argument(
        "--seed", type=int, default=20260303, help="Random seed (default: 20260303)"
    )
    parser.add_argument("--output", default="outputs/ppc", help="Output directory for results")

    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("POSTERIOR PREDICTIVE CHECKS")
    print("=" * 60)
    print(f"Number of draws: {args.n_draws}")
    print(f"Random seed: {args.seed}")
    print(f"Output directory: {output_dir}")
    print("=" * 60)

    # Draw from priors
    print("\nDrawing from priors...")
    prior_draws = {}
    for prior_name in PRIORS:
        prior_draws[prior_name] = draw_from_prior(prior_name, args.n_draws, args.seed)
        print(
            f"  {prior_name}: mean={np.mean(prior_draws[prior_name]):.3f}, sd={np.std(prior_draws[prior_name]):.3f}"
        )

    # Simulate model outputs
    print("\nSimulating model outputs...")
    simulations = simulate_model_outputs(prior_draws, args.n_draws)

    for outcome, values in simulations.items():
        print(
            f"  {outcome}: mean={np.mean(values):.3f}, 95% CI=[{np.percentile(values, 2.5):.3f}, {np.percentile(values, 97.5):.3f}]"
        )

    # Compare to empirical targets
    print("\nComparing to empirical targets...")
    comparisons = compare_to_targets(simulations, EMPIRICAL_TARGETS)

    for outcome, comp in comparisons.items():
        coverage_status = "✅" if comp["coverage"] > 0.5 else "⚠️"
        bias_status = "✅" if abs(comp["bias"]) < 0.2 else "⚠️"
        print(
            f"  {outcome}: Coverage={comp['coverage']:.1%} {coverage_status}, Bias={comp['bias']:+.1%} {bias_status}"
        )

    # Generate plots data
    print("\nGenerating plot data...")
    generate_plots_data(simulations, EMPIRICAL_TARGETS, output_dir)

    # Generate report
    print("Generating report...")
    report = generate_report(comparisons, args.n_draws, output_dir)

    report_file = output_dir / "REPORT.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n{'=' * 60}")
    print("Posterior predictive checks complete!")
    print(f"Report: {report_file}")
    print(f"Plot data: {output_dir / 'plot_data.json'}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
