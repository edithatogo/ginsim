#!/usr/bin/env python3
"""
Genetic Discrimination Policy Dashboard

Interactive exploration of genetic discrimination policy impacts.
Uses core model from src/model/ for all computations.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# =============================================================================
# Visual Design System (Single Source of Truth for Dashboard Styling)
# =============================================================================
STYLE = {
    "colors": {
        "status_quo": "#0072B2",  # Blue
        "moratorium": "#009E73",  # Green
        "statutory_ban": "#D55E00",  # Vermillion
        "neutral": "#999999",  # Grey
        "background": "#F0F2F6",
    },
    "chart_defaults": {
        "template": "plotly_white",
        "width": 700,
        "height": 500,
    },
}


def get_policy_color(policy_name: str) -> str:
    """Map policy name to standard design system color."""
    name = policy_name.lower().replace(" ", "_")
    if "status_quo" in name:
        return STYLE["colors"]["status_quo"]
    if "moratorium" in name:
        return STYLE["colors"]["moratorium"]
    if "ban" in name:
        return STYLE["colors"]["statutory_ban"]
    return STYLE["colors"]["neutral"]


# =============================================================================
# Core Model Integration
# =============================================================================
from src.model.module_a_behavior import get_standard_policies
from src.model.parameters import ModelParameters
from src.model.pipeline import evaluate_single_policy

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

**Uses core JAX-accelerated model for all computations.**
""")

# Sidebar for parameter adjustment
st.sidebar.header("⚙️ Model Parameters")

# Jurisdiction selection
jurisdiction = st.sidebar.selectbox(
    "Jurisdiction",
    ["Australia", "New Zealand"],
    help="Select jurisdiction for calibration",
)

# Load standard policies
STANDARD_POLICIES = get_standard_policies()

# Policy selection
policy_display_names = {
    "Status Quo": "status_quo",
    "Moratorium": "moratorium",
    "Statutory Ban": "statutory_ban",
}
policy_label = st.sidebar.selectbox(
    "Policy Regime",
    list(policy_display_names.keys()),
    help="Select the policy regime to evaluate",
)
selected_policy_id = policy_display_names[policy_label]
selected_policy = STANDARD_POLICIES[selected_policy_id]

# Parameter sliders with model defaults
params_default = ModelParameters()

baseline_uptake = st.sidebar.slider(
    "Baseline Testing Uptake",
    min_value=0.1,
    max_value=0.9,
    value=float(params_default.baseline_testing_uptake),
    step=0.01,
    help="Baseline probability of genetic testing",
)

deterrence_elasticity = st.sidebar.slider(
    "Deterrence Elasticity",
    min_value=0.0,
    max_value=1.0,
    value=float(params_default.deterrence_elasticity),
    step=0.01,
    help="Elasticity of testing with respect to perceived penalty",
)

moratorium_effect = st.sidebar.slider(
    "Moratorium Effect",
    min_value=0.0,
    max_value=0.5,
    value=float(params_default.moratorium_effect),
    step=0.01,
    help="Additional uptake from moratorium policy",
)


# Cache model evaluation
@st.cache_data
def evaluate_model_cached(_params, policy_id):
    """Cached policy evaluation using core model pipeline."""
    policy = STANDARD_POLICIES[policy_id]

    # Run core pipeline
    result = evaluate_single_policy(_params, policy)

    return result


# Calculate results
if st.sidebar.button("🔬 Run Model", type="primary"):
    with st.spinner("Running core model (JAX-accelerated)..."):
        params_obj = ModelParameters(
            baseline_testing_uptake=baseline_uptake,
            deterrence_elasticity=deterrence_elasticity,
            moratorium_effect=moratorium_effect,
        )

        result = evaluate_model_cached(params_obj, selected_policy_id)
        st.session_state["result"] = result
        st.session_state["policy_label"] = policy_label
        st.session_state["params_dict"] = {
            "baseline_testing_uptake": baseline_uptake,
            "deterrence_elasticity": deterrence_elasticity,
            "moratorium_effect": moratorium_effect,
        }
        st.success("Model evaluation complete!")

# Display results in tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Results", "📈 Charts", "📋 Comparison", "📖 Documentation"])

with tab1:
    st.header(f"Results: {policy_label}")

    if "result" in st.session_state:
        res = st.session_state["result"]

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                label="Testing Uptake",
                value=f"{float(res.testing_uptake):.1%}",
            )

        with col2:
            st.metric(
                label="Welfare Impact",
                value=f"{float(res.welfare_impact):.2f}",
                help="Net Welfare (Testing Benefits + Consumer Surplus - Compliance Costs)",
            )

        with col3:
            st.metric(
                label="Compliance Rate",
                value=f"{float(res.compliance_rate):.1%}",
                help="Insurer compliance with the selected policy",
            )

        st.divider()

        # Detailed metrics
        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("Insurance Metrics")
            st.write(f"**Average Premium:** {float(res.insurance_premiums['avg_premium']):.3f}")
            st.write(f"**Uninsured Rate:** {float(res.insurance_premiums['uninsured_rate']):.1%}")
            st.write(
                f"**Premium High Risk:** {float(res.insurance_premiums['premium_high_risk']):.3f}"
            )
            st.write(
                f"**Premium Low Risk:** {float(res.insurance_premiums['premium_low_risk']):.3f}"
            )
            st.write(f"**Risk Rating:** {float(res.insurance_premiums['risk_rating']):.3f}")

        with col_b:
            st.subheader("Societal Metrics")
            st.write(f"**Research Participation:** {float(res.research_participation):.1%}")
            st.write(
                f"**Testing Benefit (QALYs):** {float(res.all_metrics['welfare']['testing_benefit']):.2f}"
            )
            st.write(
                f"**Consumer Surplus:** {float(res.all_metrics['welfare']['consumer_surplus']):.2f}"
            )
            st.write(
                f"**Compliance Cost:** {float(res.all_metrics['welfare']['compliance_cost']):.2f}"
            )
    else:
        st.info("👈 Adjust parameters and click 'Run Model' to see results.")

