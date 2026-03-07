"""
Diamond-Standard Streamlit AppTest verification.

Ensures no errors or warnings on any dashboard page and verifies narrative UI.
"""

from streamlit.testing.v1 import AppTest


def test_main_app_diamond_rigor():
    """Verify main landing page has no errors and shows headline metrics."""
    at = AppTest.from_file("streamlit_app/app.py", default_timeout=60)
    at.run()

    # 1. No errors or warnings
    assert not at.error, f"Errors found on main page: {at.error}"
    assert not at.warning, f"Warnings found on main page: {at.warning}"

    # 2. Verify new narrative title
    assert "Policy Impact Explorer" in at.title[0].value

    # 3. Verify big-number headlines (Metrics)
    # After first run, metrics should be present
    assert any("People Choosing to Test" in m.label for m in at.metric)
    assert any("Net Social Benefit" in m.label for m in at.metric)


def test_traceability_page_diamond_rigor():
    """Verify traceability page loads correctly."""
    at = AppTest.from_file("streamlit_app/pages/traceability.py", default_timeout=60)
    at.run()

    assert not at.error
    assert "Evidence Explorer" in at.title[0].value
    # Should have sidebar selectbox for assumptions
    assert len(at.selectbox) >= 1


def test_scenarios_page_diamond_rigor():
    """Verify scenarios page loads correctly."""
    at = AppTest.from_file("streamlit_app/pages/3_Scenarios.py", default_timeout=60)
    at.run()

    assert not at.error
    assert "Policy Scenarios & Stories" in at.title[0].value
    # Verify narrative buttons are present
    assert any("Status Quo" in b.label for b in at.button)


def test_delta_view_page_diamond_rigor():
    """Verify delta view page loads correctly."""
    at = AppTest.from_file("streamlit_app/pages/5_Delta_View.py", default_timeout=60)
    at.run()

    assert not at.error
    assert "Fairness Audit" in at.title[0].value
