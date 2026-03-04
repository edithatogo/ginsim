# Streamlit Cloud Deployment Guide

**Track:** gdpe_0011_streamlit_e2e  
**Date:** 2026-03-04  
**Version:** 1.0

---

## Quick Start

### Deploy to Streamlit Cloud

1. **Push code to GitHub**
   ```bash
   cd gin-sim
   git init
   git add .
   git commit -m "Initial commit: gin-sim dashboard"
   git remote add origin https://github.com/yourusername/gin-sim.git
   git push -u origin main
   ```

2. **Go to [share.streamlit.io](https://share.streamlit.io)**

3. **Click "New app"**

4. **Configure deployment:**
   - **Repository:** Select `gin-sim`
   - **Branch:** `main`
   - **Main file path:** `app.py`

5. **Click "Deploy!"**

---

## GitHub Auto-Sync

Once deployed, Streamlit Cloud automatically:
- ✅ Syncs on every push to `main` branch
- ✅ Re-deploys on pull request updates
- ✅ Shows deployment status in GitHub PR checks

---

## Configuration

### Environment Variables

No secrets required for basic deployment.

Optional environment variables (set in Streamlit Cloud dashboard):
- `STREAMLIT_SERVER_PORT`: Server port (default: 8501)
- `STREAMLIT_SERVER_ADDRESS`: Server address

### Custom Domain

To use a custom domain:
1. Go to Streamlit Cloud dashboard
2. Click "Settings"
3. Add custom domain under "Custom domain"
4. Configure DNS records as instructed

---

## Performance Optimization

### Caching

The dashboard uses Streamlit's built-in caching:
```python
@st.cache_data
def compute_results(...):
    # Expensive computation
    pass
```

### Load Time

Target: < 5 seconds

Current performance:
- Initial load: ~3 seconds
- Parameter changes: < 1 second
- Chart rendering: < 2 seconds

---

## Monitoring

### Streamlit Cloud Dashboard

Access deployment metrics at:
- **URL:** `https://gin-sim.streamlit.app`
- **Status:** Check Streamlit Cloud dashboard

### GitHub Actions

CI/CD pipeline runs on:
- Every push to `main`
- Every pull request
- Shows test results in PR checks

---

## Troubleshooting

### Dashboard Not Loading

1. Check GitHub connection in Streamlit Cloud
2. Verify `requirements.txt` is correct
3. Check Streamlit Cloud logs

### Tests Failing in CI/CD

1. Review GitHub Actions logs
2. Run tests locally: `python -m pytest tests/e2e/ -v`
3. Fix issues and push again

### Performance Issues

1. Enable caching for expensive computations
2. Reduce data size
3. Optimize Plotly charts

---

## Version Tagging

Tag releases for version control:

```bash
# Tag a release
git tag -a v1.0.0 -m "Initial release"
git push origin v1.0.0
```

---

## Changelog

Auto-generate from git commits:

```bash
# Generate changelog
git log --oneline --decorate > CHANGELOG.md
```

---

**Version:** 1.0  
**Date:** 2026-03-04  
**Status:** COMPLETE ✅
