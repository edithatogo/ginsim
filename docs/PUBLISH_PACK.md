# Publish pack

`publish_pack.py` turns a meta pipeline run directory into a ready-to-share pack:
- POLICY_BRIEF.md
- POLICY_BRIEF.docx (if python-docx available)
- POLICY_BRIEF.pdf (if reportlab available)
- figures (PNG)

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
