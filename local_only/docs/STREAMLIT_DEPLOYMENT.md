# Streamlit Dashboard Deployment Guide

**Track:** gdpe_0009_streamlit_dashboard
**Date:** 2026-03-03
**Version:** 1.0

---

## Overview

This guide explains how to deploy the Genetic Discrimination Policy Dashboard to Streamlit Cloud with GitHub auto-sync.

---

## Quick Start

### 1. Local Testing

```bash
cd streamlit_app
pip install -r requirements.txt
streamlit run app.py
```

### 2. Deploy to Streamlit Cloud

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect GitHub repository
4. Select `streamlit_app/app.py` as main file
5. Deploy

---

## Configuration

### GitHub Auto-Sync

The dashboard automatically syncs with GitHub:
- Push to `main` branch → Auto-deploy
- Pull requests → Preview deployment

### Environment Variables

No secrets required for basic deployment.

For advanced features:
- `STREAMLIT_SERVER_PORT`: Server port (default: 8501)
- `STREAMLIT_SERVER_ADDRESS`: Server address (default: localhost)

---

## Performance Optimization

### Caching

```python
@st.cache_data
def load_model():
    # Model loading code
    pass
```

### Lazy Loading

```python
if st.sidebar.button("Run Analysis"):
    # Expensive computation
    pass
```

---

## User Guide

### Sidebar Controls

- **Policy Regime**: Select policy to evaluate
- **Baseline Testing Uptake**: Adjust baseline probability
- **Deterrence Elasticity**: Adjust sensitivity to penalties
- **Moratorium Effect**: Adjust policy effectiveness

### Tabs

1. **Results**: Key metrics and detailed tables
2. **Charts**: Interactive visualizations
3. **Comparison**: Side-by-side policy comparison
4. **Documentation**: Model documentation and references

---

## Maintenance

### Updating Model

1. Update model in `src/model/`
2. Import in `streamlit_app/app.py`
3. Push to GitHub → Auto-deploy

### Monitoring

- Streamlit Cloud dashboard
- GitHub Actions logs
- User feedback

---

## Troubleshooting

### Dashboard Not Loading

1. Check GitHub connection
2. Verify `requirements.txt`
3. Check Streamlit Cloud logs

### Slow Performance

1. Enable caching
2. Reduce data size
3. Optimize visualizations

---

**Version:** 1.0
**Date:** 2026-03-03
**Status:** Complete ✅
