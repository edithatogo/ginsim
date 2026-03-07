# Context Engineering for This Project

**Version:** v1.1  
**Date:** 02 March 2026

This repo treats modelling as a *decision system* rather than a single model. To reduce ambiguity and improve reproducibility,
we store “context” as first-class artefacts: assumptions, definitions, comparator rulesets, priors, decision criteria, and logs
of modelling decisions.

This document describes the current context-management approach. It should not be read as a standalone publication-readiness or "SOTA" claim.

## What’s included
1. **Jurisdiction profiles** (`context/jurisdiction_profiles/`): structured definitions of what counts as genetic information,
   what is permitted/prohibited, and how policy levers map to model constraints.
2. **Assumptions registry** (`context/assumptions_registry.yaml`): every material assumption has an ID, rationale, data source,
   and planned sensitivity analysis.
3. **Decision log** (`context/decision_log.md`): time-stamped decisions (why we chose a model class, priors, comparators, etc.).
4. **Data dictionary template** (`context/data_dictionary_template.md`): required fields, schema, provenance, and linkage rules.
5. **Experiment cards** (`context/experiment_card_template.md`): each run has a hypothesis, config hash, outputs, and interpretation.

## How to use it
- Before analysis, fill out `jurisdiction_profiles/<jurisdiction>.yaml` and the assumptions registry.
- Every modelling change should add an entry to `decision_log.md`.
- Each major run should create an experiment card and commit the config snapshot.

## Why it matters
This prevents the “hidden degrees of freedom” problem: conclusions that depend on undocumented modelling choices.
It also supports later policy translation by making legal definitions and enforcement design explicit in the analytic pipeline.


## Game-theoretic framing
See `docs/GAME_THEORETIC_FRAMING.md` and the jurisdiction evidence templates under `context/jurisdiction_profiles/`.
