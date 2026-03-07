# Implementation Plan: Empirical traceability and legacy analysis closure

**Track ID:** gdpe_0022_empirical_traceability_and_legacy_closure  
**Aspect:** empirical grounding, assumption traceability, and closure of legacy decomposition or uncertainty-analysis surfaces  
**Execution mode:** Autonomous Ralph-loop depth cycle  
**Estimated duration:** 3-6 days

---

## Phase 0 - Track Hardening

### Tasks
- [ ] Define the exact repository aspect and active-path boundaries.
- [ ] Draft the initial spec, plan, and metadata.
- [ ] Record the concrete starting targets for this track: legacy decomposition scripts, EVPPI or VOI sidecars, assumption-to-reference linkage, and any output surfaces overstating uncertainty support.
- [ ] Run 3 to 5 track-design refinement rounds by asking for improvements and incorporating them.
- [ ] Persist each refinement round as `track_refinement_round_<N>.md`.
- [ ] Update the spec and plan after the final refinement round.
- [ ] Run the Conductor review protocol for Phase 0 and persist `phase_0_review.md`.

---

## Phase 1 - Deep Exploration and Nature-Level Audit

### Tasks
- [ ] Explore the aspect in depth across code, configs, tests, outputs, docs, and dashboard surfaces.
- [ ] Identify active-path gaps, incomplete functions, placeholder logic, brittle assumptions, and reviewer-facing drift.
- [ ] Record a ranked audit with direct file and evidence references.
- [ ] Distinguish active issues from archival or non-blocking historical noise.
- [ ] Determine which legacy analytical surfaces should be repaired versus explicitly retired.
- [ ] Translate the audit into an implementation-ready closure map.
- [ ] Run the Conductor review protocol for Phase 1, auto-implement in-scope recommendations, and persist `phase_1_review.md`.

---

## Phase 2 - Implementation

### Tasks
- [ ] Replace active placeholder or scaffold logic in scope.
- [ ] Repair incomplete functions, broken surfaces, and integration gaps in scope.
- [ ] Add or strengthen tests for the repaired behavior.
- [ ] Update outputs, docs, and dashboard text where the implementation changes interpretation or usage.
- [ ] Qualify or retire any in-scope legacy surface that should no longer be presented as current analytical capability.
- [ ] Run the Conductor review protocol for Phase 2, auto-implement in-scope recommendations, and persist `phase_2_review.md`.

---

## Phase 3 - Verification, Push, and Deployment Checks

### Tasks
- [ ] Run the full relevant local verification set for the aspect.
- [ ] Run local Streamlit AppTest coverage for affected dashboard surfaces.
- [ ] Push the validated changes to the remote repository.
- [ ] Confirm the pushed commit's workflows succeed.
- [ ] Verify the live Streamlit deployment where configured.
- [ ] Run the Conductor review protocol for Phase 3, auto-implement in-scope recommendations, and persist `phase_3_review.md`.

---

## Phase 4 - Flow-on Effects, Chaining, and Template Improvement

### Tasks
- [ ] Assess direct and indirect flow-on effects of the change.
- [ ] Create the next follow-on track if any material residual work remains.
- [ ] Update the template reflection log with lessons learned and process improvements.
- [ ] Write `TRACK_COMPLETE.md` with final status, residual risks, and next-track linkage.
- [ ] Run the Conductor review protocol for Phase 4, auto-implement in-scope recommendations, and persist `phase_4_review.md`.

---

## Required verification gates

- `pytest -q`
- targeted smoke runs for repaired uncertainty, decomposition, or EVPPI scripts
- Local Streamlit AppTest coverage for touched pages
- Remote dashboard smoke test where `GDPE_REMOTE_DASHBOARD_URL` is configured
- Post-push workflow monitoring until all relevant runs complete

No phase is complete until its review artifact exists and no critical or high findings remain.
