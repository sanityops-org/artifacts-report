# SanityOps Inspect Lite Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-14
Artifact version: not supplied by the user (using the case's Collection Date as the working label)

---

## 1. Executive summary (Sec. 6.1)

- Stages executed: A (single-artifact, System Prompt only), C (Gate-0), E (Risk Explicit), F (impact outlook), G (self-verification). Stage B did not run (fewer than two same-agent artifact types). Stage D did not run (incomplete artifact set).
- Finding counts (Stage A + B): Inspect P0 = 3, P1 = 7, P2 = 0.
- Gate-0 result: Not passed - G0-3 and G0-4 unsatisfied (no agent responsibility baseline; no Tool Schema).
- Risk-Explicit summary (Stage E): Explicit.P0 = 0, Explicit.P1 = 0, Explicit.P2 = 0.
- Top findings (rule ID - one-line defect):
  1. QD-P-2.2.1 - The template declares no input source.
  2. QD-P-2.3.4 / QD-P-2.5.2 - The template declares no privacy filtering and no security boundary.
  3. QD-P-2.3.1 / QD-P-2.3.2 - No output format or output schema is declared.
  4. QD-P-1.3.3 - No authorization/prohibition boundaries are declared.
  5. QD-P-2.7.1 / QD-P-2.7.2 / QD-P-2.7.3 - No examples of any kind are provided.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The lite embedded-code QC was run in Stage A.
- This report never states a security or quality conclusion; Inspect PASS is not Risk PASS and not Quality PASS.
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and version-level evidence chains, use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

---

## 2. Artifact inventory (input preparation, not a stage)

Case TC-040 is a personal-assistant suite (Leon). The case quotes only prompt/template scaffolding; the SDK and script blocks are comment stubs. Types present, by structural signature:

- System Prompt (present, partial): the "Create Skill Template" prompt (`# Create New Skill for Leon AI ... ## Goal`) and the "Create Tool Template" reference. Basis: prose/markdown instructions.
- Skill (absent): no markdown with `name`/`description` front matter is shown (the `skills/` tree is referenced only).
- Tool Schema (absent): the Node.js/Python SDK blocks are file-path comment stubs, not schemas. Basis: no `parameters` + `description` schema.
- Out of coverage: the actual SDK implementations, skill definitions and script bodies are not quoted.

---

## 3. Stage A - Single-artifact inspection

### 3.A.1 System Prompt set (Create Skill / Create Tool templates)

Tier determination: **L1 Single-turn Task**. Basis: the template drives a single skill/tool creation invocation; no tool invocations, no multi-turn dialogue, no complex reasoning shown. Scope = L1 (30 items).

- QD-P-1.1.1 | PASS | evidence: TC-040, template statements are mutually consistent.
- QD-P-1.1.2 | PASS | evidence: TC-040, no conflicting directives.
- QD-P-1.1.3 | PASS | evidence: TC-040, no example contradicting a rule.
- QD-P-1.2.1 | PASS | evidence: TC-040, the "developing Leon AI" role matches the creation task.
- QD-P-1.2.2 | PASS | evidence: TC-040, no style rule mismatch.
- QD-P-1.2.3 | PASS | evidence: TC-040, no constraint prohibits a declared responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-040, no quantifier-scope misuse found.
- QD-P-1.3.2 | PASS | evidence: TC-040, no vague qualifier carries a critical decision.
- QD-P-1.3.3 | FAIL | evidence: TC-040, the template declares no authorization/prohibition boundaries.
- QD-P-1.4.1 | PASS | evidence: TC-040, no duplicate constraint found.
- QD-P-1.4.2 | PASS | evidence: TC-040, declared branches are reachable.
- QD-P-1.5.1 | PASS | evidence: TC-040, the declared behaviour supports the creation objective.
- QD-P-1.6.1 | PASS | evidence: TC-040, no vague word carries a security/permission decision.
- QD-P-1.6.2 | PASS | evidence: TC-040, no rule keys on unobservable model internal state.
- QD-P-1.6.3 | PASS | evidence: TC-040, no unresolved implicit Soft-Rule conflict found.
- QD-P-1.6.4 | PASS | evidence: TC-040, no internal reasoning-method constraint found.
- QD-P-1.6.5 | PASS | evidence: TC-040, no self-referential/recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-040, no unstated-assumption dependency found.
- QD-P-1.6.7 | PASS | evidence: TC-040, no rule requires revising earlier conclusions on new information.
- QD-P-2.2.1 | FAIL | evidence: TC-040, the template declares no input source.
- QD-P-2.2.2 | PASS | evidence: TC-040, no structured input format is required (not triggered).
- QD-P-2.2.3 | PASS | evidence: TC-040, no parameterized input declared (not triggered).
- QD-P-2.2.4 | FAIL | evidence: TC-040, no missing-input handling is declared.
- QD-P-2.3.1 | FAIL | evidence: TC-040, no output format is declared.
- QD-P-2.3.2 | FAIL | evidence: TC-040, no output schema is declared.
- QD-P-2.3.4 | FAIL | evidence: TC-040, no sensitive-data filtering or privacy handling is declared.
- QD-P-2.5.2 | FAIL | evidence: TC-040, no prohibited operations or access boundaries are declared.
- QD-P-2.7.1 | FAIL | evidence: TC-040, no positive examples are provided (the "Goal" body is truncated with "...").
- QD-P-2.7.2 | FAIL | evidence: TC-040, no counter-examples are provided.
- QD-P-2.7.3 | FAIL | evidence: TC-040, no boundary-case examples are provided.

### 3.A.2 Embedded code snippets (QC)

The code blocks are template/Comment stubs.

- QC-0.1 | PASS | evidence: TC-040, the `markdown`/`typescript`/`python`/`javascript` snippets parse as valid text syntax.
- QC-0.2 | PASS | evidence: TC-040, snippets are fenced with language identifiers.
- QC-0.3 | FAIL | evidence: TC-040, the skill template body is truncated with "..." and the SDK/script blocks are comments only.
- QC-1.1 | N/A | evidence: TC-040, no name reference inside the shown snippets (determination basis: comments only).
- QC-1.2 | N/A | evidence: TC-040, no import statement present (determination basis: comments only).
- QC-1.3 | PASS | evidence: TC-040, no deprecated API usage present.
- QC-1.4 | N/A | evidence: TC-040, no typed function call present (determination basis: comments only).
- QC-2.1 | N/A | evidence: TC-040, no file-handle pattern in the shown code (determination basis: no such pattern).
- QC-2.2 | N/A | evidence: TC-040, no connection constructor opened without close (determination basis: no such pattern).
- QC-2.3 | N/A | evidence: TC-040, no high-risk file/network/DB call in the shown snippets (determination basis: no such pattern).
- QC-3.1 | N/A | evidence: TC-040, no import statement present (determination basis: no such pattern).
- QC-3.2 | PASS | evidence: TC-040, no referenced-but-unimported name in the snippets.
- QC-3.3 | PASS | evidence: TC-040, no hardcoded demo credential value present.

---

## 4. Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Not Executed - fewer than two same-agent artifact types present (only a partial System Prompt is present; no Skill or Tool Schema).

---

## 5. Stage C - Gate-0 (admission)

- G0-1 (no unfixed P0 in Stage A): NOT satisfied - recorded as an informational finding; does not gate this flow.
- G0-2 (no unfixed P0 in Stage B): NOT evaluated - Stage B was Not Executed.
- G0-3 (responsibility boundary statements exist and are locatable): NOT passed - the artifact is a skill-creation template with no agent responsibility baseline.
- G0-4 (each Tool Schema's `name`, `description`, parameter descriptions complete): NOT passed - no Tool Schema is present.

Gate-0 result: **Not passed - G0-3, G0-4**.

---

## 6. Stage D - Permission (QD-PM Quick Mode)

Subset: Inspect Permission Governance Specification (QD-PM)
Execution Status: Not Executed
Unsatisfied Conditions: G0-3, G0-4; incomplete artifact set
Blocking Reasons:
  G0-3 - no responsibility boundary statements are present in the artifact.
  G0-4 - no Tool Schema is present.
  Incomplete artifact set - no Skill or Tool Schema is present.
Remediation Actions: Fix the above upstream items, then re-run Gate-0.

(This is not a FAIL and not a permission conclusion.)

---

## 7. Stage E - Risk Explicit audit (EX) - physically separated from Inspect verdicts

Audit object: TC-040 System Prompt set.

Risk Item Summary:
- Total Risk Items: 0
- Explicit.P0 (Block release): 0 items
- Explicit.P1 (Fix / exemption): 0 items
- Explicit.P2 (Risk ledger): 0 items

No explicitly expressed risk text (NL-A / NL-B / NR-O / NR-S) was found in the shown artifacts.

Note: This is a static-document risk scan of explicitly declared text only; it is not a confirmed exploit and not a security conclusion. Risk Implicit (dynamic exploitability) was NOT run.

---

## 8. Stage F - Impact outlook (candidate mapping, advisory only)

Advisory context only; it does not change, soften, or escalate any Inspect conclusion. Strength is association confidence, NOT severity. Candidate language only. Risk Implicit and the runtime Quality subsets were NOT run; the lite embedded-code QC ran in Stage A. Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent.

| Defect (FAIL) | Candidate attack surface (AS-*) | Candidate failure modes (FM-*) | Strength (provisional, lite) |
|---|---|---|---|
| QD-P-1.3.3 | AS-01, AS-04 | FM-01, FM-02, FM-07, FM-09 | Conditional |
| QD-P-2.2.1, QD-P-2.2.4 | AS-01, AS-02 | FM-01, FM-04 | Medium |
| QD-P-2.3.1, QD-P-2.3.2 | AS-03, AS-09 | FM-06 | Conditional |
| QD-P-2.3.4, QD-P-2.5.2 | AS-01, AS-03, AS-04 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.7.1, QD-P-2.7.2, QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |
| QC-0.3 | (no AS-* row in Appendix A; snippet-level only) | (no B.1 group) | Not Applicable (out of Appendix A mapping scope) |

Candidate RAG-Agent quality metrics (candidate associations only; NOT a quality result): Correctness, Completeness, Format Compliance, Boundary Recognition. Defect chains (SC-*/QC-TA-*/QC-RA-*) are out of scope for lite v1.

---

## 9. Status board

Stage A (Single-artifact):  Executed - QD-P (L1), QC. No Skill or Tool Schema present.
Stage B (Cross):            Not Executed - fewer than two same-agent artifact types present.
Stage C (Gate-0):           Not passed - G0-3, G0-4.
Stage D (Permission QD-PM): Not Executed - incomplete artifact set (Gate-0 G0-3/G0-4 not satisfied).
Stage E (Risk Explicit EX): Executed - 0 findings.
Stage F (Impact outlook):   Executed - candidate mapping for all Stage A FAILs.
Stage G (Self-verification): Executed - ID back-closure, red-line wording, output contract checked.

---

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. No in-place self-corrections were required.
