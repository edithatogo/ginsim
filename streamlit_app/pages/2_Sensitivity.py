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

try:
    from streamlit_app.dashboard_ui import (
        JURISDICTION_OPTIONS,
        jurisdiction_to_config_id,
        render_current_run_summary,
        render_footer,
        render_glossary,
        render_sidebar_build_info,
        render_view_mode_sidebar,
    )
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from dashboard_ui import (
        JURISDICTION_OPTIONS,
        jurisdiction_to_config_id,
        render_current_run_summary,
        render_footer,
        render_glossary,
        render_sidebar_build_info,
        render_view_mode_sidebar,
    )

# Page configuration
st.set_page_config(
    page_title="GINSIM Uncertainty Suite",
    page_icon="📊",
    layout="wide",
)

audience_mode = render_view_mode_sidebar()

st.title("📊 Uncertainty Explorer")
st.markdown(
    "See how uncertain assumptions can change the result, and which unknowns matter most."
)
render_glossary(audience_mode)

# Sidebar Settings
st.sidebar.header("⚙️ Simulation settings")
n_draws = st.sidebar.number_input("Number of simulation draws", 100, 10000, 1000, step=100)
if audience_mode == "General audience":
    policy_name = st.sidebar.selectbox(
        "Policy to test",
        ["Current Rules", "Temporary Ban", "Full Ban"],
    )
    policy_id = {
        "Current Rules": "status_quo",
        "Temporary Ban": "moratorium",
        "Full Ban": "ban",
    }[policy_name]
else:
    policy_name = st.sidebar.selectbox("Policy to test", ["Status Quo", "Moratorium", "Ban"])
    policy_id = policy_name.lower().replace(" ", "_")
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
    [
        "🎲 Uncertainty simulation",
        "💎 Value of better evidence",
        "🌪️ One factor at a time",
    ]
)

# 1. PSA TAB
with tab_psa:
    st.subheader("Uncertainty simulation")
    st.caption(
        "This runs the model many times with different plausible assumptions to show a range of outcomes."
    )
    if st.button("🎲 Run PSA Simulation", type="primary"):
        with st.spinner(f"Executing {n_draws} JAX-vectorized simulations..."):
            policies = get_standard_policies()
            target_policy = policies[policy_id]

            res_psa = run_psa(base_params, target_policy, n_draws=n_draws)

            c1, c2 = st.columns(2)
            with c1:
                st.metric("Average testing uptake", f"{res_psa['uptake'].mean:.1%}")
                st.caption(
                    f"Likely range: [{res_psa['uptake'].lower_95:.1%}, {res_psa['uptake'].upper_95:.1%}]"
                )

                # Histogram
                fig_uptake = px.histogram(
                    res_psa["uptake"].samples.tolist(),
                    nbins=30,
                    title="Range of predicted testing uptake",
                    labels={"value": "Predicted testing uptake"},
                )
                fig_uptake.update_layout(template="plotly_white", showlegend=False)
                st.plotly_chart(fig_uptake, use_container_width=True)

            with c2:
                st.metric("Average social benefit", f"${res_psa['welfare'].mean:,.0f}")
                st.caption(
                    f"Likely range: [${res_psa['welfare'].lower_95:,.0f}, ${res_psa['welfare'].upper_95:,.0f}]"
                )

                # Histogram
                fig_welfare = px.histogram(
                    res_psa["welfare"].samples.tolist(),
                    nbins=30,
                    title="Range of predicted social benefit",
                    labels={"value": "Social benefit ($)"},
                )
                fig_welfare.update_layout(template="plotly_white", showlegend=False)
                st.plotly_chart(fig_welfare, use_container_width=True)

# 2. VOI TAB
with tab_voi:
    st.subheader("Value of better evidence")
    st.markdown(
        "This asks how valuable it would be to reduce uncertainty before choosing a policy."
    )

    if st.button("💎 Calculate VOI Metrics", type="primary"):
        with st.spinner("Computing global welfare matrix..."):
            voi_res = run_full_voi_analysis(base_params, n_draws=n_draws)

            st.metric("Value of removing uncertainty", f"${voi_res['evpi']:,.2f}")
            st.info(
                "This is the maximum amount it would be worth paying for perfect evidence that removes decision risk."
            )

            st.subheader("Which unknown matters most?")
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
                title="Which uncertain assumption matters most?",
            )
            fig_voi.update_layout(template="plotly_white")
            st.plotly_chart(fig_voi, use_container_width=True)

# 3. TORNADO TAB
with tab_tornado:
    st.subheader("One factor at a time")
    st.caption(
        "Important: this chart currently shows how each assumption changes testing uptake only, not the full welfare result."
    )
    param_options = {
        "Fear reduces testing": "deterrence_elasticity",
        "Restrictions feel reassuring": "moratorium_effect",
        "Adverse selection pressure": "adverse_selection_elasticity",
        "Baseline insurance loading": "baseline_loading",
    }

    selected_params = st.multiselect(
        "Assumptions to vary", list(param_options.keys()), default=list(param_options.keys())
    )

    if st.button("🌪️ Generate Tornado Chart", type="primary"):
        policies = get_standard_policies()
        policy = policies[policy_id]

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
            title="Impact on testing uptake (±25% variation)", template="plotly_white"
        )
        st.plotly_chart(fig_t, use_container_width=True)

render_footer("Uncertainty Explorer")
