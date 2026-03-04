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

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Import from core model
from src.model.parameters import ModelParameters, PolicyConfig
from src.model.pipeline import evaluate_single_policy, compare_policies
from src.model.module_a_behavior_wrappers import get_standard_policies

# Page configuration
st.set_page_config(
    page_title="Genetic Discrimination Policy Dashboard",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and header
st.title("🧬 Genetic Discrimination Policy Dashboard")
st.markdown("""
Interactive exploration of policy impacts on genetic testing uptake, insurance markets, and social welfare.

**Uses core JAX-accelerated model for all computations.**
""")

# Navigation to new pages
st.info("""
**🎯 New Features:**
- 🎮 [Game Diagrams](/1_Game_Diagrams) - Visualize the 6 game-theoretic modules
- 📊 [Sensitivity Analysis](/2_Sensitivity) - Comprehensive sensitivity and uncertainty analysis
- 🎯 [Scenario Analysis](/3_Scenarios) - Compare policy scenarios and use the Australian Policy Sandbox
""")

# Sidebar for parameter adjustment
st.sidebar.header("⚙️ Model Parameters")

# Policy selection
policy_name = st.sidebar.selectbox(
    "Policy Regime",
    ["Status Quo", "Moratorium", "Statutory Ban"],
    help="Select the policy regime to evaluate"
)

# Parameter sliders with model defaults
params = ModelParameters()

baseline_uptake = st.sidebar.slider(
    "Baseline Testing Uptake",
    min_value=0.3,
    max_value=0.7,
    value=float(params.baseline_testing_uptake),
    step=0.01,
    help="Baseline probability of genetic testing"
)

deterrence_elasticity = st.sidebar.slider(
    "Deterrence Elasticity",
    min_value=0.0,
    max_value=0.5,
    value=float(params.deterrence_elasticity),
    step=0.01,
    help="Elasticity of testing with respect to perceived penalty"
)

moratorium_effect = st.sidebar.slider(
    "Moratorium Effect",
    min_value=0.0,
    max_value=0.3,
    value=float(params.moratorium_effect),
    step=0.01,
    help="Additional uptake from moratorium policy"
)

# Jurisdiction selection
jurisdiction = st.sidebar.selectbox(
    "Jurisdiction",
    ["Australia", "New Zealand"],
    help="Select jurisdiction for calibration"
)

# Cache model evaluation
@st.cache_data
def evaluate_policy_cached(params_dict, policy_name):
    """Cached policy evaluation using core model."""
    # Create parameters from dict
    params = ModelParameters(**params_dict)
    
    # Get policy config
    policies = get_standard_policies()
    policy = policies.get(policy_name.lower().replace(' ', '_'), policies['status_quo'])
    
    # Evaluate using core model
    result = evaluate_single_policy(params, policy)
    
    return {
        'testing_uptake': float(result.testing_uptake),
        'welfare_impact': float(result.welfare_impact),
        'qalys_gained': float(result.qalys_gained) if hasattr(result, 'qalys_gained') else 0.0,
    }

# Calculate results using core model
if st.sidebar.button("🔬 Run Model", type="primary"):
    with st.spinner("Running core model (JAX-accelerated)..."):
        params_dict = {
            'baseline_testing_uptake': baseline_uptake,
            'deterrence_elasticity': deterrence_elasticity,
            'moratorium_effect': moratorium_effect,
            'jurisdiction': jurisdiction.lower(),
        }
        
        results = evaluate_policy_cached(params_dict, policy_name)
        st.session_state['results'] = results
        st.session_state['policy_name'] = policy_name
        st.success("Model evaluation complete!")

# Display results in tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Results", "📈 Charts", "📋 Comparison", "📖 Documentation"])

with tab1:
    st.header("Policy Impact Results")
    
    if 'results' in st.session_state:
        results = st.session_state['results']
        policy_name = st.session_state['policy_name']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="Testing Uptake",
                value=f"{results['testing_uptake']:.1%}",
                delta=f"vs Baseline"
            )
        
        with col2:
            st.metric(
                label="Welfare Impact",
                value=f"${results['welfare_impact']:,.0f}",
                delta="Net Present Value"
            )
        
        with col3:
            st.metric(
                label="QALYs Gained",
                value=f"{results['qalys_gained']:.2f}",
                delta="Quality-Adjusted Life Years"
            )
        
        st.divider()
        
        # Detailed results table
        st.subheader("Detailed Results")
        results_df = pd.DataFrame({
            "Metric": ["Testing Uptake", "Welfare Impact", "QALYs Gained"],
            "Value": [
                f"{results['testing_uptake']:.1%}",
                f"${results['welfare_impact']:,.0f}",
                f"{results['qalys_gained']:.2f}"
            ],
            "Policy": [policy_name] * 3
        })
        st.table(results_df)
    else:
        st.info("👈 Click 'Run Model' in the sidebar to see results")

