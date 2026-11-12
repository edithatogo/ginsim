# Implementation Plan: Remote Deployment Recovery and Release Synchronization

**Track ID:** gdpe_0049_remote_deployment_recovery_and_release_sync
**Execution mode:** Focused bug-fix and release synchronization

## Phase 1: Live Failure Triage
- [x] Task: Capture the live Streamlit Cloud failure mode and identify the failing import/runtime path.
- [x] Task: Compare deployment dependencies and entrypoints between `gin-sim` and `streamlit_app`.

## Phase 2: Reliability and Test Hardening
- [x] Task: Align `gin-sim` runtime dependencies with `streamlit_app`.
- [x] Task: Add or tighten local dashboard tests and remote smoke failure detection.
- [x] Task: Fix runtime regressions surfaced by the expanded dashboard tests.
- [x] Task: Resolve the DCBA welfare identity regression surfaced by the broad non-remote suite.

## Phase 3: Release Branch Preparation
- [x] Task: Isolate the validated fix set into a clean worktree branch.
- [x] Task: Validate the clean branch with the enforced quality gate.
- [x] Task: Validate the clean branch with the broad non-remote pytest suite.
- [x] Task: Push the clean release branch to GitHub.

## Phase 4: Remaining Promotion Blockers
- [ ] Task: Resolve or explicitly defer the broken `pre-push` red-team hook path (`scripts/check_red_team.py`) so release promotion does not rely on `--no-verify`.
- [ ] Task: Reconcile the large divergence between local history and `origin/main` and choose the merge strategy for deployment promotion.
- [ ] Task: Merge the validated branch onto the branch Streamlit Cloud deploys from.
- [ ] Task: Confirm the public `https://ginsim.streamlit.app/` instance is healthy after redeploy.
