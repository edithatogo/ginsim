from src.model.dcba_ledger import compute_dcba


def test_distributional_inequality_preference():
    """
    Verify that increasing distributional weights shifts preference
    towards high-stake groups correctly.
    """
    # Group A: Gain 100, Weight 1.0 -> 100
    # Group B: Gain 100, Weight 2.0 -> 200

    res_base = compute_dcba(0.6, 0.5, 0.5, 0.5, 0.0, 0.0, distributional_weight=1.0)
    res_weighted = compute_dcba(0.6, 0.5, 0.5, 0.5, 0.0, 0.0, distributional_weight=2.0)

    print(f"Base Net: {res_base.net_welfare:.2f}")
    print(f"Weighted Net: {res_weighted.net_welfare:.2f}")

    assert res_weighted.net_welfare == res_base.net_welfare * 2.0


if __name__ == "__main__":
    test_distributional_inequality_preference()
    print("Distributional Stress Test: PASS")
