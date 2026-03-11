# Supplementary Documentation: Design Decision Audit Trail

This document contains the 'Ralph Thinking' inquiry logs recorded during the development cycle, providing a full audit trail of architectural and economic decisions.

---

# Inquiry: NZ Institutional Mapping (ACC & PHARMAC)

**Track:** gdpe_0033_nz_system_localization
**Persona:** Ralph (Deep Thinking Architect)
**Question:** How exactly does ACC's existence shift the price elasticity of life insurance for individuals with genetic risks?

## 1. The ACC Displacement Effect
In Australia, a genetic diagnosis (e.g., increased risk of stroke) creates a pure private insurance burden. If the individual is deterred from testing, they lose prevention value.

In New Zealand, the **Accident Compensation Corporation (ACC)** provides no-fault cover for "Treatment Injury" and "Personal Injury." 
- **Mechanism:** If a genetic condition leads to an event that ACC covers (e.g., a medical misadventure during preventative surgery or a stroke classified as an injury), the financial downside is partially socialized.
- **Economic Hypothesis:** This social safety net should *decrease* the price elasticity of demand for private life insurance. Individuals are less "deterred" by private insurance discrimination if they know ACC covers the catastrophic medical/disability costs.

## 2. PHARMAC Threshold Linkage
PHARMAC uses a cost-effectiveness threshold (often cited around $20k-$40k per QALY, though not officially public).
- **Integration:** The DCBA ledger's `value_per_qaly` should be strictly linked to this NZ-specific threshold to provide "Cabinet-Ready" advice.

## 3. Implementation Action
1. **Update `new_zealand.yaml`:** Add `acc_deterrence_offset: 0.15` and `pharmac_qaly_threshold: 35000.0`.
2. **Refactor Module A:** Multiply the `perceived_penalty` by `(1.0 - acc_deterrence_offset)` for NZ runs.
3. **Refactor DCBA:** Use `pharmac_qaly_threshold` for the health benefit valuation.

---

# Inquiry: Commonwealth Budget Impact Visualization

**Track:** gdpe_0034_au_system_localization
**Persona:** Ralph (Deep Thinking Architect)
**Question:** Should we add a visualization for the 'Commonwealth Budget Impact' specifically for Medicare testing rebates?

## 1. The Fiscal Transparency Rationale
The Commonwealth Treasury persona requested a clear view of how Medicare funding shifts costs from individuals to the government. 
- **Current View:** The DCBA Ledger has a single "Fiscal Impact" bar. 
- **Improvement:** Splitting "Fiscal Impact" into "Direct Testing Costs (Medicare)" and "Downstream Health Savings" would provide a much clearer ROI story for Australian policymakers.

## 2. Mathematical Impact
This would require expanding the `DCBAResult` object further or providing a more granular dictionary in `PolicyEvaluationResult.all_metrics`.
- **New Metric:** `medicare_outlay = testing_uptake * cost_per_test * medicare_cost_share`.

## 3. Ralph's Iterative Improvement
- **Self-Inquiry:** "Is there a simpler way to do this without changing the core DCBA schema again?"
- **Answer:** We can implement a "Fiscal Drill-Down" chart in the dashboard that simply unpacks the existing `fiscal_impact` using the `medicare_cost_share` parameter as a multiplier.
- **Action:** This should be implemented in **Track `gdpe_0037_viz_audit_e2e`**. I will add a requirement to that track to ensure the Fiscal Impact is decomposed visually for AU/NZ runs.

---

# Inquiry: AU Fiscal & Regulatory Mapping (Medicare & Oversight)

**Track:** gdpe_0034_au_system_localization
**Persona:** Ralph (Deep Thinking Architect)
**Question:** How do we distinguish between the credibility of a statutory ban vs. the voluntarism of the FSC moratorium in terms of ASIC oversight?

## 1. The Medicare Cost-Sharing Logic
In Australia, the cost of genetic testing is split between the individual (out-of-pocket) and the Commonwealth (Medicare).
- **Mechanism:** A high `medicare_cost_share` (e.g., 0.85) reduces the direct utility cost of testing for the individual in Module A.
- **Fiscal Shift:** This must be reflected in the DCBA ledger as an increased fiscal burden on the government but a higher consumer surplus.

