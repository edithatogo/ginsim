#!/usr/bin/env python3
"""
Scenario Analysis Page - 100% Codebase Integration Edition.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.model.pipeline import evaluate_single_policy
from src.model.scenario_analysis import (
    evaluate_scenario,
    filter_scenarios_by_jurisdiction,
    get_scenario_display_name,
    load_scenarios,
)
from streamlit_app.dashboard_ui import (
    render_current_run_summary,
    render_footer,
    render_sidebar_build_info,
)

# Page configuration
st.set_page_config(page_title="Scenario Analysis", page_icon="🎯", layout="wide")

st.title("🎯 Policy Scenarios & Stories")
st.markdown("Compare high-rigor outcomes across predefined policy narratives.")

# 1. Load Scenarios
SCENARIOS_CONFIG = Path(__file__).parent.parent.parent / "configs" / "scenarios.yaml"
scenarios = load_scenarios(SCENARIOS_CONFIG)
scenario_labels = {key: get_scenario_display_name(key, config) for key, config in scenarios.items()}

selected_scenario_key = st.sidebar.selectbox(
    "Predefined Scenario",
    list(scenarios.keys()),
    format_func=lambda key: scenario_labels[key],
)
selected_scenario = scenarios[selected_scenario_key]
selected_jurisdiction_code = str(selected_scenario.get("jurisdiction", "AU")).upper()
selected_scope = filter_scenarios_by_jurisdiction(scenarios, selected_jurisdiction_code)
render_sidebar_build_info()
render_current_run_summary(
    "Comparison Context",
    {
        "Focus Scenario": scenario_labels[selected_scenario_key],
        "Jurisdiction": selected_jurisdiction_code,
        "Scope": f"{len(selected_scope)} scenario(s)",
    },
)
st.info(selected_scenario.get("description", "Predefined scenario comparison surface."))

# 2. Run Analysis
if st.sidebar.button("🔍 Run Comparative Analysis", type="primary"):
    with st.spinner("Executing comparative analysis for the selected jurisdiction..."):
        results = []
        ordered_scope = sorted(
            selected_scope.items(),
            key=lambda item: (item[0] != selected_scenario_key, item[0]),
        )
        for name, config in ordered_scope:
            res = evaluate_scenario(name, config, evaluate_single_policy)
            results.append(
                {
                    "Scenario": get_scenario_display_name(name, config),
                    "Uptake": float(res.testing_uptake),
                    "Welfare": float(res.welfare_impact),
                    "Compliance": float(res.compliance_rate),
                    "Info Gap": float(res.all_metrics["info_gap"]),
                }
            )

        df = pd.DataFrame(results)
        st.subheader("High-Rigor Comparative Matrix")
        st.caption(
            f"Showing the {selected_jurisdiction_code} comparison set anchored on "
            f"{scenario_labels[selected_scenario_key]}."
        )
        st.dataframe(
            df.style.format(
                {
                    "Uptake": "{:.1%}",
                    "Welfare": "${:,.0f}",
                    "Compliance": "{:.1%}",
                    "Info Gap": "{:.1%}",
                }
            ),
            hide_index=True,
            use_container_width=True,
        )

        # Chart
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=df["Scenario"], y=df["Welfare"], marker_color="#0072B2", name="Net Social Benefit"
            )
        )
        fig.update_layout(
            title="Societal Welfare by Scenario (DCBA Integrated)", template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)

render_footer("Scenario Comparison Surface")
