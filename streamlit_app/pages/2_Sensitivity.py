#!/usr/bin/env python3
"""
Sensitivity Analysis Page

Comprehensive sensitivity analysis including:
- One-way sensitivity (tornado diagrams)
- Two-way sensitivity (heat maps)
- Global sensitivity (Sobol indices)
- Probabilistic sensitivity (CEAC)
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import jax.numpy as jnp
import plotly.graph_objects as go
import streamlit as st

from src.model.module_a_behavior import get_standard_policies
from src.model.parameters import ModelParameters
from src.model.pipeline import evaluate_single_policy

# Import from core model
from src.model.sensitivity_total import (
    sobol_sensitivity,
    tornado_sensitivity,
    twoway_sensitivity,
)

# Page configuration
st.set_page_config(
    page_title="Sensitivity Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Title
st.title("📊 Comprehensive Sensitivity Analysis")
st.markdown(
    """
**Powered by JAX/XLA acceleration**

Explore how uncertainty in model parameters affects policy outcomes
through multiple sensitivity analysis methods.
""",
)
st.info(
    """
**What this page answers**
- Which calibrated inputs move the selected policy result the most.
- Whether the result changes smoothly or sharply when assumptions move.
- Which conclusions are robust versus uncertainty-sensitive.

**Status**
- This page varies active model parameters and benchmark policy settings.
- Use it to understand sensitivity, not as direct empirical validation of any single parameter value.
"""
)

# Sidebar for analysis configuration
st.sidebar.header("⚙️ Analysis Configuration")

# Select analysis type
analysis_type = st.sidebar.selectbox(
    "Analysis Type",
    ["Tornado (One-Way)", "Heat Map (Two-Way)", "Sobol (Global)", "Run All"],
    help="Choose sensitivity analysis method",
)

# Parameter selection
st.sidebar.subheader("Parameters to Analyze")

# Get default parameters from ModelParameters to avoid hardcoded values
params_model = ModelParameters()
param_options = {
    "Baseline Testing Uptake": (
        "baseline_testing_uptake",
        float(params_model.baseline_testing_uptake),
    ),
    "Deterrence Elasticity": (
        "deterrence_elasticity",
        float(params_model.deterrence_elasticity),
    ),
    "Moratorium Effect": (
        "moratorium_effect",
        float(params_model.moratorium_effect),
    ),
    "Adverse Selection Elasticity": (
        "adverse_selection_elasticity",
        float(params_model.adverse_selection_elasticity),
    ),
    "High-Risk Demand Elasticity": (
        "demand_elasticity_high_risk",
        float(params_model.demand_elasticity_high_risk),
    ),
    "Baseline Loading": (
        "baseline_loading",
        float(params_model.baseline_loading),
    ),
}

selected_params = st.sidebar.multiselect(
    "Select parameters",
    list(param_options.keys()),
    default=list(param_options.keys())[:3],
)

# Range for sensitivity
range_pct = st.sidebar.slider(
    "Variation Range",
    min_value=0.1,
    max_value=0.5,
    value=0.25,
    step=0.05,
    help="Percentage variation for sensitivity analysis (e.g., 0.25 = ±25%)",
)

# Number of samples for Sobol
n_samples = st.sidebar.slider(
    "Monte Carlo Samples",
    min_value=100,
    max_value=2000,
    value=500,
    step=100,
    help="Number of samples for Sobol analysis (higher = more accurate but slower)",
)

# Policy selection
policy_name = st.sidebar.selectbox(
    "Policy Regime",
    ["Status Quo", "Moratorium", "Ban"],
    help="Select policy to analyze",
)


# Cache model evaluation
@st.cache_data
def run_sensitivity_cached(
    analysis_type: str,
    param_keys: tuple,
    range_pct: float,
    n_samples: int,
    policy_name: str,
) -> dict:
    """Run sensitivity analysis with caching."""
    # Get default parameters from ModelParameters to avoid hardcoded values
    params_model = ModelParameters()
    base_params_dict = {
        "baseline_testing_uptake": float(params_model.baseline_testing_uptake),
        "deterrence_elasticity": float(params_model.deterrence_elasticity),
        "moratorium_effect": float(params_model.moratorium_effect),
        "adverse_selection_elasticity": float(params_model.adverse_selection_elasticity),
        "demand_elasticity_high_risk": float(params_model.demand_elasticity_high_risk),
        "baseline_loading": float(params_model.baseline_loading),
    }

    # Convert to JAX array - simplified parameter mapping
    param_indices = []
    param_names = []
    base_values = []

    for key in param_keys:
        if key in param_options:
            attr_name, default_value = param_options[key]
            if attr_name in base_params_dict:
                param_indices.append(len(base_values))
                param_names.append(key)
                base_values.append(base_params_dict[attr_name])

    if not base_values:
        return {"error": "No valid parameters selected"}

    base_params = jnp.array(base_values)

    # Define model function
    policies = get_standard_policies()
    policy = policies.get(policy_name.lower().replace(" ", "_"), policies["status_quo"])

    def model_func(params_array):
        """Wrapper to evaluate model with JAX."""
        # Create ModelParameters with varied values
        params_dict = base_params_dict.copy()
        for i, key in enumerate(param_names):
            attr_name, _ = param_options[key]
            params_dict[attr_name] = float(params_array[i])

        try:
            eval_params = ModelParameters(**params_dict)
            result = evaluate_single_policy(eval_params, policy)
            return float(result.testing_uptake)
        except Exception as e:
            st.error(f"Model evaluation failed: {e}")
            return float("nan")

    results = {}

    if analysis_type in ["Tornado (One-Way)", "Run All"]:
        tornado = tornado_sensitivity(
            model_func,
            base_params,
            param_names,
            list(range(len(param_names))),
            range_pct=range_pct,
        )
        results["tornado"] = tornado

    if analysis_type in ["Sobol (Global)", "Run All"]:
        sobol = sobol_sensitivity(
            model_func,
            base_params,
            param_names,
            list(range(len(param_names))),
            n_samples=min(n_samples, 1000),  # Cap for caching
        )
        results["sobol"] = sobol

    if analysis_type in ["Heat Map (Two-Way)", "Run All"] and len(param_names) >= 2:
        heatmap = twoway_sensitivity(
            model_func,
            base_params,
            0,
            1,
            (base_values[0] * (1 - range_pct), base_values[0] * (1 + range_pct)),
            (base_values[1] * (1 - range_pct), base_values[1] * (1 + range_pct)),
            n_points=15,
        )
        results["heatmap"] = heatmap
        results["heatmap_params"] = (param_names[0], param_names[1])

    return results


# Run button
if st.sidebar.button("🔬 Run Sensitivity Analysis", type="primary"):
    with st.spinner("Running JAX-accelerated sensitivity analysis..."):
        results = run_sensitivity_cached(
            analysis_type,
            tuple(selected_params),
            range_pct,
            n_samples,
            policy_name,
        )
        st.session_state["sensitivity_results"] = results
        st.session_state["param_names"] = selected_params
        st.success("Sensitivity analysis complete!")
else:
    results = None

# Display results
if "sensitivity_results" in st.session_state:
    results = st.session_state["sensitivity_results"]

    if "error" in results:
        st.error(results["error"])
    else:
        # Tornado Diagram
        if "tornado" in results:
            st.divider()
            st.subheader("📊 Tornado Diagram (One-Way Sensitivity)")

            tornado = results["tornado"]

            # Create tornado plot
            fig = go.Figure()

            y_labels = [r.parameter for r in tornado]
            low_outcomes = [r.low_outcome for r in tornado]
            high_outcomes = [r.high_outcome for r in tornado]

            fig.add_trace(
                go.Bar(
                    y=y_labels,
                    x=[high - low for high, low in zip(high_outcomes, low_outcomes)],
                    base=list(low_outcomes),
                    orientation="h",
                    marker_color=["#3498db"] * len(tornado),
                    name="Outcome Range",
                ),
            )

            fig.update_layout(
                title="Parameter Sensitivity (Tornado Diagram)",
                xaxis_title="Testing Uptake",
                yaxis_title="Parameter",
                xaxis=dict(tickformat=".1%"),
                height=400,
                showlegend=False,
            )

            st.plotly_chart(fig, use_container_width=True)

            # Tornado results table
            st.expander("📋 View Tornado Data").dataframe(
                {
                    "Parameter": [r.parameter for r in tornado],
                    "Base Value": [f"{r.base_value:.3f}" for r in tornado],
                    "Range": [f"{r.low_value:.3f} - {r.high_value:.3f}" for r in tornado],
                    "Impact": [f"{r.low_outcome:.1%} - {r.high_outcome:.1%}" for r in tornado],
                    "Sensitivity": [f"{r.sensitivity_magnitude:.4f}" for r in tornado],
                },
            )

        # Sobol Indices
        if "sobol" in results:
            st.divider()
            st.subheader("🌐 Sobol Global Sensitivity Indices")

            sobol = results["sobol"]

            # Create Sobol plot
            fig = go.Figure()

            y_labels = [r.parameter for r in sobol]
            first_order = [float(r.first_order) for r in sobol]
            total_order = [float(r.total_order) for r in sobol]

            fig.add_trace(
                go.Bar(
                    y=y_labels,
                    x=first_order,
                    orientation="h",
                    name="First-Order (S_i)",
                    marker_color="#3498db",
                ),
            )

            fig.add_trace(
                go.Bar(
                    y=y_labels,
                    x=total_order,
                    orientation="h",
                    name="Total-Order (S_Ti)",
                    marker_color="#e74c3c",
                    opacity=0.7,
                ),
            )

            fig.update_layout(
                title="Sobol Sensitivity Indices",
                xaxis_title="Sensitivity Index",
                yaxis_title="Parameter",
                xaxis=dict(range=[0, 1], tickformat=".1%"),
                barmode="overlay",
                height=400,
            )

            st.plotly_chart(fig, use_container_width=True)

            # Explanation
            with st.expander("📖 Understanding Sobol Indices"):
                st.markdown("""
                **First-Order Index (S_i):**
                - Measures the main effect of each parameter
                - Shows how much variance is explained by that parameter alone
                - Range: 0 (no effect) to 1 (dominant effect)

                **Total-Order Index (S_Ti):**
                - Measures total contribution including interactions
                - Shows parameter's main effect + all interaction effects
                - If S_Ti >> S_i: parameter has strong interactions

                **Interpretation:**
                - High S_i: Parameter is important on its own
                - High S_Ti but low S_i: Parameter matters through interactions
                - Low both: Parameter has minimal impact
                """)

            # Sobol results table
            st.expander("📋 View Sobol Data").dataframe(
                {
                    "Parameter": [r.parameter for r in sobol],
                    "First-Order (S_i)": [f"{float(r.first_order):.3f}" for r in sobol],
                    "Total-Order (S_Ti)": [f"{float(r.total_order):.3f}" for r in sobol],
                    "Interactions": [f"{float(r.total_order - r.first_order):.3f}" for r in sobol],
                },
            )

        # Heat Map
        if "heatmap" in results:
            st.divider()
            st.subheader("🔥 Two-Way Sensitivity Heat Map")

            heatmap = results["heatmap"]
            param_names = results["heatmap_params"]

            # Create heat map
            fig = go.Figure(
                data=go.Heatmap(
                    z=heatmap.outcomes,
                    x=[f"{v:.3f}" for v in heatmap.param2_values],
                    y=[f"{v:.3f}" for v in heatmap.param1_values],
                    colorscale="RdYlBu",
                    colorbar=dict(title="Testing Uptake"),
                ),
            )

            fig.update_layout(
                title=f"Interaction: {param_names[0]} × {param_names[1]}",
                xaxis_title=param_names[1],
                yaxis_title=param_names[0],
                height=500,
            )

            st.plotly_chart(fig, use_container_width=True)

            # Heat map stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Min Outcome", f"{heatmap.min_outcome:.1%}")
            with col2:
                st.metric("Max Outcome", f"{heatmap.max_outcome:.1%}")
            with col3:
                st.metric("Range", f"{heatmap.max_outcome - heatmap.min_outcome:.1%}")

else:
    # Placeholder content
    st.info("👈 Configure analysis parameters in the sidebar and click 'Run Sensitivity Analysis'")

    # Example output
    st.markdown("""
    ### What is Sensitivity Analysis?

    Sensitivity analysis helps understand how uncertainty in model inputs affects outputs:

    - **Tornado Diagrams**: Show which parameters have the largest impact
    - **Heat Maps**: Visualize how two parameters interact to affect outcomes
    - **Sobol Indices**: Decompose output variance into contributions
      from each parameter and their interactions

    ### Why Use JAX?

    JAX acceleration enables:
    - ⚡ **Fast computation**: Vectorized operations on GPU/TPU
    - 🎯 **Accurate gradients**: Automatic differentiation for advanced analysis
    - 📊 **Large-scale Monte Carlo**: Run thousands of simulations efficiently
    """)

# Footer
st.divider()
st.caption("""
Sensitivity Analysis v1.0 | JAX-Accelerated | Last updated: 2026-03-05
""")
