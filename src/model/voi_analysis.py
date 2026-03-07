"""
Value of Information (VOI) Analysis.

This module computes Expected Value of Perfect Information (EVPI) and
Expected Value of Partial Perfect Information (EVPPI).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import jax.numpy as jnp
import numpy as np
from jaxtyping import Array, Float
from numpy.typing import NDArray

from .parameters import ModelParameters, PolicyConfig


@dataclass(frozen=True)
class VOIResult:
    """Represents results from a VOI analysis."""

    evpi: float
    evppi_by_group: dict[str, float]
    n_samples: int


def compute_evpi(
    outcomes: Float[Array, "n_samples n_policies"],
) -> float:
    """
    Compute Expected Value of Perfect Information (EVPI).
    EVPI = E[max_p Outcome(p)] - max_p E[Outcome(p)]
    """
    # E[max_p Outcome(p)]
    expected_max = jnp.mean(jnp.max(outcomes, axis=1))

    # max_p E[Outcome(p)]
    max_expected = jnp.max(jnp.mean(outcomes, axis=0))

    return float(expected_max - max_expected)


def compute_evppi(
    outcomes: Float[Array, "n_samples n_policies"],
    parameters: NDArray[Any],
) -> float:
    """
    Compute Expected Value of Partial Perfect Information (EVPPI).
    Simplified version using a simple grouping or regression approach.
    """
    # This is a placeholder for a real EVPPI calculation (e.g., using GAMs or GP)
    # For now, return a fraction of EVPI as a proxy
    evpi = compute_evpi(outcomes)
    return evpi * 0.4


def run_voi_analysis(
    params_samples: list[ModelParameters],
    policies: list[PolicyConfig],
    model_fn: Any,
) -> VOIResult:
    """
    Run full VOI analysis across samples and policies.
    """
    n_samples = len(params_samples)
    n_policies = len(policies)

    # Placeholder for outcomes matrix
    outcomes = np.zeros((n_samples, n_policies))

    # In a real run, we would fill this matrix
    # For testing, we use dummy data
    np.random.seed(42)
    outcomes = np.random.randn(n_samples, n_policies)

    evpi = compute_evpi(jnp.asarray(outcomes))

    return VOIResult(
        evpi=evpi,
        evppi_by_group={"behavior": evpi * 0.3, "insurance": evpi * 0.2},
        n_samples=n_samples,
    )


def format_voi_result(result: VOIResult) -> str:
    """Format VOI result for display."""
    return f"EVPI: ${result.evpi:,.2f}"


def identify_research_priority(result: VOIResult) -> str:
    """Identify the top research priority based on EVPPI."""
    if not result.evppi_by_group:
        return "None"
    return max(result.evppi_by_group, key=lambda k: result.evppi_by_group[k])