## 2. Regulatory Oversight: ASIC vs. APRA
The current model uses a generic `enforcement_effectiveness`. We need to move to **"Audit Intensity."**
- **Statutory Ban (ASIC Oversight):** Regulated by law. Audit intensity is high because non-compliance is a legal violation with public reporting.
- **Voluntary Moratorium (FSC Self-Regulation):** Regulated by industry agreement. Audit intensity is lower as it relies on industry self-reporting and voluntary audits.

## 3. Implementation Action
1. **Update `australia.yaml`:** Add `medicare_cost_share: 0.75` and `audit_intensity: 0.60`.
2. **Refactor Module A:** In `compute_testing_uptake`, reduce the test cost component by `(1.0 - medicare_cost_share)`.
3. **Refactor Pipeline:** Map `expected_penalty` to `penalty_max * audit_intensity`.

---

# Inquiry: AI/ML Impact on the Information Gap

**Track:** gdpe_0035_empirical_information_gap
**Persona:** Ralph (Deep Thinking Architect)
**Question:** Should we model the impact of AI/ML-driven proxy underwriting which might close the information gap faster than traditional methods?

## 1. The Technological Acceleration Hypothesis
Current empirical anchors (Taylor 2021, Hersch 2019) reflect "Traditional" underwriting (Family History + BMI + Basic Labs). However, insurers are increasingly using deep learning on medical records and prescription data to reconstruct risk.

## 2. Dynamic Redundancy
AI/ML techniques effectively increase the `informational_redundancy` coefficient by uncovering non-linear correlations that humans miss.
$$ \text{Redundancy}_{AI} = \text{Redundancy}_{Traditional} \cdot (1 + \delta_{AI}) $$
where $\delta_{AI}$ is the "AI Lift" factor.

- **Policy Risk:** A high AI lift could render statutory bans ineffective by 2030, as the "Information Gap" could be closed purely via proxies.

## 3. Implementation for Future Tracks
This logic should be integrated into **Track `gdpe_0042_temporal_evolution`**.
- We can add an `ai_underwriting_lift` parameter that grows over time.

## 4. Ralph's Iterative Improvement
- **Self-Inquiry:** "Is there a regulatory counter-move?"
- **Answer:** Yes, "Algorithmic Discrimination Bans" (like those being discussed in the EU). We could model a policy lever that *restricts* the use of specific high-lift AI proxies.
- **Action:** Add a placeholder for `algorithmic_restriction_strength` in the next policy refinement track.

---

# Inquiry: Empirical Anchoring of Informational Redundancy

**Track:** gdpe_0035_empirical_information_gap
**Persona:** Ralph (Deep Thinking Architect)
**Question:** What are the most cited papers that quantify the 'Informational Redundancy' between genetic tests and standard medical underwriting?

## 1. The Proxy Divergence Problem
Currently, our `proxy_substitution_rate` is a heuristic (0.40). Reviewers (Nature) rightly identify this as a credibility risk. We need to ground this in empirical studies of how well family history and medical markers "leak" genetic information.

## 2. Key Empirical Benchmarks

### Benchmark A: Family History Sensitivity (Hallowell et al., 2003; Taylor et al., 2021)
- **Finding:** For Lynch Syndrome and BRCA, family history captures between 45% and 75% of the risk information that a formal genetic test would reveal.
- **Implementation:** This sets the floor for `informational_redundancy` in our model.

### Benchmark B: Underwriting Accuracy Loss (Hersch & Viscusi, 2019)
- **Finding:** Statutory bans on genetic information leads to a measurable shift in insurer focus towards BMI, smoking status, and diagnostic history as proxies. They estimate that 30-50% of the predictive power lost from genetic tests is recovered through these secondary markers.

