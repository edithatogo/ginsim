# Track Spec: Remote Deployment Recovery and Release Synchronization

**Track ID:** gdpe_0049_remote_deployment_recovery_and_release_sync
**Type:** bugfix
**Status:** active

## Goal

Restore the public `ginsim.streamlit.app` deployment by aligning the deployment wrapper with the validated dashboard runtime, tightening local and CI quality gates around the dashboard surface, and moving the fixes onto a clean mergeable branch that can be promoted to the deployment branch.

## Scope

- Diagnose the live Streamlit Cloud failure against the current repository state.
- Align `gin-sim` deployment dependencies with `streamlit_app`.
- Expand dashboard-focused test coverage and remote smoke checks.
- Resolve newly surfaced runtime and arithmetic regressions until the enforced and broad non-remote suites pass.
- Prepare a clean release branch isolated from unrelated local worktree changes.
- Record remaining blockers between “validated branch” and “live redeployed site.”

## Non-Goals

- Rewriting or reconciling the unrelated dirty-worktree changes outside the deployment fix scope.
- Force-merging the branch backlog onto `origin/main` without explicit review of the remote divergence.
- Treating the public site as fixed before the release branch is merged and Streamlit Cloud has redeployed.

## Completion Criteria

- The deployment wrapper and dashboard runtime use a consistent dependency surface.
- The enforced quality gate passes locally on a clean branch.
- The broad non-remote pytest suite passes locally on a clean branch.
- A clean remote branch containing the validated fix set exists on GitHub.
- The remaining merge/redeploy steps and repo-hook blockers are documented explicitly.
