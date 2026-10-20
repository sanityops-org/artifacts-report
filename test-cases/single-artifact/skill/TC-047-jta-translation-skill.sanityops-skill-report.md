# SanityOps Inspect Lite - Skill Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Result status: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-14
Artifact version: not supplied by the user (using the case's Collection Date as the working label)
Inspected artifact: TC-047-jta-translation-skill.md - Artifact Type: Skill (SKILL.md); case Collection Date 2026-10-13

## Executive summary

- Executed stages: A, C, E, F, G. Stage B and Stage D Not Executed (structural reasons; see status board).
- Stage A defect counts: P0 = 3, P1 = 8, P2 = 1 (QD-S: P0 3 / P1 8 / P2 0; embedded-code QC: P0 0 / P1 0 / P2 1).
- Gate-0 result: Not passed - G0-4 (no Tool Schema in the artifact set; per-Tool completeness cannot be verified).
- Risk Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0 (no qualifying explicitly declared risk expression found).
- Top findings (rule ID - one-line defect):
  1. QD-S-3.4 - no non_goals / task-scope boundary declared; the LLM can expand task boundaries on its own.
  2. QD-S-1.1 - no upper bound on the number or size of inputs (e.g. number of keys in the JSON file).
  3. QD-S-1.3 - tool invocations (the jta CLI) with no retry count or execution timeout declared.
  4. QD-S-1.4 - no read/write/delete permission-type distinction although the skill writes files and uses an unscoped `Bash` capability.
  5. QD-S-5.1 - read/modify/delete scopes not distinguished while the skill writes translated files.
- What was NOT run: the Risk Implicit subset and the runtime Quality subset (the Stage A embedded-code QC is the only Quality check performed).
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and evidence chains, use sanityops-cli (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

## Stage A - Skill inspection (QD-S)

### A.0 QD-S-0 baseline (entry gate, 6 items)

| ID | Verdict | Evidence |
| --- | --- | --- |
| QD-S-0.1 Required Field Presence | PASS | TC-047-jta-translation-skill.md, front matter (lines 14-17): `name`, `description`, `version`, `allowed-tools` present |
| QD-S-0.2 Field Content Non-Empty | PASS | all four front-matter fields are non-empty |
| QD-S-0.3 Syntax Parsability | PASS | YAML front matter parses (lines 13-18) |
| QD-S-0.4 Field Type Validity | PASS | `name`/`description`/`version` are strings; `allowed-tools` is a comma-separated string list |
| QD-S-0.5 No Conflicting Declarations | PASS | no mutually contradictory declarations found |
| QD-S-0.6 Minimum Structural Completeness | PASS | front matter + titled body (When to Use / Instructions / Error Handling etc.) |

Baseline result: PASS (6/6). The Skill proceeds to QD-S-1 through QD-S-5 inspection.
Observation (no QD-S rule assigned): Step 6 states "Always use `$PROVIDER_FLAG`", while two later examples (`--provider anthropic --model claude-sonnet-4-5`, lines 157 and 241) omit it; recorded as an internal-consistency observation only.

### A.1 Skill risk-level determination

Determination: L2 (Medium Risk).
Basis: the Skill performs state-changing resource access and external system access - it installs and runs an external CLI, downloads a binary and moves it with `sudo mv` (Step 2), and writes translated files and terminology files. No deletion or irreversible data operation, and no permission change, so it is not L3; it is above L1 because it is not text-processing only.
Applied rule set: the L2 minimum rule set = 6 mandatory P0 items + 14 recommended P1 items.

### A.2 Findings by Review Schema dimension (six dimensions)

IDENTITY (what it does / does not do / what it can access)
- QD-S-3.4 FAIL (P0): no non_goals declaration. Evidence: description "Translate JSON i18n files to multiple languages ..." with no statement of what the skill does NOT do.
- QD-S-1.4 FAIL (P1): no read/write/delete permission-type distinction and no prohibited-operation declaration. Evidence: `allowed-tools: Read, Write, Bash, Glob` (line 17) grants an unscoped shell capability.
- QD-S-1.5 FAIL (P1): no permitted or prohibited data-source declaration.
- QD-S-2.4 PASS: verbs are specific to translation; no broad manage/handle/process verb used as the capability statement.

TRIGGER (when it should trigger / not trigger)
- QD-S-3.1 PASS: trigger words are enumerated (JSON, i18n, locale, internationalization).
- QD-S-3.2 FAIL (P1): no deactivation conditions declared.
- QD-S-3.6 PASS: name `jta` and the description are consistent with the body.

INPUT (size, format, overflow behavior)
- QD-S-1.1 FAIL (P0): no upper limit on input size. Evidence: "Large files (>500 keys): Use `--batch-size 10 --concurrency 2`" acknowledges large files but sets no maximum.
- QD-S-3.3 PASS: ambiguous input is handled - "Ask user to confirm which file to translate if multiple found."

EXECUTION (boundaries, retries, tool calls, chained calls)
- QD-S-1.3 FAIL (P0): no retry count or execution timeout declared. Evidence: "Error: 'Rate limit exceeded' ... `jta en.json --to zh --batch-size 10 --concurrency 1`" adjusts batching but declares no timeout or retry cap.
- QD-S-2.1 PASS: no unbounded quantity wording ("all/every/entire/complete") used as a processing directive.
- QD-S-2.2 PASS: no unterminated wording ("until success" etc.) present.
- QD-S-5.1 FAIL (P1): read/modify/delete scopes not distinguished (also listed under IDENTITY).
- QD-S-5.3 FAIL (P1): no permitted/prohibited environment boundary declared.
- QD-S-5.4 PASS: no chained invocation of other Skills declared.

OUTPUT (size, structure, partial completion)
- QD-S-1.2 FAIL (P1): no output-size limit declared.
- QD-S-2.3 PASS: no open-ended enumeration ("etc.") in output/functional structure.

FAILURE (failures, empty input, insufficient input)
- QD-S-4.1 PASS: failure behavior is declared - the "Error Handling" section names scenarios (command not found, API key not set, rate limit, invalid JSON) with remediation.
- QD-S-4.2 FAIL (P1): partial-completion legitimacy not declared.
- QD-S-4.3 FAIL (P1): post-failure prohibited behaviors not declared.

### A.3 Full L2 rule verdicts (one line per rule)

QD-S-1.1 | FAIL | evidence: TC-047-jta-translation-skill.md, Performance Tips (line 303) - "Large files (>500 keys)" acknowledged but no input maximum
QD-S-1.2 | FAIL | evidence: same file, Output Format (lines 325-337) - no output-size limit declared
QD-S-1.3 | FAIL | evidence: same file, Error Handling (lines 275-279) - batch/concurrency advice but no timeout or retry cap
QD-S-1.4 | FAIL | evidence: same file, front matter (line 17) - `allowed-tools: Read, Write, Bash, Glob` with no read/write/delete distinction
QD-S-1.5 | FAIL | evidence: same file - no permitted/prohibited data sources declared
QD-S-2.1 | PASS | evidence: same file - no unbounded quantity directive present
QD-S-2.2 | PASS | evidence: same file - no unterminated execution wording present
QD-S-2.3 | PASS | evidence: same file - no open-ended enumeration present
QD-S-2.4 | PASS | evidence: same file, description (line 15) - specific verb "Translate ... to multiple languages"
QD-S-3.1 | PASS | evidence: same file, When to Use (lines 24-30) - enumerated trigger conditions
QD-S-3.2 | FAIL | evidence: same file - no statement of when the skill should NOT trigger
QD-S-3.3 | PASS | evidence: same file, Step 4 (line 123) - "Ask user to confirm which file to translate if multiple found."
QD-S-3.4 | FAIL | evidence: same file - no non_goals declaration
QD-S-3.6 | PASS | evidence: same file, front matter (lines 14-15) - name `jta` consistent with the description
QD-S-4.1 | PASS | evidence: same file, Error Handling (lines 251-298) - declared failure scenarios and remediation
QD-S-4.2 | FAIL | evidence: same file - partial-completion legitimacy not declared
QD-S-4.3 | FAIL | evidence: same file - prohibitions after failure not declared
QD-S-5.1 | FAIL | evidence: same file - writes translated files, read/write/delete scopes not distinguished
QD-S-5.3 | FAIL | evidence: same file - no environment boundary declared
QD-S-5.4 | PASS | evidence: same file - no other-Skill chaining declared

### A.4 Defect list (sorted P0 first)

P0 (3): QD-S-1.1, QD-S-1.3, QD-S-3.4
P1 (8): QD-S-1.2, QD-S-1.4, QD-S-1.5, QD-S-3.2, QD-S-4.2, QD-S-4.3, QD-S-5.1, QD-S-5.3
P2 (1): QC-3.3

### A.5 Embedded-code QC (code-contract; QC-0 gate first)

QC-0.1 Syntax Parsability | PASS | evidence: the Bash and JSON snippets are syntactically valid.
QC-0.2 Language Declaration | PASS | evidence: every fenced block carries a language tag (`bash`, `json`).
QC-0.3 Structural Completeness | PASS | evidence: snippets are complete for their illustrative intent.
QC-0 gate: PASS. Proceed to QC-1 through QC-3.

QC-1.1 Undefined Name Reference | PASS | evidence: `jta`, `jq`, `curl`, `uname` are external binaries, not undefined names.
QC-1.2 Invalid Import | PASS | evidence: no imports used.
QC-1.3 Deprecated API Usage | PASS | evidence: no deprecated APIs used.
QC-1.4 Type Mismatch | PASS | evidence: no incompatible argument types found.
QC-2.1 Unclosed File Handle | PASS | evidence: no file handles opened in the snippets.
QC-2.2 Unreleased Network Connection | PASS | evidence: the `curl` download writes to a file; no persistent connection object.
QC-2.3 Missing Exception Handling | PASS | evidence: installation steps use `if command -v ...` guards.
QC-3.1 Unused Import | PASS | evidence: no imports used.
QC-3.2 Missing Import | PASS | evidence: no imported module referenced.
QC-3.3 Hardcoded Demo Value | FAIL (P2) | evidence: Step 3 (line 101) - `echo " export OPENAI_API_KEY=sk-..."` uses a demo credential placeholder.

## Stage B - Cross-artifact

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.

## Stage C - Gate-0

- G0-1 (no unfixed P0 in Stage A): informational - Stage A produced 3 P0 findings; recorded and carried forward; does not gate in this non-blocking flow.
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
- NL-A / NL-B (natural language): no data-exfiltration, instruction-override, permission-bypass, or constraint-removal statement. The `curl -L ... -o jta; chmod +x; sudo mv` install steps are a documented install procedure, not a declared risk expression, and the download endpoints are the project's own release URLs.
- NR-O (obfuscation): no encoded / zero-width / homoglyph payload.
- NR-S (structured configuration): no dangerous flags or abnormal callback addresses; the `sk-...` API-key placeholders are weak/demo patterns routed to QC-3.3 (Stage A) and are not classified as NR-S-9 actual credentials (per the QC-3.3 / NR-S-9 boundary note).

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
| QD-S-3.2 | AS-01; AS-04 | D1, D2, D3 | FM-02, FM-07, FM-09 | Medium |
| QD-S-4.2, QD-S-4.3 | AS-07 Anomaly Propagation and Cascading Failures | D1, D2, D3, Availability | FM-08, FM-09 | Medium |
| QD-S-5.1 | AS-04; AS-05 | D2, D3 | FM-05, FM-09 | Medium |
| QD-S-5.3 | AS-04; AS-05 | D2, D3 | FM-05, FM-09 | Conditional |
| QC-3.3 | no candidate AS/FM mapping defined for QC IDs in relevance-map.md | - | - | - |

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