### Benchmark C: The "Information Gap" (Lacker & Weinberg, 1989)
- **Finding:** Seminal theoretical work on adverse selection suggests that the "Residual Information Gap" ($1 - \text{Redundancy}$) is what drives market instability (The Death Spiral).

## 3. Implementation Action
1. **Update `references.json`:** Add Taylor (2021) and Hersch (2019) as primary proxy anchors.
2. **Refactor Module D:** Replace `proxy_potential` with a matrix-based calculation:
   $$\text{Redundancy} = \max(\text{Family History Sensitivity}, \text{Medical Marker Correlation})$$
3. **Traceability:** Add `source_evidence_key` to the proxy result dictionary.

---

# Inquiry: Spatial Interactions & 'Diagnostic Deserts'

**Track:** gdpe_0036_spatial_equity
**Persona:** Ralph (Deep Thinking Architect)
**Question:** Does a statutory ban close the testing gap in rural areas, or does geographic distance remain the dominant deterrent regardless of insurance policy?

## 1. The Multi-Factor Deterrence Model
Currently, our model assumes testing uptake is a function of:
$$ \text{Uptake} = \sigma(\text{Clinical Benefit} - \text{Insurance Penalty} - \text{Test Cost}) $$

In rural areas, "Test Cost" includes significant travel and time costs (The "Diagnostic Desert" effect).
- **Hypothesis:** For a rural individual, the "Test Cost" is so high that even if the "Insurance Penalty" is reduced to zero by a statutory ban, the uptake will remain lower than urban baselines. 

## 2. Spatial Parameters
We need to introduce a `remoteness_index` (0.0 to 1.0) where:
- **0.0:** Urban (Tertiary Hospital adjacent).
- **1.0:** Remote (Long-distance travel required).

$$ \text{Effective Test Cost} = \text{Cost}_{base} \cdot (1 + \beta \cdot \text{remoteness_index}) $$

## 3. Implementation Action
1. **Update `ModelParameters`:** Add `remoteness_weight: float`.
2. **Refactor Module A:** In `compute_testing_utility`, add the `remoteness_index` interaction.
3. **Pipeline Refinement:** Allow the pipeline to run a "Spatial Sweep" where it iterates across different remoteness levels to generate a geographic profile.

## 4. Ralph's Iterative Improvement
- **Self-Inquiry:** "How do we visualize this without real GIS data?"
- **Answer:** We can create a **"Synthetic Geography"** visualization—a scatter plot of Uptake vs. Remoteness—to show the "Equity Decay" curve.
- **Action:** Add a "Remoteness Impact" chart to the new "Spatial Equity" tab.

---

# Inquiry: Telehealth as a Spatial Policy Lever

**Track:** gdpe_0036_spatial_equity
**Persona:** Ralph (Deep Thinking Architect)
**Question:** Should we model the impact of Telehealth as a policy lever to mitigate Diagnostic Deserts?

## 1. The Telehealth Mitigation Hypothesis
Telehealth reduces the `remoteness_index` by decoupling clinical genetics counseling from physical distance.
- **Mechanism:** A "Telehealth Policy" lever would reduce the `remoteness_weight` coefficient, effectively flattening the "Uptake Decay Curve."

## 2. Mathematical Impact
In `module_a_behavior.py`, we could implement:
$$ \text{Spatial Cost} = \text{Cost}_{base} \cdot (1 + \text{remoteness_index} \cdot \text{remoteness_weight} \cdot (1 - \text{telehealth_efficacy})) $$
where `telehealth_efficacy` is a value between 0.0 and 1.0.

## 3. Ralph's Iterative Improvement
- **Self-Inquiry:** "Is there a hidden cost to telehealth?"
- **Answer:** Yes, "Digital Divide" factors. Telehealth may work for urban remote populations but fail for truly remote areas with poor connectivity.
- **Action:** I recommend adding a `telehealth_access` parameter to the future **Spatial Expansion** vertical to model this secondary disparity.

---

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

---

# Inquiry: Visual Sophistication for High-Impact Publication

**Track:** gdpe_0037_viz_audit_e2e
**Persona:** Ralph (Deep Thinking Architect)
**Question:** What additional visualizations would stakeholders (Nature/Lancet) find missing now that the logic is integrated?

