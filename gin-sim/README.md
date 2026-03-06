# gin-sim

`gin-sim/` is the deployment wrapper for the main Streamlit dashboard in [`streamlit_app/`](../streamlit_app).

## Classification

- Source of truth: [`streamlit_app/app.py`](../streamlit_app/app.py)
- Deployment entrypoint: [`gin-sim/app.py`](./app.py)
- Maintenance rule: do not implement dashboard features independently inside `gin-sim/app.py`

The wrapper exists so Streamlit Cloud can continue to use `gin-sim/app.py` as its entrypoint while the actual UI, page modules, and model wiring stay centralized in the main repository app.

## Local Run

From the repository root:

```bash
pip install -r gin-sim/requirements.txt
streamlit run gin-sim/app.py
```

This launches the same dashboard served by [`streamlit_app/app.py`](../streamlit_app/app.py).

## Smoke Suite

Minimum local dashboard smoke suite:

```bash
pytest tests/e2e/test_dashboard.py
pytest tests/unit/test_dashboard_helpers.py tests/unit/test_gin_sim_wrapper.py
```

Optional remote deployment smoke check:

```bash
GDPE_REMOTE_DASHBOARD_URL=https://ginsim.streamlit.app pytest tests/e2e/test_remote_app.py -m slow
```

The remote check is opt-in because Streamlit Cloud wake-up times and deployment state are external to the local repository.
