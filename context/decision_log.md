# Decision Log

This log tracks key modelling, methodological, and infrastructure decisions with rationale and evidence.

**Usage:** For single-author research, document decisions when:
- Choosing between multiple viable options
- Setting key model parameters or structures  
- Making assumptions that affect results
- Responding to unexpected findings

---

## Decision tracking template

```markdown
## Decision: [Title]
- **Date:** YYYY-MM-DD
- **Track:** [Track ID if applicable]
- **Category:** [Infrastructure/Methods/Policy/Evidence/Code]
- **Context:** Why this decision was needed
- **Options considered:** 
  - Option A: [description]
  - Option B: [description]
- **Decision:** [What was chosen]
- **Rationale:** Why this option was selected
- **Evidence:** Links to data, literature, or analysis
- **Impact:** What this affects in the model
- **Alternatives rejected:** Why other options were not chosen
- **Review date:** [When this should be revisited]
```

---

## Decisions

## Decision: Modular Bayesian decision analysis framework
- **Date:** 2026-03-02
- **Track:** gdpe_0001_bootstrap
- **Category:** Methods
- **Context:** Selecting the core modelling approach for policy evaluation
- **Options considered:**
  - Option A: Traditional deterministic CEA with one-way sensitivity
  - Option B: Full probabilistic Bayesian decision analysis with VOI
  - Option C: Hybrid (deterministic base + probabilistic VOI)
- **Decision:** Option B — Full probabilistic Bayesian decision analysis
- **Rationale:** 
  - Genetic discrimination policy has high uncertainty across multiple parameters
  - Decision makers need explicit uncertainty quantification (EVPI/EVPPI)
  - Bayesian framework allows evidence synthesis from heterogeneous sources
  - JAX/XLA enables scalable computation for multi-module propagation
- **Evidence:** 
  - Claxton K. The philosophical foundations of cost-effectiveness analysis.
  - Strong M et al. Probabilistic sensitivity analysis in NICE technology appraisals.
- **Impact:** All modelling modules (A-F), VOI computations, publish pack outputs
- **Alternatives rejected:** 
  - Option A: Insufficient for high-uncertainty policy context
  - Option C: Inconsistent treatment of uncertainty
- **Review date:** N/A (foundational decision)

---

## Decision: JAX-first stack over PyTorch/TensorFlow
- **Date:** 2026-03-02
- **Track:** gdpe_0001_bootstrap
- **Category:** Code/Infrastructure
- **Context:** Selecting the computational backend
- **Options considered:**
  - Option A: PyTorch + Pyro
  - Option B: JAX + NumPyro + BlackJAX
  - Option C: Stan/CmdStanPy
- **Decision:** Option B — JAX ecosystem
- **Rationale:**
  - JAX provides XLA compilation for faster MCMC/simulation
  - NumPyro + BlackJAX offer state-of-the-art samplers (NUTS, HMC, SMC)
  - Functional programming paradigm suits reproducible research
  - Better suited for research laptop deployment (lighter than PyTorch)
- **Evidence:** 
  - NumPyro documentation and benchmarks
  - BlackJAX paper (2023)
- **Impact:** All inference code, computational performance, dependency stack
- **Alternatives rejected:**
  - PyTorch: Heavier, less suited for MCMC
  - Stan: Slower for high-dimensional models, less flexible
- **Reviewer:** Self-directed
- **Review date:** N/A
- **Reflexive notes:** I have more experience with PyTorch, but invested time learning JAX for this project. This was a genuine best-choice decision, not convenience-driven.

---

## Decision: Australia and NZ as initial jurisdictions
- **Date:** 2026-03-02
- **Track:** gdpe_0001_bootstrap
- **Category:** Policy
- **Context:** Defining scope for comparative policy analysis
- **Options considered:**
  - Option A: Single jurisdiction (Australia only)
  - Option B: Australia + New Zealand comparative
  - Option C: Multi-country (AU, NZ, UK, Canada)
- **Decision:** Option B — AU + NZ comparative
- **Rationale:**
  - Both jurisdictions have active policy debates on genetic discrimination
  - Different policy approaches (moratorium vs legislative proposals)
  - Manageable scope for initial implementation
  - Personal research context and data access considerations
- **Evidence:** 
  - Australian Financial Services Council moratorium (2019-2024)
  - NZ Human Rights Commission genetic discrimination inquiries
- **Impact:** Config structure, evidence registers, publish pack design
- **Alternatives rejected:**
  - Option A: Too narrow; comparative value significant
  - Option C: Scope creep for initial implementation