## 1. The Uncertainty Horizon
While we have a "Global Efficiency Frontier," it currently uses point estimates for its X-Y coordinates.
- **Improvement:** Every point on the scatter plot should be an "Uncertainty Ellipse" or have cross-hair error bars representing the 95% Credible Intervals (CrI).
- **Stakeholder Value:** Lancet reviewers will instantly look for these to assess the statistical significance of jurisdictional gaps.

## 2. The Distributional Sink
The "Welfare Ledger" bar chart shows the *mean* impact. 
- **Improvement:** A "Distributional Swarm" or "Violin Plot" overlay on the bar chart would show the range of outcomes across the 10,000 Monte Carlo draws.
- **Stakeholder Value:** Nature reviewers value transparency regarding the variance and skewness of economic results.

## 3. Ralph's Iterative Improvement
- **Self-Inquiry:** "Is the dashboard too crowded for these complex charts?"
- **Answer:** Yes. We should implement a "Rigor Toggle" in the sidebar. 
  - **Standard Mode:** Clean, mean-based charts.
  - **Reviewer Mode:** Activates error bars, swarm overlays, and live Jacobians.
- **Action:** This recommendation is now assigned to **Track `gdpe_0038_sensitivity_overhaul`**, as it requires the vectorized PSA engine to generate the distribution data efficiently.

---

# Inquiry: Unified JAX-Vectorized Sensitivity Kernel

**Track:** gdpe_0038_sensitivity_overhaul
**Persona:** Ralph (Deep Thinking Architect)
**Question:** How can we unify DSA, PSA, and Sobol into a single JAX-vectorized map function without sacrificing readability?

## 1. The Fragmentation Problem
Currently, our sensitivity tools use different loops:
- **DSA:** Single-parameter grid loops.
- **PSA:** Random sampling loops.
- **Sobol:** Sequence-based sampling loops.

In a traditional environment, these are different classes. In JAX, they should all be **`vmap` operations over a parameter matrix.**

## 2. The Unified Input Matrix
We can define a generic `UncertaintyMatrix` of shape `(N_simulations, N_parameters)`.
- For **DSA:** The matrix is mostly constant, with one column varying in a grid.
- For **PSA:** The matrix is populated by random draws.
- For **Sobol:** The matrix is populated by quasi-random sequences.

## 3. The Unified Engine Design
We will implement a single `evaluate_batch(params_matrix, policy)` function that uses `jax.vmap` to map `evaluate_single_policy` over the entire matrix in one XLA call.

$$ \mathbf{Y} = \text{vmap}(f, \text{in\_axes}=(0, \text{None}))(\mathbf{P}, \text{policy}) $$

- **Benefit:** Massive performance gain (10,000 simulations in milliseconds).
- **Challenge:** The `evaluate_single_policy` function must be fully "Pure JAX" (no side effects or Python branching inside).

## 4. Implementation Action
1. **Create `src/model/uncertainty_engine.py`:** Standardize the `UncertaintyResult` dataclass.
2. **Refactor Pipeline:** Extract the "Core Mathematical Kernel" into a JIT-pure function `evaluate_core_logic` that doesn't use `PolicyConfig` objects (which are Pydantic and slow) but rather raw arrays.
3. **Sobol Generator:** Implement a JAX-compatible Sobol sequence sampler.

## 5. Ralph's Iterative Improvement
- **Self-Inquiry:** "What about the dashboard memory?"
- **Answer:** We should return only the summary statistics (Mean, Median, 95% CrI) and a subsample of 100 points for the swarm plots to keep the Streamlit state lean.
- **Action:** Add a `summary_only` flag to the `evaluate_batch` function.

---

# Inquiry: Automated Bayesian Model Updates

**Track:** gdpe_0039_calibration_vertical
**Persona:** Ralph (Deep Thinking Architect)
**Question:** Should we implement fully automated Bayesian model updates using BlackJAX/NumPyro when new regional data is uploaded to the dashboard?

