# SanityOps Inspect-Lite Report - TC-072-fabric-analyze-bill-system-prompt.md

- Host model: unspecified (host model self-declaration not available in this environment)
- Skill package: sanityops-inspect-lite v1.0.0
- Specification baseline: SanityOps Framework v1.0 (September 2026)
- Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
- Inspection date: 2026-10-14
- Artifact version: not supplied by the user (using the case's Collection Date as the working label; Collection Date: 2026-10-13)

## 1. Executive Summary

- Executed stages: Stage A (single-artifact System Prompt inspection, QD-P; QC not applicable), Stage C (Gate-0 admission check), Stage E (Risk Explicit), Stage F (Impact outlook), Stage G (self-verification).
- Inspect defect findings (Stage A, QD-P): P0 = 2, P1 = 8, P2 = 0 (10 FAIL over the 30 applicable L1 rules). Embedded-code QC: Not Executed (no executable code snippet).
- Gate-0 result: Not passed - G0-4.
- Risk-Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0 (no explicitly declared risk item identified in the static text).
- Top findings (up to five, rule ID - one-line defect):
  - QD-P-2.5.2 - No security boundary constraints are declared.
  - QD-P-2.3.4 - No security/privacy filtering mechanism is declared.
  - QD-P-1.3.2 - Vague judgment terms ("mostly overt or mostly dirty") carry the conclusion decision.
  - QD-P-1.6.6 - The prompt assumes the input is a bill; non-legislative input is not handled.
  - QD-P-2.2.4 - Handling of missing/empty input is undefined.
- What was NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets; the Stage A lite embedded-code QC was also not applicable here.
- Upgrade pointer: for the full inspect ruleset plus Risk and Quality, use sanityops-cli - https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md
- This report states no security conclusion and no quality conclusion; Inspect PASS is not Risk PASS and is not Quality PASS.

## 2. Stage A - System Prompt Inspection (QD-P)

Artifact inventory: one markdown transcript classified as a System Prompt by structural signature (prose instructions). The artifact is a single reusable Fabric pattern ("analyze_bill").

Tier determination: L1 (Single-turn Task). Basis: a single invocation produces the analysis; the artifact declares no tool invocations, no multi-turn dialogue, and no complex multi-step workflow (2 or more of the L1 determination criteria are satisfied). The L1 tier item set (30 items) is applied.

Not applicable at L1 (marked "-" in the tier matrix, no verdict emitted): QD-P-1.4.3, QD-P-1.5.2, QD-P-2.1.1, QD-P-2.1.2, QD-P-2.1.3, QD-P-2.1.4, QD-P-2.3.3, QD-P-2.4.1, QD-P-2.4.2, QD-P-2.4.3, QD-P-2.5.1, QD-P-2.5.3, QD-P-2.5.4, QD-P-2.5.5, QD-P-2.6.1, QD-P-2.6.2, QD-P-2.6.3.

### Part 1 - Logic defects
- QD-P-1.1.1 | PASS | P0 | evidence: TC-072, IDENTITY/STEPS/OUTPUT; no mutually exclusive directive on the same object.
- QD-P-1.1.2 | PASS | P1 | evidence: TC-072; no competing MUST-directives without arbitration.
- QD-P-1.1.3 | PASS | P0 | evidence: TC-072; no example contradicting a rule is present.
- QD-P-1.2.1 | PASS | P0 | evidence: TC-072, IDENTITY; the analyst role matches the bill-analysis responsibilities.
- QD-P-1.2.2 | PASS | P1 | evidence: TC-072; the opinionated stance matches the stated "3,129 IQ" analyzer persona.
- QD-P-1.2.3 | PASS | P0 | evidence: TC-072; no constraint prohibits the core analysis responsibility.
- QD-P-1.3.1 | PASS | P1 | evidence: TC-072, OUTPUT; quantifiers attach to concrete deliverables ("24-word summary", "5-10 16-word bullets").
- QD-P-1.3.2 | FAIL | P1 | evidence: TC-072, OUTPUT item 5; excerpt: "whether the bill is mostly overt or mostly dirty with ulterior motives" - undefined judgment terms carry the conclusion.
- QD-P-1.3.3 | PASS | P1 | evidence: TC-072; no authorization or handoff boundary applies to a single-turn analysis.
- QD-P-1.4.1 | PASS | P2 | evidence: TC-072; no duplicated constraint detected.
- QD-P-1.4.2 | PASS | P2 | evidence: TC-072; no unreachable branch detected.
- QD-P-1.5.1 | PASS | P0 | evidence: TC-072; the responsibilities cover the bill-analysis objective.
- QD-P-1.6.1 | PASS | P1 | evidence: TC-072; no vague word carries a security/permission decision.
- QD-P-1.6.2 | PASS | P1 | evidence: TC-072; no rule keyed on unobservable model internal state.
- QD-P-1.6.3 | PASS | P1 | evidence: TC-072; the STEPS and OUTPUT rules do not form an unarbitrated soft-rule conflict.
- QD-P-1.6.4 | FAIL | P1 | evidence: TC-072, STEPS item 1; excerpt: "Read the entire bill 37 times using different perspectives." - imposes an internal reasoning procedure the model cannot guarantee.
- QD-P-1.6.5 | PASS | P1 | evidence: TC-072; no self-referential/recursive constraint.
- QD-P-1.6.6 | FAIL | P1 | evidence: TC-072, IDENTITY/INPUT; the prompt assumes the input is a legislative bill, with no precondition check or handling for non-legislative input.
- QD-P-1.6.7 | PASS | P1 | evidence: TC-072; static single-pass analysis, no knowledge-revision rule implicated.

### Part 2 - Completeness/security defects
- QD-P-2.2.1 | PASS | P0 | evidence: TC-072, INPUT; the input source is declared (the "# INPUT" placeholder).
- QD-P-2.2.2 | FAIL | P1 | evidence: TC-072, INPUT; excerpt: the injected "INPUT:" carries no format, encoding, or size constraint.
- QD-P-2.2.3 | PASS | P1 | evidence: TC-072; a single input is required and no optional parameters exist to distinguish.
- QD-P-2.2.4 | FAIL | P1 | evidence: TC-072; no declaration handles empty/missing input (absence confirmed).
- QD-P-2.3.1 | PASS | P1 | evidence: TC-072, OUTPUT; the output sections are named (OVERT GOALS, COVERT GOALS, conclusion).
- QD-P-2.3.2 | PASS | P1 | evidence: TC-072, OUTPUT; the output structure and per-item count constraints are specified.
- QD-P-2.3.4 | FAIL | P0 | evidence: TC-072; no sensitive-data filtering, privacy handling, or security output constraint declared (absence confirmed).
- QD-P-2.5.2 | FAIL | P0 | evidence: TC-072; no prohibited operations, sensitive-data access boundary, or external access boundary declared (absence confirmed).
- QD-P-2.7.1 | FAIL | P1 | evidence: TC-072; no representative input-to-output example is provided (absence confirmed).
- QD-P-2.7.2 | FAIL | P1 | evidence: TC-072; no counter-example provided (absence confirmed).
- QD-P-2.7.3 | FAIL | P1 | evidence: TC-072; no boundary-case example provided (absence confirmed).

### QC - embedded code
- QC | Not Executed | n/a | evidence: TC-072; no executable code snippet is embedded (the fenced block is prompt text), so the QC-0 baseline is out of scope.

Stage A summary: 30 applicable QD-P rules, 10 FAIL (2 P0, 8 P1, 0 P2). P0 findings are carried forward and do not halt the flow.

## 3. Stage B - Cross-Artifact Inspection

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available. No cross results are invented.

## 4. Stage C - Gate-0 (admission to Permission)

Conditions verified per permission-checklist section 3.2:
- G0-1 (no unfixed P0 in Stage A): informational only; 2 P0 findings recorded and carried forward (does not gate in this non-blocking flow).
- G0-2 (no unfixed P0 in Stage B): informational only; Stage B Not Executed.
- G0-3 (responsibility boundary statements exist and are locatable): the IDENTITY block defines an analyzer role, so a responsibility baseline is locatable.
- G0-4 (each Tool Schema's name, description, and parameter descriptions are complete): unsatisfiable - the artifact set contains no Tool Schema, so no Tool-schema completeness can be verified.

Gate-0 result: Not passed - G0-4 (no Tool Schema present, so per-Tool completion of name/description/parameter descriptions cannot be verified).

## 5. Stage D - Permission Proportionality (QD-PM)

Not Executed - incomplete artifact set (precondition: full set Prompt + Skill + all Tool Schemas required; only a System Prompt is present).

## 6. Stage E - Risk Explicit (EX)

This section is a risk scan, physically separated from the Inspect verdicts above. It is not a defect verdict and not a security conclusion. Explicit-P0/P1/P2 is a Risk-Explicit assessment.

Audit object: TC-072 System Prompt. Scan path: NL-A (sentence-by-sentence) -> NL-B (cross-sentence) -> NR-O (decode) -> NR-S (structure/field).

Risk Item Summary
- Total risk items: 0
- Explicit-P0 (Block release): 0 items
- Explicit-P1 (Fix / exemption): 0 items
- Explicit-P2 (Risk ledger): 0 items

Note: no explicit risk expression (external export instruction, security-constraint removal, credential/PII/secret, dangerous flag, or external callback) was found in the static text. The literal-looking numbers ("37 times", "3,129 IQ", "10 KM by 10K") are stylistic and do not express a risk item. Risk Implicit (dynamic exploitability) was NOT run.

## 7. Stage F - Impact Outlook (candidate mapping, advisory only)

Advisory context only; this section does not change, soften, or escalate any Inspect verdict. Candidate language only; strength is not severity. Risk Implicit and the runtime Quality subsets were NOT run; only Stage E (Risk Explicit) ran (the Stage A embedded-code QC was not applicable). Per relevance.md section 1.4, no assumption is made that compensating controls outside the artifact are absent.

| Defect ID (severity) | Candidate AS-* | Candidate FM-* | Candidate RAG metrics | Strength (provisional lite) |
|---|---|---|---|---|
| QD-P-1.3.2 (P1) | AS-01, AS-04 | FM-01, FM-02, FM-07, FM-09 | Correctness, Relevance, Consistency, Format Compliance | Conditional - vague judgment terms |
| QD-P-1.6.4 (P1) | AS-01, AS-06, AS-07 | FM-01, FM-02, FM-07, FM-09 | Consistency, Robustness, Boundary Recognition, Safety Response | Conditional - internal reasoning-method constraint |
| QD-P-1.6.6 (P1) | AS-01, AS-06, AS-07 | FM-01, FM-02, FM-07, FM-09 | Consistency, Robustness, Boundary Recognition, Safety Response | Conditional - unstated input-type precondition |
| QD-P-2.2.2 (P1) | AS-02, AS-07 | FM-01, FM-04 | Relevance, Robustness, Decomposition Capability, Boundary Recognition | Medium - unconstrained injected input format |
| QD-P-2.2.4 (P1) | AS-02, AS-07 | FM-01, FM-04 | Relevance, Robustness, Decomposition Capability, Boundary Recognition | Medium - missing-input path undefined |
| QD-P-2.3.4 (P0) | AS-03 | FM-06 | Completeness, Traceability, Format Compliance, Consistency | Medium - no privacy/sensitive-data output filtering |
| QD-P-2.5.2 (P0) | AS-01, AS-03, AS-04 | FM-08, FM-09, FM-10 | Boundary Recognition, Safety Response, Coherence | Medium - no security boundary constraints declared |
| QD-P-2.7.1 (P1) | AS-01, AS-05 | FM-01, FM-07, FM-09 | Correctness, Robustness, Consistency, Format Compliance | Conditional - positive example coverage insufficient |
| QD-P-2.7.2 (P1) | AS-01, AS-05 | FM-01, FM-07, FM-09 | Correctness, Robustness, Consistency, Format Compliance | Conditional - no counter-examples |
| QD-P-2.7.3 (P1) | AS-01, AS-05 | FM-01, FM-07, FM-09 | Correctness, Robustness, Consistency, Format Compliance | Conditional - no boundary-case examples |

Boundary reminders: candidate associations only ("may", "needs dynamic verification"); no causal claim is made. Single-defect mapping only (v1 scope); defect chains are out of scope.

## 8. Stage G - Self-Verification

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. All emitted QD-P / EX IDs were confirmed against the reference files; no fabricated IDs; no causal wording in Stage F; no "secure"/"high quality" claim; no "Permission = ERROR/BLOCKED" wording. No in-place self-corrections were required.

## 9. Status Board

Stage A (Single-artifact):  Executed - System Prompt L1 inspection (QC not applicable).
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.
Stage C (Gate-0):           Not passed - G0-4.
Stage D (Permission QD-PM): Not Executed - incomplete artifact set.
Stage E (Risk Explicit EX): Executed - 0 risk items (Explicit-P0=0, Explicit-P1=0, Explicit-P2=0).
Stage F (Impact outlook):   Executed - candidate mapping for 10 Stage A FAILs (advisory only).
Stage G (Self-verification): Executed - ID back-closure OK, red-line wording OK, output contract OK.
