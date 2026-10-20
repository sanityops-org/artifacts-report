# SanityOps Inspect Lite - Skill Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Result status: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-14
Artifact version: not supplied by the user (using the case's Collection Date as the working label)
Inspected artifact: TC-053-crib-home-skill.md - Artifact Type: Skill (SKILL.md); case Collection Date 2026-10-13

## Executive summary

- Executed stages: A, C, E, F, G. Stage B and Stage D Not Executed (structural reasons; see status board).
- Stage A defect counts: P0 = 4, P1 = 11, P2 = 0 (QD-S: P0 4 / P1 11 / P2 0; embedded-code QC: 0 findings).
- Gate-0 result: Not passed - G0-4 (no Tool Schema in the artifact set; per-Tool completeness cannot be verified).
- Risk Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0 (no qualifying explicitly declared risk expression found).
- Top findings (rule ID - one-line defect):
  1. QD-S-3.4 - no non_goals / task-scope boundary declared.
  2. QD-S-2.1 - unbounded quantity directives ("--all", "all reachable lights and plugs", "group all speakers").
  3. QD-S-1.1 - no upper bound on the number of inputs (device/room/name arguments).
  4. QD-S-1.3 - CLI invocations with no retry count or execution timeout declared.
  5. QD-S-2.4 - broad capability verb "Control ... any smart home device" with no non_goals.
- What was NOT run: the Risk Implicit subset and the runtime Quality subset (the Stage A embedded-code QC is the only Quality check performed).
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and evidence chains, use sanityops-cli (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

## Stage A - Skill inspection (QD-S)

### A.0 QD-S-0 baseline (entry gate, 6 items)

| ID | Verdict | Evidence |
| --- | --- | --- |
| QD-S-0.1 Required Field Presence | PASS | TC-053-crib-home-skill.md, front matter (lines 16-18): `name: home`, `description`, `allowed-tools` present |
| QD-S-0.2 Field Content Non-Empty | PASS | all fields non-empty |
| QD-S-0.3 Syntax Parsability | PASS | YAML front matter parses (lines 15-19) |
| QD-S-0.4 Field Type Validity | PASS | values are strings |
| QD-S-0.5 No Conflicting Declarations | PASS | no mutually contradictory declarations found |
| QD-S-0.6 Minimum Structural Completeness | PASS | front matter + titled body (Quick Start / Devices / Speakers / Guidelines / Setup) |

Baseline result: PASS (6/6). The Skill proceeds to QD-S-1 through QD-S-5 inspection.

### A.1 Skill risk-level determination

Determination: L2 (Medium Risk).
Basis: the Skill performs state-changing operations on external resources - it controls smart home devices and a Spotify account (turn on/off, brightness, playback, playlist create/remove). These are recoverable, state-changing actions; there is no deletion of data, no payment, and no permission change, so it is not L3; it is above L1 because it is not text-processing only.
Applied rule set: the L2 minimum rule set = 6 mandatory P0 items + 14 recommended P1 items.

### A.2 Findings by Review Schema dimension (six dimensions)

IDENTITY (what it does / does not do / what it can access)
- QD-S-3.4 FAIL (P0): no non_goals declaration. Evidence: description "Control smart home devices (lights, switches, speakers, Spotify)" with no statement of what the skill does NOT do.
- QD-S-1.4 FAIL (P1): no read/write/delete permission-type distinction and no prohibited-operation declaration. Evidence: `allowed-tools: Bash(crib *)` (line 18) scopes to the binary but the body includes destructive-style commands (`crib spotify playlist remove ...`).
- QD-S-1.5 FAIL (P1): no permitted or prohibited data-source declaration.
- QD-S-2.4 FAIL (P1): broad capability verb "Control" used without non_goals. Evidence: "Control smart home devices ... or interact with any smart home device."

TRIGGER (when it should trigger / not trigger)
- QD-S-3.1 FAIL (P1): overly broad activation condition. Evidence: "...or interact with any smart home device."
- QD-S-3.2 FAIL (P1): no deactivation conditions declared.
- QD-S-3.6 PASS: name `home` and the description are consistent with the body.

INPUT (size, format, overflow behavior)
- QD-S-1.1 FAIL (P0): no upper limit on the number of inputs. Evidence: `crib devices on <name> [name...]` accepts an unbounded name list with no cap.
- QD-S-3.3 PASS: ambiguous input is handled - "Fuzzy name matching works everywhere" plus explicit disambiguation guidance ("speakers vs spotify").

EXECUTION (boundaries, retries, tool calls, chained calls)
- QD-S-1.3 FAIL (P0): no retry count or execution timeout declared for the CLI invocations.
- QD-S-2.1 FAIL (P0): unbounded quantity directives. Evidence: `crib devices on --all  # Turn on all reachable lights and plugs` (line 33); `crib sonos group-all  # Group all speakers together` (line 58).
- QD-S-2.2 PASS: no unterminated wording ("until success" etc.) present.
- QD-S-5.1 FAIL (P1): read/modify/delete scopes not distinguished (also listed under IDENTITY).
- QD-S-5.3 FAIL (P1): no permitted/prohibited environment boundary declared.
- QD-S-5.4 PASS: no chained invocation of other Skills declared.

OUTPUT (size, structure, partial completion)
- QD-S-1.2 FAIL (P1): no output-size limit declared (e.g. `crib devices list`, `crib spotify playlist show`).
- QD-S-2.3 FAIL (P1): open-ended enumeration. Evidence: "fulfill user requests about lights, music, speakers, and other devices." (line 21).

FAILURE (failures, empty input, insufficient input)
- QD-S-4.1 PASS: failure behavior is declared - "Errors include hints - read them to know what to do next (e.g. 'run crib setup', 'device is unreachable')." and "Unreachable devices: ... they're powered off at the switch, nothing you can do remotely."
- QD-S-4.2 FAIL (P1): partial-completion legitimacy not declared.
- QD-S-4.3 FAIL (P1): post-failure prohibited behaviors not declared (beyond the unreachable-device note).

### A.3 Full L2 rule verdicts (one line per rule)

QD-S-1.1 | FAIL | evidence: TC-053-crib-home-skill.md, Devices (line 30) - `crib devices on <name> [name...]` with no input-count cap
QD-S-1.2 | FAIL | evidence: same file, Devices/Spotify listings (lines 29, 77) - no output-size limit declared
QD-S-1.3 | FAIL | evidence: same file - CLI invocations with no retry count or execution timeout
QD-S-1.4 | FAIL | evidence: same file, front matter (line 18) + Spotify (line 81) - `allowed-tools: Bash(crib *)` with a `playlist remove` command and no read/write/delete distinction
QD-S-1.5 | FAIL | evidence: same file - no permitted/prohibited data sources declared
QD-S-2.1 | FAIL | evidence: same file, Devices (line 33) - `crib devices on --all  # Turn on all reachable lights and plugs`
QD-S-2.2 | PASS | evidence: same file - no unterminated execution wording present
QD-S-2.3 | FAIL | evidence: same file, body (line 21) - "lights, music, speakers, and other devices"
QD-S-2.4 | FAIL | evidence: same file, description (line 17) - "Control smart home devices ... interact with any smart home device"
QD-S-3.1 | FAIL | evidence: same file, description (line 17) - "...or interact with any smart home device"
QD-S-3.2 | FAIL | evidence: same file - no statement of when the skill should NOT trigger
QD-S-3.3 | PASS | evidence: same file, Guidelines (lines 84-92) - fuzzy matching + speakers/spotify disambiguation
QD-S-3.4 | FAIL | evidence: same file - no non_goals declaration
QD-S-3.6 | PASS | evidence: same file, front matter (lines 16-17) - name `home` consistent with the description
QD-S-4.1 | PASS | evidence: same file, Guidelines (lines 88-92) - "Errors include hints" + "Unreachable devices" handling
QD-S-4.2 | FAIL | evidence: same file - partial-completion legitimacy not declared
QD-S-4.3 | FAIL | evidence: same file - prohibitions after failure not declared
QD-S-5.1 | FAIL | evidence: same file - device control and playlist removal present, read/write/delete scopes not distinguished
QD-S-5.3 | FAIL | evidence: same file - no environment boundary declared
QD-S-5.4 | PASS | evidence: same file - no other-Skill chaining declared

### A.4 Defect list (sorted P0 first)

P0 (4): QD-S-1.1, QD-S-1.3, QD-S-2.1, QD-S-3.4
P1 (11): QD-S-1.2, QD-S-1.4, QD-S-1.5, QD-S-2.3, QD-S-2.4, QD-S-3.1, QD-S-3.2, QD-S-4.2, QD-S-4.3, QD-S-5.1, QD-S-5.3
P2 (0): none
QC: no embedded-code QC defect found.

### A.5 Embedded-code QC (code-contract; QC-0 gate first)

QC-0.1 Syntax Parsability | PASS | evidence: the Bash command references are syntactically valid.
QC-0.2 Language Declaration | PASS | evidence: every fenced block carries the `bash` language tag.
QC-0.3 Structural Completeness | PASS | evidence: snippets are complete for their illustrative intent.
QC-0 gate: PASS. Proceed to QC-1 through QC-3.

QC-1.1 Undefined Name Reference | PASS | evidence: `crib` is the documented CLI, not an undefined name.
QC-1.2 Invalid Import | PASS | evidence: no imports used.
QC-1.3 Deprecated API Usage | PASS | evidence: no deprecated APIs used.
QC-1.4 Type Mismatch | PASS | evidence: no incompatible argument types found.
QC-2.1 Unclosed File Handle | PASS | evidence: no file handles opened in the snippets.
QC-2.2 Unreleased Network Connection | PASS | evidence: no network connections in the snippets.
QC-2.3 Missing Exception Handling | PASS | evidence: no high-risk call requires mandatory try/except in these command references.
QC-3.1 Unused Import | PASS | evidence: no imports used.
QC-3.2 Missing Import | PASS | evidence: no imported module referenced.
QC-3.3 Hardcoded Demo Value | PASS | evidence: no credential or demo-secret literal present.

## Stage B - Cross-artifact

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.

## Stage C - Gate-0

- G0-1 (no unfixed P0 in Stage A): informational - Stage A produced 4 P0 findings; recorded and carried forward; does not gate in this non-blocking flow.
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
- NL-A / NL-B (natural language): no data-exfiltration, instruction-override, permission-bypass, or constraint-removal statement. The `--all` / blanket directives are documented capabilities of a user-invoked action, not risk expressions such as "delete all data".
- NR-O (obfuscation): no encoded / zero-width / homoglyph payload.
- NR-S (structured configuration): the `allowed-tools: Bash(crib *)` field scopes execution to the `crib` binary, matching the design scope; no dangerous flag, injected instruction, or abnormal callback address is present.

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
| QD-S-3.1, QD-S-3.2 | AS-01; AS-04 | D1, D2, D3 | FM-02, FM-07, FM-09 | Medium |
| QD-S-3.4 | AS-01; AS-05 | D2, D3 | FM-02, FM-07, FM-09 | Medium |
| QD-S-4.2, QD-S-4.3 | AS-07 | D1, D2, D3, Availability | FM-08, FM-09 | Medium |
| QD-S-5.1 | AS-04; AS-05 | D2, D3 | FM-05, FM-09 | Medium |
| QD-S-5.3 | AS-04; AS-05 | D2, D3 | FM-05, FM-09 | Conditional |

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
