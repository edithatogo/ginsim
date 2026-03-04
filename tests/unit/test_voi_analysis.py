"""
Unit tests for VOI analysis.

Uses chex for JAX-specific testing utilities.
"""

import pytest
import numpy as np
import chex

from src.model.voi_analysis import (
    compute_evpi,
    compute_evppi,
    identify_research_priority,
    run_voi_analysis,
    format_voi_result,
    VOIResult,
)


class TestComputeEVPI:
    """Tests for compute_evpi."""
    
    def test_returns_positive_evpi(self):
        """Test that EVPI is non-negative."""
        net_benefits = np.array([
            [100, 80],
            [120, 90],
            [110, 85],
        ])
        
        optimal = np.mean([100, 120, 110])  # Policy 1
        evpi = compute_evpi(net_benefits, optimal)
        
        assert evpi >= 0
    
    def test_evpi_zero_when_no_uncertainty(self):
        """Test that EVPI is zero when no uncertainty."""
        net_benefits = np.array([
            [100, 80],
            [100, 80],
            [100, 80],
        ])
        
        optimal = 100
        evpi = compute_evpi(net_benefits, optimal)
        
        chex.assert_near(evpi, 0.0, atol=1e-6)


class TestComputeEVPPi:
    """Tests for compute_evppi."""
    
    def test_returns_evppi_by_group(self):
        """Test that EVPPI is computed for each group."""
        net_benefits = np.random.randn(100, 2)
        parameter_samples = {
            'group1': np.random.randn(100),
            'group2': np.random.randn(100),
        }
        
        optimal = np.mean(np.max(net_benefits, axis=1))
        evppi = compute_evppi(net_benefits, parameter_samples, optimal)
        
        assert 'group1' in evppi
        assert 'group2' in evppi
        assert all(v >= 0 for v in evppi.values())


class TestIdentifyResearchPriority:
    """Tests for identify_research_priority."""
    
    def test_returns_highest_evppi(self):
        """Test that highest EVPPI group is identified."""
        evppi = {
            'group1': 100,
            'group2': 200,
            'group3': 150,
        }
        
        priority = identify_research_priority(evppi)
        
        assert priority == 'group2'


class TestRunVOIAnalysis:
    """Tests for run_voi_analysis."""
    
    def test_returns_voi_result(self):
        """Test that VOI analysis returns complete result."""
        net_benefits = np.random.randn(100, 3)
        policy_names = ['policy1', 'policy2', 'policy3']
        parameter_samples = {
            'group1': np.random.randn(100),
            'group2': np.random.randn(100),
        }
        
        result = run_voi_analysis(net_benefits, policy_names, parameter_samples)
        
        assert hasattr(result, 'evpi')
        assert hasattr(result, 'evppi')
        assert hasattr(result, 'total_uncertainty')
        assert hasattr(result, 'research_priority')


class TestFormatVOIResult:
    """Tests for format_voi_result."""
    
    def test_returns_string(self):
        """Test that formatting returns a string."""
        result = VOIResult(
            evpi=1000,
            evppi={'group1': 500, 'group2': 300},
            total_uncertainty=0.05,
            research_priority='group1',
        )
        
        formatted = format_voi_result(result)
        
        assert isinstance(formatted, str)
        assert 'EVPI' in formatted
        assert 'EVPPI' in formatted
        assert 'group1' in formatted
