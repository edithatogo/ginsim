# Track Specification: Teaching Personas from Internal Documents

**Track ID:** gdpe_0046_teaching_personas
**Type:** Feature Extension / Governance
**Goal:** Allow users to upload or reference organizational policy documents to "Teach" the Agentic Auditor new stakeholder personas.

## 1. Overview
This track extends the Agentic Delphi Protocol by enabling custom persona generation. Instead of relying only on the pre-defined prompt library (Nature, Treasury, etc.), users can provide text-based inputs (PDFs, Markdown, or raw text) representing their own organization's priorities. The system will use an LLM to distill these into component weightings and audit prompts.

## 2. Functional Requirements
- **Document Ingestion:** Create a utility to parse policy documents (starting with Markdown/Text).
- **Persona Distillation:** Implement logic to prompt an LLM to extract weighting preferences from the ingested text.
- **Dynamic Registry:** Allow the `AgenticAuditor` to load these custom personas alongside standard ones.
- **UI Upload:** Add a "Teach New Persona" button and text area/upload widget to the Streamlit Delphi tab.

## 3. Acceptance Criteria
- [ ] User can provide a custom policy statement in the dashboard.
- [ ] A new persona appears in the Delphi Consensus list with a custom weighting vector.
- [ ] The custom persona provides qualitative feedback in the audit trail based on its unique policy statement.
