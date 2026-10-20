# SanityOps Inspect Lite - Report

Artifact: TC-132-resume-matcher-system-prompt.md (System Prompt)

## Provenance Header
- Host model: unspecified (host model self-declaration not available in this environment)
- Skill package: sanityops-inspect-lite v1.0.0
- Specification baseline: SanityOps Framework v1.0 (September 2026)
- Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
- Inspection date: 2026-10-15
- Artifact version: not supplied by the user (using the case's Collection Date as the working label) - working label 2026-10-13

## Executive Summary
- Executed stages: Stage A (single-artifact System Prompt), Stage C (Gate-0), Stage E (Risk Explicit), Stage F (impact outlook), Stage G (self-verification).
- Not executed: Stage B (cross; single artifact, no Prompt+Skill+Tool set from the same agent), Stage D (Permission; incomplete artifact set).
- Inspect defect counts (Stage A, tier L2): P0 = 4, P1 = 4, P2 = 0.
- Gate-0 result: Not passed - G0-4 (no Tool Schema supplied; Tool field completeness unverifiable).
- Risk Explicit (Stage E): Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings (rule ID - one-line defect):
  - QD-P-2.2.2 - no input format/encoding/size constraint declared for the user answer.
  - QD-P-2.2.3 - required vs optional inputs not distinguished.
  - QD-P-2.3.4 - no security/privacy filtering declared for resume personal data.
  - QD-P-2.5.2 - no prohibition/security boundary constraints declared.
  - QD-P-1.3.2 - vague qualifier ("the most useful NEXT question") carries the adaptive decision.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets; only the lite embedded-code QC ran in Stage A.
- Upgrade pointer: for a full inspection use sanityops-cli (see the framework try-the-tools page). No security or quality conclusion is stated here.

## Artifact inventory / classification
- `TC-132-resume-matcher-system-prompt.md` -> **System Prompt** (prose/markdown instructions plus a JSON output-shape block). Basis: the case metadata declares Artifact Type = System Prompt; the carried text is the `RESUME_WIZARD_TURN_PROMPT` instruction string, not a JSON-Schema/function-calling definition and not a `name`/`description` front-matter Skill file.
- Referenced-but-not-supplied: no Tool Schema and no Skill definition accompany the prompt. Only the Prompt is present, so Stage B is structurally Not Executed and Gate-0 G0-4 cannot be satisfied.

## Stage A - System Prompt inspection (QD-P)

Tier determination: **L2 (Multi-turn Interactive)**. Basis: the artifact is a single turn of an adaptive resume wizard that runs across a multi-turn dialogue ("guiding a user ... ONE question at a time") and carries limited state (the injected CURRENT DRAFT JSON that it reads and updates each turn); it declares no tool invocations. L2 criteria satisfied: multi-turn dialogue and limited state management; L1 criteria do not hold (it is not a single-invocation task with no state), and no L3 criteria (4+ tools, workflow > 5 steps, security-sensitivity) are met. The L2 tier matrix (40 items) is applied.

### Part 1 - logic defects (QD-P-1.x)
- QD-P-1.1.1 | PASS | evidence: TC-132, RESUME_WIZARD_TURN_PROMPT - no mutually exclusive directives found.
- QD-P-1.1.2 | PASS | evidence: TC-132 - no conflicting MUST constraints requiring arbitration found (the truthfulness rules are marked "non-negotiable").
- QD-P-1.1.3 | PASS | evidence: TC-132, Output shape block - the JSON example is consistent with the stated output rules.
- QD-P-1.2.1 | PASS | evidence: TC-132 - the resume-writing role supports the stated responsibilities.
- QD-P-1.2.2 | PASS | evidence: TC-132 - the JSON-plus-localized-text output style matches the role.
- QD-P-1.2.3 | PASS | evidence: TC-132 - no constraint prohibits a core responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-132 - bounded quantifiers only ("ONE question at a time", "3 bullets", "2 bullets").
- QD-P-1.3.2 | FAIL | evidence: TC-132, ADAPTIVE FLOW - a vague qualifier carries the selection decision; excerpt: "choose the most useful NEXT question".
- QD-P-1.3.3 | PASS | evidence: TC-132 - behavior is bounded by the current section and the draft; no tool/permission scope introduced.
- QD-P-1.4.1 | PASS | evidence: TC-132 - the draft-preservation rules are consistent, not a duplicate-constraint defect.
- QD-P-1.4.2 | PASS | evidence: TC-132 - no unreachable branch found.
- QD-P-1.4.3 | PASS | evidence: TC-132 - no Skill definitions are present in this artifact; the Skill rule has no object.
- QD-P-1.5.1 | PASS | evidence: TC-132 - the stated behaviors support the general-master-resume objective.
- QD-P-1.5.2 | PASS | evidence: TC-132 - no external resource is required by the workflow; the draft and answer are injected inputs.
- QD-P-1.6.1 | PASS | evidence: TC-132 - no vague word carries a security/permission decision.
- QD-P-1.6.2 | PASS | evidence: TC-132 - no rule keyed on the model's own confidence/intent/motivation state found.
- QD-P-1.6.3 | PASS | evidence: TC-132 - no interwoven soft-rule arbitration gap found.
- QD-P-1.6.4 | PASS | evidence: TC-132 - no reasoning-method constraint found.
- QD-P-1.6.5 | PASS | evidence: TC-132 - no self-referential/recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-132 - no behavior-visible rule keyed on an unstated assumption beyond the input rules graded in Part 2.
- QD-P-1.6.7 | PASS | evidence: TC-132 - draft-update rules ("preserve existing draft data unless the user clearly changes it") address knowledge revision.

### Part 2 - completeness/security defects (QD-P-2.x)
- QD-P-2.2.1 | PASS | evidence: TC-132 - input sources declared (the current draft JSON and the user's answer).
- QD-P-2.2.2 | FAIL | evidence: TC-132 - no input format/encoding/size limits declared for the user answer (absence).
- QD-P-2.2.3 | FAIL | evidence: TC-132 - required vs optional inputs not distinguished (absence).
- QD-P-2.2.4 | PASS | evidence: TC-132, TRUTHFULNESS RULES - missing-content handling declared; excerpt: "If a needed fact is missing or vague, do NOT guess - ask for it in 'next_question'".
- QD-P-2.3.1 | PASS | evidence: TC-132, Output shape block - output format declared ("Output ONLY this JSON object and nothing else").
- QD-P-2.3.2 | PASS | evidence: TC-132 - the output JSON schema fields are enumerated.
- QD-P-2.3.3 | FAIL | evidence: TC-132 - no output stability/consistency assurance declared (absence).
- QD-P-2.3.4 | FAIL | evidence: TC-132 - no sensitive-data filtering or privacy handling rules declared (absence) for resume personal data (name, email, phone, location).
- QD-P-2.4.1 | PASS | evidence: TC-132, ADAPTIVE FLOW - the turn workflow steps are enumerated.
- QD-P-2.4.2 | PASS | evidence: TC-132 - no external tools/resources are used, so none are undeclared.
- QD-P-2.4.3 | PASS | evidence: TC-132 - no tool invocation occurs in this artifact; the rule has no object.
- QD-P-2.5.1 | PASS | evidence: TC-132 - no loop/recursion is defined, so no termination-constraint gap exists.
- QD-P-2.5.2 | FAIL | evidence: TC-132 - no prohibition/security boundary constraints declared (absence).
- QD-P-2.5.3 | PASS | evidence: TC-132 - no external permissions/tools are declared; nothing to bound.
- QD-P-2.5.4 | PASS | evidence: TC-132 - the truthfulness rules are marked "non-negotiable", giving constraint priority.
- QD-P-2.5.5 | PASS | evidence: TC-132 - no resource invocations, so no frequency-limit gap exists.
- QD-P-2.7.1 | PASS | evidence: TC-132, Output shape block - the JSON object provides a positive output example.
- QD-P-2.7.2 | FAIL | evidence: TC-132 - no counter-examples provided (absence).
- QD-P-2.7.3 | FAIL | evidence: TC-132 - no boundary-case examples provided (absence), e.g. an empty draft or a missing answer.

### Embedded-code QC (code-contract-checklist.md; QC-0 baseline first)
- QC-0.1 | PASS | evidence: TC-132, RESUME_WIZARD_TURN_PROMPT block - the Python string assignment parses as valid syntax.
- QC-0.2 | PASS | evidence: TC-132 - the fenced block carries an explicit language identifier (`python`).
- QC-0.3 | PASS | evidence: TC-132 - the snippet is a structurally complete module-level string constant.
- QC-0.4 | PASS | evidence: TC-132 - the code fence opens and closes correctly.
- QC-0.5 | PASS | evidence: TC-132 - the declared language (`python`) matches the content.
- QC-1.1, QC-1.4 | PASS | evidence: TC-132 - the interpolations ({output_language}, {current_section}, {resume_json}, {answer_text}) are runtime template placeholders; no undefined names or type mismatches.
- QC-1.2 | Not Executed | evidence: TC-132 - no dependency list supplied (dependency-context rule).
- QC-1.3 | Not Executed | evidence: TC-132 - no API version database supplied (dependency-context rule).
- QC-2.1, QC-2.2, QC-2.3 | PASS | evidence: TC-132 - no file handles, network connections, or high-risk operations appear in the snippet.
- QC-3.1, QC-3.2 | PASS | evidence: TC-132 - no imports in the snippet, so no unused/missing import.
- QC-3.3 | PASS | evidence: TC-132 - no hardcoded demo credentials or machine-specific literals found.
- QC-4.1, QC-4.2 | PASS | evidence: TC-132 - the snippet's fields are consistent with the prompt body's own declarations.

## Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)
Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available (only the System Prompt was supplied).

## Stage C - Gate-0 (admission to Permission)
- G0-1 (no unfixed P0 in Stage A): P0 findings present - recorded as an informational finding; does not gate in this non-blocking flow.
- G0-2 (no unfixed P0 in Stage B): Not evaluated - Stage B not executed.
- G0-3 (responsibility boundary statements exist and are locatable): PASS - the role statement is locatable at the top of the artifact ("You are a truthful resume-writing assistant ...").
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
No explicitly expressed risk item matching an EX classification was found. The truthfulness rules ("Never invent employers ..."), the id-reuse rule ("Never invent or reuse a positive id") and the draft-preservation rule are constraint statements, not risk expressions; no override, exfiltration, credential or PII value is present. This is a Risk-Explicit assessment of static text only; Risk Implicit (dynamic exploitability) was NOT run.

## Stage F - Impact outlook (candidate mapping, advisory only)
Note: advisory context, not a verdict. Based on Stage A FAILs only. Risk Implicit and the runtime Quality subsets were NOT run (Risk Explicit ran in Stage E; the lite embedded-code QC ran in Stage A). Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent. Strength is association confidence (provisional, lite), NOT severity. Candidate wording only.

| FAIL ID | Candidate attack surface (AS-*) | Candidate failure mode (FM-*) | Strength (provisional, lite) |
| --- | --- | --- | --- |
| QD-P-1.3.2 | AS-01, AS-04 | FM-02, FM-07, FM-09 | Medium |
| QD-P-2.2.2 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.2.3 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.3.3 | AS-03, AS-09 | FM-06 | Medium |
| QD-P-2.3.4 | AS-03 | FM-06 | Medium |
| QD-P-2.5.2 | AS-01, AS-03, AS-04 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.7.2 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |
| QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |

Candidate RAG-Agent quality metrics (candidate only, NOT a quality result): Correctness, Relevance, Consistency, Format Compliance. The Quality subset was NOT executed.

## Status Board
Stage A (Single-artifact):  Executed - full L2 tier checklist applied to the lone System Prompt
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available
Stage C (Gate-0):           Not passed - G0-4 (no Tool Schema supplied)
Stage D (Permission QD-PM): Not Executed - incomplete artifact set
Stage E (Risk Explicit EX): Executed - no finding
Stage F (Impact outlook):   Executed - candidate mapping for Stage A FAILs
Stage G (Self-verification): Executed - see statement below

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. In-place self-corrections: none.
