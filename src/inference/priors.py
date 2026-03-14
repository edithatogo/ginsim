"""
Bayesian prior helpers for uncertainty analysis.
"""

from __future__ import annotations

import jax.numpy as jnp
import jax.random as jr
from jaxtyping import Array


class BayesianPriorSuite:
    """Simple jurisdiction-aware priors for key elasticities."""

    @staticmethod
    def draw_adverse_selection_elasticity(key: Array, n_draws: int) -> Array:
        """Draw positive magnitudes that callers can sign by convention."""
        log_samples = -jr.normal(key, (n_draws,)) * 0.3 - 1.2
        return jnp.exp(log_samples)

    @staticmethod
    def draw_deterrence_elasticity(key: Array, n_draws: int) -> Array:
        """Gamma prior with mean near 0.2."""
        return jr.gamma(key, 2.0, shape=(n_draws,)) * 0.1

    @staticmethod
    def draw_equity_factor(key: Array, n_draws: int, jurisdiction: str) -> Array:
        """Jurisdiction-specific equity weighting prior."""
        base_map = {
            "new_zealand": 1.35,
            "australia": 1.15,
            "us": 1.40,
            "uk": 1.20,
            "canada": 1.10,
        }
        mu = base_map.get(jurisdiction.lower(), 1.0)
        return mu + jr.normal(key, (n_draws,)) * 0.05


def sample_parameter_matrix(
    key: Array, n_draws: int, jurisdiction: str = "australia"
) -> dict[str, Array]:
    """Generate the prior-draw matrix consumed by the sensitivity engine."""
    keys = jr.split(key, 5)
    suite = BayesianPriorSuite()
    return {
        "adverse_selection_elasticity": suite.draw_adverse_selection_elasticity(keys[0], n_draws),
        "deterrence_elasticity": suite.draw_deterrence_elasticity(keys[1], n_draws),
        "equity_factor": suite.draw_equity_factor(keys[2], n_draws, jurisdiction),
    }
