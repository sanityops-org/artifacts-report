# SanityOps Inspect Lite - Skill Report

## Report header (provenance)

- Host model: unspecified (host model self-declaration not available in this environment)
- Skill package: sanityops-inspect-lite v1.0.0
- Specification baseline: SanityOps Framework v1.0 (September 2026)
- Non-official result: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
- Inspection date: 2026-10-14
- Artifact version: not supplied by the user (using the case's Collection Date as the working label)
- Artifact under inspection: TC-139-claude-office-skills-resume-tailor-skill.md | Artifact type: Skill (SKILL.md)

## 1. Executive summary

- Stages executed: Stage A (QD-S-0 baseline only; the entry gate FAILED, so QD-S-1..QD-S-5 was stopped, and embedded-code QC was Not Applicable), Stage C (Gate-0), Stage E (Risk Explicit), Stage F (Impact outlook, advisory only), Stage G (self-verification). Stage B and Stage D were Not Executed (structural reasons in the status board).
- Skill defect counts (QD-S): 1 baseline defect (QD-S-0.2, gate-blocking); no QD-S-1..QD-S-5 verdicts were produced because the baseline gate failed. QC: Not Applicable (no embedded code snippet).
- Gate-0 result: Not passed - G0-4 (no Tool Schema artifacts supplied, so the Tool field-completeness condition cannot be satisfied).
- Risk Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings (rule ID - one-line defect):
  1. QD-S-0.2 - `description: ">"` is an unfinished YAML folded scalar; the trigger description is effectively empty.
- Not run: Risk Implicit and the runtime Quality subsets were NOT run (Inspect PASS is not Risk PASS and not Quality PASS). Risk-level determination was not reached (baseline gate failed).
- Upgrade pointer: for the complete ruleset use the open-source sanityops-cli, see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md.

## 2. Stage A - Single-artifact Skill inspection (QD-S)

### 2.1 QD-S-0 Baseline Compliance (entry gate; 6 items)

QD-S-0.1 | PASS | evidence: TC-139, YAML front matter carries required fields (`name`, `description`, `version`, etc.).
QD-S-0.2 | FAIL | evidence: TC-139, front matter. Excerpt: `description: ">"` - the value is the single character ">" (an unfinished folded-scalar marker); the field is present but effectively carries no description content.
QD-S-0.3 | PASS | evidence: TC-139, the YAML front matter parses (the quoted scalar ">" is syntactically valid).
QD-S-0.4 | PASS | evidence: TC-139, the field values match their expected types.
QD-S-0.5 | PASS | evidence: TC-139, no mutually contradictory declarations located.
QD-S-0.6 | PASS | evidence: TC-139, front matter + full body present; minimum structure complete.

Baseline result: FAIL (QD-S-0.2). Per the entry-gate rule, the Skill does NOT proceed to QD-S-1 through QD-S-5 inspection.

Remediation for QD-S-0.2: replace `description: ">"` with a real, populated description that states the trigger intent, for example `description: "Tailor a resume to a specific job description: map experience to requirements, optimize ATS keywords, and quantify achievements."`

### 2.2 Skill risk level determination

Not reached - the QD-S-0 baseline gate failed, so risk-level determination and the QD-S-1..QD-S-5 minimum set were stopped (source Sec.7.3.1).

### 2.3 Minimum rule set verdicts

Not Executed - QD-S-0 baseline failed (entry gate). No QD-S-1..QD-S-5 rule IDs are emitted.

### 2.4 Review Schema dimensions (six review dimensions)

Diagnostic notes only (no rule verdicts, because the baseline gate failed):
IDENTITY: The body states "What I can do" / "What I cannot do" - a capability boundary exists in the body but not in a machine-readable non_goals declaration.
TRIGGER: The intended trigger is inferable from the body but is NOT encoded in the front matter (the description is empty).
INPUT: No input bounds declared in the body.
EXECUTION: Declares MCP tool dependencies (`office-mcp`: extract PDF/DOCX text, create DOCX).
OUTPUT: A dedicated "Output Format" template exists.
FAILURE: A "Limitations" section exists but no structured failure-behavior declaration.

### 2.5 Defect list (sorted P0 first)

Gate-blocking baseline defect:
- QD-S-0.2 Field Content Non-Empty - `description: ">"` is effectively empty; the trigger description is absent.

(No QD-S-1..QD-S-5 defects were produced; the baseline gate stopped the checklist.)

### 2.6 QC - embedded code contract (QC-0 baseline first)

QC-0.1, QC-0.2, QC-0.3 | Not Applicable | the artifact contains no embedded code snippet; its fenced block is a Markdown output-format template, not code.
QC-1.x, QC-2.x, QC-3.x | Not Applicable | no embedded code snippet exists in this artifact.

## 3. Stage B - Cross-artifact inspection

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.

## 4. Stage C - Gate-0 (admission to Permission)

- G0-1 (single-artifact inspection has no unfixed P0): NOT satisfied - the Stage A entry gate failed (QD-S-0.2) (informational; non-blocking in the lite flow).
- G0-2 (cross-artifact inspection has no unfixed P0): NOT verifiable - Stage B was not executed (informational).
- G0-3 (responsibility boundary statements exist and are locatable): Partially satisfied - the body states "What I can do" / "What I cannot do", but the front matter carries no usable boundary statement; recorded.
- G0-4 (each Tool Schema `name`/`description`/parameter descriptions complete): NOT satisfied - no Tool Schema artifacts were supplied, so this condition cannot be met.

Gate-0 result: Not passed - G0-4 (no Tool Schema present to verify name/description/parameter completeness).

## 5. Stage D - Permission proportionality (QD-PM)

Not Executed - incomplete artifact set (a System Prompt + Skill + all Tool Schemas are required; only one Skill artifact was supplied).

## 6. Stage E - Risk Explicit audit (EX)

This section is a risk scan, physically separated from the Inspect verdicts above.

Findings: 0.
No risk expression matching an EX subcategory (NL-A / NL-B / NR-O / NR-S) was located in the static text. The empty `description` is an Inspect metadata defect, not a Risk-Explicit expression. This section assesses only statically readable text; Risk Implicit (dynamic exploitability) was NOT run.

## 7. Stage F - Impact outlook (candidate mapping, advisory only)

Advisory context only - this is not a verdict and must not change, soften, or escalate any Inspect conclusion. Candidate language only; mapping strength is NOT severity. Risk Implicit and the runtime Quality subsets were NOT run; per relevance.md Sec.1.4, no assumption is made that compensating controls outside the artifacts are absent.

Impact Card: QD-S-0.2 | required field effectively empty (metadata) | P0 (baseline, gate-blocking)
- Candidate Attack Surface: AS-09 Cross-Artifact Contract Breach (candidate association; a missing trigger description may confuse routing).
- Candidate Failure Mode: no category-level FM association is defined in Appendix B.1 for the QD-S-0.x family; recorded as a candidate only.
- Candidate RAG-Agent metrics: Relevance, Decomposition Capability, Boundary Recognition (candidate; treated under the trigger/scope grouping).
- Mapping strength: Medium (provisional, lite) - a missing trigger description may cause the Skill to load with no routing text; needs dynamic verification.

## 8. Status board

Stage A (Single-artifact):  Executed - QD-S-0 baseline failed (gate); QD-S-1..5 stopped; QC Not Applicable.
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.
Stage C (Gate-0):           Not passed - G0-4 (no Tool Schema present to verify name/description/parameter completeness).
Stage D (Permission QD-PM): Not Executed - incomplete artifact set.
Stage E (Risk Explicit EX): Executed - 0 findings.
Stage F (Impact outlook):   Executed - candidate mapping emitted (advisory).
Stage G (Self-verification): Executed - assembled report self-checked.

Self-verification: ID back-closure OK - red-line wording OK - output contract OK