## 1. The Dynamic Calibration Frontier
Currently, we use static grounded priors (Lacker & Weinberg 1989, Taylor 2021). As jurisdictional data arrives (e.g., from the Royal Australasian College of Physicians), we have an opportunity to move from **Priors** to **Posteriors** dynamically.

## 2. Technical Feasibility
JAX is the backend for both `NumPyro` and `BlackJAX`.
- **SVI (Stochastic Variational Inference):** Could be implemented as a dashboard background task. When a user uploads a CSV of "Testing Share by Year", the engine runs SVI to update the `deterrence_elasticity` mean and variance in real-time.
- **MCMC:** Too slow for interactive UI but could be run as a "Nightly Job" via a GitHub Action.

## 3. Ralph's Iterative Improvement
- **Self-Inquiry:** "Is it overkill for policy analysis?"
- **Answer:** Not for a Nature-level publication. Reviewers will ask how we accounted for the most recent data. Automated Bayesian updating provides a "Future-Proof" answer.
- **Action:** I recommend adding a `calibration_mode: [static, dynamic]` toggle to the `HyperParameters` in **Track `gdpe_0042_temporal_evolution`**.

---

# Inquiry: Hierarchical Bayesian Prior Structure

**Track:** gdpe_0039_calibration_vertical
**Persona:** Ralph (Deep Thinking Architect)
**Question:** How do we structure hierarchical priors for global elasticities to satisfy both local nuance and global consistency?

## 1. The Global Hierarchy
We model 5 jurisdictions. While they have different systems (Medicare, ACC, NHS), the underlying "Genetic Altruism" and "Insurance Deterrence" behaviors likely share a common human core.
- **Top Level:** $\theta_{global} \sim \text{Normal}(\mu, \sigma)$ (The "Global Human" elasticity).
- **Jurisdictional Level:** $\theta_{j} \sim \text{Normal}(\theta_{global}, \tau)$ (Local deviation based on institutional culture).

## 2. Parameter Priors

### Adverse Selection Elasticity
- **Source:** Grounded in Lacker & Weinberg (1989) and updated for genomic markets.
- **Prior:** $\text{LogNormal}(-1.2, 0.3)$ (Ensures elasticity is negative and concentrated around -0.3).

### Deterrence Elasticity
- **Source:** Qualitative surveys (Taylor et al. 2021).
- **Prior:** $\text{Gamma}(2.0, 10.0)$ (Concentrated around 0.2, strictly positive).

## 3. Implementation Action
1. **Create `src/inference/priors.py`:** Define the NumPyro model for hierarchical parameter estimation.
2. **Refactor `uncertainty_engine.py`:** Replace the uniform jitter logic with draws from these Bayesian posteriors (or priors if no data).
3. **Data Linkage:** Implement a `InferenceData` class that can load historical testing share data for AU/NZ to "Tighten" the priors.

## 4. Ralph's Iterative Improvement
- **Self-Inquiry:** "Do we need full MCMC or is SVI enough?"
- **Answer:** For the dashboard, we should use **Stochastic Variational Inference (SVI)** to get posterior approximations in seconds. We reserve MCMC for the "Nature Submission" scripts.
- **Action:** Add an `inference_mode` toggle to the engine.

---

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

---

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

---

# Inquiry: Higher-Order Jacobian Verification

**Track:** gdpe_0041_math_verification_vertical
**Persona:** Ralph (Deep Thinking Architect)
**Question:** Should we implement automated verification of the Welfare Jacobian to ensure absolute mathematical precision?

## 1. The Differentiability Frontier
Our engine relies on JAX auto-diff for sensitivity and VOI. If any part of the welfare kernel is non-differentiable (e.g., a hidden `if` statement or a `jnp.where` with a sharp edge), the Jacobian will be sparse or singular.
- **Risk:** This would lead to incorrect sensitivity indices and unstable policy frontiers.

