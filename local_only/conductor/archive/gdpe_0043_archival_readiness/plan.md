# Implementation Plan: Archival Readiness & Submission Pack

**Track ID:** gdpe_0043_archival_readiness
**Execution mode:** Fully Autonomous Batch (Unattended)

## Phase 1: Compliance Scrub (Ralph Loop #1)
- [x] **Task: Deep Exploration of Archival Integrity**
    - [x] Perform a "Ralph Thinking" session: Ask "What exactly defines the 'Reviewer-Ready' standard for a research-grade repository in 2026?"
- [x] **Task: Implement `scripts/validate_citations.py`**
- [ ] **Task: Comprehensive Path Scrub**
    - [ ] Identify and remove local STAFF OneDrive paths from loggers and metadata.
- [ ] **Task: Conductor - Autonomous Review & Remediation 'Compliance'**

## Phase 2: Submission Pack
- [ ] **Task: Implement `scripts/publish_pack.py`**
    - [ ] Script to consolidate all public artifacts, manifest, and locked env into a single ZIP.
- [ ] **Task: Supplementary Docs Generation**
    - [ ] Consolidate "Ralph Thinking" inquiry logs into a `SUPPLEMENTARY_DOCS.md`.
- [ ] **Task: Conductor - Autonomous Review & Remediation 'Packaging'**

## Phase 3: Final Verification
- [ ] **Task: Final Smoke Test (Build Docker)**
- [ ] **Task: Close Track**
