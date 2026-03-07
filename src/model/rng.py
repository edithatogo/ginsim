"""
RNG management for reproducible computation.

Provides centralized random number generation with:
- Reproducible seeds across runs
- Common random numbers for policy comparison (variance reduction)
- Separate streams for different computation types

Uses attrs for immutable, JAX-compatible state.
"""

from __future__ import annotations

import attrs
import jax.random as jr
from jax import Array


@attrs.define(slots=True)
class RNGManager:
    """
    Centralized RNG management for reproducible JAX computation.

    Uses attrs for immutability and memory efficiency.

    Attributes:
        base_key: Base PRNGKey
        counters: Counters per stream

    Example:
        >>> rng = RNGManager()
        >>> mcmc_key = rng.get_key('mcmc')
        >>> policy_keys = rng.get_policy_comparison_keys(n_policies=3)
    """

    base_key: Array = attrs.field(factory=lambda: jr.PRNGKey(20260303))
    counters: dict[str, int] = attrs.field(factory=dict)

    def get_key(self, stream_name: str) -> Array:
        """
        Get unique key for a computation stream.

        Args:
            stream_name: Name of computation stream (e.g., 'mcmc', 'init')

        Returns:
            Unique PRNGKey for this stream
        """
        if stream_name not in self.counters:
            self.counters[stream_name] = 0

        self.base_key, subkey = jr.split(self.base_key)
        self.counters[stream_name] += 1

        return subkey

    def get_keys(self, stream_name: str, n_keys: int) -> list[Array]:
        """
        Get multiple unique keys for a computation stream.

        Args:
            stream_name: Name of computation stream
            n_keys: Number of keys needed

        Returns:
            List of unique PRNGKeys
        """
        keys = []
        for _ in range(n_keys):
            keys.append(self.get_key(f"{stream_name}_{len(keys)}"))
        return keys

    def get_policy_comparison_keys(self, n_policies: int) -> Array:
        """
        Get CRN keys for policy comparison (variance reduction).

        Uses common random numbers to reduce variance when comparing
        policy scenarios.

        Args:
            n_policies: Number of policy scenarios to compare

        Returns:
            Array of shape (n_policies, 2) with CRN keys

        Example:
            >>> rng = RNGManager()
            >>> keys = rng.get_policy_comparison_keys(3)  # status_quo, moratorium, ban
            >>> # All three policies use same random numbers → lower variance
        """
        key = self.get_key("policy_comparison")
        return jr.split(key, n_policies)

    def get_mcmc_keys(self, n_chains: int = 4) -> list[Array]:
        """
        Get keys for parallel MCMC chains.

        Args:
            n_chains: Number of MCMC chains

        Returns:
            List of PRNGKeys for each chain
        """
        key = self.get_key("mcmc")
        keys = jr.split(key, n_chains)
        return [keys[i] for i in range(n_chains)]

    def get_batch_keys(self, batch_size: int, stream_name: str = "batch") -> Array:
        """
        Get keys for batched/vectorized computation.

        Args:
            batch_size: Size of batch
            stream_name: Name of computation stream

        Returns:
            Array of shape (batch_size, 2) with keys
        """
        key = self.get_key(stream_name)
        return jr.split(key, batch_size)

    def reset(self) -> None:
        """Reset RNG to initial state (for testing)."""
        self.base_key = jr.PRNGKey(20260303)
        self.counters = {}

    def get_stats(self) -> dict[str, int | dict[str, int]]:
        """
        Get RNG usage statistics.

        Returns:
            Dict with key usage counts per stream
        """
        return {
            "total_splits": len(self.counters),
            "streams": self.counters.copy(),
        }


# Global RNG instance (for convenience)
_global_rng: RNGManager | None = None


def get_global_rng() -> RNGManager:
    """Get or create global RNG manager."""
    global _global_rng
    if _global_rng is None:
        _global_rng = RNGManager()
    return _global_rng


def reset_global_rng(seed: int = 20260303) -> None:
    """Reset global RNG with new seed."""
    global _global_rng
    _global_rng = RNGManager(base_key=jr.PRNGKey(seed))
