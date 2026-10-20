# SanityOps Inspect Lite - Skill Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Result status: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-15
Artifact version: not supplied by the user (using the case's Collection Date as the working label)
Inspected artifact: TC-159-weizhena-deep-research-skills-skill.md - Artifact Type: Skill (SKILL.md); case Collection Date 2026-10-13

## Executive summary

- Executed stages: A, C, E, F, G. Stage B and Stage D Not Executed (structural reasons; see status board).
- Stage A defect counts: P0 = 4, P1 = 6, P2 = 0 (QD-S: P0 4 / P1 6 / P2 0; embedded-code QC: 0 findings; QC-1.2/QC-1.3 Not Executed - no dependency list / API database).
- Gate-0 result: Not passed - G0-4 (no Tool Schema in the artifact set; per-Tool completeness cannot be verified).
- Risk Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0 (no qualifying explicitly declared risk expression found).
- Top findings (rule ID - one-line defect):
  1. QD-S-3.4 - no non_goals declaration for the Skill's own task scope.
  2. QD-S-1.3 - no retry count, tool-invocation count, or execution timeout declared for the launched sub-agent and script/file operations.
  3. QD-S-1.1 - no upper limit on input number or size.
  4. QD-S-4.1 - no execution-failure behavior declared.
  5. QD-S-2.3 - open-ended enumeration present ("... technology selection, etc.").
- What was NOT run: the Risk Implicit subset and the runtime Quality subset (the Stage A embedded-code QC is the only Quality check performed; its QC-1.2/QC-1.3 sub-items were Not Executed for lack of external inputs).
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and evidence chains, use sanityops-cli (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

## Stage A - Skill inspection (QD-S)

### A.0 QD-S-0 baseline (entry gate, 6 items)

| ID | Verdict | Evidence |
| --- | --- | --- |
| QD-S-0.1 Required Field Presence | PASS | TC-159-weizhena-deep-research-skills-skill.md, front matter (lines 14-17): `name: research`, `user-invocable: true`, `allowed-tools: ...`, `description: ...` present |
| QD-S-0.2 Field Content Non-Empty | PASS | all fields carry content |
| QD-S-0.3 Syntax Parsability | PASS | YAML front matter parses |
| QD-S-0.4 Field Type Validity | PASS | `name`/`description`/`allowed-tools` are strings; `user-invocable` is a boolean |
| QD-S-0.5 No Conflicting Declarations | PASS | no mutually contradictory declarations found |
| QD-S-0.6 Minimum Structural Completeness | PASS | front matter plus a titled body (Trigger, Workflow Steps 1-5, Output Path, Follow-up Commands) |

Baseline result: PASS (6/6). The Skill proceeds to QD-S-1 through QD-S-5 inspection.

### A.1 Skill risk-level determination

Determination: L2 (Medium Risk).
Basis: per the checklist's risk-level semantics, L2 = resource access, may involve sensitive data. The Skill declares tool invocations (`allowed-tools: Read, Write, Glob, WebSearch, Task, AskUserQuestion`), launches a background web-search sub-agent, and writes files (`outline.yaml`, `fields.yaml`) into the working directory, so it goes beyond text-processing-only L1. It declares no deletion or irreversible operation and no permission change, so it is not L3.
Applied rule set: the L2 minimum rule set = 6 mandatory P0 items (QD-S-1.1, QD-S-1.3, QD-S-2.1, QD-S-2.2, QD-S-3.4, QD-S-4.1) + 14 recommended P1 items (QD-S-1.2, QD-S-1.4, QD-S-1.5, QD-S-2.3, QD-S-2.4, QD-S-3.1, QD-S-3.2, QD-S-3.3, QD-S-3.6, QD-S-4.2, QD-S-4.3, QD-S-5.1, QD-S-5.3, QD-S-5.4).

### A.2 Findings by Review Schema dimension (six dimensions)

IDENTITY (what it does / does not do / what it can access)
- QD-S-3.4 FAIL (P0): no non_goals declaration. Evidence: "description: Conduct preliminary research on a topic and generate research outline. For academic research, benchmark research, technology selection, etc." states what the Skill does but never states what it does NOT do for its own task scope.
- QD-S-1.4 FAIL (P1): no read/write/delete permission-type distinction and no prohibited-operation declaration. Evidence: "allowed-tools: Read, Write, Glob, WebSearch, Task, AskUserQuestion" lists tool names but declares no prohibited operations.
- QD-S-1.5 PASS (P1): the data source toolset is declared. Evidence: `allowed-tools` bounds the reachable sources, and the sub-agent contract states "Return structured results directly (do not write files)".

TRIGGER (when it should trigger / not trigger)
- QD-S-3.1 PASS (P1): activation is concrete. Evidence: "## Trigger `/research <topic>`".
- QD-S-3.2 FAIL (P1): no deactivation conditions declared. Evidence: "## Trigger `/research <topic>`" states only the positive trigger, with no statement of when the Skill should NOT trigger.
- QD-S-3.6 PASS (P1): `name: research` and the `description` are consistent with the body.

INPUT (size, format, overflow behavior)
- QD-S-1.1 FAIL (P0): no upper limit on input number or size. Evidence: "### Step 3: Ask User for Existing Fields Use AskUserQuestion to ask if user has existing field definition file, if so read and merge." reads an arbitrary user file with no size/count cap declared.
- QD-S-3.3 PASS (P1): ambiguous/insufficient input is handled. Evidence: "Use AskUserQuestion to confirm: - Need to add/remove items? - Does field framework meet requirements?".

EXECUTION (boundaries, retries, tool calls, chained calls)
- QD-S-1.3 FAIL (P0): tool invocations are declared but no retry count, tool-invocation count, or execution timeout is set. Evidence: "- batch_size: Number of parallel agents (confirm with AskUserQuestion) - items_per_agent: Items per agent (confirm with AskUserQuestion)" leaves the execution budget open-ended, and no timeout is declared for the launched sub-agent.
- QD-S-5.4 FAIL (P1): a sub-agent is invoked without declaring the permitted/prohibited downstream scope. Evidence: "Launch 1 web-search-agent (background)" plus `allowed-tools: ... Task ...`.

OUTPUT (size, structure, partial completion)
- QD-S-1.2 PASS (P1): output structure is bounded. Evidence: "**outline.yaml** (items + config): - topic: Research topic - items: Research objects list - execution: ..." and "**fields.yaml** (field definitions)" define the output schema.
- QD-S-2.3 FAIL (P1): open-ended enumeration present. Evidence: "For academic research, benchmark research, technology selection, etc."
- QD-S-4.2 FAIL (P1): no partial-completion legitimacy declared. Evidence: "### Step 4: Generate Outline (Separate Files) Merge {step1_output}, {step2_output} and user's existing fields, generate two files" mandates two complete files with no partial-result policy.

FAILURE (failures, empty input, insufficient input)
- QD-S-4.1 FAIL (P0): no failure behavior declared. Evidence: the workflow proceeds "### Step 5: Output and Confirm - Create directory: `./{topic_slug}/` - Save: `outline.yaml` and `fields.yaml`" with no error/unsatisfiable-request path.
- QD-S-4.3 FAIL (P1): no post-failure prohibited behaviors declared. Evidence: "**Hard Constraint**: The following prompt must be strictly reproduced, only replacing variables in {xxx}, do not modify structure or wording." is a consistency constraint, not a post-failure prohibition.

(Additional L2 items carried here for completeness)
- QD-S-2.1 PASS (P0): no unbounded exhaustive-processing directive; no "all/every/entire/complete" quantity wording is used as an execution instruction.
- QD-S-2.2 PASS (P0): no "keep trying / until success / ensure complete / persist until" wording present.
- QD-S-2.4 PASS (P1): verbs are specific ("Conduct preliminary research ... generate research outline"); no broad manage/handle/process verb used as the capability statement.
- QD-S-5.1 PASS (P1): read/write scopes are distinguished at the tool level ("Read, Write"), and no delete operation is declared.
- QD-S-5.3 PASS (P1): operations target the local working directory (`./{topic_slug}/`); no production-environment operation is declared.

### A.3 Full L2 rule verdicts (one line per rule)

QD-S-1.1 | FAIL | evidence: TC-159-weizhena-deep-research-skills-skill.md, Step 3 - "read and merge" an arbitrary user file with no size/count cap
QD-S-1.2 | PASS | evidence: same file, Step 4 - defined `outline.yaml` / `fields.yaml` output schema
QD-S-1.3 | FAIL | evidence: same file, Step 4 execution config - "batch_size: Number of parallel agents" with no bound and no timeout
QD-S-1.4 | FAIL | evidence: same file, front matter - "allowed-tools: Read, Write, Glob, WebSearch, Task, AskUserQuestion" with no prohibited-operation declaration
QD-S-1.5 | PASS | evidence: same file, sub-agent contract - "Return structured results directly (do not write files)"
QD-S-2.1 | PASS | evidence: same file - no unbounded quantity wording used as an execution instruction
QD-S-2.2 | PASS | evidence: same file - no unterminated-execution wording present
QD-S-2.3 | FAIL | evidence: same file, description - "For academic research, benchmark research, technology selection, etc."
QD-S-2.4 | PASS | evidence: same file, description - specific verb "Conduct preliminary research"
QD-S-3.1 | PASS | evidence: same file, "## Trigger `/research <topic>`" - concrete trigger
QD-S-3.2 | FAIL | evidence: same file - no statement of when the skill should NOT trigger
QD-S-3.3 | PASS | evidence: same file, Step 1 - "Use AskUserQuestion to confirm: - Need to add/remove items?"
QD-S-3.4 | FAIL | evidence: same file - no non_goals declaration
QD-S-3.6 | PASS | evidence: same file, front matter - name `research` consistent with the description
QD-S-4.1 | FAIL | evidence: same file - no failure-behavior declaration present
QD-S-4.2 | FAIL | evidence: same file, Step 4 - two files mandated with no partial-result policy
QD-S-4.3 | FAIL | evidence: same file, "Hard Constraint" - a reproduction constraint, not a post-failure prohibition
QD-S-5.1 | PASS | evidence: same file - "Read, Write" distinguished; no delete declared
QD-S-5.3 | PASS | evidence: same file - local working-directory output only
QD-S-5.4 | FAIL | evidence: same file - "Launch 1 web-search-agent" with no declared downstream scope

### A.4 Defect list (sorted P0 first)

P0 (4): QD-S-1.1, QD-S-1.3, QD-S-3.4, QD-S-4.1
P1 (6): QD-S-1.4, QD-S-2.3, QD-S-3.2, QD-S-4.2, QD-S-4.3, QD-S-5.4
P2 (0): none

### A.5 Embedded-code QC (code-contract; QC-0 gate first)

QC-0.1 Syntax Parsability | PASS | the `python` fenced block is an illustrative f-string (the case Notes confirm it is illustrative); illustrative-snippet exemption applies.
QC-0.2 Language Declaration | PASS | the Python block carries the `python` tag; the untagged blocks contain plain-text prompt/output templates, not code.
QC-0.3 Structural Completeness | PASS | illustrative-snippet exemption applies; the elided `...` lines are intentional elision.
QC-0.4 Fence Integrity | PASS | code fences open and close correctly.
QC-0.5 Language-Content Mismatch | PASS | the `python` tag matches the f-string content; no mismatch.
QC-0 gate: PASS. Proceed to QC-1 through QC-4.
QC-1.1 Undefined Name Reference | PASS | the f-string placeholders ({topic}, {YYYY-MM-DD}, {step1_output}, {time_range}) are documented template variables.
QC-1.2 Invalid Import | Not Executed | no declared dependency list is available (lite default).
QC-1.3 Deprecated API Usage | Not Executed | no API version database is available (lite default).
QC-1.4 Type Mismatch | PASS | no incompatible argument types found.
QC-2.1 Unclosed File Handle | PASS | no file handles opened in the snippets.
QC-2.2 Unreleased Network Connection | PASS | no network connection objects in the snippets.
QC-2.3 Missing Exception Handling | PASS | no high-risk file/network/DB operation inside the snippets.
QC-3.1 Unused Import | PASS | no imports present.
QC-3.2 Missing Import | PASS | no module referenced.
QC-3.3 Hardcoded Demo Value | PASS | no placeholder credentials or machine-specific paths present.
QC-4.1 Snippet-Artifact Declaration Mismatch | PASS | the illustrative snippet is consistent with the body's parameter list.
QC-4.2 Snippet-Body Version/API Drift | PASS | no version/API drift between snippet and body.

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
- NL-A / NL-B (natural language): no data-exfiltration, instruction-override, permission-bypass, or constraint-removal statement. The "Hard Constraint" that pins the sub-agent prompt is a consistency constraint, not a risk instruction.
- NR-O (obfuscation): no encoded / zero-width / homoglyph payload.
- NR-S (structured configuration): no dangerous flags and no hardcoded credentials or PII. The example date (2025-12-30) and illustrative source URLs are examples, not secrets.

Risk Item Summary: Total 0; Explicit-P0 = 0; Explicit-P1 = 0; Explicit-P2 = 0.
Note: this is a static-document risk scan; Risk Implicit (dynamic exploitability) was NOT run. An EX finding would be a static-document risk, never a confirmed exploit.

## Stage F - Impact outlook (candidate mapping, advisory only)  [separate from the verdicts]

Mandatory statements: Risk Implicit NOT run (dynamic exploitability unverified); the runtime Quality subset NOT run (only the Stage A embedded-code QC ran, and its QC-1.2/QC-1.3 sub-items were Not Executed); per relevance.md section 1.4 no assumption is made that controls outside the artifacts are absent.

Candidate mapping - one row per FAIL; strength is provisional (lite) and reflects association confidence only, NOT severity:

| Defect | Candidate attack surface | Potential impact | Candidate failure mode | Strength (provisional) |
| --- | --- | --- | --- | --- |
| QD-S-1.1, QD-S-1.3 | AS-06 Resource Exhaustion and Runaway Execution | Availability | FM-08, FM-10 | Conditional |
| QD-S-3.4 | AS-01 Instruction and Context Boundary Confusion; AS-05 Tool Misuse and High-Risk Side Effects | D2, D3 | FM-02, FM-07, FM-09 | Medium |
| QD-S-4.1, QD-S-4.2, QD-S-4.3 | AS-07 Anomaly Propagation and Cascading Failures | D1, D2, D3, Availability | FM-08, FM-09 | Conditional |
| QD-S-1.4, QD-S-5.4 | AS-04 Permission, Identity and Delegation Expansion; AS-05 | D2, D3 | FM-05, FM-09 | Medium |
| QD-S-2.3 | AS-06; AS-07 | Availability, Integrity | FM-08, FM-10 | Conditional |
| QD-S-3.2 | AS-01; AS-04 | D1, D2, D3 | FM-02, FM-07, FM-09 | Conditional |

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