- **Reviewer:** Self-directed
- **Review date:** N/A
- **Reflexive notes:** My location (NZ) and existing AU collaborations influenced this. This is appropriate given the research context, but I should acknowledge the insider perspective may miss external validity issues.

---

## Decision: Life insurance as primary domain
- **Date:** 2026-03-02
- **Track:** gdpe_0001_bootstrap
- **Category:** Policy
- **Context:** Selecting the insurance product focus
- **Options considered:**
  - Option A: Life insurance only
  - Option B: Life + disability + trauma (multi-product)
  - Option C: Include health/income protection
- **Decision:** Option A — Life insurance focus (with scaffolding for extension)
- **Rationale:**
  - Life insurance is the primary concern in genetic discrimination debates
  - Clearest adverse selection mechanism (death benefit pricing)
  - Data availability considerations
  - Keep initial scope tractable
- **Evidence:** 
  - Policy debates focus on life insurance
  - FSC moratorium covers life insurance products
- **Impact:** Module C structure, calibration targets, data requirements
- **Alternatives rejected:**
  - Option B/C: Scope expansion without proportional insight gain
- **Reviewer:** Self-directed
- **Review date:** After Phase 3 (may extend based on findings)
- **Reflexive notes:** This is the standard focus in literature, so following convention. Acknowledge this may miss important interactions (e.g., disability insurance often more relevant for genetic conditions).

---

## Decision: MIT License for code, CC-BY for outputs
- **Date:** 2026-03-03
- **Track:** gdpe_0002_evidence_anchoring
- **Category:** Infrastructure
- **Context:** Selecting open source licenses for research infrastructure
- **Options considered:**
  - Option A: MIT (code) + CC-BY (outputs)
  - Option B: GPL-3.0 (code) + CC-BY-NC (outputs)
  - Option C: Apache-2.0 (code) + CC0 (outputs)
- **Decision:** Option A — MIT + CC-BY
- **Rationale:**
  - MIT: Maximizes adoption and reuse; compatible with most licenses
  - CC-BY: Requires attribution; allows commercial use (appropriate for public policy research)
  - Aligns with funder open access requirements
- **Evidence:** 
  - Open Source Initiative license comparisons
  - University open access policy
- **Impact:** All code and documentation outputs
- **Alternatives rejected:**
  - GPL-3.0: Too restrictive for research collaboration
  - CC-BY-NC: "Non-commercial" creates ambiguity for policy use
  - CC0: No attribution requirement inappropriate for academic work
- **Reviewer:** Self-directed
- **Review date:** N/A
- **Reflexive notes:** Chose permissive licensing deliberately to encourage policy uptake. Some might argue for copyleft (GPL) to ensure improvements are shared back, but I prioritize adoption over reciprocity in this context.

---

## Decision: GRADE framework adaptation for evidence quality
- **Date:** 2026-03-03
- **Track:** gdpe_0002_evidence_anchoring
- **Category:** Methods/Evidence
- **Context:** Need systematic approach to grade evidence quality for prior conversion
- **Options considered:**
  - Option A: Adapt GRADE framework (healthcare evidence)
  - Option B: Create custom quality rubric
  - Option C: Use existing modelling-specific frameworks (ISPOR-SMDM)
- **Decision:** Option A — Adapt GRADE framework
- **Rationale:**
  - GRADE is well-established and widely understood in health economics
  - Provides clear downgrade/upgrade criteria
  - Familiar to target audience (HTA bodies, policymakers)
  - Can be adapted for modelling context
- **Evidence:** 
  - Guyatt GH et al. GRADE: An emerging consensus. BMJ. 2008
  - ISPOR-SMDM good practices (as supplementary guidance)
- **Impact:** Evidence registers, prior conversion, transparency
- **Alternatives rejected:**
  - Option B: Reinventing wheel; less credibility
  - Option C: ISPOR-SMDM focuses on model structure, not evidence quality
- **Reviewer:** Self-directed
- **Review date:** After Phase 2 (test in practice)
- **Reflexive notes:** I'm familiar with GRADE from clinical work, which influenced this choice. Acknowledge potential bias, but GRADE genuinely fits better than alternatives for this use case.

---

