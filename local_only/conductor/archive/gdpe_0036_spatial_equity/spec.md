# Track Specification: Spatial Equity & 'Diagnostic Deserts'

**Track ID:** gdpe_0036_spatial_equity
**Type:** Feature / Public Health
**Goal:** Map the geographic distribution of testing access ("Diagnostic Deserts") and visualize spatial welfare impacts across AU and NZ.

## 1. Overview
The NZ Ministry of Health persona identified "Diagnostic Deserts" as a critical policy concern. This track adds a spatial dimension to the evaluation, showing how discrimination policy might disproportionately affect rural or remote populations with limited access to clinical genetics services.

## 2. Functional Requirements
- **Spatial Meta-data:** Add `remoteness_index` to individual characteristics in `module_a_behavior.py`.
- **Welfare Heatmapping:** Implement a geographic visualization layer in Streamlit (using Mapbox/Folium or Plotly Chloropleth) to show welfare impacts by region.
- **Access Constraints:** Model the "interaction" between insurance fear and physical distance to testing centers.

## 3. Acceptance Criteria
- [ ] New "Spatial Equity" tab in the dashboard.
- [ ] Interactive maps showing testing uptake by remoteness index.
- [ ] Verification that "Diagnostic Desert" effects are mathematically distinct from "Insurance Deterrence" effects in the JAX engine.
