# Inquiry: The 'Reviewer-Ready' Diamond Standard

**Track:** gdpe_0043_archival_readiness
**Persona:** Ralph (Deep Thinking Architect)
**Question:** What exactly defines the 'Reviewer-Ready' standard for a research-grade repository in 2026?

## 1. The Archival Integrity Hierarchy
To satisfy Nature/Lancet reviewers, we need to prove that our results are not just correct, but **Immutable** and **Traceable**.

### Level 1: Reproducibility (The Engine)
- **Standard:** A single command (`uv run python scripts/finalize_pack.py`) must generate every figure and table in the manuscript.
- **Requirement:** 100% of dependencies must be locked in `uv.lock`.

### Level 2: Provenance (The Data)
- **Standard:** Every artifact must be stamped with a `Provenance ID` (Git SHA + Parameter Hash).
- **Requirement:** The `results_manifest.json` must be included in the public archive.

### Level 3: Transparency (The Audit)
- **Standard:** All design decisions and "Ralph Thinking" logs must be converted from `local_only` to a structured `SUPPLEMENTARY_DOCS.md` file.
- **Requirement:** The `EconomicSanityChecker` logs must show a "Clean Bill of Health" for the final run.

## 2. Implementation Action
1. **Scrub sensitive paths:** Use `scripts/provenance.py` to ensure no local file paths (e.g., staff OneDrive) remain in logs or metadata.
2. **Citation Audit:** Implement `scripts/validate_citations.py` (from Track 0040 inquiry).
3. **Consolidation:** Create `scripts/publish_pack.py` to create the final ZIP for Zenodo/Dryad.

## 3. Ralph's Iterative Improvement
- **Self-Inquiry:** "What if the reviewer wants to run the dashboard?"
- **Answer:** We should provide a `Dockerfile` that packages the Streamlit app exactly as we see it.
- **Action:** Verify and update the root `Dockerfile` to use the current `uv` environment.
