"""
Unit tests for sensitivity analysis.
"""

import pytest
import numpy as np

from src.model.sensitivity import (
    one_way_sensitivity,
    tornado_analysis,
    scenario_analysis,
    SensitivityResult,
)


class TestOneWaySensitivity:
    """Tests for one_way_sensitivity."""
    
    def test_returns_sensitivity_result(self):
        """Test that one-way sensitivity returns complete result."""
        def model(params):
            return params['x'] * 2
        
        base_params = {'x': 10.0}
        
        result = one_way_sensitivity(
            model,
            base_params,
            'x',
            range_pct=0.1,
        )
        
        assert result.parameter == 'x'
        assert result.base_value == 10.0
        assert result.range[0] == 9.0
        assert result.range[1] == 11.0
    
    def test_sensitivity_index_positive(self):
        """Test that sensitivity index is positive."""
        def model(params):
            return params['x'] ** 2
        
        base_params = {'x': 10.0}
        
        result = one_way_sensitivity(
            model,
            base_params,
            'x',
            range_pct=0.25,
        )
        
        assert result.sensitivity_index > 0


class TestTornadoAnalysis:
    """Tests for tornado_analysis."""
    
    def test_returns_sorted_results(self):
        """Test that tornado results are sorted by sensitivity."""
        def model(params):
            return params['x'] + params['y'] * 2
        
        base_params = {'x': 10.0, 'y': 5.0}
        
        results = tornado_analysis(
            model,
            base_params,
            ['x', 'y'],
            range_pct=0.1,
        )
        
        # Should be sorted by sensitivity (descending)
        assert len(results) == 2
        assert results[0].sensitivity_index >= results[1].sensitivity_index


class TestScenarioAnalysis:
    """Tests for scenario_analysis."""
    
    def test_returns_scenario_results(self):
        """Test that scenario analysis returns all scenarios."""
        def model(params):
            return params['x'] * params['y']
        
        base_params = {'x': 10.0, 'y': 5.0}
        
        scenarios = {
            'optimistic': {'x': 15.0, 'y': 7.5},
            'pessimistic': {'x': 5.0, 'y': 2.5},
        }
        
        results = scenario_analysis(model, base_params, scenarios)
        
        assert 'base' in results
        assert 'optimistic' in results
        assert 'pessimistic' in results
    
    def test_computes_change_from_base(self):
        """Test that change from base is computed."""
        def model(params):
            return params['x']
        
        base_params = {'x': 10.0}
        
        scenarios = {
            'increase': {'x': 15.0},
        }
        
        results = scenario_analysis(model, base_params, scenarios)
        
        # Change should be (15 - 10) / 10 = 0.5
        assert abs(results['increase']['change_from_base'] - 0.5) < 0.01
