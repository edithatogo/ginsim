# Product Guidelines

## Purpose
This document defines the communication style, tone, and branding for all outputs produced by this research project.

---

## Voice and Tone

### Primary Voice: **Authoritative yet Accessible**

We write for multiple audiences (researchers, policymakers, clinicians, advocates). Our voice adapts while maintaining credibility.

#### For Academic Audiences
- **Tone:** Precise, technical, hedged appropriately
- **Language:** Domain-specific terminology acceptable
- **Certainty:** Explicit uncertainty quantification (credible intervals, probabilities)
- **Example:** "Our Bayesian decision analysis suggests a 73% probability that Policy B dominates Policy A on net welfare grounds (95% CrI: 0.68–0.78), driven primarily by reduced deterrence effects."

#### For Policy Audiences
- **Tone:** Clear, actionable, evidence-based
- **Language:** Minimize jargon; explain necessary technical terms
- **Certainty:** Plain-language uncertainty (e.g., "moderate confidence", "key uncertainty")
- **Example:** "The evidence suggests that moratorium approaches increase genetic testing uptake by 10–20%, though the exact magnitude depends on enforcement mechanisms. We have moderate confidence in this estimate."

#### For Public/Advocacy Audiences
- **Tone:** Empathetic, clear, focused on human impact
- **Language:** Avoid all jargon; use concrete examples
- **Certainty:** Simple framing (e.g., "research shows", "studies suggest")
- **Example:** "When people worry that genetic test results could affect their insurance, some choose not to get tested—even when testing could save their lives. Our research looks at how different policies affect these decisions."

---

## Writing Principles

### 1. **Evidence-First**
All claims must be traceable to evidence in our registers. Use the GRADE framework to communicate confidence.

✅ **Good:** "Moderate-quality evidence from Australian surveys suggests 15–25% of at-risk individuals avoid testing due to insurance concerns (Taylor et al., 2021)."

❌ **Bad:** "Many people avoid genetic testing because of insurance worries."

### 2. **Transparent Uncertainty**
Never hide uncertainty. Quantify it where possible.

✅ **Good:** "The model estimates 120–180 additional QALYs per year (95% uncertainty interval), with EVPPI analysis suggesting that better data on testing behaviour would be most valuable."

❌ **Bad:** "The policy will save 150 QALYs per year."

### 3. **Comparative Framing**
Always present policies comparatively, not in isolation.

✅ **Good:** "Compared to the baseline (no restrictions), the moratorium increases testing uptake by 12% (9–16%), while a full ban increases uptake by 18% (14–23%)."

❌ **Bad:** "The moratorium increases testing uptake by 12%."

### 4. **Distributional Awareness**
Highlight who benefits and who bears costs.

✅ **Good:** "While the moratorium reduces adverse selection pressure on insurers, the primary welfare gains accrue to individuals with elevated genetic risk, who face lower effective premiums and reduced anxiety about discrimination."

❌ **Bad:** "The moratorium improves welfare."

### 5. **Actionable Conclusions**
End with clear implications, not just findings.

✅ **Good:** "For policymakers: enforcement mechanisms matter more than the formal policy label. A weakly enforced ban may be less effective than a strongly enforced moratorium with clear penalties."

❌ **Bad:** "Further research is needed."

---

## Document-Specific Guidelines

### Academic Papers
- Follow CHEERS 2022 reporting guidelines
- Use structured abstracts (Background, Methods, Results, Conclusions)
- Include limitations section (required, not optional)
- Cite using author-year format
- Target journals: *Value in Health*, *Medical Decision Making*, *Journal of Health Economics*, *Genetics in Medicine*

### Policy Briefs
- Maximum 4 pages (excluding appendices)
- Executive summary: ≤200 words, no citations
- Key findings: 3–5 bullet points
- Recommendations: clearly separated from evidence
- Use colorblind-safe figures
- Provide plain-language glossary

### Technical Reports
- Full methods disclosure
- Reproducibility checklist completed
- Run manifest included (git hash, timestamp, config)
- Sensitivity analyses prominent (not buried in appendix)
- Code and data availability statement

