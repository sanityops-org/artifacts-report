# SanityOps Inspect Lite - Skill Report

## Report header (provenance)

- Host model: unspecified (host model self-declaration not available in this environment)
- Skill package: sanityops-inspect-lite v1.0.0
- Specification baseline: SanityOps Framework v1.0 (September 2026)
- Non-official result: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
- Inspection date: 2026-10-14
- Artifact version: not supplied by the user (using the case's Collection Date as the working label)
- Artifact under inspection: TC-138-marketingskills-content-strategy-skill.md | Artifact type: Skill (SKILL.md)

## 1. Executive summary

- Stages executed: Stage A (Single-artifact Skill inspection + embedded-code QC), Stage C (Gate-0), Stage E (Risk Explicit), Stage F (Impact outlook, advisory only), Stage G (self-verification). Stage B and Stage D were Not Executed (structural reasons in the status board).
- Skill defect counts (QD-S): P0 = 3, P1 = 0, P2 = 0. Embedded-code QC: 0 defects (QC Not Applicable - fenced blocks are directory-tree diagrams, not code).
- Gate-0 result: Not passed - G0-4 (no Tool Schema artifacts supplied, so the Tool field-completeness condition cannot be satisfied).
- Risk Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings (rule ID - one-line defect):
  1. QD-S-1.1 - no upper bound declared on the number or size of inputs (keyword exports, transcripts, survey data).
  2. QD-S-1.3 - uses web search but declares no retry count, tool-invocation count, or timeout.
  3. QD-S-4.1 - no execution-failure behavior declared.
- Not run: Risk Implicit and the runtime Quality subsets were NOT run (Inspect PASS is not Risk PASS and not Quality PASS). The lite embedded-code QC is the only Quality check performed here.
- Upgrade pointer: for the complete ruleset use the open-source sanityops-cli, see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md.

## 2. Stage A - Single-artifact Skill inspection (QD-S)

### 2.1 QD-S-0 Baseline Compliance (entry gate; 6 items)

QD-S-0.1 | PASS | evidence: TC-138, YAML front matter carries `name`, `description`, and `metadata`.
QD-S-0.2 | PASS | evidence: TC-138, both fields carry non-empty content (a long verbatim trigger list).
QD-S-0.3 | PASS | evidence: TC-138, the YAML front matter parses (plain and nested mappings).
QD-S-0.4 | PASS | evidence: TC-138, `name`/`description` are strings; `metadata.version` is a scalar.
QD-S-0.5 | PASS | evidence: TC-138, no mutually contradictory declarations located.
QD-S-0.6 | PASS | evidence: TC-138, front matter + body present; minimum structure complete.

Baseline result: PASS on all six items. Proceeding to risk-level determination.

### 2.2 Skill risk level determination

Level: L2 (Medium Risk).
Basis: the Skill instructs the use of web search and reads a project context file (`.agents/product-marketing.md`) -> external system access, at least L2; no delete or irreversible operation is declared -> not L3.

### 2.3 Minimum rule set verdicts (L2 mandatory set)

QD-S-1.1 | FAIL | evidence: TC-138, "Content Ideation Sources / 1. Keyword Data". Excerpt: "If user provides keyword exports (Ahrefs, SEMrush, GSC), analyze for:" (no upper bound on the number or size of inputs).
QD-S-1.3 | FAIL | evidence: TC-138, "Content Ideation Sources / 4. Forum Research". Excerpt: "Use web search to find content ideas" (a tool invocation is declared; no retry count, tool-invocation count, or timeout).
QD-S-2.1 | PASS | evidence: TC-138, "Treat Content Like a Product". Excerpt: "Every piece is its own launch." - "every piece" is a design principle, not an unbounded processing quantity; no "process all/every record" instruction is declared.
QD-S-2.2 | PASS | evidence: TC-138, no "keep trying / until success / ensure complete / persist until" wording was located.
QD-S-3.4 | PASS | evidence: TC-138, front matter description. Excerpt: "For writing individual pieces, see copywriting. For SEO-specific audits, see seo-audit." - an explicit out-of-scope routing (non_goals) is present.
QD-S-4.1 | FAIL | evidence: TC-138, whole body. No execution-failure handling is declared; "Check for product marketing context first" addresses input availability, not failure behavior.

### 2.4 Review Schema dimensions (six review dimensions)

IDENTITY (QD-S-3.4, QD-S-5.1): No defect - the description routes out-of-scope work to sibling skills (copywriting, seo-audit, social); scope boundary is stated.
TRIGGER (QD-S-3.1, QD-S-3.2): No defect at the L2 mandatory set; positive triggers are enumerated and negative/adjacent routing is explicit.
INPUT (QD-S-1.1, QD-S-3.3): Defect - no max_items / max size declared for keyword exports, transcripts, or survey data.
EXECUTION (QD-S-1.3, QD-S-5.4): Defect - web search is used with no retry/timeout/call budget.
OUTPUT (QD-S-1.2, QD-S-2.3): No defect at the L2 mandatory set; a concrete "Output Format" section is provided (QD-S-1.2 is outside the L2 mandatory set).
FAILURE (QD-S-4.x): Defect - no failure behavior declared.

### 2.5 Defect list (sorted P0 first)

P0:
- QD-S-1.1 Input Boundary Missing - no upper bound on input number/size.
- QD-S-1.3 Execution Resource Boundary Missing - web-search tool chain with no retry/timeout/call budget.
- QD-S-4.1 Undefined Failure Behavior - no execution-failure handling.

P1: none reported. P2: none reported.

### 2.6 QC - embedded code contract (QC-0 baseline first)

The artifact contains fenced blocks (three) used as directory-tree diagrams (hub/spoke and pillar structures) with no language identifier; the remaining blocks are Markdown tables.
QC-0.1, QC-0.2, QC-0.3 | Not Applicable | the fenced blocks are directory-tree diagrams, not code snippets; QC scope is code snippets only.
QC-1.x, QC-2.x, QC-3.x | Not Applicable | no embedded code snippet exists in this artifact.

## 3. Stage B - Cross-artifact inspection

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.

## 4. Stage C - Gate-0 (admission to Permission)

- G0-1 (single-artifact inspection has no unfixed P0): NOT satisfied - Stage A records unfixed P0 findings (informational; non-blocking in the lite flow).
- G0-2 (cross-artifact inspection has no unfixed P0): NOT verifiable - Stage B was not executed (informational).
- G0-3 (responsibility boundary statements exist and are locatable): Satisfied - the description and "Related Skills" section state scope and out-of-scope routing (locatable in the front matter description).
- G0-4 (each Tool Schema `name`/`description`/parameter descriptions complete): NOT satisfied - no Tool Schema artifacts were supplied, so this condition cannot be met.

Gate-0 result: Not passed - G0-4 (no Tool Schema present to verify name/description/parameter completeness).

## 5. Stage D - Permission proportionality (QD-PM)

Not Executed - incomplete artifact set (a System Prompt + Skill + all Tool Schemas are required; only one Skill artifact was supplied).

## 6. Stage E - Risk Explicit audit (EX)

This section is a risk scan, physically separated from the Inspect verdicts above.

Findings: 0.
No risk expression matching an EX subcategory (NL-A / NL-B / NR-O / NR-S) was located in the static text: no data-exfiltration instruction, no encoded payload, no zero-width/homoglyph obfuscation, no dangerous config flag, no hardcoded credential or PII, and no reverse-constraint-removal wording. This section assesses only statically readable text; Risk Implicit (dynamic exploitability) was NOT run.

## 7. Stage F - Impact outlook (candidate mapping, advisory only)

Advisory context only - this is not a verdict and must not change, soften, or escalate any Inspect conclusion. Candidate language only; mapping strength is NOT severity. Risk Implicit and the runtime Quality subsets were NOT run; per relevance.md Sec.1.4, no assumption is made that compensating controls outside the artifacts are absent.

Impact Card: QD-S-1.1 | input boundary missing | P0
- Candidate Attack Surface: AS-06 Resource Exhaustion and Runaway Execution (candidate association).
- Candidate Failure Mode: FM-08, FM-10 (category-level).
- Candidate RAG-Agent metrics: Completeness, Timeliness, Robustness (candidate).
- Mapping strength: Medium (provisional, lite) - unbounded intake may expand processing; needs dynamic verification.

Impact Card: QD-S-1.3 | execution resource boundary missing | P0
- Candidate Attack Surface: AS-06 (candidate association).
- Candidate Failure Mode: FM-08, FM-10 (category-level).
- Candidate RAG-Agent metrics: Completeness, Timeliness, Robustness (candidate).
- Mapping strength: Medium (provisional, lite) - unbudgeted search calls may iterate; needs dynamic verification.

Impact Card: QD-S-4.1 | failure behavior undefined | P0
- Candidate Attack Surface: AS-07 Anomaly Propagation and Cascading Failures (candidate association).
- Candidate Failure Mode: FM-08, FM-09 (category-level).
- Candidate RAG-Agent metrics: Completeness, Coherence, Safety Response (candidate).
- Mapping strength: Conditional (provisional, lite) - undefined post-failure behavior may expand scope; needs dynamic verification.

## 8. Status board

Stage A (Single-artifact):  Executed - Skill (QD-S) minimum set + embedded-code QC.
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.
Stage C (Gate-0):           Not passed - G0-4 (no Tool Schema present to verify name/description/parameter completeness).
Stage D (Permission QD-PM): Not Executed - incomplete artifact set.
Stage E (Risk Explicit EX): Executed - 0 findings.
Stage F (Impact outlook):   Executed - candidate mapping emitted (advisory).
Stage G (Self-verification): Executed - assembled report self-checked.

Self-verification: ID back-closure OK - red-line wording OK - output contract OK
