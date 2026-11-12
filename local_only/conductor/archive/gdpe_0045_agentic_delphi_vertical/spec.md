# Track Specification: Agentic Delphi Protocol Vertical

**Track ID:** gdpe_0045_agentic_delphi_vertical
**Type:** Structural Overhaul / Governance
**Goal:** Integrate the multi-persona audit framework as a permanent governance layer, enabling live "Stakeholder Sentiment" analysis for every policy scenario.

## 1. Overview
Instead of a static peer review, this vertical makes the "Simulated Stakeholder Meeting" a dynamic feature of the pipeline. Every time a user runs a scenario, the personas (Nature, Treasury, etc.) re-audit the results and provide qualitative feedback.

## 2. Functional Requirements
- **Live Auditor Integration:** Create `src/model/agentic_auditor.py` to wrap persona-based LLM queries.
- **Sentiment Consensus:** Implement a "Delphi Protocol" logic to reach consensus among personas on a specific result.
- **Divergence Metrics:** Calculate the "Epistemic Divergence" between different persona groups.

## 3. Acceptance Criteria
- [ ] Every dashboard run includes a "Virtual Stakeholder Verdict."
- [ ] New "Stakeholder Consensus" visualization in Streamlit.
- [ ] Logic for detect "Policy Drift" based on persona sentiment trends.