with tab2:
    st.header("Visualizations")

    if "result" in st.session_state:
        # 1. Multi-Policy Comparison Bar Chart
        st.subheader("Policy Comparison: Testing Uptake")

        policy_ids = ["status_quo", "moratorium", "statutory_ban"]
        policy_names = ["Status Quo", "Moratorium", "Statutory Ban"]

        uptakes = []
        current_params = ModelParameters(**st.session_state["params_dict"])
        for pid in policy_ids:
            r = evaluate_model_cached(current_params, pid)
            uptakes.append(float(r.testing_uptake))

        fig = go.Figure(
            data=[
                go.Bar(
                    x=policy_names,
                    y=uptakes,
                    marker_color=[get_policy_color(n) for n in policy_names],
                    text=[f"{u:.1%}" for u in uptakes],
                    textposition="outside",
                ),
            ]
        )

        fig.update_layout(
            template=STYLE["chart_defaults"]["template"],
            yaxis=dict(title="Testing Uptake", tickformat=".0%", range=[0, 1]),
            height=400,
        )
        st.plotly_chart(fig, use_container_width=True)

        # 2. Sensitivity Line Chart
        st.subheader("One-Way Sensitivity: Deterrence Elasticity")

        elasticity_range = np.linspace(0.0, 1.0, 20)
        sens_uptakes = []

        for e in elasticity_range:
            p_dict = st.session_state["params_dict"].copy()
            p_dict["deterrence_elasticity"] = float(e)
            p_obj = ModelParameters(**p_dict)
            r = evaluate_model_cached(p_obj, selected_policy_id)
            sens_uptakes.append(float(r.testing_uptake))

        fig2 = go.Figure()
        fig2.add_trace(
            go.Scatter(
                x=elasticity_range,
                y=sens_uptakes,
                mode="lines+markers",
                line=dict(color=get_policy_color(policy_label), width=3),
                name=policy_label,
            )
        )

        fig2.update_layout(
            template=STYLE["chart_defaults"]["template"],
            xaxis_title="Deterrence Elasticity",
            yaxis=dict(title="Testing Uptake", tickformat=".0%"),
            height=400,
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("👈 Run the model to enable visualizations.")

with tab3:
    st.header("Comparative Analysis")

    if "result" in st.session_state:
        # Table of all policies
        policy_data = []
        current_params = ModelParameters(**st.session_state["params_dict"])
        for pid in ["status_quo", "moratorium", "statutory_ban"]:
            r = evaluate_model_cached(current_params, pid)
            policy_data.append(
                {
                    "Policy": pid.replace("_", " ").title(),
                    "Testing Uptake": f"{float(r.testing_uptake):.1%}",
                    "Avg Premium": f"{float(r.insurance_premiums['avg_premium']):.3f}",
                    "Compliance": f"{float(r.compliance_rate):.1%}",
                    "Net Welfare": f"{float(r.welfare_impact):.2f}",
                }
            )

        df = pd.DataFrame(policy_data)
        st.table(df)

        # Navigation to deeper analysis
        st.success(
            "For interaction effects and Sobol analysis, visit the [Sensitivity Analysis](/2_Sensitivity) page."
        )
    else:
        st.info("👈 Run the model to see policy comparisons.")

with tab4:
    st.header("Scientific Documentation")

    st.markdown(
        f"""
    ## Single Source of Truth
    This dashboard is linked directly to the core JAX-accelerated model. 
    
    **Backend:** JAX / XLA (Optimized)
    
    ### Jurisdictional Context: {jurisdiction}
    The model is calibrated using the **Australia Evidence Register** (`AU_behav_001`, `AU_ins_003`).
    
    ### Visual Legend
    - <font color='{STYLE["colors"]["status_quo"]}'>■</font> **Status Quo**: No genetic restrictions.
    - <font color='{STYLE["colors"]["moratorium"]}'>■</font> **Moratorium**: Voluntary industry agreement (e.g., FSC 2019).
    - <font color='{STYLE["colors"]["statutory_ban"]}'>■</font> **Statutory Ban**: Legislated prohibition (e.g., Proposed 2025 Bill).
    
    ### Reference Parameters
    - **Baseline Uptake (0.52):** Ettema et al. (2021)
    - **Deterrence Elasticity (0.18):** McGuire et al. (2019)
    - **Moratorium Effect (0.15):** Taylor et al. (2021)
    """,
        unsafe_allow_html=True,
    )

# Navigation Footer
st.divider()
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    if st.button("🎮 Go to Game Diagrams"):
        st.switch_page("pages/1_Game_Diagrams.py")
with col_f2:
    if st.button("📊 Go to Sensitivity Analysis"):
        st.switch_page("pages/2_Sensitivity.py")
with col_f3:
    if st.button("🎯 Go to Scenario Analysis"):
        st.switch_page("pages/3_Scenarios.py")
