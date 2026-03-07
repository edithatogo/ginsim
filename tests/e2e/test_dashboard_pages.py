"""
Smoke tests for non-landing Streamlit dashboard pages.
"""

from streamlit.testing.v1 import AppTest


def test_sensitivity_page_loads() -> None:
    app = AppTest.from_file("streamlit_app/pages/2_Sensitivity.py", default_timeout=30)
    app.run()
    assert app.title[0].value == "📊 Comprehensive Sensitivity Analysis"
    assert len(app.selectbox) >= 2


def test_scenarios_page_loads() -> None:
    app = AppTest.from_file("streamlit_app/pages/3_Scenarios.py", default_timeout=30)
    app.run()
    assert app.title[0].value == "🎯 Scenario Analysis & Policy Sandbox"
    assert len(app.selectbox) >= 2


def test_extended_games_page_loads() -> None:
    app = AppTest.from_file("streamlit_app/pages/4_Extended_Games.py", default_timeout=30)
    app.run()
    assert app.title[0].value == "🎮 Extended Strategic Games"
    assert len(app.radio) >= 1


def test_delta_view_page_loads() -> None:
    app = AppTest.from_file("streamlit_app/pages/5_Delta_View.py", default_timeout=30)
    app.run()
    assert app.title[0].value == "📊 Comparative Delta View"
    assert len(app.selectbox) >= 1
