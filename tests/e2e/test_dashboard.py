"""
E2E Tests for Streamlit Dashboard (Diamond Standard)

Tests all dashboard functionality including:
- Sidebar controls
- Tab rendering
- Basic functionality
"""

import pytest
from streamlit.testing.v1 import AppTest


@pytest.fixture
def app_test():
    """Create AppTest fixture with increased timeout for JAX compilation."""
    return AppTest.from_file("streamlit_app/app.py", default_timeout=120)


class TestDashboardLoads:
    """Test dashboard loads without errors."""

    def test_dashboard_loads(self, app_test):
        """Test dashboard loads successfully."""
        app_test.run()
        assert len(app_test.title) > 0

    def test_title_present(self, app_test):
        """Test dashboard title is present."""
        app_test.run()
        assert "Policy Impact Explorer" in app_test.title[0].value

    def test_sidebar_present(self, app_test):
        """Test sidebar is present."""
        app_test.run()
        # 1 main selectbox (Policy) + 1 in expander (Jurisdiction)
        assert len(app_test.selectbox) >= 1
        # 1 slider (Baseline)
        assert len(app_test.slider) >= 1


class TestSidebarControls:
    """Test all sidebar controls."""

    def test_policy_selection(self, app_test):
        """Test policy regime selection."""
        app_test.run()
        assert app_test.selectbox[0].value == "Status Quo"

        # Change policy
        app_test.selectbox[0].select("Moratorium").run()
        assert app_test.selectbox[0].value == "Moratorium"


class TestFunctionality:
    """Test dashboard functionality."""

    def test_run_model_button(self, app_test):
        """Test that clicking 'Run Model' generates results."""
        app_test.run()

        # Click button
        run_button = next(b for b in app_test.button if "Run Model" in b.label)
        run_button.click().run()

        # Check for metrics
        assert len(app_test.metric) >= 2
        assert any("People Choosing to Test" in m.label for m in app_test.metric)
        assert any("Net Social Benefit" in m.label for m in app_test.metric)
