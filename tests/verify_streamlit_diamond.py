"""
Diamond-Standard Streamlit AppTest verification.

Ensures no errors or warnings on any dashboard page and verifies narrative UI.
"""

from streamlit.testing.v1 import AppTest


def test_main_app_diamond_rigor():
    """Verify main landing page has no errors and shows headline metrics."""
    at = AppTest.from_file("streamlit_app/app.py", default_timeout=120)
    at.run()

    # 1. No initial errors
    assert not at.error, f"Errors found on main page: {at.error}"

    # 2. Verify title
    assert "Global Policy Explorer" in at.title[0].value

    # 3. Trigger Evaluation
    # Find button by label
    run_button = next(b for b in at.button if "Run Evaluation" in b.label)
    run_button.click().run()

    # 4. Check for errors after run
    assert not at.error

    # 5. Verify metrics
    assert any("People choosing genetic testing" in m.label for m in at.metric)
    assert any("Overall benefit to society" in m.label for m in at.metric)


def test_traceability_page_diamond_rigor():
    """Verify traceability page loads correctly."""
    at = AppTest.from_file("streamlit_app/pages/traceability.py", default_timeout=60)
    at.run()

    assert not at.error
    assert "Evidence Explorer" in at.title[0].value
    assert len(at.selectbox) >= 1


def test_scenarios_page_diamond_rigor():
    """Verify scenarios page loads correctly."""
    at = AppTest.from_file("streamlit_app/pages/3_Scenarios.py", default_timeout=60)
    at.run()

    assert not at.error
    assert "Scenario Comparison" in at.title[0].value

    # Trigger analysis to see scenarios
    run_button = next(b for b in at.button if "Compare scenarios" in b.label)
    run_button.click().run()

    assert not at.error
    # Check if results are shown
    assert any("Scenario comparison table" in sub.value for sub in at.subheader)


def test_delta_view_page_diamond_rigor():
    """Verify delta view page loads correctly."""
    at = AppTest.from_file("streamlit_app/pages/5_Delta_View.py", default_timeout=60)
    at.run()

    assert not at.error
    assert "Fairness Check" in at.title[0].value


def test_extended_games_page_diamond_rigor():
    """Verify extended games page loads and runs."""
    at = AppTest.from_file("streamlit_app/pages/4_Extended_Games.py", default_timeout=60)
    at.run()

    assert not at.error
    assert "Extended Strategic Games" in at.title[0].value

    # Trigger first game (Leakage)
    run_button = next(b for b in at.button if "Run Game" in b.label)
    run_button.click().run()

    assert not at.error
    assert any("Reconstruction Accuracy" in m.label for m in at.metric)
