# Python style guide

- Prefer explicit types for public functions (type hints).
- Avoid global mutable state; pass parameters explicitly.
- Use deterministic seeds when randomness is involved.
- Keep modules small and single-purpose.
- Prefer pure functions for transforms; isolate IO.

## Formatting and linting (recommended)
- `black` for formatting
- `ruff` for lint + import sorting

## Testing (recommended)
- `pytest` for unit tests
- Focus on:
  - schema validation
  - policy encoding/mapping
  - invariants (bounds, monotonicity where expected)
  - reproducibility (seeded runs)
