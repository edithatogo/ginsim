"""
E2E Tests for Streamlit Dashboard (Global Benchmarking Edition)
"""

import pytest
from streamlit.testing.v1 import AppTest


@pytest.fixture
def app_test():
    """Create AppTest fixture."""
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
        assert "Global Policy Explorer" in app_test.title[0].value

    def test_sidebar_present(self, app_test):
        """Test sidebar is present."""
        app_test.run()
        assert len(app_test.selectbox) >= 1
        assert len(app_test.slider) >= 1


class TestSidebarControls:
    """Test all sidebar controls."""

    def test_policy_selection(self, app_test):
        """Test policy regime selection."""
        app_test.run()
        # Find by label to be safe
        policy_box = next(s for s in app_test.selectbox if "Select Policy to Evaluate" in s.label)
        assert policy_box.value == "Status Quo"

        # Change policy
        policy_box.select("Moratorium").run()
        assert policy_box.value == "Moratorium"


class TestFunctionality:
    """Test dashboard functionality."""

    def test_run_model_button(self, app_test):
        """Test that clicking 'Run Evaluation' generates correct numerical results."""
        app_test.run()

        # Find the specific button name
        run_button = next(b for b in app_test.button if "Run Evaluation" in b.label)
        run_button.click().run()

        # Check for restored metrics
        uptake_metric = next(m for m in app_test.metric if "Testing Uptake" in m.label)
        # Expected value from CLI baseline: 61.3% (formatted)
        assert "61.3%" in uptake_metric.value

        welfare_metric = next(m for m in app_test.metric if "Net Social Benefit" in m.label)
        # Verify welfare is formatted
        assert "$" in welfare_metric.value
        # Value might be negative due to setup costs ($ -1,000,000)
        assert len(welfare_metric.value) > 2