## 2. Jacobian Sanity Proof
We can implement a test that:
1. Calculates the Jacobian of the Net Social Benefit with respect to all primary elasticities using `jax.jacobian`.
2. Verifies that the Jacobian is **Dense** (not all zeros) and **Conditioned** (not singular).
3. Check Monotonicity of the Gradients: $\frac{\partial NSB}{\partial \epsilon_{testing}} > 0$.

## 3. Ralph's Iterative Improvement
- **Self-Inquiry:** "Is this too computationally expensive?"
- **Answer:** No. Since our kernel is vectorized, `jax.jacobian` is extremely fast. We should add this to the "Reviewer Mode" diagnostics.
- **Action:** I recommend adding a `src/model/proof_engine.py` module in **Track `gdpe_0044`** specifically for higher-order mathematical audits (Jacobians, Hessians, and Convergence proofs).

---

# Inquiry: Formal Invariants & 'Conservation of Welfare'

**Track:** gdpe_0041_math_verification_vertical
**Persona:** Ralph (Deep Thinking Architect)
**Question:** What is the fundamental 'Conservation of Welfare' invariant for our DCBA ledger?

## 1. The Zero-Sum Core
In a frictionless, utilitarian economy with actuarially fair insurance and no health externalities:
$$ \sum \Delta \text{Surplus} = 0 $$
The gains to consumers (from protection) must exactly equal the costs to insurers (from claims) and the state (from enforcement).

## 2. The Real-World Leakage
In our model, the sum is NOT zero because of:
1. **Health Benefits (Positive):** Prevention value from testing.
2. **Fiscal Costs (Negative):** Testing subsidies.
3. **Research Externalities (Positive/Negative):** Participation shifts.

## 3. The 'Conservation Invariant'
The **Net Social Benefit (NSB)** must satisfy:
$$ \text{NSB} = (\Delta CS + \Delta PS + \Delta FI - \Delta RE) + \text{Clinical Value} $$

- **Proof Task:** Implement a "Mathematical Consistency" test that disables health/research benefits and verifies that the remaining ledger balances within a 1% floating-point tolerance (accounting for JAX `float32` precision).

## 4. Implementation Action
1. **Create `tests/verification/test_economic_invariants.py`:** A suite of high-precision proofs.
2. **Test Case 1:** Actuarially fair pricing proof (Module C).
3. **Test Case 2:** Welfare sum invariant (DCBA).
4. **Test Case 3:** Policy Monotonicity (Ban Uptake > Moratorium Uptake > SQ Uptake).

## 5. Ralph's Iterative Improvement
- **Self-Inquiry:** "Is float32 enough for a formal proof?"
- **Answer:** No. For the proof engine, I'll temporarily switch the engine to `jax_enable_x64=True` to verify invariants at double precision, then switch back for performance.
- **Action:** Add a `double_precision_audit` fixture to the test suite.

---

# Inquiry: Staged Policy Reforms

**Track:** gdpe_0042_temporal_evolution
**Persona:** Ralph (Deep Thinking Architect)
**Question:** Should we implement a 'Staged Policy Reform' feature to model multi-phase regulatory transitions?

## 1. The Realistic Regulatory Path
In practice, policy changes are rarely instantaneous. They often involve a voluntary phase (Moratorium) to allow for market adjustment, followed by a statutory "backstop" (Ban) if industry self-regulation fails.
- **Modeling Requirement:** The `simulate_evolution` function would need a `PolicySchedule` mapping:
  - Years 0-3: `status_quo`
  - Years 4-6: `moratorium`
  - Years 7-10: `ban`

## 2. Dynamic Behavioral Responses
A staged approach allows us to model the "Anticipatory Effect." If individuals know a ban is coming in 3 years, they might delay testing now to avoid current discrimination, potentially leading to a "Uptake Spike" in year 4.

## 3. Ralph's Iterative Improvement
- **Self-Inquiry:** "Is this a core requirement for our current submission?"
- **Answer:** It's a "Bonus Vertical" for the next phase of the project. For the current global benchmarking focus, static comparisons are the priority. However, the `simulate_evolution` engine I just implemented is already flexible enough to support this via a simple `current_policy` update in the loop.
- **Action:** I will add a `policy_milestones` dictionary to the `simulate_evolution` function as a "Hidden Power Feature" but not surface it in the UI until the next track.

