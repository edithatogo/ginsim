# New Zealand Transferability Audit

**Track:** `gdpe_0020_dashboard_policy_alignment_and_publication_sync`
**Date:** 2026-03-07
**Status:** In progress

---

## Purpose

This audit documents the New Zealand calibration entries that currently depend on transferred, extrapolated, or adaptation-based evidence. The goal is not to eliminate all borrowed evidence immediately, but to make every transfer explicit, justify it, and connect it to uncertainty treatment and replacement priorities.

## Overall Assessment

The New Zealand calibration remains heavily transfer-based.

Signals from `configs/calibration_new_zealand.yaml`:
- `12` total calibrated parameters are summarized in the file.
- `3` are described as NZ-specific in the file summary.
- `9` are described as extrapolated/adapted.
- the file explicitly states that NZ has `0 quantitative studies` in this domain and that all evidence quality is effectively very low.

This means NZ results can still be analytically useful, but they must be presented as high-uncertainty policy appraisal rather than mature jurisdiction-specific estimation.

## Transfer Register

| Parameter | Current source basis | Transfer type | Why it was borrowed | Main risk | Current mitigation | Replacement priority |
|---|---|---|---|---|---|---|
| `baseline_testing_uptake` | `ettema2021` with NZ contextual notes | Netherlands -> NZ extrapolation | No NZ quantitative uptake evidence in repo | Base-rate misspecification | Wider SD and explicit uncertainty note | High |
| `deterrence_elasticity` | `hrc2020` + `mcguire2019` | Qualitative NZ + US quantitative blend | No NZ causal estimate of deterrence | Behavioural effect may be over- or under-scaled | Very wide range and EVPPI priority | Very high |
| `moratorium_effect` | `hrc2020` | Informal-practice proxy | No formal NZ moratorium policy | Policy comparator may overstate real NZ practice | Extremely wide range | Very high |
| `adverse_selection_elasticity` | `hersch2019` | US structural result adjusted for NZ concentration | No NZ market estimate | Wrong structural response under NZ insurer concentration | Lower mean plus wider SD | Very high |
| `demand_elasticity_high_risk` | `armstrong2020` | US -> NZ extrapolation | No NZ demand response evidence | Incorrect premium-demand coupling | Wider SD and truncation | High |
| `baseline_loading` | `hrc2020` + `fsc2019` | NZ informal-practice proxy using AU policy anchor | No NZ loading data | Misstates current underwriting baseline | Extremely wide range | High |
| `family_history_sensitivity` | `tabor2018` | US -> NZ extrapolation | No NZ family-history proxy estimate | Proxy model may not reflect NZ underwriting practice | Wider SD than AU | Medium |
| `proxy_substitution_rate` | `lowenstein2021` | Multi-jurisdiction -> NZ extrapolation | No NZ substitution evidence | Overstates or understates leakage under reform | Wide Beta prior | High |
| `pass_through_rate` | `finkelstein2019` | US structural result adjusted for NZ concentration | No NZ pass-through estimate | Market-power assumption may be directionally wrong | Lower mean than AU plus wider SD | High |
| `research_participation_elasticity` | `blevins2020` | International -> NZ extrapolation | No NZ estimate of research externality | Externality claims may be weakly grounded | Wider SD and explicit note | Medium |

## Transferability Logic Currently Used

The current repo is implicitly applying four transfer rules:

1. **Developed-system baseline rule**
   Use a non-NZ developed-country estimate as a starting mean when no NZ quantitative estimate exists.

2. **Contextual adjustment rule**
   Shift the mean if NZ-specific qualitative evidence suggests a directionally different effect.

3. **Variance inflation rule**
   Widen the prior SD relative to the Australian or overseas analogue to reflect transfer uncertainty.

4. **Decision caution rule**
   Treat NZ outputs as higher-uncertainty and higher-VOI than AU outputs.

These rules are reasonable as interim practice, but they need to be described explicitly in manuscript/protocol/dashboard surfaces rather than left implicit in calibration comments.

## Priority Risks

### Very high priority
- `deterrence_elasticity`
- `moratorium_effect`
- `adverse_selection_elasticity`

These sit closest to the main policy claims and can materially change comparative conclusions.

### High priority
- `baseline_testing_uptake`
- `demand_elasticity_high_risk`
- `baseline_loading`
- `proxy_substitution_rate`
- `pass_through_rate`

These shape both effect size and distributional interpretation.

### Medium priority
- `family_history_sensitivity`
- `research_participation_elasticity`

These matter, but are less central to the headline benchmark-policy comparison surface.

## Required Follow-up

1. Create manuscript/protocol language that explicitly states NZ estimates are transfer-based and uncertainty-inflated.
2. Ensure dashboard and report surfaces distinguish NZ benchmark outputs from any stronger empirical claims.
3. Link each transferred parameter to the assumptions registry and the reference validator output.
4. Add a replacement roadmap for direct NZ evidence recovery where feasible.
5. Keep NZ-facing recommendation language cautious until active-path placeholder logic and documentation claims are fully reconciled.
