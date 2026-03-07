#!/usr/bin/env python3
"""
Scenario Analysis Page

Compare policy outcomes across predefined scenarios and custom configurations.
Features:
- Pre-defined scenarios (AU 2025 Ban, FSC Moratorium, international benchmarks)
- Policy Stories (Narrative Presets)
- Australian Policy Designer (Sandbox)
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
    compare_scenarios,
    load_scenarios,
)
from streamlit_app.dashboard_helpers import evaluate_sandbox_policy

# Page configuration
st.set_page_config(
    page_title="Scenario Analysis",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Title
st.title("🎯 Policy Scenarios & Stories")
st.markdown("""
**How do different policy choices affect the real world?**
This page translates abstract settings into 'Policy Stories'—predefined scenarios that represent common policy directions.
""")

# 1. Narrative Policy Stories (Presets)
st.subheader("📖 Choose a Policy Story")
col_s1, col_s2, col_s3 = st.columns(3)

with col_s1:
    if st.button("🏛️ The Status Quo", help="Australia's current market-led approach"):
        st.session_state["active_story"] = "au_status_quo"

with col_s2:
    if st.button("🤝 The Industry Compromise", help="Self-regulation with caps (Moratorium)"):
        st.session_state["active_story"] = "au_fsc_moratorium"

with col_s3:
    if st.button("🛡️ The Protective Ban", help="Legislated ban on genetic information"):
        st.session_state["active_story"] = "au_2025_ban"

# Sidebar for manual config
st.sidebar.header("⚙️ Scenario Configuration")
SCENARIOS_CONFIG = Path(__file__).parent.parent.parent / "configs" / "scenarios.yaml"


@st.cache_data
def load_scenarios_cached():
    return load_scenarios(SCENARIOS_CONFIG)


scenarios = load_scenarios_cached()

# Auto-select based on story button
default_idx = 0
if "active_story" in st.session_state:
    keys = list(scenarios.keys())
    if st.session_state["active_story"] in keys:
        default_idx = keys.index(st.session_state["active_story"])

selected_scenario_key = st.sidebar.selectbox(
    "Predefined Scenario", list(scenarios.keys()), index=default_idx
)

# Display Story Narrative
st.info(f"""
**Current Story:** {scenarios[selected_scenario_key].get("name", selected_scenario_key)}
{scenarios[selected_scenario_key].get("description", "No description available.")}
""")

# Run comparison logic
if st.sidebar.button("🔍 Run Comparison", type="primary"):

    def model_func(params, policy):
        return evaluate_single_policy(params, policy)

    comparison = compare_scenarios(scenarios, model_func, baseline_name="au_status_quo")
    st.session_state["scenario_comparison"] = comparison

# Display Results
if "scenario_comparison" in st.session_state:
    comp = st.session_state["scenario_comparison"]
    st.divider()
    st.subheader("📈 Projected Impacts")

    # Simple summary table
    data = []
    for r in comp.scenarios:
        data.append(
            {
                "Scenario": r.scenario_name,
                "Uptake": f"{r.testing_uptake:.1%}",
                "Net Benefit": f"${r.welfare_impact:,.0f}",
                "Compliance": f"{r.compliance_rate:.1%}",
            }
        )
    st.dataframe(pd.DataFrame(data), hide_index=True, use_container_width=True)

    # Chart
    fig = go.Figure()
    names = [r.scenario_name for r in comp.scenarios]
    uptakes = [r.testing_uptake for r in comp.scenarios]
    fig.add_trace(go.Bar(x=names, y=uptakes, marker_color="#3498db"))
    fig.update_layout(title="Testing Uptake Comparison", yaxis_tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)

# Australian Policy Sandbox (Humanized)
with st.expander("🛠️ Custom Policy Designer (Advanced)"):
    st.markdown("Adjust parameters manually to explore the design space.")
    # Sandbox logic remains but tucked away
    c1, c2 = st.columns(2)
    with c1:
        s_uptake = st.slider("Baseline Uptake", 0.3, 0.7, 0.52)
        s_enforcement = st.slider("Enforcement Strength", 0.0, 1.0, 0.7)
    with c2:
        res = evaluate_sandbox_policy(
            baseline_testing_uptake=s_uptake, enforcement_effectiveness=s_enforcement
        )
        st.metric("Estimated Uptake", f"{float(res.testing_uptake):.1%}")
        st.metric("Social Benefit", f"${float(res.welfare_impact):,.0f}")

st.divider()
st.caption("Developed by Authors' analysis • 2026.03")
