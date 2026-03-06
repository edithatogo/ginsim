#!/usr/bin/env python3
"""
Genetic Discrimination Policy Dashboard

Interactive exploration of genetic discrimination policy impacts.
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Genetic Discrimination Policy Dashboard",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Title and header
st.title("🧬 Genetic Discrimination Policy Dashboard")
st.markdown("""
Interactive exploration of policy impacts on genetic testing uptake, insurance markets, and social welfare.
""")

# Sidebar for parameter adjustment
st.sidebar.header("⚙️ Model Parameters")

# Policy selection
policy = st.sidebar.selectbox(
    "Policy Regime",
    ["Status Quo", "Moratorium", "Statutory Ban"],
    help="Select the policy regime to evaluate",
)

# Parameter sliders
baseline_uptake = st.sidebar.slider(
    "Baseline Testing Uptake",
    min_value=0.3,
    max_value=0.7,
    value=0.52,
    step=0.01,
    help="Baseline probability of genetic testing",
)

deterrence_elasticity = st.sidebar.slider(
    "Deterrence Elasticity",
    min_value=0.0,
    max_value=0.5,
    value=0.18,
    step=0.01,
    help="Elasticity of testing with respect to perceived penalty",
)

moratorium_effect = st.sidebar.slider(
    "Moratorium Effect",
    min_value=0.0,
    max_value=0.3,
    value=0.15,
    step=0.01,
    help="Additional uptake from moratorium policy",
)


# Compute results based on policy
def compute_policy_impact(policy, baseline, deterrence, moratorium):
    """Compute policy impact on testing uptake."""
    if policy == "Status Quo":
        uptake = baseline
        effect = 0.0
    elif policy == "Moratorium":
        uptake = baseline + moratorium
        effect = moratorium
    else:  # Statutory Ban
        uptake = baseline + moratorium * 1.5
        effect = moratorium * 1.5

    return min(uptake, 0.95), effect


# Calculate results
uptake, effect = compute_policy_impact(
    policy,
    baseline_uptake,
    deterrence_elasticity,
    moratorium_effect,
)

# Display results in tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Results", "📈 Charts", "📋 Comparison", "📖 Documentation"])

with tab1:
    st.header("Policy Impact Results")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Testing Uptake",
            value=f"{uptake:.1%}",
            delta=f"+{effect:.1%} vs Status Quo",
        )

    with col2:
        st.metric(
            label="Perceived Penalty",
            value=f"{(1 - uptake) * 100:.0f}%",
            delta="-15% vs Status Quo" if policy != "Status Quo" else "Baseline",
        )

    with col3:
        st.metric(
            label="Welfare Impact",
            value=f"${effect * 1000000:.0f}K",
            delta="Positive" if effect > 0 else "Neutral",
        )

    st.divider()

    # Detailed results table
    st.subheader("Detailed Results")
    results_df = pd.DataFrame(
        {
            "Metric": ["Testing Uptake", "Deterrence Rate", "Welfare Impact"],
            "Value": [
                f"{uptake:.1%}",
                f"{(1 - uptake) * 100:.1f}%",
                f"${effect * 1000000:,.0f}",
            ],
            "Change vs Status Quo": [
                f"+{effect:.1%}",
                f"-{effect:.1%}",
                f"${effect * 1000000:,.0f}",
            ],
        }
    )
    st.table(results_df)

with tab2:
    st.header("Visualizations")

    # Policy comparison chart
    st.subheader("Testing Uptake by Policy")

    policies = ["Status Quo", "Moratorium", "Statutory Ban"]
    uptakes = [
        baseline_uptake,
        min(baseline_uptake + moratorium_effect, 0.95),
        min(baseline_uptake + moratorium_effect * 1.5, 0.95),
    ]

    fig = go.Figure(
        data=[
            go.Bar(
                x=policies,
                y=uptakes,
                marker_color=["#0072B2", "#009E73", "#D55E00"],
                text=[f"{u:.1%}" for u in uptakes],
                textposition="outside",
            ),
        ]
    )

    fig.update_layout(
        title="Testing Uptake by Policy Regime",
        xaxis_title="Policy",
        yaxis_title="Testing Uptake",
        yaxis=dict(tickformat=".0%"),
        showlegend=False,
        width=700,
        height=500,
    )

    st.plotly_chart(fig, use_container_width=False, width=700)

    # Sensitivity analysis
    st.subheader("Sensitivity Analysis")

    elasticity_range = np.linspace(0.0, 0.5, 50)
    uptake_sensitivity = [
        min(baseline_uptake + moratorium_effect * (1 + 0.5 * e / deterrence_elasticity), 0.95)
        for e in elasticity_range
    ]

    fig2 = go.Figure()
    fig2.add_trace(
        go.Scatter(
            x=elasticity_range,
            y=uptake_sensitivity,
            mode="lines",
            line=dict(color="#0072B2", width=3),
        )
    )

    fig2.update_layout(
        title="Sensitivity to Deterrence Elasticity",
        xaxis_title="Deterrence Elasticity",
        yaxis_title="Testing Uptake",
        yaxis=dict(tickformat=".0%"),
        width=700,
        height=500,
    )

    st.plotly_chart(fig2, use_container_width=False, width=700)

with tab3:
    st.header("Policy Comparison")

    # Side-by-side comparison
    comparison_data = {
        "Policy": ["Status Quo", "Moratorium", "Statutory Ban"],
        "Testing Uptake": [
            f"{baseline_uptake:.1%}",
            f"{min(baseline_uptake + moratorium_effect, 0.95):.1%}",
            f"{min(baseline_uptake + moratorium_effect * 1.5, 0.95):.1%}",
        ],
        "Change": ["—", f"+{moratorium_effect:.1%}", f"+{moratorium_effect * 1.5:.1%}"],
        "Information Use": ["Full", "Restricted", "None"],
        "Premium Differentiation": ["Yes", "Limited", "None"],
    }

    comparison_df = pd.DataFrame(comparison_data)
    st.table(comparison_df)

    # Download button (fixed for pandas compatibility)
    csv = comparison_df.to_csv(index=False, encoding="utf-8")
    st.download_button(
        label="📥 Download Comparison (CSV)",
        data=csv,
        file_name="policy_comparison.csv",
        mime="text/csv",
        help="Download policy comparison data as CSV",
    )

with tab4:
    st.header("Documentation")

    st.markdown("""
    ## Model Overview
    
    This dashboard implements a game-theoretic model of genetic discrimination in life insurance markets.
    
    ### Modules
    
    - **Module A**: Behavior/Deterrence - Testing participation decisions
    - **Module C**: Insurance Equilibrium - Premium setting under asymmetric information
    - **Module D**: Proxy Substitution - Insurer response to information constraints
    - **Module E**: Pass-Through - Market structure effects
    - **Module F**: Data Quality - Research participation externalities
    - **Enforcement**: Compliance - Regulatory enforcement
    
    ### Key Parameters
    
    | Parameter | Base Value | Source |
    |-----------|------------|--------|
    | Baseline Testing Uptake | 0.52 | Ettema et al. (2021) |
    | Deterrence Elasticity | 0.18 | McGuire et al. (2019) |
    | Moratorium Effect | 0.15 | Taylor et al. (2021) |
    
    ### References
    
    - Ettema et al. (2021). Uptake of Genetic Testing. Genetics in Medicine.
    - McGuire et al. (2019). Perceived Genetic Discrimination. AJHG.
    - Taylor et al. (2021). Genetic Discrimination in Australia. JLM.
    - Hersch & Viscusi (2019). Genetic Information and Insurance Markets. Geneva Risk.
    
    ### About
    
    Developed by Dylan A. Mordaunt  
    Victoria University of Wellington  
    School of Economics and Finance
    
    **License:** MIT License
    """)

# Footer
st.divider()
st.caption("""
Dashboard v1.0 | Model v0.2.0 | Last updated: 2026-03-03
""")
