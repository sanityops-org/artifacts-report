# SanityOps Inspect Lite - Skill Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Result status: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-15
Artifact version: not supplied by the user (using the case's Collection Date 2026-10-14 as the working label)
Inspected artifact: TC-179-travel-hacking-toolkit-trip-planner-skill.md - Artifact Type: Skill (SKILL.md); case Collection Date 2026-10-14

## Executive summary

- Executed stages: A, C, E, F, G. Stage B and Stage D Not Executed (structural reasons; see status board).
- Stage A defect counts: P0 = 3, P1 = 2, P2 = 0 (QD-S: P0 3 / P1 2 / P2 0; embedded-code QC: 0 findings, no code snippets).
- Gate-0 result: Not passed - G0-4 (no Tool Schema in the artifact set; per-Tool completeness cannot be verified).
- Risk Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0 (no qualifying explicitly declared risk expression found).
- Top findings (rule ID - one-line defect):
  1. QD-S-1.1 - no upper limit on the number or size of inputs (travelers, dates, preferences, searches).
  2. QD-S-1.3 - the Skill orchestrates many tool/search invocations and retries but declares no retry count, tool-invocation count or timeout.
  3. QD-S-2.1 - unbounded exhaustive-processing wording ("Launch ALL searches simultaneously") with no declared cap, over an open-ended sub-search set.
  4. QD-S-1.2 - no upper limit declared on output size for the cost matrices and recommendations.
  5. QD-S-2.3 - open-ended enumeration in the source list ("Duffel, Ignav, seats.aero, ... Airbnb, etc").
- What was NOT run: the Risk Implicit subset and the runtime Quality subset (the Stage A embedded-code QC is the only Quality check performed, and it found no code snippets).
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and evidence chains, use sanityops-cli (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

## Stage A - Skill inspection (QD-S)

### A.0 QD-S-0 baseline (entry gate, 6 items)

| ID | Verdict | Evidence |
| --- | --- | --- |
| QD-S-0.1 Required Field Presence | PASS | TC-179-travel-hacking-toolkit-trip-planner-skill.md, front matter (lines 13-19): `name: trip-planner`, a `description`, `category`, `summary` and `api_key` are present |
| QD-S-0.2 Field Content Non-Empty | PASS | all fields carry content |
| QD-S-0.3 Syntax Parsability | PASS | the YAML front matter parses (lines 13-19) |
| QD-S-0.4 Field Type Validity | PASS | all front-matter values are strings |
| QD-S-0.5 No Conflicting Declarations | PASS | no mutually contradictory declarations found |
| QD-S-0.6 Minimum Structural Completeness | PASS | front matter plus a titled body (companion skills / When to Use / When NOT to Use / 6-step Workflow / Error Handling / Limitations) |

Baseline result: PASS (6/6). The Skill proceeds to QD-S-1 through QD-S-5 inspection.

### A.1 Skill risk-level determination

Determination: L2 (Medium Risk).
Basis: the Skill is not text-processing only - it orchestrates external searches (`compare-flights`, `compare-hotels`, `transfer-partners`, `trip-calculator`) against many external services (Duffel, Ignav, seats.aero, Chase, Amex, SerpAPI, Trivago, LiteAPI, Airbnb, etc.). This is resource access that may involve sensitive data (traveler details, loyalty balances). No deletion, irreversible action or payment is declared, so it is not L3.
Applied rule set: the L2 minimum rule set = 6 mandatory items (QD-S-1.1, QD-S-1.3, QD-S-2.1, QD-S-2.2, QD-S-3.4, QD-S-4.1) + 14 recommended items (QD-S-1.2, QD-S-1.4, QD-S-1.5, QD-S-2.3, QD-S-2.4, QD-S-3.1, QD-S-3.2, QD-S-3.3, QD-S-3.6, QD-S-4.2, QD-S-4.3, QD-S-5.1, QD-S-5.3, QD-S-5.4).

### A.2 Findings by Review Schema dimension (six dimensions)

IDENTITY (what it does / does not do / what it can access)
- QD-S-3.4 PASS (P0): a task-scope boundary is declared. Evidence: the "When NOT to Use" section routes flight-only, hotel-only, award-calendar and points-only requests to sibling skills.
- QD-S-1.4 PASS (P1): the Skill's operations are read-only searches/quotes; no write/delete capability is declared, so no prohibited-operation gap arises.
- QD-S-1.5 PASS (P1): the data sources are declared. Evidence: the workflow names the sources and the companion reference skills.
- QD-S-2.4 PASS (P1): the verb is specific ("Orchestrates `compare-flights`, `compare-hotels`, `transfer-partners`, and `trip-calculator`"); no broad manage/handle/process verb is used as the capability statement.
- QD-S-5.1 PASS (P1): the Skill declares only read/search operations; read/modify/delete scopes are not conflated.

TRIGGER (when it should trigger / not trigger)
- QD-S-3.1 PASS (P1): activation conditions are concrete. Evidence: "'Plan a trip to Paris Aug 11-15'", "'How much would a trip to Stockholm cost in points vs cash?'".
- QD-S-3.2 PASS (P1): deactivation conditions are declared. Evidence: the "When NOT to Use" section ("Flight-only comparison (use `compare-flights`)", "Hotel-only comparison (use `compare-hotels`)").
- QD-S-3.6 PASS (P1): `name: trip-planner` and the `description` are consistent with the body.

INPUT (size, format, overflow behavior)
- QD-S-1.1 FAIL (P0): no upper limit on input number or size. Evidence: Step 1 "Parse Trip Parameters" declares no cap on the number of travelers, dates, preferences or searches.
- QD-S-3.3 PASS (P1): ambiguous input is handled explicitly. Evidence: "If anything is ambiguous, ask. Don't guess dates or travelers."

EXECUTION (boundaries, retries, tool calls, chained calls)
- QD-S-1.3 FAIL (P0): involves tool invocations and retries with no declared execution-resource bound. Evidence: Step 2 "Launch ALL searches simultaneously." and "Each of these internally runs their own parallel sub-searches (... etc)." plus the Error Handling line "Retry seats.aero for award options." - no retry count, tool-invocation count or timeout is declared.
- QD-S-2.1 FAIL (P0): uses unbounded exhaustive wording with no cap. Evidence: Step 2 "Launch ALL searches simultaneously." - an execution directive over an open-ended sub-search set ("... etc").
- QD-S-2.2 PASS (P0): no unterminated-execution wording ("keep trying / until success / persist until") present.
- QD-S-5.4 PASS (P1): the downstream skills it invokes are enumerated. Evidence: "Orchestrates `compare-flights`, `compare-hotels`, `transfer-partners`, and `trip-calculator`" plus the companion reference-skill list.

OUTPUT (size, structure, partial completion)
- QD-S-1.2 FAIL (P1): no upper limit declared on output size. Evidence: the Step 3 cost matrix, Step 5 trip-by-strategy table and Step 6 source-status report define no bound on rows, columns or total length.

FAILURE (failures, empty input, insufficient input)
- QD-S-4.1 PASS (P0): failure behavior is declared. Evidence: "**NEVER fail silently.** If any sub-search fails, note it and continue with what you have."
- QD-S-4.2 PASS (P1): partial completion is declared. Evidence: "If flights fail but hotels succeed (or vice versa), present what you have and note the gap".
- QD-S-4.3 PASS (P1): post-failure behavior is constrained. Evidence: "**NEVER fail silently.**" plus "If ALL sources fail for one component, say so".
- QD-S-5.3 PASS (P1): the operational context is live external search/quoting; no production-diagnostic or destructive environment operation is declared.

### A.3 Full L2 rule verdicts (one line per rule)

QD-S-1.1 | FAIL | evidence: TC-179-travel-hacking-toolkit-trip-planner-skill.md, Step 1 - no input count/size cap
QD-S-1.2 | FAIL | evidence: same file, Steps 3/5/6 - no output-size bound on the matrices and reports
QD-S-1.3 | FAIL | evidence: same file, Step 2 / Error Handling - "Launch ALL searches" and "Retry seats.aero" with no retry/timeout/call-count bound
QD-S-1.4 | PASS | evidence: same file - read-only search orchestration; no write/delete declared
QD-S-1.5 | PASS | evidence: same file, Workflow - named search sources and companion skills
QD-S-2.1 | FAIL | evidence: same file, Step 2 - "Launch ALL searches simultaneously."
QD-S-2.2 | PASS | evidence: same file - no unterminated-execution wording present
QD-S-2.3 | FAIL | evidence: same file, Step 2 - "(Duffel, Ignav, seats.aero, Chase, Amex, SerpAPI, Trivago, LiteAPI, Airbnb, etc)."
QD-S-2.4 | PASS | evidence: same file, body - specific verb "Orchestrates"
QD-S-3.1 | PASS | evidence: same file, When to Use - concrete trip-planning triggers
QD-S-3.2 | PASS | evidence: same file, When NOT to Use - explicit deactivation/routing
QD-S-3.3 | PASS | evidence: same file, Step 1 - "If anything is ambiguous, ask."
QD-S-3.4 | PASS | evidence: same file, When NOT to Use - scope boundary declared
QD-S-3.6 | PASS | evidence: same file, front matter - name `trip-planner` consistent with the description
QD-S-4.1 | PASS | evidence: same file, Error Handling - "NEVER fail silently."
QD-S-4.2 | PASS | evidence: same file, Error Handling - partial results presented and gap noted
QD-S-4.3 | PASS | evidence: same file, Error Handling - "NEVER fail silently."
QD-S-5.1 | PASS | evidence: same file - read/search only; scopes not conflated
QD-S-5.3 | PASS | evidence: same file - no production destructive environment operation declared
QD-S-5.4 | PASS | evidence: same file - downstream skills enumerated

### A.4 Defect list (sorted P0 first)

P0 (3): QD-S-1.1, QD-S-1.3, QD-S-2.1
P1 (2): QD-S-1.2, QD-S-2.3
P2 (0): none

### A.5 Embedded-code QC (code-contract; QC-0 gate first)

The artifact's fenced blocks contain plain-text workflow/log templates (a PARALLEL step list, source-status lines and error messages), not programming-language code snippets. There is therefore no embedded code snippet in scope for the QC checklist; QC-0.1-QC-0.5 and QC-1.x-QC-4.x did not execute. QC findings: 0.

## Stage B - Cross-artifact

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent is available. Cross-artifact relationships (QD-PS/QD-PT/QD-ST/QD-CYC) require at least two of the three artifact types from one agent; only a single Skill is present.

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
- NL-A / NL-B (natural language): no data-exfiltration, instruction-override, permission-bypass or constraint-removal statement. The "hold before transfer" and "NEVER fail silently" rules are defensive constraints.
- NR-O (obfuscation): no encoded, zero-width or homoglyph payload.
- NR-S (structured configuration): no dangerous flags and no hardcoded credentials or PII. The front-matter line `api_key: Uses individual skill keys` is a description, not a credential value (no key string is embedded), so NR-S-9 does not apply.

Risk Item Summary: Total 0; Explicit-P0 = 0; Explicit-P1 = 0; Explicit-P2 = 0.
Note: this is a static-document risk scan; Risk Implicit (dynamic exploitability) was NOT run. An EX finding would be a static-document risk, never a confirmed exploit.

## Stage F - Impact outlook (candidate mapping, advisory only)  [separate from the verdicts]

Mandatory statements: Risk Implicit NOT run (dynamic exploitability unverified); the runtime Quality subset NOT run (only the Stage A embedded-code QC ran, and it found no code snippets); per relevance.md section 1.4 no assumption is made that controls outside the artifacts are absent.

Candidate mapping - one row per FAIL; strength is provisional (lite) and reflects association confidence only, NOT severity:

| Defect | Candidate attack surface | Potential impact | Candidate failure mode | Strength (provisional) |
| --- | --- | --- | --- | --- |
| QD-S-1.1 | AS-06 Resource Exhaustion and Runaway Execution | Availability | FM-08, FM-10 | Conditional |
| QD-S-1.2 | AS-06 Resource Exhaustion and Runaway Execution | Availability | FM-08, FM-10 | Conditional |
| QD-S-1.3 | AS-06 Resource Exhaustion and Runaway Execution | Availability | FM-08, FM-10 | Conditional |
| QD-S-2.1 | AS-06 Resource Exhaustion and Runaway Execution; AS-07 Anomaly Propagation and Cascading Failures | Availability, Integrity | FM-08, FM-10 | Conditional |
| QD-S-2.3 | AS-06 Resource Exhaustion and Runaway Execution; AS-07 Anomaly Propagation and Cascading Failures | Availability, Integrity | FM-08, FM-10 | Conditional |

Candidate RAG-Agent quality metrics (candidate only): resource/unbounded declarations -> Completeness, Timeliness, Robustness.

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

In-place self-corrections: (1) artifact emoji and em dashes were omitted or rendered in plain ASCII within evidence; (2) the EX domain-prefix separator and the status-board dash are non-CJK; (3) all emitted QD-S IDs are present in skill-checklist.md, and all AS-*/FM-* codes are present in relevance-map.md.
