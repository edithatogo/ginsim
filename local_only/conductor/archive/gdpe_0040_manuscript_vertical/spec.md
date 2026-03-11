# Track Specification: Automated Manuscript & Report Synchronization

**Track ID:** gdpe_0040_manuscript_vertical
**Type:** Structural Overhaul / Publication
**Goal:** Implement a synchronization engine that keeps the internal manuscript (Markdown) and dashboard reports perfectly aligned with the latest model results.

## 1. Overview
Ensuring that the scientific narrative matches the numerical results is critical for transparency. This track automates the injection of live model outputs (coefficients, welfare totals, QALY gains) into `local_only/docs/MANUSCRIPT.md` and a "Live Publication" view in Streamlit.

## 2. Functional Requirements
- **Markdown Injection Engine:** Implement logic to replace placeholders in Markdown files (e.g., `{{ total_welfare }}`) with live, provenance-hashed results.
- **Dynamic Report Tab:** Create a "Publication Narrative" tab in Streamlit that renders the manuscript text with live interactive charts embedded.
- **Provenance Watermarking:** Ensure every synchronized report block is tagged with the specific Run Manifest Hash.

## 3. Acceptance Criteria
- [ ] `local_only/docs/MANUSCRIPT.md` can be updated with one command/button.
- [ ] Streamlit "Publication" tab displays the full narrative with live-injected values.
- [ ] No more manual copy-pasting of numbers into reports.
