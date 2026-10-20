# SanityOps Inspect Lite - Report

Artifact: TC-129-dataherald-system-prompt.md (System Prompt)

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
- Inspect defect counts (Stage A, tier L3): P0 = 12, P1 = 1, P2 = 1.
- Gate-0 result: Not passed - G0-4 (no Tool Schema supplied; Tool field completeness unverifiable).
- Risk Explicit (Stage E): Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings (rule ID - one-line defect):
  - QD-P-2.5.2 - no security boundary constraints declared (no untrusted-content rule for DB/retrieval returns).
  - QD-P-2.3.4 - no security/privacy filtering declared.
  - QD-P-2.5.3 - no permission control boundary declared for database access.
  - QD-P-2.2.2 - no input format/encoding/size constraint declared.
  - QD-P-1.6.1 - a vague word ("does not seem related") carries a behavioral decision.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets; only the lite embedded-code QC ran in Stage A.
- Upgrade pointer: for a full inspection use sanityops-cli (see the framework try-the-tools page). No security or quality conclusion is stated here.

## Artifact inventory / classification
- `TC-129-dataherald-system-prompt.md` -> **System Prompt**. Basis: the case metadata declares Artifact Type = System Prompt; the carried text is a set of prompt constants (`AGENT_PREFIX`, `PLAN_*`, `FORMAT_INSTRUCTIONS`, `SUFFIX_*`, `FINETUNING_*`, `ERROR_PARSING_MESSAGE`) that compose the agent's instructions, not a JSON-Schema/function-calling definition and not a `name`/`description` front-matter Skill file.
- Referenced-but-not-supplied: the tools named internally (FewshotExamplesRetriever, GetAdminInstructions, DbTablesWithRelevanceScores, DbRelevantTablesSchema, DbRelevantColumnsInfo, SystemTime, DbColumnEntityChecker, SqlDbQuery, GenerateSql) and their schemas. Only the Prompt is present, so Stage B is structurally Not Executed and Gate-0 G0-4 cannot be satisfied.

## Stage A - System Prompt inspection (QD-P)

Tier determination: **L3 (Complex Agent)**. Basis: the prompt defines a natural-language-to-SQL agent that coordinates 4+ tools (few-shot retriever, admin-instructions, table/schema/column tools, entity checker, SystemTime, SqlDbQuery, GenerateSql); the operating procedure is an 8-item plan (a workflow > 5 steps); and the agent executes SQL against a production database (security-sensitive data access). L3 criteria satisfied (4+ tool invocations; complex workflow; security-sensitive). The L3 tier matrix (47 items) is applied.

### Part 1 - logic defects (QD-P-1.x)
- QD-P-1.1.1 | PASS | evidence: TC-129 - no mutually exclusive directives found (the time-function ban is consistent with the SystemTime instruction).
- QD-P-1.1.2 | PASS | evidence: TC-129 - no conflicting MUST constraints requiring arbitration found (the plan steps and tips reinforce rather than contradict each other).
- QD-P-1.1.3 | PASS | evidence: TC-129 - the SUFFIX starting example ("Thought: I should Collect examples of Question/SQL pairs ...") is consistent with the plan and FORMAT_INSTRUCTIONS.
- QD-P-1.2.1 | PASS | evidence: TC-129 - the SQL-agent role supports the stated responsibilities.
- QD-P-1.2.2 | PASS | evidence: TC-129 - the ReAct output style matches the role.
- QD-P-1.2.3 | PASS | evidence: TC-129 - no constraint prohibits a core responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-129 - no quantifier scope error found ("Only use the below tools" is a bounded scope rule).
- QD-P-1.3.2 | FAIL | evidence: TC-129, PLAN plan text - vague qualifiers used to bound tool behavior; excerpt: "obtain the schema of possibly relevant tables to identify the possibly relevant columns".
- QD-P-1.3.3 | PASS | evidence: TC-129 - behavior is bounded by the enumerated tool set and the off-topic empty-string rule; no unbounded scope introduced.
- QD-P-1.4.1 | PASS | evidence: TC-129 - the tips restate plan steps for emphasis but consistently; not a conflicting duplicate.
- QD-P-1.4.2 | PASS | evidence: TC-129 - the optional SystemTime step and the NULL-handling tip are reachable; no unreachable branch found.
- QD-P-1.4.3 | PASS | evidence: TC-129 - no Skill definitions are present in this artifact; the Skill rule has no object.
- QD-P-1.5.1 | PASS | evidence: TC-129 - stated behaviors support the correct-SQL objective.
- QD-P-1.5.2 | PASS | evidence: TC-129 - the tools named by the plan are declared ("Only use the below tools").
- QD-P-1.6.1 | FAIL | evidence: TC-129, AGENT_PREFIX - a vague qualifier carries a behavioral decision; excerpt: "If the question does not seem related to the database, return an empty string."
- QD-P-1.6.2 | FAIL | evidence: TC-129, ERROR_PARSING_MESSAGE - a rule is keyed on the model's own knowledge state; excerpt: "If you know the final answer and do not need to use any tools, directly return the final answer in this format".
- QD-P-1.6.3 | PASS | evidence: TC-129 - no interwoven soft-rule arbitration gap found.
- QD-P-1.6.4 | PASS | evidence: TC-129 - the ReAct format is stated as an output protocol, not an internal reasoning-method constraint.
- QD-P-1.6.5 | PASS | evidence: TC-129 - no self-referential/recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-129 - the reuse assumption ("labelled as correct pairs") is stated explicitly, not left implicit; no behavior-visible rule keyed on an unstated assumption beyond the input rules graded in Part 2.
- QD-P-1.6.7 | PASS | evidence: TC-129 - the rewrite-query-on-error behavior provides a conclusion-revision path; no static-knowledge gap found.

