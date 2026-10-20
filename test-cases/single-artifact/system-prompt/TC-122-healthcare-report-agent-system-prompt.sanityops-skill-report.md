# SanityOps Inspect Lite - Report

Artifact: TC-122-healthcare-report-agent-system-prompt.md (System Prompt)

## Provenance Header
- Host model: unspecified (host model self-declaration not available in this environment)
- Skill package: sanityops-inspect-lite v1.0.0
- Specification baseline: SanityOps Framework v1.0 (September 2026)
- Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
- Inspection date: 2026-10-15
- Artifact version: not supplied by the user (using the case's Collection Date as the working label) - working label 2026-10-13

## Executive Summary
- Executed stages: Stage A (single-artifact System Prompt), Stage C (Gate-0), Stage E (Risk Explicit), Stage F (impact outlook), Stage G (self-verification).
- Not executed: Stage B (cross; no Prompt+Skill+Tool set from the same agent), Stage D (Permission; incomplete artifact set).
- Inspect defect counts (Stage A, tier L2): P0 = 5, P1 = 5, P2 = 0.
- Gate-0 result: Not passed - G0-4 (no Tool Schema supplied; Tool field completeness unverifiable).
- Risk Explicit (Stage E): Explicit·P0 = 0, Explicit·P1 = 0, Explicit·P2 = 0.
- Top findings (rule ID - one-line defect):
  - QD-P-2.4.3 - no tool invocation parameter specification or failure handling declared.
  - QD-P-2.3.1 - no output format declared for the final report.
  - QD-P-2.2.2 - no input format/encoding/size limits declared.
  - QD-P-2.2.3 - required vs optional inputs not distinguished.
  - QD-P-2.2.4 - no handling declared for missing or malformed user input.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets; only the lite embedded-code QC ran in Stage A.
- Upgrade pointer: for a full inspection use sanityops-cli (see the framework try-the-tools page). No security or quality conclusion is stated here.

## Artifact inventory / classification
- `TC-122-healthcare-report-agent-system-prompt.md` -> **System Prompt**. Basis: the case metadata declares Artifact Type = System Prompt; the carried content is a Python f-string prompt returned by `build_system_prompt(schema_info)` (prose/markdown instructions), not a JSON-Schema/function-calling definition and not a `name`/`description` front-matter Skill file.
- Referenced-but-not-supplied: the tool schemas for `stats_tool`, `tavily_search`, and `plot_tool`. Only the Prompt is present, so Stage B is structurally Not Executed and Gate-0 G0-4 cannot be satisfied.

## Stage A - System Prompt inspection (QD-P)

Tier determination: **L2 (Multi-turn Interactive)**. Basis: the agent declares 3 tools (`stats_tool`, `tavily_search`, `plot_tool` = 1-3 tool invocations) and a recommended 4-step execution plan (explore data, identify anomalies, targeted search, synthesize = a simple workflow within 5 steps) with limited state over a question/answer dialogue. L2 criteria satisfied. L3 criteria are not met: no 4+ tool invocations and no workflow greater than 5 steps; the health-data/PII handling raises sensitivity but is a single L3 criterion, so the "any 2 or more" L3 threshold is not reached. The L2 tier matrix (40 items) is applied.

### Part 1 - logic defects (QD-P-1.x)
- QD-P-1.1.1 | PASS | evidence: TC-122 - no mutually exclusive directives found.
- QD-P-1.1.2 | PASS | evidence: TC-122 - no conflicting MUST constraints requiring arbitration found.
- QD-P-1.1.3 | PASS | evidence: TC-122 - the good/bad search examples are consistent with the stated search rule.
- QD-P-1.2.1 | PASS | evidence: TC-122 - the Senior Data Analyst role supports the query-and-report responsibilities.
- QD-P-1.2.2 | PASS | evidence: TC-122 - the analyst/reporting style matches the role.
- QD-P-1.2.3 | PASS | evidence: TC-122 - no constraint prohibits a core responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-122 - no quantifier scope error found.
- QD-P-1.3.2 | PASS | evidence: TC-122 - no vague qualifier carries a critical behavioral decision; the interpretation caveats are stated as concrete rules.
- QD-P-1.3.3 | PASS | evidence: TC-122, SCOPE & PRIVACY - behavioral boundaries are declared; excerpt: "Refuse general knowledge questions not related to health/SRAG."
- QD-P-1.4.1 | PASS | evidence: TC-122 - no duplicate-constraint defect found.
- QD-P-1.4.2 | PASS | evidence: TC-122 - no never-triggered condition found.
- QD-P-1.4.3 | PASS | evidence: TC-122 - no Skill definitions are present in this artifact; the Skill rule has no object.
- QD-P-1.5.1 | PASS | evidence: TC-122 - the stated behaviors support the KPI-reporting objective.
- QD-P-1.5.2 | PASS | evidence: TC-122 - every step of the strategic plan uses a declared tool (stats_tool, tavily_search, plot_tool).
- QD-P-1.6.1 | PASS | evidence: TC-122 - no vague word carries a security/permission decision.
- QD-P-1.6.2 | PASS | evidence: TC-122 - no rule keyed on the model's internal state (confidence/intent/motivation) found.
- QD-P-1.6.3 | PASS | evidence: TC-122 - no interwoven soft-rule arbitration gap found.
- QD-P-1.6.4 | PASS | evidence: TC-122 - no reasoning-method constraint found.
- QD-P-1.6.5 | PASS | evidence: TC-122 - no self-referential/recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-122 - the key assumptions are stated (static dataset; sample values in the schema), not left implicit.
- QD-P-1.6.7 | PASS | evidence: TC-122 - the data-lag interpretation rule acts as a conclusion-revision mechanism for provisional recent data.

### Part 2 - completeness/security defects (QD-P-2.x)
- QD-P-2.2.1 | PASS | evidence: TC-122 - input sources are declared (the user's question, the `srag_analytics` database, and external news via tavily_search).
- QD-P-2.2.2 | FAIL | evidence: TC-122 - no input format/encoding/size limits declared for the user's question (absence).
- QD-P-2.2.3 | FAIL | evidence: TC-122 - required vs optional inputs are not distinguished (absence).
- QD-P-2.2.4 | FAIL | evidence: TC-122 - no handling declared for missing, empty, or malformed user input (absence).
- QD-P-2.3.1 | FAIL | evidence: TC-122 - no output format declared (absence); the final report's structure, fields and encoding are unspecified ("Combine the quantitative data and the qualitative news into the final report").
- QD-P-2.3.2 | PASS | evidence: TC-122 - a narrative report is produced; no structured schema is required.
- QD-P-2.3.3 | FAIL | evidence: TC-122 - no output stability/consistency assurance declared (absence).
- QD-P-2.3.4 | PASS | evidence: TC-122, SCOPE & PRIVACY - a privacy/data-handling rule is declared; excerpt: "Refuse requests for PII (names/CPFs)."
- QD-P-2.4.1 | PASS | evidence: TC-122, STRATEGIC PLAN - the recommended execution order is enumerated as a 4-step workflow.
- QD-P-2.4.2 | PASS | evidence: TC-122 - the tools used are declared (stats_tool, tavily_search, plot_tool).
- QD-P-2.4.3 | FAIL | evidence: TC-122 - tool invocation parameter specifications and failure handling are not declared (absence); the prompt names the tools but gives no parameter contract for stats_tool, tavily_search, or plot_tool.
- QD-P-2.5.1 | PASS | evidence: TC-122 - no loop or recursion is defined, so no termination-constraint gap exists.
- QD-P-2.5.2 | PASS | evidence: TC-122, SCOPE & PRIVACY - a data-access/prohibition boundary is declared; excerpt: "Refuse requests for PII (names/CPFs)."
- QD-P-2.5.3 | FAIL | evidence: TC-122 - no permission control boundary declared beyond the scope/PII refusals (absence).
- QD-P-2.5.4 | FAIL | evidence: TC-122 - no arbitration rule for potentially conflicting constraints declared (absence).
- QD-P-2.5.5 | FAIL | evidence: TC-122 - no resource invocation frequency limits declared (absence), despite external search and database queries.
- QD-P-2.7.1 | PASS | evidence: TC-122 - positive examples are provided ("Good search (e.g.): 'Low influenza vaccination coverage Brazil 2026'").
- QD-P-2.7.2 | PASS | evidence: TC-122 - a counter-example is provided ("Bad search (e.g.): 'SRAG news Brazil'").
- QD-P-2.7.3 | FAIL | evidence: TC-122 - no boundary-case examples provided (absence).

### Embedded-code QC (code-contract-checklist.md; QC-0 baseline first)
- QC-0.1 | PASS | evidence: TC-122, `build_system_prompt` block - the Python parses as valid syntax.
- QC-0.2 | PASS | evidence: TC-122 - the fenced block carries an explicit language identifier (`python`).
- QC-0.3 | PASS | evidence: TC-122 - the snippet is a structurally complete function with its import.
- QC-0.4 | PASS | evidence: TC-122 - the code fence opens and closes correctly.
- QC-0.5 | PASS | evidence: TC-122 - the declared language (`python`) matches the content.
- QC-1.1, QC-1.4 | PASS | evidence: TC-122 - `datetime` is imported and used correctly; no undefined names or type mismatches.
- QC-1.2 | Not Executed | evidence: TC-122 - no dependency list supplied (dependency-context rule).
- QC-1.3 | Not Executed | evidence: TC-122 - no API version database supplied (dependency-context rule).
- QC-2.1, QC-2.2, QC-2.3 | PASS | evidence: TC-122 - no file handles, network connections, or high-risk operations appear in the prompt snippet.
- QC-3.1, QC-3.2 | PASS | evidence: TC-122 - no unused/missing imports (datetime is used).
- QC-3.3 | PASS | evidence: TC-122 - no hardcoded demo credentials or machine-specific literals found.
- QC-4.1, QC-4.2 | PASS | evidence: TC-122 - snippet content is consistent with the prompt body's own declarations.

## Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)
Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available. The tool schemas referenced by the prompt were not supplied.

## Stage C - Gate-0 (admission to Permission)
- G0-1 (no unfixed P0 in Stage A): P0 findings present - recorded as an informational finding; does not gate in this non-blocking flow.
- G0-2 (no unfixed P0 in Stage B): Not evaluated - Stage B not executed.
- G0-3 (responsibility boundary statements exist and are locatable): PASS - the role statement is locatable at the top of the returned prompt; excerpt: "You are a Senior Data Analyst for a Health Organization."
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
No explicitly expressed risk item matching an EX classification was found. The SQL-safety rules, the mandatory PII refusal, and the interpretation caveats are constraint statements, not risk expressions. This is a Risk-Explicit assessment of static text only; Risk Implicit (dynamic exploitability) was NOT run.

## Stage F - Impact outlook (candidate mapping, advisory only)
Note: advisory context, not a verdict. Based on Stage A FAILs only. Risk Implicit and the runtime Quality subsets were NOT run (Risk Explicit ran in Stage E; the lite embedded-code QC ran in Stage A). Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent. Strength is association confidence (provisional, lite), NOT severity. Candidate wording only.

| FAIL ID | Candidate attack surface (AS-*) | Candidate failure mode (FM-*) | Strength (provisional, lite) |
| --- | --- | --- | --- |
| QD-P-2.2.2 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.2.3 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.2.4 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.3.1 | AS-03, AS-09 | FM-06 | Medium |
| QD-P-2.3.3 | AS-03, AS-09 | FM-06 | Medium |
| QD-P-2.4.3 | AS-05, AS-07, AS-09 | FM-03, FM-04, FM-05 | Medium |
| QD-P-2.5.3 | AS-04, AS-05 | FM-08, FM-09, FM-10 | Conditional |
| QD-P-2.5.4 | AS-01, AS-07 | FM-08, FM-09, FM-10 | Conditional |
| QD-P-2.5.5 | AS-06 | FM-08, FM-10 | Conditional |
| QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |

Candidate RAG-Agent quality metrics (candidate only, NOT a quality result): Correctness, Completeness, Traceability, Boundary Recognition, Safety Response. The Quality subset was NOT executed.

## Status Board
Stage A (Single-artifact):  Executed - full L2 tier checklist applied to the lone System Prompt
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available
Stage C (Gate-0):           Not passed - G0-4 (no Tool Schema supplied)
Stage D (Permission QD-PM): Not Executed - incomplete artifact set
Stage E (Risk Explicit EX): Executed - no finding
Stage F (Impact outlook):   Executed - candidate mapping for Stage A FAILs
Stage G (Self-verification): Executed - see statement below

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. In-place self-corrections: none.
