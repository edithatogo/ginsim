#!/usr/bin/env python3
"""
GINSIM: Genetic Information Non-Discrimination Policy Integrated Economic Evaluation
Main Dashboard - SOTA Temporal Evolution Edition.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.model.module_a_behavior import compute_testing_uptake, get_standard_policies
from src.model.parameters import load_jurisdiction_parameters
from src.model.pipeline import evaluate_single_policy, simulate_evolution

try:
    from streamlit_app.dashboard_ui import (
        render_current_run_summary,
        render_footer,
        render_glossary,
        render_sidebar_build_info,
        render_start_here,
        render_view_mode_sidebar,
    )
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from dashboard_ui import (
        render_current_run_summary,
        render_footer,
        render_glossary,
        render_sidebar_build_info,
        render_start_here,
        render_view_mode_sidebar,
    )

try:
    from src.model.adversarial_engine import AdversarialEngine
except ImportError:
    AdversarialEngine = None

try:
    from src.model.agentic_auditor import AgenticAuditor
    from src.utils.persona_distiller import PersonaDistiller
except ImportError:
    AgenticAuditor = None
    PersonaDistiller = None

try:
    from src.utils.hta_export import HTAExporter
except ImportError:
    HTAExporter = None

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

ADVERSARIAL_ENGINE_AVAILABLE = AdversarialEngine is not None
AUDITOR_LAYER_AVAILABLE = AgenticAuditor is not None and PersonaDistiller is not None
HTA_EXPORT_AVAILABLE = HTAExporter is not None
GENERAL_POLICY_LABELS = {
    "status_quo": "Current Rules",
    "moratorium": "Temporary Ban",
    "ban": "Full Ban",
}
GENERAL_POLICY_TO_ID = {label: key for key, label in GENERAL_POLICY_LABELS.items()}


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
audience_mode = render_view_mode_sidebar()

# 1. Assumption Controls
st.sidebar.subheader("Choose what to explore")
if audience_mode == "General audience":
    jurisdiction = st.sidebar.selectbox(
        "Country", ["Australia", "New Zealand", "UK", "Canada", "US"]
    )
else:
    jurisdiction = "Australia"

deterrence_level = st.sidebar.select_slider(
    "How much fear reduces testing", options=["Low", "Standard", "High"], value="Standard"
)
deterrence_map = {"Low": 0.05, "Standard": 0.18, "High": 0.40}

if audience_mode == "General audience":
    moratorium_belief = "Standard"
else:
    moratorium_belief = st.sidebar.select_slider(
        "How reassuring restrictions feel", options=["Low", "Standard", "High"], value="Standard"
    )
trust_map = {"Low": 0.05, "Standard": 0.15, "High": 0.30}

# EQUITY TOGGLE
st.sidebar.markdown("---")
if audience_mode != "General audience":
    st.sidebar.subheader("⚖️ Distributional Equity")
    use_equity_weights = st.sidebar.toggle(
        "Enable Jurisdictional Equity Weighting",
        value=False,
        help="Applies weights based on Māori Health Sovereignty (NZ) or Vertical Equity (AU).",
    )
else:
    use_equity_weights = False

if audience_mode != "General audience":
    st.sidebar.subheader("🤖 Governance & Audit")
    if AUDITOR_LAYER_AVAILABLE:
        enable_auditor = st.sidebar.toggle(
            "Enable audit panel",
            value=True,
            help="Turns on the stakeholder-audit surface used in research and policy mode.",
        )
    else:
        enable_auditor = False
        st.sidebar.caption("Audit panel unavailable in this deployment.")
else:
    enable_auditor = False

with st.sidebar.expander("⚙️ Advanced Controls"):
    if audience_mode != "General audience":
        jurisdiction = st.selectbox(
            "Base Jurisdiction", ["Australia", "New Zealand", "UK", "Canada", "US"]
        )
        baseline_uptake = st.slider("Baseline Testing Share", 0.1, 0.9, 0.52)
        taper_range_val = st.slider("Taper Range (Glide Path $)", 0, 500000, 100000, step=10000)
        simulation_year = st.slider(
            "Simulation Year (Horizon)",
            0,
            10,
            0,
            help="0 = Current Year (2026), 10 = 10 Years Future (2036).",
        )
    else:
        baseline_uptake = st.slider(
            "Typical testing rate before policy changes",
            0.1,
            0.9,
            0.52,
            help="A rough starting point for how many people would test without a new policy.",
        )
        taper_range_val = 100000
        simulation_year = 0

render_sidebar_build_info()

st.title("🧬 Genetic Discrimination: Global Policy Explorer")
st.markdown("### Benchmarking and Temporal Evolution Analysis")
render_start_here(audience_mode)
render_glossary(audience_mode)
render_current_run_summary(
    "Current Sandbox Context",
    {
        "Jurisdiction": jurisdiction,
        "Deterrence": deterrence_level,
        "Moratorium": moratorium_belief,
        "Equity": "On" if use_equity_weights else "Off",
        "Audit Layer": (
            "On"
            if enable_auditor
            else ("Unavailable" if not AUDITOR_LAYER_AVAILABLE else "Off")
        ),
    },
)

STANDARD_POLICIES = get_standard_policies()

# 2. Main Narrative Tabs
if audience_mode == "General audience":
    tab_order = [
        ("main", "1. 🏠 Start Here"),
        ("bench", "2. 🌍 Compare Countries"),
        ("sandbox", "3. 🔄 Try Policy Scenarios"),
    ]
else:
    tab_order = [
        ("main", "🏠 Primary Evaluation"),
        ("bench", "🌍 Global Benchmarking"),
        ("sandbox", "🧪 Cross-Pollination Sandbox"),
        ("spatial", "🗺️ Spatial Equity"),
        ("redteam", "🔴 Adversarial Red-Teaming"),
        ("delphi", "🧑‍⚖️ Stakeholder Consensus"),
        ("interop", "🔄 Interoperability"),
        ("evidence", "🔬 Evidence & Traceability"),
    ]

tabs = st.tabs([label for _, label in tab_order])
tab_map = {key: tab for (key, _), tab in zip(tab_order, tabs, strict=False)}


@st.cache_data
def evaluate_cached(_params, policy_id, year=0):
    policy = STANDARD_POLICIES[policy_id]
    if policy_id == "moratorium":
        policy = policy.model_copy(update={"taper_range": float(taper_range_val)})
    return evaluate_single_policy(_params, policy, year=year)


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
with tab_map["main"]:
    if audience_mode == "General audience":
        st.caption("Step 1 of 3: choose a policy and see the main result.")
    if audience_mode == "General audience":
        policy_label = st.selectbox(
            "Choose a policy",
            list(GENERAL_POLICY_LABELS.values()),
        )
        selected_policy_id = GENERAL_POLICY_TO_ID[policy_label]
    else:
        policy_label = st.selectbox(
            "Select Policy to Evaluate:", ["Status Quo", "Moratorium", "Ban"]
        )
        selected_policy_id = policy_label.lower().replace(" ", "_")

    params_obj = get_params(jurisdiction, deterrence_level, moratorium_belief, baseline_uptake)
    render_current_run_summary(
        "Evaluation Context",
        {
            "Policy": policy_label,
            "Horizon": f"Year {simulation_year}",
            "Base Uptake": f"{baseline_uptake:.0%}",
            "Audit Layer": "On" if enable_auditor else "Off",
        },
    )

    c_run, c_temp = st.columns(2)
    with c_run:
        if st.button("🔬 Run Evaluation", type="primary", key="main_run"):
            with st.spinner(f"Executing pipeline for Year {simulation_year}..."):
                result = evaluate_cached(params_obj, selected_policy_id, year=simulation_year)
                st.session_state["main_result"] = result
                st.session_state["main_params"] = params_obj

    if audience_mode != "General audience":
        with c_temp:
            if st.button("📈 Project 10-Year Trajectory", type="secondary"):
                with st.spinner("Simulating temporal evolution..."):
                    target_policy = STANDARD_POLICIES[selected_policy_id]
                    history_bundle = simulate_evolution(params_obj, target_policy)
                    st.session_state["temporal_history"] = history_bundle["annual"]
                    st.session_state["aggregate_result"] = history_bundle["aggregate"]
    else:
        with c_temp:
            st.caption("Advanced projections are available in `Research / policy` mode.")

    if "main_result" in st.session_state:
        res = st.session_state["main_result"]
        st.info(f"Viewing results for **Year {simulation_year}**.")

        if use_equity_weights:
            w_impact = float(res.equity_weighted_welfare)
            w_label = "Net Social Benefit (Equity-Weighted)"
        else:
            w_impact = float(res.welfare_impact)
            w_label = "Net Social Benefit (Utilitarian)"

        uptake_label = (
            "People choosing genetic testing"
            if audience_mode == "General audience"
            else "Testing Uptake"
        )
        welfare_label = (
            "Overall benefit to society" if audience_mode == "General audience" else w_label
        )
        compliance_label = (
            "Insurers following the rules"
            if audience_mode == "General audience"
            else "Market Compliance"
        )
        qaly_label = "Health gains" if audience_mode == "General audience" else "Clinical QALY Gains"

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric(
                uptake_label,
                f"{float(res.testing_uptake):.0%}"
                if audience_mode == "General audience"
                else f"{float(res.testing_uptake):.1%}",
            )
        with c2:
            st.metric(welfare_label, f"${w_impact:,.0f}")
        with c3:
            st.metric(
                compliance_label,
                f"{float(res.compliance_rate):.0%}"
                if audience_mode == "General audience"
                else f"{float(res.compliance_rate):.1%}",
            )
        with c4:
            st.metric(
                qaly_label,
                f"{float(res.clinical_outcomes['total_qaly_gains']):.1f}"
                if audience_mode == "General audience"
                else f"{float(res.clinical_outcomes['total_qaly_gains']):.2f}",
            )

        if audience_mode == "General audience":
            if w_impact > 0:
                welfare_direction = "helps overall"
            elif w_impact < 0:
                welfare_direction = "looks worse overall"
            else:
                welfare_direction = "looks neutral overall"
            st.success(
                f"In plain language: under **{policy_label}**, about **{float(res.testing_uptake):.0%}** of people choose testing, "
                f"insurer rule-following is **{float(res.compliance_rate):.0%}**, and the policy **{welfare_direction}** in this model."
            )
            st.subheader("What changed?")
            premium_high = float(res.insurance_premiums["premium_high"])
            uninsured_rate = float(res.insurance_premiums["uninsured_rate"])
            takeaway_rows = pd.DataFrame(
                [
                    {
                        "Area": "People choosing testing",
                        "Value": float(res.testing_uptake),
                    },
                    {
                        "Area": "Insurers following the rules",
                        "Value": float(res.compliance_rate),
                    },
                    {
                        "Area": "People left uninsured",
                        "Value": uninsured_rate,
                    },
                ]
            )
            fig_simple = px.bar(
                takeaway_rows,
                x="Area",
                y="Value",
                title="Three headline effects",
                color="Area",
                color_discrete_sequence=["#56B4E9", "#009E73", "#D55E00"],
            )
            fig_simple.update_layout(template="plotly_white", showlegend=False, yaxis_tickformat=".0%")
            st.plotly_chart(fig_simple, use_container_width=True)
            st.markdown(
                f"- **Testing:** about **{float(res.testing_uptake):.0%}** of people choose testing.\n"
                f"- **Rule-following:** insurers follow the rules about **{float(res.compliance_rate):.0%}** of the time.\n"
                f"- **Insurance pressure:** the model's high-risk premium is about **{premium_high:.1f}**, and about **{uninsured_rate:.0%}** are left uninsured."
            )
        else:
            col_l, col_r = st.columns([2, 1])
            with col_l:
                st.subheader("Stakeholder Impact Ledger")
                w = res.all_metrics["welfare"]
                names = ["Consumer", "Insurer", "Health", "Fiscal", "Research"]
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
                        marker_color=["#56B4E9", "#E69F00", "#CC79A7", "#999999", "#D55E00"],
                    )
                )
                fig.update_layout(template="plotly_white")
                st.plotly_chart(fig, use_container_width=True)

            with col_r:
                st.subheader("Market Indicators")
                st.write(f"**Premium High Risk:** {res.insurance_premiums['premium_high']:.3f}")
                gap = res.all_metrics["proxy"]["residual_information_gap"]
                redundancy = res.all_metrics["proxy"].get("informational_redundancy", 0.0)
                ev_key = res.all_metrics["proxy"].get("source_evidence_key", "N/A")
                st.write(f"**Information Gap:** {gap:.1%}")
                st.write(f"**Informational Redundancy:** {redundancy:.1%}")
                st.caption(f"Evidence Anchor: `{ev_key}`")

        if audience_mode != "General audience":
            with st.expander("Technical Proofs"):
                proofs = res.all_metrics.get("proofs", {})
                if proofs:
                    p1, p2, p3 = st.columns(3)
                    p1.metric("Equilibrium Type", str(proofs.get("equilibrium_type", "n/a")).title())
                    p2.metric(
                        "FOC Residual",
                        f"{float(proofs.get('premium_stationarity', 0.0)):.3e}",
                    )
                    p3.metric(
                        "Compliance Residual",
                        f"{float(proofs.get('compliance_fixed_point_residual', 0.0)):.3e}",
                    )
                    st.caption(
                        "Jacobian and Hessian diagnostics are computed from the current policy solve."
                    )
                    st.write(
                        f"Jacobian: `{float(proofs.get('premium_jacobian', 0.0)):.3e}`  "
                        f"Hessian: `{float(proofs.get('premium_hessian', 0.0)):.3e}`"
                    )
                else:
                    st.info("Proof diagnostics will appear after an evaluation run.")

    if "temporal_history" in st.session_state:
        st.divider()
        st.subheader("📅 10-Year Market Trajectory")
        hist = st.session_state["temporal_history"]

        # Display aggregate welfare
        agg_res = st.session_state["aggregate_result"]
        st.success(f"Aggregate 10-Year Net Welfare: **${float(agg_res.welfare_impact):,.0f}**")

        df_hist = pd.DataFrame(
            [
                {
                    "Year": year,
                    "Uptake": float(res.testing_uptake),
                    "Premium (High)": float(res.insurance_premiums["premium_high"]),
                    "Premium (Low)": float(res.insurance_premiums["premium_low"]),
                    "Welfare": float(res.welfare_impact),
                }
                for year, res in hist.items()
            ]
        )

        c_h1, c_h2 = st.columns(2)
        with c_h1:
            fig_u = px.line(df_hist, x="Year", y="Uptake", title="Testing Uptake Projection")
            fig_u.update_layout(template="plotly_white", yaxis_tickformat=".0%")
            st.plotly_chart(fig_u, use_container_width=True)
        with c_h2:
            fig_p = px.line(
                df_hist, x="Year", y=["Premium (High)", "Premium (Low)"], title="Premium Evolution"
            )
            fig_p.update_layout(template="plotly_white")
            st.plotly_chart(fig_p, use_container_width=True)

        st.info(
            "The projection accounts for annual technological drift (increasing proxy accuracy) and inflationary pressure on regulatory thresholds."
        )

# TAB 2: GLOBAL BENCHMARKING
with tab_map["bench"]:
    if audience_mode == "General audience":
        st.caption("Step 2 of 3: see how the broad result changes across countries.")
    st.subheader(
        "How countries compare"
        if audience_mode == "General audience"
        else "The Global Policy Frontier"
    )
    if audience_mode == "General audience":
        st.caption("Use this page to see how the broad result changes across countries.")
    if st.button(
        "🌐 Compare countries" if audience_mode == "General audience" else "🌐 Run Global Benchmark",
        type="primary" if audience_mode == "General audience" else "secondary",
    ):
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
                val = (
                    float(r.equity_weighted_welfare)
                    if use_equity_weights
                    else float(r.welfare_impact)
                )
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
        if audience_mode == "General audience":
            best_row = df_bench.sort_values("Welfare", ascending=False).iloc[0]
            st.success(
                f"Headline result: in this comparison, **{best_row['Jurisdiction']}** has the strongest overall result "
                f"with about **{best_row['Uptake']:.0%}** testing uptake."
            )
            fig_bench = px.bar(
                df_bench.sort_values("Welfare", ascending=False),
                x="Jurisdiction",
                y="Welfare",
                color="Jurisdiction",
                title="Overall social benefit by country",
            )
            fig_bench.update_layout(template="plotly_white", showlegend=False)
            st.plotly_chart(fig_bench, use_container_width=True)
        else:
            fig_bench = px.scatter(
                df_bench,
                x="Uptake",
                y="Welfare",
                text="Jurisdiction",
                color="Policy",
                title=f"Global Efficiency Frontier ({title_suffix})",
            )
            fig_bench.update_traces(textposition="top center", marker={"size": 12})
            fig_bench.update_layout(template="plotly_white", xaxis_tickformat=".0%")
            st.plotly_chart(fig_bench, use_container_width=True)

# TAB 3: SANDBOX
with tab_map["sandbox"]:
    if audience_mode == "General audience":
        st.caption("Step 3 of 3: try a different country's rules on the selected population.")
    st.subheader(
        "🔄 Try policy scenarios"
        if audience_mode == "General audience"
        else "🧪 Policy Cross-Pollination"
    )
    if audience_mode == "General audience":
        st.caption("Pick a population and apply a different country's policy rules to it.")
    c_pop, c_pol = st.columns(2)
    with c_pop:
        pop_country = st.selectbox(
            "Select Population:", ["Australia", "New Zealand", "UK", "Canada", "US"]
        )
    with c_pol:
        if audience_mode == "General audience":
            pol_country = st.selectbox(
                "Choose policy rules:",
                ["Current Rules", "Temporary Ban", "Full Ban"],
            )
        else:
            pol_country = st.selectbox(
                "Select Policy:",
                ["Status Quo", "Moratorium (UK ABI)", "Statutory Ban (Canada GNDA)"],
            )
    if st.button(
        "🔄 Try this scenario" if audience_mode == "General audience" else "🧪 Run Counterfactual",
        type="primary",
    ):
        params_counter = get_params(
            pop_country, deterrence_level, moratorium_belief, baseline_uptake
        )
        p_policies = get_standard_policies()
        p_obj = p_policies["status_quo"]
        if pol_country in {"Temporary Ban", "Moratorium (UK ABI)"}:
            p_obj = p_policies["moratorium"]
        if pol_country in {"Full Ban", "Statutory Ban (Canada GNDA)"}:
            p_obj = p_policies["ban"]
        res_counter = evaluate_single_policy(params_counter, p_obj)
        st.success(f"Results for {pop_country} under {pol_country} rules:")
        sc1, sc2 = st.columns(2)
        sc1.metric(
            "Counterfactual Uptake",
            f"{float(res_counter.testing_uptake):.0%}"
            if audience_mode == "General audience"
            else f"{float(res_counter.testing_uptake):.1%}",
        )
        val_c = (
            float(res_counter.equity_weighted_welfare)
            if use_equity_weights
            else float(res_counter.welfare_impact)
        )
        sc2.metric("Counterfactual Welfare", f"${val_c:,.0f}")
        if audience_mode == "General audience":
            st.info(
                f"Plain-language takeaway: if **{pop_country}** used **{pol_country}** rules, the model predicts "
                f"about **{float(res_counter.testing_uptake):.0%}** testing uptake and overall social benefit of "
                f"**${val_c:,.0f}**."
            )
            compare_df = pd.DataFrame(
                [
                    {"Measure": "Testing uptake", "Value": float(res_counter.testing_uptake)},
                    {"Measure": "Compliance", "Value": float(res_counter.compliance_rate)},
                ]
            )
            fig_counter = px.bar(
                compare_df,
                x="Measure",
                y="Value",
                color="Measure",
                title="Two quick checks for this scenario",
                color_discrete_sequence=["#56B4E9", "#009E73"],
            )
            fig_counter.update_layout(template="plotly_white", showlegend=False, yaxis_tickformat=".0%")
            st.plotly_chart(fig_counter, use_container_width=True)

if "spatial" in tab_map:
    # TAB 4: SPATIAL EQUITY
    with tab_map["spatial"]:
        st.subheader("Map of 'Diagnostic Deserts' and Access Equity")
        current_params = get_params(
            jurisdiction, deterrence_level, moratorium_belief, baseline_uptake
        )
        if st.button("🗺️ Generate Remoteness Profile", type="primary"):
            remoteness_levels = np.linspace(0.0, 1.0, 10)
            spatial_results = []
            with st.spinner("Simulating geographic sweep..."):
                for policy_name, policy_obj in STANDARD_POLICIES.items():
                    for r_idx in remoteness_levels:
                        uptake = compute_testing_uptake(
                            current_params, policy_obj, remoteness_index=float(r_idx)
                        )
                        spatial_results.append(
                            {
                                "Policy": policy_name.replace("_", " ").title(),
                                "Remoteness": r_idx,
                                "Uptake": float(uptake),
                            }
                        )
            df_spatial = pd.DataFrame(spatial_results)
            fig_spatial = px.line(
                df_spatial,
                x="Remoteness",
                y="Uptake",
                color="Policy",
                title=f"Testing Uptake Decay by Geographic Remoteness ({jurisdiction.title()})",
            )
            fig_spatial.update_layout(template="plotly_white", yaxis_tickformat=".0%")
            st.plotly_chart(fig_spatial, use_container_width=True)
if "redteam" in tab_map:
    with tab_map["redteam"]:
        st.subheader("🔴 Economic Red-Teaming (Stress Testing)")
        st.write(
            "Find the 'Worst-Case' parameters that collapse a policy's welfare gain using gradient-based optimization (JAX/Optax)."
        )
        if not ADVERSARIAL_ENGINE_AVAILABLE:
            st.info(
                "Economic red-teaming is unavailable in this deployment because the adversarial engine "
                "module is not part of the current shipped code surface."
            )
        else:
            c_rt1, c_rt2 = st.columns(2)
            with c_rt1:
                rt_policy = st.selectbox("Policy to Stress Test:", ["Moratorium", "Ban"])
                rt_steps = st.slider("Optimization Steps", 50, 300, 100)
            with c_rt2:
                rt_lr = st.slider("Learning Rate", 0.01, 0.20, 0.05)
                rt_individuals = st.number_input(
                    "Individuals for Uptake Simulation", 100, 2000, 500
                )

            if st.button("🚀 Run Adversarial Search", type="primary"):
                engine = AdversarialEngine(
                    learning_rate=rt_lr, steps=rt_steps, n_individuals=int(rt_individuals)
                )

                current_params = get_params(
                    jurisdiction, deterrence_level, moratorium_belief, baseline_uptake
                )
                p_target = STANDARD_POLICIES[rt_policy.lower()]
                p_base = STANDARD_POLICIES["status_quo"]

                with st.spinner(f"Searching for failure modes of '{rt_policy}'..."):
                    rt_result = engine.find_worst_case(p_target, p_base, current_params)

                if rt_result.success:
                    st.success(
                        f"Worst-Case Scenario Found (Welfare Delta: ${rt_result.min_welfare_delta:,.2f}M)"
                    )

                    st.write("### Adversarial Parameter Combination")

                    theta = rt_result.worst_case_theta
                    col_p1, col_p2, col_p3 = st.columns(3)
                    col_p1.metric("Optimized Prevalence", f"{theta['final_proportion_high']:.1%}")
                    col_p2.metric("Optimized Loading", f"{theta['final_loading']:.1%}")
                    col_p3.metric("Fear Elasticity", f"{theta['final_as_elasticity']:.2f}")

                    col_p4, col_p5, col_p6 = st.columns(3)
                    col_p4.metric("High-Risk Cost", f"{theta['final_risk_high']:.2f}")
                    col_p5.metric("Low-Risk Cost", f"{theta['final_risk_low']:.2f}")
                    col_p6.metric(
                        "High-Risk Elasticity", f"{theta['final_demand_elasticity_high']:.2f}"
                    )

                    st.warning(
                        f"**Interpretation:** In this scenario, the {rt_policy} policy delivers its minimum value. "
                        "The model 'broke' the policy by maximizing the prevalence of high-risk individuals and the markup (loading), "
                        "while making people extremely sensitive to the 'fear of discrimination' (as_elasticity)."
                    )

                    st.write("### Comparison under Stress-Test Parameters")

                    res_r = rt_result.reform_welfare_result
                    res_b = rt_result.baseline_welfare_result

                    if res_r and res_b:
                        comp_data = []

                        def add_comp(name, r_val, b_val):
                            comp_data.append(
                                {"Component": name, "Policy": rt_policy, "Value ($M)": float(r_val)}
                            )
                            comp_data.append(
                                {
                                    "Component": name,
                                    "Policy": "Status Quo",
                                    "Value ($M)": float(b_val),
                                }
                            )

                        add_comp("Consumer Surplus", res_r.consumer_surplus, res_b.consumer_surplus)
                        add_comp("Insurer Profits", res_r.producer_surplus, res_b.producer_surplus)
                        add_comp("Health Benefits", res_r.health_benefits, res_b.health_benefits)
                        add_comp("Fiscal Impact", res_r.fiscal_impact, res_b.fiscal_impact)

                        df_comp = pd.DataFrame(comp_data)
                        fig_comp = px.bar(
                            df_comp,
                            x="Component",
                            y="Value ($M)",
                            color="Policy",
                            barmode="group",
                            title=f"Welfare Components: {rt_policy} vs Status Quo (Worst-Case)",
                        )
                        fig_comp.update_layout(template="plotly_white")
                        st.plotly_chart(fig_comp, use_container_width=True)

                    st.write("### Optimization Path (Robustness Search)")
                    if rt_result.loss_history:
                        df_loss = pd.DataFrame(
                            {
                                "Step": range(len(rt_result.loss_history)),
                                "Welfare Delta ($M)": rt_result.loss_history,
                            }
                        )
                        fig_loss = px.line(
                            df_loss,
                            x="Step",
                            y="Welfare Delta ($M)",
                            title="Gradient Descent towards Failure",
                        )
                        fig_loss.update_layout(template="plotly_white")
                        st.plotly_chart(fig_loss, use_container_width=True)

                        st.info(
                            "The optimization seeks the parameter set that minimizes the welfare difference between the Reform and Status Quo. "
                            "A negative value indicates the reform is actively worse than doing nothing under these adversarial assumptions."
                        )

                else:
                    st.error("Optimization failed to converge or returned NaNs.")

if "delphi" in tab_map:
    # TAB 5: STAKEHOLDER CONSENSUS
    with tab_map["delphi"]:
        st.subheader("🧑‍⚖️ Agentic Delphi Protocol")
        st.write(
            "Simulate a consensus-building process among diverse stakeholder personas (Treasury, Lancet, etc.)."
        )

        if not AUDITOR_LAYER_AVAILABLE:
            st.info(
                "The agentic audit layer is unavailable in this deployment because the auditor "
                "modules are not part of the current shipped code surface."
            )
        elif not enable_auditor:
            st.warning(
                "Agentic Audit Layer is disabled in the sidebar. Please enable it to use this feature."
            )
        elif "main_result" not in st.session_state:
            st.warning("Please run a primary evaluation first to provide data for the audit.")
        else:
            res = st.session_state["main_result"]

            if "auditor" not in st.session_state:
                st.session_state["auditor"] = AgenticAuditor()
            auditor = st.session_state["auditor"]
            distiller = PersonaDistiller()

            with st.expander("🎓 Teach New Persona from Policy Document"):
                st.write(
                    "Provide a text-based policy statement to 'distill' a new stakeholder persona."
                )
                custom_name = st.text_input("Persona Name:", placeholder="e.g., Māori Health Board")
                policy_text = st.text_area(
                    "Policy Statement / Text:",
                    height=150,
                    placeholder="Paste policy document text here...",
                )

                if st.button("🧠 Distill & Add Persona"):
                    if custom_name and policy_text:
                        with st.spinner("Distilling priorities..."):
                            new_config = distiller.distill_persona(policy_text, name=custom_name)
                            auditor.add_persona(new_config)
                            st.success(
                                f"Persona '{custom_name}' taught successfully and added to registry."
                            )
                            if "delphi_history" in st.session_state:
                                del st.session_state["delphi_history"]
                    else:
                        st.error("Please provide both a name and policy text.")
            st.divider()

            c_del1, c_del2 = st.columns([1, 2])
            with c_del1:
                delphi_rounds = st.slider("Delphi Rounds", 1, 5, 3)
                if st.button("⚖️ Initiate Audit & Consensus", type="primary"):
                    with st.spinner("Simulating stakeholder meeting..."):
                        history = auditor.run_delphi_session(
                            res.dcba_result, max_rounds=delphi_rounds
                        )
                        st.session_state["delphi_history"] = history

            if "delphi_history" in st.session_state:
                history = st.session_state["delphi_history"]
                last_round = history[-1]

                with c_del2:
                    div_data = [
                        auditor.compute_divergence(r)["coefficient_of_variation"] for r in history
                    ]
                    df_div = pd.DataFrame(
                        {
                            "Round": range(1, len(div_data) + 1),
                            "Epistemic Divergence (CV)": div_data,
                        }
                    )
                    fig_div = px.line(
                        df_div,
                        x="Round",
                        y="Epistemic Divergence (CV)",
                        title="Consensus Trend (Delphi Protocol)",
                    )
                    fig_div.update_layout(template="plotly_white")
                    st.plotly_chart(fig_div, use_container_width=True)

                st.divider()
                col_v1, col_v2 = st.columns([1, 1])

                with col_v1:
                    st.write("### Persona Welfare Polar Plot")
                    categories = [v.name for v in last_round.values()]
                    values = [v.subjective_welfare for v in last_round.values()]

                    fig_radar = go.Figure()
                    fig_radar.add_trace(
                        go.Scatterpolar(
                            r=values,
                            theta=categories,
                            fill="toself",
                            name="Subjective Welfare ($M)",
                        )
                    )
                    fig_radar.update_layout(
                        polar={"radialaxis": {"visible": True}},
                        showlegend=False,
                        template="plotly_white",
                    )
                    st.plotly_chart(fig_radar, use_container_width=True)

                with col_v2:
                    st.write("### Auditor Trail (Final Round)")
                    for _pid, v in last_round.items():
                        with st.expander(f"**{v.name}**"):
                            st.write(f"**Sentiment:** {v.qualitative_feedback}")
                            if v.key_concerns:
                                st.write("**Key Concerns:**")
                                for c in v.key_concerns:
                                    st.write(f"- {c}")
                            else:
                                st.write("✅ No critical concerns identified.")

                st.info(
                    "The Delphi Protocol forces personas to adjust their subjective weightings towards the collective mean. "
                    "The 'Radar Plot' shows the final perceived value of the policy across different ideological axes."
                )

if "interop" in tab_map:
    # TAB 6: INTEROPERABILITY
    with tab_map["interop"]:
        st.subheader("🔄 HTA Interoperability & Data Export")
        st.write(
            "Export model results in standardized formats for Health Technology Assessment (HTA) dossiers or cross-platform integration."
        )

        if not HTA_EXPORT_AVAILABLE:
            st.info(
                "HTA export is unavailable in this deployment because the exporter module is not part "
                "of the current shipped code surface."
            )
        elif "main_result" not in st.session_state:
            st.warning(
                "Please run an evaluation in the 'Primary Evaluation' tab first to export data."
            )
        else:
            res = st.session_state["main_result"]
            params = st.session_state["main_params"]

            c_exp1, c_exp2 = st.columns(2)

            with c_exp1:
                st.write("### Standardized JSON Dossier")
                st.caption("Machine-readable format for auditable replication.")

                dossier_path = "hta_dossier.json"
                HTAExporter.to_json_dossier(res, params, dossier_path)

                with open(dossier_path, "rb") as f:
                    st.download_button(
                        label="📥 Download JSON Dossier",
                        data=f,
                        file_name=f"GINSIM_HTA_{res.policy_name}_{res.jurisdiction}.json",
                        mime="application/json",
                    )

            with c_exp2:
                st.write("### Excel Submission Template")
                st.caption("Multi-sheet workbook for jurisdictional HTA committees.")

                excel_path = "hta_submission.xlsx"
                HTAExporter.to_excel_template([res], excel_path)

                with open(excel_path, "rb") as f:
                    st.download_button(
                        label="📥 Download Excel Template",
                        data=f,
                        file_name=f"GINSIM_HTA_Submission_{res.jurisdiction}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )

            st.divider()
            st.write("#### Schema Preview")
            with st.expander("View Outcome Schema (v1.0.0)"):
                preview = {
                    "metadata": ["timestamp", "jurisdiction", "engine"],
                    "inputs": ["adverse_selection_elasticity", "deterrence_elasticity", "..."],
                    "outcomes": {
                        "utilitarian_welfare": "float",
                        "components": ["consumer_surplus", "producer_surplus", "..."],
                        "behavioral": ["testing_uptake", "compliance_rate"],
                    },
                }
                st.json(preview)

if "evidence" in tab_map:
    with tab_map["evidence"]:
        st.subheader("🧬 Diamond-Standard Traceability")
        st.caption("Temporal Evolution Engine v1.0 • 10-Year Market Drift Active")

render_footer("Temporal Logic Integrated")
