#!/usr/bin/env python3
"""
GINSIM: Genetic Information Non-Discrimination Policy Integrated Economic Evaluation
Main Dashboard - SOTA Equity Localization Edition.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.model.module_a_behavior import get_standard_policies
from src.model.parameters import load_jurisdiction_parameters
from src.model.pipeline import evaluate_single_policy

# =============================================================================
# Visual Design System
# =============================================================================
STYLE = {
    "colors": {
        "status_quo": "#0072B2",
        "moratorium": "#009E73",
        "ban": "#D55E00",
        "neutral": "#999999",
        "consumer": "#56B4E9",
        "insurer": "#E69F00",
        "health": "#CC79A7",
    },
}


def get_policy_color(policy_name: str) -> str:
    name = policy_name.lower().replace(" ", "_")
    if "status_quo" in name:
        return STYLE["colors"]["status_quo"]
    if "moratorium" in name:
        return STYLE["colors"]["moratorium"]
    if "ban" in name:
        return STYLE["colors"]["ban"]
    return STYLE["colors"]["neutral"]


# =============================================================================
# Page Layout
# =============================================================================
st.set_page_config(
    page_title="GINSIM Global Policy Impact Explorer",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.title("🧪 Policy Sandbox")
st.sidebar.markdown("---")

# 1. Assumption Controls
st.sidebar.subheader("Adjust Assumptions")
deterrence_level = st.sidebar.select_slider(
    "Deterrence Elasticity", options=["Low", "Standard", "High"], value="Standard"
)
deterrence_map = {"Low": 0.05, "Standard": 0.18, "High": 0.40}

moratorium_belief = st.sidebar.select_slider(
    "Moratorium Effect", options=["Low", "Standard", "High"], value="Standard"
)
trust_map = {"Low": 0.05, "Standard": 0.15, "High": 0.30}

# NEW: EQUITY TOGGLE
st.sidebar.markdown("---")
st.sidebar.subheader("⚖️ Distributional Equity")
use_equity_weights = st.sidebar.toggle(
    "Enable Jurisdictional Equity Weighting",
    value=False,
    help="Applies weights based on Māori Health Sovereignty (NZ) or Vertical Equity (AU).",
)

with st.sidebar.expander("⚙️ Advanced Controls"):
    jurisdiction = st.selectbox(
        "Base Jurisdiction", ["Australia", "New Zealand", "UK", "Canada", "US"]
    )
    baseline_uptake = st.slider("Baseline Testing Share", 0.1, 0.9, 0.52)
    taper_range_val = st.slider("Taper Range (Glide Path $)", 0, 500000, 100000, step=10000)

st.title("🧬 Genetic Discrimination: Global Policy Explorer")
st.markdown("### Benchmarking and Equity-Weighted Analysis (Track gdpe_0031)")

STANDARD_POLICIES = get_standard_policies()

# 2. Main Narrative Tabs
tab_main, tab_bench, tab_sandbox, tab_evidence = st.tabs(
    [
        "🏠 Primary Evaluation",
        "🌐 Global Benchmarking",
        "🧪 Cross-Pollination Sandbox",
        "🔬 Evidence & Traceability",
    ]
)


@st.cache_data
def evaluate_cached(_params, policy_id):
    # Ensure policy also gets the taper_range from UI if it's a moratorium
    policy = STANDARD_POLICIES[policy_id]
    if policy_id == "moratorium":
        policy = policy.model_copy(update={"taper_range": float(taper_range_val)})
    return evaluate_single_policy(_params, policy)


def get_params(j_name, d_lvl, m_bel, b_uptake):
    p = load_jurisdiction_parameters(j_name.lower().replace(" ", "_"))
    return p.model_copy(
        update={
            "deterrence_elasticity": deterrence_map[d_lvl],
            "moratorium_effect": trust_map[m_bel],
            "baseline_testing_uptake": b_uptake,
        }
    )


# TAB 1: PRIMARY EVALUATION
with tab_main:
    policy_label = st.selectbox("Select Policy to Evaluate:", ["Status Quo", "Moratorium", "Ban"])
    selected_policy_id = policy_label.lower().replace(" ", "_")

    params_obj = get_params(jurisdiction, deterrence_level, moratorium_belief, baseline_uptake)

    if st.button("🔬 Run Evaluation", type="primary", key="main_run"):
        with st.spinner("Executing full pipeline..."):
            result = evaluate_cached(params_obj, selected_policy_id)
            st.session_state["main_result"] = result
            st.session_state["main_params"] = params_obj

    if "main_result" in st.session_state:
        res = st.session_state["main_result"]

        # Decide which welfare to show
        if use_equity_weights:
            w_impact = float(res.equity_weighted_welfare)
            w_label = "Net Social Benefit (Equity-Weighted)"
        else:
            w_impact = float(res.welfare_impact)
            w_label = "Net Social Benefit (Utilitarian)"

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Testing Uptake", f"{float(res.testing_uptake):.1%}")
        with c2:
            st.metric(w_label, f"${w_impact:,.0f}")
        with c3:
            st.metric("Market Compliance", f"{float(res.compliance_rate):.1%}")
        with c4:
            st.metric(
                "Clinical QALY Gains", f"{float(res.clinical_outcomes['total_qaly_gains']):.2f}"
            )

        col_l, col_r = st.columns([2, 1])
        with col_l:
            st.subheader("Distributional Welfare Ledger (DCBA)")
            w = res.all_metrics["welfare"]
            names = [
                "Consumer Surplus",
                "Producer Surplus",
                "Health Benefits",
                "Fiscal Impact",
                "Research Ext.",
            ]

            # Apply visual weight to bar chart if enabled
            e_factor = float(res.dcba_result.equity_factor) if use_equity_weights else 1.0

            vals = [
                w["consumer_surplus"] * e_factor,
                w["producer_surplus"],
                w["health_benefits"] * e_factor,
                w["fiscal_impact"],
                -w["research_externalities"],
            ]

            fig = go.Figure(
                go.Bar(
                    x=names,
                    y=vals,
                    marker_color=[
                        STYLE["colors"]["consumer"],
                        STYLE["colors"]["insurer"],
                        STYLE["colors"]["health"],
                        "#999999",
                        "#D55E00",
                    ],
                )
            )
            fig.update_layout(
                template="plotly_white", title=f"Stakeholder Impact (Equity Factor: {e_factor:.2f}x)"
            )
            st.plotly_chart(fig, use_container_width=True)
        with col_r:
            st.subheader("Market Indicators")
            st.write(f"**Premium High Risk:** {res.insurance_premiums['premium_high']:.3f}")
            st.write(f"**Information Gap:** {res.all_metrics['proxy']['residual_information_gap']:.1%}")
            if selected_policy_id == "moratorium":
                st.info(f"Taper Range active: ${taper_range_val:,.0f}")
            st.info(f"Jurisdiction: {jurisdiction.title()}")
            if use_equity_weights:
                st.success(f"Applying {e_factor:.2f}x weight to people-centric outcomes.")

# TAB 2: GLOBAL BENCHMARKING
with tab_bench:
    st.subheader("The Global Policy Frontier")

    if st.button("🌐 Run Global Benchmark", type="secondary"):
        countries = ["Australia", "New Zealand", "UK", "Canada", "US"]
        bench_data = []

        with st.spinner("Computing global matrix..."):
            for c in countries:
                p = get_params(c, "Standard", "Standard", 0.52)
                pid = "status_quo"
                if c == "UK":
                    pid = "moratorium"
                if c == "Canada":
                    pid = "ban"

                r = evaluate_cached(p, pid)
                if use_equity_weights:
                    val = float(r.equity_weighted_welfare)
                else:
                    val = float(r.welfare_impact)

                bench_data.append(
                    {
                        "Jurisdiction": c,
                        "Policy": pid.replace("_", " ").title(),
                        "Uptake": float(r.testing_uptake),
                        "Welfare": val,
                    }
                )

        df_bench = pd.DataFrame(bench_data)
        title_suffix = "Equity-Weighted" if use_equity_weights else "Utilitarian"
        fig_bench = px.scatter(
            df_bench,
            x="Uptake",
            y="Welfare",
            text="Jurisdiction",
            color="Policy",
            size_max=60,
            title=f"Global Efficiency Frontier ({title_suffix})",
        )
        fig_bench.update_traces(textposition="top center", marker={"size": 12})
        fig_bench.update_layout(template="plotly_white", xaxis_tickformat=".0%")
        st.plotly_chart(fig_bench, use_container_width=True)

        st.subheader("International Regulatory Matrix")
        reg_matrix = [
            {
                "Jurisdiction": "Australia",
                "Instrument": "FSC Moratorium",
                "Type": "Voluntary",
                "Thresholds": "$500k Life",
            },
            {
                "Jurisdiction": "New Zealand",
                "Instrument": "ICNZ Agreement",
                "Type": "Voluntary",
                "Thresholds": "Varies",
            },
            {
                "Jurisdiction": "UK",
                "Instrument": "ABI Code",
                "Type": "Voluntary (Semi-Statutory)",
                "Thresholds": "£500k Life",
            },
            {
                "Jurisdiction": "Canada",
                "Instrument": "GNDA",
                "Type": "Statutory (Criminal)",
                "Thresholds": "None (Full Ban)",
            },
            {
                "Jurisdiction": "US",
                "Instrument": "GINA",
                "Type": "Statutory (Federal)",
                "Thresholds": "Market-Specific (Excl. Life)",
            },
        ]
        st.table(reg_matrix)

# TAB 3: SANDBOX
with tab_sandbox:
    st.subheader("🧪 Policy Cross-Pollination")
    c_pop, c_pol = st.columns(2)
    with c_pop:
        pop_country = st.selectbox(
            "Select Population:", ["Australia", "New Zealand", "UK", "Canada", "US"]
        )
    with c_pol:
        pol_country = st.selectbox(
            "Select Policy:", ["Status Quo", "Moratorium (UK ABI)", "Statutory Ban (Canada GNDA)"]
        )

    if st.button("🧪 Run Counterfactual", type="primary"):
        params_counter = get_params(pop_country, deterrence_level, moratorium_belief, baseline_uptake)
        p_policies = get_standard_policies()
        p_obj = p_policies["status_quo"]
        if "UK" in pol_country:
            p_obj = p_policies["moratorium"]
        if "Canada" in pol_country:
            p_obj = p_policies["ban"]
        res_counter = evaluate_single_policy(params_counter, p_obj)

        st.success(f"Results for {pop_country} under {pol_country} rules:")
        sc1, sc2 = st.columns(2)
        sc1.metric("Counterfactual Uptake", f"{float(res_counter.testing_uptake):.1%}")
        if use_equity_weights:
            val_c = float(res_counter.equity_weighted_welfare)
        else:
            val_c = float(res_counter.welfare_impact)
        sc2.metric("Counterfactual Welfare", f"${val_c:,.0f}")

with tab_evidence:
    st.subheader("🧬 Diamond-Standard Traceability")
    st.caption("Equity Localization Engine v1.0 • Māori Health Sovereignty & Vertical Equity Active")

st.divider()
st.caption("Developed by Dylan A Mordaunt • 2026.03 • Equity Weights Integrated")
