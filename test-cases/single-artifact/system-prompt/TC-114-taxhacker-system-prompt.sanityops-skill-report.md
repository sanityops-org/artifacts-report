# SanityOps Inspect Lite - Report

Artifact: TC-114-taxhacker-system-prompt.md (System Prompt)

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
- Inspect defect counts (Stage A, tier L1): P0 = 2, P1 = 5, P2 = 0.
- Gate-0 result: Not passed - G0-4 (no Tool Schema supplied; Tool field completeness unverifiable).
- Risk Explicit (Stage E): Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings (rule ID - one-line defect):
  - QD-P-2.5.2 - no security boundary constraints; the invoice document is not declared as untrusted data (indirect-injection surface).
  - QD-P-2.3.4 - no security/privacy filtering declared for extracted financial/PII content.
  - QD-P-2.2.2 - no input format/encoding/size constraint declared.
  - QD-P-2.2.3 - required vs optional inputs not distinguished.
  - QD-P-2.7.2 - no counter-examples provided.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets; only the lite embedded-code QC ran in Stage A.
- Upgrade pointer: for a full inspection use sanityops-cli (see the framework try-the-tools page). No security or quality conclusion is stated here.

## Artifact inventory / classification
- `TC-114-taxhacker-system-prompt.md` -> **System Prompt** (prose instruction template + embedded TypeScript snippets). Basis: the case metadata declares Artifact Type = System Prompt; the carried text is a user-editable prompt template (`DEFAULT_PROMPT_ANALYSE_NEW_FILE`) with placeholder substitution, not a JSON-Schema/function-calling definition and not a `name`/`description` front-matter Skill file.
- Embedded snippets present (inspected as embedded code, not standalone files): `buildLLMPrompt` (TypeScript), `fieldsToJsonSchema` (TypeScript), and a settings-object literal.
- Referenced-but-not-supplied: the `Field`/`Category`/`Project` ambient types and the model-call wiring. Only the Prompt plus embedded snippets are present, so Stage B is structurally Not Executed and Gate-0 G0-4 cannot be satisfied.

## Stage A - System Prompt inspection (QD-P)

Tier determination: **L1 (Single-turn Task)**. Basis: the prompt performs a single extraction pass over one supplied invoice and returns one object; no tool invocations, no multi-turn dialogue, and no complex workflow are declared. L1 criteria satisfied (single skill; no tool invocations; no multi-turn dialogue; no complex reasoning); L2/L3 criteria not met. The L1 tier matrix (30 items) is applied.

### Part 1 - logic defects (QD-P-1.x)
- QD-P-1.1.1 | PASS | evidence: TC-114 - no mutually exclusive directives found.
- QD-P-1.1.2 | PASS | evidence: TC-114 - no conflicting MUST constraints requiring arbitration found.
- QD-P-1.1.3 | PASS | evidence: TC-114 - the "Return only one object" rule is consistent with the schema builder's single-object contract.
- QD-P-1.2.1 | PASS | evidence: TC-114 - the "accountant and invoice analysis assistant" role supports the extraction task.
- QD-P-1.2.2 | PASS | evidence: TC-114 - the output style (a single object, no extra text) matches the role.
- QD-P-1.2.3 | PASS | evidence: TC-114 - no constraint prohibits a core responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-114 - quantifiers ("all separate products", "any other text") are bounded.
- QD-P-1.3.2 | PASS | evidence: TC-114 - no unstable vague qualifier found; the missing-value rule is deterministic ("leave it blank").
- QD-P-1.3.3 | PASS | evidence: TC-114 - behavior is bounded to extraction from the supplied invoice.
- QD-P-1.4.1 | PASS | evidence: TC-114 - no duplicate-constraint defect found.
- QD-P-1.4.2 | PASS | evidence: TC-114 - no unreachable branch found.
- QD-P-1.5.1 | PASS | evidence: TC-114 - stated behaviors (fields, items, categories, projects) support the extraction objective.
- QD-P-1.6.1 | PASS | evidence: TC-114 - no vague word carries a security/permission decision.
- QD-P-1.6.2 | PASS | evidence: TC-114 - no rule keyed on the model's own internal state found.
- QD-P-1.6.3 | PASS | evidence: TC-114 - no interwoven soft-rule arbitration gap found.
- QD-P-1.6.4 | PASS | evidence: TC-114 - no reasoning-method constraint found.
- QD-P-1.6.5 | PASS | evidence: TC-114 - no self-referential/recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-114 - no behavior-visible rule keyed on an unstated assumption beyond the input rules graded in Part 2.
- QD-P-1.6.7 | PASS | evidence: TC-114 - no static-knowledge conclusion-revision gap found.

