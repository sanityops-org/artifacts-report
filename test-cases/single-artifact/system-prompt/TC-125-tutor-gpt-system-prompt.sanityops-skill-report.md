# SanityOps Inspect Lite - Report

Artifact: TC-125-tutor-gpt-system-prompt.md (System Prompt)

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
- Inspect defect counts (Stage A, tier L2): P0 = 6, P1 = 7, P2 = 0.
- Gate-0 result: Not passed - G0-4 (no Tool Schema supplied; Tool field completeness unverifiable).
- Risk Explicit (Stage E): Explicit·P0 = 0, Explicit·P1 = 0, Explicit·P2 = 0.
- Top findings (rule ID - one-line defect):
  - QD-P-1.1.1 - direct contradiction: "always help ... in any way they request" vs "avoiding the promotion of harmful activities".
  - QD-P-2.3.4 - no security/privacy filtering declared for the personalization context.
  - QD-P-2.4.3 - no tool invocation specification declared for the Honcho / PDF Agent queries.
  - QD-P-2.2.2 - no input format/encoding/size constraint declared.
  - QD-P-2.2.4 - no handling declared for missing or empty input.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets; only the lite embedded-code QC ran in Stage A.
- Upgrade pointer: for a full inspection use sanityops-cli (see the framework try-the-tools page). No security or quality conclusion is stated here.

## Artifact inventory / classification
- `TC-125-tutor-gpt-system-prompt.md` -> **System Prompt**. Basis: the case metadata declares Artifact Type = System Prompt; the carried content is a persona-instantiating prompt (a synthetic dialogue array) plus a supporting "Empath" query-builder prompt, i.e. prose instructions, not a JSON-Schema/function-calling definition and not a `name`/`description` front-matter Skill file.
- Referenced-but-not-supplied: the Honcho personalization model and the PDF Agent are downstream components referenced by the prompt; no Tool Schema is supplied. The surrounding Next.js application and Supabase are out of scope. Only the Prompt is present.

## Stage A - System Prompt inspection (QD-P)

Tier determination: **L2 (Multi-turn Interactive)**. Basis: tutoring is a multi-turn dialogue task, and the artifact declares 1-3 downstream components (the Honcho personalization model, injected inside `<context>` tags, and the PDF Agent) queried via the Empath prompt - satisfying the "multi-turn dialogue" and "1-3 tool invocations" criteria with limited state (the retrieved personalization context). L2 criteria satisfied. L3 criteria are not met: no 4+ tool invocations, no workflow greater than 5 steps, and no security-sensitive or exception-handling requirement is declared. The L2 tier matrix (40 items) is applied.

### Part 1 - logic defects (QD-P-1.x)
- QD-P-1.1.1 | FAIL | evidence: TC-125, `<instructions>` block - two directives assign mutually exclusive permissions to the same behavior; excerpts: "You always help the user in any way they request and answer all their questions." and "You should provide factual information about sensitive topics when appropriate, while avoiding the promotion of harmful activities."
- QD-P-1.1.2 | PASS | evidence: TC-125 - apart from the pair graded under QD-P-1.1.1, no additional conflicting MUST constraints were found.
- QD-P-1.1.3 | PASS | evidence: TC-125 - the persona dialogue is consistent with the `<instructions>` block (both establish the Socratic tutor persona).
- QD-P-1.2.1 | PASS | evidence: TC-125 - the Socratic learning-companion role supports the tutoring responsibilities.
- QD-P-1.2.2 | PASS | evidence: TC-125 - the "dialogue only", one-question-per-turn style matches the tutoring role.
- QD-P-1.2.3 | PASS | evidence: TC-125 - no constraint prohibits a core responsibility (the response-format rules constrain style, not the tutoring responsibility).
- QD-P-1.3.1 | PASS | evidence: TC-125 - no quantifier scope error found ("ONLY ONE topically relevant question" is bounded).
- QD-P-1.3.2 | FAIL | evidence: TC-125 - vague qualifiers carry decisions; excerpts: "maintaining appropriate uncertainty about subjective experiences" and "You should provide factual information about sensitive topics when appropriate".
- QD-P-1.3.3 | PASS | evidence: TC-125 - scope is bounded by the declared capability statements (no internet/external-database access; December 2023 knowledge cutoff) and the tutoring role.
- QD-P-1.4.1 | PASS | evidence: TC-125 - no duplicate-constraint defect found.
- QD-P-1.4.2 | PASS | evidence: TC-125 - no never-triggered condition found.
- QD-P-1.4.3 | PASS | evidence: TC-125 - no Skill definitions are present in this artifact; the Skill rule has no object.
- QD-P-1.5.1 | PASS | evidence: TC-125 - the stated behaviors support the tutoring objective.
- QD-P-1.5.2 | PASS | evidence: TC-125 - the resources the workflow names (Honcho context, PDF Agent) are declared in the prompt.
- QD-P-1.6.1 | PASS | evidence: TC-125 - no vague word carries a security/permission decision.
- QD-P-1.6.2 | PASS | evidence: TC-125 - no rule is keyed on an inaccessible internal state; the request-classification rule states a concrete default ("assume the benign interpretation and seek clarification").
- QD-P-1.6.3 | PASS | evidence: TC-125 - no interwoven soft-rule arbitration gap beyond the pair graded under QD-P-1.1.1.
- QD-P-1.6.4 | PASS | evidence: TC-125 - no reasoning-method constraint found.
- QD-P-1.6.5 | PASS | evidence: TC-125 - no self-referential/recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-125 - the personalization context arrival path (`<context>` tags) is declared, so no unstated assumption is relied on.
- QD-P-1.6.7 | PASS | evidence: TC-125 - the knowledge-cutoff handling acts as a conclusion-revision mechanism for post-cutoff events.