## Decision: YAML format for evidence registers
- **Date:** 2026-03-03
- **Track:** gdpe_0002_evidence_anchoring
- **Category:** Infrastructure/Methods
- **Context:** Selecting format for structured evidence documentation
- **Options considered:**
  - Option A: YAML (human-readable structured format)
  - Option B: JSON (machine-readable)
  - Option C: Markdown tables (simple but limited)
  - Option D: SQLite database (structured but complex)
- **Decision:** Option A — YAML
- **Rationale:**
  - Human-readable and editable (unlike JSON)
  - Structured enough for programmatic access
  - Compatible with existing config infrastructure
  - Supports comments and documentation inline
- **Evidence:** 
  - Existing use in configs/ directory
  - Python PyYAML support
- **Impact:** Evidence register structure, future automation
- **Alternatives rejected:**
  - JSON: Poor human readability
  - Markdown: Insufficient structure for complex data
  - SQLite: Overkill; harder to version control
- **Reviewer:** Self-directed
- **Review date:** N/A
- **Reflexive notes:** YAML is my default for structured configs. This is partly habit, but genuinely the best fit for this use case.

---

## Decision: Phase review gates with automated validation
- **Date:** 2026-03-03
- **Track:** gdpe_0002_evidence_anchoring
- **Category:** Infrastructure/Workflow
- **Context:** Ensuring quality and consistency across research phases
- **Options considered:**
  - Option A: Manual review at end of each phase
  - Option B: Automated validation gates (reference checking, code quality)
  - Option C: Hybrid (automated checks + human sign-off)
- **Decision:** Option C — Hybrid with automated checks
- **Rationale:**
  - Automated checks catch objective issues (reference completeness, code errors)
  - Human review needed for subjective quality (evidence grading, model validity)
  - Reduces cognitive load by handling routine checks automatically
  - Creates audit trail for reproducibility
- **Evidence:** 
  - Software engineering best practices (CI/CD)
  - Research reproducibility frameworks
- **Impact:** All future phases; workflow enforcement
- **Alternatives rejected:**
  - Option A: Too error-prone; no audit trail
  - Option B: Cannot assess research quality automatically
- **Reviewer:** Self-directed
- **Review date:** After Phase 3 (evaluate effectiveness)
- **Reflexive notes:** This reflects my clinical background where checklists + expert judgment both matter. May be over-engineering for solo research, but builds good habits and supports future collaboration.

---

## Decision: Reference validation pipeline (custom script)
- **Date:** 2026-03-03
- **Track:** gdpe_0002_evidence_anchoring
- **Category:** Infrastructure/Code
- **Context:** Need to validate bibliography completeness and citation consistency
- **Options considered:**
  - Option A: Use existing tools (bibtex-tidy, JabRef validation)
  - Option B: Custom Python script with project-specific rules
  - Option C: Manual checking
- **Decision:** Option B — Custom Python script
- **Rationale:**
  - Existing tools don't check citation usage in project files
  - Need integration with evidence registers (YAML)
  - Custom rules for research project (GRADE quality, prior conversion)
  - Can extend for future needs (DOI resolution, duplicate detection)
- **Evidence:** 
  - Review of bibtex-tidy features
  - Project-specific requirements
- **Impact:** Reference quality, citation consistency
- **Alternatives rejected:**
  - Option A: Limited functionality for this use case
  - Option C: Error-prone; not scalable
- **Reviewer:** Self-directed
- **Review date:** After Phase 5 (before publication)
- **Reflexive notes:** I enjoy building tools, so there's risk of over-engineering here. However, reference checking is genuinely tedious manually, and the script will save time long-term.

---

## Decision: Product guidelines document
- **Date:** 2026-03-03
- **Track:** gdpe_0002_evidence_anchoring
- **Category:** Infrastructure/Communication
- **Context:** Need consistent voice and tone across research outputs
- **Options considered:**
  - Option A: Create detailed product guidelines (voice, tone, visual design)
  - Option B: Simple style guide (grammar, formatting only)
  - Option C: No formal guidelines (write naturally)
- **Decision:** Option A — Comprehensive product guidelines
- **Rationale:**
  - Multiple audiences (academic, policy, public) require different tones
  - Ensures consistency across documents
  - Explicit guidance on uncertainty communication
  - Supports future collaboration (shared understanding)
- **Evidence:** 
  - CHEERS 2022 reporting guidelines
  - Health communication best practices
- **Impact:** All written outputs; publication strategy
- **Alternatives rejected:**
  - Option B: Insufficient for multi-audience research
  - Option C: Inconsistent quality; harder for collaborators
