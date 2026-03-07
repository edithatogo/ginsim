"""
Property-based tests for Module E Enforcement & Compliance logic.
"""

import jax.numpy as jnp
from hypothesis import given, settings
from hypothesis import strategies as st

from src.model.module_enforcement import (
    _compute_compliance_decision_jit,
    _compute_expected_penalty_jit,
)


@settings(deadline=None)
@given(
    penalty_max=st.floats(min_value=1e-5, max_value=1e9),
    detection_prob=st.floats(min_value=1e-10, max_value=1.0),
    effectiveness=st.floats(min_value=1e-10, max_value=1.0),
)
def test_expected_penalty_properties(penalty_max, detection_prob, effectiveness):
    """
    Property: Expected penalty should be linear and non-negative.
    """
    res = _compute_expected_penalty_jit(penalty_max, detection_prob, effectiveness)
    assert res >= 0.0
    if penalty_max > 0 and detection_prob > 0 and effectiveness > 0:
        assert res > 0.0


@settings(deadline=None)
@given(
    expected_penalty=st.floats(min_value=0.0, max_value=1e9),
    compliance_cost=st.floats(min_value=0.0, max_value=1e9),
)
def test_compliance_stability(expected_penalty, compliance_cost):
    """
    Property: Compliance decision should be stable even for massive penalty/cost differences.
    """
    res = _compute_compliance_decision_jit(expected_penalty, compliance_cost)
    assert not jnp.isnan(res)
    assert 0.0 <= res <= 1.0


@settings(deadline=None)
@given(
    cost=st.floats(min_value=1000.0, max_value=10000.0),
    penalty_low=st.floats(min_value=0.0, max_value=500.0),
    penalty_high=st.floats(min_value=20000.0, max_value=100000.0),
)
def test_deterrence_monotonicity(cost, penalty_low, penalty_high):
    """
    Property: Higher expected penalty MUST yield higher compliance probability.
    """
    compliance_low = _compute_compliance_decision_jit(penalty_low, cost)
    compliance_high = _compute_compliance_decision_jit(penalty_high, cost)

    assert compliance_high > compliance_low
