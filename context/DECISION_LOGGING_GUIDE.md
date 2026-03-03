# Decision Logging and Reflexive Journaling Guide

**Purpose:** Ensure transparent, reflexive research practice throughout the project.

---

## Overview

This project maintains two complementary documentation streams:

1. **Decision Log** (`context/decision_log.md`) - Formal record of key decisions with rationale
2. **Reflexive Journal** (`context/reflexive_journal/`) - Critical self-reflection on positionality, biases, and assumptions

---

## Decision Log

### What to Document

Document decisions when:
- Choosing between multiple viable options
- Setting key model parameters or structures
- Selecting methods or frameworks
- Defining scope or boundaries
- Making ethical judgments
- Responding to unexpected findings

### Decision Categories

| Category | Examples |
|----------|----------|
| **Infrastructure** | Tools, platforms, file formats, workflows |
| **Methods** | Statistical approaches, modelling frameworks, evidence grading |
| **Policy** | Jurisdiction selection, scenario definitions, comparators |
| **Evidence** | Inclusion/exclusion, quality thresholds, prior conversion |
| **Code** | Architecture, libraries, testing strategies |
| **Ethics** | Data governance, community engagement, positionality |

### When to Update

- **During work:** Capture decisions as made (don't rely on memory)
- **Phase reviews:** Review and ensure all significant decisions documented
- **Before outputs:** Verify decisions supporting key findings are recorded

### Quality Standards

Good decision entries:
- ✅ List at least 2-3 options considered
- ✅ Explain why chosen option was selected
- ✅ Explain why alternatives were rejected
- ✅ Link to supporting evidence
- ✅ Note who reviewed the decision
- ✅ Set review date if decision should be revisited
- ✅ Include reflexive notes on biases/positionality

---

## Reflexive Journal

### Purpose

Reflexive journaling is critical self-reflection on:
- **Positionality** - How your background affects research
- **Power dynamics** - Who has voice, who is marginalized
- **Assumptions** - What you're taking for granted
- **Emotions** - How you feel about the work and why
- **Biases** - Where your judgment may be skewed

### When to Write

**Required:**
- End of each phase (Phase 1, 2, 3, 4, 5)
- After major decisions with ethical dimensions
- When encountering conflicting evidence
- Before finalizing policy recommendations

**Optional:**
- After difficult conversations
- When feeling stuck or uncertain
- After stakeholder meetings
- When recognizing personal bias in action

### Structure

Use the template at `context/reflexive_journal_template.md`:

1. **Context** - What triggered this reflection
2. **Positionality Check** - Your background and potential biases
3. **Critical Reflection** - Assumptions, uncertainties, missing perspectives
4. **Power and Privilege** - Who has voice, who doesn't
5. **Emotional Response** - How you feel and why
6. **Alternative Viewpoints** - What would critics/community members say
7. **Changes Made** - What you'll do differently
8. **Commitments** - Specific actions for future work

### Quality Standards

Good reflexive entries:
- ✅ Are honest about uncertainties and discomfort
- ✅ Name specific biases (not generic "I may be biased")
- ✅ Identify concrete missing perspectives
- ✅ Connect emotions to underlying values
- ✅ Steel-man counter-arguments (strongest version, not straw-man)
- ✅ Make specific commitments with deadlines
- ✅ Are written for yourself first, others second

---

## Integration with Workflow

### Phase Review Checklist

At each phase review, verify:

- [ ] Decision log updated with all significant decisions from phase
- [ ] Reflexive journal entry written for phase
- [ ] Commitments from previous phase reviewed and acted upon
- [ ] Assumptions registry updated with new explicit assumptions
- [ ] Key decisions linked to evidence registers

### Conductor Track Integration

The track plan includes decision logging as implicit in all tasks. Specific tasks:

**Phase 1:** 
- ✅ Decision log created with 12+ decisions
- ✅ Reflexive journal entry #1 written
- ✅ Template established for future entries

**Phase 2:**
- [ ] Document calibration decisions (evidence-to-prior conversions)
- [ ] Reflexive entry on uncertainty handling
- [ ] Review Phase 1 commitments

**Phase 3:**
- [ ] Document data access decisions
- [ ] Reflexive entry on power dynamics in data governance

**Phase 4:**
- [ ] Document validation decisions
- [ ] Reflexive entry on external reviewer feedback

**Phase 5:**
- [ ] Document dissemination decisions
- [ ] Final reflexive entry on overall research journey

---

## File Locations

| Document | Path | Purpose |
|----------|------|---------|
| Decision Log | `context/decision_log.md` | Formal decision tracking |
| Reflexive Journal Template | `context/reflexive_journal_template.md` | Template for entries |
| Reflexive Journal Entries | `context/reflexive_journal/entry_#[number].md` | Individual entries |
| Assumptions Registry | `context/assumptions_registry.yaml` | Explicit assumptions |

---

## Examples

### Good Decision Entry

See decision_log.md entries for:
- "GRADE framework adaptation" - Shows options, rationale, alternatives, reflexive note on familiarity bias
- "NZ evidence adapted from AU" - Acknowledges uncertainty, epistemic humility

### Good Reflexive Entry

See `reflexive_journal/entry_01_phase1_complete.md` for:
- Honest emotional processing (frustration, guilt, anxiety)
- Specific power analysis (who has voice, who doesn't)
- Concrete commitments with deadlines
- Steel-manned critiques

---

## Common Pitfalls

### Decision Log

❌ **Too brief:** "Decided to use YAML. Better than JSON."
✅ **Better:** "Decided to use YAML over JSON (human readability) and Markdown (structure). See discussion in [link]."

❌ **No alternatives:** "Using Bayesian approach."
✅ **Better:** "Considered Bayesian vs frequentist vs hybrid. Chose Bayesian because..."

❌ **No reflexive note:** [Missing]
✅ **Better:** "My training in health economics predisposes me toward Bayesian approaches. Acknowledging this bias..."

### Reflexive Journal

❌ **Performative:** "I may have some biases but I think I handled them well."
✅ **Better:** "I caught myself dismissing qualitative evidence as 'just anecdotes.' This reflects my quantitative training bias."

❌ **Vague commitments:** "I'll do better at engagement."
✅ **Better:** "By 2026-03-17, I will contact Dr [Name] at [Organization] to discuss Māori governance of this research."

❌ **Writing for audience:** Polished, defensive
✅ **Better:** Raw, honest, uncomfortable truths

---

## Review and Accountability

### Self-Review

Before phase sign-off:
1. Read previous phase's commitments
2. Verify each was actioned
3. If not, document why in new reflexive entry
4. Make new/updated commitments

### External Accountability

Consider sharing:
- Decision log with supervisors/collaborators
- Selected reflexive entries with trusted colleagues
- Commitments with accountability partners

---

## References

- Bolton C. Reflexivity in research. [Methodological resources]
- Māori Data Sovereignty Network. Te Mana Raraunga principles.
- GRADE Working Group. GRADE guidelines.
- ISPOR-SMDM Modeling Good Practices Task Force.

---

**Version:** 1.0  
**Date:** 2026-03-03  
**Track:** gdpe_0002_evidence_anchoring
