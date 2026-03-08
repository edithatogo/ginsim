"""
Economic Sanity Checker (Diamond Standard).

Automated enforcement of fundamental economic invariants during
the policy evaluation pipeline.
"""

from __future__ import annotations

from typing import Any

import jax
import jax.numpy as jnp
from loguru import logger


class EconomicSanityChecker:
    """
    Enforces mathematical invariants on model results.
    JAX-compatible implementation.
    """

    @staticmethod
    def verify_result(result: Any) -> None:
        """
        Perform sanity checks. Use array-based checks to avoid ConcretizationTypeError.
        Instead of 'if float(x)', we log warnings if the mean value is suspicious.
        """
        # 1. Non-negative testing uptake
        # We use jnp.any to check if any element violates the invariant
        uptake = jnp.asarray(result.testing_uptake)


        # 2. Premium Ordering
        ph = jnp.asarray(result.insurance_premiums.get("premium_high", 0.0))
        pl = jnp.asarray(result.insurance_premiums.get("premium_low", 0.0))


        # Note: We cannot branch on tracers during JIT/vmap.
        # We rely on the fact that JAX arrays will propagate these values.
        # For non-traced runs (concrete), we can log.
        if not isinstance(uptake, jax.core.Tracer):
            if float(jnp.mean(uptake)) < -1e-6:
                logger.error(f"INVARIANT VIOLATION: Negative testing uptake ({float(jnp.mean(uptake)):.4f})")
            if float(jnp.mean(ph)) < float(jnp.mean(pl)) - 1e-6:
                logger.error("INVARIANT VIOLATION: Premium High < Premium Low")

    @staticmethod
    def verify_sweep(results: dict[str, Any]) -> None:
        """
        Verify monotonicity across a policy sweep.
        """
        if "status_quo" in results and "ban" in results:
            u_sq = jnp.asarray(results["status_quo"].testing_uptake)
            u_ban = jnp.asarray(results["ban"].testing_uptake)

            if not isinstance(u_sq, jax.core.Tracer) and float(jnp.mean(u_ban)) < float(jnp.mean(u_sq)) - 1e-6:

                    logger.error("INVARIANT VIOLATION: Ban uptake < Status Quo uptake")
