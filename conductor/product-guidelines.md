# Product Guidelines

## Prose Style & Documentation Standards

### Tone & Voice
- **Academic Rigor:** Maintain formal, precise language suitable for peer-reviewed research contexts
- **Clarity Over Complexity:** Explain technical concepts accessibly without sacrificing accuracy
- **Neutral & Objective:** Present findings without advocacy; let data speak for itself
- **Transparency:** Explicitly state assumptions, limitations, and uncertainty ranges

### Documentation Structure
- **README-first:** All modules must have a README explaining purpose, inputs, outputs, and key assumptions
- **Inline Comments:** Use docstrings for all public functions; explain *why*, not just *what*
- **Citation Trail:** Link claims to evidence in the structured evidence register (`context/` directory)
- **Versioned Changes:** Document breaking changes in CHANGELOG.md with migration guidance

### Audience Considerations
| Audience | Needs | Documentation Layer |
|----------|-------|---------------------|
| **Peer Reviewers** | Audit trail, assumption validation, reproducibility | `docs/`, `protocols/`, validation scripts |
| **Policy Makers** | Executive summaries, visual dashboards, scenario comparisons | Streamlit app, policy briefs |
| **Researchers** | API reference, extension points, calibration data | Module docstrings, `src/` READMEs |
| **Developers** | Setup instructions, testing protocols, contribution guidelines | CONTRIBUTING.md, this file |

---

## Branding & Visual Identity

