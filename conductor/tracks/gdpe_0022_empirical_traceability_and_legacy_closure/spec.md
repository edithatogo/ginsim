# Track Specification: Empirical traceability and legacy analysis closure

**Track ID:** gdpe_0022_empirical_traceability_and_legacy_closure  
**Type:** Nature-Depth Improvement Cycle  
**Aspect:** empirical grounding, assumption traceability, and closure of legacy decomposition or uncertainty-analysis surfaces  
**Date:** 2026-03-07

---

## 1. Objective

Take the repository aspect `empirical grounding, assumption traceability, and closure of legacy decomposition or uncertainty-analysis surfaces` from its current state to the strongest publication-grade, reviewer-defensible, deployment-safe state that is realistically achievable within one track.

This track must not behave like a shallow bugfix pass. It must:

- explore the aspect in depth;
- judge it against Nature-family expectations for sophistication, coherence, traceability, UX, reproducibility, and completeness;
- identify gaps, placeholders, scaffolding, drift, and hidden downstream effects;
- implement the highest-value closure work;
- review itself before phase progression and before closure;
- push validated changes remotely and confirm the remote workflows and Streamlit deployment status;
- create the next track if flow-on work remains.

This track opts into:

- autonomous phase-loop execution;
- Ralph-style iterative improvement;
- post-phase Conductor review and auto-remediation;
- post-push workflow monitoring;
- end-of-track next-track creation;
- template reflection and improvement.

## 2. Scope

This track is specifically concerned with the still-open gap between the repository's active model path and the older legacy uncertainty, decomposition, EVPPI, and evidence-traceability surfaces that still matter for reviewer confidence and publication-grade closure.

### 2.1 Aspect exploration
- Inspect the chosen aspect deeply enough to identify active-path behavior, hidden assumptions, dead scaffolding, output/reporting effects, and deployment implications.
- Map the aspect to the exact code paths, configs, docs, outputs, tests, and dashboard surfaces it touches.
- Distinguish active-path defects from archival noise.
- Prioritize the known weak surfaces first:
  - legacy decomposition and EVPPI scripts that were previously noted as broken against removed APIs;
  - evidence-to-parameter linkage and assumption justification surfaces;
  - any manuscript or output artifacts that still imply richer uncertainty support than the active path actually delivers.

### 2.2 Nature-level audit
- Evaluate the aspect against top-tier publication expectations:
  - empirical grounding;
  - functional completeness;
  - reviewer clarity;
  - output quality;
  - interpretability;
  - deployment robustness;
  - test coverage;
  - traceability;
  - claims discipline.
- Treat placeholders, synthetic outputs, misleading docs, broken tests, unverified UI paths, and weak evidence linkage as first-class gaps.

### 2.3 Plan and implementation
- Convert the audit into a concrete plan focused on the chosen aspect.
- Replace active-path placeholder logic where found.
- Repair defects, missing tests, missing docs, broken outputs, or incoherent UX in scope.
- Keep the implementation narrow enough that the track remains coherent.
- Where a legacy analytical surface should not be repaired, explicitly retire or qualify it rather than leaving it half-alive.

### 2.4 Review and auto-remediation
- At the end of each phase, run the Conductor review protocol for the current phase scope.
- Automatically implement in-scope recommendations.
- Re-run the review until no critical or high findings remain.

### 2.5 Remote and deployment verification
- Run relevant local verification.
- Push to the remote repository.
- Confirm GitHub Actions or equivalent workflows succeed for the pushed commit.
- Verify the Streamlit dashboard locally and, where configured, against the live deployment.

### 2.6 Flow-on effects and chaining
- Assess downstream impacts of the change after implementation and after push.
- Create the next follow-on track if residual work remains.
- Update this template's reflection log with lessons learned.

## 3. Acceptance Criteria

- [ ] The chosen repository aspect has been explored deeply enough to separate active defects from archival noise.
- [ ] A Nature-level audit has been recorded and converted into a specific implementation plan.
- [ ] In-scope active-path gaps, placeholders, drift, and broken surfaces have been addressed.
- [ ] Legacy uncertainty/decomposition or EVPPI surfaces are either repaired to active-path compatibility or explicitly retired with current-state documentation.
- [ ] Evidence, assumptions, and output claims for this aspect are aligned so a reviewer does not encounter unsupported sophistication claims.
- [ ] Relevant tests and smoke runs pass locally.
- [ ] Streamlit dashboard verification passes locally; remote verification passes where configured.
- [ ] The pushed commit's workflows succeed.
- [ ] Flow-on effects are assessed and recorded.
- [ ] If residual work remains, a concrete next track is created before closure.
- [ ] The template reflection log is updated with at least one improvement to the template or process.
- [ ] Phase review artifacts exist and show review, auto-remediation, and decision to proceed.

## 4. Cross-agent operating rules

This template is intended to work across Codex, Gemini CLI, and Qwen Code:

- Do not rely on agent-specific slash commands.
- Use plain markdown artifacts and explicit filenames.
- Record assumptions, commands, verification steps, and next actions in files, not only chat.
- Keep handoff artifacts stable enough that a different coding agent can resume without hidden context.

## 5. Required refinement loop before implementation

Before Phase 1 implementation starts, run a track-design refinement loop:

1. Propose the initial track.
2. Ask: "Are there any improvements to this track that you would recommend?"
3. Incorporate the answer.
4. Repeat the same question and incorporation cycle 3 to 5 times total.
5. If no human operator is available, simulate the same refinement loop through structured self-critique documented in `track_refinement_round_<N>.md`.

The purpose is to harden the track before coding begins rather than after avoidable design drift has already occurred.
