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


@pytest.fixture()
def app_test():
    """Create AppTest fixture with increased timeout for JAX compilation."""
    return AppTest.from_file("streamlit_app/app.py", default_timeout=30)


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
        # 2 selectboxes (Jurisdiction, Policy Regime)
        assert len(app_test.selectbox) >= 2
        # 3 sliders (Baseline, Deterrence, Moratorium)
        assert len(app_test.slider) >= 3

    def test_plain_language_guide_present(self, app_test):
        """Test landing page includes first-pass guidance."""
        app_test.run()
        assert any(
            "Plain-language guide and glossary" in getattr(node, "label", "")
            for node in app_test.expander
        )


class TestSidebarControls:
    """Test all sidebar controls."""

    def test_policy_selection(self, app_test):
        """Test policy regime selection."""
        app_test.run()
        # Policy Regime is the 2nd selectbox now
        assert app_test.selectbox[1].value == "Status Quo"

        # Change policy
        app_test.selectbox[1].set_value("Moratorium")
        app_test.run()
        assert app_test.selectbox[1].value == "Moratorium"

    def test_baseline_uptake_slider(self, app_test):
        """Test baseline testing uptake slider."""
        app_test.run()
        assert app_test.slider[0].value == 0.52

        # Change slider
        app_test.slider[0].set_value(0.60)
        app_test.run()
        assert app_test.slider[0].value == 0.60


class TestFunctionality:
    """Test dashboard functionality."""

    def test_run_model_button(self, app_test):
        """Test that clicking 'Run Model' generates results."""
        app_test.run()

        # Click button
        # find by label
        run_button = next(b for b in app_test.button if b.label == "🔬 Run Model")
        run_button.click().run()

        # Check for metrics instead of session state (more reliable)
        assert len(app_test.metric) >= 3
        # First metric is Testing Uptake
        assert "Testing Uptake" in app_test.metric[0].label
        # Value should be a percentage
        assert "%" in app_test.metric[0].value
        assert "Long-run Net Welfare" in app_test.metric[1].label