### Part 2 - completeness/security defects (QD-P-2.x)
- QD-P-2.1.1 | FAIL | evidence: TC-129, PLAN_WITH_INSTRUCTIONS - a list-numbering defect; excerpt: the step list reads "1) ... / 2) Use the GetAdminInstructions tool ... / 2) Use the DbRelevantTablesSchema tool ... / 4) ..." (step number "2)" is duplicated and "3)" is skipped).
- QD-P-2.1.2 | PASS | evidence: TC-129 - tool and section references are named clearly.
- QD-P-2.1.3 | PASS | evidence: TC-129 - section hierarchy is reasonable.
- QD-P-2.1.4 | PASS | evidence: TC-129 - no language-conciseness defect found.
- QD-P-2.2.1 | PASS | evidence: TC-129 - the input source is declared ("Given an input question").
- QD-P-2.2.2 | FAIL | evidence: TC-129 - no input question format/encoding/size limits declared (absence).
- QD-P-2.2.3 | FAIL | evidence: TC-129 - required vs optional inputs not distinguished (absence).
- QD-P-2.2.4 | FAIL | evidence: TC-129 - no handling declared for missing or empty input (absence; the empty-string rule covers only off-topic questions).
- QD-P-2.3.1 | PASS | evidence: TC-129 - output format declared (SQL between ```sql and ``` fences; ReAct Thought/Action/Action Input/Observation/Final Answer grammar).
- QD-P-2.3.2 | PASS | evidence: TC-129, FORMAT_INSTRUCTIONS - the ReAct output fields are defined; no structured schema required.
- QD-P-2.3.3 | FAIL | evidence: TC-129 - no output stability/consistency assurance declared (absence).
- QD-P-2.3.4 | FAIL | evidence: TC-129 - no sensitive-data filtering or privacy handling rules declared (absence) for database content.
- QD-P-2.4.1 | PASS | evidence: TC-129 - the plan enumerates the workflow steps.
- QD-P-2.4.2 | PASS | evidence: TC-129 - the tools used are declared (named in the plan and bounded by "Only use the below tools").
- QD-P-2.4.3 | PASS | evidence: TC-129 - the invocation format (Action / Action Input) is declared and an error-retry rule is given ("if the SQL query resulted in errors or not correct results, rewrite the SQL query and try again").
- QD-P-2.5.1 | PASS | evidence: TC-129 - the loop has a declared termination (Final Answer) and the "I don't know" fallback.
- QD-P-2.5.2 | FAIL | evidence: TC-129 - no prohibition/security boundary constraints declared (absence); DB/retrieval return content is not declared as data-not-instructions.
- QD-P-2.5.3 | FAIL | evidence: TC-129 - no permission control boundary declared for the database access (absence).
- QD-P-2.5.4 | FAIL | evidence: TC-129 - no arbitration rule for potentially conflicting constraints declared (absence).
- QD-P-2.5.5 | PASS | evidence: TC-129, tip1 - a request-count limit for the few-shot retriever is declared ("The maximum number of Question/SQL pairs you can request is {max_examples}").
- QD-P-2.6.1 | PASS | evidence: TC-129 - query errors ("rewrite the SQL query and try again") and parse errors (ERROR_PARSING_MESSAGE) are covered.
- QD-P-2.6.2 | PASS | evidence: TC-129 - a recovery path is declared (rewrite-query retry; the "I don't know" fallback on persistent parsing errors).
- QD-P-2.6.3 | PASS | evidence: TC-129 - the retry-on-error rule is bounded by the "I don't know" fallback; no explicitly unreasonable retry found.
- QD-P-2.7.1 | PASS | evidence: TC-129 - the ReAct format template and a starting example are provided.
- QD-P-2.7.2 | FAIL | evidence: TC-129 - no worked counter-examples of typical error patterns provided (absence); ERROR_PARSING_MESSAGE gives format-recovery instructions only.
- QD-P-2.7.3 | FAIL | evidence: TC-129 - no boundary-case examples provided (absence).

