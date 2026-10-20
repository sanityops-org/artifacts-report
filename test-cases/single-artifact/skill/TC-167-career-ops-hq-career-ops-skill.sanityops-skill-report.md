# SanityOps Inspect Lite - Skill Inspection Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-15
Artifact version: not supplied by the user (using the case's Collection Date 2026-10-14 as the working label)
Inspected artifact: TC-167-career-ops-hq-career-ops-skill.md - Artifact Type: Skill (SKILL.md); case Collection Date 2026-10-14

## Executive summary

- Executed stages: A, C, E, F, G. Stage B and Stage D Not Executed (structural reasons; see status board).
- Stage A defect counts: P0 = 2, P1 = 3, P2 = 0 (QD-S: P0 2 / P1 3 / P2 0; embedded-code QC: 0 findings).
- Gate-0 result: Not passed - G0-4 (no Tool Schema in the artifact set; per-Tool completeness cannot be verified).
- Risk Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0 (no qualifying explicitly declared risk expression found).
- Top findings (rule ID - one-line defect):
  1. QD-S-1.1 - no upper limit declared on input number or size (JD text, URLs, document imports).
  2. QD-S-1.3 - no retry count, tool-invocation count, or execution timeout declared for the tool-driven modes (`scan`, `apply`, `batch`).
  3. QD-S-3.2 - no deactivation condition declared.
  4. QD-S-4.3 - no post-failure prohibited behaviors declared.
  5. QD-S-5.4 - subagent delegation declared without a permitted/prohibited downstream Skill scope.
- What was NOT run: the Risk Implicit subset and the runtime Quality subset (the Stage A embedded-code QC is the only Quality check performed).
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and evidence chains, use sanityops-cli (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

## Stage A - Skill inspection (QD-S)

### A.0 QD-S-0 baseline (entry gate, 6 items)

| ID | Verdict | Evidence |
| --- | --- | --- |
| QD-S-0.1 Required Field Presence | PASS | TC-167-career-ops-hq-career-ops-skill.md, front matter (lines 14-24): `name: career-ops`, a multiline `description`, plus router fields (`arguments`, `user_invocable`, `user-invocable`, `argument-hint`, `license`) |
| QD-S-0.2 Field Content Non-Empty | PASS | all present fields carry content; the `argument-hint` enumerates the supported modes |
| QD-S-0.3 Syntax Parsability | PASS | YAML front matter parses (folded-scalar `description`, boolean and string fields) |
| QD-S-0.4 Field Type Validity | PASS | `name`/`description`/`arguments`/`license` are strings; `user_invocable`/`user-invocable` are booleans |
| QD-S-0.5 No Conflicting Declarations | PASS | no mutually contradictory declarations found (the `user_invocable` / `user-invocable` keys are duplicate spellings of the same value `true`, not a contradiction) |
| QD-S-0.6 Minimum Structural Completeness | PASS | front matter plus a titled body (router, project-root resolution, invocation notes, mode routing, output-language directive, context loading by mode, subagent delegation) |

Baseline result: PASS (6/6). The Skill proceeds to QD-S-1 through QD-S-5 inspection.

### A.1 Skill risk-level determination

Determination: L2 (Medium Risk).
Basis: per the checklist's risk-level semantics, L2 = resource access, may involve sensitive data. This Skill is a job-search command center that reads and writes project files (tracker, pipeline, config), reads `config/profile.yml`, and drives external portal tools via delegated workers. No irreversible operation (delete, overwrite, permission change) is declared, so it is not L3.
Applied rule set: the L2 minimum rule set = 6 mandatory P0 items + 14 recommended P1 items.

### A.2 Findings by Review Schema dimension (six dimensions)

IDENTITY (what it does / does not do / what it can access)
- QD-S-3.4 PASS (P0): a task-scope boundary is declared. Evidence: the `email` mode is "Formal application email draft (draft-only; never sends, submits, or clicks)"; `triage` "writes no files"; `intake` operates with "nothing written without confirm".
- QD-S-1.4 PASS (P1): permission boundaries are declared. Evidence: mode-level operation boundaries ("draft-only; never sends, submits, or clicks"; "writes no files"; "nothing written without confirm").
- QD-S-1.5 PASS (P1): the data the router reads is scoped. Evidence: it reads `config/profile.yml`, `modes/*.md`, and `data/*.md` by explicit path.
- QD-S-2.4 PASS (P1): the capability is a router over an enumerated mode set; no broad manage/handle verb is used as the capability statement.
- QD-S-5.1 PASS (P1): no conflation of read/write/delete; write actions carry explicit confirm/opt-in gates (`latex-tex` is "opt-in"; `intake` writes only on confirm).

TRIGGER (when it should trigger / not trigger)
- QD-S-3.1 PASS (P1): activation is concrete. Evidence: the description states triggers ("pastes a job URL or JD, asks to scan portals, generate a CV/PDF, track applications, ...") and the "## Mode Routing" table maps each input token to a mode.
- QD-S-3.2 FAIL (P1): no deactivation conditions declared. Evidence: the artifact enumerates sub-commands and a fallback ("If `$mode` is not a sub-command AND doesn't look like a JD, show discovery") but states no condition under which the Skill should NOT trigger.
- QD-S-3.6 PASS (P1): name `career-ops` and the description are consistent with the router body.

INPUT (size, format, overflow behavior)
- QD-S-1.1 FAIL (P0): no upper limit on input number or size. Evidence: the router accepts JD text, URLs and "document imports" with no declared cap on the number or size of inputs.
- QD-S-3.3 PASS (P1): ambiguous input is handled. Evidence: "If genuinely ambiguous, an interactive session asks and stops before persistence; an unattended worker uses the primary market and records that fallback in the report header or Block G."

EXECUTION (boundaries, retries, tool calls, chained calls)
- QD-S-1.3 FAIL (P0): no execution resource boundary declared. Evidence: modes `scan`, `apply` (with Playwright) and `pipeline` (3+ URLs) involve tool invocations and delegated workers, but no retry count, tool-invocation count, or execution timeout is declared.
- QD-S-5.4 FAIL (P1): chained/delegated invocation is declared without a permitted/prohibited downstream scope. Evidence: "Modes delegated to subagent ... launch as a worker/subagent" using `Agent(subagent_type="general-purpose", prompt=..., description=...)`, with no downstream Skill whitelist declared.

OUTPUT (size, structure, partial completion)
- QD-S-1.2 PASS (P1): the router's own output is bounded. Evidence: no-argument input shows a fixed "career-ops -- Command Center" menu; the output-language directive injects one bounded paragraph.
- QD-S-2.3 PASS (P1): no open-ended enumeration ("etc." / "and others" / "such as") is used in a functional structure; the mode list is closed.

FAILURE (failures, empty input, insufficient input)
- QD-S-4.1 PASS (P0): a failure behavior is declared. Evidence: "If those two sentinels cannot be found, stop and locate the career-ops checkout before reading or writing files."
- QD-S-4.2 PASS (P1): partial completion is accommodated. Evidence: the unattended-worker fallback path (use the primary market and record the fallback) accepts a degraded result.
- QD-S-4.3 FAIL (P1): no post-failure prohibited behaviors declared. Evidence: the router states no explicit prohibitions on what the model must NOT do after a failure.

(Additional L2 items carried here for completeness)
- QD-S-2.1 PASS (P0): the "every"/"all" usages are bounded by declared sets ("EVERY declared market's `_shared.md`", "every declared directory's `_shared.md`"), not unbounded quantity directives.
- QD-S-2.2 PASS (P0): no unterminated-execution wording (`keep trying / until success / ensure complete / persist until`) present.
- QD-S-5.3 PASS (P1): the Skill is declared local-first, so no production-environment operation is introduced.

### A.3 Full L2 rule verdicts (one line per rule)

QD-S-1.1 | FAIL | evidence: TC-167-career-ops-hq-career-ops-skill.md - no cap declared on the number or size of inputs (JD text, URLs, document imports)
QD-S-1.2 | PASS | evidence: same file, "Discovery Mode" - a fixed command menu is the router's bounded own output
QD-S-1.3 | FAIL | evidence: same file, "Modes delegated to subagent" - tool-driven modes with no retry count, tool-invocation count, or execution timeout
QD-S-1.4 | PASS | evidence: same file - mode-level operation boundaries ("draft-only; never sends, submits, or clicks"; "nothing written without confirm")
QD-S-1.5 | PASS | evidence: same file - reads only explicit paths (`config/profile.yml`, `modes/*.md`, `data/*.md`)
QD-S-2.1 | PASS | evidence: same file - "every declared market" / "every declared directory" are bounded by the declared set
QD-S-2.2 | PASS | evidence: same file - no unterminated-execution wording present
QD-S-2.3 | PASS | evidence: same file - the mode list is closed; no open-ended enumeration in a functional structure
QD-S-2.4 | PASS | evidence: same file - an enumerated router over a closed mode set
QD-S-3.1 | PASS | evidence: same file, "## Mode Routing" - maps every input token to a mode; auto-pipeline detection keyword rules defined
QD-S-3.2 | FAIL | evidence: same file - no statement of when the skill should NOT trigger
QD-S-3.3 | PASS | evidence: same file, "Output Language Directive" - "If genuinely ambiguous, an interactive session asks and stops"
QD-S-3.4 | PASS | evidence: same file - `email` "draft-only; never sends, submits, or clicks"; `triage` "writes no files"
QD-S-3.6 | PASS | evidence: same file, front matter - name `career-ops` consistent with the description
QD-S-4.1 | PASS | evidence: same file, "Project Root Resolution" - "If those two sentinels cannot be found, stop and locate the career-ops checkout"
QD-S-4.2 | PASS | evidence: same file - unattended-worker fallback records a degraded result
QD-S-4.3 | FAIL | evidence: same file - no explicit post-failure prohibited behaviors declared
QD-S-5.1 | PASS | evidence: same file - write actions are gated (opt-in `latex-tex`; confirm-gated `intake`)
QD-S-5.3 | PASS | evidence: same file - declared local-first; no production-environment operation introduced
QD-S-5.4 | FAIL | evidence: same file, "Modes delegated to subagent" - delegates via `Agent(subagent_type="general-purpose", ...)` without a permitted/prohibited downstream scope

### A.4 Defect list (sorted P0 first)

P0 (2): QD-S-1.1, QD-S-1.3
P1 (3): QD-S-3.2, QD-S-4.3, QD-S-5.4
P2 (0): none

### A.5 Embedded-code QC (code-contract; QC-0 gate first)

The artifact embeds one illustrative framework-call snippet in a `python` fence (`Agent(subagent_type=..., prompt=..., description=...)`) plus several `text` blocks (Codex prompt examples, a discovery menu) . The `python` block is explicitly illustrative ("If your CLI exposes an `Agent(...)` primitive, the call looks like this") and refers to a host primitive, so per the illustrative-snippet rule it is exempt from the QC-0.1 / QC-0.3 parse-completeness requirements; the `text` blocks are not code. No undefined-name, import, resource, or hardcoded-value defect is internally evident. QC findings: 0.

## Stage B - Cross-artifact

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available. Cross-artifact relationships (QD-PS/QD-PT/QD-ST/QD-CYC) require at least two of the three artifact types from one agent; only a single Skill is present.

## Stage C - Gate-0

- G0-1 (no unfixed P0 in Stage A): informational - Stage A produced 2 P0 findings; recorded and carried forward; does not gate in this non-blocking flow.
- G0-2 (no unfixed P0 in Stage B): informational - Stage B Not Executed.
- G0-3 (responsibility boundary statements exist and are locatable): recorded as informational/indeterminate - a lone Skill carries no Prompt-level responsibility baseline to cite; the router's mode-level operation boundaries are locatable in this artifact.
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
- NL-A / NL-B (natural language): no data-exfiltration, instruction-override, permission-bypass, or constraint-removal statement. The draft-only and confirm-before-write rules are defensive constraints.
- NR-O (obfuscation): no encoded / zero-width / homoglyph payload.
- NR-S (structured configuration): no dangerous flags and no hardcoded credentials or PII. Credential handling is referenced only as a negative test ("Whether it exposes credentials or reads the whole `.env`"); no literal secret is present.

Risk Item Summary: Total 0; Explicit-P0 = 0; Explicit-P1 = 0; Explicit-P2 = 0.
Note: this is a static-document risk scan; Risk Implicit (dynamic exploitability) was NOT run. An EX finding would be a static-document risk, never a confirmed exploit.

## Stage F - Impact outlook (candidate mapping, advisory only)  [separate from the verdicts]

Mandatory statements: Risk Implicit NOT run (dynamic exploitability unverified); the runtime Quality subset NOT run (only the Stage A embedded-code QC ran, and it found no internally evident code defect); per relevance.md section 1.4 no assumption is made that controls outside the artifacts are absent.

Candidate mapping - one row per FAIL; strength is provisional (lite) and reflects association confidence only, NOT severity:

| Defect | Candidate attack surface | Potential impact | Candidate failure mode | Strength (provisional) |
| --- | --- | --- | --- | --- |
| QD-S-1.1 | AS-06 Resource Exhaustion and Runaway Execution | Availability | FM-08, FM-10 | Conditional |
| QD-S-1.3 | AS-06 Resource Exhaustion and Runaway Execution | Availability | FM-08, FM-10 | Medium |
| QD-S-3.2 | AS-01 Instruction and Context Boundary Confusion; AS-04 Permission, Identity and Delegation Expansion | D1, D2, D3 | FM-02, FM-07, FM-09 | Conditional |
| QD-S-4.3 | AS-07 Anomaly Propagation and Cascading Failures | D1, D2, D3, Availability | FM-08, FM-09 | Conditional |
| QD-S-5.4 | AS-04 Permission, Identity and Delegation Expansion; AS-05 Tool Misuse and High-Risk Side Effects; AS-07 | D1, D2, D3 | FM-05, FM-09 | Medium |

Candidate RAG-Agent quality metrics (candidate only): resource/unbounded declarations -> Completeness, Timeliness, Robustness; trigger/scope/ambiguity -> Relevance, Decomposition Capability, Boundary Recognition; failure expansion -> Completeness, Coherence, Safety Response.

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

In-place self-corrections: (1) the EX domain-prefix separator and the status-board dash are ASCII hyphens; (2) all emitted QD-S IDs are present in skill-checklist.md, and all AS-*/FM-* codes are present in relevance-map.md; (3) no CJK characters appear anywhere in this report.
