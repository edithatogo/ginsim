#!/usr/bin/env python3
"""
Comparative Delta View Page

Side-by-side policy comparison with Narrative Fairness Audit.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd
import streamlit as st

# Import from core model
from src.model.fairness import audit_policy_fairness  # New import
from src.model.pipeline import evaluate_single_policy
from src.model.scenario_analysis import evaluate_scenario, load_scenarios

# Page configuration
st.set_page_config(
    page_title="Policy Comparison & Fairness Audit",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Title
st.title("⚖️ Policy Comparison & Fairness Audit")
st.markdown("""
**How do policies compare against the baseline?**
This page evaluates the 'Fairness' of each policy shift using established ethical frameworks.
""")

# Sidebar config (reused from previous version)
st.sidebar.header("⚙️ Comparison Settings")
SCENARIOS_CONFIG = Path(__file__).parent.parent.parent / "configs" / "scenarios.yaml"


@st.cache_data
def load_scenarios_cached():
    return load_scenarios(SCENARIOS_CONFIG)


scenarios = load_scenarios_cached()

baseline_key = st.sidebar.selectbox("Select Baseline", list(scenarios.keys()), index=0)
available_policies = [k for k in scenarios if k != baseline_key]
selected_policies = st.sidebar.multiselect(
    "Compare Against:", available_policies, default=available_policies[:2]
)

# Run Analysis
if st.sidebar.button("⚖️ Audit Policies", type="primary"):
    with st.spinner("Auditing for fairness and impact..."):

        def model_func(params, policy):
            return evaluate_single_policy(params, policy)

        # Base result
        b_res = evaluate_scenario(baseline_key, scenarios[baseline_key], model_func)

        results = []
        for pk in selected_policies:
            r = evaluate_scenario(pk, scenarios[pk], model_func)

            # Run Fairness Audit
            u_delta = r.testing_uptake - b_res.testing_uptake
            w_delta = r.welfare_impact - b_res.welfare_impact
            p_delta = (
                r.insurance_premiums["premium_high"] - b_res.insurance_premiums["premium_high"]
            )

            fairness = audit_policy_fairness(u_delta, w_delta, p_delta)

            results.append(
                {
                    "Policy": scenarios[pk].get("name", pk),
                    "Uptake Delta": f"{u_delta:+.1%}",
                    "Benefit Delta": f"${w_delta:+,.0f}",
                    "Ethical Category": fairness["ethical_category"],
                    "Fairness Rationale": fairness["narrative_rationale"],
                }
            )
        st.session_state["fairness_results"] = results

# Display Audit Table
if "fairness_results" in st.session_state:
    st.subheader("🏁 The Fairness Verdict")
    st.table(pd.DataFrame(st.session_state["fairness_results"]))

    st.info("""
    **Understanding Ethical Categories:**
    - **Rawlsian Equity:** Prioritizes outcomes for the most vulnerable (high genetic risk).
    - **Utilitarian Efficiency:** Prioritizes the greatest net benefit for the largest number of people.
    - **Precautionary Protection:** Prioritizes information safety even at a minor cost to market efficiency.
    """)

st.divider()
st.caption("Developed by Authors' analysis • 2026.03")
