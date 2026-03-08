#!/usr/bin/env python3
"""
Sensitivity Analysis Page - Diamond Standard (Restored)

Comprehensive sensitivity analysis including:
- One-way sensitivity (Tornado diagrams)
- Two-way interaction (Heatmaps)
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from src.model.module_a_behavior import get_standard_policies
from src.model.parameters import ModelParameters
from src.model.pipeline import evaluate_single_policy
from src.model.sensitivity import tornado_analysis

# Page configuration
st.set_page_config(
    page_title="GINSIM Sensitivity Analysis",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Sensitivity & Robustness Analysis")
st.markdown("Explore how model outcomes shift under different parameter uncertainties.")

# Sidebar Settings
st.sidebar.header("⚙️ Analysis Controls")
params_model = ModelParameters()
param_options = {
    "Deterrence Elasticity": "deterrence_elasticity",
    "Moratorium Effect": "moratorium_effect",
    "Adverse Selection": "adverse_selection_elasticity",
    "Baseline Loading": "baseline_loading",
}

selected_params = st.sidebar.multiselect(
    "Select Parameters for Tornado",
    list(param_options.keys()),
    default=list(param_options.keys())[:3],
)

range_pct = st.sidebar.slider("Variation Range (±%)", 0.1, 0.5, 0.25)
policy_name = st.sidebar.selectbox("Policy Focus", ["Status Quo", "Moratorium", "Ban"])

tab_tornado, tab_heatmap = st.tabs(["🌪️ One-Way (Tornado)", "🔥 Two-Way (Heatmap)"])

with tab_tornado:
    if st.button("🔬 Run Tornado Analysis", type="primary"):
        policies = get_standard_policies()
        policy = policies.get(policy_name.lower().replace(" ", "_"), policies["status_quo"])

        def model_func(p):
            res = evaluate_single_policy(p, policy)
            return float(res.testing_uptake)

        attr_names = [param_options[k] for k in selected_params]
        results = tornado_analysis(model_func, params_model, attr_names, variation=range_pct)

        fig = go.Figure()
        y_labels = [r.parameter_name for r in results]
        swings = [r.upper_outcome - r.lower_outcome for r in results]

        fig.add_trace(
            go.Bar(
                y=y_labels,
                x=swings,
                base=[r.lower_outcome for r in results],
                orientation="h",
                marker_color="#3498db",
            )
        )
        fig.update_layout(title=f"Policy Sensitivity: {policy_name}", xaxis_tickformat=".1%")
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("View Numerical Indices"):
            st.table(
                [
                    {"Param": r.parameter_name, "Impact": f"{r.sensitivity_index:.4f}"}
                    for r in results
                ]
            )

with tab_heatmap:
    st.subheader("Parameter Interaction Heatmap")
    c1, c2 = st.columns(2)
    with c1:
        p1 = st.selectbox("X-Axis Parameter", list(param_options.keys()), index=0)
    with c2:
        p2 = st.selectbox("Y-Axis Parameter", list(param_options.keys()), index=1)

    if st.button("🔥 Generate Interaction Map"):
        with st.spinner("Computing interaction grid..."):
            policies = get_standard_policies()
            policy = policies[policy_name.lower().replace(" ", "_")]

            x_range = np.linspace(0.01, 0.5, 10)
            y_range = np.linspace(0.01, 0.5, 10)
            z_data = []

            for y_val in y_range:
                row = []
                for x_val in x_range:
                    # Create temporary params
                    test_params = ModelParameters(
                        **{param_options[p1]: x_val, param_options[p2]: y_val}
                    )
                    res = evaluate_single_policy(test_params, policy)
                    row.append(float(res.testing_uptake))
                z_data.append(row)

            fig = go.Figure(
                data=go.Heatmap(
                    z=z_data,
                    x=x_range,
                    y=y_range,
                    colorscale="Viridis",
                    colorbar={"title": "Testing Uptake"},
                )
            )
            fig.update_layout(xaxis_title=p1, yaxis_title=p2)
            st.plotly_chart(fig, use_container_width=True)

st.divider()
st.caption("Developed by Dylan A Mordaunt • 2026.03")
