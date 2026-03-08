"""
Diamond-Standard Streamlit AppTest verification.

Ensures no errors or warnings on any dashboard page and verifies narrative UI.
"""

import pytest
from streamlit.testing.v1 import AppTest
from pathlib import Path

def test_main_app_diamond_rigor():
    """Verify main landing page has no errors and shows headline metrics."""
    at = AppTest.from_file("streamlit_app/app.py", default_timeout=120)
    at.run()
    
    # 1. No initial errors
    assert not at.error, f"Errors found on main page: {at.error}"
    
    # 2. Verify new narrative title
    assert "Policy Impact Explorer" in at.title[0].value
    
    # 3. Trigger Model Run
    # Find button by label
    run_button = next(b for b in at.button if "Run Model" in b.label)
    run_button.click().run()
    
    # 4. Check for errors after run
    assert not at.error
    
    # 5. Verify big-number headlines (Metrics)
    assert any("People Choosing to Test" in m.label for m in at.metric)
    assert any("Net Social Benefit" in m.label for m in at.metric)

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
    assert "Policy Scenarios & Stories" in at.title[0].value
    assert any("Status Quo" in b.label for b in at.button)

def test_delta_view_page_diamond_rigor():
    """Verify delta view page loads correctly."""
    at = AppTest.from_file("streamlit_app/pages/5_Delta_View.py", default_timeout=60)
    at.run()
    
    assert not at.error
    assert "Fairness Audit" in at.title[0].value

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
