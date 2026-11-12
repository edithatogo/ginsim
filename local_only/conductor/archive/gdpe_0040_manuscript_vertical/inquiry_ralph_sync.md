# Inquiry: Bit-for-Bit Manuscript Consistency

**Track:** gdpe_0040_manuscript_vertical
**Persona:** Ralph (Deep Thinking Architect)
**Question:** How do we maintain bit-for-bit consistency between JAX engine results and manuscript claims without manual copy-pasting?

## 1. The Desynchronization Problem
Scientific manuscripts often contain dozens of numerical claims (e.g., "Testing uptake increased by 4.2%"). If the model is recalibrated, these claims become stale and invalid.

## 2. The Macro-Variable Bridge
We will implement a "Result Manifest" system:
- **Registry:** `outputs/manifest.json` contains the authoritative scalar results for every jurisdictional policy.
- **Macros:** A LaTeX style-file (`macros.tex`) or Markdown replacement script that maps keys like `\AU_BAN_UPTAKE` to `0.6152`.

## 3. Implementation Action
1. **Create `scripts/sync_manuscript_data.py`:** A script that runs the full evaluation sweep and updates a JSON manifest.
2. **Markdown Refactor:** Update the manuscript draft in `local_only/docs/manuscript.md` to use placeholders like `{{AU_BAN_UPTAKE}}`.
3. **Automation:** Add a task to the `Snakefile` or a post-run hook that automatically injects the manifest values into the manuscript.

## 4. Ralph's Iterative Improvement
- **Self-Inquiry:** "What about the charts?"
- **Answer:** Every chart in the manuscript should have a `provenance_id` in its caption that links back to the specific git commit and parameter set used to generate it.
- **Action:** Update `reporting_common.py` to include a `provenance_hash` in all result objects.
