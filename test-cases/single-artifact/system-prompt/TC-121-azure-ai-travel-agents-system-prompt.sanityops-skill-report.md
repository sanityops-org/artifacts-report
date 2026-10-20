# SanityOps Inspect Lite - Report

Artifact: TC-121-azure-ai-travel-agents-system-prompt.md (System Prompt)

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
- Inspect defect counts (Stage A, tier L2): P0 = 7, P1 = 7, P2 = 0.
- Gate-0 result: Not passed - G0-4 (no Tool Schema supplied; Tool field completeness unverifiable).
- Risk Explicit (Stage E): Explicit·P0 = 0, Explicit·P1 = 0, Explicit·P2 = 0.
- Top findings (rule ID - one-line defect):
  - QD-P-2.5.2 - no prohibition/security boundary constraints declared.
  - QD-P-2.4.3 - no tool invocation parameter specification or failure handling declared.
  - QD-P-2.3.1 - no output format declared.
  - QD-P-2.3.4 - no security/privacy filtering declared.
  - QD-P-1.3.3 - critical behavioral boundaries (prohibition scope, handoff conditions) undefined.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets; only the lite embedded-code QC ran in Stage A.
- Upgrade pointer: for a full inspection use sanityops-cli (see the framework try-the-tools page). No security or quality conclusion is stated here.

## Artifact inventory / classification
- `TC-121-azure-ai-travel-agents-system-prompt.md` -> **System Prompt**. Basis: the case metadata declares Artifact Type = System Prompt (per-agent `instructions`); the carried content is prose instructions passed as the `instructions=` argument of a Microsoft Agent Framework `ChatAgent`, not a JSON-Schema/function-calling definition and not a `name`/`description` front-matter Skill file. The embedded Python is the agent-construction code that owns the prompt; it is inspected as an embedded snippet, not as a standalone source file.
- Referenced-but-not-supplied: the MCP tool schemas wired by `create_mcp_tool([...])` and the other agents in the same directory (`destination_recommendation_agent`, `triage_agent`, `echo_agent`). Only the two quoted agent prompts are present, so Stage B is structurally Not Executed and Gate-0 G0-4 cannot be satisfied.

## Stage A - System Prompt inspection (QD-P)

Tier determination: **L2 (Multi-turn Interactive)**. Basis: each agent is a conversational travel-planning agent that clarifies customer requirements over dialogue (multi-turn dialogue), and each agent declares a single MCP tool set (1-3 tool invocations). The workflow is simple (extract preferences, identify budget, understand dates, clarify ambiguity - within 5 steps) with limited state. L2 criteria satisfied. L3 criteria are not met: no 4+ tool invocations, no workflow greater than 5 steps, no security-sensitive operation, and no exception-handling requirement. The L2 tier matrix (40 items) is applied.

### Part 1 - logic defects (QD-P-1.x)
- QD-P-1.1.1 | PASS | evidence: TC-121 - no mutually exclusive directives found.
- QD-P-1.1.2 | PASS | evidence: TC-121 - no conflicting MUST constraints requiring arbitration found.
- QD-P-1.1.3 | PASS | evidence: TC-121 - no examples are provided, so no rule/example contradiction exists.
- QD-P-1.2.1 | PASS | evidence: TC-121 - each agent's role supports its stated responsibilities (preference analysis vs. itinerary construction).
- QD-P-1.2.2 | PASS | evidence: TC-121 - the interpersonal style guidance ("empathetic, patient, thorough") matches the customer-service role.
- QD-P-1.2.3 | PASS | evidence: TC-121 - no constraint prohibits a core responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-121 - no quantifier scope error found.
- QD-P-1.3.2 | PASS | evidence: TC-121 - the soft quality adjectives ("personalized", "realistic, enjoyable") are output-quality guidance, not decision-carrying vague qualifiers on a behavioral boundary.
- QD-P-1.3.3 | FAIL | evidence: TC-121 - critical behavioral boundaries are undefined; excerpt: "Clarify any ambiguous requirements" (no prohibition scope, escalation or handoff boundary is declared for either agent), and the itinerary agent's "Be detail-oriented, practical, and create realistic, enjoyable itineraries" leaves the scope of allowed behavior unbounded.
- QD-P-1.4.1 | PASS | evidence: TC-121 - no duplicate-constraint defect found.
- QD-P-1.4.2 | PASS | evidence: TC-121 - no never-triggered condition found.
- QD-P-1.4.3 | PASS | evidence: TC-121 - no Skill definitions are present in this artifact; the Skill rule has no object.
- QD-P-1.5.1 | PASS | evidence: TC-121 - the enumerated responsibilities support each agent's objective.
- QD-P-1.5.2 | PASS | evidence: TC-121 - the resources the workflow names (the per-agent MCP tool set) are declared alongside the prompt.
- QD-P-1.6.1 | PASS | evidence: TC-121 - no vague word carries a security/permission decision.
- QD-P-1.6.2 | PASS | evidence: TC-121 - no rule keyed on the model's internal state (confidence/intent/motivation) found.
- QD-P-1.6.3 | PASS | evidence: TC-121 - no interwoven soft-rule arbitration gap found.
- QD-P-1.6.4 | PASS | evidence: TC-121 - no reasoning-method constraint found.
- QD-P-1.6.5 | PASS | evidence: TC-121 - no self-referential/recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-121 - no behavior-visible rule keyed on an unstated assumption beyond the input rules graded in Part 2.
- QD-P-1.6.7 | PASS | evidence: TC-121 - no static-knowledge conclusion-revision gap found.

