# SanityOps Inspect Lite - Report

Artifact: TC-115-notesgpt-system-prompt.md (System Prompt)

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
- Inspect defect counts (Stage A, tier L1): P0 = 2, P1 = 6, P2 = 0.
- Gate-0 result: Not passed - G0-4 (no Tool Schema supplied; Tool field completeness unverifiable).
- Risk Explicit (Stage E): Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings (rule ID - one-line defect):
  - QD-P-2.5.2 - no security boundary constraints; the transcript is not declared as untrusted data (indirect-injection surface).
  - QD-P-2.3.4 - no security/privacy filtering declared for sensitive transcript content.
  - QD-P-2.2.2 - no input length/format constraint declared.
  - QD-P-2.2.3 - required vs optional inputs not distinguished.
  - QD-P-2.2.4 - no missing-input handling declared in the prompt text.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets; only the lite embedded-code QC ran in Stage A.
- Upgrade pointer: for a full inspection use sanityops-cli (see the framework try-the-tools page). No security or quality conclusion is stated here.

## Artifact inventory / classification
- `TC-115-notesgpt-system-prompt.md` -> **System Prompt** (a single-sentence `system` message + zod field descriptors that act as secondary instructions). Basis: the case metadata declares Artifact Type = System Prompt; the effective instruction set is the `system` message plus field-description text, not a JSON-Schema/function-calling definition and not a `name`/`description` front-matter Skill file.
- Embedded snippet present (inspected as embedded code, not a standalone file): the `convex/together.ts` action (TypeScript) that builds the chat call and the zod `NoteSchema`.
- Referenced-but-not-supplied: the model/tool wiring outside the snippet. Only the Prompt plus its embedded snippet are present, so Stage B is structurally Not Executed and Gate-0 G0-4 cannot be satisfied.

## Stage A - System Prompt inspection (QD-P)

Tier determination: **L1 (Single-turn Task)**. Basis: the prompt performs a single extraction pass over one transcript and returns one JSON object; no tool invocations, no multi-turn dialogue, and no complex workflow are declared. L1 criteria satisfied (single skill; no tool invocations; no multi-turn dialogue; no complex reasoning); L2/L3 criteria not met. The L1 tier matrix (30 items) is applied.

### Part 1 - logic defects (QD-P-1.x)
- QD-P-1.1.1 | PASS | evidence: TC-115 - no mutually exclusive directives found.
- QD-P-1.1.2 | PASS | evidence: TC-115 - no conflicting MUST constraints requiring arbitration found.
- QD-P-1.1.3 | PASS | evidence: TC-115 - the inline JSON shape matches the zod `NoteSchema` (title/summary/actionItems).
- QD-P-1.2.1 | PASS | evidence: TC-115 - the extraction role supports the stated transformation task.
- QD-P-1.2.2 | PASS | evidence: TC-115 - the JSON output style matches the extraction role.
- QD-P-1.2.3 | PASS | evidence: TC-115 - no constraint prohibits a core responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-115 - quantifiers ("all action item lists", "fully resolved") are bounded by the schema.
- QD-P-1.3.2 | PASS | evidence: TC-115 - "short" qualifiers are bounded by the `summary.max(500)` limit and by the field descriptors; no unstable qualifier found.
- QD-P-1.3.3 | PASS | evidence: TC-115 - behavior is bounded to a single extraction pass over the transcript.
- QD-P-1.4.1 | PASS | evidence: TC-115 - no duplicate-constraint defect found.
- QD-P-1.4.2 | PASS | evidence: TC-115 - no unreachable branch found.
- QD-P-1.5.1 | PASS | evidence: TC-115 - stated behaviors (title, summary, action items) support the objective.
- QD-P-1.6.1 | PASS | evidence: TC-115 - no vague word carries a security/permission decision.
- QD-P-1.6.2 | PASS | evidence: TC-115 - no rule keyed on the model's own internal state found.
- QD-P-1.6.3 | PASS | evidence: TC-115 - no interwoven soft-rule arbitration gap found.
- QD-P-1.6.4 | PASS | evidence: TC-115 - no reasoning-method constraint found.
- QD-P-1.6.5 | PASS | evidence: TC-115 - no self-referential/recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-115 - no behavior-visible rule keyed on an unstated assumption beyond the input rules graded in Part 2.
- QD-P-1.6.7 | PASS | evidence: TC-115 - no static-knowledge conclusion-revision gap found.

