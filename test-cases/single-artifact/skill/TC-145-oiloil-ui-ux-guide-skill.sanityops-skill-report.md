# SanityOps Inspect Lite - Skill Report

## Report header (provenance)

- Host model: unspecified (host model self-declaration not available in this environment)
- Skill package: sanityops-inspect-lite v1.0.0
- Specification baseline: SanityOps Framework v1.0 (September 2026)
- Non-official result: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
- Inspection date: 2026-10-14
- Artifact version: not supplied by the user (using the case's Collection Date as the working label)
- Artifact under inspection: TC-145-oiloil-ui-ux-guide-skill.md | Artifact type: Skill (SKILL.md)

## 1. Executive summary

- Stages executed: Stage A (Single-artifact Skill inspection + embedded-code QC), Stage C (Gate-0), Stage E (Risk Explicit), Stage F (Impact outlook, advisory only), Stage G (self-verification). Stage B and Stage D were Not Executed (structural reasons in the status board).
- Skill defect counts (QD-S): P0 = 3, P1 = 0, P2 = 0. Embedded-code QC: Not Applicable (no embedded code snippet).
- Gate-0 result: Not passed - G0-4 (no Tool Schema artifacts supplied, so the Tool field-completeness condition cannot be satisfied).
- Risk Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings (rule ID - one-line defect):
  1. QD-S-1.1 - no upper bound declared on the number or size of inputs (project files/config read).
  2. QD-S-1.3 - reads project files and opens a browser preview with no retry count, tool-invocation count, or timeout.
  3. QD-S-4.1 - no execution-failure behavior declared.
- Not run: Risk Implicit and the runtime Quality subsets were NOT run (Inspect PASS is not Risk PASS and not Quality PASS). The lite embedded-code QC is the only Quality check performed here.
- Upgrade pointer: for the complete ruleset use the open-source sanityops-cli, see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md.

Note on language: the artifact is bilingual; its front-matter description is in Chinese. All Chinese evidence below is rendered in English translation and marked "(translated)".

## 2. Stage A - Single-artifact Skill inspection (QD-S)

### 2.1 QD-S-0 Baseline Compliance (entry gate; 6 items)

QD-S-0.1 | PASS | evidence: TC-145, YAML front matter carries `name` and `description`.
QD-S-0.2 | PASS | evidence: TC-145, both fields carry non-empty content (the description is Chinese but populated).
QD-S-0.3 | PASS | evidence: TC-145, the YAML front matter parses (a double-quoted scalar holding CJK text).
QD-S-0.4 | PASS | evidence: TC-145, `name`/`description` are strings.
QD-S-0.5 | PASS | evidence: TC-145, no mutually contradictory declarations located.
QD-S-0.6 | PASS | evidence: TC-145, front matter + body present; minimum structure complete.

Baseline result: PASS on all six items. Proceeding to risk-level determination.

### 2.2 Skill risk level determination

Level: L2 (Medium Risk).
Basis: the `design` workflow reads the target project's code/config files (tailwind config, theme files, package.json) -> resource access, at least L2; no delete or irreversible operation is declared -> not L3.

### 2.3 Minimum rule set verdicts (L2 mandatory set)

QD-S-1.1 | FAIL | evidence: TC-145, "design mode - default". Excerpt (translated): "spend 30 seconds scanning the project ... look at actual font-sizes, radii, and spacing in two or three real UI files" - many project files are read with no upper bound on the number or size of inputs.
QD-S-1.3 | FAIL | evidence: TC-145, "design mode - Phase 4a". Excerpt (translated): "open the template ... and render 5 surfaces" - file reads and a browser preview are performed with no retry count, tool-invocation count, or timeout.
QD-S-2.1 | PASS | evidence: TC-145, "Operating principles". Excerpt (translated): "run the complete flow" - the wording "complete" is bounded by the defined Phases 0-5; no unbounded processing quantity is declared.
QD-S-2.2 | PASS | evidence: TC-145, no "keep trying / until success / ensure complete / persist until" wording was located.
QD-S-3.4 | PASS | evidence: TC-145, front matter description. Excerpt (translated): "when the user asks for a design system, a design spec, or a complete interface review use this skill; simple questions about a single color, font-size, or button size are answered directly" - an explicit out-of-scope (non_goals) routing is present.
QD-S-4.1 | FAIL | evidence: TC-145, whole body. No execution-failure handling is declared (the five-stage "maturity" classification handles input state, not execution failure).

### 2.4 Review Schema dimensions (six review dimensions)

IDENTITY (QD-S-3.4, QD-S-5.1): No defect - the description and mode table state what the Skill does and route trivial questions away.
TRIGGER (QD-S-3.1, QD-S-3.2): No defect at the L2 mandatory set; three modes with a default and a switch table are stated.
INPUT (QD-S-1.1, QD-S-3.3): Defect - no max_items / max size declared for the project files read.
EXECUTION (QD-S-1.3, QD-S-5.4): Defect - unbudgeted file reads and browser preview.
OUTPUT (QD-S-1.2, QD-S-2.3): No defect at the L2 mandatory set; explicit output artifacts are named (`design-spec.md`, `review-template.md`, preview HTML) (QD-S-1.2 is outside the L2 mandatory set).
FAILURE (QD-S-4.x): Defect - no failure behavior declared.

### 2.5 Defect list (sorted P0 first)

P0:
- QD-S-1.1 Input Boundary Missing - no upper bound on the number/size of project files read.
- QD-S-1.3 Execution Resource Boundary Missing - file reads / browser preview with no retry/timeout/call budget.
- QD-S-4.1 Undefined Failure Behavior - no execution-failure handling.

P1: none reported. P2: none reported.

### 2.6 QC - embedded code contract (QC-0 baseline first)

QC-0.1, QC-0.2, QC-0.3 | Not Applicable | the artifact contains no embedded code snippet (it is methodology prose, tables, and per-mode workflows).
QC-1.x, QC-2.x, QC-3.x | Not Applicable | no embedded code snippet exists in this artifact.

## 3. Stage B - Cross-artifact inspection

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.

## 4. Stage C - Gate-0 (admission to Permission)

- G0-1 (single-artifact inspection has no unfixed P0): NOT satisfied - Stage A records 3 unfixed P0 findings (informational; non-blocking in the lite flow).
- G0-2 (cross-artifact inspection has no unfixed P0): NOT verifiable - Stage B was not executed (informational).
- G0-3 (responsibility boundary statements exist and are locatable): Partially satisfied - the description states scope and excludes trivial questions, but no explicit responsibility statement is present; recorded.
- G0-4 (each Tool Schema `name`/`description`/parameter descriptions complete): NOT satisfied - no Tool Schema artifacts were supplied, so this condition cannot be met.

Gate-0 result: Not passed - G0-4 (no Tool Schema present to verify name/description/parameter completeness).

## 5. Stage D - Permission proportionality (QD-PM)

Not Executed - incomplete artifact set (a System Prompt + Skill + all Tool Schemas are required; only one Skill artifact was supplied).

## 6. Stage E - Risk Explicit audit (EX)

This section is a risk scan, physically separated from the Inspect verdicts above.

Findings: 0.
No risk expression matching an EX subcategory (NL-A / NL-B / NR-O / NR-S) was located in the static text (English content and English translations of the CJK content both checked): no data-exfiltration instruction, no encoded payload, no zero-width/homoglyph obfuscation, no dangerous config flag, no hardcoded credential or PII, and no reverse-constraint-removal wording. This section assesses only statically readable text; Risk Implicit (dynamic exploitability) was NOT run.

## 7. Stage F - Impact outlook (candidate mapping, advisory only)

Advisory context only - this is not a verdict and must not change, soften, or escalate any Inspect conclusion. Candidate language only; mapping strength is NOT severity. Risk Implicit and the runtime Quality subsets were NOT run; per relevance.md Sec.1.4, no assumption is made that compensating controls outside the artifacts are absent.

Impact Card: QD-S-1.1 | input boundary missing | P0
- Candidate Attack Surface: AS-06 Resource Exhaustion and Runaway Execution (candidate association).
- Candidate Failure Mode: FM-08, FM-10 (category-level).
- Candidate RAG-Agent metrics: Completeness, Timeliness, Robustness (candidate).
- Mapping strength: Medium (provisional, lite) - unbounded project scanning may expand processing; needs dynamic verification.

Impact Card: QD-S-1.3 | execution resource boundary missing | P0
- Candidate Attack Surface: AS-06 (candidate association).
- Candidate Failure Mode: FM-08, FM-10 (category-level).
- Candidate RAG-Agent metrics: Completeness, Timeliness, Robustness (candidate).
- Mapping strength: Medium (provisional, lite) - unbudgeted reads/preview may iterate; needs dynamic verification.

Impact Card: QD-S-4.1 | failure behavior undefined | P0
- Candidate Attack Surface: AS-07 Anomaly Propagation and Cascading Failures (candidate association).
- Candidate Failure Mode: FM-08, FM-09 (category-level).
- Candidate RAG-Agent metrics: Completeness, Coherence, Safety Response (candidate).
- Mapping strength: Conditional (provisional, lite) - undefined post-failure behavior may expand scope; needs dynamic verification.

## 8. Status board

Stage A (Single-artifact):  Executed - Skill (QD-S) minimum set + embedded-code QC (Not Applicable).
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.
Stage C (Gate-0):           Not passed - G0-4 (no Tool Schema present to verify name/description/parameter completeness).
Stage D (Permission QD-PM): Not Executed - incomplete artifact set.
Stage E (Risk Explicit EX): Executed - 0 findings.
Stage F (Impact outlook):   Executed - candidate mapping emitted (advisory).
Stage G (Self-verification): Executed - assembled report self-checked.

Self-verification: ID back-closure OK - red-line wording OK - output contract OK
