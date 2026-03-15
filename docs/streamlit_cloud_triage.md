# Streamlit Cloud Triage Workflow

This workflow is for production issues on the deployed Streamlit Cloud app when
the public routes fail but local or CI smoke checks are green.

## 1. Download the hosted logs

Streamlit Cloud does not expose a public logs API, so log download is browser
automated through the authenticated `Manage app` UI.

One-time browser setup:

```bash
uv run --with playwright python -m playwright install chromium
```

Interactive download:

```bash
uv run --with playwright python scripts/download_streamlit_cloud_logs.py \
  --app-url https://ginsim.streamlit.app/ \
  --output-dir artifacts/streamlit_cloud_logs
```

Authenticated-state download:

```bash
uv run --with playwright python scripts/download_streamlit_cloud_logs.py \
  --app-url https://ginsim.streamlit.app/ \
  --storage-state ~/.config/streamlit-cloud/storage-state.json \
  --headless \
  --output-dir artifacts/streamlit_cloud_logs
```

If the download fails, the script writes a screenshot and HTML snapshot to the
output directory for selector repair.

## 2. Summarize the log signatures

```bash
uv run python scripts/summarize_streamlit_cloud_logs.py \
  artifacts/streamlit_cloud_logs/<downloaded-log-or-zip> \
  --json-output artifacts/streamlit_cloud_logs/latest-summary.json
```

The summary groups repeated tracebacks into distinct signatures so the next test
to add is obvious.

## 3. Turn the production error into a regression case

- Add or extend a case in [remote_app_cases.py](../tests/e2e/remote_app_cases.py).
- If the failure is route-specific, add the page/action/assertion there first.
- If the failure needs lower-level coverage, add a focused unit or AppTest case
  alongside the smoke manifest update.

## 4. Validate

```bash
uv run --with ruff ruff check src/utils/streamlit_cloud_logs.py \
  scripts/download_streamlit_cloud_logs.py \
  scripts/summarize_streamlit_cloud_logs.py \
  tests/e2e/remote_app_cases.py \
  tests/e2e/test_remote_app.py \
  tests/unit/test_streamlit_cloud_logs.py \
  tests/unit/test_remote_app_cases.py
```

```bash
uv run --with pytest --with pytest-cov python -m pytest \
  tests/unit/test_streamlit_cloud_logs.py \
  tests/unit/test_remote_app_cases.py -q --no-cov
```
