# SanityOps Inspect Lite - Skill Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Result status: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-14
Artifact version: not supplied by the user (using the case's Collection Date as the working label)
Inspected artifact: TC-154-equalang-skill.md - Artifact Type: Skill (SKILL.md); case Collection Date 2026-10-13

## Executive summary

- Executed stages: A, C, E, F, G. Stage B and Stage D Not Executed (structural reasons; see status board).
- Stage A defect counts: P0 = 1, P1 = 3, P2 = 1 (QD-S: P0 1 / P1 3 / P2 0; embedded-code QC: P2 1).
- Gate-0 result: Not passed - G0-4 (no Tool Schema in the artifact set; per-Tool completeness cannot be verified).
- Risk Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0 (no qualifying explicitly declared risk expression found).
- Top findings (rule ID - one-line defect):
  1. QD-S-1.3 - script invocation with no retry count or execution timeout declared.
  2. QD-S-1.4 - no read/write/delete permission-type distinction declared.
  3. QD-S-5.1 - read/modify/delete scopes not distinguished although the skill writes result files.
  4. QC-3.3 - placeholder credential pattern in the setup example (`EQUALANG_API_KEY=el_...`).
  5. QD-S-5.3 - no environment boundary declared.
- What was NOT run: the Risk Implicit subset and the runtime Quality subset (the Stage A embedded-code QC is the only Quality check performed).
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and evidence chains, use sanityops-cli (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

## Stage A - Skill inspection (QD-S)

### A.0 QD-S-0 baseline (entry gate, 6 items)

| ID | Verdict | Evidence |
| --- | --- | --- |
| QD-S-0.1 Required Field Presence | PASS | TC-154-equalang-skill.md, front matter (lines 13-16): `name: equalang`, `description`, `license: Apache-2.0` present |
| QD-S-0.2 Field Content Non-Empty | PASS | all fields carry content |
| QD-S-0.3 Syntax Parsability | PASS | YAML front matter parses (lines 13-16) |
| QD-S-0.4 Field Type Validity | PASS | `name`/`description`/`license` are strings |
| QD-S-0.5 No Conflicting Declarations | PASS | no mutually contradictory declarations found |
| QD-S-0.6 Minimum Structural Completeness | PASS | front matter plus a titled body (Setup / Commands / Reading the output / Worth knowing) |

Baseline result: PASS (6/6). The Skill proceeds to QD-S-1 through QD-S-5 inspection.

### A.1 Skill risk-level determination

Determination: L2 (Medium Risk).
Basis: the Skill is not text-processing only - it runs a bundled Python script (`python3 scripts/equalang.py ...`) that uploads files to an external paid service, waits for a job, and writes result files beside the source. These are recoverable resource operations with no deletion, irreversible action, or permission change, so it is not L3.
Applied rule set: the L2 minimum rule set = 6 mandatory P0 items + 14 recommended P1 items.

### A.2 Findings by Review Schema dimension (six dimensions)

IDENTITY (what it does / does not do / what it can access)
- QD-S-3.4 PASS: a non_goals / scope boundary is declared. Evidence: "not for a sentence you can translate yourself".
- QD-S-1.4 FAIL (P1): no read/write/delete permission-type distinction and no prohibited-operation declaration, although the script writes result files.
- QD-S-1.5 PASS: accepted input sources are declared. Evidence: "A path, a public URL (Equalang fetches it), or --file-id from estimate".
- QD-S-2.4 PASS: verbs are specific ("Translate whole files", "transcribe recordings"); no broad manage/handle/process verb used as the capability statement.
- QD-S-5.1 FAIL (P1): read/modify/delete scopes are not distinguished (also listed under EXECUTION).

TRIGGER (when it should trigger / not trigger)
- QD-S-3.1 PASS: activation is specific. Evidence: "Use when the user points at a FILE or a URL of one and wants it translated or transcribed".
- QD-S-3.2 PASS: deactivation conditions are declared. Evidence: "not for a sentence you can translate yourself".
- QD-S-3.6 PASS: name `equalang` and the description are consistent with the body.

INPUT (size, format, overflow behavior)
- QD-S-1.1 PASS: input limits are declared. Evidence: "at most 50 of 5,000 characters, 20,000 per call"; "up to 100,000 characters"; "Up to 100 MB".
- QD-S-3.3 PASS: insufficient/ambiguous input is handled. Evidence: "Without a key every command answers with how to get one and where it goes".

EXECUTION (boundaries, retries, tool calls, chained calls)
- QD-S-1.3 FAIL (P0): no retry count, tool-invocation count, or execution timeout declared although the script is invoked. Evidence: "Retry only when `retryable` is true" states a policy but declares no count or timeout.
- QD-S-2.1 PASS: no unbounded quantity directive; input caps are declared.
- QD-S-2.2 PASS: no unterminated-execution wording present.
- QD-S-5.3 FAIL (P1): no permitted/prohibited environment boundary declared.
- QD-S-5.4 PASS: no chained invocation of other Skills declared.

OUTPUT (size, structure, partial completion)
- QD-S-1.2 PASS: output is bounded to file paths. Evidence: "You get paths back, never the file's contents".
- QD-S-2.3 PASS: no open-ended enumeration in the artifact.

FAILURE (failures, empty input, insufficient input)
- QD-S-4.1 PASS: failure behavior is declared. Evidence: "A failure prints `{\"error\", \"code\", \"retryable\"}` and exits 1."
- QD-S-4.2 PASS: partial-completion legitimacy is declared. Evidence: "A cancelled or failed job is not charged."
- QD-S-4.3 PASS: post-failure prohibitions are declared. Evidence: "Retry only when `retryable` is true; `INSUFFICIENT_CREDITS` means the user tops up ..., not that you try again."

### A.3 Full L2 rule verdicts (one line per rule)

QD-S-1.1 | PASS | evidence: TC-154-equalang-skill.md, Commands - "at most 50 of 5,000 characters, 20,000 per call"; "Up to 100 MB"
QD-S-1.2 | PASS | evidence: same file, Reading the output - "You get paths back, never the file's contents"
QD-S-1.3 | FAIL | evidence: same file, Reading the output - retry policy stated but no retry count or execution timeout
QD-S-1.4 | FAIL | evidence: same file - no read/write/delete distinction or prohibited-operation declaration
QD-S-1.5 | PASS | evidence: same file, Commands - accepted inputs declared (path, public URL, --file-id)
QD-S-2.1 | PASS | evidence: same file - input caps declared; no unbounded quantity directive
QD-S-2.2 | PASS | evidence: same file - no unterminated-execution wording present
QD-S-2.3 | PASS | evidence: same file - no open-ended enumeration present
QD-S-2.4 | PASS | evidence: same file, description - specific verb "Translate whole files"
QD-S-3.1 | PASS | evidence: same file, description - specific trigger (points at a FILE or URL)
QD-S-3.2 | PASS | evidence: same file, description - "not for a sentence you can translate yourself"
QD-S-3.3 | PASS | evidence: same file, Setup - "Without a key every command answers with how to get one"
QD-S-3.4 | PASS | evidence: same file, description - "not for a sentence you can translate yourself"
QD-S-3.6 | PASS | evidence: same file, front matter - name `equalang` consistent with the description
QD-S-4.1 | PASS | evidence: same file, Reading the output - error object with `code` and `retryable`
QD-S-4.2 | PASS | evidence: same file, Worth knowing - "A cancelled or failed job is not charged"
QD-S-4.3 | PASS | evidence: same file, Reading the output - "Retry only when `retryable` is true"
QD-S-5.1 | FAIL | evidence: same file - writes result files but read/write/delete scopes not distinguished
QD-S-5.3 | FAIL | evidence: same file - no environment boundary declared
QD-S-5.4 | PASS | evidence: same file - no other-Skill chaining declared

### A.4 Defect list (sorted P0 first)

P0 (1): QD-S-1.3
P1 (3): QD-S-1.4, QD-S-5.1, QD-S-5.3
P2 (1): QC-3.3

### A.5 Embedded-code QC (code-contract; QC-0 gate first)

QC-0.1 Syntax Parsability | PASS | evidence: the bash setup block and command examples parse as valid syntax.
QC-0.2 Language Declaration | PASS | evidence: the fenced blocks carry the `bash` language tag.
QC-0.3 Structural Completeness | PASS | evidence: snippets are complete for their illustrative intent.
QC-0 gate: PASS. Proceed to QC-1 through QC-3.

QC-1.1 Undefined Name Reference | PASS | evidence: `python3` is an external binary; `el_...` and `<file_id>` are placeholders.
QC-1.2 Invalid Import | PASS | evidence: no imports referenced.
QC-1.3 Deprecated API Usage | PASS | evidence: no deprecated APIs used.
QC-1.4 Type Mismatch | PASS | evidence: no incompatible argument types found.
QC-2.1 Unclosed File Handle | PASS | evidence: the setup block uses `umask 077` and a redirection, not an unclosed handle.
QC-2.2 Unreleased Network Connection | PASS | evidence: no network connection objects in the snippets.
QC-2.3 Missing Exception Handling | PASS | evidence: no high-risk file/network/DB operation inside the snippets.
QC-3.1 Unused Import | PASS | evidence: no imports used.
QC-3.2 Missing Import | PASS | evidence: no imported module referenced.
QC-3.3 Hardcoded Demo Value | FAIL (P2) | evidence: Setup - `echo 'EQUALANG_API_KEY=el_...'` uses a placeholder credential pattern.

## Stage B - Cross-artifact

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.

## Stage C - Gate-0

- G0-1 (no unfixed P0 in Stage A): informational - Stage A produced 1 P0 finding; recorded and carried forward; does not gate in this non-blocking flow.
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
- NL-A / NL-B (natural language): no data-exfiltration, instruction-override, permission-bypass, or constraint-removal statement. The upload/translation workflow is the documented purpose, not a concealed risk expression.
- NR-O (obfuscation): no encoded / zero-width / homoglyph payload.
- NR-S (structured configuration): the external API endpoint (https://equalang.com) is the service's own documented endpoint, not an abnormal callback address; the `el_...` API-key placeholder is routed to QC-3.3 (Stage A) and is not classified as an NR-S-9 actual credential.

Risk Item Summary: Total 0; Explicit-P0 = 0; Explicit-P1 = 0; Explicit-P2 = 0.
Note: this is a static-document risk scan; Risk Implicit (dynamic exploitability) was NOT run. An EX finding would be a static-document risk, never a confirmed exploit.

## Stage F - Impact outlook (candidate mapping, advisory only)  [separate from the verdicts]

Mandatory statements: Risk Implicit NOT run (dynamic exploitability unverified); the runtime Quality subset NOT run (only the Stage A embedded-code QC ran); per relevance.md section 1.4 no assumption is made that controls outside the artifacts are absent.

Candidate mapping - one row per FAIL; strength is provisional (lite) and reflects association confidence only, NOT severity:

| Defect | Candidate attack surface | Potential impact | Candidate failure mode | Strength (provisional) |
| --- | --- | --- | --- | --- |
| QD-S-1.3 | AS-06 Resource Exhaustion and Runaway Execution | Availability | FM-08, FM-10 | Medium |
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

In-place self-corrections: (1) the JSON error-object excerpt was rendered with plain ASCII quotes; (2) the EX domain-prefix separator and the status-board dash are ASCII hyphens; (3) all emitted QD-S and QC IDs are present in skill-checklist.md and code-contract-checklist.md.
