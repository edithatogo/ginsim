"""
Unit tests for Module C: Insurance Equilibrium.
"""

import jax.numpy as jnp

from src.model.module_c_insurance_eq import (
    compute_demand,
    compute_equilibrium,
    compute_expected_profit,
    compute_premium_divergence,
    compute_risk_premium,
    get_standard_risk_parameters,
    pooling_equilibrium,
    separating_equilibrium,
    zero_profit_premium,
)
from src.model.parameters import ModelParameters, PolicyConfig


class TestRiskPremium:
    """Tests for compute_risk_premium."""

    def test_premium_positive(self):
        """Test that premium is always positive."""
        premium = compute_risk_premium(risk_probability=0.1, sum_insured=1.0, loading=0.15)
        assert premium > 0.0

    def test_premium_increases_with_risk(self):
        """Test that premium increases with risk probability."""
        premium_low = compute_risk_premium(risk_probability=0.1)
        premium_high = compute_risk_premium(risk_probability=0.3)
        assert premium_high > premium_low

    def test_premium_increases_with_loading(self):
        """Test that premium increases with loading."""
        premium_no_loading = compute_risk_premium(risk_probability=0.1, loading=0.0)
        premium_with_loading = compute_risk_premium(risk_probability=0.1, loading=0.15)
        assert premium_with_loading > premium_no_loading


class TestDemand:
    """Tests for compute_demand."""

    def test_demand_bounded(self):
        """Test that demand is bounded [0, 1]."""
        for premium in [0.01, 0.1, 0.5, 1.0, 2.0]:
            demand = compute_demand(premium=premium)
            assert 0.0 <= demand <= 1.0

    def test_demand_decreases_with_premium(self):
        """Test that demand decreases as premium increases."""
        demand_low = compute_demand(premium=0.05)
        demand_high = compute_demand(premium=0.2)
        assert demand_high < demand_low

    def test_demand_more_elastic_for_high_risk(self):
        """Test that high-risk individuals have more elastic demand."""
        params = ModelParameters()

        # High-risk should be more sensitive to price
        demand_high_risk = compute_demand(
            premium=0.15,
            price_elasticity=params.demand_elasticity_high_risk,
        )
        demand_low_risk = compute_demand(premium=0.15)

        # With negative elasticity, more negative = more elastic
        # At higher premiums, high-risk should have lower demand
        assert demand_high_risk <= demand_low_risk


class TestExpectedProfit:
    """Tests for compute_expected_profit."""

    def test_zero_profit_at_fair_premium(self):
        """Test that profit is zero at actuarially fair premium."""
        risk = 0.1
        premium = zero_profit_premium(risk)
        profit = compute_expected_profit(premium, risk)

        # Should be very close to zero
        assert jnp.abs(profit) < 1e-6

    def test_positive_profit_above_fair_premium(self):
        """Test that profit is positive when premium > fair premium."""
        risk = 0.1
        fair_premium = zero_profit_premium(risk)

        profit = compute_expected_profit(fair_premium * 1.2, risk)
        assert profit > 0.0

    def test_negative_profit_below_fair_premium(self):
        """Test that profit is negative when premium < fair premium."""
        risk = 0.1
        fair_premium = zero_profit_premium(risk)

        profit = compute_expected_profit(fair_premium * 0.8, risk)
        assert profit < 0.0


class TestSeparatingEquilibrium:
    """Tests for separating_equilibrium."""

    def test_premiums_differ_by_risk(self):
        """Test that premiums differ by risk type."""
        params = ModelParameters()

        eq = separating_equilibrium(params, risk_high=0.3, risk_low=0.1)

        assert eq.premium_high_risk > eq.premium_low_risk

    def test_profits_near_zero(self):
        """Test that insurer profits are near zero."""
        params = ModelParameters()

        eq = separating_equilibrium(params, risk_high=0.3, risk_low=0.1)

        assert jnp.abs(eq.insurer_profits) < 0.01

    def test_convergence(self):
        """Test that separating equilibrium always converges."""
        params = ModelParameters()

        eq = separating_equilibrium(params, risk_high=0.3, risk_low=0.1)

        assert eq.converged
        assert eq.iterations == 1  # Closed form solution


