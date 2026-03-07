#!/usr/bin/env python3
"""
Comparative Delta View Page

Side-by-side policy comparison with automatic Net Welfare Gain calculation.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Import from core model
from src.model.delta_view import (
    comparative_delta_analysis,
    format_delta_table,
)
from src.model.pipeline import evaluate_single_policy
from src.model.scenario_analysis import evaluate_scenario, load_scenarios
from streamlit_app.dashboard_helpers import format_positive_share

# Page configuration
st.set_page_config(
    page_title="Comparative Delta View",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Title
st.title("📊 Comparative Delta View")
st.markdown("""
**Side-by-side policy comparison with automatic Net Welfare Gain calculations.**

Compare multiple policies against a baseline and see:
- Testing uptake deltas
- Long-run net welfare deltas
- QALY differences
- Compliance rate changes
- **Net Welfare Gain** (NPV adjusted, implementation/admin costs deducted)
- Cost-Benefit ratios
""")
st.info(
    """
**What this page answers**
- How far each selected scenario moves relative to the baseline on uptake, welfare, QALYs, and compliance.
- Which policy looks strongest once simple implementation and administration costs are layered on.

**Status**
- This page compares pre-defined scenarios that now bind canonical policy regimes through the scenario engine.
- The NPV cost settings are user-specified decision inputs, so treat them as policy-analysis assumptions rather than observed costs.
"""
)

# Sidebar for configuration
st.sidebar.header("⚙️ Comparison Settings")

# Load scenarios
SCENARIOS_CONFIG = Path(__file__).parent.parent.parent / "configs" / "scenarios.yaml"


@st.cache_data
def load_scenarios_cached():
    """Load scenarios with caching."""
    try:
        return load_scenarios(SCENARIOS_CONFIG)
    except FileNotFoundError:
        return {}


scenarios = load_scenarios_cached()

# Baseline selector
st.sidebar.subheader("Baseline Policy")
baseline_options = {
    "au_status_quo": "Australia Status Quo",
    "au_fsc_moratorium": "FSC Moratorium",
    "nz_current": "New Zealand Current",
}

baseline_label_to_key = {label: key for key, label in baseline_options.items()}
baseline_label = st.sidebar.selectbox(
    "Select Baseline",
    list(baseline_label_to_key.keys()),
    help="Baseline policy for delta calculations",
)
baseline_key = baseline_label_to_key[baseline_label]

# Comparison policies selector
st.sidebar.subheader("Policies to Compare")
available_policies = [k for k in scenarios if k != baseline_key]

selected_policies = st.sidebar.multiselect(
    "Select comparison policies",
    available_policies,
    default=available_policies[:3] if len(available_policies) > 3 else available_policies,
    help="Policies to compare against baseline",
)
st.sidebar.caption(
    "Use benchmark scenarios for policy comparison; sandbox-like scenarios are better treated as exploratory."
)

# Cost parameters
st.sidebar.subheader("Cost Parameters")

implementation_cost = st.sidebar.number_input(
    "Implementation Cost ($)",
    min_value=0,
    max_value=10000000,
    value=1000000,
    step=100000,
    help="One-time implementation cost",
)

administrative_cost = st.sidebar.number_input(
    "Annual Administrative Cost ($)",
    min_value=0,
    max_value=1000000,
    value=100000,
    step=50000,
    help="Ongoing annual administrative cost",
)

time_horizon = st.sidebar.slider(
    "Time Horizon (years)",
    min_value=1,
    max_value=30,
    value=10,
    step=1,
    help="Time horizon for NPV calculation",
)

discount_rate = st.sidebar.slider(
    "Discount Rate",
    min_value=0.0,
    max_value=0.1,
    value=0.03,
    step=0.005,
    help="Discount rate for NPV calculation",
)

# Run button
if st.sidebar.button("🔬 Run Comparative Analysis", type="primary"):
    with st.spinner("Running comparative analysis..."):
        # Evaluate all policies
        def model_func(params, policy):
            return evaluate_single_policy(params, policy)

        # Get baseline result
        baseline_config = scenarios.get(baseline_key, {})
        baseline_result = evaluate_scenario(baseline_key, baseline_config, model_func)

        baseline_dict = {
            "testing_uptake": baseline_result.testing_uptake,
            "welfare_impact": baseline_result.welfare_impact,
            "qalys_gained": baseline_result.qalys_gained,
            "compliance_rate": baseline_result.compliance_rate,
        }

        # Evaluate comparison policies
        policy_results = {}
        for policy_key in selected_policies:
            policy_config = scenarios.get(policy_key, {})
            result = evaluate_scenario(policy_key, policy_config, model_func)
            policy_results[policy_key] = {
                "testing_uptake": result.testing_uptake,
                "welfare_impact": result.welfare_impact,
                "qalys_gained": result.qalys_gained,
                "compliance_rate": result.compliance_rate,
            }

        # Run comparative analysis
        cost_params = {
            "implementation_cost": float(implementation_cost),
            "administrative_cost": float(administrative_cost),
            "time_horizon": float(time_horizon),
            "discount_rate": float(discount_rate),
        }

        analysis = comparative_delta_analysis(baseline_dict, policy_results, cost_params)
        st.session_state["delta_analysis"] = analysis
        st.session_state["baseline_result"] = baseline_result
        st.success("Comparative analysis complete!")
else:
    analysis = None

# Display results
if "delta_analysis" in st.session_state:
    analysis = st.session_state["delta_analysis"]
    baseline_result = st.session_state["baseline_result"]

    st.divider()
    st.subheader(
        f"📊 Delta Analysis (Baseline: {baseline_options.get(baseline_key, baseline_key)})"
    )

    # Create comparison dataframe
    data = []
    for metrics in analysis.delta_metrics:
        data.append(
            {
                "Policy": metrics.policy_name,
                "Δ Uptake": f"{metrics.testing_uptake_delta:+.1%}",
                "Δ Welfare": f"${metrics.welfare_delta:+,.0f}",
                "Δ QALYs": f"{metrics.qalys_delta:+.2f}",
                "Δ Compliance": f"{metrics.compliance_delta:+.1%}",
                "Net Welfare Gain": f"${metrics.net_welfare_gain:+,.0f}",
                "Cost-Benefit Ratio": f"{metrics.cost_benefit_ratio:.2f}",
            }
        )

    df = pd.DataFrame(data)
    st.dataframe(df, hide_index=True)
    st.caption(
        "Interpretation: positive deltas mean the comparison scenario outperforms the selected baseline on that metric. Welfare metrics are currency-denominated decision metrics; QALYs are reported separately."
    )

    # Visualization: Welfare Delta Comparison
    st.divider()
    st.subheader("💰 Long-run Net Welfare Deltas")

    fig = go.Figure()

    policy_names = [m.policy_name for m in analysis.delta_metrics]
    welfare_deltas = [m.welfare_delta for m in analysis.delta_metrics]
    colors = ["#2ecc71" if w > 0 else "#e74c3c" for w in welfare_deltas]

    fig.add_trace(
        go.Bar(
            x=policy_names,
            y=welfare_deltas,
            marker_color=colors,
            text=[f"${w:+,.0f}" for w in welfare_deltas],
            textposition="outside",
        )
    )

    fig.update_layout(
        title="Long-run Net Welfare vs Baseline",
        xaxis_title="Policy",
        yaxis_title="Long-run Net Welfare Delta ($)",
        yaxis={"tickformat": "$,.0f"},
        height=400,
        showlegend=False,
    )

    st.plotly_chart(fig, width="stretch")

    # Visualization: Net Welfare Gain
    st.divider()
    st.subheader("💵 Net Welfare Gain (NPV Adjusted)")

    fig2 = go.Figure()

    net_gains = [m.net_welfare_gain for m in analysis.delta_metrics]
    colors2 = ["#2ecc71" if g > 0 else "#e74c3c" for g in net_gains]

    fig2.add_trace(
        go.Bar(
            x=policy_names,
            y=net_gains,
            marker_color=colors2,
            text=[f"${g:+,.0f}" for g in net_gains],
            textposition="outside",
        )
    )

    fig2.update_layout(
        title="Net Welfare Gain (Implementation + Admin Costs Deducted)",
        xaxis_title="Policy",
        yaxis_title="Net Welfare Gain ($)",
        yaxis={"tickformat": "$,.0f"},
        height=400,
        showlegend=False,
    )

    st.plotly_chart(fig2, width="stretch")

    # Rankings
    st.divider()
    st.subheader("🏆 Policy Rankings")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**By Welfare Impact:**")
        for i, policy in enumerate(analysis.ranking_by_welfare, 1):
            st.write(f"{i}. {policy}")

    with col2:
        st.markdown("**By Testing Uptake:**")
        for i, policy in enumerate(analysis.ranking_by_uptake, 1):
            st.write(f"{i}. {policy}")

    # Summary insights
    st.divider()
    st.subheader("📋 Summary Insights")

    best_welfare = analysis.summary.get("best_welfare_policy", "N/A")
    best_uptake = analysis.summary.get("best_uptake_policy", "N/A")
    positive_welfare = analysis.summary.get("policies_with_positive_welfare", 0)
    total_policies = analysis.summary.get("total_policies_compared", 0)
    positive_share = format_positive_share(positive_welfare, total_policies)

    st.info(f"""
    **Key Findings:**
    - **Best policy by welfare:** {best_welfare}
    - **Best policy by uptake:** {best_uptake}
    - **Policies with positive welfare impact:** {positive_welfare}/{total_policies} ({positive_share})
    """)

    # Detailed markdown table
    with st.expander("📋 View Detailed Markdown Table"):
        st.markdown(format_delta_table(analysis))

    # Download button
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download Comparison (CSV)",
        data=csv,
        file_name="delta_comparison.csv",
        mime="text/csv",
        help="Download delta comparison data",
    )

# Documentation
st.divider()
with st.expander("📖 About Net Welfare Gain Calculation"):
    st.markdown("""
    ### Net Welfare Gain Formula

    The Net Welfare Gain is calculated as:

    ```
    Net Welfare Gain = Long-run Welfare Delta - Implementation Cost - PV(Administrative Costs)

    Where:
    - PV(Administrative Costs) = Σ [Admin Cost / (1 + r)^t] for t = 1 to time horizon
    - r = discount rate
    ```

    ### Cost-Benefit Ratio

    ```
    C/B Ratio = |Long-run Welfare Delta| / Total Costs

    Interpretation:
    - C/B > 1: Benefits exceed costs
    - C/B = 1: Break-even
    - C/B < 1: Costs exceed benefits
    ```

    ### Default Parameters

    - **Implementation Cost:** $1,000,000 (one-time)
    - **Administrative Cost:** $100,000/year
    - **Time Horizon:** 10 years
    - **Discount Rate:** 3% (standard for policy analysis)
    """)

# Footer
st.caption("""
Comparative Delta View v1.0 | Last updated: 2026-03-05
""")
