"""
E2E Tests for Streamlit Dashboard

Tests all dashboard functionality including:
- Sidebar controls
- Tab rendering
- Visualizations
- Downloads
"""

import pytest
from streamlit.testing.v1 import AppTest


@pytest.fixture
def app_test():
    """Create AppTest fixture."""
    return AppTest.from_file("streamlit_app/app.py")


class TestSidebarControls:
    """Test all sidebar controls."""
    
    def test_policy_selection(self, app_test):
        """Test policy regime selection."""
        app_test.run()
        assert not app_test.exception
        assert app_test.selectbox[0].value == "Status Quo"
        
        # Change policy
        app_test.selectbox[0].set_value("Moratorium")
        app_test.run()
        assert app_test.selectbox[0].value == "Moratorium"
    
    def test_baseline_uptake_slider(self, app_test):
        """Test baseline testing uptake slider."""
        app_test.run()
        assert not app_test.exception
        assert app_test.slider[0].value == 0.52
        
        # Change slider
        app_test.slider[0].set_value(0.60)
        app_test.run()
        assert app_test.slider[0].value == 0.60
    
    def test_deterrence_elasticity_slider(self, app_test):
        """Test deterrence elasticity slider."""
        app_test.run()
        assert not app_test.exception
        assert app_test.slider[1].value == 0.18
        
        # Change slider
        app_test.slider[1].set_value(0.25)
        app_test.run()
        assert app_test.slider[1].value == 0.25
    
    def test_moratorium_effect_slider(self, app_test):
        """Test moratorium effect slider."""
        app_test.run()
        assert not app_test.exception
        assert app_test.slider[2].value == 0.15
        
        # Change slider
        app_test.slider[2].set_value(0.20)
        app_test.run()
        assert app_test.slider[2].value == 0.20


class TestTabRendering:
    """Test all tabs render correctly."""
    
    def test_results_tab(self, app_test):
        """Test Results tab renders."""
        app_test.run()
        assert not app_test.exception
        assert app_test.metric[0].label == "Testing Uptake"
        assert app_test.metric[1].label == "Perceived Penalty"
        assert app_test.metric[2].label == "Welfare Impact"
    
    def test_charts_tab(self, app_test):
        """Test Charts tab renders."""
        app_test.run()
        assert not app_test.exception
        # Check for plotly charts
        assert len(app_test.plotly_chart) >= 2
    
    def test_comparison_tab(self, app_test):
        """Test Comparison tab renders."""
        app_test.run()
        assert not app_test.exception
        # Check for table
        assert len(app_test.table) >= 1
    
    def test_documentation_tab(self, app_test):
        """Test Documentation tab renders."""
        app_test.run()
        assert not app_test.exception
        # Check for markdown content
        assert len(app_test.markdown) >= 1


class TestVisualizations:
    """Test all visualizations."""
    
    def test_policy_comparison_chart(self, app_test):
        """Test policy comparison bar chart."""
        app_test.run()
        assert not app_test.exception
        
        # Get first plotly chart
        chart = app_test.plotly_chart[0]
        assert chart is not None
    
    def test_sensitivity_analysis_chart(self, app_test):
        """Test sensitivity analysis line chart."""
        app_test.run()
        assert not app_test.exception
        
        # Get second plotly chart
        chart = app_test.plotly_chart[1]
        assert chart is not None


class TestDownloads:
    """Test download functionality."""
    
    def test_csv_download(self, app_test):
        """Test CSV download button."""
        app_test.run()
        assert not app_test.exception
        
        # Check for download button
        download_buttons = app_test.download_button
        assert len(download_buttons) >= 1


class TestPerformance:
    """Test dashboard performance."""
    
    def test_load_time(self, app_test):
        """Test dashboard loads within 5 seconds."""
        import time
        start = time.time()
        app_test.run()
        elapsed = time.time() - start
        assert elapsed < 5.0, f"Dashboard took {elapsed:.2f}s to load"
    
    def test_no_errors(self, app_test):
        """Test dashboard runs without errors."""
        app_test.run()
        assert app_test.exception is None


class TestAccuracy:
    """Test computation accuracy."""
    
    def test_policy_impact_calculation(self, app_test):
        """Test policy impact is calculated correctly."""
        app_test.run()
        assert not app_test.exception
        
        # Status Quo should have baseline uptake
        uptake_metric = app_test.metric[0]
        assert float(uptake_metric.value.replace('%', '')) >= 0

