#!/usr/bin/env python3
"""
Delta View: Cross-Scenario Fairness Audit Page.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd
import streamlit as st

from src.model.fairness import audit_policy_fairness
from src.model.parameters import load_jurisdiction_parameters
from src.model.pipeline import evaluate_single_policy, get_standard_policies
from src.model.scenario_analysis import evaluate_scenario, load_scenarios

st.set_page_config(page_title="Fairness Audit", page_icon="⚖️", layout="wide")

st.title("⚖️ Policy Fairness Audit")
st.markdown("Auditing policy reforms against the 'Separating' Status Quo baseline.")

# Controls
jurisdiction = st.sidebar.selectbox("Jurisdiction", ["Australia", "New Zealand", "UK", "Canada", "US"])
baseline_key = "au_status_quo" # Standard anchor

scenarios = load_scenarios(project_root / "configs" / "scenarios.yaml")

if st.button("⚖️ Audit Policies", type="primary"):
    with st.spinner("Executing fairness audit matrix..."):
        # We use standard model function
        def model_func(params, policy):
            return evaluate_single_policy(params, policy)
        
        # Base result
        b_res = evaluate_scenario(baseline_key, scenarios[baseline_key], model_func)
        
        results = []
        selected_policies = ["au_moratorium", "au_ban"] # Focus on primary comparisons
        
        for pk in selected_policies:
            if pk not in scenarios: continue
            r = evaluate_scenario(pk, scenarios[pk], model_func)
            
            u_delta = float(r.testing_uptake) - float(b_res.testing_uptake)
            w_delta = float(r.welfare_impact) - float(b_res.welfare_impact)
            p_delta = float(r.insurance_premiums["premium_high"]) - float(b_res.insurance_premiums["premium_high"])
            
            fairness = audit_policy_fairness(u_delta, w_delta, p_delta)
            
            results.append(
                {
                    "Policy": scenarios[pk].get("name", pk),
                    "Uptake Delta": f"{u_delta:+.1%}",
                    "Benefit Delta": f"${w_delta:+,.0f}",
                    "Ethical Category": "FAIR" if fairness.is_fair else "UNFAIR",
                    "Fairness Rationale": "; ".join(fairness.reasons) if fairness.reasons else "Maintains equity.",
                }
            )
            
        df = pd.DataFrame(results)
        st.subheader("Fairness Verdict Matrix")
        st.table(df)
        
st.divider()
st.caption("Developed by Dylan A Mordaunt • 2026.03 • Fairness Engine Active")