### Part 2 - completeness/security defects (QD-P-2.x)
- QD-P-2.2.1 | PASS | evidence: TC-115 - the input source is declared ("a transcript of a voice message", passed as the `user` message).
- QD-P-2.2.2 | FAIL | evidence: TC-115 - no input length/format/encoding constraint declared for the transcript (absence); the model's 1000-token budget lives only in code, not as a prompt-level declaration.
- QD-P-2.2.3 | FAIL | evidence: TC-115 - required vs optional inputs not distinguished (absence).
- QD-P-2.2.4 | FAIL | evidence: TC-115 - no missing-input handling declared in the prompt text (absence); the `"Summary failed to generate"` fallback lives in the surrounding code block, not in the declared instructions.
- QD-P-2.3.1 | PASS | evidence: TC-115 - output format declared (JSON with title/summary/actionItems).
- QD-P-2.3.2 | PASS | evidence: TC-115 - the output schema is complete (`NoteSchema`: title, summary, actionItems).
- QD-P-2.3.4 | FAIL | evidence: TC-115 - no sensitive-data filtering or privacy handling rules declared (absence) for voice-transcript (PII) content.
- QD-P-2.5.2 | FAIL | evidence: TC-115 - no security boundary constraints declared (absence); the transcript is not declared as untrusted content to be treated as data, not instructions.
- QD-P-2.7.1 | PASS | evidence: TC-115 - the expected output shape is fixed both inline and by the zod schema; a positive structure is provided.
- QD-P-2.7.2 | FAIL | evidence: TC-115 - no counter-examples provided (absence).
- QD-P-2.7.3 | FAIL | evidence: TC-115 - no boundary-case examples provided (absence).

### Embedded-code QC (code-contract-checklist.md; QC-0 baseline first)
- QC-0.1 | PASS | evidence: TC-115, `convex/together.ts` block - the TypeScript action parses as valid syntax.
- QC-0.2 | PASS | evidence: TC-115 - the snippet is inside a fenced block with an explicit language identifier (`typescript`).
- QC-0.3 | PASS | evidence: TC-115 - the action is structurally complete as an illustrative snippet.
- QC-0.4 | PASS | evidence: TC-115 - fences open and close correctly.
- QC-0.5 | PASS | evidence: TC-115 - the declared language identifier matches the content.
- QC-1.1, QC-1.4 | PASS | evidence: TC-115 - referenced symbols (OpenAI, Instructor, z, v, internalAction, internal.together.saveSummary) are elided imports in an illustrative snippet; no type mismatch detected.
- QC-1.2 | Not Executed | evidence: TC-115 - no dependency list supplied (dependency-context rule).
- QC-1.3 | Not Executed | evidence: TC-115 - no API version database supplied (dependency-context rule).
- QC-2.1, QC-2.2 | PASS | evidence: TC-115 - no file handles or network connections opened without close/context manager.
- QC-2.3 | PASS | evidence: TC-115 - the model call is wrapped in try/catch with a fallback path.
- QC-3.1, QC-3.2 | PASS | evidence: TC-115 - no unused/missing imports within the illustrative snippet.
- QC-3.3 | PASS | evidence: TC-115 - `apiKey: togetherApiKey` is a variable reference, not a hardcoded secret; no demo literals found.
- QC-4.1, QC-4.2 | PASS | evidence: TC-115 - the inline JSON shape, the `NoteSchema`, and the descriptive fields are mutually consistent.

## Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)
Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.

## Stage C - Gate-0 (admission to Permission)
- G0-1 (no unfixed P0 in Stage A): P0 findings present - recorded as an informational finding; does not gate in this non-blocking flow.
- G0-2 (no unfixed P0 in Stage B): Not evaluated - Stage B not executed.
- G0-3 (responsibility boundary statements exist and are locatable): PASS - the role/task statement is locatable in the `system` message ("Extract a title, summary, and action items").
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
No explicitly expressed risk item matching an EX classification was found. The instruction is a plain extraction directive; the field descriptors are output-shape guidance, and the fallback string ("Summary failed to generate") is a degradation behavior, not a risk expression. This is a Risk-Explicit assessment of static text only; Risk Implicit (dynamic exploitability) was NOT run.

## Stage F - Impact outlook (candidate mapping, advisory only)
Note: advisory context, not a verdict. Based on Stage A FAILs only. Risk Implicit and the runtime Quality subsets were NOT run (Risk Explicit ran in Stage E; the lite embedded-code QC ran in Stage A). Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent. Strength is association confidence (provisional, lite), NOT severity. Candidate wording only.

| FAIL ID | Candidate attack surface (AS-*) | Candidate failure mode (FM-*) | Strength (provisional, lite) |
| --- | --- | --- | --- |
| QD-P-2.2.2 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.2.3 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.2.4 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.3.4 | AS-03 | FM-06 | Medium |
| QD-P-2.5.2 | AS-01, AS-03, AS-04 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.7.2 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |
| QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |

Candidate RAG-Agent quality metrics (candidate only, NOT a quality result): Correctness, Completeness, Robustness, Boundary Recognition, Safety Response. The Quality subset was NOT executed.

## Status Board
Stage A (Single-artifact):  Executed - full L1 tier checklist applied to the lone System Prompt
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available
Stage C (Gate-0):           Not passed - G0-4 (no Tool Schema supplied)
Stage D (Permission QD-PM): Not Executed - incomplete artifact set
Stage E (Risk Explicit EX): Executed - no finding
Stage F (Impact outlook):   Executed - candidate mapping for Stage A FAILs
Stage G (Self-verification): Executed - see statement below

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. In-place self-corrections: none.
