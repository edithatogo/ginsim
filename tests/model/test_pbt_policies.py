from __future__ import annotations

import hypothesis.strategies as st
import jax.numpy as jnp
from hypothesis import given, settings

from src.model.module_a_behavior import compute_testing_uptake
from src.model.module_c_insurance_eq import compute_equilibrium
from src.model.parameters import PolicyConfig, get_default_parameters

# Strategies for PolicyConfig
policy_strategy = st.builds(
    PolicyConfig,
    name=st.text(min_size=1),
    description=st.text(),
    allow_genetic_test_results=st.booleans(),
    allow_family_history=st.booleans(),
    enforcement_strength=st.floats(min_value=0.0, max_value=1.0),
    penalty_max=st.floats(min_value=0.0, max_value=1e6),
    sum_insured_caps=st.one_of(
        st.none(),
        st.dictionaries(
            keys=st.sampled_from(["life", "tpd", "trauma", "income_protection"]),
            values=st.floats(min_value=1000.0, max_value=1e7),
        ),
    ),
    taper_range=st.floats(min_value=0.0, max_value=1e6),
    penalty_type=st.sampled_from(["civil", "criminal"]),
)

# Strategies for ModelParameters (subset of fields that are safe to randomize)
parameter_strategy = st.builds(
    get_default_parameters().model_copy,
    update=st.dictionaries(
        keys=st.sampled_from(
            [
                "baseline_testing_uptake",
                "deterrence_elasticity",
                "moratorium_effect",
                "adverse_selection_elasticity",
                "demand_elasticity_high_risk",
                "baseline_loading",
                "family_history_sensitivity",
                "proxy_substitution_rate",
            ]
        ),
        # Most of these are expected to be between 0 and 1, or small negatives
        values=st.floats(min_value=0.01, max_value=0.99),
    ),
)


@given(policy=policy_strategy)
@settings(max_examples=50, deadline=None)
def test_uptake_stability_pbt(policy):
    params = get_default_parameters()
    uptake = compute_testing_uptake(params, policy)
    # Uptake must always be a probability in [0, 1]
    assert 0.0 <= float(uptake) <= 1.0


@given(
    params_update=st.dictionaries(
        keys=st.sampled_from(["demand_elasticity_high_risk"]),
        values=st.floats(min_value=-5.0, max_value=-0.01),
    )
)
@settings(max_examples=50, deadline=None)
def test_equilibrium_stability_pbt(params_update):
    params = get_default_parameters().model_copy(update=params_update)
    policy = PolicyConfig(name="test", description="test", allow_genetic_test_results=False)

    eq = compute_equilibrium(params, policy)
    # Premiums should be positive and finite
    assert float(eq.premium_high) > 0
    assert float(eq.premium_low) > 0
    assert not jnp.isnan(eq.premium_high)
