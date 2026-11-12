# Implementation Plan: Teaching Personas

**Track ID:** gdpe_0046_teaching_personas
**Execution mode:** Autonomous Phase Loop

## Phase 1: Ingestion & Distillation (Numerical Grounding)
- [x] **Task: Deep Exploration of Document Grounding**
    - [x] Perform a "Ralph Thinking" session: Ask "How do we ensure the LLM-distilled weights for a new persona are consistent with the existing ones, and not just arbitrary noise?"
- [x] **Task: Implement `src/utils/persona_distiller.py`.**
- [x] **Task: Conductor - Autonomous Review & Remediation 'Distillation'**

## Phase 2: Dynamic Auditor Core
- [x] **Task: Update `src/model/agentic_auditor.py` to support dynamic loading.**
- [x] **Task: Implement caching for 'Taught' personas.**
- [x] **Task: Conductor - Autonomous Review & Remediation 'Dynamic'**

## Phase 3: UI Integration
- [x] **Task: Add "Teach Persona" interface to Streamlit.**
- [x] **Task: Implement feedback loop for 'Weight Calibration' by the user.**
- [x] **Task: Conductor - Autonomous Review & Remediation 'UI'**

## Phase 4: Final Verification
- [x] **Task: Integration Test with standard policy documents.**
- [x] **Task: Close Track**