### Presentations
- One key message per slide
- All figures have descriptive titles (not "Results" but "Moratorium Increases Testing Uptake by 12%")
- Uncertainty shown on all quantitative claims
- Backup slides for methods (move technical details out of main flow)

---

## Visual Design

### Color Palette
Use colorblind-safe palettes:
- **Primary:** Viridis, Plasma, or Cividis (sequential)
- **Diverging:** RdBu (reversed), PiYG
- **Categorical:** Okabe-Ito or Wong palettes

**Never use:** Red-green combinations without additional differentiation.

### Figure Standards
- Minimum font size: 8pt in final output
- Axis labels with units
- Confidence/uncertainty intervals on all estimates
- Source note: "Source: Authors' analysis" or data source
- Panel labels (A, B, C, D) for multi-panel figures

### Table Standards
- No vertical lines
- Minimal horizontal lines (header and footer only, typically)
- Uncertainty in parentheses below point estimates
- Notes section explaining abbreviations, methods

---

## Naming and Terminology

### Preferred Terms

| Use | Avoid |
|-----|-------|
| "Policy restricting use of genetic information" | "Genetic discrimination ban" (unless specific) |
| "Testing uptake" | "Testing rate" |
| "Adverse selection pressure" | "Adverse selection spiral" (unless modeled) |
| "Perceived discrimination risk" | "Fear of discrimination" |
| "Information asymmetry" | "Information imbalance" |
| "Welfare impact" | "Benefit" or "cost" (unless monetary) |
| "Aotearoa New Zealand" | "NZ" (in formal writing) |

### Acronyms
Define at first use, then use consistently:
- QALY: quality-adjusted life year
- VOI: value of information
- EVPI: expected value of perfect information
- EVPPI: expected value of partial perfect information
- DCBA: distributional cost-benefit analysis
- HTA: health technology assessment

---

## Citation and Attribution

### In-Text Citations
- Use author-year format: (Smith et al., 2021) or "Smith et al. (2021) found..."
- For 3+ authors: use "et al." from first citation
- For our own work in progress: "Authors' analysis" or "Mordaunt (forthcoming)"

### Bibliography
- Maintain in `context/references.bib` (BibTeX format)
- Run `python -m scripts.validate_references` before submission
- Include DOIs for all entries where available
- Verify all citations are in bibliography and vice versa

### Data Attribution
- Acknowledge data sources in methods and footnotes
- Include data license/copyright statements
- For restricted data: "Data accessed under agreement with [organization]"

---

## Ethics and Positionality

### Acknowledge Limitations
- Be explicit about what the model does and does not capture
- Note excluded domains (e.g., employment discrimination, if not modeled)
- Discuss generalizability (AU/NZ to other jurisdictions)

### Avoid Overclaiming
- Use "suggests", "indicates", "is consistent with" rather than "proves"
- Distinguish model outputs from empirical findings
- Clearly label assumptions vs. evidence

### Community Engagement
- Acknowledge input from affected communities where applicable
- Note if lived experience was incorporated (or why it wasn't)
- Consider plain-language summary for public audiences

---

## Review and Quality Assurance

### Pre-Release Checklist
Before any public output, verify:
- [ ] All claims traceable to evidence or clearly labeled as assumptions
- [ ] Uncertainty quantified and visible
- [ ] Terminology consistent with this guide
- [ ] References validated (`scripts/validate_references.py`)
- [ ] Figures accessible (colorblind-safe, readable fonts)
- [ ] Limitations discussed
- [ ] Appropriate tone for target audience

### Peer Review
- Technical outputs: ≥1 independent expert review
- Policy briefs: ≥1 policy audience member + ≥1 technical reviewer
- Public materials: Plain-language review by non-expert

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-03 | Initial version |

---

## References

- CHEERS 2022 Statement: Husereau D, et al. Value Health. 2022;25(1):3-9.
- GRADE Handbook: Schünemann HJ, et al. 2013.
- Okabe-Ito colorblind palette: http://jfly.iam.u-tokyo.ac.jp/color/
- Wong colorblind palette: Wong B. Nature Methods. 2011;8:441.
