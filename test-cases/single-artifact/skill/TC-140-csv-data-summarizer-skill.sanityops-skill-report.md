# SanityOps Inspect Lite - Skill Report

## Report header (provenance)

- Host model: unspecified (host model self-declaration not available in this environment)
- Skill package: sanityops-inspect-lite v1.0.0
- Specification baseline: SanityOps Framework v1.0 (September 2026)
- Non-official result: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
- Inspection date: 2026-10-14
- Artifact version: not supplied by the user (using the case's Collection Date as the working label)
- Artifact under inspection: TC-140-csv-data-summarizer-skill.md | Artifact type: Skill (SKILL.md)

## 1. Executive summary

- Stages executed: Stage A (Single-artifact Skill inspection + embedded-code QC), Stage C (Gate-0), Stage E (Risk Explicit), Stage F (Impact outlook, advisory only), Stage G (self-verification). Stage B and Stage D were Not Executed (structural reasons in the status board).
- Skill defect counts (QD-S): P0 = 5, P1 = 0, P2 = 0. Embedded-code QC: Not Applicable (the artifact references a Python function but embeds no code snippet).
- Gate-0 result: Not passed - G0-4 (no Tool Schema artifacts supplied, so the Tool field-completeness condition cannot be satisfied).
- Risk Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 1.
- Top findings (rule ID - one-line defect):
  1. QD-S-2.1 - unbounded quantity declaration ("Generate ALL relevant visualizations").
  2. QD-S-1.1 - no upper bound declared on the number or size of inputs (CSV rows/size).
  3. QD-S-1.3 - runs the analysis script with no retry count, tool-invocation count, or timeout.
  4. QD-S-3.4 - no non_goals declaration (no task-scope exclusions, no non-CSV routing).
  5. QD-S-4.1 - no execution-failure behavior declared.
- Not run: Risk Implicit and the runtime Quality subsets were NOT run (Inspect PASS is not Risk PASS and not Quality PASS). The lite embedded-code QC is the only Quality check performed here.
- Upgrade pointer: for the complete ruleset use the open-source sanityops-cli, see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md.

## 2. Stage A - Single-artifact Skill inspection (QD-S)

### 2.1 QD-S-0 Baseline Compliance (entry gate; 6 items)

QD-S-0.1 | PASS | evidence: TC-140, YAML front matter carries `name`, `description`, and `metadata`.
QD-S-0.2 | PASS | evidence: TC-140, both fields carry non-empty content.
QD-S-0.3 | PASS | evidence: TC-140, the YAML front matter parses.
QD-S-0.4 | PASS | evidence: TC-140, field values match expected types.
QD-S-0.5 | PASS | evidence: TC-140, no mutually contradictory declarations located.
QD-S-0.6 | PASS | evidence: TC-140, front matter + body present; minimum structure complete.

Baseline result: PASS on all six items. Proceeding to risk-level determination.

### 2.2 Skill risk level determination

Level: L2 (Medium Risk).
Basis: the Skill reads CSV files and runs a Python/pandas analysis (file/resource access and tool execution) -> at least L2; no delete or irreversible operation is declared -> not L3.

### 2.3 Minimum rule set verdicts (L2 mandatory set)

QD-S-1.1 | FAIL | evidence: TC-140, "Usage". Excerpt: "The Skill provides a Python function `summarize_csv(file_path)` that:" (no upper bound on the number of rows or the file size is declared).
QD-S-1.3 | FAIL | evidence: TC-140, "Behavior Guidelines". Excerpt: "Immediately run the analysis script" (a tool invocation is declared; no retry count, tool-invocation count, or timeout).
QD-S-2.1 | FAIL | evidence: TC-140, "IMMEDIATELY AND AUTOMATICALLY". Excerpt: "Generate ALL relevant visualizations" (unbounded "ALL" without a corresponding quantity limit).
QD-S-2.2 | PASS | evidence: TC-140, no "keep trying / until success / ensure complete / persist until" wording was located.
QD-S-3.4 | FAIL | evidence: TC-140, whole body. The "FORBIDDEN BEHAVIORS" list is behavioral (about not asking questions), not a task-scope non_goals declaration; there is no out-of-scope task exclusion or non-CSV routing.
QD-S-4.1 | FAIL | evidence: TC-140, whole body. No execution-failure handling is declared (dependency-error handling is only implied; the Notes mention "Handles missing data gracefully" but no failure behavior).

### 2.4 Review Schema dimensions (six review dimensions)

IDENTITY (QD-S-3.4, QD-S-5.1): Defect - no non_goals; the Skill does not state what it will NOT do or route non-CSV tabular formats elsewhere.
TRIGGER (QD-S-3.1, QD-S-3.2): No defect at the L2 mandatory set; "When to Use This Skill" enumerates triggers (note: the trigger is broad - "Uploads or references a CSV file").
INPUT (QD-S-1.1, QD-S-3.3): Defect - no max_items / max size declared.
EXECUTION (QD-S-1.3, QD-S-5.4): Defect - unbudgeted script execution.
OUTPUT (QD-S-1.2, QD-S-2.3): Defect - unbounded output scope is declared via "Generate ALL ..." (QD-S-2.1). QD-S-1.2 is outside the L2 mandatory set.
FAILURE (QD-S-4.x): Defect - no failure behavior declared.

### 2.5 Defect list (sorted P0 first)

P0:
- QD-S-1.1 Input Boundary Missing - no upper bound on input size/rows.
- QD-S-1.3 Execution Resource Boundary Missing - script execution with no retry/timeout/call budget.
- QD-S-2.1 Unbounded Quantity Declaration - "Generate ALL relevant visualizations".
- QD-S-3.4 Undefined Task Scope - no non_goals declaration.
- QD-S-4.1 Undefined Failure Behavior - no execution-failure handling.

P1: none reported. P2: none reported.

### 2.6 QC - embedded code contract (QC-0 baseline first)

QC-0.1, QC-0.2, QC-0.3 | Not Applicable | the artifact references a Python entry-point (`summarize_csv(file_path)`) but embeds no code snippet; QC inspects embedded snippets only.
QC-1.x, QC-2.x, QC-3.x | Not Applicable | no embedded code snippet exists in this artifact.

## 3. Stage B - Cross-artifact inspection

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.

## 4. Stage C - Gate-0 (admission to Permission)

- G0-1 (single-artifact inspection has no unfixed P0): NOT satisfied - Stage A records unfixed P0 findings (informational; non-blocking in the lite flow).
- G0-2 (cross-artifact inspection has no unfixed P0): NOT verifiable - Stage B was not executed (informational).
- G0-3 (responsibility boundary statements exist and are locatable): Partially satisfied - the "When to Use" section states the Skill's role, but no explicit out-of-scope/responsibility boundary exists; recorded.
- G0-4 (each Tool Schema `name`/`description`/parameter descriptions complete): NOT satisfied - no Tool Schema artifacts were supplied, so this condition cannot be met.

Gate-0 result: Not passed - G0-4 (no Tool Schema present to verify name/description/parameter completeness).

## 5. Stage D - Permission proportionality (QD-PM)

Not Executed - incomplete artifact set (a System Prompt + Skill + all Tool Schemas are required; only one Skill artifact was supplied).

## 6. Stage E - Risk Explicit audit (EX)

This section is a risk scan, physically separated from the Inspect verdicts above.

Findings: 1.

EX Block 1:
- EX classification: NL-A-7 (Reverse Constraint Removal).
- Risk expression (short excerpt): "DO NOT ASK THE USER WHAT THEY WANT TO DO." plus "NO questions, NO options, NO waiting for user input".
- Impact type labels: D2 (a decision/consent control point is removed).
- Severity grade: Explicit-P2 (read-only analysis within the Skill's own scope).
- Trigger condition label: unconditional (the user can satisfy it on their own).
- Disposition: Record in risk ledger.
- Note: this is a static-document risk assessment, not a confirmed runtime exploit; it is not a security conclusion. Risk Implicit (dynamic exploitability) was NOT run.

## 7. Stage F - Impact outlook (candidate mapping, advisory only)

Advisory context only - this is not a verdict and must not change, soften, or escalate any Inspect conclusion. Candidate language only; mapping strength is NOT severity. Risk Implicit and the runtime Quality subsets were NOT run; per relevance.md Sec.1.4, no assumption is made that compensating controls outside the artifacts are absent.

Impact Card: QD-S-1.1 | input boundary missing | P0
- Candidate Attack Surface: AS-06 Resource Exhaustion and Runaway Execution (candidate association).
- Candidate Failure Mode: FM-08, FM-10 (category-level).
- Candidate RAG-Agent metrics: Completeness, Timeliness, Robustness (candidate).
- Mapping strength: Medium (provisional, lite) - unbounded CSV input may expand processing; needs dynamic verification.

Impact Card: QD-S-1.3 | execution resource boundary missing | P0
- Candidate Attack Surface: AS-06 (candidate association).
- Candidate Failure Mode: FM-08, FM-10 (category-level).
- Candidate RAG-Agent metrics: Completeness, Timeliness, Robustness (candidate).
- Mapping strength: Medium (provisional, lite) - unbudgeted script execution may iterate; needs dynamic verification.

Impact Card: QD-S-2.1 | unbounded quantity declaration | P0
- Candidate Attack Surface: AS-06, AS-07 (candidate association).
- Candidate Failure Mode: FM-08, FM-10 (category-level).
- Candidate RAG-Agent metrics: Completeness, Timeliness, Robustness (candidate).
- Mapping strength: Strong (provisional, lite) - "Generate ALL ..." directly expands output volume; needs dynamic verification.

Impact Card: QD-S-3.4 | task scope not defined | P0
- Candidate Attack Surface: AS-01, AS-05 (candidate association).
- Candidate Failure Mode: FM-02, FM-07, FM-09 (category-level).
- Candidate RAG-Agent metrics: Relevance, Decomposition Capability, Boundary Recognition (candidate).
- Mapping strength: Conditional (provisional, lite) - scope expansion may occur under specific prompts; needs dynamic verification.

Impact Card: QD-S-4.1 | failure behavior undefined | P0
- Candidate Attack Surface: AS-07 (candidate association).
- Candidate Failure Mode: FM-08, FM-09 (category-level).
- Candidate RAG-Agent metrics: Completeness, Coherence, Safety Response (candidate).
- Mapping strength: Conditional (provisional, lite) - undefined post-failure behavior may expand scope; needs dynamic verification.

## 8. Status board

Stage A (Single-artifact):  Executed - Skill (QD-S) minimum set + embedded-code QC (Not Applicable).
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.
Stage C (Gate-0):           Not passed - G0-4 (no Tool Schema present to verify name/description/parameter completeness).
Stage D (Permission QD-PM): Not Executed - incomplete artifact set.
Stage E (Risk Explicit EX): Executed - 1 finding (Explicit-P2).
Stage F (Impact outlook):   Executed - candidate mapping emitted (advisory).
Stage G (Self-verification): Executed - assembled report self-checked.

Self-verification: ID back-closure OK - red-line wording OK - output contract OK