### Embedded-code QC (code-contract-checklist.md; QC-0 baseline first)
- QC-0.1 | PASS | evidence: TC-129, prompt-constant block - the Python module of triple-quoted constants parses as valid syntax.
- QC-0.2 | PASS | evidence: TC-129 - the fenced block carries an explicit language identifier (`python`).
- QC-0.3 | PASS | evidence: TC-129 - the snippet is a structurally complete module (no truncation).
- QC-0.4 | PASS | evidence: TC-129 - the code fence opens and closes correctly.
- QC-0.5 | PASS | evidence: TC-129 - the declared language (`python`) matches the content.
- QC-1.1, QC-1.4 | PASS | evidence: TC-129 - interpolated placeholders ({dialect}, {agent_plan}, {input}, {admin_instructions}) are runtime inputs; no undefined names or type mismatches.
- QC-1.2 | Not Executed | evidence: TC-129 - no dependency list supplied (dependency-context rule).
- QC-1.3 | Not Executed | evidence: TC-129 - no API version database supplied (dependency-context rule).
- QC-2.1, QC-2.2, QC-2.3 | PASS | evidence: TC-129 - no file handles, network connections, or high-risk operations appear in the snippet.
- QC-3.1, QC-3.2 | PASS | evidence: TC-129 - no unused/missing imports (no imports in the snippet).
- QC-3.3 | PASS | evidence: TC-129 - no hardcoded demo credentials or machine-specific literals found.
- QC-4.1, QC-4.2 | PASS | evidence: TC-129 - snippet fields are consistent with the prompt body's own declarations.

## Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)
Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available. The tool schemas referenced by the prompt were not supplied.

## Stage C - Gate-0 (admission to Permission)
- G0-1 (no unfixed P0 in Stage A): P0 findings present - recorded as an informational finding; does not gate in this non-blocking flow.
- G0-2 (no unfixed P0 in Stage B): Not evaluated - Stage B not executed.
- G0-3 (responsibility boundary statements exist and are locatable): PASS - the role statement is locatable in AGENT_PREFIX ("You are an agent designed to interact with a SQL database to find a correct SQL query for the given question.").
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
No explicitly expressed risk item matching an EX classification was found. The tool-scope constraints ("Only use the below tools. Only use the information returned by the below tools to construct your final answer.") and the time-function ban are constraint declarations, not risk expressions. This is a Risk-Explicit assessment of static text only; Risk Implicit (dynamic exploitability) was NOT run.

## Stage F - Impact outlook (candidate mapping, advisory only)
Note: advisory context, not a verdict. Based on Stage A FAILs only. Risk Implicit and the runtime Quality subsets were NOT run (Risk Explicit ran in Stage E; the lite embedded-code QC ran in Stage A). Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent. Strength is association confidence (provisional, lite), NOT severity. Candidate wording only.

| FAIL ID | Candidate attack surface (AS-*) | Candidate failure mode (FM-*) | Strength (provisional, lite) |
| --- | --- | --- | --- |
| QD-P-1.3.2 | AS-01, AS-04 | FM-02, FM-07, FM-09 | Medium |
| QD-P-1.6.1 | AS-01, AS-04 | FM-02, FM-07, FM-09 | Medium |
| QD-P-1.6.2 | AS-01, AS-07 | FM-01, FM-07, FM-09 | Medium |
| QD-P-2.1.1 | AS-09 | FM-06 | Conditional |
| QD-P-2.2.2 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.2.3 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.2.4 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.3.3 | AS-03, AS-09 | FM-06 | Medium |
| QD-P-2.3.4 | AS-03 | FM-06 | Medium |
| QD-P-2.5.2 | AS-01, AS-03, AS-04 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.5.3 | AS-04, AS-05 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.5.4 | AS-01, AS-07 | FM-08, FM-09, FM-10 | Conditional |
| QD-P-2.7.2 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |
| QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |

Candidate RAG-Agent quality metrics (candidate only, NOT a quality result): Correctness, Robustness, Boundary Recognition, Safety Response, Traceability, Format Compliance. The Quality subset was NOT executed.

## Status Board
Stage A (Single-artifact):  Executed - full L3 tier checklist applied to the lone System Prompt
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available
Stage C (Gate-0):           Not passed - G0-4 (no Tool Schema supplied)
Stage D (Permission QD-PM): Not Executed - incomplete artifact set
Stage E (Risk Explicit EX): Executed - no finding
Stage F (Impact outlook):   Executed - candidate mapping for Stage A FAILs
Stage G (Self-verification): Executed - see statement below

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. In-place self-corrections: none.
