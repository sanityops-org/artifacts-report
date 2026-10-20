# SanityOps Inspect Lite - Report

Artifact: TC-128-vanna-system-prompt.md (System Prompt)

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
- Inspect defect counts (Stage A, tier L3): P0 = 15, P1 = 1, P2 = 0.
- Gate-0 result: Not passed - G0-4 (no Tool Schema supplied; Tool field completeness unverifiable).
- Risk Explicit (Stage E): Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings (rule ID - one-line defect):
  - QD-P-2.5.2 - no security boundary constraints declared (no untrusted-content rule for tool/DB returns).
  - QD-P-2.3.4 - no security/privacy filtering declared.
  - QD-P-2.5.3 - no permission control boundary declared for database access.
  - QD-P-2.4.3 - tool invocation failure handling is not declared.
  - QD-P-2.2.2 - no input format/encoding/size constraint declared.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets; only the lite embedded-code QC ran in Stage A.
- Upgrade pointer: for a full inspection use sanityops-cli (see the framework try-the-tools page). No security or quality conclusion is stated here.

## Artifact inventory / classification
- `TC-128-vanna-system-prompt.md` -> **System Prompt**. Basis: the case metadata declares Artifact Type = System Prompt; the carried text is the prompt string assembled by `DefaultSystemPromptBuilder.build_system_prompt()` (persona, response guidelines, memory-workflow instructions), not a `name`/`description` front-matter Skill file. Basis for treating it as a Prompt rather than a Tool Schema: the payload is prose/markdown instructions, not a JSON-Schema/function-calling definition.
- Referenced-but-not-supplied: the tools named internally (run_sql, visualize_data, calculator, search_saved_correct_tool_uses, save_question_tool_args, save_text_memory) and their schemas. Only the Prompt is present, so Stage B is structurally Not Executed and Gate-0 G0-4 cannot be satisfied.

## Stage A - System Prompt inspection (QD-P)

Tier determination: **L3 (Complex Agent)**. Basis: the prompt is a data-analysis / text-to-SQL analyst that coordinates 4+ tools (run_sql, visualize_data, calculator, plus the search/save/text memory tools), enforces a multi-step memory workflow (search-first, execute, save-after-success) that exceeds 5 steps, and operates on database content (security-sensitive data access). L3 criteria satisfied (4+ tool invocations; complex workflow; security-sensitive); multi-turn dialogue and tool use also hold, so L2 is covered by upward compatibility. The L3 tier matrix (47 items) is applied.

### Part 1 - logic defects (QD-P-1.x)
- QD-P-1.1.1 | PASS | evidence: TC-128 - no mutually exclusive directives found.
- QD-P-1.1.2 | PASS | evidence: TC-128 - the mandatory search-first rule and its enumerated exceptions ("The only exceptions to searching first are: ...") do not produce an unresolved conflict.
- QD-P-1.1.3 | PASS | evidence: TC-128 - the inline "Example workflow" (search first, then execute, then save) is consistent with the stated rules.
- QD-P-1.2.1 | PASS | evidence: TC-128 - the "Vanna, an AI data analyst assistant" role supports the stated responsibilities.
- QD-P-1.2.2 | PASS | evidence: TC-128 - the summary/interpreting output style matches the analyst role.
- QD-P-1.2.3 | PASS | evidence: TC-128 - no constraint prohibits a core responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-128 - no quantifier scope error found ("BEFORE executing any tool", "AFTER successfully executing a tool" are bounded step rules).
- QD-P-1.3.2 | FAIL | evidence: TC-128, Example workflow - vague qualifier used to select behavior; excerpt: "Then: Execute the appropriate tool(s) based on search results and the question".
- QD-P-1.3.3 | PASS | evidence: TC-128 - behavior is bounded by the declared tool set and the memory workflow; no unbounded authorization scope introduced.
- QD-P-1.4.1 | PASS | evidence: TC-128 - the search-first rule is restated for emphasis ("Do NOT skip the search step") but consistently, not as a conflicting duplicate.
- QD-P-1.4.2 | PASS | evidence: TC-128 - the declared exceptions to the search-first rule are reachable; no unreachable branch found.
- QD-P-1.4.3 | PASS | evidence: TC-128 - no Skill definitions are present in this artifact; the Skill rule has no object.
- QD-P-1.5.1 | PASS | evidence: TC-128 - stated behaviors support the data-analysis objective.
- QD-P-1.5.2 | PASS | evidence: TC-128 - the workflow's tools are declared ("You have access to the following tools: {tool_names}").
- QD-P-1.6.1 | PASS | evidence: TC-128 - no vague word carries a security/permission decision.
- QD-P-1.6.2 | FAIL | evidence: TC-128, memory workflow - a rule is keyed on the model's own judgment; excerpt: "Do NOT skip the search step, even if you think you know how to answer."
- QD-P-1.6.3 | PASS | evidence: TC-128 - no interwoven soft-rule arbitration gap found.
- QD-P-1.6.4 | PASS | evidence: TC-128 - no internal reasoning-method constraint found.
- QD-P-1.6.5 | PASS | evidence: TC-128 - no self-referential/recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-128 - the "if any" wording handles the no-prior-patterns case; no behavior-visible rule keyed on an unstated assumption beyond the input rules graded in Part 2.
- QD-P-1.6.7 | PASS | evidence: TC-128 - no static-knowledge conclusion-revision gap found.

