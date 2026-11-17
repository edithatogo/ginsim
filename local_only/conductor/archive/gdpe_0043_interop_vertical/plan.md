# Implementation Plan: Interoperability Vertical

**Track ID:** gdpe_0043_interop_vertical
**Execution mode:** Autonomous Phase Loop (with Ralph thinking)

## Phase 1: Ecosystem Mapping (Ralph Loop #1)
- [x] **Task: Deep Exploration of HTA Interoperability**
    - [x] Perform a "Ralph Thinking" session: Ask "Can we create a 'Universal Policy Schema' that allows other researchers to replicate our model results using only our exported JSON, without needing access to our Python environment?"
- [x] **Task: Define the "Outcome Schema" for GINSIM.**
- [x] **Task: Conductor - Autonomous Review & Remediation 'Schema'**

## Phase 2: Export Engine
- [x] **Task: Implement `src/utils/hta_export.py`.**
- [x] **Task: Implement Excel template generation (using `openpyxl` or `pandas`).**
- [x] **Task: Conductor - Autonomous Review & Remediation 'Export'**

## Phase 3: Dashboard Promulgation
- [x] **Task: Add "Model Interoperability" tab to Streamlit.**
- [x] **Task: Implement one-click "Download HTA Dossier."**
- [x] **Task: Conductor - Autonomous Review & Remediation 'UI'**

## Phase 4: Final Verification
- [ ] **Task: Improvement Inquiry**
    - [ ] Ask "Should we implement a 'Model-as-a-Service' API (FastAPI) to allow live remote queries from other platforms?"
- [x] **Task: Close Track**

## Phase: Review Fixes
- [x] Task: Apply review suggestions 7ca45a8
