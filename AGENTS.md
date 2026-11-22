# Working on GINSIM

Read [README.md](README.md), [CONTRIBUTING.md](CONTRIBUTING.md) and the relevant
model assumptions and evidence registers before editing. Preserve the
distinction between exploratory strategic scenarios and validated policy claims.

## Game capability ownership

UOGTO is the authoritative game ontology; Paignia owns reusable game
representations and solvers. For every newly identified, added or materially
changed game, follow
the [contributor intake rule](CONTRIBUTING.md#game-capability-intake) and record
both semantic coverage and reusable implementation needs using:

- [UOGTO downstream game intake](https://github.com/edithatogo/UOGTO/blob/main/docs/contracts/downstream-game-intake.md).
- [Paignia downstream game intake](https://github.com/edithatogo/paignia/blob/main/docs/integrations/downstream-game-intake.md).

Record UOGTO's `reuse_existing`, `extension_required`, `unsupported` or
`mapping_review_pending` disposition separately from Paignia's `reuse_existing`,
`extension_required`, `unsupported`, `domain_only` or `assessment_pending`.
Genetic-risk evidence, insurance assumptions, payoff construction and
calibration remain here. Route generic representations, algorithms and synthetic
conformance fixtures upstream instead of adding a competing reusable solver.

Existing local models may remain while migration is assessed, with their
mathematical scope labelled. A response formula or model name does not establish
an equilibrium solution. Any later migration needs accepted immutable provider
revisions and the focused conformance checks actually run.
