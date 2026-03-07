# Publish pack

`publish_pack.py` turns a meta pipeline run directory into a reporting pack:
- POLICY_BRIEF.md
- POLICY_BRIEF.docx (if python-docx available)
- POLICY_BRIEF.pdf (if reportlab available)
- figures (PNG)
- figure captions (`*_caption.md`)

The pack now uses:
- data-driven narrative text from the reporting bundle rather than static template prose;
- canonical policy labels;
- path-safe run identifiers and manifest excerpts rather than local filesystem paths;
- premium indices and long-run net-benefit labels that match the active dashboard/reporting surfaces.
- manuscript-facing figure outputs with paired caption files for each publication-facing figure.

Related reviewer-facing inventory:
- `docs/MANUSCRIPT_ASSET_INVENTORY.md`
- `docs/SUBMISSION_GAP_REGISTER.md`

## Usage
First run the meta pipeline:
```bash
python -m scripts.run_meta_pipeline --n_draws 500
```

Then generate a publish pack:
```bash
python -m scripts.publish_pack --meta_dir outputs/runs/meta_pipeline/<timestamp>
```

Outputs are written to:
`<meta_dir>/publish_pack/`