### Part 2 - completeness/security defects (QD-P-2.x)
- QD-P-2.2.1 | PASS | evidence: TC-121 - the input source is declared by role; excerpt: "understand and analyze customer travel preferences, requirements, and constraints" (the customer's request).
- QD-P-2.2.2 | FAIL | evidence: TC-121 - no input format/encoding/size limits declared (absence).
- QD-P-2.2.3 | FAIL | evidence: TC-121 - required vs optional inputs are not distinguished (absence).
- QD-P-2.2.4 | PASS | evidence: TC-121 - handling of under-specified input is declared; excerpt: "Clarify any ambiguous requirements".
- QD-P-2.3.1 | FAIL | evidence: TC-121 - no output format declared (absence); no structure, fields or encoding are specified for the itinerary or the preference summary.
- QD-P-2.3.2 | PASS | evidence: TC-121 - free-text conversational output; no structured schema is required.
- QD-P-2.3.3 | FAIL | evidence: TC-121 - no output stability/consistency assurance declared (absence).
- QD-P-2.3.4 | FAIL | evidence: TC-121 - no sensitive-data filtering or privacy handling rules declared (absence).
- QD-P-2.4.1 | PASS | evidence: TC-121 - the enumerated responsibilities provide the workflow steps for each agent.
- QD-P-2.4.2 | PASS | evidence: TC-121 - the tools used are declared (the per-agent MCP tool set in `tools=[create_mcp_tool([...])]`).
- QD-P-2.4.3 | FAIL | evidence: TC-121 - no tool invocation specification declared; excerpt: "Use available tools for planning assistance" gives no parameter specification, invocation sequence, or failure handling (absence).
- QD-P-2.5.1 | PASS | evidence: TC-121 - no loop or recursion is defined, so no termination-constraint gap exists.
- QD-P-2.5.2 | FAIL | evidence: TC-121 - no prohibition/security boundary constraints declared (absence); no untrusted-input boundary and no prohibited-operation boundary are stated.
- QD-P-2.5.3 | FAIL | evidence: TC-121 - no permission control boundary declared (absence).
- QD-P-2.5.4 | FAIL | evidence: TC-121 - no arbitration rule for potentially conflicting constraints declared (absence).
- QD-P-2.5.5 | FAIL | evidence: TC-121 - no resource invocation frequency limits declared (absence), despite MCP tool usage.
- QD-P-2.7.1 | FAIL | evidence: TC-121 - no positive examples provided (absence).
- QD-P-2.7.2 | FAIL | evidence: TC-121 - no counter-examples provided (absence).
- QD-P-2.7.3 | FAIL | evidence: TC-121 - no boundary-case examples provided (absence).

### Embedded-code QC (code-contract-checklist.md; QC-0 baseline first)
- QC-0.1 | PASS | evidence: TC-121, `ChatAgent(...)` construction blocks - the Python parses as valid syntax.
- QC-0.2 | PASS | evidence: TC-121 - each snippet is inside a fenced block with an explicit language identifier (`python`).
- QC-0.3 | PASS | evidence: TC-121 - the snippets are verbatim module excerpts; module-level imports and helpers (os, AzureOpenAIChatClient, create_mcp_tool) live outside the quoted lines.
- QC-0.4 | PASS | evidence: TC-121 - the code fences open and close correctly.
- QC-0.5 | PASS | evidence: TC-121 - the declared language (`python`) matches the content.
- QC-1.1, QC-1.4 | PASS | evidence: TC-121 - the names used are module-level imports/helpers of the owning source file; no type mismatch is evident.
- QC-1.2 | Not Executed | evidence: TC-121 - no dependency list supplied (dependency-context rule).
- QC-1.3 | Not Executed | evidence: TC-121 - no API version database supplied (dependency-context rule).
- QC-2.1, QC-2.2, QC-2.3 | PASS | evidence: TC-121 - no file handles, network connections, or high-risk operations appear in the snippets.
- QC-3.1, QC-3.2 | PASS | evidence: TC-121 - no unused/missing imports inside the quoted excerpt (no imports in the snippet).
- QC-3.3 | PASS | evidence: TC-121 - the API key is read from the environment (`os.environ.get("AZURE_OPENAI_API_KEY", "")`), not hardcoded; no machine-specific literals found.
- QC-4.1, QC-4.2 | PASS | evidence: TC-121 - snippet content is consistent with the prompt body's own declarations.

## Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)
Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available. The MCP tool schemas referenced by the prompts were not supplied.

## Stage C - Gate-0 (admission to Permission)
- G0-1 (no unfixed P0 in Stage A): P0 findings present - recorded as an informational finding; does not gate in this non-blocking flow.
- G0-2 (no unfixed P0 in Stage B): Not evaluated - Stage B not executed.
- G0-3 (responsibility boundary statements exist and are locatable): PASS - the role statement is locatable in each agent's instructions; excerpt: "You are a customer service agent for a travel planning system."
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
No explicitly expressed risk item matching an EX classification was found. The role statements and behavioral guidance are descriptive/quality instructions, not risk expressions. This is a Risk-Explicit assessment of static text only; Risk Implicit (dynamic exploitability) was NOT run.

## Stage F - Impact outlook (candidate mapping, advisory only)
Note: advisory context, not a verdict. Based on Stage A FAILs only. Risk Implicit and the runtime Quality subsets were NOT run (Risk Explicit ran in Stage E; the lite embedded-code QC ran in Stage A). Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent. Strength is association confidence (provisional, lite), NOT severity. Candidate wording only.

| FAIL ID | Candidate attack surface (AS-*) | Candidate failure mode (FM-*) | Strength (provisional, lite) |
| --- | --- | --- | --- |
| QD-P-1.3.3 | AS-01, AS-04 | FM-01, FM-02, FM-07, FM-09 | Medium |
| QD-P-2.2.2 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.2.3 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.3.1 | AS-03, AS-09 | FM-06 | Medium |
| QD-P-2.3.3 | AS-03, AS-09 | FM-06 | Medium |
| QD-P-2.3.4 | AS-03 | FM-06 | Medium |
| QD-P-2.4.3 | AS-05, AS-07, AS-09 | FM-03, FM-04, FM-05 | Medium |
| QD-P-2.5.2 | AS-01, AS-03, AS-04 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.5.3 | AS-04, AS-05 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.5.4 | AS-01, AS-07 | FM-08, FM-09, FM-10 | Conditional |
| QD-P-2.5.5 | AS-06 | FM-08, FM-10 | Conditional |
| QD-P-2.7.1 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |
| QD-P-2.7.2 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |
| QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |

Candidate RAG-Agent quality metrics (candidate only, NOT a quality result): Correctness, Completeness, Relevance, Robustness, Boundary Recognition, Safety Response. The Quality subset was NOT executed.

## Status Board
Stage A (Single-artifact):  Executed - full L2 tier checklist applied to the lone System Prompt
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available
Stage C (Gate-0):           Not passed - G0-4 (no Tool Schema supplied)
Stage D (Permission QD-PM): Not Executed - incomplete artifact set
Stage E (Risk Explicit EX): Executed - no finding
Stage F (Impact outlook):   Executed - candidate mapping for Stage A FAILs
Stage G (Self-verification): Executed - see statement below

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. In-place self-corrections: none.
