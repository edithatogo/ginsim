"""
Extendable regression cases for the remote Streamlit smoke test.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RemoteSmokeCase:
    sidebar_label: str
    expected_heading: str
    action_button: str | None = None
    expected_text: str | None = None
    additional_assertions: tuple[str, ...] = ()


REMOTE_SMOKE_CASES = (
    RemoteSmokeCase(
        sidebar_label="Game Diagrams",
        expected_heading="Game-Theoretic Module Diagrams",
    ),
    RemoteSmokeCase(
        sidebar_label="Sensitivity",
        expected_heading="Comprehensive Sensitivity & VOI Suite",
        action_button="🎲 Run PSA Simulation",
        expected_text="Expected Uptake (Mean)",
        additional_assertions=("95% CrI:",),
    ),
    RemoteSmokeCase(
        sidebar_label="Scenarios",
        expected_heading="Policy Scenarios & Stories",
        action_button="🔍 Run Comparative Analysis",
        expected_text="High-Rigor Comparative Matrix",
        additional_assertions=("Societal Welfare by Scenario (DCBA Integrated)",),
    ),
    RemoteSmokeCase(
        sidebar_label="Extended Games",
        expected_heading="Extended Strategic Games",
        action_button="🔬 Run Game Simulation",
        expected_text="Reconstruction Accuracy",
        additional_assertions=("Welfare Loss",),
    ),
    RemoteSmokeCase(
        sidebar_label="Delta View",
        expected_heading="Policy Fairness Audit",
        action_button="⚖️ Audit Policies",
        expected_text="Fairness Verdict Matrix",
        additional_assertions=("Ethical Category",),
    ),
)
