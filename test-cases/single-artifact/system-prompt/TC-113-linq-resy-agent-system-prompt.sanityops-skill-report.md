# SanityOps Inspect Lite - Report

Artifact: TC-113-linq-resy-agent-system-prompt.md (System Prompt)

## Provenance Header
- Host model: unspecified (host model self-declaration not available in this environment)
- Skill package: sanityops-inspect-lite v1.0.0
- Specification baseline: SanityOps Framework v1.0 (September 2026)
- Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
- Inspection date: 2026-10-15
- Artifact version: not supplied by the user (using the case's Collection Date as the working label) - working label 2026-10-14

## Executive Summary
- Executed stages: Stage A (single-artifact System Prompt), Stage C (Gate-0), Stage E (Risk Explicit), Stage F (impact outlook), Stage G (self-verification).
- Not executed: Stage B (cross; no Prompt+Skill+Tool set from the same agent), Stage D (Permission; incomplete artifact set).
- Inspect defect counts (Stage A, tier L3): P0 = 14, P1 = 1, P2 = 0.
- Gate-0 result: Not passed - G0-4 (no Tool Schema supplied; Tool field completeness unverifiable).
- Risk Explicit (Stage E): Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings (rule ID - one-line defect):
  - QD-P-2.2.2 - no input format/encoding/size constraint declared.
  - QD-P-2.2.3 - required vs optional inputs not distinguished.
  - QD-P-2.5.2 - no security boundary constraints (no untrusted-content / indirect-injection rule).
  - QD-P-2.3.4 - no security/privacy filtering declared.
  - QD-P-2.4.3 - tool invocation failure handling / parameter specification not declared.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets; only the lite embedded-code QC ran in Stage A.
- Upgrade pointer: for a full inspection use sanityops-cli (see the framework try-the-tools page). No security or quality conclusion is stated here.

## Artifact inventory / classification
- `TC-113-linq-resy-agent-system-prompt.md` -> **System Prompt** (prose/markdown instructions + a code-lifecycle context). Basis: the case metadata declares Artifact Type = System Prompt; the carried text is a base `SYSTEM_PROMPT` string plus context-derived postscript sections, not a JSON-Schema/function-calling definition and not a `name`/`description` front-matter Skill file.
- Referenced-but-not-supplied: the Resy tool schemas (resy_search, resy slots, resy_book, resy_cancel, resy_profile, resy_sign_out, remember_user) and the web-search tool. Only the Prompt is present, so Stage B is structurally Not Executed and Gate-0 G0-4 cannot be satisfied.

## Stage A - System Prompt inspection (QD-P)

Tier determination: **L3 (Complex Agent)**. Basis: the prompt defines a text-message reservation assistant over iMessage/RCS that uses 4+ distinct tools (restaurant search, time-slot lookup, booking, cancel, profile lookup, sign-out, remember_user, web search), operates over multi-turn conversation history, has real-world side effects (actual Resy reservations), and is privacy/permission-adjacent (user profile PII, system-handled authentication). L3 criteria satisfied: 4+ tool invocations and security-sensitive (privacy/permissions); multi-turn dialogue and limited state management also hold, so L2 is covered by upward compatibility. The L3 tier matrix (47 items) is applied.

### Part 1 - logic defects (QD-P-1.x)
- QD-P-1.1.1 | PASS | evidence: TC-113 - no mutually exclusive directives found.
- QD-P-1.1.2 | PASS | evidence: TC-113 - no conflicting MUST constraints requiring arbitration found (tool-timing and style rules do not collide).
- QD-P-1.1.3 | PASS | evidence: TC-113 - the inline example message ("heres your reservation link" then the URL) is consistent with the `---` split rule.
- QD-P-1.2.1 | PASS | evidence: TC-113 - the reservation-assistant role supports the stated responsibilities.
- QD-P-1.2.2 | PASS | evidence: TC-113, ## Response Style - the texting style matches the role and channel.
- QD-P-1.2.3 | PASS | evidence: TC-113 - no constraint prohibits a core responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-113 - no quantifier scope error found ("each message", "2-4 separate messages" are bounded).
- QD-P-1.3.2 | FAIL | evidence: TC-113, ## Reactions - vague qualifiers used; excerpt: "React to messages sparingly - text responses are always preferred. Use reactions only as supplements." (also "Use web search proactively", "Only use when explicitly requested or for truly special moments").
- QD-P-1.3.3 | PASS | evidence: TC-113 - behavior is bounded by the reservation workflow and the channel rules; no unbounded tool/permission scope introduced.
- QD-P-1.4.1 | PASS | evidence: TC-113 - no duplicate-constraint defect found.
- QD-P-1.4.2 | PASS | evidence: TC-113 - no unreachable branch found.
- QD-P-1.4.3 | PASS | evidence: TC-113 - no Skill definitions are present in this artifact; the Skill rule has no object.
- QD-P-1.5.1 | PASS | evidence: TC-113 - stated behaviors support the reservation objective.
- QD-P-1.5.2 | PASS | evidence: TC-113 - every tool the workflow names is declared in the prompt.
- QD-P-1.6.1 | PASS | evidence: TC-113 - no vague word carries a security/permission decision.
- QD-P-1.6.2 | PASS | evidence: TC-113 - no rule keyed on the model's own internal state (confidence/intent/motivation) found.
- QD-P-1.6.3 | PASS | evidence: TC-113 - no interwoven soft-rule arbitration gap found.
- QD-P-1.6.4 | PASS | evidence: TC-113 - no reasoning-method constraint found.
- QD-P-1.6.5 | PASS | evidence: TC-113 - no self-referential/recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-113 - no behavior-visible rule keyed on an unstated assumption beyond the input rules graded in Part 2.
- QD-P-1.6.7 | PASS | evidence: TC-113 - no static-knowledge conclusion-revision gap found.

### Part 2 - completeness/security defects (QD-P-2.x)
- QD-P-2.1.1 | PASS | evidence: TC-113 - the markdown structure is readable; no format-compliance defect found.
- QD-P-2.1.2 | PASS | evidence: TC-113 - tool and section references are named clearly.
- QD-P-2.1.3 | PASS | evidence: TC-113 - section hierarchy is reasonable.
- QD-P-2.1.4 | PASS | evidence: TC-113 - no language-conciseness defect found.
- QD-P-2.2.1 | PASS | evidence: TC-113, ## Conversation Awareness - input sources declared (user text messages, conversation history, web search results).
- QD-P-2.2.2 | FAIL | evidence: TC-113 - no input format/encoding/size limits declared for incoming text messages (absence).
- QD-P-2.2.3 | FAIL | evidence: TC-113 - required vs optional inputs not distinguished (absence).
- QD-P-2.2.4 | FAIL | evidence: TC-113 - no handling declared for missing or malformed input (absence).
- QD-P-2.3.1 | PASS | evidence: TC-113, ## Response Style - output format declared (plain text, no markdown, `---` message splitting).
- QD-P-2.3.2 | PASS | evidence: TC-113 - free-text output with declared style; no structured schema required.
- QD-P-2.3.3 | FAIL | evidence: TC-113 - no output stability/consistency assurance declared (absence).
- QD-P-2.3.4 | FAIL | evidence: TC-113 - no sensitive-data filtering or privacy handling rules declared (absence) for user profile / conversation content.
- QD-P-2.4.1 | PASS | evidence: TC-113, ## Resy Booking Flow - the booking workflow steps are enumerated.
- QD-P-2.4.2 | PASS | evidence: TC-113 - the tools used (resy_search, slots, book, cancel, profile, sign_out, remember_user) are declared.
- QD-P-2.4.3 | FAIL | evidence: TC-113, ## Resy Booking Flow - invocation sequence is given but parameter specifications and invocation failure handling are not declared (partial absence).
- QD-P-2.5.1 | PASS | evidence: TC-113 - no loop/recursion is defined, so no termination-constraint gap exists.
- QD-P-2.5.2 | FAIL | evidence: TC-113 - no prohibition/security boundary constraints declared (absence); untrusted web-search results are not declared as data-not-instructions.
- QD-P-2.5.3 | FAIL | evidence: TC-113 - no permission control boundary declared beyond the auth split (absence).
- QD-P-2.5.4 | FAIL | evidence: TC-113 - no arbitration rule for potentially conflicting soft constraints declared (absence).
- QD-P-2.5.5 | FAIL | evidence: TC-113 - no resource invocation frequency limits declared (absence), despite proactive web search.
- QD-P-2.6.1 | FAIL | evidence: TC-113 - runtime exceptions from tool invocation are not covered (absence).
- QD-P-2.6.2 | FAIL | evidence: TC-113 - no degradation/recovery strategy declared (absence).
- QD-P-2.6.3 | PASS | evidence: TC-113 - no retry mechanism is declared, so no unreasonable-retry defect exists.
- QD-P-2.7.1 | PASS | evidence: TC-113 - a positive example of the confirmation message is provided.
- QD-P-2.7.2 | FAIL | evidence: TC-113 - no counter-examples provided (absence).
- QD-P-2.7.3 | FAIL | evidence: TC-113 - no boundary-case examples provided (absence).

### Embedded-code QC (code-contract-checklist.md; QC-0 baseline first)
- QC-0.1 | PASS | evidence: TC-113, `buildSystemPrompt(chatContext)` postscript block - the template interpolations parse as valid structure.
- QC-0.2 | PASS | evidence: TC-113 - each snippet is inside a fenced block with an explicit language identifier (`text`).
- QC-0.3 | PASS | evidence: TC-113 - the snippet is a structurally complete prompt-template fragment.
- QC-0.4 | PASS | evidence: TC-113 - fences open and close correctly.
- QC-0.5 | PASS | evidence: TC-113 - the declared language (`text`) matches the content.
- QC-1.1, QC-1.4 | PASS | evidence: TC-113 - interpolations ({senderHandle}, {profile.name}, {chatName}, {participants}, {service}) are runtime inputs; no undefined names or type mismatches.
- QC-1.2 | Not Executed | evidence: TC-113 - no dependency list supplied (dependency-context rule).
- QC-1.3 | Not Executed | evidence: TC-113 - no API version database supplied (dependency-context rule).
- QC-2.1, QC-2.2, QC-2.3 | PASS | evidence: TC-113 - no file handles, network connections, or high-risk operations appear in the prompt snippets.
- QC-3.1, QC-3.2 | PASS | evidence: TC-113 - no unused/missing imports (no imports in the snippets).
- QC-3.3 | PASS | evidence: TC-113 - no hardcoded demo credentials or machine-specific literals found.
- QC-4.1, QC-4.2 | PASS | evidence: TC-113 - snippet fields are consistent with the prompt body's own declarations.

## Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)
Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available. The tool schemas referenced by the prompt were not supplied.

## Stage C - Gate-0 (admission to Permission)
- G0-1 (no unfixed P0 in Stage A): P0 findings present - recorded as an informational finding; does not gate in this non-blocking flow.
- G0-2 (no unfixed P0 in Stage B): Not evaluated - Stage B not executed.
- G0-3 (responsibility boundary statements exist and are locatable): PASS - the role statement is locatable at the top of the artifact ("You are a helpful AI reservation assistant accessible via text message").
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
No explicitly expressed risk item matching an EX classification was found. The anti-deception rules ("NEVER write '[signed you out]'", "you MUST use the actual tools") and the auth-delegation statement ("You do NOT handle auth. The system does.") are constraint statements, not risk expressions. This is a Risk-Explicit assessment of static text only; Risk Implicit (dynamic exploitability) was NOT run.

## Stage F - Impact outlook (candidate mapping, advisory only)
Note: advisory context, not a verdict. Based on Stage A FAILs only. Risk Implicit and the runtime Quality subsets were NOT run (Risk Explicit ran in Stage E; the lite embedded-code QC ran in Stage A). Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent. Strength is association confidence (provisional, lite), NOT severity. Candidate wording only.

| FAIL ID | Candidate attack surface (AS-*) | Candidate failure mode (FM-*) | Strength (provisional, lite) |
| --- | --- | --- | --- |
| QD-P-1.3.2 | AS-01, AS-04 | FM-02, FM-07, FM-09 | Medium |
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

Candidate RAG-Agent quality metrics (candidate only, NOT a quality result): Correctness, Robustness, Boundary Recognition, Safety Response, Traceability. The Quality subset was NOT executed.

## Status Board
Stage A (Single-artifact):  Executed - full L3 tier checklist applied to the lone System Prompt
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available
Stage C (Gate-0):           Not passed - G0-4 (no Tool Schema supplied)
Stage D (Permission QD-PM): Not Executed - incomplete artifact set
Stage E (Risk Explicit EX): Executed - no finding
Stage F (Impact outlook):   Executed - candidate mapping for Stage A FAILs
Stage G (Self-verification): Executed - see statement below

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. In-place self-corrections: none.