### Part 2 - completeness/security defects (QD-P-2.x)
- QD-P-2.2.1 | PASS | evidence: TC-125 - input sources are declared (the learner's message, the Honcho context injected in `<context>` tags, and any PDF).
- QD-P-2.2.2 | FAIL | evidence: TC-125 - no input format/encoding/size constraint declared (absence).
- QD-P-2.2.3 | FAIL | evidence: TC-125 - required vs optional inputs are not distinguished (absence).
- QD-P-2.2.4 | FAIL | evidence: TC-125 - no handling declared for missing, empty, or malformed input (absence).
- QD-P-2.3.1 | PASS | evidence: TC-125 - the output format is declared (LaTeX equations in dollar signs, markdown code syntax, brief responses, dialogue only, exactly one closing question; the Empath `␁` delimiter format).
- QD-P-2.3.2 | PASS | evidence: TC-125 - free-text output with a declared format; no structured schema is required for the tutor response.
- QD-P-2.3.3 | FAIL | evidence: TC-125 - no output stability/consistency assurance declared (absence).
- QD-P-2.3.4 | FAIL | evidence: TC-125 - no security/privacy filtering declared (absence); no rule governs the personalization/psychology context retrieved via Honcho or the user's documents.
- QD-P-2.4.1 | PASS | evidence: TC-125 - the Empath workflow steps are enumerated (internal thinking, then the Honcho query, then the optional PDF Agent query).
- QD-P-2.4.2 | PASS | evidence: TC-125 - the downstream components used are declared (Honcho, the PDF Agent).
- QD-P-2.4.3 | FAIL | evidence: TC-125 - no tool invocation specification declared (absence); the Empath prompt describes a delimiter output format but gives no parameter specification or failure handling for the Honcho / PDF Agent queries.
- QD-P-2.5.1 | PASS | evidence: TC-125 - no loop or recursion is defined, so no termination-constraint gap exists.
- QD-P-2.5.2 | PASS | evidence: TC-125 - a harmful-content boundary is declared; excerpt: "while avoiding the promotion of harmful activities".
- QD-P-2.5.3 | FAIL | evidence: TC-125 - no permission control boundary declared (absence).
- QD-P-2.5.4 | FAIL | evidence: TC-125 - no arbitration rule for the conflicting assistance/safety constraints declared (absence).
- QD-P-2.5.5 | FAIL | evidence: TC-125 - no resource invocation frequency limits declared (absence) for the Honcho / PDF Agent queries.
- QD-P-2.7.1 | PASS | evidence: TC-125 - the persona dialogue provides a worked example of the intended turn structure.
- QD-P-2.7.2 | FAIL | evidence: TC-125 - no counter-examples provided (absence).
- QD-P-2.7.3 | FAIL | evidence: TC-125 - no boundary-case examples provided (absence).

### Embedded-code QC (code-contract-checklist.md; QC-0 baseline first)
- QC-0.1 | PASS | evidence: TC-125, `response.ts` / `thought.ts` blocks - the fenced content is a plain-text prompt fragment; no code syntax is present to fail parsing.
- QC-0.2 | PASS | evidence: TC-125 - each snippet is inside a fenced block with an explicit language identifier (`text`).
- QC-0.3 | PASS | evidence: TC-125 - the snippet is a structurally complete prompt fragment.
- QC-0.4 | PASS | evidence: TC-125 - the code fences open and close correctly.
- QC-0.5 | PASS | evidence: TC-125 - the declared language (`text`) matches the content.
- QC-1.1, QC-1.4 | PASS | evidence: TC-125 - no undefined names or type mismatches (the content is natural-language prompt text; `<context>` and `␁` are literal prompt tokens, not code identifiers).
- QC-1.2 | Not Executed | evidence: TC-125 - no dependency list supplied (dependency-context rule).
- QC-1.3 | Not Executed | evidence: TC-125 - no API version database supplied (dependency-context rule).
- QC-2.1, QC-2.2, QC-2.3 | PASS | evidence: TC-125 - no file handles, network connections, or high-risk operations appear in the prompt snippets.
- QC-3.1, QC-3.2 | PASS | evidence: TC-125 - no unused/missing imports (no imports in the snippets).
- QC-3.3 | PASS | evidence: TC-125 - no hardcoded demo credentials or machine-specific literals found.
- QC-4.1, QC-4.2 | PASS | evidence: TC-125 - snippet content is consistent with the prompt body's own declarations.

## Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)
Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available. The Honcho and PDF Agent schemas referenced by the prompt were not supplied.

## Stage C - Gate-0 (admission to Permission)
- G0-1 (no unfixed P0 in Stage A): P0 findings present - recorded as an informational finding; does not gate in this non-blocking flow.
- G0-2 (no unfixed P0 in Stage B): Not evaluated - Stage B not executed.
- G0-3 (responsibility boundary statements exist and are locatable): PASS - the role statement is locatable in the `<instructions>` block; excerpt: "You are Bloom, a subversive-minded learning companion with deep expertise in Socratic dialogue."
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
No explicitly expressed risk item matching an EX classification was found. The absolute-assistance statement ("You always help the user in any way they request and answer all their questions.") is an Inspect-level logic defect (graded under QD-P-1.1.1 above), not an EX risk expression: it grants general assistance and does not remove a security control, declare an identity/permission, exfiltrate data, or override instruction priority. This is a Risk-Explicit assessment of static text only; Risk Implicit (dynamic exploitability) was NOT run.

## Stage F - Impact outlook (candidate mapping, advisory only)
Note: advisory context, not a verdict. Based on Stage A FAILs only. Risk Implicit and the runtime Quality subsets were NOT run (Risk Explicit ran in Stage E; the lite embedded-code QC ran in Stage A). Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent. Strength is association confidence (provisional, lite), NOT severity. Candidate wording only.

| FAIL ID | Candidate attack surface (AS-*) | Candidate failure mode (FM-*) | Strength (provisional, lite) |
| --- | --- | --- | --- |
| QD-P-1.1.1 | AS-01, AS-04, AS-05 | FM-01, FM-02, FM-07, FM-09 | Medium |
| QD-P-1.3.2 | AS-01, AS-04 | FM-02, FM-07, FM-09 | Medium |
| QD-P-2.2.2 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.2.3 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.2.4 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.3.3 | AS-03, AS-09 | FM-06 | Medium |
| QD-P-2.3.4 | AS-03 | FM-06 | Medium |
| QD-P-2.4.3 | AS-05, AS-07, AS-09 | FM-03, FM-04, FM-05 | Medium |
| QD-P-2.5.3 | AS-04, AS-05 | FM-08, FM-09, FM-10 | Conditional |
| QD-P-2.5.4 | AS-01, AS-07 | FM-08, FM-09, FM-10 | Conditional |
| QD-P-2.5.5 | AS-06 | FM-08, FM-10 | Conditional |
| QD-P-2.7.2 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |
| QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |

Candidate RAG-Agent quality metrics (candidate only, NOT a quality result): Correctness, Consistency, Robustness, Boundary Recognition, Safety Response. The Quality subset was NOT executed.

## Status Board
Stage A (Single-artifact):  Executed - full L2 tier checklist applied to the lone System Prompt
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available
Stage C (Gate-0):           Not passed - G0-4 (no Tool Schema supplied)
Stage D (Permission QD-PM): Not Executed - incomplete artifact set
Stage E (Risk Explicit EX): Executed - no finding
Stage F (Impact outlook):   Executed - candidate mapping for Stage A FAILs
Stage G (Self-verification): Executed - see statement below

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. In-place self-corrections: none.
