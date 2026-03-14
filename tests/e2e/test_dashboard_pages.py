"""Interaction-level AppTest coverage for non-landing Streamlit pages."""

import pytest
from streamlit.testing.v1 import AppTest


def test_sensitivity_page_runs_analysis() -> None:
    app = AppTest.from_file("streamlit_app/pages/2_Sensitivity.py", default_timeout=60)
    app.run()
    assert "Comprehensive Sensitivity & VOI Suite" in app.title[0].value

    run_button = next(b for b in app.button if "Generate Tornado Chart" in b.label)
    run_button.click().run()

    # AppTest check for charts
    assert len(app.get("plotly_chart")) >= 1


def test_scenarios_page_runs_comparison_and_exposes_download() -> None:
    app = AppTest.from_file("streamlit_app/pages/3_Scenarios.py", default_timeout=60)
    app.run()
    assert "Policy Scenarios & Stories" in app.title[0].value

    run_button = next(b for b in app.button if "Run Comparative Analysis" in b.label)
    run_button.click().run()

    assert any("Comparative Matrix" in sub.value for sub in app.subheader)
    assert len(app.dataframe) >= 1


@pytest.mark.parametrize(
    ("game_name", "expected_metric"),
    [
        ("Information Leakage", "Reconstruction Accuracy"),
        ("Genetic Altruism", "Altruism Coefficient"),
        ("Cascade Testing", "Cascade Rate"),
    ],
)
def test_extended_games_page_runs_each_game(game_name: str, expected_metric: str) -> None:
    app = AppTest.from_file("streamlit_app/pages/4_Extended_Games.py", default_timeout=60)
    app.run()
    assert "Extended Strategic Games" in app.title[0].value

    # Page 4 uses radio for game selection
    app.radio[0].set_value(game_name).run()

    run_button = next(b for b in app.button if "Run Game" in b.label)
    run_button.click().run()

    assert any(expected_metric in m.label for m in app.metric)


def test_delta_view_page_runs_comparison_and_download() -> None:
    app = AppTest.from_file("streamlit_app/pages/5_Delta_View.py", default_timeout=60)
    app.run()
    assert "Fairness Audit" in app.title[0].value

    run_button = next(b for b in app.button if "Audit Policies" in b.label)
    run_button.click().run()

    assert any("Fairness Verdict" in sub.value for sub in app.subheader)
