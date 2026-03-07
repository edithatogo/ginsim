#!/usr/bin/env python3
"""
Extended Strategic Games Page

Interactive exploration of advanced game-theoretic scenarios:
- Information Leakage Game
- Genetic Altruism Game
- Cascade Testing Game
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import jax.numpy as jnp
import plotly.graph_objects as go
import streamlit as st

# Import from core model
from src.model.extended_games import (
    cascade_testing_game,
    genetic_altruism_game,
    information_leakage_game,
)

# Page configuration
st.set_page_config(
    page_title="Extended Strategic Games",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Title
st.title("🎮 Extended Strategic Games")
st.markdown("""
**Explore advanced game-theoretic scenarios beyond basic policy analysis.**

These games model complex behavioral dynamics:
- **Information Leakage:** How insurers bypass genetic bans using proxies
- **Genetic Altruism:** Family-influenced testing decisions
- **Cascade Testing:** Sequential testing within families
""")
st.warning(
    """
Exploratory surface: these games are designed to show strategic mechanisms and edge cases.
They are not currently equivalent to the benchmark policy-comparison surfaces used for core scenario results.
"""
)

# Sidebar for game selection
st.sidebar.header("⚙️ Game Configuration")

game_selection = st.sidebar.radio(
    "Select Game",
    ["Information Leakage", "Genetic Altruism", "Cascade Testing"],
    help="Choose which strategic game to explore",
)

# Run button
run_clicked = st.sidebar.button("🔬 Run Game Simulation", type="primary")

if run_clicked or f"{game_selection}_results" in st.session_state:
    # Execute selected game
    if game_selection == "Information Leakage":
        st.sidebar.subheader("Information Leakage Parameters")

        baseline_uptake = st.sidebar.slider(
            "Baseline Testing Uptake",
            min_value=0.3,
            max_value=0.7,
            value=0.52,
            step=0.01,
        )

        ban_effectiveness = st.sidebar.slider(
            "Ban Effectiveness",
            min_value=0.0,
            max_value=1.0,
            value=0.8,
            step=0.05,
            help="How effectively the ban prevents discrimination",
        )

        proxy_accuracy = st.sidebar.slider(
            "Proxy Accuracy",
            min_value=0.0,
            max_value=1.0,
            value=0.6,
            step=0.05,
            help="How well proxies predict genetic risk",
        )

        insurer_inference = st.sidebar.slider(
            "Insurer Inference Strength",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.05,
            help="Insurer's ability to use proxies",
        )

        result = information_leakage_game(
            baseline_uptake=jnp.asarray(float(baseline_uptake)),
            ban_effectiveness=jnp.asarray(float(ban_effectiveness)),
            proxy_accuracy=jnp.asarray(float(proxy_accuracy)),
            insurer_inference_strength=jnp.asarray(float(insurer_inference)),
        )

        st.session_state["leakage_results"] = result
        st.session_state["current_game"] = "Information Leakage"

    elif game_selection == "Genetic Altruism":
        st.sidebar.subheader("Genetic Altruism Parameters")

        baseline_uptake = st.sidebar.slider(
            "Baseline Testing Uptake",
            min_value=0.3,
            max_value=0.7,
            value=0.5,
            step=0.01,
        )

        family_risk = st.sidebar.slider(
            "Family Risk Level",
            min_value=0.0,
            max_value=1.0,
            value=0.3,
            step=0.05,
            help="Family's genetic risk level",
        )

        altruism_strength = st.sidebar.slider(
            "Altruism Strength",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.05,
            help="Strength of altruistic motivation",
        )

        family_size = st.sidebar.slider(
            "Family Size",
            min_value=2,
            max_value=10,
            value=4,
            step=1,
        )

        result = genetic_altruism_game(
            baseline_uptake=jnp.asarray(float(baseline_uptake)),
            family_risk_level=jnp.asarray(float(family_risk)),
            altruism_strength=jnp.asarray(float(altruism_strength)),
            family_size=jnp.asarray(float(family_size)),
        )

        st.session_state["altruism_results"] = result
        st.session_state["current_game"] = "Genetic Altruism"

    elif game_selection == "Cascade Testing":
        st.sidebar.subheader("Cascade Testing Parameters")

        index_rate = st.sidebar.slider(
            "Index Case Rate",
            min_value=0.01,
            max_value=0.2,
            value=0.05,
            step=0.01,
            help="Rate of initial testers",
        )

        contact_rate = st.sidebar.slider(
            "Family Contact Rate",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.05,
            help="Fraction of families contacted",
        )

        cascade_uptake = st.sidebar.slider(
            "Uptake After Contact",
            min_value=0.0,
            max_value=1.0,
            value=0.4,
            step=0.05,
            help="Testing uptake after family contact",
        )

        family_size = st.sidebar.slider(
            "Average Family Size",
            min_value=2,
            max_value=10,
            value=4,
            step=1,
        )

        test_cost = st.sidebar.number_input(
            "Cost per Test ($)",
            min_value=0,
            max_value=5000,
            value=500,
            step=50,
        )

        detection_yield = st.sidebar.slider(
            "Detection Yield",
            min_value=0.01,
            max_value=0.5,
            value=0.1,
            step=0.01,
            help="Probability of detecting mutation",
        )

        result = cascade_testing_game(
            index_case_rate=jnp.asarray(float(index_rate)),
            family_contact_rate=jnp.asarray(float(contact_rate)),
            uptake_after_contact=jnp.asarray(float(cascade_uptake)),
            average_family_size=jnp.asarray(float(family_size)),
            cost_per_test=jnp.asarray(float(test_cost)),
            detection_yield=jnp.asarray(float(detection_yield)),
        )

        st.session_state["cascade_results"] = result
        st.session_state["current_game"] = "Cascade Testing"

# Display results
st.divider()

if "current_game" in st.session_state:
    game_name = st.session_state["current_game"]
    st.subheader(f"📊 {game_name} Results")

    if game_name == "Information Leakage":
        result = st.session_state.get("leakage_results")
        if result:
            # Metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Reconstruction Accuracy", f"{result.reconstruction_accuracy:.1%}")
            with col2:
                st.metric("Bypass Rate", f"{result.bypass_rate:.1%}")
            with col3:
                st.metric("Effective Uptake", f"{result.effective_uptake:.1%}")
            with col4:
                st.metric("Welfare Loss", f"${result.welfare_loss:,.0f}")

            # Visualization
            fig = go.Figure()

            fig.add_trace(
                go.Bar(
                    x=["Reconstruction", "Bypass", "Effective Uptake"],
                    y=[
                        result.reconstruction_accuracy,
                        result.bypass_rate,
                        result.effective_uptake,
                    ],
                    marker_color=["#e74c3c", "#f39c12", "#2ecc71"],
                    text=[
                        f"{result.reconstruction_accuracy:.1%}",
                        f"{result.bypass_rate:.1%}",
                        f"{result.effective_uptake:.1%}",
                    ],
                    textposition="outside",
                ),
            )

            fig.update_layout(
                title="Information Leakage Metrics",
                yaxis_title="Value",
                yaxis=dict(tickformat=".0%"),
                height=400,
                showlegend=False,
            )

            st.plotly_chart(fig, use_container_width=True)

            # Insights
            st.info(
                f"""
                **Key Insight:** With {result.bypass_rate:.1%} bypass rate, 
                approximately {result.bypass_rate * 100:.0f}% of the ban's effectiveness 
                is lost through proxy-based information leakage.
                """,
            )

    elif game_name == "Genetic Altruism":
        result = st.session_state.get("altruism_results")
        if result:
            # Metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Altruism Coefficient", f"{result.altruism_coefficient:.2f}")
            with col2:
                st.metric("Family Testing Rate", f"{result.family_testing_rate:.1%}")
            with col3:
                st.metric("Spillover Effect", f"{result.spillover_effect:.3f}")
            with col4:
                st.metric("Welfare Impact", f"${result.welfare_impact:,.0f}")

            # Visualization
            fig = go.Figure()

            fig.add_trace(
                go.Bar(
                    x=["Baseline", "With Altruism"],
                    y=[0.5, result.family_testing_rate],
                    marker_color=["#95a5a6", "#3498db"],
                    text=[f"{0.5:.1%}", f"{result.family_testing_rate:.1%}"],
                    textposition="outside",
                ),
            )

            fig.update_layout(
                title="Testing Rate: Self-Interest vs Altruism",
                yaxis_title="Testing Rate",
                yaxis=dict(tickformat=".0%"),
                height=400,
                showlegend=False,
            )

            st.plotly_chart(fig, use_container_width=True)

            # Insights
            st.success(
                f"""
                **Positive Spillover:** Altruistic behavior increases family testing 
                by {(result.family_testing_rate - 0.5) * 100:.1f} percentage points,
                generating ${result.welfare_impact:,.0f} in net welfare.
                """,
            )

    elif game_name == "Cascade Testing":
        result = st.session_state.get("cascade_results")
        if result:
            # Metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Cascade Rate", f"{result.cascade_rate:.1f}x")
            with col2:
                st.metric("Index Cases", result.index_cases)
            with col3:
                st.metric("Secondary Cases", result.secondary_cases)
            with col4:
                st.metric("Total Tests", result.total_tests)

            # Additional metrics
            col5, col6 = st.columns(2)
            with col5:
                st.metric("Cost per Detection", f"${result.cost_effectiveness:,.0f}")
            with col6:
                detection_count = result.index_cases * 0.1 + result.secondary_cases * 0.05
                st.metric("Estimated Detections", int(detection_count))

            # Visualization
            fig = go.Figure()

            fig.add_trace(
                go.Bar(
                    x=["Index Cases", "Secondary Cases"],
                    y=[result.index_cases, result.secondary_cases],
                    marker_color=["#3498db", "#2ecc71"],
                    text=[str(result.index_cases), str(result.secondary_cases)],
                    textposition="outside",
                ),
            )

            fig.update_layout(
                title="Cascade Testing Breakdown",
                yaxis_title="Number of Cases",
                height=400,
                showlegend=False,
            )

            st.plotly_chart(fig, use_container_width=True)

            # Insights
            st.info(
                f"""
                **Cascade Effect:** Each index case generates {result.cascade_rate:.1f} 
                additional tests through family cascade, making this 
                ${result.cost_effectiveness:,.0f} per detection.
                """,
            )

# Documentation
st.divider()
with st.expander("📖 About Extended Strategic Games"):
    st.markdown("""
    ### Information Leakage Game
    
    Models how insurers may circumvent genetic discrimination bans using proxy variables:
    - **Family History:** Insurers use family medical history to infer genetic risk
    - **Medical Records:** Electronic health records may reveal genetic information
    - **Lifestyle Factors:** Correlated behaviors may signal genetic predisposition
    
    **Policy Implication:** Strong enforcement and broad definitions of genetic information
    are needed to prevent leakage.
    
    ---
    
    ### Genetic Altruism Game
    
    Models testing decisions influenced by family welfare:
    - **Altruistic Motivation:** Getting tested to help family members
    - **Spillover Effects:** Non-tested family members benefit from information
    - **Family Size Effect:** Larger families show stronger altruism
    
    **Policy Implication:** Family-centered interventions may be more effective
    than individual-focused approaches.
    
    ---
    
    ### Cascade Testing Game
    
    Models sequential testing within families after index case identification:
    - **Index Cases:** Initial testers who identify genetic risk
    - **Cascade Effect:** Family members tested after contact
    - **Cost-Effectiveness:** Cascade testing often more efficient than population screening
    
    **Policy Implication:** Supporting cascade testing programs can improve
    cost-effectiveness of genetic testing initiatives.
    """)

# Footer
st.caption("""
Extended Strategic Games v1.0 | Last updated: 2026-03-05
""")
