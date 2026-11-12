from __future__ import annotations

import hypothesis.strategies as st
from hypothesis import given, settings

from src.model.parameters import PolicyConfig, get_default_parameters
from src.model.pipeline import evaluate_single_policy

# A strategy for base ModelParameters
params_strategy = st.builds(
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
                "research_participation_elasticity",
                "research_participation_value",
            ]
        ),
        values=st.floats(min_value=0.1, max_value=0.9),  # Safe range for stability
    ),
)


@given(params=params_strategy)
@settings(max_examples=30, deadline=None)
def test_welfare_monotonicity_pbt(params):
    # Standard policies
    sq = PolicyConfig(
        name="sq", description="SQ", allow_genetic_test_results=True, allow_family_history=True
    )
    moratorium = PolicyConfig(
        name="mor",
        description="Mor",
        allow_genetic_test_results=False,
        allow_family_history=True,
        sum_insured_caps={"life": 500000.0},
    )
    ban = PolicyConfig(
        name="ban", description="Ban", allow_genetic_test_results=False, allow_family_history=False
    )

    res_sq = evaluate_single_policy(params, sq)
    res_mor = evaluate_single_policy(params, moratorium)
    res_ban = evaluate_single_policy(params, ban)

    # Uptake Monotonicity: Ban >= Moratorium >= Status Quo
    # (Because protections remove deterrence)
    assert res_ban.testing_uptake >= res_mor.testing_uptake - 1e-6
    assert res_mor.testing_uptake >= res_sq.testing_uptake - 1e-6

    # Health Benefits Monotonicity: Ban >= Moratorium >= Status Quo
    # (Directly tied to uptake)
    assert (
        res_ban.all_metrics["welfare"]["health_benefits"]
        >= res_mor.all_metrics["welfare"]["health_benefits"] - 1e-6
    )
    assert (
        res_mor.all_metrics["welfare"]["health_benefits"]
        >= res_sq.all_metrics["welfare"]["health_benefits"] - 1e-6
    )


@given(params=params_strategy)
@settings(max_examples=30, deadline=None)
def test_premium_monotonicity_pbt(params):
    sq = PolicyConfig(name="sq", description="SQ", allow_genetic_test_results=True)
    ban = PolicyConfig(name="ban", description="Ban", allow_genetic_test_results=False)

    res_sq = evaluate_single_policy(params, sq)
    res_ban = evaluate_single_policy(params, ban)

    # Risk Rating (High/Low) should be 1.0 (no rating) or close to it in Ban
    # and significantly higher in Status Quo
    rr_sq = res_sq.insurance_premiums["risk_rating"]
    rr_ban = res_ban.insurance_premiums["risk_rating"]

    assert rr_sq >= rr_ban - 1e-6
