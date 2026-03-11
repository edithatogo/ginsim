from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger

from src.model.parameters import (
    ModelParameters,
    PolicyConfig,
    load_jurisdiction_parameters,
)
from src.model.pipeline import evaluate_single_policy
from src.model.policy_loader import load_policies_config
from src.utils.logging_config import setup_logging
from src.utils.manifest import write_manifest
from src.utils.posterior import deterministic_subsample, load_draws_npy
from src.utils.sampling import SamplingMode, select_draw

setup_logging(level="INFO")


def get_policies_path(jurisdiction: str) -> Path:
    mapping = {
        "australia": Path("configs/policies_australia.yaml"),
        "new_zealand": Path("configs/policies_new_zealand.yaml"),
        "nz": Path("configs/policies_new_zealand.yaml"),
        "au": Path("configs/policies_australia.yaml"),
    }
    if jurisdiction not in mapping:
        msg = f"Unknown jurisdiction: {jurisdiction}. Use australia or new_zealand."
        raise ValueError(msg)
    return mapping[jurisdiction]


def maybe_load(path_str: str, n: int) -> list[dict[str, Any]] | None:
    if not path_str:
        return None
    path = Path(path_str)
    if not path.exists():
        return None
    return deterministic_subsample(load_draws_npy(path), n)


def _clip(value: float, lower: float, upper: float) -> float:
    return float(np.clip(value, lower, upper))


def _sample_model_parameters(
    base: ModelParameters,
    draw: dict[str, Any] | None,
    rng: np.random.Generator,
) -> ModelParameters:
    if draw:
        return base.model_copy(
            update={key: value for key, value in draw.items() if key in base.model_fields}
        )

    sampled = {
        "baseline_testing_uptake": _clip(
            rng.normal(base.baseline_testing_uptake, 0.03), 0.01, 0.99
        ),
        "deterrence_elasticity": _clip(rng.normal(base.deterrence_elasticity, 0.02), 0.0, 1.0),
        "moratorium_effect": _clip(rng.normal(base.moratorium_effect, 0.03), 0.0, 1.0),
        "adverse_selection_elasticity": max(
            0.0, rng.normal(base.adverse_selection_elasticity, 0.01)
        ),
        "demand_elasticity_high_risk": min(
            0.0,
            rng.normal(base.demand_elasticity_high_risk, 0.03),
        ),
        "baseline_loading": max(0.0, rng.normal(base.baseline_loading, 0.02)),
        "family_history_sensitivity": _clip(
            rng.normal(base.family_history_sensitivity, 0.03), 0.0, 1.0
        ),
        "proxy_substitution_rate": _clip(rng.normal(base.proxy_substitution_rate, 0.03), 0.0, 1.0),
        "pass_through_rate": _clip(rng.normal(base.pass_through_rate, 0.04), 0.0, 1.0),
        "research_participation_elasticity": min(
            0.0,
            rng.normal(base.research_participation_elasticity, 0.02),
        ),
        "enforcement_effectiveness": _clip(
            rng.normal(base.enforcement_effectiveness, 0.04),
            0.0,
            1.0,
        ),
        "complaint_rate": _clip(rng.normal(base.complaint_rate, 0.005), 0.0, 1.0),
    }
    return base.model_copy(update=sampled)


def _theta_row(params: ModelParameters) -> dict[str, dict[str, float]]:
    return {
        "mapping": {
            "baseline_testing_uptake": float(params.baseline_testing_uptake),
            "deterrence_elasticity": float(params.deterrence_elasticity),
            "moratorium_effect": float(params.moratorium_effect),
        },
        "behavior": {
            "baseline_testing_uptake": float(params.baseline_testing_uptake),
            "deterrence_elasticity": float(params.deterrence_elasticity),
            "moratorium_effect": float(params.moratorium_effect),
        },
        "clinical": {
            "research_participation_elasticity": float(params.research_participation_elasticity),
        },
        "insurance": {
            "adverse_selection_elasticity": float(params.adverse_selection_elasticity),
            "demand_elasticity_high_risk": float(params.demand_elasticity_high_risk),
            "baseline_loading": float(params.baseline_loading),
        },
        "passthrough": {
            "pass_through_rate": float(params.pass_through_rate),
        },
        "data_quality": {
            "family_history_sensitivity": float(params.family_history_sensitivity),
            "proxy_substitution_rate": float(params.proxy_substitution_rate),
            "research_participation_elasticity": float(params.research_participation_elasticity),
            "enforcement_effectiveness": float(params.enforcement_effectiveness),
            "complaint_rate": float(params.complaint_rate),
        },
    }


