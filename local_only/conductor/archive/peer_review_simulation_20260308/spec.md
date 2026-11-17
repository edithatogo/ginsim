# Track Specification: SOTA Multi-Persona Peer Review & Policy Audit

**Track ID:** peer_review_simulation_20260308
**Type:** Feature / Analysis
**Goal:** Simulate a comprehensive peer review and policy audit from high-impact journals and government departments to prioritize repository improvements and jurisdictional expansions.

## 1. Overview
This track implements an advanced simulation layer where the repository is audited by virtual personas representing Nature, Lancet, and MJA editors, as well as health and treasury executives from Australia and New Zealand. The simulation aims to identify gaps in rigor, utility, and feasibility, which will then be prioritized and implemented into the dashboard, manuscript, and core logic.

## 2. Functional Requirements

### 2.1 Persona Simulation & Questioning
- **Scientific Personas:** Nature, Lancet, MJA (Editors & Reviewers).
- **Government Personas (AU):** Commonwealth Department of Health (Exec/Advisor), Treasury (Exec/Advisor).
- **Government Personas (NZ):** Ministry of Health (Exec/Advisor), NZ Treasury (Exec/Advisor).
- **Questions to Address:**
    1. Utility: Is this model useful for its intended purpose?
    2. Policy Impact: Does it help in making specific policy decisions?
    3. Gaps: What is missing that would make it more helpful?
    4. Features: Recommendations for new inputs, outputs, equations, tables, or visualizations.
    5. Jurisdiction: Is expansion beyond AU/NZ recommended?

### 2.2 Parallel Code Investigation
- Use **Codebase Investigator** sub-agents for each persona group to ensure deep, independent analysis of the current code's alignment with their specific standards.
- Save outputs from these investigator sessions into `local_only/context/simulated_reviews/`.

### 2.3 Synthesis & Prioritization
- Simulate a "Stakeholder Meeting" where all personas meet to prioritize implementation of new features.
- Resulting priorities must be promulgated into:
    - **Dashboard:** New interactive features or tabs.
    - **Manuscript:** Methodological refinements and internal reporting.
    - **Core Logic:** Mathematical updates or new jurisdictional modules.

### 2.4 Jurisdictional Scope
- Separate and unified analysis for Australia and New Zealand.
- Investigation into the value of adding specific international jurisdictions (e.g., UK, USA, Canada).

## 3. Non-Functional Requirements
- **Diamond Standard Rigor:** All simulated feedback must be grounded in the existing code's JAX/Jacobian proofs and PBT coverage.
- **Traceability:** Link simulated feedback to specific line numbers and architectural patterns identified by the sub-agents.

## 4. Acceptance Criteria
- [ ] Review reports from all 7+ persona groups generated and saved locally.
- [ ] "Stakeholder Meeting Minutes" and "Prioritization Matrix" generated.
- [ ] At least one high-priority feature from the meeting implemented in the Streamlit app.
- [ ] Manuscript methods section updated based on scientific editorial feedback.
- [ ] Recommendations for additional jurisdictions documented.

## 5. Out of Scope
- Full implementation of *every* feature suggested (only prioritized features are in scope).
- Live interviews with actual humans (strictly simulation-based).
