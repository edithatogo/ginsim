# Submission Gap Register

**Status:** Draft scaffold created in `gdpe_0021` Phase 1  
**Purpose:** Centralize the remaining barriers between the current repository state and a clean top-tier journal submission package.

---

## Register

| Gap ID | Blocker | Reviewer impact | Affected artifact(s) | Current status | Planned closure mechanism | Deferral rationale |
|---|---|---|---|---|---|---|
| SGR-001 | Reviewer-facing map is only partially populated | Reviewer must infer links between claims, code, outputs, and assumptions | `docs/REVIEWER_NAVIGATION_MAP.md`, methods/protocol docs | Open | Complete map population in `gdpe_0021` Phase 2 | None |
| SGR-002 | Historical/milestone docs still need clearer archival qualification in selected still-visible surfaces | Reviewer may misread milestone-era readiness or topology language as current state | selected docs under `docs/`, `protocols/`, `conductor/` | Open | Harmonization and archival framing in `gdpe_0021` Phase 2 | None |
| SGR-003 | Manuscript asset inventory is not yet centralized | Figure/table/caption completeness is harder to audit quickly | publish-pack docs and generated artifacts | Open | Build asset inventory in `gdpe_0021` Phase 3 | None |
| SGR-004 | Remaining submission blockers are currently being consolidated | Submission readiness is harder to assess at a glance | repo-facing readiness and output docs | In progress | Maintain this register as the canonical blocker list through track closeout | None |

## Use

- Add a row when a genuine submission blocker or reviewer-confusion risk is identified.
- Close a row only when the corresponding artifact has been updated and the result is validated.
- If a blocker is intentionally deferred, the rationale should be explicit and reviewer-safe.