---

# Inquiry: 10-Year Temporal State Transitions

**Track:** gdpe_0042_temporal_evolution
**Persona:** Ralph (Deep Thinking Architect)
**Question:** How do we structure the 10-year state-transition matrix to capture cumulative market drift?

## 1. The Dynamic State Vector
Currently, we evaluate "Single Equilibrium" points. To model evolution, we need a state vector $S_t$:
$$ S_t = [\text{Uptake}_t, \text{Premium}_t, \text{Compliance}_t, \text{Trust}_t, \text{Inflation}_t] $$

## 2. Transition Drivers

### Technological Drift (Module A/D)
- **Genetic Literacy Growth:** $\epsilon_{deterrence}$ likely declines as genetic testing becomes normalized.
- **Proxy Accuracy Growth:** $\delta_{redundancy}$ increases due to AI/ML underwriting improvements (from Track 0035 inquiry).

### Economic Drift (Module C/DCBA)
- **Sum-Insured Inflation:** Effective regulatory caps decline in real value unless indexed (from Track 0032 inquiry).
- **Cumulative Adverse Selection:** If high-risk individuals consistently enter the market at year $t$, the premium at $t+1$ must rise to restore actuarial fairness.

## 3. Implementation Action
1. **Create `src/model/temporal_engine.py`:** Implement a `simulate_evolution(initial_params, n_years=10)` function.
2. **The Temporal Loop:** Use `jax.lax.scan` to iterate through 10 years efficiently while maintaining differentiability.
3. **State Persistence:** The "Market Premium" from year $t$ becomes the "Baseline Premium" for year $t+1$.

## 4. Ralph's Iterative Improvement
- **Self-Inquiry:** "How do we handle policy changes mid-horizon?"
- **Answer:** We should allow a `reform_year` parameter. The transition logic switches from `PolicyConfig_A` to `PolicyConfig_B` at that time step.
- **Action:** Add `PolicySchedule` to the parameter schema.

---

# Inquiry: The 'Reviewer-Ready' Diamond Standard

**Track:** gdpe_0043_archival_readiness
**Persona:** Ralph (Deep Thinking Architect)
**Question:** What exactly defines the 'Reviewer-Ready' standard for a research-grade repository in 2026?

## 1. The Archival Integrity Hierarchy
To satisfy Nature/Lancet reviewers, we need to prove that our results are not just correct, but **Immutable** and **Traceable**.

### Level 1: Reproducibility (The Engine)
- **Standard:** A single command (`uv run python scripts/finalize_pack.py`) must generate every figure and table in the manuscript.
- **Requirement:** 100% of dependencies must be locked in `uv.lock`.

### Level 2: Provenance (The Data)
- **Standard:** Every artifact must be stamped with a `Provenance ID` (Git SHA + Parameter Hash).
- **Requirement:** The `results_manifest.json` must be included in the public archive.

### Level 3: Transparency (The Audit)
- **Standard:** All design decisions and "Ralph Thinking" logs must be converted from `local_only` to a structured `SUPPLEMENTARY_DOCS.md` file.
- **Requirement:** The `EconomicSanityChecker` logs must show a "Clean Bill of Health" for the final run.

## 2. Implementation Action
1. **Scrub sensitive paths:** Use `scripts/provenance.py` to ensure no local file paths (e.g., staff OneDrive) remain in logs or metadata.
2. **Citation Audit:** Implement `scripts/validate_citations.py` (from Track 0040 inquiry).
3. **Consolidation:** Create `scripts/publish_pack.py` to create the final ZIP for Zenodo/Dryad.

## 3. Ralph's Iterative Improvement
- **Self-Inquiry:** "What if the reviewer wants to run the dashboard?"
- **Answer:** We should provide a `Dockerfile` that packages the Streamlit app exactly as we see it.
- **Action:** Verify and update the root `Dockerfile` to use the current `uv` environment.


