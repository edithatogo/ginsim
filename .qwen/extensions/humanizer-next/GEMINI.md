# Humanizer-next Extension for Gemini CLI

This extension provides academic writing refinement and reference validation for research projects.

## Commands

### /humanize
Refines AI-generated text to sound more natural and academic.

**Usage:** `/humanize <text>` or `/humanize --file <path>`

**Options:**
- `--tone`: Set tone (academic, policy, technical, plain-language)
- `--audience`: Target audience (researchers, policymakers, general public)
- `--check-references`: Validate citations against bibliography

### /check-references
Validates references and citations in the project.

**Checks performed:**
1. All in-text citations have matching bibliography entries
2. All bibliography entries are complete (author, year, title, journal/DOI)
3. DOI resolution check (optional, requires internet)
4. Duplicate detection
5. Orphaned bibliography entries (in bibliography but not cited)

**Usage:**
- `/check-references` — Full validation
- `/check-references --fix` — Auto-fix common issues
- `/check-references --report` — Generate validation report

### /polish-paragraph
Refines a single paragraph for academic writing quality.

**Checks:**
- Sentence structure variety
- Passive vs active voice balance
- Hedging language appropriateness
- Transition words
- Paragraph coherence

---

## Reference Validation Pipeline

The reference checking pipeline integrates with the project's `context/references.bib` file.

### Validation Rules

1. **Citation Completeness**
   - Required fields: author, year, title
   - At least one of: journal, doi, publisher, url

2. **DOI Validation**
   - Format check: `10.xxxx/xxxxx`
   - Resolution check (optional API call to doi.org)

3. **Author Name Consistency**
   - Detects variations (e.g., "Smith J" vs "Smith, John")
   - Suggests standardization

4. **Journal Name Standardization**
   - Converts abbreviations to full names (or vice versa)
   - Checks against ISSN registry

5. **Duplicate Detection**
   - Identifies duplicate entries by DOI or title similarity
   - Suggests merges

### Output Formats

- **Console report:** Quick summary with issues
- **Markdown report:** Detailed validation report
- **Fixed BibTeX:** Auto-corrected bibliography

---

## Integration with Conductor Tracks

Humanizer-next integrates with Conductor phase reviews:

1. **Automatic trigger:** At end of each phase, run `/check-references`
2. **Blocker detection:** Critical reference issues block phase completion
3. **Auto-fix:** Common issues fixed automatically before review

---

## Configuration

Edit `.qwen/extensions/humanizer-next/config.yaml`:

```yaml
tone: academic
audience: researchers
check_references_on_phase_complete: true
auto_fix_common_issues: true
doi_validation: true
journal_standardization: iso4  # or 'full'
```

---

## Example Workflow

```bash
# During writing
/humanize --tone academic --audience researchers <draft_text>

# Before phase completion
/check-references --report

# Auto-fix and generate clean bibliography
/check-references --fix --output context/references_clean.bib

# Polish specific section
/polish-paragraph --file docs/POLICY_BRIEF_DRAFT.md --section executive_summary
```

---

## Dependencies

- Python 3.10+
- `bibtexparser` or `bibtex-tidy`
- `requests` (for DOI validation)
- `habanero` (CrossRef API access)

Install:
```bash
pip install bibtex-tidy habanero requests
```