- **Reviewer:** Self-directed
- **Review date:** Before first publication
- **Reflexive notes:** This reflects my experience with inconsistent writing across projects. May seem excessive for solo work, but builds discipline and supports future team expansion.

---

## Decision: Humanizer-next extension setup
- **Date:** 2026-03-03
- **Track:** gdpe_0002_evidence_anchoring
- **Category:** Infrastructure/Workflow
- **Context:** Improve writing quality and automate reference checking in AI-assisted workflow
- **Options considered:**
  - Option A: Set up humanizer-next extension with reference validation
  - Option B: Use built-in AI writing tools only
  - Option C: Manual writing and checking
- **Decision:** Option A — Humanizer-next with custom configuration
- **Rationale:**
  - Integrates reference validation with AI writing workflow
  - Academic writing refinement appropriate for research outputs
  - Automated checking reduces errors
  - Configurable for different audiences (academic, policy)
- **Evidence:** 
  - Extension documentation
  - Writing quality improvements from AI assistance
- **Impact:** Writing workflow, output quality
- **Alternatives rejected:**
  - Option B: Limited validation capabilities
  - Option C: Time-consuming; more errors
- **Reviewer:** Self-directed
- **Review date:** After Phase 3 (evaluate effectiveness)
- **Reflexive notes:** I'm experimenting with AI writing tools. Acknowledge tension between efficiency and maintaining authentic voice. Using AI as assistant, not replacement for critical thinking.

---

## Decision: Evidence register structure (modules A-F + enforcement)
- **Date:** 2026-03-03
- **Track:** gdpe_0002_evidence_anchoring
- **Category:** Methods/Evidence
- **Context:** Organizing evidence by modelling module
- **Options considered:**
  - Option A: Organize by module (A-F + enforcement)
  - Option B: Organize by evidence type (empirical, modelling, policy)
  - Option C: Organize by jurisdiction only
- **Decision:** Option A — Module-based organization
- **Rationale:**
  - Direct mapping to model structure
  - Clear traceability from evidence to parameters
  - Supports module-by-module calibration
  - Easier to identify evidence gaps per module
- **Evidence:** 
  - Model architecture documentation
  - Traceability best practices
- **Impact:** Evidence organization, calibration workflow
- **Alternatives rejected:**
  - Option B: Harder to map to model parameters
  - Option C: Loses module-specific context
- **Reviewer:** Self-directed
- **Review date:** N/A
- **Reflexive notes:** This is the obvious choice given the modular model design. No real tension here.

---

## Decision: NZ evidence adapted from AU with wider priors
- **Date:** 2026-03-03
- **Track:** gdpe_0002_evidence_anchoring
- **Category:** Methods/Evidence
- **Context:** NZ has minimal direct evidence; need approach for parameter estimation
- **Options considered:**
  - Option A: Use AU evidence with wider priors for NZ
  - Option B: Expert elicitation for NZ-specific parameters
  - Option C: Assume identical parameters (no jurisdictional difference)
- **Decision:** Option A — AU evidence with wider priors
- **Rationale:**
  - NZ and AU share similarities (health systems, insurance markets)
  - Wider priors reflect additional uncertainty from extrapolation
  - More defensible than assuming no difference
  - Can be updated as NZ-specific evidence becomes available
- **Evidence:** 
  - Comparative health system analysis
  - Insurance market similarities
- **Impact:** NZ parameter estimates, uncertainty quantification
- **Alternatives rejected:**
  - Option B: Resource-intensive; not feasible in Phase 1
  - Option C: Ignores real differences; underestimates uncertainty
- **Reviewer:** Self-directed
- **Review date:** After Phase 2 (validate priors)
- **Reflexive notes:** As a New Zealander, I'm aware of tendencies to assume AU findings apply directly. Deliberately widening priors to acknowledge uncertainty. This is epistemically humble approach.

---

## Decision: Policy timeline as standalone document
- **Date:** 2026-03-03
- **Track:** gdpe_0002_evidence_anchoring
- **Category:** Infrastructure/Evidence
- **Context:** Policy timelines embedded in evidence registers vs. standalone
- **Options considered:**
  - Option A: Standalone policy timeline document
  - Option B: Embedded within each jurisdiction's evidence register
  - Option C: Separate wiki/website
- **Decision:** Option A — Standalone comparative document
- **Rationale:**
  - Facilitates direct AU/NZ comparison
  - Easier to update as policies change
  - Clear reference for modelling scenarios
  - Supports policy scenario analysis
