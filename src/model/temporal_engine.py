"""
Temporal Evolution Engine (Diamond Standard).

Simulates the 10-year trajectory of genetic insurance markets
using JAX-recursive state transitions.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import jax.numpy as jnp

from .parameters import ModelParameters, PolicyConfig
from .pipeline import evaluate_single_policy


@dataclass(frozen=True)
class TemporalState:
    """State vector for a single year in the simulation."""
    year: int
    uptake: Any
    premium_high: Any
    premium_low: Any
    net_welfare: Any


def simulate_evolution(
    params: ModelParameters,
    policy: PolicyConfig,
    n_years: int = 10,
    inflation_rate: float = 0.03,
    tech_drift: float = 0.02, # 2% annual increase in proxy accuracy
) -> list[TemporalState]:
    """
    Simulates the multi-year trajectory of the market.
    Currently implemented as a sequential loop for transparency,
    but utilizes JAX kernels internally.
    """
    history = []

    # Initial state from static evaluation
    current_params = params

    for t in range(n_years):
        # 1. Run full pipeline for current year
        res = evaluate_single_policy(current_params, policy)

        state = TemporalState(
            year=t,
            uptake=res.testing_uptake,
            premium_high=res.insurance_premiums["premium_high"],
            premium_low=res.insurance_premiums["premium_low"],
            net_welfare=res.welfare_impact
        )
        history.append(state)

        # 2. Transition: Update params for next year
        # - Inflation reduces the effective regulatory cap (if not indexed)
        # - Tech drift increases proxy substitution rate
        # - Cumulative uptake increases adverse selection pressure (simplified)

        new_proxy_rate = jnp.minimum(
            jnp.asarray(current_params.proxy_substitution_rate) * (1.0 + tech_drift),
            0.95
        )

        # Effective cap in next year (Real value declines)
        new_taper = jnp.asarray(getattr(current_params, "taper_range", 0.0)) * (1.0 - inflation_rate)

        current_params = current_params.model_copy(update={
            "proxy_substitution_rate": float(new_proxy_rate),
            "taper_range": float(new_taper)
        })

    return history
