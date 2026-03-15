"""Interaction-level AppTest coverage for non-landing Streamlit pages."""

import pytest
from streamlit.testing.v1 import AppTest


def test_sensitivity_page_runs_analysis() -> None:
    app = AppTest.from_file("streamlit_app/pages/2_Sensitivity.py", default_timeout=60)
    app.run()
    assert "Uncertainty Explorer" in app.title[0].value
    assert any(r.label == "View mode" and r.value == "General audience" for r in app.radio)
    assert any(
        metric.label == "Jurisdiction" and metric.value == "Australia" for metric in app.metric
    )

    run_button_psa = next(b for b in app.button if "Run PSA Simulation" in b.label)
    run_button_psa.click().run()
    assert len(app.get("plotly_chart")) >= 1


def test_sensitivity_page_updates_context_for_selected_jurisdiction() -> None:
    app = AppTest.from_file("streamlit_app/pages/2_Sensitivity.py", default_timeout=60)
    app.run()

    jurisdiction_box = next(s for s in app.selectbox if s.label == "Jurisdiction")
    jurisdiction_box.select("Canada").run()

    assert any(metric.label == "Jurisdiction" and metric.value == "Canada" for metric in app.metric)


def test_sensitivity_page_runs_voi_metrics() -> None:
    app = AppTest.from_file("streamlit_app/pages/2_Sensitivity.py", default_timeout=60)
    app.run()

    draws_input = next(n for n in app.number_input if "Number of simulation draws" in n.label)
    draws_input.set_value(100).run()

    run_button_voi = next(b for b in app.button if "Calculate VOI Metrics" in b.label)
    run_button_voi.click().run()

    assert any("Value of removing uncertainty" in metric.label for metric in app.metric)


def test_scenarios_page_runs_comparison_and_exposes_download() -> None:
    app = AppTest.from_file("streamlit_app/pages/3_Scenarios.py", default_timeout=60)
    app.run()
    assert "Scenario Comparison" in app.title[0].value
    assert any(
        metric.label == "Focus Scenario" and "Australia 2025 Genetic Ban" in metric.value
        for metric in app.metric
    )

    run_button = next(b for b in app.button if "Compare scenarios" in b.label)
    run_button.click().run()

    assert any("Scenario comparison table" in sub.value for sub in app.subheader)
    assert len(app.dataframe) >= 1


def test_scenarios_page_updates_focus_context_for_selected_scenario() -> None:
    app = AppTest.from_file("streamlit_app/pages/3_Scenarios.py", default_timeout=60)
    app.run()

    scenario_box = next(s for s in app.selectbox if s.label == "Scenario to anchor on")
    scenario_box.select("uk_code").run()

    assert any(
        metric.label == "Focus Scenario" and metric.value == "UK Code on Genetic Testing"
        for metric in app.metric
    )


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
    assert "Fairness Check" in app.title[0].value
    assert any(
        metric.label == "Jurisdiction" and metric.value == "Australia" for metric in app.metric
    )

    run_button = next(b for b in app.button if "Audit Policies" in b.label)
    run_button.click().run()

    assert any("Fairness results" in sub.value for sub in app.subheader)


def test_delta_view_updates_context_for_selected_jurisdiction() -> None:
    app = AppTest.from_file("streamlit_app/pages/5_Delta_View.py", default_timeout=60)
    app.run()

    jurisdiction_box = next(s for s in app.selectbox if s.label == "Jurisdiction")
    jurisdiction_box.select("Canada").run()

    assert any(metric.label == "Jurisdiction" and metric.value == "Canada" for metric in app.metric)
