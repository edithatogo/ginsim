# Inquiry: Visual Integrity & Trace-to-Pixel Leakage

**Track:** gdpe_0037_viz_audit_e2e
**Persona:** Ralph (Deep Thinking Architect)
**Question:** How could the data be misinterpreted between JAX tracers and Streamlit state?

## 1. The Concretization Trap
JAX operates on abstract tracers during JIT. Streamlit requires concrete Python floats/integers. 
- **Risk:** If we use `float(tracer)` inside a JAX loop, it fails. If we do it *outside* (which we currently do in `pipeline.py`), it works, but we may lose precision or inadvertently convert a high-dimensional array into a single mean, masking distributional variance.

## 2. Metric Labels vs. Engine Keys
We recently added many new metrics (Redundancy, Tapering, Remoteness). 
- **Risk:** The dashboard might display "Net Social Benefit" while the engine returns `weighted_welfare`. If the `equity_weighted_toggle` is off but the label doesn't change, we create a "Linguistic Mismatch" that invalidates stakeholder trust.

## 3. Visual Scale Invariants
Radar charts and Scatter plots often use relative scaling.
- **Risk:** If the "Global Frontier" scatter plot doesn't have a fixed origin (0,0), a small difference in welfare might look like a massive jurisdictional gap due to automatic axis cropping.

## 4. Implementation Action (Audit Matrix)
I will build a map of every UI element to its source code line:
1. **Testing Uptake:** -> `src/model/module_a_behavior.py:compute_testing_uptake`
2. **Welfare Total:** -> `src/model/dcba_ledger.py:compute_dcba`
3. **Information Gap:** -> `src/model/module_d_proxy.py:compute_proxy_substitution_effect`
4. **Clinical QALYs:** -> `src/model/module_b_clinical.py:compute_clinical_outcomes`

## 5. Ralph's Iterative Improvement
- **Self-Inquiry:** "How can we prove the charts are correct to a reviewer?"
- **Answer:** We should add a "Raw Data" toggle to every chart expander that shows the exact dataframe being plotted.
- **Action:** Add `st.dataframe` visibility to the "Evidence Linkage" tab for every primary output.
