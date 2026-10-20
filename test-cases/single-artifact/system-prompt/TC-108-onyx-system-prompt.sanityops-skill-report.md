# SanityOps Inspect Lite - Report

Artifact: TC-108-onyx-system-prompt.md (System Prompt)

## Provenance Header
- Host model: unspecified (host model self-declaration not available in this environment)
- Skill package: sanityops-inspect-lite v1.0.0
- Specification baseline: SanityOps Framework v1.0 (September 2026)
- Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
- Inspection date: 2026-10-14
- Artifact version: not supplied by the user (using the case's Collection Date as the working label) - working label 2026-10-13

## Executive Summary
- Executed stages: Stage A (single-artifact System Prompt), Stage C (Gate-0), Stage E (Risk Explicit), Stage F (impact outlook), Stage G (self-verification).
- Not executed: Stage B (cross; no Prompt+Skill+Tool set from the same agent), Stage D (Permission; incomplete artifact set).
- Inspect defect counts (Stage A, tier L2): P0 = 8, P1 = 10, P2 = 0.
- Gate-0 result: Not passed - G0-4 (no Tool Schema supplied; Tool field completeness unverifiable).
- Risk Explicit (Stage E): Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings (rule ID - one-line defect):
  - QD-P-1.3.3 - authorization/prohibition boundary scope not declared.
  - QD-P-2.5.2 - no security boundary constraints declared.
  - QD-P-2.3.4 - no security/privacy filtering declared.
  - QD-P-2.4.2 - tools/resources only referenced generically ("available tools (if any)").
  - QD-P-1.6.2 - behavior keyed on the model's own ambiguity judgment.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets; only the lite embedded-code QC ran in Stage A.
- Upgrade pointer: for a full inspection use sanityops-cli (see the framework try-the-tools page). No security or quality conclusion is stated here.

## Stage A - System Prompt inspection (QD-P)

Tier determination: L2 (Multi-turn Interactive). Basis: the prompt is a multi-turn conversational assistant (references the user's query and tool use); tools are referenced ("available tools (if any)") but no 4+ tool set or >5-step workflow is declared. Multi-turn dialogue + tool use = two L2 criteria satisfied; L3 criteria are not met.

### Part 1 - logic defects (QD-P-1.x)
- QD-P-1.1.1 | PASS | evidence: TC-108, DEFAULT_SYSTEM_PROMPT - no mutually exclusive directives found.
- QD-P-1.1.2 | PASS | evidence: TC-108 - no conflicting MUST constraints requiring arbitration found.
- QD-P-1.1.3 | PASS | evidence: TC-108, REQUIRE_CITATION_GUIDANCE / Response Style - no example-rule contradiction found.
- QD-P-1.2.1 | PASS | evidence: TC-108, DEFAULT_SYSTEM_PROMPT - role supports the stated goal.
- QD-P-1.2.2 | PASS | evidence: TC-108, Response Style - output style matches the assistant role.
- QD-P-1.2.3 | PASS | evidence: TC-108 - no constraint prohibits a core responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-108 - no quantifier scope error found.
- QD-P-1.3.2 | PASS | evidence: TC-108 - no constraining vague qualifier on a critical behavior found.
- QD-P-1.3.3 | FAIL | evidence: TC-108, DEFAULT_SYSTEM_PROMPT - authorization scope, prohibition scope, and handoff conditions are not declared; excerpt: "You are an expert assistant who is truthful, nuanced, insightful, and efficient".
- QD-P-1.4.1 | PASS | evidence: TC-108 - no duplicated constraint found.
- QD-P-1.4.2 | PASS | evidence: TC-108 - no unreachable branch found.
- QD-P-1.4.3 | PASS | evidence: TC-108 - no Skill definitions present; not applicable beyond baseline.
- QD-P-1.5.1 | PASS | evidence: TC-108 - stated behaviors support the goal.
- QD-P-1.5.2 | PASS | evidence: TC-108 - workflow resources (tools/context) referenced consistently with the task.
- QD-P-1.6.1 | PASS | evidence: TC-108 - no vague word carries a security/permission decision.
- QD-P-1.6.2 | FAIL | evidence: TC-108, DEFAULT_SYSTEM_PROMPT - a rule is keyed on the model's own judgment; excerpt: "Whenever there is any ambiguity around the user's query (or more information would be helpful), you use available tools (if any) to get more context".
- QD-P-1.6.3 | PASS | evidence: TC-108 - no interwoven soft-rule arbitration gap found.
- QD-P-1.6.4 | FAIL | evidence: TC-108, DEFAULT_SYSTEM_PROMPT - a reasoning-method constraint is imposed; excerpt: "think step-by-step through complex problems".
- QD-P-1.6.5 | PASS | evidence: TC-108 - no self-referential/recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-108 - no behavior-visible rule keyed on an unstated assumption beyond the input rules graded in Part 2.
- QD-P-1.6.7 | PASS | evidence: TC-108 - no static-knowledge conclusion-revision gap found.

### Part 2 - completeness/security defects (QD-P-2.x)
- QD-P-2.2.1 | PASS | evidence: TC-108, DEFAULT_SYSTEM_PROMPT - input sources declared (user query; search/tool context).
- QD-P-2.2.2 | FAIL | evidence: TC-108 - no input data format/encoding/size limits declared (absence).
- QD-P-2.2.3 | FAIL | evidence: TC-108 - required vs optional inputs not distinguished (absence).
- QD-P-2.2.4 | FAIL | evidence: TC-108 - handling when a required input is missing not defined at the prompt level (absence). The completeness reminder addresses missing retrieved content, not missing required input.
- QD-P-2.3.1 | PASS | evidence: TC-108, Response Style - output format declared (Markdown/LaTeX, tables, rules).
- QD-P-2.3.2 | PASS | evidence: TC-108 - free-text output with declared formatting rules; no structured output schema required.
- QD-P-2.3.3 | FAIL | evidence: TC-108 - no output stability/consistency assurance declared (absence).
- QD-P-2.3.4 | FAIL | evidence: TC-108 - no sensitive-data filtering or privacy handling rules declared (absence).
- QD-P-2.4.1 | PASS | evidence: TC-108 - single-turn retrieval interaction; no multi-step workflow requiring step completeness.
- QD-P-2.4.2 | FAIL | evidence: TC-108, DEFAULT_SYSTEM_PROMPT - tools/resources referenced only generically; excerpt: "you use available tools (if any) to get more context".
- QD-P-2.4.3 | FAIL | evidence: TC-108 - no tool invocation parameter/sequence/failure specification declared (absence).
- QD-P-2.5.1 | FAIL | evidence: TC-108 - no termination constraints declared (absence).
- QD-P-2.5.2 | FAIL | evidence: TC-108 - no prohibition/security boundary constraints declared (absence).
- QD-P-2.5.3 | FAIL | evidence: TC-108 - no permission control boundaries declared (absence).
- QD-P-2.5.4 | FAIL | evidence: TC-108 - arbitration rules for potentially conflicting constraints not defined (absence).
- QD-P-2.5.5 | FAIL | evidence: TC-108 - resource invocation frequency limits not declared (absence).
- QD-P-2.7.1 | FAIL | evidence: TC-108 - no behavior-level positive examples provided (absence).
- QD-P-2.7.2 | FAIL | evidence: TC-108 - no counter-examples provided (absence).
- QD-P-2.7.3 | FAIL | evidence: TC-108 - no boundary-case examples provided (absence).

### Embedded-code QC (code-contract-checklist.md; QC-0 baseline first)
- QC-0.1 | PASS | evidence: TC-108, DEFAULT_SYSTEM_PROMPT block - the Python f-string snippet parses as valid syntax.
- QC-0.2 | PASS | evidence: TC-108 - fenced block carries explicit language identifier (`python`).
- QC-0.3 | PASS | evidence: TC-108 - snippet is a partial module excerpt but structurally parseable.
- QC-1.1..1.4, QC-2.1..2.3, QC-3.1..3.3 | PASS | evidence: TC-108 - the embedded Python is a partial module excerpt (imports are project-internal; file content truncated upstream); no file handles, network connections, missing imports, or hardcoded credentials detected. Unused-import determination is inconclusive on a partial excerpt.

## Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)
Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.

## Stage C - Gate-0 (admission to Permission)
- G0-1 (no unfixed P0 in Stage A): P0 findings present - recorded as an informational finding; does not gate in this non-blocking flow.
- G0-2 (no unfixed P0 in Stage B): Not evaluated - Stage B not executed.
- G0-3 (responsibility boundary statements exist and are locatable): PASS - the persona/goal statement is locatable in DEFAULT_SYSTEM_PROMPT.
- G0-4 (each Tool Schema name/description/parameter descriptions complete): FAIL - no Tool Schema is supplied; field-by-field completeness cannot be verified.
- Gate-0 result: Not passed - G0-4.

## Stage D - Permission proportionality (QD-PM, Quick Mode)
Not Executed - incomplete artifact set (Gate-0 G0-4 unsatisfied; no Tool Schema supplied).

Subset: Inspect Permission Governance Specification (QD-PM)
Execution Status: Not Executed
Unsatisfied Conditions: G0-4
Blocking Reasons:
  G0-4 - no Tool Schema supplied; operation semantics undeterminable; permission items cannot be categorized.
Remediation Actions: Fix above upstream items, then re-run Gate-0

(Wording note: the Permission stage was "Not Executed" because Gate-0 was not satisfied; it is not reported as FAIL and no ERROR/BLOCKED status is asserted.)

## Stage E - Risk Explicit (EX) - physically separated from Inspect verdicts
Scan scope: System Prompt static text (NL-A / NL-B / NR-O / NR-S).
Findings: none.
No explicitly expressed risk item matching an EX classification was found in the artifact text. This is a Risk-Explicit assessment of static text only; Risk Implicit (dynamic exploitability) was NOT run.

## Stage F - Impact outlook (candidate mapping, advisory only)
Note: advisory context, not a verdict. Based on Stage A FAILs only. Risk Implicit and the runtime Quality subsets were NOT run (Risk Explicit ran in Stage E; the lite embedded-code QC ran in Stage A). Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent. Strength is association confidence (provisional, lite), NOT severity. Candidate wording only.

| FAIL ID | Candidate attack surface (AS-*) | Candidate failure mode (FM-*) | Strength (provisional, lite) |
| --- | --- | --- | --- |
| QD-P-1.3.3 | AS-01, AS-04 | FM-02, FM-07, FM-09 | Medium |
| QD-P-1.6.2 | AS-01, AS-07 | FM-01, FM-07, FM-09 | Medium |
| QD-P-1.6.4 | AS-01, AS-06, AS-07 | FM-01, FM-07, FM-09 | Conditional |
| QD-P-2.2.2 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.2.3 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.2.4 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.3.3 | AS-03, AS-09 | FM-06 | Conditional |
| QD-P-2.3.4 | AS-03 | FM-06 | Medium |
| QD-P-2.4.2 | AS-05, AS-07, AS-09 | FM-03, FM-04, FM-05 | Medium |
| QD-P-2.4.3 | AS-05, AS-07, AS-09 | FM-03, FM-04, FM-05 | Medium |
| QD-P-2.5.1 | AS-06 | FM-08, FM-09, FM-10 | Conditional |
| QD-P-2.5.2 | AS-01, AS-03, AS-04 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.5.3 | AS-04, AS-05 | FM-08, FM-09, FM-10 | Conditional |
| QD-P-2.5.4 | AS-01, AS-07 | FM-08, FM-09, FM-10 | Conditional |
| QD-P-2.5.5 | AS-06 | FM-08, FM-09, FM-10 | Conditional |
| QD-P-2.7.1 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |
| QD-P-2.7.2 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |
| QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |

Candidate RAG-Agent quality metrics (candidate only, NOT a quality result): Correctness, Robustness, Boundary Recognition, Safety Response. The Quality subset was NOT executed.

## Status Board
Stage A (Single-artifact):  Executed - full L2 tier checklist applied to the lone System Prompt
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available
Stage C (Gate-0):           Not passed - G0-4 (no Tool Schema supplied)
Stage D (Permission QD-PM): Not Executed - incomplete artifact set
Stage E (Risk Explicit EX): Executed - no finding
Stage F (Impact outlook):   Executed - candidate mapping for Stage A FAILs
Stage G (Self-verification): Executed - see statement below

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. In-place self-corrections: none.