### Color Palette
- **Primary:** Deep blue (#1f4e79) - conveys trust, academic rigor
- **Secondary:** Teal (#008080) - represents health, equity
- **Accent:** Gold (#d4af37) - highlights key findings, policy recommendations
- **Semantic Colors:**
  - Success/Positive Impact: Green (#2e7d32)
  - Warning/Caution: Amber (#f57c00)
  - Risk/Negative Impact: Red (#c62828)
  - Neutral/Baseline: Gray (#616161)

### Typography
- **Headings:** Sans-serif (system default: Segoe UI, San Francisco, Roboto)
- **Body Text:** Sans-serif for readability at all sizes
- **Code/Monospace:** Consolas, Monaco, or Fira Code for code blocks, parameter names
- **Mathematical Notation:** LaTeX rendering via MathJax/KaTeX where applicable

### Logo & Iconography
- Use simple, geometric icons for model modules (A-F)
- Maintain consistency between Streamlit app and documentation
- Avoid decorative elements; prioritize clarity and accessibility

---

## UX Principles (Streamlit Dashboard)

### Core Design Philosophy
- **Sandbox Mentality:** Enable rapid "what-if" exploration without requiring technical expertise
- **Progressive Disclosure:** Start simple; reveal advanced parameters on demand
- **Immediate Feedback:** All parameter changes trigger instant recalculation (leverage JAX compilation)
- **Error Prevention:** Validate inputs client-side; provide sensible defaults and ranges

### Interaction Patterns
1. **Policy Selector:** Prominent dropdown at top; switches entire dashboard context
2. **Parameter Sliders:** Use for sensitivity analysis; show baseline marker
3. **Comparison Mode:** Side-by-side policy comparison with delta highlighting
4. **Red-Teaming:** Active search for failure modes using adversarial optimization (JAX/Optax)
5. **Stakeholder Consensus:** Multi-persona Delphi Protocol for live qualitative auditing
6. **Downloadable Outputs:** All charts exportable as PNG/SVG; tables as CSV
5. **Shareable Links:** Encode parameter state in URL for collaboration

### Accessibility Requirements
- **Colorblind-Safe Palettes:** All visualizations pass WCAG 2.1 AA contrast ratios
- **Keyboard Navigation:** Full dashboard navigable without mouse
- **Screen Reader Support:** Alt text for all charts; semantic HTML structure
- **Responsive Layout:** Functional on tablets (minimum 768px width)

### Performance Expectations
- **Initial Load:** < 5 seconds to interactive dashboard
- **Recalculation:** < 2 seconds for parameter changes (cached JAX functions)
- **Large Datasets:** Lazy-load posterior samples; paginate tables

---

## Research Integrity & Reproducibility

### Reproducibility Standards
- **Deterministic Seeds:** All stochastic processes use explicit, logged RNG seeds
- **Version Pinning:** Dependencies locked via `uv.lock`; Docker image for deployment
- **Data Provenance:** All external data sources cited with DOI/accession numbers
- **Run Manifests:** Every simulation outputs metadata (timestamp, git commit, parameters)

### Assumption Tracking
- **Explicit Declaration:** All model assumptions documented in `protocols/assumptions.yaml`
- **Sensitivity Tagging:** Mark parameters as `robust`, `uncertain`, or `assumed`
- **Change Log:** Track assumption revisions with justification and impact analysis

### Validation Protocol
- **Unit Tests:** All core functions have tests covering edge cases (minimum 80% coverage)
- **Benchmark Comparisons:** Validate against published results (e.g., prior literature values)
- **Peer Review Readiness:** All reviewer-facing documentation in `docs/` kept current
- **Delphi Protocol:** Live agentic auditing by Nature/Lancet/Treasury personas for scenario robustness
- **External Audit Trail:** `context/reflexive_journal/` documents design decisions

---

## Cultural Responsiveness (Aotearoa NZ & Australia Context)

### Te Tiriti o Waitangi Alignment
- **Partnership:** Engage with Māori stakeholders in model design and interpretation
- **Protection:** Ensure model does not perpetuate biases against Indigenous populations
- **Participation:** Enable Māori data sovereignty in any future data linkage work

### Indigenous Data Considerations
- **CARE Principles:** Collective benefit, Authority to control, Responsibility, Ethics
- **Proxy Variable Caution:** Document risks of ethnic/racial categorization in models
- **Community Engagement:** Plan for feedback loops with affected communities

### Language & Terminology
- **Bicultural Labels:** Use "Aotearoa New Zealand" in formal contexts
- **Indigenous Capitalization:** "Māori", "Aboriginal and Torres Strait Islander peoples"
- **Person-First Language:** "People with genetic conditions" not "genetic disease carriers"

---

## Code Style & Architecture Guidelines

### Naming Conventions
- **Modules:** `snake_case` (e.g., `module_a_behavior.py`)
- **Classes:** `PascalCase` (e.g., `ModelParameters`, `PolicyConfig`)
- **Functions:** `snake_case` with verb prefixes (e.g., `evaluate_policy_sweep`, `compute_nash_equilibrium`)
- **Constants:** `UPPER_SNAKE_CASE` (e.g., `DEFAULT_N_DRAWS`, `STATUS_QUO_LABEL`)

### Architectural Principles
- **Modularity:** Each module (A-F) is independently testable and swappable
- **Immutability:** Prefer immutable data structures (frozen dataclasses, tuples)
- **Pure Functions:** Maximize pure functions; isolate side effects (I/O, RNG) at boundaries
- **Type Safety:** Use `jaxtyping` + `beartype` for runtime type checking in development

### Error Handling
- **Informative Messages:** Include parameter values, expected ranges, and failure context
- **Graceful Degradation:** Dashboard remains functional if optional modules fail
- **Logging:** Use `loguru` for structured logging; output to `outputs/logs/`

---

## Release & Communication Protocol

### Version Numbering
- **Semantic Versioning:** MAJOR.MINOR.PATCH (e.g., 2.0.0 = Diamond Standard release)
- **Pre-release Tags:** `-alpha`, `-beta`, `-rc` for testing releases
- **Breaking Changes:** Bump MAJOR version; document migration path

### Release Artifacts
- **GitHub Release:** Tagged commit with changelog, DOI via Zenodo integration
- **Docker Image:** Versioned container on Docker Hub/GitHub Container Registry
- **Streamlit Deployment:** Auto-deploy on main branch merge (GitHub Actions)

### Stakeholder Communication
- **Academic Audiences:** Preprints (bioRxiv/medRxiv), conference presentations
- **Policy Audiences:** Briefing papers, interactive dashboard demos
- **Public Audiences:** Plain-language summaries, media releases (via university comms)
