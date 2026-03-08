from src.model.module_a_behavior import compute_testing_uptake
from src.model.module_d_proxy import compute_proxy_substitution_effect
from src.model.parameters import ModelParameters, get_default_parameters, PolicyConfig


def test_game_engine_integration():
    """
    Ensure Modules A and D integrate without numerical collapse.
    """
    params = get_default_parameters()
    baseline = PolicyConfig(name="base", description="d", allow_genetic_test_results=True)
    ban = PolicyConfig(name="ban", description="d", allow_genetic_test_results=False)

    # Uptake shift
    uptake_base = compute_testing_uptake(params, baseline)
    uptake_ban = compute_testing_uptake(params, ban)

    # Proxy shift
    proxy_res = compute_proxy_substitution_effect(params, baseline, ban)

    print(f"Uptake Ban: {uptake_ban:.4f}")
    print(f"Info Gap: {proxy_res['residual_information_gap']:.4f}")

    assert uptake_ban > uptake_base
    assert proxy_res["residual_information_gap"] > 0


if __name__ == "__main__":
    test_game_engine_integration()
    print("Integration Stress Test: PASS")
