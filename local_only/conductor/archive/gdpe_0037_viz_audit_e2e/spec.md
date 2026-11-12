# Track Specification: End-to-End Visualization Audit

**Track ID:** gdpe_0037_viz_audit_e2e
**Type:** Verification / Quality
**Goal:** Perform a systematic, interaction-level audit of all repository visualizations to ensure mathematical correctness, data-to-UI synchronization, and alignment with the Diamond Standard.

## 1. Overview
The dashboard has grown in complexity, with new Radar, Bar, and Scatter charts integrated. This track ensures that every pixel displayed in Streamlit accurately reflects the underlying JAX engine results, without silent drops or approximation errors.

## 2. Functional Requirements
- **Verification Mapping:** Map every chart in `app.py` and `pages/*.py` to its corresponding core logic function in `src/model/`.
- **Numerical Validation:** Cross-check Streamlit `st.metric` and `st.plotly_chart` values against raw `pytest` outputs.
- **Visual Invariants:** Ensure consistent axis scaling, colorblind-safe palettes, and standardized labelling across all jurisdictions.
- **Export Audit:** Verify that "Download Report" functions produce data consistent with the on-screen visualizations.

## 3. Non-Functional Requirements
- **Correctness:** Zero discrepancy allowed between JAX array outputs and UI display.
- **Traceability:** Every chart must display its Provenance Audit ID where relevant.

## 4. Acceptance Criteria
- [ ] Complete Audit Matrix (Chart vs. Data Source) documented.
- [ ] Interaction-level tests (Playwright/AppTest) updated to verify numerical values, not just existence.
- [ ] Any "Visual Drops" (e.g., clipped labels, misleading axes) identified and fixed.
- [ ] Final "Visual Quality Gate" passed.
