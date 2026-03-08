#!/usr/bin/env python3
"""
GINSIM: Genetic Information Non-Discrimination Policy Integrated Economic Evaluation
Main Dashboard - SOTA Global Benchmarking Edition.
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
import numpy as np

from src.model.module_a_behavior import get_standard_policies
from src.model.parameters import ModelParameters, load_jurisdiction_parameters
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
        "health": "#CC79A7"
    },
}

def get_policy_color(policy_name: str) -> str:
    name = policy_name.lower().replace(" ", "_")
    if 'status_quo' in name: return STYLE['colors']['status_quo']
    if 'moratorium' in name: return STYLE['colors']['moratorium']
    if 'ban' in name: return STYLE['colors']['ban']
    return STYLE['colors']['neutral']

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
    "Deterrence Elasticity",
    options=["Low", "Standard", "High"],
    value="Standard"
)
deterrence_map = {"Low": 0.05, "Standard": 0.18, "High": 0.40}

moratorium_belief = st.sidebar.select_slider(
    "Moratorium Effect",
    options=["Low", "Standard", "High"],
    value="Standard"
)
trust_map = {"Low": 0.05, "Standard": 0.15, "High": 0.30}

with st.sidebar.expander("⚙️ Advanced Controls"):
    jurisdiction = st.selectbox("Base Jurisdiction", ["Australia", "New Zealand", "UK", "Canada", "US"])
    baseline_uptake = st.slider("Baseline Testing Share", 0.1, 0.9, 0.52)

st.title("🧬 Genetic Discrimination: Global Policy Explorer")
st.markdown("### Benchmarking and Cross-Pollination Analysis (Track gdpe_0030)")

STANDARD_POLICIES = get_standard_policies()

# 2. Main Narrative Tabs
tab_main, tab_bench, tab_sandbox, tab_evidence = st.tabs([
    "🏠 Primary Evaluation", 
    "🌐 Global Benchmarking", 
    "🧪 Cross-Pollination Sandbox",
    "🔬 Evidence & Traceability"
])

@st.cache_data
def evaluate_cached(_params, policy_id):
    return evaluate_single_policy(_params, STANDARD_POLICIES[policy_id])

def get_params(j_name, d_lvl, m_bel, b_uptake):
    p = load_jurisdiction_parameters(j_name.lower().replace(" ", "_"))
    return p.model_copy(update={
        "deterrence_elasticity": deterrence_map[d_lvl],
        "moratorium_effect": trust_map[m_bel],
        "baseline_testing_uptake": b_uptake,
    })

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
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.metric("Testing Uptake", f"{float(res.testing_uptake):.1%}")
        with c2: st.metric("Net Social Benefit (PPP)", f"${float(res.welfare_impact):,.0f}")
        with c3: st.metric("Market Compliance", f"{float(res.compliance_rate):.1%}")
        with c4: st.metric("Clinical QALY Gains", f"{float(res.clinical_outcomes['total_qaly_gains']):.2f}")

        col_l, col_r = st.columns([2, 1])
        with col_l:
            st.subheader("Distributional Welfare Ledger (DCBA)")
            w = res.all_metrics["welfare"]
            names = ["Consumer Surplus", "Producer Surplus", "Health Benefits", "Fiscal Impact", "Research Ext."]
            vals = [w["consumer_surplus"], w["producer_surplus"], w["health_benefits"], w["fiscal_impact"], -w["research_externalities"]]
            fig = go.Figure(go.Bar(x=names, y=vals, marker_color=[STYLE["colors"]["consumer"], STYLE["colors"]["insurer"], STYLE["colors"]["health"], "#999999", "#D55E00"]))
            fig.update_layout(template="plotly_white", title="PPP-Normalized Stakeholder Impact")
            st.plotly_chart(fig, use_container_width=True)
        with col_r:
            st.subheader("Market Indicators")
            st.write(f"**Premium High Risk:** {res.insurance_premiums['premium_high']:.3f}")
            st.write(f"**Information Gap:** {res.all_metrics['proxy']['residual_information_gap']:.1%}")
            st.info(f"Currency: {jurisdiction} (Adjusted via PPP: {params_obj.ppp_conversion_factor:.2f}x)")

# TAB 2: GLOBAL BENCHMARKING
with tab_bench:
    st.subheader("The Global Policy Frontier")
    st.markdown("Comparing all jurisdictions under their respective primary policies.")
    
    if st.button("🌐 Run Global Benchmark", type="secondary"):
        countries = ["Australia", "New Zealand", "UK", "Canada", "US"]
        bench_data = []
        
        with st.spinner("Computing global matrix..."):
            for c in countries:
                p = get_params(c, "Standard", "Standard", 0.52)
                # Map primary policy for each country
                pid = "status_quo"
                if c == "UK": pid = "moratorium"
                if c == "Canada": pid = "ban"
                
                r = evaluate_cached(p, pid)
                bench_data.append({
                    "Jurisdiction": c,
                    "Policy": pid.replace("_", " ").title(),
                    "Uptake": float(r.testing_uptake),
                    "Welfare": float(r.welfare_impact)
                })
        
        df_bench = pd.DataFrame(bench_data)
        fig_bench = px.scatter(
            df_bench, x="Uptake", y="Welfare", text="Jurisdiction", 
            color="Policy", size_max=60,
            title="Global Efficiency Frontier (PPP Normalized)"
        )
        fig_bench.update_traces(textposition='top center', marker=dict(size=12))
        fig_bench.update_layout(template="plotly_white", xaxis_tickformat=".0%")
        st.plotly_chart(fig_bench, use_container_width=True)
        
        st.subheader("International Regulatory Matrix")
        reg_matrix = [
            {"Jurisdiction": "Australia", "Instrument": "FSC Moratorium", "Type": "Voluntary", "Thresholds": "$500k Life"},
            {"Jurisdiction": "New Zealand", "Instrument": "ICNZ Agreement", "Type": "Voluntary", "Thresholds": "Varies"},
            {"Jurisdiction": "UK", "Instrument": "ABI Code", "Type": "Voluntary (Semi-Statutory)", "Thresholds": "£500k Life"},
            {"Jurisdiction": "Canada", "Instrument": "GNDA", "Type": "Statutory (Criminal)", "Thresholds": "None (Full Ban)"},
            {"Jurisdiction": "US", "Instrument": "GINA", "Type": "Statutory (Federal)", "Thresholds": "Market-Specific (Excl. Life)"}
        ]
        st.table(reg_matrix)

# TAB 3: CROSS-POLLINATION SANDBOX
with tab_sandbox:
    st.subheader("🧪 Policy Cross-Pollination")
    st.markdown("What if we applied one country's policy to another country's population?")
    
    c_pop, c_pol = st.columns(2)
    with c_pop:
        pop_country = st.selectbox("Select Population (Demographics & Costs):", ["Australia", "New Zealand", "UK", "Canada", "US"])
    with c_pol:
        pol_country = st.selectbox("Select Policy (Rules & Thresholds):", ["Status Quo", "UK Moratorium", "Canadian Ban"])
    
    if st.button("🧪 Run Counterfactual", type="primary"):
        # 1. Load population params
        params_counter = get_params(pop_country, deterrence_level, moratorium_belief, baseline_uptake)
        
        # 2. Select policy object
        p_policies = get_standard_policies()
        p_obj = p_policies["status_quo"]
        if "UK" in pol_country: p_obj = p_policies["moratorium"]
        if "Canadian" in pol_country: p_obj = p_policies["ban"]
        
        res_counter = evaluate_single_policy(params_counter, p_obj)
        
        st.success(f"Results for {pop_country} under {pol_country} rules:")
        sc1, sc2 = st.columns(2)
        sc1.metric("Counterfactual Uptake", f"{float(res_counter.testing_uptake):.1%}")
        sc2.metric("Counterfactual Welfare (PPP)", f"${float(res_counter.welfare_impact):,.0f}")

# TAB 4: EVIDENCE
with tab_evidence:
    st.subheader("🧬 Diamond-Standard Traceability")
    if st.button("🔎 Browse Data Provenance"): st.switch_page("pages/traceability.py")
    st.caption("Global Benchmarking Engine v1.0 • Built with JAX & Streamlit")

st.divider()
st.caption("Developed by Dylan A Mordaunt • 2026.03 • Global Benchmarking Enabled")
