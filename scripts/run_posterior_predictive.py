#!/usr/bin/env python3
"""
Posterior predictive check runner for the genetic discrimination policy model.

Usage:
    python -m scripts.run_posterior_predictive --n_draws 2000 --output outputs/ppc/
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

import numpy as np
from loguru import logger
from scipy.stats import beta, norm

from src.model.module_a_behavior import get_standard_policies
from src.model.module_c_insurance_eq import compute_premium_divergence
from src.model.parameters import ModelParameters, get_default_parameters
from src.model.pipeline import evaluate_single_policy
from src.utils.logging_config import setup_logging

# Initialize logging
setup_logging(level="INFO")

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


def draw_from_prior(prior_name: str, n_draws: int, seed: int | None = None) -> np.ndarray:
    """Draw samples from a prior distribution."""
    if seed is not None:
        np.random.seed(seed)

    prior = PRIORS[prior_name]

    if prior["dist"] == "beta":
        return beta.rvs(prior["alpha"], prior["beta"], size=n_draws)

    if prior["dist"] == "normal":
        draws = norm.rvs(prior["mean"], prior["sd"], size=n_draws)

        trunc = prior.get("trunc", (None, None))
        if trunc[0] is not None:
            draws = np.maximum(draws, trunc[0])
        if trunc[1] is not None:
            draws = np.minimum(draws, trunc[1])

        return draws

    msg = f"Unknown distribution: {prior['dist']}"
    raise ValueError(msg)


def _build_model_parameters(draws: dict[str, np.ndarray], draw_idx: int) -> ModelParameters:
    """Materialize a single parameter draw as validated model parameters."""
    base = get_default_parameters()
    updates = {name: float(values[draw_idx]) for name, values in draws.items()}
    return base.model_copy(update=updates)


def simulate_model_outputs(draws: dict[str, np.ndarray], n_draws: int) -> dict[str, np.ndarray]:
    """
    Simulate model outputs from prior draws using the active policy pipeline.
    """
    policies = get_standard_policies()
    baseline_policy = policies["status_quo"]
    reform_policy = policies["moratorium"]

    testing_uptake: list[float] = []
    premium_divergence: list[float] = []
    welfare_impact: list[float] = []
    deterrence_rate: list[float] = []

    for draw_idx in range(n_draws):
        params = _build_model_parameters(draws, draw_idx)
        baseline_result = evaluate_single_policy(params, baseline_policy)
        reform_result = evaluate_single_policy(params, reform_policy)
        premium_metrics = compute_premium_divergence(params, baseline_policy, reform_policy)

        testing_uptake.append(float(baseline_result.testing_uptake))
        premium_divergence.append(abs(float(premium_metrics["relative_divergence"])))
        welfare_impact.append(float(reform_result.welfare_impact - baseline_result.welfare_impact))
        deterrence_rate.append(float(params.deterrence_elasticity))

    return {
        "testing_uptake": np.asarray(testing_uptake, dtype=float),
        "premium_divergence": np.asarray(premium_divergence, dtype=float),
        "welfare_impact": np.asarray(welfare_impact, dtype=float),
        "deterrence_rate": np.asarray(deterrence_rate, dtype=float),
    }


def compare_to_targets(
    simulations: dict[str, np.ndarray], targets: dict[str, dict]
) -> dict[str, dict]:
    """Compare simulated outputs to empirical targets."""
    comparisons = {}

    for outcome, target in targets.items():
        if outcome not in simulations:
            continue

        sim_values = simulations[outcome]
        within_ci = np.sum(
            (sim_values >= target["ci_lower"]) & (sim_values <= target["ci_upper"])
        ) / len(sim_values)
        sim_mean = float(np.mean(sim_values))
        bias = (sim_mean - target["value"]) / target["value"]

        comparisons[outcome] = {
            "target_value": target["value"],
            "target_ci": [target["ci_lower"], target["ci_upper"]],
            "sim_mean": sim_mean,
            "sim_sd": float(np.std(sim_values)),
            "sim_ci": [
                float(np.percentile(sim_values, 2.5)),
                float(np.percentile(sim_values, 97.5)),
            ],
            "coverage": float(within_ci),
            "bias": float(bias),
            "source": target["source"],
        }

    return comparisons


def generate_plots_data(
    simulations: dict[str, np.ndarray], targets: dict[str, dict], output_dir: Path
) -> None:
    """Generate compact JSON data for posterior predictive plots."""
    plot_data = {}

    for outcome, values in simulations.items():
        plot_data[outcome] = {
            "values": values.tolist()[:100],
            "mean": float(np.mean(values)),
            "ci": [
                float(np.percentile(values, 2.5)),
                float(np.percentile(values, 97.5)),
            ],
        }

        if outcome in targets:
            plot_data[outcome]["target"] = targets[outcome]["value"]
            plot_data[outcome]["target_ci"] = [
                targets[outcome]["ci_lower"],
                targets[outcome]["ci_upper"],
            ]

    (output_dir / "plot_data.json").write_text(
        json.dumps(plot_data, indent=2) + "\n", encoding="utf-8"
    )


def generate_report(comparisons: dict[str, dict], n_draws: int, output_dir: Path) -> str:
    """Generate markdown report."""
    lines = [
        "# Posterior Predictive Check Report",
        "",
        f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Prior draws:** {n_draws}",
        "",
        "## Overview",
        "",
        "Posterior predictive checks compare model outputs generated from prior draws against empirical targets.",
        "These outputs now come from the active policy pipeline rather than synthetic placeholder equations.",
        "",
        "## Results by Outcome",
        "",
    ]

    overall_pass = True

    for outcome, comp in comparisons.items():
        coverage_status = "[PASS]" if comp["coverage"] > 0.5 else "[WARN]"
        bias_status = "[PASS]" if abs(comp["bias"]) < 0.2 else "[WARN]"

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
            lines.append("**[WARN] Note:** Poor calibration. Consider adjusting priors.")
            lines.append("")

    lines.append("## Overall Assessment")
    lines.append("")

    if overall_pass:
        lines.append(
            "[PASS] **All outcomes well-calibrated.** Priors are reasonably consistent with empirical evidence."
        )
    else:
        lines.append("[WARN] **Some outcomes are poorly calibrated.** Consider prior adjustments:")
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
    lines.append("4. Document prior adjustments in the decision log")

    return "\n".join(lines)


def main() -> None:
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

    logger.info("Starting Posterior Predictive Checks")
    logger.info(f"Number of draws: {args.n_draws}")
    logger.info(f"Random seed: {args.seed}")
    logger.info(f"Output directory: {output_dir}")

    logger.info("Drawing from priors...")
    prior_draws = {}
    for prior_name in PRIORS:
        prior_draws[prior_name] = draw_from_prior(prior_name, args.n_draws, args.seed)
        logger.debug(
            f"  {prior_name}: mean={np.mean(prior_draws[prior_name]):.3f}, sd={np.std(prior_draws[prior_name]):.3f}"
        )

    logger.info("Simulating model outputs...")
    simulations = simulate_model_outputs(prior_draws, args.n_draws)

    for outcome, values in simulations.items():
        logger.info(
            f"  {outcome}: mean={np.mean(values):.3f}, 95% CI=[{np.percentile(values, 2.5):.3f}, {np.percentile(values, 97.5):.3f}]"
        )

    logger.info("Comparing to empirical targets...")
    comparisons = compare_to_targets(simulations, EMPIRICAL_TARGETS)

    for outcome, comp in comparisons.items():
        coverage_status = "[PASS]" if comp["coverage"] > 0.5 else "[WARN]"
        bias_status = "[PASS]" if abs(comp["bias"]) < 0.2 else "[WARN]"
        logger.info(
            f"  {outcome}: Coverage={comp['coverage']:.1%} {coverage_status}, Bias={comp['bias']:+.1%} {bias_status}"
        )

    logger.info("Generating plot data...")
    generate_plots_data(simulations, EMPIRICAL_TARGETS, output_dir)

    logger.info("Generating report...")
    report = generate_report(comparisons, args.n_draws, output_dir)
    report_file = output_dir / "REPORT.md"
    report_file.write_text(report, encoding="utf-8")

    logger.success("Posterior predictive checks complete!")
    logger.info(f"Report: {report_file}")


if __name__ == "__main__":
    main()
