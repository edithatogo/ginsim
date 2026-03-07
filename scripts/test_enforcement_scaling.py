from src.model.module_enforcement import compute_optimal_enforcement
from src.model.parameters import ModelParameters, PolicyConfig


def test_enforcement_scaling():
    """
    Verify that enforcement logic scales correctly with budget.
    """
    params = ModelParameters(enforcement_budget=1000000.0, marginal_cost_enforcement=0.1)
    res_base = compute_optimal_enforcement(params, PolicyConfig(name="test", description="d"))

    params_rich = params.model_copy(update={"enforcement_budget": 5000000.0})
    res_rich = compute_optimal_enforcement(params_rich, PolicyConfig(name="test", description="d"))

    print(f"Base Optimal: {res_base.optimal_enforcement:.4f}")
    print(f"Rich Optimal: {res_rich.optimal_enforcement:.4f}")

    assert res_rich.optimal_enforcement >= res_base.optimal_enforcement


if __name__ == "__main__":
    test_enforcement_scaling()
    print("Enforcement Stress Test: PASS")
