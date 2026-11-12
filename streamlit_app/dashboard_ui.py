"""
Shared dashboard UX helpers for the Streamlit surfaces.
"""

from __future__ import annotations

import os
import subprocess
from collections.abc import Mapping
from functools import lru_cache
from pathlib import Path

import streamlit as st

JURISDICTION_OPTIONS = ["Australia", "New Zealand", "UK", "Canada", "US"]
AUDIENCE_MODES = ["General audience", "Research / policy"]

_GLOSSARY = {
    "Moratorium": "A temporary restriction. In this app it means insurers face limits on using genetic test results.",
    "Status Quo": "The current rules with no new reform added.",
    "Testing uptake": "The share of people who choose to take a genetic test.",
    "Social benefit": "The model's combined view of health gains, costs, and broader effects on society.",
    "Compliance": "How closely insurers follow the policy rules.",
    "Equity weighting": "Giving more weight to impacts on groups facing greater disadvantage.",
    "Uncertainty": "The fact that some assumptions in the model are not known exactly.",
    "Scenario": "A named policy story or setup used to compare outcomes.",
}

_JURISDICTION_TO_CONFIG_ID = {
    "Australia": "australia",
    "New Zealand": "new_zealand",
    "UK": "uk",
    "Canada": "canada",
    "US": "us",
}

_JURISDICTION_TO_CODE = {
    "Australia": "AU",
    "New Zealand": "NZ",
    "UK": "UK",
    "Canada": "CA",
    "US": "US",
}


def jurisdiction_to_config_id(label: str) -> str:
    """Map a user-facing jurisdiction label to the config identifier."""
    return _JURISDICTION_TO_CONFIG_ID.get(label, "australia")


def jurisdiction_to_code(label: str) -> str:
    """Map a user-facing jurisdiction label to the scenario config code."""
    return _JURISDICTION_TO_CODE.get(label, "AU")


@lru_cache(maxsize=1)
def get_build_label() -> str:
    """Return a short deployment/build label for operator visibility."""
    for env_name in (
        "GINSIM_BUILD_SHA",
        "GITHUB_SHA",
        "VERCEL_GIT_COMMIT_SHA",
        "RAILWAY_GIT_COMMIT_SHA",
        "RENDER_GIT_COMMIT",
    ):
        value = os.environ.get(env_name)
        if value:
            return value[:7]

    project_root = Path(__file__).resolve().parents[1]
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=project_root,
            capture_output=True,
            check=True,
            text=True,
            timeout=2,
        )
    except Exception:
        return "local"

    build_label = result.stdout.strip()
    return build_label or "local"


def render_sidebar_build_info() -> None:
    """Surface a lightweight build stamp in the sidebar."""
    st.sidebar.markdown("---")
    st.sidebar.caption(f"Build: `{get_build_label()}`")


def render_view_mode_sidebar() -> str:
    """Render and persist the shared app audience mode."""
    current_mode = st.session_state.get("audience_mode", AUDIENCE_MODES[0])
    if current_mode not in AUDIENCE_MODES:
        current_mode = AUDIENCE_MODES[0]

    selected = st.sidebar.radio(
        "View mode",
        AUDIENCE_MODES,
        index=AUDIENCE_MODES.index(current_mode),
        key="audience_mode_selector",
        help="General audience mode uses simpler language. Research / policy mode keeps the technical surfaces.",
    )
    st.session_state["audience_mode"] = selected
    return selected


def render_current_run_summary(title: str, items: Mapping[str, str]) -> None:
    """Render a compact current-context summary strip."""
    entries = list(items.items())
    if not entries:
        return

    st.subheader(title)
    columns = st.columns(len(entries))
    for column, (label, value) in zip(columns, entries, strict=False):
        column.metric(label, str(value))


def render_start_here(audience_mode: str = "Research / policy") -> None:
    """Provide first-run orientation for the landing page."""
    st.subheader("Start Here")
    if audience_mode == "General audience":
        st.markdown(
            "1. Pick a country and a policy in the sidebar.\n"
            "2. Click **Run Evaluation** to see what changes for people, insurers, and society.\n"
            "3. Use the other tabs to compare countries or try alternative policy settings."
        )
        st.info(
            "This app has a simple mode for general readers and an advanced mode for research and policy work."
        )
        return

    st.markdown(
        "1. Set the jurisdiction and assumption sliders in the sidebar.\n"
        "2. Run a primary evaluation to generate uptake, welfare, and compliance results.\n"
        "3. Use the other tabs to stress-test the result with uncertainty, scenarios, and fairness audits."
    )


def render_glossary(audience_mode: str) -> None:
    """Show a compact glossary for non-specialist readers."""
    if audience_mode != "General audience":
        return

    with st.expander("Glossary"):
        for term, definition in _GLOSSARY.items():
            st.markdown(f"**{term}:** {definition}")


def render_footer(extra: str | None = None) -> None:
    """Render a consistent footer with deployment metadata."""
    parts = [
        "Developed by Dylan A Mordaunt",
        "2026.03",
        f"Build {get_build_label()}",
    ]
    if extra:
        parts.append(extra)

    st.divider()
    st.caption(" • ".join(parts))
