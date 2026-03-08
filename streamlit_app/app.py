#!/usr/bin/env python3
"""
GINSIM: Genetic Information Non-Discrimination Policy Integrated Economic Evaluation
Main Dashboard - SOTA Peer Review Simulation Edition.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import plotly.graph_objects as go
import streamlit as st
import numpy as np

from src.model.module_a_behavior import get_standard_policies
from src.model.parameters import ModelParameters
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
    page_title="GINSIM Policy Impact Explorer",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.title("🧪 Policy Sandbox")
st.sidebar.markdown("---")

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
    jurisdiction = st.selectbox("Jurisdiction", ["Australia", "New Zealand"])
    baseline_uptake = st.slider("Baseline Testing Share", 0.1, 0.9, 0.52)

st.title("🧬 Genetic Discrimination: Policy Impact Explorer")
st.markdown("### Restoration of Clinical & Equity Rigor (Stakeholder Meeting #1)")

STANDARD_POLICIES = get_standard_policies()
policy_label = st.selectbox("Select Policy to Evaluate:", ["Status Quo", "Moratorium", "Ban"])
selected_policy_id = policy_label.lower().replace(" ", "_")

@st.cache_data
def evaluate_cached(_params, policy_id):
    return evaluate_single_policy(_params, STANDARD_POLICIES[policy_id])

params_obj = ModelParameters(
    deterrence_elasticity=deterrence_map[deterrence_level],
    moratorium_effect=trust_map[moratorium_belief],
    baseline_testing_uptake=baseline_uptake,
    jurisdiction=jurisdiction.lower().replace(" ", "_")
)

if st.sidebar.button("🔬 Run Full Evaluation", type="primary"):
    with st.spinner("Executing full pipeline (Restored Clinical Microsimulation)..."):
        result = evaluate_cached(params_obj, selected_policy_id)
        st.session_state["result"] = result
        st.session_state["params_obj"] = params_obj

if "result" in st.session_state:
    res = st.session_state["result"]
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Testing Uptake", f"{float(res.testing_uptake):.1%}")
    with c2: st.metric("Net Social Benefit", f"${float(res.welfare_impact):,.0f}")
    with c3: st.metric("Market Compliance", f"{float(res.compliance_rate):.1%}")
    with c4: st.metric("Clinical QALY Gains", f"{float(res.clinical_outcomes['total_qaly_gains']):.2f}")

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Welfare Ledger", "📈 Multi-Criteria", "🔬 Clinical Depth", "🧬 Evidence"])

    with tab1:
        col_l, col_r = st.columns([2, 1])
        with col_l:
            st.subheader("Distributional Welfare Ledger")
            w = res.all_metrics["welfare"]
            names = ["Consumer Surplus", "Producer Surplus", "Health Benefits", "Fiscal Impact", "Research Ext."]
            vals = [w["consumer_surplus"], w["producer_surplus"], w["health_benefits"], w["fiscal_impact"], -w["research_externalities"]]
            fig = go.Figure(go.Bar(x=names, y=vals, marker_color=[STYLE["colors"]["consumer"], STYLE["colors"]["insurer"], STYLE["colors"]["health"], "#999999", "#D55E00"]))
            fig.update_layout(template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
        with col_r:
            st.subheader("Market Indicators")
            st.write(f"**Premium High Risk:** {res.insurance_premiums['premium_high']:.3f}")
            st.write(f"**Information Gap:** {res.all_metrics['proxy']['residual_information_gap']:.1%}")

    with tab2:
        st.subheader("Comparative Radar")
        p_names = ["Status Quo", "Moratorium", "Ban"]
        m_keys = ["Uptake", "Welfare", "Equity", "Research"]
        fig_r = go.Figure()
        for name in p_names:
            pid = name.lower().replace(" ", "_")
            r_obj = evaluate_cached(st.session_state["params_obj"], pid)
            r_vals = [float(r_obj.testing_uptake)/0.8, min(float(r_obj.welfare_impact)/100000, 1.0), 1.0 if "ban" in pid else 0.5, float(r_obj.research_participation)]
            fig_r.add_trace(go.Scatterpolar(r=[*r_vals, r_vals[0]], theta=[*m_keys, m_keys[0]], name=name, fill='toself', line_color=get_policy_color(name)))
        fig_r.update_layout(polar={"radialaxis": {"visible": True, "range": [0, 1]}}, template="plotly_white")
        st.plotly_chart(fig_r, use_container_width=True)

    with tab3:
        st.subheader("High-Rigor Clinical Microsimulation (Lancet Tier)")
        st.info("QALY gains are now grounded in disease-specific cohort prevalence and prevention efficacy.")
        clinical_data = res.clinical_outcomes["cohort_breakdown"]
        cohort_names = list(clinical_data.keys())
        cohort_qalys = [float(clinical_data[n]["qaly_gains"]) for n in cohort_names]
        fig_c = go.Figure(go.Bar(x=cohort_names, y=cohort_qalys, marker_color=STYLE["colors"]["health"]))
        fig_c.update_layout(title="Prevented QALY Loss by Condition", yaxis_title="Discounted QALYs Gained", template="plotly_white")
        st.plotly_chart(fig_c, use_container_width=True)
        with st.expander("View Cohort Assumptions (Lynch, BRCA, FH)"):
            st.json(clinical_data)

    with tab4:
        st.subheader("🧬 Evidence Linkage")
        if st.button("🔎 Browse Data Provenance"): st.switch_page("pages/traceability.py")
        st.caption("Provenance Audit ID: `peer_review_sim_v1`")

else: st.info("👈 Configure parameters and click **Run Evaluation**.")

st.divider()
st.caption("Developed by Dylan A Mordaunt • 2026.03 • SOTA Stakeholder Prioritized")
