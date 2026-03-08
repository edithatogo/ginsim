#!/usr/bin/env python3
"""
Sensitivity Analysis Page

Comprehensive sensitivity analysis including:
- One-way sensitivity (tornado diagrams)
- Scenario Analysis
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import plotly.graph_objects as go
import streamlit as st

from src.model.module_a_behavior import get_standard_policies
from src.model.parameters import ModelParameters
from src.model.pipeline import evaluate_single_policy

# Import from core model
from src.model.sensitivity import (
    tornado_analysis,
)

# Page configuration
st.set_page_config(
    page_title="Sensitivity Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Title
st.title("📊 Sensitivity Analysis")
st.markdown(
    """
Explore how uncertainty in model parameters affects policy outcomes.
""",
)

# Parameter selection
st.sidebar.header("⚙️ Analysis Settings")

# Get default parameters
params_model = ModelParameters()
param_options = {
    "Deterrence Elasticity": "deterrence_elasticity",
    "Moratorium Effect": "moratorium_effect",
    "Adverse Selection": "adverse_selection_elasticity",
    "Baseline Loading": "baseline_loading",
}

selected_params = st.sidebar.multiselect(
    "Select parameters",
    list(param_options.keys()),
    default=list(param_options.keys())[:2],
)

range_pct = st.sidebar.slider("Variation Range", 0.1, 0.5, 0.25, 0.05)

policy_name = st.sidebar.selectbox(
    "Policy Regime",
    ["Status Quo", "Moratorium", "Ban"],
)

# Run button
if st.sidebar.button("🔬 Run Tornado Analysis", type="primary"):
    with st.spinner("Running sensitivity analysis..."):
        policies = get_standard_policies()
        policy = policies.get(policy_name.lower().replace(" ", "_"), policies["status_quo"])

        def model_func(p):
            res = evaluate_single_policy(p, policy)
            return float(res.testing_uptake)

        # Run analysis
        attr_names = [param_options[k] for k in selected_params]
        results = tornado_analysis(model_func, params_model, attr_names, variation=range_pct)
        st.session_state["tornado_results"] = results

# Display
if "tornado_results" in st.session_state:
    st.subheader("🌪️ Tornado Diagram")
    results = st.session_state["tornado_results"]

    fig = go.Figure()
    y_labels = [r.parameter_name for r in results]
    lows = [r.lower_outcome for r in results]
    highs = [r.upper_outcome for r in results]

    fig.add_trace(
        go.Bar(
            y=y_labels,
            x=[h - l for h, l in zip(highs, lows, strict=False)],
            base=lows,
            orientation="h",
            marker_color="#3498db",
        )
    )
    fig.update_layout(title="Impact on Testing Uptake", xaxis_tickformat=".1%")
    st.plotly_chart(fig, use_container_width=True)

    # Detailed Data
    with st.expander("📋 View Data Table"):
        st.table(
            [
                {
                    "Parameter": r.parameter_name,
                    "Base": f"{r.base_outcome:.1%}",
                    "Low": f"{r.lower_outcome:.1%}",
                    "High": f"{r.upper_outcome:.1%}",
                    "Index": f"{r.sensitivity_index:.4f}",
                }
                for r in results
            ]
        )

st.divider()
st.caption("Developed by Authors' analysis • 2026.03")