with tab2:
    st.header("Visualizations")
    
    if 'results' in st.session_state:
        # Policy comparison chart
        st.subheader("Testing Uptake by Policy")
        
        policies = ["Status Quo", "Moratorium", "Statutory Ban"]
        
        # Get uptakes for all policies
        params_dict = {
            'baseline_testing_uptake': baseline_uptake,
            'deterrence_elasticity': deterrence_elasticity,
            'moratorium_effect': moratorium_effect,
            'jurisdiction': jurisdiction.lower(),
        }
        
        uptakes = []
        for pol in policies:
            result = evaluate_policy_cached(params_dict, pol)
            uptakes.append(result['testing_uptake'])
        
        fig = go.Figure(data=[
            go.Bar(
                x=policies,
                y=uptakes,
                marker_color=['#0072B2', '#009E73', '#D55E00'],
                text=[f'{u:.1%}' for u in uptakes],
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            title="Testing Uptake by Policy Regime",
            xaxis_title="Policy",
            yaxis_title="Testing Uptake",
            yaxis=dict(tickformat='.0%'),
            showlegend=False,
            width=700,
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=False)
        
        # Sensitivity analysis
        st.subheader("Sensitivity Analysis")
        
        # One-way sensitivity
        elasticity_range = np.linspace(0.0, 0.5, 50)
        uptake_sensitivity = []
        
        for e in elasticity_range:
            params_dict_sens = params_dict.copy()
            params_dict_sens['deterrence_elasticity'] = e
            result = evaluate_policy_cached(params_dict_sens, policy_name)
            uptake_sensitivity.append(result['testing_uptake'])
        
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=elasticity_range,
            y=uptake_sensitivity,
            mode='lines',
            line=dict(color='#0072B2', width=3)
        ))
        
        fig2.update_layout(
            title="Sensitivity to Deterrence Elasticity",
            xaxis_title="Deterrence Elasticity",
            yaxis_title="Testing Uptake",
            yaxis=dict(tickformat='.0%'),
            width=700,
            height=500
        )
        
        st.plotly_chart(fig2, use_container_width=False)
    else:
        st.info("👈 Click 'Run Model' in the sidebar to see visualizations")

with tab3:
    st.header("Policy Comparison")
    
    if 'results' in st.session_state:
        # Get results for all policies
        params_dict = {
            'baseline_testing_uptake': baseline_uptake,
            'deterrence_elasticity': deterrence_elasticity,
            'moratorium_effect': moratorium_effect,
            'jurisdiction': jurisdiction.lower(),
        }
        
        comparison_data = {
            "Policy": [],
            "Testing Uptake": [],
            "Welfare Impact": [],
            "QALYs Gained": []
        }
        
        for pol in ["Status Quo", "Moratorium", "Statutory Ban"]:
            result = evaluate_policy_cached(params_dict, pol)
            comparison_data["Policy"].append(pol)
            comparison_data["Testing Uptake"].append(f"{result['testing_uptake']:.1%}")
            comparison_data["Welfare Impact"].append(f"${result['welfare_impact']:,.0f}")
            comparison_data["QALYs Gained"].append(f"{result['qalys_gained']:.2f}")
        
        comparison_df = pd.DataFrame(comparison_data)
        st.table(comparison_df)
        
        # Download button
        csv = comparison_df.to_csv(index=False, encoding='utf-8')
        st.download_button(
            label="📥 Download Comparison (CSV)",
            data=csv,
            file_name="policy_comparison.csv",
            mime="text/csv",
            help="Download policy comparison data as CSV"
        )
    else:
        st.info("👈 Click 'Run Model' in the sidebar to see comparison")

with tab4:
    st.header("Documentation")
    
    st.markdown("""
    ## Model Overview
    
    This dashboard uses the **core JAX-accelerated model** from the genetic discrimination policy evaluation framework.
    
    ### Core Modules
    
    The model implements 6 game-theoretic modules:
    
    1. **Module A**: Behavior/Deterrence - Testing participation decisions
    2. **Module C**: Insurance Equilibrium - Premium setting under asymmetric information
    3. **Module D**: Proxy Substitution - Insurer response to information constraints
    4. **Module E**: Pass-Through - Market structure effects
    5. **Module F**: Data Quality - Research participation externalities
    6. **Enforcement**: Compliance - Regulatory enforcement
    
    ### Key Parameters
    
    | Parameter | Base Value | Source |
    |-----------|------------|--------|
    | Baseline Testing Uptake | 0.52 | Ettema et al. (2021) |
    | Deterrence Elasticity | 0.18 | McGuire et al. (2019) |
    | Moratorium Effect | 0.15 | Taylor et al. (2021) |
    
    ### JAX/XLA Acceleration
    
    The core model uses JAX with JIT compilation for:
    - **Vectorization**: Efficient batch computation
    - **Automatic Differentiation**: Gradient-based optimization
    - **XLA Acceleration**: Optimized computation graphs
    
    ### References
    
    - Ettema et al. (2021). Uptake of Genetic Testing. Genetics in Medicine.
    - McGuire et al. (2019). Perceived Genetic Discrimination. AJHG.
    - Taylor et al. (2021). Genetic Discrimination in Australia. JLM.
    - Hersch & Viscusi (2019). Genetic Information and Insurance Markets. Geneva Risk.
    
    ### About
    
    **Developer:** Dylan A. Mordaunt  
    **Affiliation:** Victoria University of Wellington  
    **School of Economics and Finance**
    
    **License:** MIT License
    """)

# Footer
st.divider()
st.caption("""
Dashboard v2.0 | Core Model v0.2.0 | JAX-Accelerated | Last updated: 2026-03-04
""")
