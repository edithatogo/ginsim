#!/usr/bin/env python3
"""
Scenario Analysis Page

Compare policy outcomes across predefined scenarios and custom configurations.
Features:
- Pre-defined scenarios (AU 2025 Ban, FSC Moratorium, international benchmarks)
- Australian Policy Designer (Sandbox)
- Comparative "Delta" view
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from streamlit_app.dashboard_helpers import evaluate_sandbox_policy
from src.model.pipeline import evaluate_single_policy

# Import from core model
from src.model.scenario_analysis import (
    compare_scenarios,
    format_comparison_table,
    load_scenarios,
)

# Page configuration
st.set_page_config(
    page_title="Scenario Analysis",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Title
st.title("🎯 Scenario Analysis & Policy Sandbox")
st.markdown("""
**Compare policy outcomes across different regimes and jurisdictions.**

- **Pre-defined Scenarios:** Australia 2025 Ban, FSC Moratorium, international benchmarks
- **Policy Sandbox:** Design custom scenarios with adjustable parameters
- **Delta View:** See comparative impacts relative to baseline
""")
st.info(
    """
**What this page answers**
- How benchmark scenarios compare against a chosen baseline on uptake, welfare, and compliance.
- Which scenario assumptions are tied to a real policy regime versus a sandbox policy design.

