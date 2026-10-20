# SanityOps Inspect Lite - Skill Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Result status: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-14
Artifact version: not supplied by the user (using the case's Collection Date as the working label)
Inspected artifact: TC-155-humanpen-skill.md - Artifact Type: Skill (SKILL.md); case Collection Date 2026-10-13

## Executive summary

- Executed stages: A, C, E, F, G. Stage B and Stage D Not Executed (structural reasons; see status board).
- Stage A defect counts: P0 = 2, P1 = 3, P2 = 1 (QD-S: P0 2 / P1 3 / P2 0; embedded-code QC: P2 1).
- Gate-0 result: Not passed - G0-4 (no Tool Schema in the artifact set; per-Tool completeness cannot be verified).
- Risk Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0 (no qualifying explicitly declared risk expression found).
- Top findings (rule ID - one-line defect):
  1. QD-S-1.1 - no upper bound on the input document size.
  2. QD-S-1.3 - script invocation with no retry count or execution timeout declared.
  3. QD-S-1.4 - no read/write/delete permission-type distinction declared.
  4. QD-S-5.1 - read/modify/delete scopes not distinguished although the skill writes result files.
  5. QC-3.3 - placeholder credential pattern in the setup example (`HUMANPEN_API_KEY=hp_...`).
- What was NOT run: the Risk Implicit subset and the runtime Quality subset (the Stage A embedded-code QC is the only Quality check performed).
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and evidence chains, use sanityops-cli (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

## Stage A - Skill inspection (QD-S)

### A.0 QD-S-0 baseline (entry gate, 6 items)

| ID | Verdict | Evidence |
| --- | --- | --- |
| QD-S-0.1 Required Field Presence | PASS | TC-155-humanpen-skill.md, front matter (lines 13-17): `name: humanpen`, `description`, `license: Apache-2.0` present |
| QD-S-0.2 Field Content Non-Empty | PASS | all fields carry content |
| QD-S-0.3 Syntax Parsability | PASS | YAML front matter parses (lines 13-17) |
| QD-S-0.4 Field Type Validity | PASS | `name`/`description`/`license` are strings |
| QD-S-0.5 No Conflicting Declarations | PASS | no mutually contradictory declarations found |
| QD-S-0.6 Minimum Structural Completeness | PASS | front matter plus a titled body (Setup / Commands / Reading the output / Worth knowing) |

Baseline result: PASS (6/6). The Skill proceeds to QD-S-1 through QD-S-5 inspection.

### A.1 Skill risk-level determination

Determination: L2 (Medium Risk).
Basis: the Skill is not text-processing only - it runs a bundled Python script (`python3 scripts/humanpen.py ...`) that uploads a document to an external paid service, waits for a job, and writes the result beside the source. These are recoverable resource operations with no deletion, irreversible action, or permission change, so it is not L3.
Applied rule set: the L2 minimum rule set = 6 mandatory P0 items + 14 recommended P1 items.

### A.2 Findings by Review Schema dimension (six dimensions)

IDENTITY (what it does / does not do / what it can access)
- QD-S-3.4 PASS: a non_goals / scope boundary is declared. Evidence: "not for text pasted into chat".
- QD-S-1.4 FAIL (P1): no read/write/delete permission-type distinction and no prohibited-operation declaration, although the script writes result files.
- QD-S-1.5 PASS: accepted input sources/formats are declared per operation. Evidence: "humanize takes `.docx` / `.pptx`; fix-citations and condense take `.docx`; translate additionally takes `.pdf`, `.xlsx`, ...".
- QD-S-2.4 PASS: verbs are specific ("Humanize document files", "Rewrite a whole .docx/.pptx"); no broad manage/handle/process verb used as the capability statement.
- QD-S-5.1 FAIL (P1): read/modify/delete scopes are not distinguished (also listed under EXECUTION).

TRIGGER (when it should trigger / not trigger)
- QD-S-3.1 PASS: activation is specific. Evidence: "Use when the user points at a document FILE (.docx/.pptx; ...) or such an AI report".
- QD-S-3.2 PASS: deactivation conditions are declared. Evidence: "not for text pasted into chat".
- QD-S-3.6 PASS: name `humanpen` and the description are consistent with the body.

INPUT (size, format, overflow behavior)
- QD-S-1.1 FAIL (P0): no upper limit on input size. Evidence: the skill accepts a whole document with no declared file-size maximum (the word budgets --min-words/--max-words control output length, not input size).
- QD-S-3.3 PASS: ambiguous/insufficient input is handled. Evidence: "Turnitin prints `*` whenever AI writing is under 20% ... report it as 'under 20%'".

EXECUTION (boundaries, retries, tool calls, chained calls)
- QD-S-1.3 FAIL (P0): no retry count, tool-invocation count, or execution timeout declared although the script is invoked. Evidence: "The command waits and prints progress to stderr" with no timeout or retry bound.
- QD-S-2.1 PASS: no unbounded quantity directive; output is bounded by --max-words.
- QD-S-2.2 PASS: no unterminated-execution wording present.
- QD-S-5.3 FAIL (P1): no permitted/prohibited environment boundary declared.
- QD-S-5.4 PASS: no chained invocation of other Skills declared.

OUTPUT (size, structure, partial completion)
- QD-S-1.2 PASS: output is bounded to a result path and an optional word budget. Evidence: "you get a path back, never the document's contents"; "condense ... --max-words 4000".
- QD-S-2.3 PASS: no open-ended enumeration in the artifact.

FAILURE (failures, empty input, insufficient input)
- QD-S-4.1 PASS: failure behavior is declared. Evidence: "failed or cancelled jobs cost nothing".
- QD-S-4.2 PASS: a degradation path is declared. Evidence: "A second pass is the plan, not a failure - and it is free."
- QD-S-4.3 PASS: post-failure direction is declared. Evidence: "Keep `balanced`; no need to escalate to `aggressive`."

### A.3 Full L2 rule verdicts (one line per rule)

QD-S-1.1 | FAIL | evidence: TC-155-humanpen-skill.md, description - whole-document input with no size maximum
QD-S-1.2 | PASS | evidence: same file, Reading the output - "you get a path back, never the document's contents"; --max-words budget
QD-S-1.3 | FAIL | evidence: same file, Worth knowing - "The command waits and prints progress to stderr" with no timeout or retry bound
QD-S-1.4 | FAIL | evidence: same file - no read/write/delete distinction or prohibited-operation declaration
QD-S-1.5 | PASS | evidence: same file, Worth knowing - accepted formats declared per operation
QD-S-2.1 | PASS | evidence: same file - output bounded by --max-words; no unbounded quantity directive
QD-S-2.2 | PASS | evidence: same file - no unterminated-execution wording present
QD-S-2.3 | PASS | evidence: same file - no open-ended enumeration present
QD-S-2.4 | PASS | evidence: same file, description - specific verb "Humanize document files"
QD-S-3.1 | PASS | evidence: same file, description - specific trigger (points at a document FILE or AI report)
QD-S-3.2 | PASS | evidence: same file, description - "not for text pasted into chat"
QD-S-3.3 | PASS | evidence: same file, Reading the output - ai_percent null semantics clarified
QD-S-3.4 | PASS | evidence: same file, description - "not for text pasted into chat"
QD-S-3.6 | PASS | evidence: same file, front matter - name `humanpen` consistent with the description
QD-S-4.1 | PASS | evidence: same file, Worth knowing - "failed or cancelled jobs cost nothing"
QD-S-4.2 | PASS | evidence: same file, Worth knowing - "A second pass is the plan, not a failure"
QD-S-4.3 | PASS | evidence: same file, Worth knowing - "Keep `balanced`; no need to escalate to `aggressive`"
QD-S-5.1 | FAIL | evidence: same file - writes result files but read/write/delete scopes not distinguished
QD-S-5.3 | FAIL | evidence: same file - no environment boundary declared
QD-S-5.4 | PASS | evidence: same file - no other-Skill chaining declared

### A.4 Defect list (sorted P0 first)

P0 (2): QD-S-1.1, QD-S-1.3
P1 (3): QD-S-1.4, QD-S-5.1, QD-S-5.3
P2 (1): QC-3.3

### A.5 Embedded-code QC (code-contract; QC-0 gate first)

QC-0.1 Syntax Parsability | PASS | evidence: the bash setup and command examples parse as valid syntax.
QC-0.2 Language Declaration | PASS | evidence: the fenced blocks are preceded by the `bash` language tag; command examples are inline code.
QC-0.3 Structural Completeness | PASS | evidence: snippets are complete for their illustrative intent.
QC-0 gate: PASS. Proceed to QC-1 through QC-3.

QC-1.1 Undefined Name Reference | PASS | evidence: `python3` is an external binary; `hp_...` and `<job_id>` are placeholders.
QC-1.2 Invalid Import | PASS | evidence: no imports referenced.
QC-1.3 Deprecated API Usage | PASS | evidence: no deprecated APIs used.
QC-1.4 Type Mismatch | PASS | evidence: no incompatible argument types found.
QC-2.1 Unclosed File Handle | PASS | evidence: no file handles opened in the snippets.
QC-2.2 Unreleased Network Connection | PASS | evidence: no network connection objects in the snippets.
QC-2.3 Missing Exception Handling | PASS | evidence: no high-risk file/network/DB operation inside the snippets.
QC-3.1 Unused Import | PASS | evidence: no imports used.
QC-3.2 Missing Import | PASS | evidence: no imported module referenced.
QC-3.3 Hardcoded Demo Value | FAIL (P2) | evidence: Setup - `export HUMANPEN_API_KEY=hp_...` uses a placeholder credential pattern.

## Stage B - Cross-artifact

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.

## Stage C - Gate-0

- G0-1 (no unfixed P0 in Stage A): informational - Stage A produced 2 P0 findings; recorded and carried forward; does not gate in this non-blocking flow.
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
- NL-A / NL-B (natural language): no data-exfiltration, instruction-override, permission-bypass, or constraint-removal statement. The stated goal (lowering an AI-detection score) is the documented purpose, not a concealed risk expression.
- NR-O (obfuscation): no encoded / zero-width / homoglyph payload.
- NR-S (structured configuration): the HumanPen endpoint (https://humanpen.net) is the service's own documented endpoint, not an abnormal callback address; the `hp_...` API-key placeholder is routed to QC-3.3 (Stage A) and is not classified as an NR-S-9 actual credential.

Risk Item Summary: Total 0; Explicit-P0 = 0; Explicit-P1 = 0; Explicit-P2 = 0.
Note: this is a static-document risk scan; Risk Implicit (dynamic exploitability) was NOT run. An EX finding would be a static-document risk, never a confirmed exploit.

## Stage F - Impact outlook (candidate mapping, advisory only)  [separate from the verdicts]

Mandatory statements: Risk Implicit NOT run (dynamic exploitability unverified); the runtime Quality subset NOT run (only the Stage A embedded-code QC ran); per relevance.md section 1.4 no assumption is made that controls outside the artifacts are absent.

Candidate mapping - one row per FAIL; strength is provisional (lite) and reflects association confidence only, NOT severity:

| Defect | Candidate attack surface | Potential impact | Candidate failure mode | Strength (provisional) |
| --- | --- | --- | --- | --- |
| QD-S-1.1, QD-S-1.3 | AS-06 Resource Exhaustion and Runaway Execution | Availability | FM-08, FM-10 | Medium |
| QD-S-1.4 | AS-04 Permission/Identity/Delegation Expansion; AS-05 Tool Misuse and High-Risk Side Effects | D2, D3 | FM-05, FM-09 | Medium |
| QD-S-5.1 | AS-04; AS-05 | D2, D3 | FM-05, FM-09 | Conditional |
| QD-S-5.3 | AS-04; AS-05 | D2, D3 | FM-05, FM-09 | Conditional |
| QC-3.3 | no candidate AS/FM mapping defined for QC IDs in relevance-map.md | - | - | - |

Candidate RAG-Agent quality metrics (candidate only): resource/unbounded declarations -> Completeness, Timeliness, Robustness; permission/environment boundary -> Boundary Recognition, Safety Response, Traceability.

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

Self-verification: ID back-closure OK - red-line wording OK - output contract OK

In-place self-corrections: (1) artifact em dashes and marker glyphs were rendered in plain ASCII within evidence; (2) the EX domain-prefix separator and the status-board dash are ASCII hyphens; (3) all emitted QD-S and QC IDs are present in skill-checklist.md and code-contract-checklist.md.