### Part 2 - completeness/security defects (QD-P-2.x)
- QD-P-2.2.1 | PASS | evidence: TC-114 - the input source is declared ("from the given invoice").
- QD-P-2.2.2 | FAIL | evidence: TC-114 - no input document format/encoding/size limits declared (absence); image vs PDF vs text is not constrained.
- QD-P-2.2.3 | FAIL | evidence: TC-114 - required vs optional inputs not distinguished (absence).
- QD-P-2.2.4 | PASS | evidence: TC-114 - missing-input handling declared; excerpt: "If you can't find something leave it blank, NEVER make up information".
- QD-P-2.3.1 | PASS | evidence: TC-114 - output format declared ("Return only one object", structured JSON via the accompanying schema).
- QD-P-2.3.2 | PASS | evidence: TC-114 - the output schema (`fieldsToJsonSchema`, required fields + `items`, `additionalProperties: false`) is provided.
- QD-P-2.3.4 | FAIL | evidence: TC-114 - no sensitive-data filtering or privacy handling rules declared (absence) for extracted invoice/financial content.
- QD-P-2.5.2 | FAIL | evidence: TC-114 - no security boundary constraints declared (absence); the invoice/document content is not declared as untrusted data to be treated as data, not instructions.
- QD-P-2.7.1 | PASS | evidence: TC-114 - the prompt fixes a concrete positive output shape (fields + items); a positive example of the expected structure exists via the schema.
- QD-P-2.7.2 | FAIL | evidence: TC-114 - no counter-examples provided (absence).
- QD-P-2.7.3 | FAIL | evidence: TC-114 - no boundary-case examples provided (absence), beyond the generic "leave it blank" sentence.

### Embedded-code QC (code-contract-checklist.md; QC-0 baseline first)
- QC-0.1 | PASS | evidence: TC-114, `buildLLMPrompt` / `fieldsToJsonSchema` blocks - both TypeScript snippets parse as valid syntax.
- QC-0.2 | PASS | evidence: TC-114 - each snippet is inside a fenced block with an explicit language identifier (`typescript` / `text`).
- QC-0.3 | PASS | evidence: TC-114 - both functions are complete enough for standalone parsing.
- QC-0.4 | PASS | evidence: TC-114 - fences open and close correctly.
- QC-0.5 | PASS | evidence: TC-114 - the declared language identifiers match the content.
- QC-1.1, QC-1.4 | PASS | evidence: TC-114 - all referenced symbols (field, category, project) are parameters; no undefined names or type mismatches detected.
- QC-1.2 | Not Executed | evidence: TC-114 - no dependency list supplied (dependency-context rule).
- QC-1.3 | Not Executed | evidence: TC-114 - no API version database supplied (dependency-context rule).
- QC-2.1, QC-2.2, QC-2.3 | PASS | evidence: TC-114 - the snippets perform pure string substitution; no file handles, network connections, or high-risk operations.
- QC-3.1, QC-3.2 | PASS | evidence: TC-114 - no unused/missing imports in the snippets.
- QC-3.3 | PASS | evidence: TC-114 - no hardcoded credentials or machine-specific literals found.
- QC-4.1, QC-4.2 | PASS | evidence: TC-114 - the `{fields}`/`{categories}`/`{projects}` placeholders in the snippets match the declarations in the prompt body and the setting description.

## Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)
Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.

## Stage C - Gate-0 (admission to Permission)
- G0-1 (no unfixed P0 in Stage A): P0 findings present - recorded as an informational finding; does not gate in this non-blocking flow.
- G0-2 (no unfixed P0 in Stage B): Not evaluated - Stage B not executed.
- G0-3 (responsibility boundary statements exist and are locatable): PASS - the role statement is locatable in the first line ("You are an accountant and invoice analysis assistant").
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
No explicitly expressed risk item matching an EX classification was found. The grounding rules ("NEVER make up information", "If you can't find something leave it blank") and the output-purity rule ("Do not include any other text in your response!") are constraint statements, not risk expressions. This is a Risk-Explicit assessment of static text only; Risk Implicit (dynamic exploitability) was NOT run.

## Stage F - Impact outlook (candidate mapping, advisory only)
Note: advisory context, not a verdict. Based on Stage A FAILs only. Risk Implicit and the runtime Quality subsets were NOT run (Risk Explicit ran in Stage E; the lite embedded-code QC ran in Stage A). Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent. Strength is association confidence (provisional, lite), NOT severity. Candidate wording only.

| FAIL ID | Candidate attack surface (AS-*) | Candidate failure mode (FM-*) | Strength (provisional, lite) |
| --- | --- | --- | --- |
| QD-P-2.2.2 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.2.3 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.3.4 | AS-03 | FM-06 | Medium |
| QD-P-2.5.2 | AS-01, AS-03, AS-04 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.7.2 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |
| QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |

Candidate RAG-Agent quality metrics (candidate only, NOT a quality result): Correctness, Format Compliance, Boundary Recognition, Safety Response. The Quality subset was NOT executed.

## Status Board
Stage A (Single-artifact):  Executed - full L1 tier checklist applied to the lone System Prompt
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available
Stage C (Gate-0):           Not passed - G0-4 (no Tool Schema supplied)
Stage D (Permission QD-PM): Not Executed - incomplete artifact set
Stage E (Risk Explicit EX): Executed - no finding
Stage F (Impact outlook):   Executed - candidate mapping for Stage A FAILs
Stage G (Self-verification): Executed - see statement below

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. In-place self-corrections: none.
