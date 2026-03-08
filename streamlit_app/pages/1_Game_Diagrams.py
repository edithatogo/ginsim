#!/usr/bin/env python3
"""
Game Diagrams Page

Interactive visualization of the 6 game-theoretic modules in the
genetic discrimination policy model.
"""

import sys
from io import BytesIO
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import matplotlib.pyplot as plt
import streamlit as st

# Import from core model
from src.model.game_diagrams import (
    create_enforcement_diagram,
    create_module_a_diagram,
    create_module_c_diagram,
    create_module_d_diagram,
    create_module_f_diagram,
)

# Page configuration
st.set_page_config(
    page_title="Game Diagrams",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Title
st.title("🎮 Game-Theoretic Module Diagrams")
st.markdown("""
Interactive visualizations of the 6 game-theoretic modules in the genetic discrimination policy model.

**Each diagram shows:**
- Key actors and decision points
- Information flows and asymmetries
- Policy intervention points
- Equilibrium outcomes
""")

# Sidebar for diagram selection and customization
st.sidebar.header("⚙️ Diagram Settings")

# Diagram selection
diagram_options = {
    "Module A: Behavior/Deterrence": "module_a",
    "Module C: Insurance Equilibrium": "module_c",
    "Module D: Proxy Substitution": "module_d",
    "Module E: Pass-Through": "module_e",
    "Module F: Data Quality": "module_f",
    "Enforcement: Compliance": "enforcement",
}

selected_diagram = st.sidebar.selectbox(
    "Select Module",
    list(diagram_options.keys()),
    help="Choose which game-theoretic module to visualize",
)

diagram_key = diagram_options[selected_diagram]

# Customization options
st.sidebar.subheader("Visual Customization")
show_parameters = st.sidebar.checkbox(
    "Show Model Parameters",
    value=True,
    help="Display current parameter values on diagram",
)

# Get parameters from session state or use defaults
default_params = {
    "module_a": {
        "baseline_uptake": 0.52,
        "deterrence_elasticity": 0.18,
    },
    "module_d": {
        "proxy_accuracy": 0.65,
    },
    "module_e": {
        "pass_through_rate": 0.75,
    },
    "module_f": {
        "research_participation_rate": 0.45,
    },
    "enforcement": {
        "enforcement_strength": 0.7,
        "penalty_rate": 0.5,
    },
}


# Cache diagram creation
@st.cache_data
def create_diagram_cached(diagram_key: str, params: dict) -> BytesIO:
    """Create diagram and return as BytesIO for caching."""
    fig = None

    if diagram_key == "module_a":
        fig = create_module_a_diagram(params=params if show_parameters else None)
    elif diagram_key == "module_c":
        fig = create_module_c_diagram(params=params if show_parameters else None)
    elif diagram_key == "module_d":
        fig = create_module_d_diagram(params=params if show_parameters else None)
    elif diagram_key == "module_e":
        fig = create_enforcement_diagram(params=params if show_parameters else None)
    elif diagram_key == "module_f":
        fig = create_module_f_diagram(params=params if show_parameters else None)
    elif diagram_key == "enforcement":
        fig = create_enforcement_diagram(params=params if show_parameters else None)

    if fig:
        buf = BytesIO()
        fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
        buf.seek(0)
        plt.close(fig)
        return buf

    return None


# Create diagram
params = default_params.get(diagram_key, {})
diagram_buffer = create_diagram_cached(diagram_key, params)

# Display diagram
if diagram_buffer:
    st.image(diagram_buffer, use_container_width=True)
else:
    st.error("Failed to generate diagram")

# Display module description
st.divider()
st.subheader(f"📖 {selected_diagram}")

descriptions = {
    "Module A: Behavior/Deterrence": """
    **Purpose:** Models individual decision-making about genetic testing participation.

    **Key Components:**
    - **Decision Node:** Individual decides whether to take genetic test
    - **Information Set:** Perceived discrimination risk influences decision
    - **Policy Impact:** Bans/moratoria reduce perceived risk → increase testing uptake

    **Equilibrium:** Testing uptake rate determined by deterrence elasticity and policy regime.

    **Key Parameters:**
    - Baseline testing uptake (default: 52%)
    - Deterrence elasticity (default: 18%)
    - Moratorium effect (default: 15%)

    **Policy Insight:** Stronger genetic protections → higher testing uptake → better health outcomes.
    """,
    "Module C: Insurance Equilibrium": """
    **Purpose:** Models insurance market equilibrium under asymmetric information.

    **Key Components:**
    - **High Risk Pool:** Individuals with higher genetic risk
    - **Low Risk Pool:** Individuals with lower genetic risk
    - **Insurer:** Sets premiums without observing individual risk types
    - **Asymmetric Information:** Insurer cannot directly observe risk type

    **Equilibrium Types:**
    - **Separating:** Different premiums for different risk types
    - **Pooling:** Single average premium (adverse selection)

    **Policy Impact:** Genetic testing bans reduce information asymmetry → shift equilibrium type.

    **Key Parameters:**
    - Risk premium differential
    - Proportion of high-risk individuals
    - Information availability

    **Policy Insight:** Information restrictions can improve outcomes for high-risk individuals.
    """,
    "Module D: Proxy Substitution": """
    **Purpose:** Models how insurers use proxies when genetic information is restricted.

    **Key Components:**
    - **Blocked Information:** Genetic test results unavailable (policy restriction)
    - **Alternative Proxies:** Family history, medical records, lifestyle factors
    - **Insurer Inference:** Reconstructs risk using available proxies
    - **Information Leakage:** Proxy use partially circumvents policy intent

    **Key Metric:** Reconstruction Accuracy (how well proxies predict true risk)

    **Policy Impact:** Even with genetic ban, insurers may infer risk via proxies → reduces policy effectiveness.

    **Key Parameters:**
    - Proxy accuracy (default: 65%)
    - Substitution rate
    - Family history predictive value

    **Policy Insight:** Stronger policies must address proxy substitution to be fully effective.
    """,
    "Module E: Pass-Through": """
    **Purpose:** Models how policy costs/benefits pass through market structure.

    **Key Components:**
    - **Insurers:** Set premiums based on risk expectations
    - **Intermediaries:** Brokers, agents, market frictions
    - **Consumers:** Face final premiums and coverage terms

    **Pass-Through Rate:** Fraction of policy cost/benefit passed to consumers.

    **Market Structure Effects:**
    - High competition → High pass-through
    - Market frictions → Incomplete pass-through
    - Monopoly power → Strategic pass-through

    **Policy Impact:** Effectiveness depends on market structure and competition level.

    **Key Parameters:**
    - Pass-through rate (default: 75%)
    - Market concentration
    - Friction magnitude

    **Policy Insight:** Market structure matters - same policy has different effects in different markets.
    """,
    "Module F: Data Quality": """
    **Purpose:** Models positive externality from genetic discrimination protections to research.

    **Key Components:**
    - **Policy:** Genetic discrimination protections
    - **Public Trust:** Increases with strong protections
    - **Research Participation:** Higher trust → more participation
    - **Data Quality:** Better participation → better research data
    - **Feedback Loop:** Better data → better policy design

    **Positive Externality:** Genetic protections benefit research community beyond direct policy goals.

    **Policy Impact:** Strong protections → ↑ trust → ↑ participation → ↑ data quality → better policy.

    **Key Parameters:**
    - Research participation rate (default: 45%)
    - Trust elasticity
    - Data quality improvement

    **Policy Insight:** Genetic protections have spillover benefits for research and future policy.
    """,
    "Enforcement: Compliance": """
    **Purpose:** Models compliance dynamics between insurers and regulators.

    **Key Components:**
    - **Regulator:** Sets rules and enforcement strength
    - **Enforcement Mechanism:** Monitoring and penalty system
    - **Insurer:** Decides whether to comply or violate
    - **Compliance Decision:** Trade-off between compliance cost and expected penalty

    **Equilibrium:** Compliance rate determined by enforcement strength and penalty magnitude.

    **Policy Impact:** Strong enforcement → high compliance; weak enforcement → strategic violations.

    **Key Parameters:**
    - Enforcement strength (default: 70%)
    - Penalty rate (default: 50%)
    - Detection probability

    **Policy Insight:** Optimal policy balances enforcement cost against compliance benefits.
    """,
}

st.markdown(descriptions.get(selected_diagram, "Description not available"))

# Export functionality
st.divider()
st.subheader("📥 Export Diagram")

col1, col2, col3 = st.columns(3)

with col1:
    if diagram_buffer:
        st.download_button(
            label="📥 Download PNG",
            data=diagram_buffer.getvalue(),
            file_name=f"{diagram_key}_diagram.png",
            mime="image/png",
            help="Download diagram as PNG image",
        )


# Create SVG version for download
@st.cache_data
def create_svg_diagram(diagram_key: str, params: dict) -> BytesIO:
    """Create SVG version of diagram."""
    fig = None

    if diagram_key == "module_a":
        fig = create_module_a_diagram(params=params if show_parameters else None)
    elif diagram_key == "module_c":
        fig = create_module_c_diagram(params=params if show_parameters else None)
    elif diagram_key == "module_d":
        fig = create_module_d_diagram(params=params if show_parameters else None)
    elif diagram_key == "module_e":
        fig = create_enforcement_diagram(params=params if show_parameters else None)
    elif diagram_key == "module_f":
        fig = create_module_f_diagram(params=params if show_parameters else None)
    elif diagram_key == "enforcement":
        fig = create_enforcement_diagram(params=params if show_parameters else None)

    if fig:
        buf = BytesIO()
        fig.savefig(buf, format="svg", bbox_inches="tight")
        buf.seek(0)
        plt.close(fig)
        return buf

    return None


with col2:
    svg_buffer = create_svg_diagram(diagram_key, params)
    if svg_buffer:
        st.download_button(
            label="📥 Download SVG",
            data=svg_buffer.getvalue(),
            file_name=f"{diagram_key}_diagram.svg",
            mime="image/svg+xml",
            help="Download diagram as SVG vector image",
        )

with col3:
    st.caption("Diagrams are generated using matplotlib for model interpretation and review.")

# Navigation
st.divider()
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    **Next Steps:**
    - Explore sensitivity analysis in the [Sensitivity](/Sensitivity) page
    - View scenario comparisons in the [Scenarios](/Scenarios) page
    - Return to [Main Dashboard](/)
    """)

# Footer
st.caption("""
Game Diagrams v1.0 | Generated with matplotlib | Last updated: 2026-03-05
""")
