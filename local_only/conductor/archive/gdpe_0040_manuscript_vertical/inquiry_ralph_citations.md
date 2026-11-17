# Inquiry: Automated Citation Integrity

**Track:** gdpe_0040_manuscript_vertical
**Persona:** Ralph (Deep Thinking Architect)
**Question:** Should we implement automated BibTeX validation to ensure every citation in the manuscript exists in the master .bib file?

## 1. The Citation Drift Risk
As the manuscript evolves, we add new citations (e.g., Taylor 2021). If these are not added to `context/references.bib`, the final LaTeX/Pandoc compilation will fail or have missing entries.

## 2. Technical Validation
We can implement a script that:
1. Parses `local_only/docs/manuscript_draft.md` for cite-keys (e.g., `[@taylor2021]`).
2. Parses `context/references.bib` for valid entries.
3. Reports any "Missing citations" or "Unused bib entries."

## 3. Ralph's Iterative Improvement
- **Self-Inquiry:** "Can we automate the BibTeX additions too?"
- **Answer:** We could use a tool like `pybtex` to fetch BibTeX from DOIs automatically if a missing key is detected.
- **Action:** I recommend adding a `scripts/validate_citations.py` task to the final **Archival Readiness** track (`gdpe_0043`) to ensure perfect concordance before the remote push.
