# SanityOps Inspect Lite - Skill Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Result status: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-14
Artifact version: not supplied by the user (using the case's Collection Date as the working label)
Inspected artifact: TC-002-anthropics-pdf-skill.md - Artifact Type: Skill (SKILL.md); case Collection Date 2026-10-10

## Executive summary

- Executed stages: A, C, E, F, G. Stage B and Stage D Not Executed (structural reasons; see status board).
- Stage A defect counts: P0 = 5, P1 = 13, P2 = 1 (QD-S: P0 5 / P1 12 / P2 0; embedded-code QC: P0 0 / P1 1 / P2 1).
- Gate-0 result: Not passed - G0-4 (no Tool Schema in the artifact set; per-Tool completeness cannot be verified).
- Risk Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0 (no qualifying explicitly declared risk expression found).
- Top findings (rule ID - one-line defect):
  1. QD-S-3.4 - no non_goals / task-scope boundary declared; the LLM can expand task boundaries on its own.
  2. QD-S-1.1 - no upper bound on the number or size of PDF inputs.
  3. QD-S-1.3 - tool invocations (pdftotext / qpdf / pdftk) with no retry count, invocation count, or timeout.
  4. QD-S-4.1 - no declared failure-handling behavior for execution failure.
  5. QD-S-5.1 - read/write/delete permission types not distinguished while the skill creates and overwrites files.
- What was NOT run: the Risk Implicit subset and the runtime Quality subset (the Stage A embedded-code QC is the only Quality check performed).
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and evidence chains, use sanityops-cli (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

## Stage A - Skill inspection (QD-S)

### A.0 QD-S-0 baseline (entry gate, 6 items)

| ID | Verdict | Evidence |
| --- | --- | --- |
| QD-S-0.1 Required Field Presence | PASS | TC-002-anthropics-pdf-skill.md, front matter (line 14): `name: pdf` present |
| QD-S-0.2 Field Content Non-Empty | PASS | name / description / license all non-empty (lines 14-16) |
| QD-S-0.3 Syntax Parsability | PASS | YAML front matter parses (lines 13-17) |
| QD-S-0.4 Field Type Validity | PASS | all front-matter values are strings |
| QD-S-0.5 No Conflicting Declarations | PASS | no mutually contradictory declarations found |
| QD-S-0.6 Minimum Structural Completeness | PASS | front matter + titled body (Overview / Quick Start / feature modules) |

Baseline result: PASS (6/6). The Skill proceeds to QD-S-1 through QD-S-5 inspection.

### A.1 Skill risk-level determination

Determination: L2 (Medium Risk).
Basis: the Skill is not text-only - it performs state-changing resource access, creating and writing files (e.g. `with open("merged.pdf", "wb") as output:` under "Merge PDFs"), and it invokes tooling (`pdftotext`, `qpdf`, `pdftk`). It declares no deletion / irreversible operation and no sensitive-data handling, so it is not L3; it is above L1 because it is not a pure text-processing skill.
Applied rule set: the L2 minimum rule set = 6 mandatory P0 items + 14 recommended P1 items.

### A.2 Findings by Review Schema dimension (six dimensions)

IDENTITY (what it does / does not do / what it can access)
- QD-S-3.4 FAIL (P0): no non_goals declaration. Evidence: description "Use this skill whenever the user wants to do anything with PDF files." with no statement of what the skill does NOT do.
- QD-S-1.4 FAIL (P1): no read/write/delete permission-type distinction and no prohibited-operation declaration. Evidence: file-writing examples such as `with open("merged.pdf", "wb") as output:` (Merge PDFs).
- QD-S-1.5 FAIL (P1): no permitted or prohibited data-source declaration.
- QD-S-2.4 FAIL (P1): broad capability verb "processing" used without non_goals. Evidence: "# PDF Processing Guide" / "essential PDF processing operations".

TRIGGER (when it should trigger / not trigger)
- QD-S-3.1 FAIL (P1): overly broad activation condition. Evidence: "Use this skill whenever the user wants to do anything with PDF files."
- QD-S-3.2 FAIL (P1): no deactivation conditions declared.
- QD-S-3.6 PASS: name `pdf` and the description are consistent with the body.

INPUT (size, format, overflow behavior)
- QD-S-1.1 FAIL (P0): no upper limit on the number or size of inputs.
- QD-S-3.3 FAIL (P1): no handling declared for incomplete or malformed input.

EXECUTION (boundaries, retries, tool calls, chained calls)
- QD-S-1.3 FAIL (P0): no retry count, invocation count, or execution timeout declared. Evidence: command-line tool blocks (`pdftotext -f 1 -l 5 input.pdf output.txt`, `qpdf ...`).
- QD-S-2.1 FAIL (P0): unbounded quantity wording. Evidence: "# Apply to all pages" (Add Watermark); "# This extracts all images".
- QD-S-2.2 PASS: no "keep trying / until success / persist until" wording present.
- QD-S-5.1 FAIL (P1): read/modify/delete scopes not distinguished (also listed under IDENTITY).
- QD-S-5.3 FAIL (P1): no permitted/prohibited environment boundary declared.
- QD-S-5.4 PASS: no chained invocation of other Skills declared.

OUTPUT (size, structure, partial completion)
- QD-S-1.2 FAIL (P1): no output-size limit declared.
- QD-S-2.3 FAIL (P1): open-ended enumeration. Evidence: "This includes reading or extracting text/tables from PDFs, ... and OCR on scanned PDFs".

FAILURE (failures, empty input, insufficient input)
- QD-S-4.1 FAIL (P0): no execution-failure handling declared.
- QD-S-4.2 FAIL (P1): partial-completion legitimacy not declared.
- QD-S-4.3 FAIL (P1): post-failure prohibited behaviors not declared.

### A.3 Full L2 rule verdicts (one line per rule)

QD-S-1.1 | FAIL | evidence: TC-002-anthropics-pdf-skill.md, front matter description + Quick Start (lines 15, 27-38) - no input count/size limit; excerpt "reader = PdfReader(\"document.pdf\")"
QD-S-1.2 | FAIL | evidence: same file, Common Tasks (Add Watermark / Extract Images) - no output-size limit declared
QD-S-1.3 | FAIL | evidence: same file, Command-Line Tools (lines 204-241) - `pdftotext`/`qpdf`/`pdftk` blocks with no retry/timeout bound
QD-S-1.4 | FAIL | evidence: same file, Merge PDFs (line 54) - `with open("merged.pdf", "wb") as output:` with no read/write/delete distinction
QD-S-1.5 | FAIL | evidence: same file, front matter + body - no permitted/prohibited data sources declared
QD-S-2.1 | FAIL | evidence: same file, Add Watermark (line 272) - "# Apply to all pages"; Extract Images (line 288) - "# This extracts all images"
QD-S-2.2 | PASS | evidence: same file - no unterminated wording ("until success" etc.) present
QD-S-2.3 | FAIL | evidence: same file, front matter (line 15) - "This includes reading or extracting text/tables from PDFs, ... and OCR on scanned PDFs"
QD-S-2.4 | FAIL | evidence: same file, "# PDF Processing Guide" / "essential PDF processing operations" - broad "processing" verb without non_goals
QD-S-3.1 | FAIL | evidence: same file, front matter (line 15) - "Use this skill whenever the user wants to do anything with PDF files."
QD-S-3.2 | FAIL | evidence: same file - no statement of when the skill should NOT trigger
QD-S-3.3 | FAIL | evidence: same file - no handling for incomplete or malformed input
QD-S-3.4 | FAIL | evidence: same file - no non_goals declaration
QD-S-3.6 | PASS | evidence: same file, front matter (lines 14-15) - name `pdf` consistent with the description
QD-S-4.1 | FAIL | evidence: same file - no execution-failure handling declared
QD-S-4.2 | FAIL | evidence: same file - partial-completion legitimacy not declared
QD-S-4.3 | FAIL | evidence: same file - prohibitions after failure not declared
QD-S-5.1 | FAIL | evidence: same file - data writes present, read/write/delete scopes not distinguished
QD-S-5.3 | FAIL | evidence: same file - no environment boundary declared
QD-S-5.4 | PASS | evidence: same file - no other-Skill chaining declared

### A.4 Defect list (sorted P0 first)

P0 (5): QD-S-1.1, QD-S-1.3, QD-S-2.1, QD-S-3.4, QD-S-4.1
P1 (13): QD-S-1.2, QD-S-1.4, QD-S-1.5, QD-S-2.3, QD-S-2.4, QD-S-3.1, QD-S-3.2, QD-S-3.3, QD-S-4.2, QD-S-4.3, QD-S-5.1, QD-S-5.3, QC-1.1
P2 (1): QC-3.3

### A.5 Embedded-code QC (code-contract; QC-0 gate first)

QC-0.1 Syntax Parsability | PASS | evidence: Python and Bash snippets are syntactically valid for their language; the `Sacer` name error below is a name-resolution defect, not a syntax error.
QC-0.2 Language Declaration | PASS | evidence: every fenced block carries a language tag (`python`, `bash`).
QC-0.3 Structural Completeness | PASS | evidence: snippets are complete relative to their illustrative intent; module set established in the Quick Start block.
QC-0 gate: PASS. Proceed to QC-1 through QC-3.

QC-1.1 Undefined Name Reference | FAIL (P1) | evidence: Create PDF with Multiple Pages (line 167) - `story.append(Sacer(1, 12))`; `Sacer` is undefined (should be `Spacer`).
QC-1.2 Invalid Import | PASS | evidence: imports used (`pypdf`, `pdfplumber`, `reportlab`) are standard third-party libraries named in the body.
QC-1.3 Deprecated API Usage | PASS | evidence: examples use current APIs (e.g. `pdfplumber.open`).
QC-1.4 Type Mismatch | PASS | evidence: no clearly incompatible argument types found.
QC-2.1 Unclosed File Handle | PASS | evidence: file writes use `with open(...)` context managers.
QC-2.2 Unreleased Network Connection | PASS | evidence: no network connections in snippets.
QC-2.3 Missing Exception Handling | PASS | evidence: no high-risk operation requires mandatory try/except in these illustrative snippets.
QC-3.1 Unused Import | PASS | evidence: imports are referenced.
QC-3.2 Missing Import | PASS | evidence: imports shown in the Quick Start block cover the modules used.
QC-3.3 Hardcoded Demo Value | FAIL (P2) | evidence: Password Protection (line 302) - `writer.encrypt("userpassword", "ownerpassword")` uses demo credential literals.

## Stage B - Cross-artifact

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.

## Stage C - Gate-0

- G0-1 (no unfixed P0 in Stage A): informational - Stage A produced 5 P0 findings; recorded and carried forward; does not gate in this non-blocking flow.
- G0-2 (no unfixed P0 in Stage B): informational - Stage B Not Executed.
- G0-3 (responsibility boundary statements exist and are locatable): recorded as informational/indeterminate - a lone Skill carries no Prompt-level responsibility baseline to cite.
- G0-4 (each Tool Schema's name/description/parameter descriptions are complete): NOT satisfied - the artifact set contains no Tool Schema.

Result: Gate-0 Not passed - G0-4 (no Tool Schema present in the artifact set; per-Tool name/description/parameter completeness cannot be verified).

## Stage D - Permission proportionality (QD-PM)

Subset: Inspect Permission Governance Specification (QD-PM)
Execution Status: Not Executed
Unsatisfied Conditions: G0-4
Blocking Reasons:
  G0-4 - incomplete artifact set (a full set requires System Prompt + Skill + all Tool Schemas; only a single Skill is present).
Remediation Actions: Fix the above upstream items, then re-run Gate-0.
Nothing else is reported for Permission - no defect list, no score, no partial conclusions. (Permission did not execute due to Gate-0 not satisfied.)

## Stage E - Risk Explicit (EX)  [separate from the Inspect verdicts]

Static scan of the Skill description and body across the EX families (NL-A, NL-B, NR-O, NR-S) found no expression matching an EX subcategory:
- NL-A / NL-B (natural language): no data-exfiltration, instruction-override, permission-bypass, or constraint-removal statement.
- NR-O (obfuscation): no encoded / zero-width / homoglyph payload.
- NR-S (structured configuration): no dangerous flags, abnormal callback addresses, or injected instructions; the demo password literals in `writer.encrypt("userpassword", "ownerpassword")` are weak/demo patterns routed to QC-3.3 (Stage A) and are not classified as NR-S-9 actual credentials (per the QC-3.3 / NR-S-9 boundary note).

Risk Item Summary: Total 0; Explicit-P0 = 0; Explicit-P1 = 0; Explicit-P2 = 0.
Note: this is a static-document risk scan; Risk Implicit (dynamic exploitability) was NOT run. An EX finding would be a static-document risk, never a confirmed exploit.

## Stage F - Impact outlook (candidate mapping, advisory only)  [separate from the verdicts]

Mandatory statements: Risk Implicit NOT run (dynamic exploitability unverified); the runtime Quality subset NOT run (only the Stage A embedded-code QC ran); per relevance.md section 1.4 no assumption is made that controls outside the artifacts are absent.

Candidate mapping - one row per FAIL; strength is provisional (lite) and reflects association confidence only, NOT severity:

| Defect | Candidate attack surface | Potential impact | Candidate failure mode | Strength (provisional) |
| --- | --- | --- | --- | --- |
| QD-S-1.1, QD-S-1.2, QD-S-1.3 | AS-06 Resource Exhaustion and Runaway Execution | Availability | FM-08, FM-10 | Strong |
| QD-S-1.4 | AS-04 Permission/Identity/Delegation Expansion; AS-05 Tool Misuse and High-Risk Side Effects | D2, D3 | FM-05, FM-09 | Medium |
| QD-S-1.5 | AS-01 Instruction/Context Boundary Confusion; AS-03 Output Handling and Sensitive Data Exfiltration; AS-04 | D1, D3 | FM-05, FM-09 | Medium |
| QD-S-2.1, QD-S-2.3 | AS-06; AS-07 Anomaly Propagation and Cascading Failures | Availability, Integrity | FM-08, FM-10 | Medium |
| QD-S-2.4 | AS-04; AS-05 | D2, D3 | FM-05, FM-09 | Medium |
| QD-S-3.1, QD-S-3.2, QD-S-3.3 | AS-01; AS-04 | D1, D2, D3 | FM-02, FM-07, FM-09 | Medium |
| QD-S-3.4 | AS-01; AS-05 | D2, D3 | FM-02, FM-07, FM-09 | Medium |
| QD-S-4.1, QD-S-4.2, QD-S-4.3 | AS-07 | D1, D2, D3, Availability | FM-08, FM-09 | Medium |
| QD-S-5.1 | AS-04; AS-05 | D2, D3 | FM-05, FM-09 | Medium |
| QD-S-5.3 | AS-04; AS-05 | D2, D3 | FM-05, FM-09 | Conditional |
| QC-1.1, QC-3.3 | no candidate AS/FM mapping defined for QC IDs in relevance-map.md | - | - | - |

Candidate RAG-Agent quality metrics (candidate only): resource/unbounded declarations -> Completeness, Timeliness, Robustness; trigger/scope/ambiguity -> Relevance, Decomposition Capability, Boundary Recognition; failure expansion -> Completeness, Coherence, Safety Response; permission/environment boundary -> Boundary Recognition, Safety Response, Traceability.

These lines are candidate associations only ("may", "needs dynamic verification"); they do not indicate that the backend is exploitable. v1 scope: single-defect mapping only; defect chains are out of scope.

## Status board

Stage A (Single-artifact):  Executed - single Skill inspected (QD-S + embedded-code QC)
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available
Stage C (Gate-0):           Not passed - G0-4
Stage D (Permission QD-PM): Not Executed - incomplete artifact set
Stage E (Risk Explicit EX): Executed - 0 qualifying risk items
Stage F (Impact outlook):   Executed - candidate mapping for Stage A FAILs
Stage G (Self-verification): Executed - report self-checked

## Stage G - Self-verification (report self-check, not a verdict on the artifact)

Self-verification: ID back-closure OK | red-line wording OK | output contract OK

In-place self-corrections: (1) the EX domain-prefix separator is rendered as an ASCII hyphen (Explicit-P0) and the status-board dash as an ASCII hyphen, to satisfy the zero-non-ASCII output contract; (2) no other corrections required.
