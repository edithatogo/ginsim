"""
Shared helpers for dashboard pages and deployment wrappers.
"""

from __future__ import annotations

from src.model.module_a_behavior import get_standard_policies
from src.model.parameters import ModelParameters, PolicyConfig
from src.model.pipeline import PolicyEvaluationResult, evaluate_single_policy

_SANDBOX_PENALTY_MAX = 1_000_000.0


def build_sandbox_policy(
    enforcement_strength: float,
    penalty_rate: float,
) -> PolicyConfig:
    """Build the custom dashboard sandbox policy from slider inputs."""
    moratorium = get_standard_policies()["moratorium"]
    return PolicyConfig(
        name="sandbox_policy",
        description="Custom Australian dashboard sandbox policy",
        allow_genetic_test_results=moratorium.allow_genetic_test_results,
        allow_family_history=moratorium.allow_family_history,
        sum_insured_caps=moratorium.sum_insured_caps,
        enforcement_strength=enforcement_strength,
        penalty_max=penalty_rate * _SANDBOX_PENALTY_MAX,
        penalty_type="civil",
    )


def evaluate_sandbox_policy(
    baseline_testing_uptake: float,
    deterrence_elasticity: float,
    enforcement_effectiveness: float,
    penalty_rate: float,
) -> PolicyEvaluationResult:
    """Evaluate the dashboard sandbox using the core policy pipeline."""
    from src.model.parameters import load_jurisdiction_parameters
    
    # Use Australia as the sandbox base population
    base_params = load_jurisdiction_parameters("australia")
    params = base_params.model_copy(update={
        "baseline_testing_uptake": baseline_testing_uptake,
        "deterrence_elasticity": deterrence_elasticity,
        "enforcement_effectiveness": enforcement_effectiveness,
    })
    policy = build_sandbox_policy(
        enforcement_strength=enforcement_effectiveness,
        penalty_rate=penalty_rate,
    )
    return evaluate_single_policy(params, policy)


def format_positive_share(positive_count: int, total_count: int) -> str:
    """Format a policy share defensively for dashboard summaries."""
    if total_count <= 0:
        return "0%"
    share = positive_count / total_count
    return f"{share:.0%}"