class TestPoolingEquilibrium:
    """Tests for pooling_equilibrium."""

    def test_same_premium_for_all(self):
        """Test that pooling has same premium for all risk types."""
        params = ModelParameters()

        eq = pooling_equilibrium(params, risk_high=0.3, risk_low=0.1)

        assert jnp.isclose(eq.premium_high_risk, eq.premium_low_risk)

    def test_premium_between_risk_types(self):
        """Test that pooling premium is between high and low risk premiums."""
        params = ModelParameters()

        eq_sep = separating_equilibrium(params, risk_high=0.3, risk_low=0.1)
        eq_pool = pooling_equilibrium(params, risk_high=0.3, risk_low=0.1)

        # Pooling premium should be between separating premiums
        assert eq_pool.premium_high_risk >= eq_sep.premium_low_risk
        assert eq_pool.premium_high_risk <= eq_sep.premium_high_risk

    def test_convergence(self):
        """Test that pooling equilibrium converges."""
        params = ModelParameters()

        eq = pooling_equilibrium(params, risk_high=0.3, risk_low=0.1)

        assert eq.converged


class TestComputeEquilibrium:
    """Tests for compute_equilibrium."""

    def test_separating_with_information(self):
        """Test that full information leads to separating equilibrium."""
        params = ModelParameters()

        policy = PolicyConfig(
            name="full_info",
            description="Full information",
            allow_genetic_test_results=True,
        )

        eq = compute_equilibrium(params, policy, risk_high=0.3, risk_low=0.1)

        # Should have different premiums
        assert eq.premium_high_risk > eq.premium_low_risk

    def test_pooling_without_information(self):
        """Test that no information leads to pooling equilibrium."""
        params = ModelParameters()

        policy = PolicyConfig(
            name="no_info",
            description="No information",
            allow_genetic_test_results=False,
        )

        eq = compute_equilibrium(params, policy, risk_high=0.3, risk_low=0.1)

        # Should have same premiums
        assert jnp.isclose(eq.premium_high_risk, eq.premium_low_risk)


class TestPremiumDivergence:
    """Tests for compute_premium_divergence."""

    def test_divergence_structure(self):
        """Test that divergence output has correct structure."""
        params = ModelParameters()

        policies = {
            "status_quo": PolicyConfig(
                name="status_quo",
                description="Status quo",
                allow_genetic_test_results=True,
            ),
            "ban": PolicyConfig(
                name="ban",
                description="Ban",
                allow_genetic_test_results=False,
            ),
        }

        divergence = compute_premium_divergence(
            params,
            policies["status_quo"],
            policies["ban"],
        )

        assert "avg_premium_baseline" in divergence
        assert "avg_premium_reform" in divergence
        assert "absolute_divergence" in divergence
        assert "relative_divergence" in divergence
        assert "risk_rating_baseline" in divergence
        assert "risk_rating_reform" in divergence

    def test_ban_reduces_risk_rating(self):
        """Test that ban reduces risk rating (premium differentiation)."""
        params = ModelParameters()

        status_quo = PolicyConfig(
            name="status_quo",
            description="Status quo",
            allow_genetic_test_results=True,
        )

        ban = PolicyConfig(
            name="ban",
            description="Ban",
            allow_genetic_test_results=False,
        )

        divergence = compute_premium_divergence(params, status_quo, ban)

        # Ban should reduce risk rating (less differentiation)
        assert divergence["risk_rating_reform"] < divergence["risk_rating_baseline"]


class TestGetStandardRiskParameters:
    """Tests for get_standard_risk_parameters."""

    def test_returns_all_parameters(self):
        """Test that all risk parameters are returned."""
        params = get_standard_risk_parameters()

        assert "risk_high" in params
        assert "risk_low" in params
        assert "proportion_high" in params

    def test_parameters_are_reasonable(self):
        """Test that parameters are reasonable values."""
        params = get_standard_risk_parameters()

        assert 0.0 < params["risk_low"] < params["risk_high"] < 1.0
        assert 0.0 < params["proportion_high"] < 1.0
