# Specification: Game Engine Hardening

**Track ID:** gdpe_0047_game_engine_hardening
**Aspect:** Core logic paths in Module A (Insurance) and Module D (Welfare).

## Goal
Now that the inputs and foundations are hardened (via gdpe_0022), we must ensure the core strategic decision branches in the game engine are 100% covered by Property-Based Testing (PBT).

## Scope
- `src/model/module_a_insurance.py` (or equivalent)
- `src/model/module_d_welfare.py` (or equivalent)
- Verification of equilibrium conditions under extreme parameter sets.

## Acceptance Criteria
- 100% statement coverage for Modules A & D logic.
- `Hypothesis` PBT suite for insurer solvency and welfare monotonicity.
- No regression in benchmark scenarios.