# SanityOps Inspect-Lite Report - TC-019-deep-research-system-prompt.md

- Host model: unspecified (host model self-declaration not available in this environment)
- Skill package: sanityops-inspect-lite v1.0.0
- Specification baseline: SanityOps Framework v1.0 (September 2026)
- Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
- Inspection date: 2026-10-14
- Artifact version: not supplied by the user (using the case's Collection Date as the working label; Collection Date: 2026-10-12)

## 1. Executive Summary

- Executed stages: Stage A (single-artifact System Prompt inspection, QD-P, plus embedded-code QC on the TypeScript carrier), Stage C (Gate-0 admission check), Stage E (Risk Explicit), Stage F (Impact outlook), Stage G (self-verification).
- Inspect defect findings (Stage A): P0 = 3, P1 = 10, P2 = 1 (14 FAIL verdicts over 30 applicable L1 rules).
- Gate-0 result: Not passed - G0-4.
- Risk-Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 1 (1 explicitly declared risk item).
- Top findings (up to five, rule ID - one-line defect):
  - QD-P-2.2.1 - The input source is not declared at all.
  - QD-P-2.5.2 - No security boundary constraints are declared.
  - QD-P-2.3.4 - No security/privacy filtering mechanism is declared.
  - QD-P-2.3.1 - No output format is defined.
  - QD-P-1.6.1 - The vague term "news" carries a trust decision ("assume the user is right when presented with news").
- What was NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets; only the lite embedded-code QC ran inside Stage A.
- Upgrade pointer: for the full inspect ruleset plus Risk and Quality, use sanityops-cli - https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md
- This report states no security conclusion and no quality conclusion; Inspect PASS is not Risk PASS and is not Quality PASS.

## 2. Stage A - System Prompt Inspection (QD-P)

Artifact inventory: one file, classified as a System Prompt by structural signature (prose instructions returned by the `systemPrompt` function). The embedded TypeScript carrier is inspected under the lite embedded-code QC sub-check.

Tier determination: L1 (Single-turn Task). Basis: a single invocation produces the research response; the artifact declares no tool invocations, no multi-turn dialogue, and no complex multi-step workflow (2 or more of the L1 determination criteria are satisfied). The L1 tier item set (30 items) is applied.

Not applicable at L1 (marked "-" in the tier matrix, no verdict emitted): QD-P-1.4.3, QD-P-1.5.2, QD-P-2.1.1, QD-P-2.1.2, QD-P-2.1.3, QD-P-2.1.4, QD-P-2.3.3, QD-P-2.4.1, QD-P-2.4.2, QD-P-2.4.3, QD-P-2.5.1, QD-P-2.5.3, QD-P-2.5.4, QD-P-2.5.5, QD-P-2.6.1, QD-P-2.6.2, QD-P-2.6.3.

### Part 1 - Logic defects
- QD-P-1.1.1 | PASS | P0 | evidence: TC-019, instruction list; no mutually exclusive directives detected.
- QD-P-1.1.2 | PASS | P1 | evidence: TC-019; no competing MUST-directives without arbitration.
- QD-P-1.1.3 | PASS | P0 | evidence: TC-019; no example provided that could contradict a rule.
- QD-P-1.2.1 | PASS | P0 | evidence: TC-019, "You are an expert researcher."; role matches the responsibilities.
- QD-P-1.2.2 | PASS | P1 | evidence: TC-019; expert role and detailed expert output style are consistent.
- QD-P-1.2.3 | PASS | P0 | evidence: TC-019; no constraint prohibits the core responsibility.
- QD-P-1.3.1 | PASS | P1 | evidence: TC-019; "all subject matter" is a bounded scope statement, no misuse detected.
- QD-P-1.3.2 | FAIL | P1 | evidence: TC-019, instruction list; excerpt: "Be highly organized." / "Be proactive and anticipate my needs." / "be as detailed as possible" - undefined qualifiers set unstable output boundaries.
- QD-P-1.3.3 | PASS | P1 | evidence: TC-019; no authorization/handoff boundary applies to a single-turn research responder.
- QD-P-1.4.1 | FAIL | P2 | evidence: TC-019, instruction list; the detail requirement is duplicated - "be as detailed as possible and make sure your response is correct." and "Provide detailed explanations, I'm comfortable with lots of detail.".
- QD-P-1.4.2 | PASS | P2 | evidence: TC-019; no unreachable branch detected.
- QD-P-1.5.1 | PASS | P0 | evidence: TC-019; responsibilities support the research objective.
- QD-P-1.6.1 | FAIL | P1 | evidence: TC-019, instruction list; excerpt: "assume the user is right when presented with news." - the term "news" is undefined and carries a trust decision.
- QD-P-1.6.2 | PASS | P1 | evidence: TC-019; no rule keyed on unobservable internal state.
- QD-P-1.6.3 | PASS | P1 | evidence: TC-019; soft rules do not interweave into an unarbitrated conflict.
- QD-P-1.6.4 | PASS | P1 | evidence: TC-019; no reasoning-method constraint imposed.
- QD-P-1.6.5 | PASS | P1 | evidence: TC-019; no self-referential/recursive constraint.
- QD-P-1.6.6 | PASS | P1 | evidence: TC-019; no unstated precondition rule detected.
- QD-P-1.6.7 | PASS | P1 | evidence: TC-019; single-turn artifact, no knowledge-revision rule implicated.

### Part 2 - Completeness/security defects
- QD-P-2.2.1 | FAIL | P0 | evidence: TC-019; no input source, input data type, or acquisition method is declared anywhere in the prompt (absence confirmed).
- QD-P-2.2.2 | FAIL | P1 | evidence: TC-019; no input format, encoding, or size constraint declared (absence confirmed).
- QD-P-2.2.3 | FAIL | P1 | evidence: TC-019; required vs optional input is not distinguished (absence confirmed).
- QD-P-2.2.4 | FAIL | P1 | evidence: TC-019; no missing/empty-input handling declared (absence confirmed).
- QD-P-2.3.1 | FAIL | P1 | evidence: TC-019; no output format is defined (the prompt asks only for a detailed response; absence confirmed).
- QD-P-2.3.2 | FAIL | P1 | evidence: TC-019; no output schema (fields, structure, types) is defined (absence confirmed).
- QD-P-2.3.4 | FAIL | P0 | evidence: TC-019; no sensitive-data filtering, privacy handling, or security output constraint declared (absence confirmed).
- QD-P-2.5.2 | FAIL | P0 | evidence: TC-019; no prohibited operations, sensitive-data access boundary, or external access boundary declared (absence confirmed).
- QD-P-2.7.1 | FAIL | P1 | evidence: TC-019; no positive example is provided (absence confirmed).
- QD-P-2.7.2 | FAIL | P1 | evidence: TC-019; no counter-example is provided (absence confirmed).
- QD-P-2.7.3 | FAIL | P1 | evidence: TC-019; no boundary-case example is provided (absence confirmed).

### QC - embedded code (TypeScript carrier)
- QC-0.1 | PASS | P0 | evidence: TC-019, systemPrompt function parses as valid TypeScript.
- QC-0.2 | PASS | P1 | evidence: TC-019, code block labeled ```typescript.
- QC-0.3 | PASS | P1 | evidence: TC-019, arrow function is structurally complete (no truncation marker).
- QC-1.1 | PASS | P1 | evidence: TC-019; only the global Date is referenced, no undefined name.
- QC-1.2 | PASS | P2 | evidence: TC-019; no import statement, nothing invalid.
- QC-1.3 | PASS | P2 | evidence: TC-019; no deprecated API.
- QC-1.4 | PASS | P2 | evidence: TC-019; no type incompatibility.
- QC-2.1 | PASS | P1 | evidence: TC-019; no file handle opened.
- QC-2.2 | PASS | P2 | evidence: TC-019; no network connection opened.
- QC-2.3 | PASS | P2 | evidence: TC-019; no high-risk file/network/DB call.
- QC-3.1 | PASS | P2 | evidence: TC-019; no unused import.
- QC-3.2 | PASS | P1 | evidence: TC-019; no missing import.
- QC-3.3 | PASS | P2 | evidence: TC-019; no hardcoded demo credential/value.

Stage A summary: 30 applicable rules, 14 FAIL (3 P0, 10 P1, 1 P2). P0 findings are carried forward and do not halt the flow.

## 3. Stage B - Cross-Artifact Inspection

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available. No cross results are invented.

## 4. Stage C - Gate-0 (admission to Permission)

- G0-1 (no unfixed P0 in Stage A): informational only; 3 P0 findings recorded and carried forward (does not gate in this non-blocking flow).
- G0-2 (no unfixed P0 in Stage B): informational only; Stage B Not Executed.
- G0-3 (responsibility boundary statements exist and are locatable): the Prompt defines a role ("You are an expert researcher"), so a responsibility baseline is locatable.
- G0-4 (each Tool Schema's name, description, and parameter descriptions are complete): unsatisfiable - the artifact set contains no Tool Schema.

Gate-0 result: Not passed - G0-4 (no Tool Schema present, so per-Tool completion of name/description/parameter descriptions cannot be verified).

## 5. Stage D - Permission Proportionality (QD-PM)

Not Executed - incomplete artifact set (Precondition: full set Prompt + Skill + all Tool Schemas required; only a System Prompt is present).

## 6. Stage E - Risk Explicit (EX)

This section is a risk scan, physically separated from the Inspect verdicts above. It is not a defect verdict and not a security conclusion. Explicit-P0/P1/P2 is a Risk-Explicit assessment, not a confirmed runtime exploit.

Audit object: TC-019 System Prompt. Scan path: NL-A (sentence-by-sentence) -> NL-B (cross-sentence) -> NR-O (decode) -> NR-S (structure/field).

Risk Item Summary
- Total risk items: 1
- Explicit-P0 (Block release): 0 items
- Explicit-P1 (Fix / exemption): 0 items
- Explicit-P2 (Risk ledger): 1 item

Risk Item Details
- EX Classification: NL-A-7 (Reverse Constraint Removal)
- Risk Expression: "assume the user is right when presented with news." and "Value good arguments over authorities, the source is irrelevant."
- Severity Grade: Explicit-P2
- Reason: the two instructions explicitly remove a verification/sourcing constraint on a read-only research agent; the worst possible consequence stays within an existing read-only scope (quality of an informational answer), matching the P2 criterion "read-only, or within existing permission scope". Static text only.
- Impact Type Labels: D2
- Trigger Condition Label: unconditional (the user can supply such claims on their own).
- Disposition: Record in risk ledger.
- Remediation Suggestion: add a scope/verification boundary for user-supplied claims (restrict the constraint removal).

Note: Risk Implicit (dynamic exploitability) was NOT run. This is a static-document risk item, not a confirmed exploit.

## 7. Stage F - Impact Outlook (candidate mapping, advisory only)

Advisory context only; this section does not change, soften, or escalate any Inspect verdict. Candidate language only; strength is not severity. Risk Implicit and the runtime Quality subsets were NOT run; only Stage E (Risk Explicit) and the Stage A lite embedded-code QC ran. Per relevance.md section 1.4, no assumption is made that compensating controls outside the artifact are absent.

| Defect ID (severity) | Candidate AS-* | Candidate FM-* | Candidate RAG metrics | Strength (provisional lite) |
|---|---|---|---|---|
| QD-P-1.3.2 (P1) | AS-01, AS-04 | FM-08, FM-09, FM-10 | Boundary Recognition, Safety Response, Coherence | Conditional - undefined output-boundary qualifiers |
| QD-P-1.4.1 (P2) | AS-05, AS-09 | FM-01, FM-02, FM-07, FM-09 | Correctness, Relevance, Consistency, Format Compliance | Conditional - redundant constraint |
| QD-P-1.6.1 (P1) | AS-01, AS-04 | FM-01, FM-02, FM-07, FM-09 | Correctness, Relevance, Consistency, Format Compliance | Conditional - vague trust term |
| QD-P-2.2.1 (P0) | AS-01, AS-03 | FM-01, FM-04 | Relevance, Robustness, Decomposition Capability, Boundary Recognition | Strong - input source entirely undeclared |
| QD-P-2.2.2 (P1) | AS-02, AS-07 | FM-01, FM-04 | Relevance, Robustness, Decomposition Capability, Boundary Recognition | Medium - unconstrained input format |
| QD-P-2.2.3 (P1) | AS-02, AS-07 | FM-01, FM-04 | Relevance, Robustness, Decomposition Capability, Boundary Recognition | Conditional - required/optional not distinguished |
| QD-P-2.2.4 (P1) | AS-02, AS-07 | FM-01, FM-04 | Relevance, Robustness, Decomposition Capability, Boundary Recognition | Medium - missing-input path undefined |
| QD-P-2.3.1 (P1) | AS-03, AS-09 | FM-06 | Completeness, Traceability, Format Compliance, Consistency | Medium - no output format defined |
| QD-P-2.3.2 (P1) | AS-03, AS-09 | FM-06 | Completeness, Traceability, Format Compliance, Consistency | Conditional - no output schema |
| QD-P-2.3.4 (P0) | AS-03 | FM-06 | Completeness, Traceability, Format Compliance, Consistency | Medium - no privacy/sensitive-data output filtering |
| QD-P-2.5.2 (P0) | AS-01, AS-03, AS-04 | FM-08, FM-09, FM-10 | Boundary Recognition, Safety Response, Coherence | Medium - no security boundary constraints declared |
| QD-P-2.7.1 (P1) | AS-01, AS-05 | FM-01, FM-07, FM-09 | Correctness, Robustness, Consistency, Format Compliance | Conditional - no positive example |
| QD-P-2.7.2 (P1) | AS-01, AS-05 | FM-01, FM-07, FM-09 | Correctness, Robustness, Consistency, Format Compliance | Conditional - no counter-example |
| QD-P-2.7.3 (P1) | AS-01, AS-05 | FM-01, FM-07, FM-09 | Correctness, Robustness, Consistency, Format Compliance | Conditional - no boundary-case example |

Boundary reminders: candidate associations only ("may", "needs dynamic verification"); no causal claim is made. Single-defect mapping only (v1 scope); defect chains are out of scope.

## 8. Stage G - Self-Verification

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. All emitted QD-P / QC / EX IDs were confirmed against the reference files; no fabricated IDs; no causal wording in Stage F; no "secure"/"high quality" claim; no "Permission = ERROR/BLOCKED" wording. No in-place self-corrections were required.

## 9. Status Board

Stage A (Single-artifact):  Executed - System Prompt L1 inspection + embedded-code QC.
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.
Stage C (Gate-0):           Not passed - G0-4.
Stage D (Permission QD-PM): Not Executed - incomplete artifact set.
Stage E (Risk Explicit EX): Executed - 1 risk item (Explicit-P0=0, Explicit-P1=0, Explicit-P2=1).
Stage F (Impact outlook):   Executed - candidate mapping for 14 Stage A FAILs (advisory only).
Stage G (Self-verification): Executed - ID back-closure OK, red-line wording OK, output contract OK.