def _theta_matrix(rows: list[dict[str, float]]) -> np.ndarray:
    columns = sorted(rows[0])
    return np.array([[float(row[column]) for column in columns] for row in rows], dtype=float)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--jurisdiction", default="australia")
    parser.add_argument("--n_draws", type=int, default=500)
    parser.add_argument(
        "--sampling_mode",
        default="independent",
        choices=["independent", "common_index", "random"],
    )
    parser.add_argument("--out", default="outputs/runs/full_uncertainty")
    parser.add_argument("--mapping_posterior", default="")
    parser.add_argument("--behavior_posterior", default="")
    parser.add_argument("--clinical_posterior", default="")
    parser.add_argument("--insurance_posterior", default="")
    parser.add_argument("--passthrough_posterior", default="")
    parser.add_argument("--data_quality_posterior", default="")
    args = parser.parse_args()

    policies_path = get_policies_path(args.jurisdiction)
    policies_config = load_policies_config(policies_path)
    base_params = load_jurisdiction_parameters(args.jurisdiction)

    n_draws = args.n_draws
    mode: SamplingMode = args.sampling_mode
    rng = np.random.default_rng(20260307)

    posterior_groups = {
        "mapping": maybe_load(args.mapping_posterior, n_draws),
        "behavior": maybe_load(args.behavior_posterior, n_draws),
        "clinical": maybe_load(args.clinical_posterior, n_draws),
        "insurance": maybe_load(args.insurance_posterior, n_draws),
        "passthrough": maybe_load(args.passthrough_posterior, n_draws),
        "data_quality": maybe_load(args.data_quality_posterior, n_draws),
    }

    policies = [
        PolicyConfig(
            name=policy.name,
            description=policy.description,
            allow_genetic_test_results=policy.allow_genetic_test_results,
            allow_family_history=policy.allow_family_history,
            sum_insured_caps=policy.sum_insured_caps,
            enforcement_strength=policy.enforcement_strength,
        )
        for policy in policies_config.policies.values()
    ]

    rows: list[dict[str, Any]] = []
    theta_rows = {group: [] for group in posterior_groups}
    net_benefit_matrix = np.zeros((n_draws, len(policies)), dtype=float)

    for draw_index in range(n_draws):
        merged_draw: dict[str, Any] = {}
        for group_name, draws in posterior_groups.items():
            selected = (
                select_draw(draws, draw_index, n_draws, mode, rng) if draws is not None else None
            )
            if isinstance(selected, dict):
                merged_draw.update(selected)

        sampled_params = _sample_model_parameters(base_params, merged_draw or None, rng)
        theta_row = _theta_row(sampled_params)
        for group_name, values in theta_row.items():
            theta_rows[group_name].append(values)

        for policy_index, policy in enumerate(policies):
            result = evaluate_single_policy(sampled_params, policy)
            welfare_metrics = result.all_metrics["welfare"]
            net_benefit = float(welfare_metrics["net_welfare"])
            health_benefits = float(welfare_metrics["health_benefits"])
            avg_premium = float(result.insurance_premiums["avg_premium"])

            net_benefit_matrix[draw_index, policy_index] = net_benefit
            rows.append(
                {
                    "jurisdiction": policies_config.jurisdiction,
                    "domain": policies_config.domain,
                    "draw": draw_index,
                    "policy": policy.name,
                    "net_qalys": health_benefits / 50_000.0,
                    "avg_premium": avg_premium,
                    "nb": net_benefit,
                }
            )

    out_dir = (
        Path(args.out)
        / f"{policies_config.jurisdiction}_{pd.Timestamp.utcnow().strftime('%Y%m%dT%H%M%SZ')}"
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    write_manifest(
        out_dir,
        repo_root=Path(),
        jurisdiction=policies_config.jurisdiction,
        domain=policies_config.domain,
        policies_file=policies_path,
        base_config_file=Path("configs/base.yaml"),
        notes="Full uncertainty run using current pipeline evaluation with parameter perturbation fallback.",
        extra={"n_draws": n_draws, "sampling_mode": args.sampling_mode},
    )

    draws_df = pd.DataFrame(rows)
    draws_df.to_csv(out_dir / "full_uncertainty_draws.csv", index=False)
    np.save(out_dir / "net_benefit_matrix.npy", net_benefit_matrix)

    for group_name, values in theta_rows.items():
        if values:
            np.save(out_dir / f"theta_{group_name}.npy", _theta_matrix(values))

    summary = (
        draws_df.groupby("policy")
        .agg(
            nb_mean=("nb", "mean"),
            nb_p05=("nb", lambda series: float(np.quantile(series, 0.05))),
            nb_p95=("nb", lambda series: float(np.quantile(series, 0.95))),
        )
        .reset_index()
        .sort_values("nb_mean", ascending=False)
    )
    summary.to_csv(out_dir / "full_uncertainty_summary.csv", index=False)

    logger.info(f"Wrote results to: {out_dir}")
    logger.info(f"\n{summary.to_string(index=False)}")


if __name__ == "__main__":
    main()
