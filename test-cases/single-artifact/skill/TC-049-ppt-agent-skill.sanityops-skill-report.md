# SanityOps Inspect Lite - Skill Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Result status: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-14
Artifact version: not supplied by the user (using the case's Collection Date as the working label)
Inspected artifact: TC-049-ppt-agent-skill.md - Artifact Type: Skill (SKILL.md); case Collection Date 2026-10-13. The artifact body is authored in Chinese; all evidence excerpts below are rendered in English and marked "(translated)" per the output contract.

## Executive summary

- Executed stages: A, C, E, F, G. Stage B and Stage D Not Executed (structural reasons; see status board).
- Stage A defect counts: P0 = 4, P1 = 9, P2 = 0 (QD-S: P0 4 / P1 9 / P2 0; embedded-code QC: 0 findings).
- Gate-0 result: Not passed - G0-4 (no Tool Schema in the artifact set; per-Tool completeness cannot be verified).
- Risk Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0 (no qualifying explicitly declared risk expression found).
- Top findings (rule ID - one-line defect):
  1. QD-S-3.4 - no non_goals / task-scope boundary declared.
  2. QD-S-2.1 - unbounded quantity wording ("use them all" when gathering material) with no cap.
  3. QD-S-1.1 - no upper bound on the number or size of inputs.
  4. QD-S-1.3 - script/tool invocations with no retry count or execution timeout declared.
  5. QD-S-1.4 - no declared tool permission boundary (no `allowed-tools`; scripts run Bash/Python/Node with no read/write/delete distinction).
- What was NOT run: the Risk Implicit subset and the runtime Quality subset (the Stage A embedded-code QC is the only Quality check performed).
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and evidence chains, use sanityops-cli (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

## Stage A - Skill inspection (QD-S)

### A.0 QD-S-0 baseline (entry gate, 6 items)

| ID | Verdict | Evidence |
| --- | --- | --- |
| QD-S-0.1 Required Field Presence | PASS | TC-049-ppt-agent-skill.md, front matter (lines 16-17): `name: ppt-agent` and `description` present |
| QD-S-0.2 Field Content Non-Empty | PASS | both fields non-empty |
| QD-S-0.3 Syntax Parsability | PASS | YAML front matter parses (lines 15-18) |
| QD-S-0.4 Field Type Validity | PASS | both values are strings |
| QD-S-0.5 No Conflicting Declarations | PASS | no mutually contradictory declarations found |
| QD-S-0.6 Minimum Structural Completeness | PASS | front matter + titled body (Core concept / Environment awareness / 6-step pipeline / etc.) |

Baseline result: PASS (6/6). The Skill proceeds to QD-S-1 through QD-S-5 inspection.

### A.1 Skill risk-level determination

Determination: L2 (Medium Risk).
Basis: the Skill performs state-changing resource access and local script/tool execution - it creates files (HTML slides, SVG, PPTX, images), runs Python/Node scripts and `pip install`, and creates an output directory. It declares no deletion / irreversible operation and no sensitive-data handling, so it is not L3; it is above L1 because it is not a pure text-processing skill.
Applied rule set: the L2 minimum rule set = 6 mandatory P0 items + 14 recommended P1 items.

### A.2 Findings by Review Schema dimension (six dimensions)

IDENTITY (what it does / does not do / what it can access)
- QD-S-3.4 FAIL (P0): no non_goals declaration. Evidence (translated): "simulate a professional PPT design company's complete workflow" (Core concept, line 21) with no statement of what the skill does NOT do.
- QD-S-1.4 FAIL (P1): no declared permission boundary and no read/write/delete distinction. Evidence: the front matter declares no `allowed-tools`, while the body runs shell / Python / Node and writes files (Step 6, lines 200-225).
- QD-S-1.5 FAIL (P1): no permitted or prohibited data-source declaration (the skill gathers material via search, Step 2, lines 88-94).
- QD-S-2.4 PASS: capability verbs are specific to presentation generation; no broad manage/handle/process verb used as the capability statement.

TRIGGER (when it should trigger / not trigger)
- QD-S-3.1 FAIL (P1): overly broad activation condition. Evidence (translated): "even if the user only says 'help me make an intro about X' ... as long as it hints at needing structured multi-page presentation content, it should trigger" (description, line 17).
- QD-S-3.2 FAIL (P1): no deactivation conditions declared.
- QD-S-3.6 PASS: name `ppt-agent` and the description are consistent with the body.

INPUT (size, format, overflow behavior)
- QD-S-1.1 FAIL (P0): no upper limit on the number or size of inputs.
- QD-S-3.3 PASS: ambiguous input is handled - Step 1 is a forced interview that asks the user and waits ("Do not skip; ask and wait for the user to reply", translated, line 70).

EXECUTION (boundaries, retries, tool calls, chained calls)
- QD-S-1.3 FAIL (P0): no retry count or execution timeout declared. Evidence: script invocations with no bound (e.g. `python3 SKILL_DIR/scripts/html_packager.py ...`, line 207).
- QD-S-2.1 FAIL (P0): unbounded quantity wording. Evidence (translated): "Inventory every information-acquisition capability, use them all" (Step 2, line 89).
- QD-S-2.2 PASS: no unterminated wording ("until success" etc.) present.
- QD-S-5.1 FAIL (P1): read/modify/delete scopes not distinguished (also listed under IDENTITY).
- QD-S-5.3 FAIL (P1): no permitted/prohibited environment boundary declared.
- QD-S-5.4 PASS: no chained invocation of other Skills declared.

OUTPUT (size, structure, partial completion)
- QD-S-1.2 FAIL (P1): no output-size limit declared. Evidence: the complexity table caps nothing at the top - "Large > 18 pages" has no upper bound (lines 62-66).
- QD-S-2.3 FAIL (P1): open-ended enumeration. Evidence (translated): "10 layouts each as a file (asymmetric / hero-top / l-shape, etc.)" (reference index, line 274).

FAILURE (failures, empty input, insufficient input)
- QD-S-4.1 PASS: failure/degradation behavior is declared - the "Environment awareness" table gives per-capability fallback strategies, and Step 6 declares degradation when Node.js is unavailable ("skip this and step 3, output only preview.html", translated, line 215).
- QD-S-4.2 PASS: partial-completion legitimacy is declared (degraded runs may output preview.html only, line 215).
- QD-S-4.3 FAIL (P1): post-failure prohibited behaviors not declared.

### A.3 Full L2 rule verdicts (one line per rule)

QD-S-1.1 | FAIL | evidence: TC-049-ppt-agent-skill.md, no input count/size maximum declared anywhere in the body
QD-S-1.2 | FAIL | evidence: same file, complexity table (lines 62-66) - "Large > 18 pages" has no upper bound
QD-S-1.3 | FAIL | evidence: same file, Step 6 script invocations (lines 207-218) - no timeout or retry cap
QD-S-1.4 | FAIL | evidence: same file, front matter (lines 16-17) - no `allowed-tools`; body writes files and runs shell/Python/Node
QD-S-1.5 | FAIL | evidence: same file, Step 2 (lines 88-94) - no permitted/prohibited data sources declared
QD-S-2.1 | FAIL | evidence: same file, Step 2 (line 89) - "use them all" (translated);
QD-S-2.2 | PASS | evidence: same file - no unterminated execution wording present
QD-S-2.3 | FAIL | evidence: same file, reference index (line 274) - "asymmetric / hero-top / l-shape, etc." (translated)
QD-S-2.4 | PASS | evidence: same file, description (line 17) - specific generation verbs
QD-S-3.1 | FAIL | evidence: same file, description (line 17) - "as long as it hints at needing structured multi-page presentation content, it should trigger" (translated)
QD-S-3.2 | FAIL | evidence: same file - no statement of when the skill should NOT trigger
QD-S-3.3 | PASS | evidence: same file, Step 1 forced interview (line 70) - asks the user and waits
QD-S-3.4 | FAIL | evidence: same file - no non_goals declaration
QD-S-3.6 | PASS | evidence: same file, front matter (lines 16-17) - name `ppt-agent` consistent with the description
QD-S-4.1 | PASS | evidence: same file, Environment awareness (lines 30-36) + Step 6 degradation (line 215)
QD-S-4.2 | PASS | evidence: same file, Step 6 degradation (line 215) - partial output (preview.html only) is declared acceptable
QD-S-4.3 | FAIL | evidence: same file - prohibitions after failure not declared
QD-S-5.1 | FAIL | evidence: same file - writes files, read/write/delete scopes not distinguished
QD-S-5.3 | FAIL | evidence: same file - no environment boundary declared
QD-S-5.4 | PASS | evidence: same file - no other-Skill chaining declared

### A.4 Defect list (sorted P0 first)

P0 (4): QD-S-1.1, QD-S-1.3, QD-S-2.1, QD-S-3.4
P1 (9): QD-S-1.2, QD-S-1.4, QD-S-1.5, QD-S-2.3, QD-S-3.1, QD-S-3.2, QD-S-4.3, QD-S-5.1, QD-S-5.3
P2 (0): none
QC: no embedded-code QC defect found.

### A.5 Embedded-code QC (code-contract; QC-0 gate first)

QC-0.1 Syntax Parsability | PASS | evidence: the Bash snippets (`pip install ...`, `python3 SKILL_DIR/scripts/...`) are syntactically valid.
QC-0.2 Language Declaration | PASS | evidence: every fenced block carries a language tag (`bash`).
QC-0.3 Structural Completeness | PASS | evidence: snippets are complete for their illustrative intent.
QC-0 gate: PASS. Proceed to QC-1 through QC-3.

QC-1.1 Undefined Name Reference | PASS | evidence: `SKILL_DIR` is a documented path variable, not an undefined name.
QC-1.2 Invalid Import | PASS | evidence: no imports used.
QC-1.3 Deprecated API Usage | PASS | evidence: no deprecated APIs used.
QC-1.4 Type Mismatch | PASS | evidence: no incompatible argument types found.
QC-2.1 Unclosed File Handle | PASS | evidence: no file handles opened in the snippets.
QC-2.2 Unreleased Network Connection | PASS | evidence: no network connections in the snippets.
QC-2.3 Missing Exception Handling | PASS | evidence: `pip install ... 2>/dev/null` suppresses stderr; no high-risk call requires mandatory try/except in the illustrative snippet.
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
- NL-A / NL-B (natural language): no data-exfiltration, instruction-override, permission-bypass, or constraint-removal statement.
- NR-O (obfuscation): no encoded / zero-width / homoglyph payload.
- NR-S (structured configuration): no dangerous flags, abnormal callback addresses, or injected instructions. The fenced code blocks are illustrative script invocations inside natural-language sections, not executable code embedded in structured configuration fields (not NR-S-4).

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
| QD-S-3.1, QD-S-3.2 | AS-01; AS-04 | D1, D2, D3 | FM-02, FM-07, FM-09 | Medium |
| QD-S-3.4 | AS-01; AS-05 | D2, D3 | FM-02, FM-07, FM-09 | Medium |
| QD-S-4.3 | AS-07 | D1, D2, D3, Availability | FM-08, FM-09 | Medium |
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

In-place self-corrections: (1) Chinese artifact excerpts were rendered in English and marked "(translated)" to satisfy the zero-non-ASCII output contract; (2) the EX domain-prefix separator is rendered as an ASCII hyphen (Explicit-P0) and the status-board dash as an ASCII hyphen; (3) no other corrections required.
