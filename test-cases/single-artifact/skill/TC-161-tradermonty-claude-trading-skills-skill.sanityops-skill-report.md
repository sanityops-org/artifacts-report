# SanityOps Inspect Lite - Skill Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Result status: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-15
Artifact version: not supplied by the user (using the case's Collection Date as the working label)
Inspected artifact: TC-161-tradermonty-claude-trading-skills-skill.md - Artifact Type: Skill (SKILL.md); case Collection Date 2026-10-14

## Executive summary

- Executed stages: A, C, E, F, G. Stage B and Stage D Not Executed (structural reasons; see status board).
- Stage A defect counts: P0 = 4, P1 = 4, P2 = 0 (QD-S: P0 4 / P1 4 / P2 0; embedded-code QC: 0 findings; QC-1.2/QC-1.3 Not Executed - no dependency list / API database).
- Gate-0 result: Not passed - G0-4 (no Tool Schema in the artifact set; per-Tool completeness cannot be verified).
- Risk Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0 (no qualifying explicitly declared risk expression found).
- Top findings (rule ID - one-line defect):
  1. QD-S-1.3 - the Skill runs a Python script but declares no retry count, tool-invocation count, or execution timeout.
  2. QD-S-1.1 - no upper limit on input number or size.
  3. QD-S-3.4 - no non_goals declaration (only a positive "long stock trades" scope statement).
  4. QD-S-4.1 - no execution-failure behavior declared.
  5. QD-S-1.4 - no read/write/delete permission-type distinction or prohibited-operation declaration.
- What was NOT run: the Risk Implicit subset and the runtime Quality subset (the Stage A embedded-code QC is the only Quality check performed; its QC-1.2/QC-1.3 sub-items were Not Executed for lack of external inputs).
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and evidence chains, use sanityops-cli (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

## Stage A - Skill inspection (QD-S)

### A.0 QD-S-0 baseline (entry gate, 6 items)

| ID | Verdict | Evidence |
| --- | --- | --- |
| QD-S-0.1 Required Field Presence | PASS | TC-161-tradermonty-claude-trading-skills-skill.md, front matter (lines 14-15): `name: position-sizer` and `description: ...` present |
| QD-S-0.2 Field Content Non-Empty | PASS | both fields carry content |
| QD-S-0.3 Syntax Parsability | PASS | YAML front matter parses |
| QD-S-0.4 Field Type Validity | PASS | `name` and `description` are strings |
| QD-S-0.5 No Conflicting Declarations | PASS | no mutually contradictory declarations found |
| QD-S-0.6 Minimum Structural Completeness | PASS | front matter plus a titled body (Overview, When to Use, Prerequisites, Workflow Steps 1-6, Output Format, Key Principles) |

Baseline result: PASS (6/6). The Skill proceeds to QD-S-1 through QD-S-5 inspection.

### A.1 Skill risk-level determination

Determination: L2 (Medium Risk).
Basis: per the checklist's risk-level semantics, L2 = resource access, may involve sensitive data. The Skill executes a calculation script (`python3 skills/position-sizer/scripts/position_sizer.py`) and writes report files to `reports/`, so it goes beyond text-processing-only L1. It declares no deletion or irreversible operation and no permission change (and `## Prerequisites` records "No API keys required", "standard library only"), so it is not L3.
Applied rule set: the L2 minimum rule set = 6 mandatory P0 items (QD-S-1.1, QD-S-1.3, QD-S-2.1, QD-S-2.2, QD-S-3.4, QD-S-4.1) + 14 recommended P1 items (QD-S-1.2, QD-S-1.4, QD-S-1.5, QD-S-2.3, QD-S-2.4, QD-S-3.1, QD-S-3.2, QD-S-3.3, QD-S-3.6, QD-S-4.2, QD-S-4.3, QD-S-5.1, QD-S-5.3, QD-S-5.4).

### A.2 Findings by Review Schema dimension (six dimensions)

IDENTITY (what it does / does not do / what it can access)
- QD-S-3.4 FAIL (P0): no non_goals declaration. Evidence: "description: Calculate risk-based position sizes for long stock trades." scopes the Skill positively but states no explicit non_goals (e.g., it does not state that it excludes short trades, options, or portfolio construction).
- QD-S-1.4 FAIL (P1): no read/write/delete permission-type distinction and no prohibited-operation declaration. Evidence: "Reports are saved to `reports/` with filenames `position_sizer_YYYY-MM-DD_HHMMSS.json` and `.md`." declares a file-write but no prohibited operation types.
- QD-S-1.5 FAIL (P1): no permitted/prohibited data source declared. Evidence: "If the user provides a stock ticker but not specific prices, use available tools to look up the current price and suggest entry/stop levels based on technical analysis." names a data lookup but declares no permitted/prohibited data-source boundary.

TRIGGER (when it should trigger / not trigger)
- QD-S-3.1 PASS (P1): activation conditions are concrete. Evidence: "## When to Use - User asks \"how many shares should I buy?\" - User wants to calculate position size for a specific trade setup ...".
- QD-S-3.2 FAIL (P1): no deactivation conditions declared. Evidence: "## When to Use" lists five positive user intents and states no condition under which the Skill should NOT trigger.
- QD-S-3.6 PASS (P1): `name: position-sizer` and the `description` are consistent with the body.

INPUT (size, format, overflow behavior)
- QD-S-1.1 FAIL (P0): no upper limit on input number or size. Evidence: "### Step 1: Gather Trade Parameters Collect from the user: - **Required**: Account size (total equity) - **Mode A (Fixed Fractional)**: Entry price, stop price, risk percentage (default 1%)" declares no cap.
- QD-S-3.3 PASS (P1): ambiguous/insufficient input is handled. Evidence: "If the user provides a stock ticker but not specific prices, use available tools to look up the current price and suggest entry/stop levels based on technical analysis."

EXECUTION (boundaries, retries, tool calls, chained calls)
- QD-S-1.3 FAIL (P0): a script is invoked but no retry count, tool-invocation count, or execution timeout is set. Evidence: "python3 skills/position-sizer/scripts/position_sizer.py --account-size 100000 --entry 155 --stop 148.50 --risk-pct 1.0 --output-dir reports/" is invoked with no execution budget declared.
- QD-S-5.4 PASS (P1): no chained invocation of other Skills declared; `references/sizing_methodologies.md` is a documentation reference.

OUTPUT (size, structure, partial completion)
- QD-S-1.2 PASS (P1): output structure is bounded. Evidence: the fixed "### JSON Report" schema ("schema_version", "mode", "parameters", "calculations", "final_recommended_shares" ...) plus the "### Markdown Report" description.
- QD-S-2.3 PASS (P1): no open-ended enumeration ("etc.", "and others") in the output/functional structure.
- QD-S-4.2 PASS (P1): partial completion is not a concept for this single-shot calculation; the output is a single deterministic JSON/Markdown report with a fixed schema.

FAILURE (failures, empty input, insufficient input)
- QD-S-4.1 FAIL (P0): no failure behavior declared. Evidence: "## Prerequisites - No API keys required - Python 3.9+ with standard library only" declares the environment but no behavior for a script failure, invalid input, or unsatisfiable request.
- QD-S-4.3 FAIL (P1): no post-failure prohibited behaviors declared. Evidence: "## Key Principles 1. **Survival first**: Position sizing is about surviving losing streaks, not maximizing winners" states principles but no post-failure prohibitions.

(Additional L2 items carried here for completeness)
- QD-S-2.1 PASS (P0): no unbounded exhaustive-processing directive; "All methods apply portfolio constraints" is a bounded reference to the three declared methods.
- QD-S-2.2 PASS (P0): no "keep trying / until success / ensure complete / persist until" wording present.
- QD-S-2.4 PASS (P1): verbs are specific ("Calculate risk-based position sizes"); no broad manage/handle/process verb used as the capability statement.
- QD-S-5.1 PASS (P1): the only declared data operation is writing a report to `reports/`; no delete or modify operation is declared, so read/write/delete scopes are not conflated.
- QD-S-5.3 PASS (P1): operations target a local `reports/` directory; no production-environment operation is declared.

### A.3 Full L2 rule verdicts (one line per rule)

QD-S-1.1 | FAIL | evidence: TC-161-tradermonty-claude-trading-skills-skill.md, Step 1 - "Account size (total equity)" and mode parameters with no input cap
QD-S-1.2 | PASS | evidence: same file, Output Format - fixed JSON + Markdown report schema
QD-S-1.3 | FAIL | evidence: same file, Step 2 - "python3 skills/position-sizer/scripts/position_sizer.py ..." with no retry/timeout bound
QD-S-1.4 | FAIL | evidence: same file - "Reports are saved to `reports/`..." with no prohibited-operation declaration
QD-S-1.5 | FAIL | evidence: same file, Step 1 - "use available tools to look up the current price" with no data-source boundary
QD-S-2.1 | PASS | evidence: same file - no unbounded quantity wording used as an execution instruction
QD-S-2.2 | PASS | evidence: same file - no unterminated-execution wording present
QD-S-2.3 | PASS | evidence: same file - no open-ended enumeration in output/functional structure
QD-S-2.4 | PASS | evidence: same file, description - specific verb "Calculate risk-based position sizes"
QD-S-3.1 | PASS | evidence: same file, "## When to Use" - concrete user intents
QD-S-3.2 | FAIL | evidence: same file - no statement of when the skill should NOT trigger
QD-S-3.3 | PASS | evidence: same file, Step 1 - "If the user provides a stock ticker but not specific prices, use available tools to look up the current price"
QD-S-3.4 | FAIL | evidence: same file - no non_goals declaration
QD-S-3.6 | PASS | evidence: same file, front matter - name `position-sizer` consistent with the description
QD-S-4.1 | FAIL | evidence: same file - no failure-behavior declaration present
QD-S-4.2 | PASS | evidence: same file - single-shot deterministic output, no completeness pursuit
QD-S-4.3 | FAIL | evidence: same file - no post-failure prohibited behaviors declared
QD-S-5.1 | PASS | evidence: same file - report write only; no delete/modify declared
QD-S-5.3 | PASS | evidence: same file - local `reports/` output only
QD-S-5.4 | PASS | evidence: same file - no other-Skill chaining declared

### A.4 Defect list (sorted P0 first)

P0 (4): QD-S-1.1, QD-S-1.3, QD-S-3.4, QD-S-4.1
P1 (4): QD-S-1.4, QD-S-1.5, QD-S-3.2, QD-S-4.3
P2 (0): none

### A.5 Embedded-code QC (code-contract; QC-0 gate first)

QC-0.1 Syntax Parsability | PASS | the `bash` command blocks parse as valid shell; the `json` block parses as valid JSON.
QC-0.2 Language Declaration | PASS | the fenced blocks carry the `bash` and `json` language tags.
QC-0.3 Structural Completeness | PASS | the CLI invocations and the JSON schema example are complete for their illustrative intent.
QC-0.4 Fence Integrity | PASS | all code fences open and close correctly.
QC-0.5 Language-Content Mismatch | PASS | tags match content (`bash` for commands, `json` for the report schema).
QC-0 gate: PASS. Proceed to QC-1 through QC-4.
QC-1.1 Undefined Name Reference | PASS | `python3` is an external binary; the `--account-size`/`--entry`/`--stop` flags are the script's declared CLI interface.
QC-1.2 Invalid Import | Not Executed | no declared dependency list is available (lite default).
QC-1.3 Deprecated API Usage | Not Executed | no API version database is available (lite default).
QC-1.4 Type Mismatch | PASS | no incompatible argument types found in the CLI examples.
QC-2.1 Unclosed File Handle | PASS | no file handles opened in the snippets.
QC-2.2 Unreleased Network Connection | PASS | no network connection objects in the snippets.
QC-2.3 Missing Exception Handling | PASS | the snippets are CLI invocations, not code performing high-risk file/network/DB operations.
QC-3.1 Unused Import | PASS | no imports present.
QC-3.2 Missing Import | PASS | no module referenced.
QC-3.3 Hardcoded Demo Value | PASS | the numeric values (100000, 155, 148.50) are illustrative CLI example arguments; no credentials, machine-specific paths or internal IPs are present.
QC-4.1 Snippet-Artifact Declaration Mismatch | PASS | the CLI parameters match the JSON schema fields in the body.
QC-4.2 Snippet-Body Version/API Drift | PASS | no version/API drift between snippets and body.

## Stage B - Cross-artifact

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available. Cross-artifact relationships (QD-PS/QD-PT/QD-ST/QD-CYC) require at least two of the three artifact types from one agent; only a single Skill is present.

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
- NL-A / NL-B (natural language): no data-exfiltration, instruction-override, permission-bypass, or constraint-removal statement. The risk-management rules ("never exceed 2%", "Half Kelly") are defensive constraints.
- NR-O (obfuscation): no encoded / zero-width / homoglyph payload.
- NR-S (structured configuration): no dangerous flags and no hardcoded credentials or PII. The JSON example contains only trade parameters (entry price, account size), not secrets or personal data. The FINRA regulatory note is a public rule reference.

Risk Item Summary: Total 0; Explicit-P0 = 0; Explicit-P1 = 0; Explicit-P2 = 0.
Note: this is a static-document risk scan; Risk Implicit (dynamic exploitability) was NOT run. An EX finding would be a static-document risk, never a confirmed exploit.

## Stage F - Impact outlook (candidate mapping, advisory only)  [separate from the verdicts]

Mandatory statements: Risk Implicit NOT run (dynamic exploitability unverified); the runtime Quality subset NOT run (only the Stage A embedded-code QC ran, and its QC-1.2/QC-1.3 sub-items were Not Executed); per relevance.md section 1.4 no assumption is made that controls outside the artifacts are absent.

Candidate mapping - one row per FAIL; strength is provisional (lite) and reflects association confidence only, NOT severity:

| Defect | Candidate attack surface | Potential impact | Candidate failure mode | Strength (provisional) |
| --- | --- | --- | --- | --- |
| QD-S-1.1, QD-S-1.3 | AS-06 Resource Exhaustion and Runaway Execution | Availability | FM-08, FM-10 | Conditional |
| QD-S-3.4 | AS-01 Instruction and Context Boundary Confusion; AS-05 Tool Misuse and High-Risk Side Effects | D2, D3 | FM-02, FM-07, FM-09 | Medium |
| QD-S-1.4 | AS-04 Permission, Identity and Delegation Expansion; AS-05 | D2, D3 | FM-05, FM-09 | Medium |
| QD-S-1.5 | AS-01; AS-03 Output Handling and Sensitive Data Exfiltration; AS-04 | D1, D3 | FM-05, FM-09 | Conditional |
| QD-S-3.2 | AS-01; AS-04 | D1, D2, D3 | FM-02, FM-07, FM-09 | Conditional |
| QD-S-4.1, QD-S-4.3 | AS-07 Anomaly Propagation and Cascading Failures | D1, D2, D3, Availability | FM-08, FM-09 | Conditional |

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

In-place self-corrections: (1) artifact arrows/en dashes were rendered in plain ASCII within evidence; (2) the EX domain-prefix separator and the status-board dash are ASCII hyphens; (3) all emitted QD-S/QC IDs are present in skill-checklist.md / code-contract-checklist.md, and all AS-*/FM-* codes are present in relevance-map.md.
