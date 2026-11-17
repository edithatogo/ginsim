# Track Specification: Institutionalized Logging

**Track ID:** gdpe_0028_institutionalized_logging
**Type:** Chore / Infrastructure
**Goal:** Transition the repository from print-based output to a unified, SOTA logging framework using `loguru`.

## 1. Overview
The current repository relies heavily on `print()` statements in scripts and lacks observability in core `src/` modules. This track institutionalizes `loguru` as the primary observability layer, providing structured, level-based logging across all execution environments (CLI, Dashboard, and CI/CD).

## 2. Functional Requirements
- **Central Config:** Create `src/utils/logging_config.py` to manage global log levels, sink formatting, and file rotation.
- **Src Instrumentation:** Add `from loguru import logger` to all core modules in `src/model/` and `src/utils/`.
- **Script Migration:** Replace `print()` statements in all `scripts/` with appropriate `logger.info`, `logger.error`, or `logger.success` calls.
- **Traceability:** Ensure logs include the `PROVENANCE_HASH` or Git commit where relevant.

## 3. Non-Functional Requirements
- **Zero-Noise CI:** Logs in CI should be clean and structured (no debug spam unless requested).
- **Performance:** Ensure logging calls don't introduce bottlenecks in JIT-compiled JAX loops (use logging outside JIT boundaries).

## 4. Acceptance Criteria
- [ ] Central logging configuration is active.
- [ ] 100% of `print()` calls in non-test scripts are migrated to `logger`.
- [ ] Core model functions emit lifecycle logs (e.g., "Starting equilibrium solve").
- [ ] Quality gate passes with clean linting for new logging imports.
