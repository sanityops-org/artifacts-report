# SanityOps Inspect Lite - Skill Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Result status: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-15
Artifact version: not supplied by the user (using the case's Collection Date 2026-10-14 as the working label)
Inspected artifact: TC-173-jezweb-claude-skills-award-application-skill.md - Artifact Type: Skill (SKILL.md); case Collection Date 2026-10-14

## Executive summary

- Executed stages: A, C, E, F, G. Stage B and Stage D Not Executed (structural reasons; see status board).
- Stage A defect counts: P0 = 4, P1 = 5, P2 = 0 (QD-S: P0 4 / P1 5 / P2 0; embedded-code QC: 0 findings, no code snippets).
- Gate-0 result: Not passed - G0-4 (no Tool Schema in the artifact set; per-Tool completeness cannot be verified).
- Risk Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0 (no qualifying explicitly declared risk expression found).
- Top findings (rule ID - one-line defect):
  1. QD-S-1.1 - no upper bound on the number or size of inputs.
  2. QD-S-1.3 - the Skill performs an external URL fetch but declares no retry count, tool-invocation count or execution timeout.
  3. QD-S-3.4 - no non_goals / task-scope boundary declared.
  4. QD-S-4.1 - no failure behavior declared.
  5. QD-S-1.4 / QD-S-5.1 - no read/write/delete permission-type distinction for the criteria-page fetch.
- What was NOT run: the Risk Implicit subset and the runtime Quality subset (the Stage A embedded-code QC is the only Quality check performed).
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and evidence chains, use sanityops-cli (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

## Stage A - Skill inspection (QD-S)

### A.0 QD-S-0 baseline (entry gate, 6 items)

| ID | Verdict | Evidence |
| --- | --- | --- |
| QD-S-0.1 Required Field Presence | PASS | TC-173-jezweb-claude-skills-award-application-skill.md, front matter (lines 13-16): `name: award-application` and `description: ...` present |
| QD-S-0.2 Field Content Non-Empty | PASS | both fields carry content |
| QD-S-0.3 Syntax Parsability | PASS | YAML front matter parses (lines 13-16); the quoted multi-line `description` is well formed |
| QD-S-0.4 Field Type Validity | PASS | `name` and `description` are strings |
| QD-S-0.5 No Conflicting Declarations | PASS | no mutually contradictory declarations found |
| QD-S-0.6 Minimum Structural Completeness | PASS | front matter plus a titled body (Process / Writing Approach / What Awards Look For / Anti-Patterns / Example / Context Rules) |

Baseline result: PASS (6/6). The Skill proceeds to QD-S-1 through QD-S-5 inspection.

### A.1 Skill risk-level determination

Determination: L2 (Medium Risk).
Basis: the Skill is not text-processing only - Process step 1 instructs "If the user has a URL for the award, fetch the criteria page", i.e. an external system access (web fetch), and it reads a user-provided brief. That resource access places it at L2; no deletion, irreversible action, or permission change is declared, so it is not L3.
Applied rule set: the L2 minimum rule set = 6 mandatory P0 items (QD-S-1.1, QD-S-1.3, QD-S-2.1, QD-S-2.2, QD-S-3.4, QD-S-4.1) + 14 recommended P1 items.

### A.2 Findings by Review Schema dimension (six dimensions)

IDENTITY (what it does / does not do / what it can access)
- QD-S-3.4 FAIL (P0): no non_goals declaration. Evidence: the description and body define what the Skill writes ("Produces award submissions and grant applications that address every criterion with quantified evidence") but never state what tasks the Skill does NOT perform; there is no deferral, exclusion or refusal statement.
- QD-S-1.4 FAIL (P1): no read/write/delete permission-type distinction and no prohibited-operation declaration for the criteria-page fetch.
- QD-S-1.5 PASS (P1): a data-source boundary is declared. Evidence: Process step 1 "Ask the user for: Award/grant name and organiser ..." and "If the user has a URL for the award, fetch the criteria page."
- QD-S-2.4 PASS (P1): verbs are specific ("Write compelling award submissions, grant applications, and competition entries"); no broad manage/handle/process verb is used as the capability statement.
- QD-S-5.1 FAIL (P1): read/modify/delete scopes are not distinguished (also listed under EXECUTION).

TRIGGER (when it should trigger / not trigger)
- QD-S-3.1 PASS (P1): activation conditions are concrete. Evidence: description "Use whenever the user is applying for a business award (Telstra, chamber of commerce, industry awards), a grant, a competition, or any submission demonstrating merit against defined criteria."
- QD-S-3.2 FAIL (P1): no deactivation conditions declared. Evidence: the description gives positive scenarios only; no statement of when the Skill should NOT trigger.
- QD-S-3.6 PASS (P1): `name: award-application` and the `description` are consistent with the body.

INPUT (size, format, overflow behavior)
- QD-S-1.1 FAIL (P0): no upper limit on the number or size of inputs. Evidence: the Skill accepts a brief of arbitrary size (criteria list, word limits, achievements) with no declared cap.
- QD-S-3.3 PASS (P1, optional): insufficient-input handling is declared. Evidence: Process step 2 "If the user cannot provide evidence for a criterion, flag it explicitly."

EXECUTION (boundaries, retries, tool calls, chained calls)
- QD-S-1.3 FAIL (P0): execution resource boundary missing. Evidence: the Skill performs an external fetch ("fetch the criteria page") but declares no retry count, tool-invocation count, or execution timeout.
- QD-S-2.1 PASS (P0): no unbounded quantity directive is used as an execution instruction; "every criterion" is bounded by the finite selection-criteria list supplied by the user.
- QD-S-2.2 PASS (P0): no unterminated-execution wording present.
- QD-S-5.4 PASS (P1): no chained invocation of another Skill declared.
- QD-S-5.3 FAIL (P1): no permitted/prohibited environment boundary declared.

OUTPUT (size, structure, partial completion)
- QD-S-1.2 PASS (P1): output size is bounded by the award's word limits. Evidence: "Respect word limits absolutely ... If the limit is 500 words, submit 480-500."
- QD-S-2.3 PASS (P1): no open-ended enumeration present.

FAILURE (failures, empty input, insufficient input)
- QD-S-4.1 FAIL (P0): no failure behavior declared. Evidence: the artifact closes on the "Context Rules" section and contains no execution-failure handling declaration (no rule for a failed fetch or an unsatisfiable submission).
- QD-S-4.2 PASS (P1): partial coverage is declared acceptable. Evidence: "If you genuinely have nothing for a criterion, acknowledge it honestly and pivot to what you do have."
- QD-S-4.3 FAIL (P1): no post-failure prohibited-behavior declaration.

### A.3 Full L2 rule verdicts (one line per rule)

QD-S-1.1 | FAIL | evidence: TC-173-jezweb-claude-skills-award-application-skill.md, Process step 1 - inputs accepted with no cap on number or size
QD-S-1.2 | PASS | evidence: same file, "Respect word limits absolutely" - "If the limit is 500 words, submit 480-500"
QD-S-1.3 | FAIL | evidence: same file, Process step 1 - "fetch the criteria page" with no retry/timeout/call-count bound
QD-S-1.4 | FAIL | evidence: same file - no read/write/delete distinction or prohibited-operation declaration
QD-S-1.5 | PASS | evidence: same file, Process step 1 - "Ask the user for: Award/grant name and organiser ..."
QD-S-2.1 | PASS | evidence: same file - "every criterion" bounded by the finite criteria list
QD-S-2.2 | PASS | evidence: same file - no unterminated-execution wording present
QD-S-2.3 | PASS | evidence: same file - no open-ended enumeration ("etc." / "and others")
QD-S-2.4 | PASS | evidence: same file, description - specific verb "Write compelling award submissions"
QD-S-3.1 | PASS | evidence: same file, description - concrete triggers (business award, grant, competition, merit submission)
QD-S-3.2 | FAIL | evidence: same file, description - no statement of when the skill should NOT trigger
QD-S-3.3 | PASS | evidence: same file, Process step 2 - "If the user cannot provide evidence for a criterion, flag it explicitly"
QD-S-3.4 | FAIL | evidence: same file - no non_goals declaration (no task-scope exclusion or deferral)
QD-S-3.6 | PASS | evidence: same file, front matter - name `award-application` consistent with the description
QD-S-4.1 | FAIL | evidence: same file, Context Rules - no failure-behavior declaration present
QD-S-4.2 | PASS | evidence: same file, Anti-Patterns - "acknowledge it honestly and pivot to what you do have"
QD-S-4.3 | FAIL | evidence: same file - no post-failure prohibited-behavior declaration
QD-S-5.1 | FAIL | evidence: same file - read/write/delete scopes not distinguished for the criteria-page fetch
QD-S-5.3 | FAIL | evidence: same file - no environment boundary declared
QD-S-5.4 | PASS | evidence: same file - no other-Skill chaining declared

### A.4 Defect list (sorted P0 first)

P0 (4): QD-S-1.1, QD-S-1.3, QD-S-3.4, QD-S-4.1
P1 (5): QD-S-1.4, QD-S-3.2, QD-S-4.3, QD-S-5.1, QD-S-5.3
P2 (0): none

### A.5 Embedded-code QC (code-contract; QC-0 gate first)

The artifact embeds no code snippets (its body is prose, tables and blockquoted examples; there are no fenced code blocks). QC-0.1-QC-0.5 and QC-1.x-QC-4.x therefore did not execute - there are no embedded snippets to inspect. QC findings: 0.

## Stage B - Cross-artifact

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available. Cross-artifact relationships (QD-PS/QD-PT/QD-ST/QD-CYC) require at least two of the three artifact types from one agent; only a single Skill is present.

## Stage C - Gate-0

- G0-1 (no unfixed P0 in Stage A): informational - Stage A produced 4 P0 findings; recorded and carried forward; does not gate in this non-blocking flow.
- G0-2 (no unfixed P0 in Stage B): informational - Stage B Not Executed.
- G0-3 (responsibility boundary statements exist and are locatable): recorded as informational/indeterminate - a lone Skill carries no Prompt-level responsibility baseline to cite, and the Skill's own body declares no non_goals/task-scope boundary to locate (consistent with the QD-S-3.4 finding).
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
- NL-A / NL-B (natural language): no data-exfiltration, instruction-override, permission-bypass, or constraint-removal statement. The anti-pattern guidance ("Vague claims without evidence", "Hyperbole and superlatives", "Remove hedging language") is defensive writing guidance.
- NR-O (obfuscation): no encoded / zero-width / homoglyph payload.
- NR-S (structured configuration): no dangerous flags and no hardcoded credentials or PII. The named award bodies and the example company figures are ordinary illustrative content, not secrets.

Risk Item Summary: Total 0; Explicit-P0 = 0; Explicit-P1 = 0; Explicit-P2 = 0.
Note: this is a static-document risk scan; Risk Implicit (dynamic exploitability) was NOT run. An EX finding would be a static-document risk, never a confirmed exploit.

## Stage F - Impact outlook (candidate mapping, advisory only)  [separate from the verdicts]

Mandatory statements: Risk Implicit NOT run (dynamic exploitability unverified); the runtime Quality subset NOT run (only the Stage A embedded-code QC ran, and it found no snippets); per relevance.md section 1.4 no assumption is made that controls outside the artifacts are absent.

Candidate mapping - one row per FAIL; strength is provisional (lite) and reflects association confidence only, NOT severity:

| Defect | Candidate attack surface | Potential impact | Candidate failure mode | Strength (provisional) |
| --- | --- | --- | --- | --- |
| QD-S-1.1 | AS-06 Resource Exhaustion and Runaway Execution | Availability | FM-08, FM-10 | Conditional |
| QD-S-1.3 | AS-06 Resource Exhaustion and Runaway Execution | Availability | FM-08, FM-10 | Conditional |
| QD-S-4.1 | AS-07 Anomaly Propagation and Cascading Failures | D1, D2, D3, Availability | FM-08, FM-09 | Conditional |
| QD-S-3.4 | AS-01 Instruction and Context Boundary Confusion; AS-05 Tool Misuse and High-Risk Side Effects | D2, D3 | FM-02, FM-07, FM-09 | Medium |
| QD-S-1.4, QD-S-5.1, QD-S-5.3 | AS-04 Permission, Identity and Delegation Expansion; AS-05 Tool Misuse and High-Risk Side Effects | D2, D3 | FM-05, FM-09 | Medium |
| QD-S-3.2, QD-S-4.3 | AS-01 Instruction and Context Boundary Confusion; AS-07 Anomaly Propagation and Cascading Failures | D1, D2, D3, Availability | FM-02, FM-07, FM-08, FM-09 | Conditional |

Candidate RAG-Agent quality metrics (candidate only): resource/unbounded declarations -> Completeness, Timeliness, Robustness; trigger/scope/ambiguity -> Relevance, Decomposition Capability, Boundary Recognition; permission/environment boundary -> Boundary Recognition, Safety Response, Traceability; failure expansion -> Completeness, Coherence, Safety Response.

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

In-place self-corrections: (1) artifact blockquote markers were rendered in plain ASCII within evidence; (2) the EX domain-prefix separator and the status-board dash are ASCII hyphens; (3) all emitted QD-S IDs are present in skill-checklist.md, and all AS-*/FM-* codes are present in relevance-map.md.
