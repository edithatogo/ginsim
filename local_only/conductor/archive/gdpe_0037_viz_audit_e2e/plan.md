# Implementation Plan: End-to-End Visualization Audit

**Track ID:** gdpe_0037_viz_audit_e2e
**Execution mode:** Autonomous Phase Loop (with Ralph thinking)

## Phase 1: Deep Mapping (Ralph Loop #1)
- [x] **Task: Deep Exploration of UI-Data Linkage**
    - [x] Perform a "Ralph Thinking" session: Ask "How could the data be misinterpreted between JAX tracers and Streamlit state?"
    - [x] Trace the path from `PolicyEvaluationResult` to each `go.Figure`.
- [x] **Task: Document the Audit Matrix**
- [x] **Task: Conductor - Autonomous Review & Remediation 'Mapping'**

## Phase 2: Systematic Verification
- [x] **Task: Numerical Cross-Check**
    - [x] Run the model CLI and the app locally; verify the QALY and Welfare metrics match to 4 decimal places.
- [x] **Task: Plotly Configuration Review**
    - [x] Audit hover-templates, tooltips, and axis limits.
- [x] **Task: Conductor - Autonomous Review & Remediation 'Verification'**

## Phase 3: Automated UI Regression
- [x] **Task: Expand AppTests**
    - [x] Implement value-based assertions in `tests/e2e/test_dashboard.py`.
- [x] **Task: Export/Download Audit**
- [x] **Task: Conductor - Autonomous Review & Remediation 'Regression'**

## Phase 4: Iterative Improvement (Ralph Loop #2)
- [x] **Task: Improvement Inquiry**
    - [x] Ask "What additional visualizations would stakeholders (Nature/Lancet) find missing now that the logic is integrated?"
    - [x] Suggest 2 improvements to the UI/UX.
- [x] **Task: Close Track**
