# SanityOps Inspect Lite - Skill Report

## Report header (provenance)

- Host model: unspecified (host model self-declaration not available in this environment)
- Skill package: sanityops-inspect-lite v1.0.0
- Specification baseline: SanityOps Framework v1.0 (September 2026)
- Non-official result: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
- Inspection date: 2026-10-14
- Artifact version: not supplied by the user (using the case's Collection Date as the working label)
- Artifact under inspection: TC-081-claude-skills-contract-proposal-writer-skill.md | Artifact type: Skill (SKILL.md)

## 1. Executive summary

- Stages executed: Stage A (Single-artifact Skill inspection + embedded-code QC), Stage C (Gate-0), Stage E (Risk Explicit), Stage F (Impact outlook, advisory only), Stage G (self-verification). Stage B and Stage D were Not Executed (structural reasons in the status board).
- Skill defect counts (QD-S): P0 = 4, P1 = 0, P2 = 0. Embedded-code QC: 0 defects (QC-0 baseline PASS; QC-1..3 Not Applicable).
- Gate-0 result: Not passed - G0-4 (no Tool Schema artifacts supplied, so the Tool field-completeness condition cannot be satisfied).
- Risk Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings (rule ID - one-line defect):
  1. QD-S-3.4 - no non_goals / out-of-scope task declaration (the Skill never states what it must NOT do).
  2. QD-S-1.1 - no upper bound declared on the number or size of inputs.
  3. QD-S-1.3 - invokes the pandoc command chain but declares no retry count, tool-invocation count, or timeout.
  4. QD-S-4.1 - no execution-failure behavior declared (only missing-input handling).
- Not run: Risk Implicit and the runtime Quality subsets were NOT run (Inspect PASS is not Risk PASS and not Quality PASS). The lite embedded-code QC is the only Quality check performed here.
- Upgrade pointer: for the complete ruleset (full Inspect + Risk Explicit/Implicit + Quality, with remediation and version-level evidence chains) use the open-source sanityops-cli, see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md.

## 2. Stage A - Single-artifact Skill inspection (QD-S)

### 2.1 QD-S-0 Baseline Compliance (entry gate; 6 items)

QD-S-0.1 | PASS | evidence: TC-081, YAML front matter carries `name` and `description`.
QD-S-0.2 | PASS | evidence: TC-081, both fields carry non-empty content.
QD-S-0.3 | PASS | evidence: TC-081, the YAML front matter parses (double-quoted scalar values).
QD-S-0.4 | PASS | evidence: TC-081, `name`/`description` values are strings.
QD-S-0.5 | PASS | evidence: TC-081, no mutually contradictory declarations located.
QD-S-0.6 | PASS | evidence: TC-081, front matter + body present; minimum structure complete.

Baseline result: PASS on all six items. Proceeding to risk-level determination.

### 2.2 Skill risk level determination

Level: L2 (Medium Risk).
Basis: the Workflow writes DOCX output and invokes the `pandoc` command (a write operation / tool invocation) -> at least L2; no delete or irreversible operation is declared -> not L3.

### 2.3 Minimum rule set verdicts (L2 mandatory set)

QD-S-1.1 | FAIL | evidence: TC-081, "Workflow / 1. Gather Requirements". Excerpt: "Ask the user:" (8 intake questions; no upper bound on number or size of inputs is declared).
QD-S-1.3 | FAIL | evidence: TC-081, "Workflow / 4. Convert to DOCX". Excerpt: "pandoc contract.md -o contract.docx" (a tool invocation is declared, but no retry count, tool-invocation count, or timeout).
QD-S-2.1 | PASS | evidence: TC-081, "3. Generate & Fill". Excerpt: "Fill all [BRACKETED] placeholders." - "all" is bounded by the fixed template placeholders; no unbounded processing quantity is declared.
QD-S-2.2 | PASS | evidence: TC-081, no "keep trying / until success / ensure complete / persist until" wording was located.
QD-S-3.4 | FAIL | evidence: TC-081, whole body. Nearest limitation excerpt: "Not a substitute for legal counsel." No non_goals / out-of-scope task declaration exists (a legal disclaimer is not a task-scope exclusion).
QD-S-4.1 | FAIL | evidence: TC-081, "3. Generate & Fill". Excerpt: "Flag missing data as \"REQUIRED\"." - this handles missing input, not execution failure; no failure behavior is declared.

### 2.4 Review Schema dimensions (six review dimensions)

IDENTITY (QD-S-3.4, QD-S-5.1): Defect - no non_goals. "Core Capabilities" lists what it does; no explicit statement of what it does NOT do.
TRIGGER (QD-S-3.1, QD-S-3.2): No defect at the L2 mandatory set. "When to Use" is specific and the description enumerates trigger scenarios.
INPUT (QD-S-1.1, QD-S-3.3): Defect - no max_items / max size declared.
EXECUTION (QD-S-1.3, QD-S-5.4): Defect - no retry/timeout/tool-call budget despite the pandoc command chain.
OUTPUT (QD-S-1.2, QD-S-2.3): No defect at the L2 mandatory set; three templates plus an NDA/DPA block define output structure (QD-S-1.2 is outside the L2 mandatory set).
FAILURE (QD-S-4.x): Defect - no failure behavior declared.

### 2.5 Defect list (sorted P0 first)

P0:
- QD-S-1.1 Input Boundary Missing - no upper bound on input number/size.
- QD-S-1.3 Execution Resource Boundary Missing - pandoc/tool chain with no retry/timeout/call budget.
- QD-S-3.4 Undefined Task Scope - no non_goals declaration.
- QD-S-4.1 Undefined Failure Behavior - no execution-failure handling.

P1: none reported. P2: none reported.

### 2.6 QC - embedded code contract (QC-0 baseline first)

Embedded snippets: one fenced `bash` block under "Workflow / 4. Convert to DOCX" (pandoc conversion).
QC-0.1 | PASS | the snippet lines are valid shell commands.
QC-0.2 | PASS | a language identifier (`bash`) is present.
QC-0.3 | PASS | the snippet is complete for its purpose (no truncation, no missing imports).
QC-1.1, QC-1.2, QC-1.3, QC-1.4, QC-2.1, QC-2.2, QC-2.3, QC-3.1, QC-3.2, QC-3.3 | Not Applicable | the only embedded block is a shell/DOCX-conversion snippet; these sub-checks target Python/typed snippets. The remaining fenced blocks are Markdown contract templates, not code.

## 3. Stage B - Cross-artifact inspection

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.

## 4. Stage C - Gate-0 (admission to Permission)

- G0-1 (single-artifact inspection has no unfixed P0): NOT satisfied - Stage A records unfixed P0 findings (informational; non-blocking in the lite flow).
- G0-2 (cross-artifact inspection has no unfixed P0): NOT verifiable - Stage B was not executed (informational).
- G0-3 (responsibility boundary statements exist and are locatable): Partially satisfied - the Skill declares capabilities ("Core Capabilities") and audience ("When to Use"), but no explicit responsibility/out-of-scope statement; recorded.
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
- Mapping strength: Medium (provisional, lite) - an unbudgeted command chain may iterate; needs dynamic verification.

Impact Card: QD-S-3.4 | task scope not defined | P0
- Candidate Attack Surface: AS-01 Instruction and Context Boundary Confusion; AS-05 Tool Misuse and High-Risk Side Effects (candidate association).
- Candidate Failure Mode: FM-02, FM-07, FM-09 (category-level).
- Candidate RAG-Agent metrics: Relevance, Decomposition Capability, Boundary Recognition (candidate).
- Mapping strength: Conditional (provisional, lite) - scope expansion may occur under specific prompts; needs dynamic verification.

Impact Card: QD-S-4.1 | failure behavior undefined | P0
- Candidate Attack Surface: AS-07 Anomaly Propagation and Cascading Failures (candidate association).
- Candidate Failure Mode: FM-08, FM-09 (category-level).
- Candidate RAG-Agent metrics: Completeness, Coherence, Safety Response (candidate).
- Mapping strength: Medium (provisional, lite) - undefined post-failure behavior may expand scope; needs dynamic verification.

## 8. Status board

Stage A (Single-artifact):  Executed - Skill (QD-S) minimum set + embedded-code QC.
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.
Stage C (Gate-0):           Not passed - G0-4 (no Tool Schema present to verify name/description/parameter completeness).
Stage D (Permission QD-PM): Not Executed - incomplete artifact set.
Stage E (Risk Explicit EX): Executed - 0 findings.
Stage F (Impact outlook):   Executed - candidate mapping emitted (advisory).
Stage G (Self-verification): Executed - assembled report self-checked.

Self-verification: ID back-closure OK - red-line wording OK - output contract OK
