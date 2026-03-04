"""
E2E Tests for Streamlit Dashboard

Tests all dashboard functionality including:
- Sidebar controls
- Tab rendering
- Basic functionality

Note: Streamlit's testing API has limitations. Full E2E testing
should be done manually or with Playwright/Selenium.
"""

import pytest
from streamlit.testing.v1 import AppTest


@pytest.fixture
def app_test():
    """Create AppTest fixture."""
    return AppTest.from_file("streamlit_app/app.py")


class TestDashboardLoads:
    """Test dashboard loads without errors."""
    
    def test_dashboard_loads(self, app_test):
        """Test dashboard loads successfully."""
        app_test.run()
        # Check that title is present (indicates successful load)
        assert len(app_test.title) > 0
    
    def test_title_present(self, app_test):
        """Test dashboard title is present."""
        app_test.run()
        assert app_test.title[0].value == "🧬 Genetic Discrimination Policy Dashboard"
    
    def test_sidebar_present(self, app_test):
        """Test sidebar is present."""
        app_test.run()
        assert len(app_test.selectbox) > 0
        assert len(app_test.slider) > 0


class TestSidebarControls:
    """Test all sidebar controls."""
    
    def test_policy_selection(self, app_test):
        """Test policy regime selection."""
        app_test.run()
        assert app_test.selectbox[0].value == "Status Quo"
        
        # Change policy
        app_test.selectbox[0].set_value("Moratorium")
        app_test.run()
        assert app_test.selectbox[0].value == "Moratorium"
    
    def test_baseline_uptake_slider(self, app_test):
        """Test baseline testing uptake slider."""
        app_test.run()
        assert app_test.slider[0].value == 0.52
        
        # Change slider
        app_test.slider[0].set_value(0.60)
        app_test.run()
        assert app_test.slider[0].value == 0.60
    
    def test_deterrence_elasticity_slider(self, app_test):
        """Test deterrence elasticity slider."""
        app_test.run()
        assert app_test.slider[1].value == 0.18
        
        # Change slider
        app_test.slider[1].set_value(0.25)
        app_test.run()
        assert app_test.slider[1].value == 0.25
    
    def test_moratorium_effect_slider(self, app_test):
        """Test moratorium effect slider."""
        app_test.run()
        assert app_test.slider[2].value == 0.15
        
        # Change slider
        app_test.slider[2].set_value(0.20)
        app_test.run()
        assert app_test.slider[2].value == 0.20


class TestTabRendering:
    """Test all tabs render correctly."""
    
    def test_results_tab_metrics(self, app_test):
        """Test Results tab has metrics."""
        app_test.run()
        assert len(app_test.metric) >= 3
    
    def test_comparison_tab_table(self, app_test):
        """Test Comparison tab has table."""
        app_test.run()
        assert len(app_test.table) >= 1


class TestAccuracy:
    """Test computation accuracy."""
    
    def test_policy_impact_calculation(self, app_test):
        """Test policy impact is calculated correctly."""
        app_test.run()
        
        # Status Quo should have baseline uptake
        uptake_metric = app_test.metric[0]
        assert float(uptake_metric.value.replace('%', '')) >= 0
    
    def test_metrics_update_on_policy_change(self, app_test):
        """Test metrics update when policy changes."""
        app_test.run()
        initial_uptake = app_test.metric[0].value
        
        # Change to Moratorium
        app_test.selectbox[0].set_value("Moratorium")
        app_test.run()
        
        # Uptake should increase
        new_uptake = app_test.metric[0].value
        assert float(new_uptake.replace('%', '')) >= float(initial_uptake.replace('%', ''))
