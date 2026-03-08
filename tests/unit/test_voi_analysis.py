"""
Unit tests for Value of Information (VOI) Analysis.
"""

import jax.numpy as jnp
import numpy as np

from src.model.parameters import PolicyConfig, get_default_parameters
from src.model.voi_analysis import (
    VOIResult,
    compute_evpi,
    compute_evppi,
    format_voi_result,
    identify_research_priority,
    run_voi_analysis,
)


class TestComputeEVPI:
    """Tests for compute_evpi."""

    def test_returns_positive_evpi(self):
        """Test that EVPI is positive for varied outcomes."""
        # [n_samples, n_policies]
        outcomes = jnp.array(
            [
                [100.0, 80.0],
                [120.0, 90.0],
                [110.0, 85.0],
            ]
        )
        evpi = compute_evpi(outcomes)
        assert evpi >= 0.0

    def test_evpi_zero_when_no_uncertainty(self):
        """Test that EVPI is zero when all samples are identical."""
        outcomes = jnp.array(
            [
                [100.0, 80.0],
                [100.0, 80.0],
                [100.0, 80.0],
            ]
        )
        evpi = compute_evpi(outcomes)
        assert abs(evpi) < 1e-5


class TestComputeEVPPi:
    """Tests for compute_evppi."""

    def test_returns_evppi_by_group(self):
        """Test that EVPPI returns a reasonable value."""
        np.random.seed(42)
        outcomes = jnp.asarray(np.random.randn(100, 2))
        parameters = np.random.randn(100, 3)

        evppi = compute_evppi(outcomes, parameters)
        assert isinstance(float(evppi), float)


class TestIdentifyResearchPriority:
    """Tests for identify_research_priority."""

    def test_returns_highest_evppi(self):
        """Test that it identifies the group with max EVPPI."""
        result = VOIResult(
            evpi=1000.0,
            evppi_by_group={"group1": 100.0, "group2": 200.0, "group3": 150.0},
            n_samples=100,
        )
        priority = identify_research_priority(result)
        assert priority == "group2"


class TestRunVOIAnalysis:
    """Tests for run_voi_analysis."""

    def test_returns_voi_result(self):
        """Test the full analysis orchestration."""
        params_samples = [get_default_parameters() for _ in range(5)]
        policies = [
            PolicyConfig(name="p1", description="d1"),
            PolicyConfig(name="p2", description="d2"),
        ]

        def mock_model(p, pol):
            return 100.0

        result = run_voi_analysis(params_samples, policies, mock_model)

        assert isinstance(result, VOIResult)
        assert result.evpi >= 0
        assert "behavior" in result.evppi_by_group


class TestFormatVOIResult:
    """Tests for format_voi_result."""

    def test_returns_string(self):
        """Test that formatting returns a string."""
        result = VOIResult(evpi=1000.0, evppi_by_group={"group1": 500.0}, n_samples=100)

        formatted = format_voi_result(result)

        assert isinstance(formatted, str)
        assert "EVPI" in formatted
