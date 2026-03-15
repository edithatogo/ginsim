#!/usr/bin/env python3
"""
Sensitivity Analysis Page - SOTA Global Uncertainty Overhaul.

Comprehensive suite including:
- JAX-vectorized One-Way Analysis (Tornado)
- Probabilistic Sensitivity Analysis (PSA)
- Value of Information (VOI / EVPI / EVPPI)
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.model.module_a_behavior import get_standard_policies
from src.model.parameters import load_jurisdiction_parameters
from src.model.pipeline import evaluate_single_policy
from src.model.sensitivity import tornado_analysis
from src.model.uncertainty_engine import run_full_voi_analysis, run_psa
from streamlit_app.dashboard_ui import (
    JURISDICTION_OPTIONS,
    jurisdiction_to_config_id,
    render_current_run_summary,
    render_footer,
    render_sidebar_build_info,
)

# Page configuration
st.set_page_config(
    page_title="GINSIM Uncertainty Suite",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Comprehensive Sensitivity & VOI Suite")
st.markdown("Quantifying policy robustness and the value of scientific evidence.")

# Sidebar Settings
st.sidebar.header("⚙️ Global MC Settings")
n_draws = st.sidebar.number_input("Monte Carlo Draws", 100, 10000, 1000, step=100)
policy_name = st.sidebar.selectbox("Target Policy", ["Status Quo", "Moratorium", "Ban"])
jurisdiction = st.sidebar.selectbox("Jurisdiction", JURISDICTION_OPTIONS)
render_sidebar_build_info()

base_params = load_jurisdiction_parameters(jurisdiction_to_config_id(jurisdiction))
render_current_run_summary(
    "Current Analysis Context",
    {
        "Jurisdiction": jurisdiction,
        "Policy": policy_name,
        "Draws": f"{n_draws:,}",
    },
)

tab_psa, tab_voi, tab_tornado = st.tabs(
    ["🎲 Probabilistic (PSA)", "💎 Value of Info (VOI)", "🌪️ One-Way (Tornado)"]
)

# 1. PSA TAB
with tab_psa:
    st.subheader("Monte Carlo Uncertainty Propagation")
    if st.button("🎲 Run PSA Simulation", type="primary"):
        with st.spinner(f"Executing {n_draws} JAX-vectorized simulations..."):
            policies = get_standard_policies()
            target_policy = policies[policy_name.lower().replace(" ", "_")]

            res_psa = run_psa(base_params, target_policy, n_draws=n_draws)

            c1, c2 = st.columns(2)
            with c1:
                st.metric("Expected Uptake (Mean)", f"{res_psa['uptake'].mean:.1%}")
                st.caption(
                    f"95% CrI: [{res_psa['uptake'].lower_95:.1%}, {res_psa['uptake'].upper_95:.1%}]"
                )

                # Histogram
                fig_uptake = px.histogram(
                    res_psa["uptake"].samples.tolist(),
                    nbins=30,
                    title="Uptake Distribution",
                    labels={"value": "Predicted Uptake"},
                )
                fig_uptake.update_layout(template="plotly_white", showlegend=False)
                st.plotly_chart(fig_uptake, use_container_width=True)

            with c2:
                st.metric("Expected Welfare (Mean)", f"${res_psa['welfare'].mean:,.0f}")
                st.caption(
                    f"95% CrI: [${res_psa['welfare'].lower_95:,.0f}, ${res_psa['welfare'].upper_95:,.0f}]"
                )

                # Histogram
                fig_welfare = px.histogram(
                    res_psa["welfare"].samples.tolist(),
                    nbins=30,
                    title="Welfare Distribution (PPP)",
                    labels={"value": "Standardized Welfare Impact ($)"},
                )
                fig_welfare.update_layout(template="plotly_white", showlegend=False)
                st.plotly_chart(fig_welfare, use_container_width=True)

# 2. VOI TAB
with tab_voi:
    st.subheader("Expected Value of Information (EVPI)")
    st.markdown(
        "How much is it worth to resolve all parameter uncertainty before choosing a policy?"
    )

    if st.button("💎 Calculate VOI Metrics", type="primary"):
        with st.spinner("Computing global welfare matrix..."):
            voi_res = run_full_voi_analysis(base_params, n_draws=n_draws)

            st.metric("Global EVPI (Total Uncertainty)", f"${voi_res['evpi']:,.2f}")
            st.info(
                "EVPI represents the maximum a society should pay for perfect scientific evidence to eliminate all decision risk."
            )

            st.subheader("Partial Information Value (EVPPI)")
            evppi_df = pd.DataFrame(
                [
                    {"Parameter": k, "Value of Information ($)": v}
                    for k, v in voi_res["evppi"].items()
                ]
            ).sort_values("Value of Information ($)", ascending=False)

            fig_voi = px.bar(
                evppi_df,
                x="Value of Information ($)",
                y="Parameter",
                orientation="h",
                title="Research Priorities: Which parameter matters most?",
            )
            fig_voi.update_layout(template="plotly_white")
            st.plotly_chart(fig_voi, use_container_width=True)

# 3. TORNADO TAB
with tab_tornado:
    st.subheader("One-Way Deterministic Sensitivity")
    param_options = {
        "Deterrence Elasticity": "deterrence_elasticity",
        "Moratorium Effect": "moratorium_effect",
        "Adverse Selection": "adverse_selection_elasticity",
        "Baseline Loading": "baseline_loading",
    }

    selected_params = st.multiselect(
        "Parameters to Vary", list(param_options.keys()), default=list(param_options.keys())
    )

    if st.button("🌪️ Generate Tornado Chart", type="primary"):
        policies = get_standard_policies()
        policy = policies[policy_name.lower().replace(" ", "_")]

        def model_func(p):
            res = evaluate_single_policy(p, policy)
            return float(res.testing_uptake)

        attr_names = [param_options[k] for k in selected_params]
        results = tornado_analysis(model_func, base_params, attr_names, variation=0.25)

        fig_t = go.Figure()
        y_labels = [r.parameter_name for r in results]
        swings = [r.upper_outcome - r.lower_outcome for r in results]

        fig_t.add_trace(
            go.Bar(
                y=y_labels,
                x=swings,
                base=[r.lower_outcome for r in results],
                orientation="h",
                marker_color="#3498db",
            )
        )
        fig_t.update_layout(
            title="Impact on Testing Uptake (±25% variation)", template="plotly_white"
        )
        st.plotly_chart(fig_t, use_container_width=True)

render_footer("JAX-Vectorized Uncertainty Suite")