- **Evidence:** 
  - Policy documents from both jurisdictions
  - Parliamentary inquiry reports
- **Impact:** Policy scenario modelling, comparative analysis
- **Alternatives rejected:**
  - Option B: Harder to compare across jurisdictions
  - Option C: Overkill; harder to version control
- **Reviewer:** Self-directed
- **Review date:** Quarterly (policy changes)
- **Reflexive notes:** Comparative framing is central to this research. Standalone document reinforces this. May seem redundant with evidence register timelines, but the comparison value justifies it.

---

## Decision: Very low quality evidence accepted with wide priors
- **Date:** 2026-03-03
- **Track:** gdpe_0002_evidence_anchoring
- **Category:** Methods/Evidence
- **Context:** NZ evidence base is extremely weak (all "Very Low" quality)
- **Options considered:**
  - Option A: Accept very low quality evidence with wide priors
  - Option B: Exclude very low quality evidence; use uninformative priors
  - Option C: Conduct expert elicitation to supplement
- **Decision:** Option A — Accept with wide priors
- **Rationale:**
  - Some evidence is better than none
  - Wide priors appropriately reflect uncertainty
  - VOI analysis will identify highest-value evidence gaps
  - Can be updated as better evidence emerges
- **Evidence:** 
  - HRC Inquiry (2020) - qualitative submissions
  - International evidence extrapolated
- **Impact:** NZ parameter estimates, VOI priorities
- **Alternatives rejected:**
  - Option B: Loses all contextual information
  - Option C: Not feasible in current timeline
- **Reviewer:** Self-directed
- **Review date:** After Phase 4 (VOI results)
- **Reflexive notes:** This is intellectually uncomfortable - building policy models on very weak evidence. But that's the reality of this policy domain. The model should make this uncertainty visible, not hide it. VOI will show where evidence matters most.

---

## Decision: Phase 1 review completed with minor fixes
- **Date:** 2026-03-03
- **Track:** gdpe_0002_evidence_anchoring
- **Category:** Workflow/Quality
- **Context:** Phase 1 review identified 1 error and 2 warnings in references
- **Options considered:**
  - Option A: Fix error, accept warnings, proceed to Phase 2
  - Option B: Fix all issues including warnings before proceeding
  - Option C: Delay Phase 2 until all warnings resolved
- **Decision:** Option A — Fix error, accept warnings, proceed
- **Rationale:**
  - Error (missing institution) was critical; fixed immediately
  - Warnings (missing DOI, corporate author) are acceptable limitations
  - Phase 2 work can proceed in parallel with minor reference updates
  - Perfectionism should not block progress
- **Evidence:** 
  - Reference validation report
  - Nature of warnings (not critical)
- **Impact:** Phase 1 completion, Phase 2 initiation
- **Alternatives rejected:**
  - Option B/C: Unnecessary delay; warnings don't affect validity
- **Reviewer:** Self-directed
- **Review date:** N/A
- **Reflexive notes:** I have a tendency toward perfectionism that can slow progress. Deliberately choosing "good enough" here. The warnings are genuinely minor and don't affect research quality.

---

## Decision: Māori data sovereignty principles acknowledged
- **Date:** 2026-03-03
- **Track:** gdpe_0002_evidence_anchoring
- **Category:** Ethics/Governance
- **Context:** NZ research involving genetic data requires Māori data sovereignty consideration
- **Options considered:**
  - Option A: Explicitly acknowledge Te Mana Raraunga principles in evidence register
  - Option B: Generic ethics statement only
  - Option C: No specific mention (assume covered by ethics approval)
- **Decision:** Option A — Explicit acknowledgment
- **Rationale:**
  - Genetic data has specific significance for Māori (whakapapa)
  - Te Mana Raraunga provides clear framework
  - Research should demonstrate cultural competence
  - Future data access will require Māori governance anyway
- **Evidence:** 
  - Te Mana Raraunga - Māori Data Sovereignty Network principles
  - NZ health research guidelines
- **Impact:** Data access planning, ethics applications
- **Alternatives rejected:**
  - Option B: Insufficient for genetic data
  - Option C: Ignores specific Māori rights and interests
- **Reviewer:** Self-directed
- **Review date:** Before data access applications
- **Reflexive notes:** As a non-Māori researcher, I need to be proactive about this. This isn't box-ticking; it's fundamental to ethical research in Aotearoa. May require genuine partnership with Māori researchers/communities as project develops.

---

**END OF DECISION LOG**
