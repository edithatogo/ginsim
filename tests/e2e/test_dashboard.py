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

    def test_start_here_guidance_present(self, app_test):
        """Test the landing page provides a first-run workflow."""
        app_test.run()
        assert any("Start Here" in sub.value for sub in app_test.subheader)

    def test_primary_controls_present(self, app_test):
        """Test the primary control surfaces are rendered."""
        app_test.run()
        labels = [widget.label for widget in app_test.selectbox]
        assert any("Select Policy to Evaluate" in label for label in labels)
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
        """Test that clicking 'Run Evaluation' generates the expected metric surface."""
        app_test.run()

        run_button = next(b for b in app_test.button if "Run Evaluation" in b.label)
        run_button.click().run()

        metric_labels = [m.label for m in app_test.metric]
        assert "Testing Uptake" in metric_labels
        assert any("Net Social Benefit" in label for label in metric_labels)

        uptake_metric = next(m for m in app_test.metric if m.label == "Testing Uptake")
        welfare_metric = next(m for m in app_test.metric if "Net Social Benefit" in m.label)

        assert "%" in uptake_metric.value
        assert "$" in welfare_metric.value

    def test_narrative_update_is_disabled_when_script_is_missing(self, app_test):
        """Test the manuscript update action is guarded when the injector script is absent."""
        app_test.run()

        narrative_button = next(b for b in app_test.button if "Update Narrative" in b.label)
        assert narrative_button.disabled
        assert any(
            "Narrative updates are unavailable in this deployment" in info.value
            for info in app_test.info
        )
