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
from src.model.module_a_behavior import get_standard_policies
from src.model.parameters import load_jurisdiction_parameters
from src.model.pipeline import evaluate_single_policy
from src.model.scenario_analysis import (
    evaluate_scenario,
    filter_scenarios_by_jurisdiction,
    get_scenario_display_name,
    load_scenarios,
)
from streamlit_app.dashboard_ui import (
    JURISDICTION_OPTIONS,
    jurisdiction_to_code,
    jurisdiction_to_config_id,
    render_current_run_summary,
    render_footer,
    render_sidebar_build_info,
)

st.set_page_config(page_title="Fairness Audit", page_icon="⚖️", layout="wide")

st.title("⚖️ Policy Fairness Audit")
st.markdown("Auditing policy reforms against the 'Separating' Status Quo baseline.")

# Controls
jurisdiction = st.sidebar.selectbox("Jurisdiction", JURISDICTION_OPTIONS)
selected_code = jurisdiction_to_code(jurisdiction)
render_sidebar_build_info()

scenarios = load_scenarios(project_root / "configs" / "scenarios.yaml")
jurisdiction_scenarios = filter_scenarios_by_jurisdiction(scenarios, selected_code)
reform_scenarios = {
    key: config
    for key, config in jurisdiction_scenarios.items()
    if str(config.get("policy_id", "")).lower() != "status_quo"
}
render_current_run_summary(
    "Audit Context",
    {
        "Jurisdiction": jurisdiction,
        "Baseline": "Status Quo",
        "Compared Policies": str(len(reform_scenarios)),
    },
)

if st.button("⚖️ Audit Policies", type="primary"):
    if not reform_scenarios:
        st.warning(
            "No reform scenarios are currently defined for this jurisdiction. "
            "Add jurisdiction-specific reform scenarios to the scenario config to enable the audit."
        )
    else:
        with st.spinner("Executing fairness audit matrix..."):

            def model_func(params, policy):
                return evaluate_single_policy(params, policy)

            params = load_jurisdiction_parameters(jurisdiction_to_config_id(jurisdiction))
            baseline_policy = get_standard_policies()["status_quo"]
            b_res = evaluate_single_policy(params, baseline_policy)

            results = []

            for pk, config in reform_scenarios.items():
                r = evaluate_scenario(pk, config, model_func)

                u_delta = float(r.testing_uptake) - float(b_res.testing_uptake)
                w_delta = float(r.welfare_impact) - float(b_res.welfare_impact)
                ew_delta = float(r.equity_weighted_welfare) - float(b_res.equity_weighted_welfare)
                p_delta = float(r.insurance_premiums["premium_high"]) - float(
                    b_res.insurance_premiums["premium_high"]
                )

                fairness = audit_policy_fairness(u_delta, w_delta, p_delta)

                results.append(
                    {
                        "Policy": get_scenario_display_name(pk, config),
                        "Uptake Delta": f"{u_delta:+.1%}",
                        "Utilitarian Delta": f"${w_delta:+,.0f}",
                        "Equity-Weighted Delta": f"${ew_delta:+,.0f}",
                        "Ethical Category": "FAIR" if fairness.is_fair else "UNFAIR",
                        "Fairness Rationale": "; ".join(fairness.reasons)
                        if fairness.reasons
                        else "Maintains equity.",
                    }
                )

            df = pd.DataFrame(results)
            st.subheader("Fairness Verdict Matrix")
            st.table(df)

render_footer("Fairness Engine Active")