**Status**
- Pre-defined scenarios now bind a canonical policy (`status_quo`, `moratorium`, or `ban`) plus scenario-specific parameter overrides.
- The Australian policy designer below is exploratory and should not be read as a calibrated benchmark regime.
"""
)

# Sidebar for scenario selection
st.sidebar.header("⚙️ Scenario Configuration")

# Load scenarios
SCENARIOS_CONFIG = Path(__file__).parent.parent.parent / "configs" / "scenarios.yaml"


@st.cache_data
def load_scenarios_cached():
    """Load scenarios with caching."""
    try:
        return load_scenarios(SCENARIOS_CONFIG)
    except FileNotFoundError:
        st.error(f"Scenario config not found: {SCENARIOS_CONFIG}")
        return {}


scenarios = load_scenarios_cached()

# Scenario selector
scenario_labels = {
    name: f"{config.get('name', name)} ({config.get('jurisdiction', 'Unknown')})"
    for name, config in scenarios.items()
}
scenario_label_to_key = {label: key for key, label in scenario_labels.items()}

selected_scenario_label = st.sidebar.selectbox(
    "Select Scenario",
    list(scenario_label_to_key.keys()),
    help="Choose a predefined policy scenario",
)
selected_scenario_key = scenario_label_to_key[selected_scenario_label]

# Display scenario description
if selected_scenario_key in scenarios:
    scenario_config = scenarios[selected_scenario_key]
    st.sidebar.info(f"**Description:** {scenario_config.get('description', 'No description')}")
    if scenario_config.get("policy_id"):
        st.sidebar.caption(f"Canonical policy: `{scenario_config['policy_id']}`")
    if scenario_config.get("note"):
        st.sidebar.caption(f"Scenario note: {scenario_config['note']}")

# Baseline selector
st.sidebar.subheader("Comparison Settings")
baseline_options = {
    "au_status_quo": "Australia Status Quo",
    "nz_current": "New Zealand Current",
}

baseline_label_to_key = {label: key for key, label in baseline_options.items()}
baseline_label = st.sidebar.selectbox(
    "Baseline for Comparison",
    list(baseline_label_to_key.keys()),
    help="Select baseline scenario for delta calculations",
)
baseline_key = baseline_label_to_key[baseline_label]

# Run button
if st.sidebar.button("🔬 Run Scenario Comparison", type="primary"):
    with st.spinner("Running scenario analysis..."):
        # Get model function
        def model_func(params, policy):
            return evaluate_single_policy(params, policy)

        # Run comparison
        comparison = compare_scenarios(scenarios, model_func, baseline_name=baseline_key)
        st.session_state["scenario_comparison"] = comparison
        st.success("Scenario comparison complete!")
else:
    comparison = None

# Display results
if "scenario_comparison" in st.session_state:
    comparison = st.session_state["scenario_comparison"]

    st.divider()
    st.subheader(
        f"📊 Scenario Comparison (Baseline: {baseline_options.get(baseline_key, baseline_key)})",
    )

    # Create comparison dataframe
    data = []
    for result in comparison.scenarios:
        delta = comparison.delta_from_baseline.get(result.scenario_name, {})
        data.append(
            {
                "Scenario": result.scenario_name,
                "Jurisdiction": result.jurisdiction,
                "Testing Uptake": f"{result.testing_uptake:.1%}",
                "Δ Uptake": f"{delta.get('testing_uptake_delta', 0):+.1%}" if delta else "—",
                "Welfare Impact": f"${result.welfare_impact:,.0f}",
                "Δ Welfare": f"${delta.get('welfare_delta', 0):+,.0f}" if delta else "—",
                "Compliance": f"{result.compliance_rate:.1%}",
            },
        )

    df = pd.DataFrame(data)
    st.dataframe(df, width="stretch", hide_index=True)
    st.caption(
        "Interpretation: benchmark scenarios differ through both model parameters and the canonical policy regime shown in the scenario config."
    )

    # Visualization: Testing Uptake Comparison
    st.divider()
    st.subheader("📈 Testing Uptake by Scenario")

    fig = go.Figure()

    scenario_names = [r.scenario_name for r in comparison.scenarios]
    uptakes = [r.testing_uptake for r in comparison.scenarios]
    colors = []

    for r in comparison.scenarios:
        if r.scenario_name == baseline_key:
            colors.append("#95a5a6")  # Gray for baseline
        else:
            delta = comparison.delta_from_baseline.get(r.scenario_name, {}).get(
                "testing_uptake_delta",
                0,
            )
            if delta > 0:
                colors.append("#2ecc71")  # Green for positive
            else:
                colors.append("#e74c3c")  # Red for negative

    fig.add_trace(
        go.Bar(
            x=scenario_names,
            y=uptakes,
            marker_color=colors,
            text=[f"{u:.1%}" for u in uptakes],
            textposition="outside",
        ),
    )

    fig.update_layout(
        title="Testing Uptake Across Policy Scenarios",
        xaxis_title="Scenario",
        yaxis_title="Testing Uptake",
        yaxis=dict(tickformat=".0%"),
        height=500,
        showlegend=False,
    )

    st.plotly_chart(fig, width="stretch")

    # Welfare Impact Comparison
    st.divider()
    st.subheader("💰 Welfare Impact by Scenario")

    fig2 = go.Figure()

    welfares = [r.welfare_impact for r in comparison.scenarios]

    fig2.add_trace(
        go.Bar(
            x=scenario_names,
            y=welfares,
            marker_color=[
                "#3498db"
                if r.scenario_name == baseline_key
                else "#27ae60"
                if r.welfare_impact > 0
                else "#c0392b"
                for r in comparison.scenarios
            ],
            text=[f"${w:,.0f}" for w in welfares],
            textposition="outside",
        ),
    )

    fig2.update_layout(
        title="Welfare Impact Across Policy Scenarios",
        xaxis_title="Scenario",
        yaxis_title="Welfare Impact ($)",
        yaxis=dict(tickformat="$,.0f"),
        height=500,
        showlegend=False,
    )

    st.plotly_chart(fig2, width="stretch")

    # Detailed results expander
    with st.expander("📋 View Detailed Results"):
        st.markdown(format_comparison_table(comparison))

# Australian Policy Sandbox
st.divider()
st.subheader("🇦🇺 Australian Policy Designer (Sandbox)")
st.markdown("""
**Design custom policy scenarios for Australia.** Adjust caps, enforcement, and penalties to see impacts.
""")
st.warning(
    "Exploratory surface: this sandbox is useful for intuition and design-space exploration, but it is not the same as a validated benchmark policy scenario."
)

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Policy Parameters")

    sandbox_uptake = st.slider(
        "Baseline Testing Uptake",
        min_value=0.3,
        max_value=0.7,
        value=0.52,
        step=0.01,
        help="Baseline probability of genetic testing",
    )

    sandbox_deterrence = st.slider(
        "Deterrence Elasticity",
        min_value=0.0,
        max_value=0.3,
        value=0.12,
        step=0.01,
        help="Sensitivity of testing to discrimination risk",
    )

    sandbox_enforcement = st.slider(
        "Enforcement Strength",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.05,
        help="Probability of detecting violations",
    )

    sandbox_penalty = st.slider(
        "Penalty Rate",
        min_value=0.0,
        max_value=1.0,
        value=0.6,
        step=0.05,
        help="Severity of penalties for violations",
    )

with col2:
    st.markdown("#### Expected Outcomes")

    sandbox_result = evaluate_sandbox_policy(
        baseline_testing_uptake=sandbox_uptake,
        deterrence_elasticity=sandbox_deterrence,
        enforcement_effectiveness=sandbox_enforcement,
        penalty_rate=sandbox_penalty,
    )

    st.metric("Estimated Testing Uptake", f"{float(sandbox_result.testing_uptake):.1%}")
    st.metric("Estimated Welfare Impact", f"${float(sandbox_result.welfare_impact):,.0f}")
    st.metric("Policy Effectiveness Score", f"{float(sandbox_result.compliance_rate) * 100:.0f}/100")

# Download button
if comparison:
    st.divider()
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download Comparison (CSV)",
        data=csv,
        file_name="scenario_comparison.csv",
        mime="text/csv",
        help="Download scenario comparison data",
    )

# Footer
st.divider()
st.caption("""
Scenario Analysis v1.0 | Last updated: 2026-03-05 | Data source: Authors' analysis
""")
