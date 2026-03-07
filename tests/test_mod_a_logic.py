"""
Property-based tests for Module A Behavior logic.
"""

import jax.numpy as jnp
from hypothesis import given, settings
from hypothesis import strategies as st

from src.model.module_a_behavior import compute_testing_probability


@settings(deadline=None)
@given(
    utility=st.floats(min_value=-1000.0, max_value=1000.0),
    scale=st.floats(min_value=0.1, max_value=10.0),
)
def test_probability_numerical_stability(utility, scale):
    """
    Property: Probability calculation must be stable even for extreme utility values.
    Should never return NaN or values outside [0, 1].
    """
    u_arr = jnp.array([utility], dtype=jnp.float32)
    prob = compute_testing_probability(u_arr, scale=scale)

    assert not jnp.isnan(prob).any()
    assert jnp.all(prob >= 0.0)
    assert jnp.all(prob <= 1.0)


@settings(deadline=None)
@given(
    utility=st.floats(min_value=0.01, max_value=100.0),
)
def test_rational_participation(utility):
    """
    Property: Positive utility MUST yield probability > 0.5.
    """
    u_arr = jnp.array([utility], dtype=jnp.float32)
    prob = compute_testing_probability(u_arr, scale=1.0)

    assert jnp.all(prob > 0.5)


@settings(deadline=None)
@given(
    utility=st.floats(min_value=-100.0, max_value=-0.01),
)
def test_rational_non_participation(utility):
    """
    Property: Negative utility MUST yield probability < 0.5.
    """
    u_arr = jnp.array([utility], dtype=jnp.float32)
    prob = compute_testing_probability(u_arr, scale=1.0)

    assert jnp.all(prob < 0.5)
