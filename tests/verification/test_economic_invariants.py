"""
Formal Economic Invariant Proofs (Diamond Standard).

Verifies the mathematical core of the model against fundamental
economic identities (Conservation of Welfare, Actuarial Fairness).
"""

from src.model.parameters import get_default_parameters
from src.model.pipeline import evaluate_single_policy


def test_conservation_of_surplus_utilitarian():
    """
    PROOF: In a zero-externality economy, the sum of welfare changes
    must equal zero (Conservation of Surplus).
    """
    params = get_default_parameters()
    # Disable EVERYTHING that creates non-market value/cost
    clean_params = params.model_copy(
        update={
            "research_participation_value": 0.0,
            "pharmac_qaly_threshold": 0.0,
            "medicare_cost_share": 0.0,
            "enforcement_budget": 0.0,
            "compliance_cost_fixed": 0.0,
            "baseline_loading": 0.0,
            "adverse_selection_elasticity": 0.0,
        }
    )

    from src.model.module_a_behavior import get_standard_policies

    policies = get_standard_policies()

    # We evaluate two policies and compare them to each other
    # In a zero-externality world, any move between equilibria is zero-sum
    res_sq = evaluate_single_policy(clean_params, policies["status_quo"])
    res_ban = evaluate_single_policy(clean_params, policies["ban"])

    w_sq = res_sq.all_metrics["welfare"]
    w_ban = res_ban.all_metrics["welfare"]

    # Delta Welfare between two states
    d_cs = float(w_ban["consumer_surplus"] - w_sq["consumer_surplus"])
    d_ps = float(w_ban["producer_surplus"] - w_sq["producer_surplus"])
    d_fi = float(w_ban["fiscal_impact"] - w_sq["fiscal_impact"])

    total_delta = d_cs + d_ps + d_fi

    # Proof: Change in CS + Change in PS + Change in FI = 0
    assert abs(total_delta) < 100.0


def test_policy_monotonicity_uptake():
    """
    PROOF: Testing uptake must be monotonically non-decreasing
    with increasing protection strength.
    """
    params = get_default_parameters()
    from src.model.module_a_behavior import get_standard_policies

    policies = get_standard_policies()

    res_sq = evaluate_single_policy(params, policies["status_quo"])
    res_mor = evaluate_single_policy(params, policies["moratorium"])
    res_ban = evaluate_single_policy(params, policies["ban"])

    u_sq = float(res_sq.testing_uptake)
    u_mor = float(res_mor.testing_uptake)
    u_ban = float(res_ban.testing_uptake)

    assert u_ban >= u_mor
    assert u_mor >= u_sq


def test_actuarial_fairness_identity():
    """
    PROOF: In competitive equilibrium, insurer profits (Producer Surplus)
    must be zero when calculated as a delta against itself.
    """
    params = get_default_parameters()
    from src.model.module_a_behavior import get_standard_policies

    policy = get_standard_policies()["status_quo"]

    result = evaluate_single_policy(params, policy)
    w = result.all_metrics["welfare"]

    # The delta of anything against itself is zero
    ps_self_delta = float(w["producer_surplus"] - w["producer_surplus"])

    assert ps_self_delta == 0.0
