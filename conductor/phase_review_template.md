# Phase Review Template

**Track:** [Track ID]  
**Phase:** [Phase Number and Name]  
**Review Date:** YYYY-MM-DD  
**Reviewer:** [Name/AI Assistant]

---

## Phase Completion Checklist

### Tasks
- [ ] All phase tasks marked as `[x]` in plan.md
- [ ] Task artifacts/outputs collected and documented

### Acceptance Criteria
- [ ] All acceptance criteria met (see plan.md)
- [ ] Evidence of completion documented below

### Quality Checks
- [ ] Reference validation run (`python -m scripts.validate_references --report`)
- [ ] No critical reference errors (warnings acceptable with documentation)
- [ ] Code quality checks passed (if code changes)
- [ ] Tests passed (if applicable)

### Documentation
- [ ] New/updated documentation follows product-guidelines.md
- [ ] Writing tone appropriate for target audience
- [ ] All claims evidence-based or labeled as assumptions

---

## Automated Check Results

### Reference Validation
```
[Paste output from: python -m scripts.validate_references --report]
```

**Status:** [ ] Pass [ ] Pass with warnings [ ] Fail

### Code Quality (if applicable)
```
[Paste output from: ruff check src/ scripts/]
```

**Status:** [ ] Pass [ ] Pass with warnings [ ] Fail

### Tests (if applicable)
```
[Paste output from: pytest -q]
```

**Status:** [ ] Pass [ ] Pass with warnings [ ] Fail

---

## Issues and Recommendations

### Critical Issues (must fix before proceeding)
[List any blockers]

### Warnings (should fix, but can proceed)
[List non-critical issues]

### Suggestions for next phase
[Recommendations for improvement]

---

## Artifacts Produced

[List all outputs, documents, code, data produced in this phase]

| Artifact | Path | Description |
|----------|------|-------------|
| | | |

---

## Review Decision

- [ ] **Proceed to next phase** — All criteria met, no critical issues
- [ ] **Proceed with minor revisions** — Warnings noted, will address in parallel
- [ ] **Requires major revisions** — Critical issues must be resolved first

**Reviewer sign-off:** _________________  
**Date:** _________________

---

## Next Phase Preparation

**Next phase:** [Phase N+1 Name]  
**Ready to start:** [Yes/No]  
**Prerequisites met:** [Yes/No]

**Notes:**
