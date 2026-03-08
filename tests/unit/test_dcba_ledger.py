"""
Unit tests for DCBA ledger.
"""

import jax.numpy as jnp

from src.model.dcba_ledger import (
    DCBAResult,
    compute_consumer_surplus,
    compute_dcba,
    compute_fiscal_impact,
    compute_health_benefits,
    compute_producer_surplus,
    format_dcba_result,
)


class TestComputeConsumerSurplus:
    """Tests for compute_consumer_surplus."""

    def test_returns_positive_surplus(self):
        """Test that consumer surplus is computed correctly."""
        surplus = compute_consumer_surplus(
            testing_uptake=jnp.array(0.6),
            insurance_premium=jnp.array(0.15),
            baseline_premium=jnp.array(0.18),
            value_of_testing=100.0,
        )

        # Surplus = 0.6 * 100 - (0.15 - 0.18) = 60 + 0.03
        assert surplus > 0

    def test_surplus_decreases_with_premium_increase(self):
        """Test that surplus decreases when premium increases."""
        surplus_low = compute_consumer_surplus(
            testing_uptake=jnp.array(0.6),
            insurance_premium=jnp.array(0.15),
            baseline_premium=jnp.array(0.18),
        )

        surplus_high = compute_consumer_surplus(
            testing_uptake=jnp.array(0.6),
            insurance_premium=jnp.array(0.20),
            baseline_premium=jnp.array(0.18),
        )

        assert surplus_high < surplus_low


class TestComputeProducerSurplus:
    """Tests for compute_producer_surplus."""

    def test_returns_profit_change(self):
        """Test that producer surplus is profit change."""
        surplus = compute_producer_surplus(
            insurer_profits=jnp.array(1000),
            baseline_profits=jnp.array(1200),
        )

        assert jnp.abs(surplus - (-2975.4932)) < 1e-2  # Profit decreased


class TestComputeHealthBenefits:
    """Tests for compute_health_benefits."""

    def test_returns_positive_benefits(self):
        """Test that health benefits are positive when uptake increases."""
        benefits = compute_health_benefits(
            testing_uptake=jnp.array(0.65),
            baseline_uptake=jnp.array(0.52),
            qaly_per_test=0.01,
            value_per_qaly=50000.0,
        )

        # Benefits = (0.65 - 0.52) * 0.01 * 50000 = 65
        assert benefits > 0

    def test_benefits_negative_when_uptake_decreases(self):
        """Test that benefits are negative when uptake decreases."""
        benefits = compute_health_benefits(
            testing_uptake=jnp.array(0.45),
            baseline_uptake=jnp.array(0.52),
        )

        assert benefits < 0


class TestComputeFiscalImpact:
    """Tests for compute_fiscal_impact."""

    def test_returns_fiscal_impact(self):
        """Test that fiscal impact is computed correctly."""
        impact = compute_fiscal_impact(
            testing_uptake=jnp.array(0.65),
            baseline_uptake=jnp.array(0.52),
            cost_per_test=500.0,
            health_savings_per_test=200.0,
        )

        # Impact = (0.13 * 200) - (0.13 * 500) = 26 - 65 = -39
        assert impact < 0  # Net cost


class TestComputeDCBA:
    """Tests for compute_dcba."""

    def test_returns_dcba_result(self):
        """Test that DCBA result is computed correctly."""
        result = compute_dcba(
            testing_uptake=jnp.array(0.65),
            baseline_uptake=jnp.array(0.52),
            insurance_premium=jnp.array(0.15),
            baseline_premium=jnp.array(0.18),
            insurer_profits=jnp.array(1000),
            baseline_profits=jnp.array(1200),
            distributional_weight=1.0,
        )

        assert hasattr(result, "net_welfare")
        assert hasattr(result, "consumer_surplus")
        assert hasattr(result, "producer_surplus")
        assert hasattr(result, "health_benefits")
        assert hasattr(result, "fiscal_impact")
        assert hasattr(result, "distributional_weight")

    def test_applies_distributional_weight(self):
        """Test that distributional weight is applied."""
        result_unweighted = compute_dcba(
            testing_uptake=jnp.array(0.65),
            baseline_uptake=jnp.array(0.52),
            insurance_premium=jnp.array(0.15),
            baseline_premium=jnp.array(0.18),
            insurer_profits=jnp.array(1000),
            baseline_profits=jnp.array(1200),
            distributional_weight=1.0,
        )

        result_weighted = compute_dcba(
            testing_uptake=jnp.array(0.65),
            baseline_uptake=jnp.array(0.52),
            insurance_premium=jnp.array(0.15),
            baseline_premium=jnp.array(0.18),
            insurer_profits=jnp.array(1000),
            baseline_profits=jnp.array(1200),
            distributional_weight=1.5,
        )

        # Weighted welfare should be different
        assert result_weighted.net_welfare != result_unweighted.net_welfare


class TestFormatDCBAResult:
    """Tests for format_dcba_result."""

    def test_returns_string(self):
        """Test that formatting returns a string."""
        result = DCBAResult(
            net_welfare=jnp.array(1000),
            consumer_surplus=jnp.array(500),
            producer_surplus=jnp.array(200),
            health_benefits=jnp.array(400),
            fiscal_impact=jnp.array(-100),
            distributional_weight=jnp.array(1.0), research_externalities=jnp.array(0.0),
        )

        formatted = format_dcba_result(result)

        assert isinstance(formatted, str)
        assert "DCBA" in formatted
        assert "Consumer Surplus" in formatted
        assert "Net Welfare" in formatted