### Part 2 - completeness/security defects (QD-P-2.x)
- QD-P-2.1.1 | PASS | evidence: TC-128 - the sectioned prompt structure is readable; no format-compliance defect found.
- QD-P-2.1.2 | PASS | evidence: TC-128 - tool and section references are named clearly.
- QD-P-2.1.3 | PASS | evidence: TC-128 - section hierarchy is reasonable.
- QD-P-2.1.4 | PASS | evidence: TC-128 - no language-conciseness defect found.
- QD-P-2.2.1 | PASS | evidence: TC-128 - the input source is declared (the user's question; e.g. "call search_saved_correct_tool_uses with the user's question").
- QD-P-2.2.2 | FAIL | evidence: TC-128 - no input question format/encoding/size limits declared (absence).
- QD-P-2.2.3 | FAIL | evidence: TC-128 - required vs optional inputs not distinguished (absence).
- QD-P-2.2.4 | FAIL | evidence: TC-128 - no handling declared for missing or malformed input (absence).
- QD-P-2.3.1 | PASS | evidence: TC-128, Response Guidelines - output structure declared (summary/observations as the final step; raw result excluded from the response).
- QD-P-2.3.2 | PASS | evidence: TC-128 - free-text output with declared structure; no structured schema required.
- QD-P-2.3.3 | FAIL | evidence: TC-128 - no output stability/consistency assurance declared (absence).
- QD-P-2.3.4 | FAIL | evidence: TC-128 - no sensitive-data filtering or privacy handling rules declared (absence) for database content.
- QD-P-2.4.1 | PASS | evidence: TC-128 - the memory workflow steps (search first, execute, save after success) are enumerated.
- QD-P-2.4.2 | PASS | evidence: TC-128 - the tools used are declared (tool-name list plus the named memory tools).
- QD-P-2.4.3 | FAIL | evidence: TC-128 - invocation examples are given for the memory tools, but tool-invocation failure handling is not declared (partial absence).
- QD-P-2.5.1 | PASS | evidence: TC-128 - no loop/recursion is defined, so no termination-constraint gap exists.
- QD-P-2.5.2 | FAIL | evidence: TC-128 - no prohibition/security boundary constraints declared (absence); tool/DB return content is not declared as data-not-instructions.
- QD-P-2.5.3 | FAIL | evidence: TC-128 - no permission control boundary declared for the database access (absence).
- QD-P-2.5.4 | FAIL | evidence: TC-128 - no arbitration rule for potentially conflicting constraints declared (absence).
- QD-P-2.5.5 | FAIL | evidence: TC-128 - no resource invocation frequency limits declared (absence).
- QD-P-2.6.1 | FAIL | evidence: TC-128 - runtime exceptions from tool invocation are not covered (absence).
- QD-P-2.6.2 | FAIL | evidence: TC-128 - no degradation/recovery strategy declared (absence).
- QD-P-2.6.3 | PASS | evidence: TC-128 - no retry mechanism is declared, so no unreasonable-retry defect exists.
- QD-P-2.7.1 | PASS | evidence: TC-128 - an example workflow and text-memory examples are provided.
- QD-P-2.7.2 | FAIL | evidence: TC-128 - no worked counter-examples of typical error patterns provided (absence); only prohibition guidance ("DO NOT save: ...").
- QD-P-2.7.3 | FAIL | evidence: TC-128 - no boundary-case examples provided (absence).

### Embedded-code QC (code-contract-checklist.md; QC-0 baseline first)
- QC-0.1 | PASS | evidence: TC-128, `build_system_prompt()` block - the Python template builder parses as valid syntax.
- QC-0.2 | PASS | evidence: TC-128 - the fenced block carries an explicit language identifier (`python`).
- QC-0.3 | PASS | evidence: TC-128 - the snippet is a structurally complete module (imports present, no truncation).
- QC-0.4 | PASS | evidence: TC-128 - the code fence opens and closes correctly.
- QC-0.5 | PASS | evidence: TC-128 - the declared language (`python`) matches the content.
- QC-1.1, QC-1.4 | PASS | evidence: TC-128 - interpolated values (today_date, tool_names) are runtime inputs; no undefined names or type mismatches.
- QC-1.2 | Not Executed | evidence: TC-128 - no dependency list supplied (dependency-context rule).
- QC-1.3 | Not Executed | evidence: TC-128 - no API version database supplied (dependency-context rule).
- QC-2.1, QC-2.2, QC-2.3 | PASS | evidence: TC-128 - no file handles, network connections, or high-risk operations appear in the snippet.
- QC-3.1, QC-3.2 | PASS | evidence: TC-128 - all imports shown (datetime, SystemPromptBuilder, TYPE_CHECKING/List/Optional) are referenced.
- QC-3.3 | PASS | evidence: TC-128 - no hardcoded demo credentials or machine-specific literals found.
- QC-4.1, QC-4.2 | PASS | evidence: TC-128 - snippet fields are consistent with the prompt body's own declarations.

## Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)
Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available. The tool schemas referenced by the prompt were not supplied.

## Stage C - Gate-0 (admission to Permission)
- G0-1 (no unfixed P0 in Stage A): P0 findings present - recorded as an informational finding; does not gate in this non-blocking flow.
- G0-2 (no unfixed P0 in Stage B): Not evaluated - Stage B not executed.
- G0-3 (responsibility boundary statements exist and are locatable): PASS - the role statement is locatable in the base prompt ("You are Vanna, an AI data analyst assistant ...").
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
No explicitly expressed risk item matching an EX classification was found. The memory-workflow mandates ("MUST first call search_saved_correct_tool_uses", "MUST call save_question_tool_args") and the "DO NOT save" guidance are workflow constraint declarations, not risk expressions. This is a Risk-Explicit assessment of static text only; Risk Implicit (dynamic exploitability) was NOT run.

## Stage F - Impact outlook (candidate mapping, advisory only)
Note: advisory context, not a verdict. Based on Stage A FAILs only. Risk Implicit and the runtime Quality subsets were NOT run (Risk Explicit ran in Stage E; the lite embedded-code QC ran in Stage A). Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent. Strength is association confidence (provisional, lite), NOT severity. Candidate wording only.

| FAIL ID | Candidate attack surface (AS-*) | Candidate failure mode (FM-*) | Strength (provisional, lite) |
| --- | --- | --- | --- |
| QD-P-1.3.2 | AS-01, AS-04 | FM-02, FM-07, FM-09 | Medium |
| QD-P-1.6.2 | AS-01, AS-07 | FM-01, FM-07, FM-09 | Medium |
| QD-P-2.2.2 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.2.3 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.2.4 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.3.3 | AS-03, AS-09 | FM-06 | Medium |
| QD-P-2.3.4 | AS-03 | FM-06 | Medium |
| QD-P-2.4.3 | AS-05, AS-07, AS-09 | FM-03, FM-04, FM-05 | Medium |
| QD-P-2.5.2 | AS-01, AS-03, AS-04 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.5.3 | AS-04, AS-05 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.5.4 | AS-01, AS-07 | FM-08, FM-09, FM-10 | Conditional |
| QD-P-2.5.5 | AS-06 | FM-08, FM-10 | Conditional |
| QD-P-2.6.1 | AS-07 | FM-08, FM-10 | Medium |
| QD-P-2.6.2 | AS-07 | FM-08, FM-10 | Medium |
| QD-P-2.7.2 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |
| QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |

Candidate RAG-Agent quality metrics (candidate only, NOT a quality result): Correctness, Robustness, Boundary Recognition, Safety Response, Traceability, Consistency. The Quality subset was NOT executed.

## Status Board
Stage A (Single-artifact):  Executed - full L3 tier checklist applied to the lone System Prompt
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available
Stage C (Gate-0):           Not passed - G0-4 (no Tool Schema supplied)
Stage D (Permission QD-PM): Not Executed - incomplete artifact set
Stage E (Risk Explicit EX): Executed - no finding
Stage F (Impact outlook):   Executed - candidate mapping for Stage A FAILs
Stage G (Self-verification): Executed - see statement below

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. In-place self-corrections: none.
