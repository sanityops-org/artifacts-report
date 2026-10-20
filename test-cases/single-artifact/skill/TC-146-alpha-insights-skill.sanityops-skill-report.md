# SanityOps Inspect Lite - Skill Report

## Report header (provenance)

- Host model: unspecified (host model self-declaration not available in this environment)
- Skill package: sanityops-inspect-lite v1.0.0
- Specification baseline: SanityOps Framework v1.0 (September 2026)
- Non-official result: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
- Inspection date: 2026-10-14
- Artifact version: not supplied by the user (using the case's Collection Date as the working label)
- Artifact under inspection: TC-146-alpha-insights-skill.md | Artifact type: Skill (SKILL.md)

## 1. Executive summary

- Stages executed: Stage A (Single-artifact Skill inspection + embedded-code QC), Stage C (Gate-0), Stage E (Risk Explicit), Stage F (Impact outlook, advisory only), Stage G (self-verification). Stage B and Stage D were Not Executed (structural reasons in the status board).
- Skill defect counts (QD-S): P0 = 4, P1 = 0, P2 = 0. Embedded-code QC: 2 defects (QC-2.1 P1 unclosed file handle; QC-2.3 P2 missing exception handling).
- Gate-0 result: Not passed - G0-4 (no Tool Schema artifacts supplied, so the Tool field-completeness condition cannot be satisfied).
- Risk Explicit summary: Explicit-P0 = 0, Explicit-P1 = 0, Explicit-P2 = 0.
- Top findings (rule ID - one-line defect):
  1. QD-S-2.1 - unbounded quantity declaration ("ALL downstream nodes must be incrementally updated").
  2. QD-S-1.1 - no upper bound declared on the number or size of inputs.
  3. QD-S-1.3 - runs scripts, hooks, and Subagents with no retry count, tool-invocation count, or execution budget.
  4. QD-S-3.4 - no non_goals declaration (no out-of-scope task exclusion).
- Not run: Risk Implicit and the runtime Quality subsets were NOT run (Inspect PASS is not Risk PASS and not Quality PASS). The lite embedded-code QC is the only Quality check performed here.
- Upgrade pointer: for the complete ruleset use the open-source sanityops-cli, see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md.

Note on language: the artifact's top-level orchestration file is English; internal referenced files are Chinese. All quoted evidence below is English (ASCII) text from the artifact.

## 2. Stage A - Single-artifact Skill inspection (QD-S)

### 2.1 QD-S-0 Baseline Compliance (entry gate; 6 items)

QD-S-0.1 | PASS | evidence: TC-146, YAML front matter carries `name`, `description`, `effort`, `license`, `metadata`, and `hooks`.
QD-S-0.2 | PASS | evidence: TC-146, all required fields carry non-empty content.
QD-S-0.3 | PASS | evidence: TC-146, the YAML front matter parses (nested `hooks` list/mapping).
QD-S-0.4 | PASS | evidence: TC-146, field values match expected types.
QD-S-0.5 | PASS | evidence: TC-146, no mutually contradictory declarations located.
QD-S-0.6 | PASS | evidence: TC-146, front matter + body present; minimum structure complete.

Baseline result: PASS on all six items. Proceeding to risk-level determination.

### 2.2 Skill risk level determination

Level: L2 (Medium Risk).
Basis: the Skill writes deliverables to a workspace directory and executes local scripts/hooks (Bash/Python, Subagents) -> write operations and script execution, at least L2; no delete or irreversible external operation is declared -> not L3.

### 2.3 Minimum rule set verdicts (L2 mandatory set)

QD-S-1.1 | FAIL | evidence: TC-146, "Stage 1: Briefing". Excerpt: "**Interactive Clarification**: Use AskUserQuestion" with no declared cap on the amount of user input consumed (no upper bound on the number or size of inputs).
QD-S-1.3 | FAIL | evidence: TC-146, front matter `hooks`. Excerpt: "timeout: 3" / "timeout: 10" / "timeout: 5" - only per-hook timeouts are declared; the Skill declares no retry count, tool-invocation count, or overall execution budget for its research/track execution.
QD-S-2.1 | FAIL | evidence: TC-146, "Change Cascade Rule". Excerpt: "**At ANY Stage, when modifying a completed upstream deliverable, ALL downstream nodes must be incrementally updated.**" - unbounded "ALL" without a corresponding quantity limit.
QD-S-2.2 | PASS | evidence: TC-146, no "keep trying / until success / ensure complete / persist until" wording was located.
QD-S-3.4 | FAIL | evidence: TC-146, front matter description and body. The description enumerates ten research scenarios (what it does) but declares no non_goals / out-of-scope task exclusion; the "Self-Containment Principle" forbids external Skills but does not constrain task scope.
QD-S-4.1 | PASS | evidence: TC-146, "Failure Handling" and "Edge Case Handling". Excerpt: "| Tool failure | Fall back by priority: search engine -> web scraping -> direct URL; inform user when all tools unavailable |" - failure behavior is declared.

### 2.4 Review Schema dimensions (six review dimensions)

IDENTITY (QD-S-3.4, QD-S-5.1): Defect - no non_goals; the scenario list is broad with no task-scope exclusion.
TRIGGER (QD-S-3.1, QD-S-3.2): No defect at the L2 mandatory set; the description enumerates ten scenarios and a fixed opening statement.
INPUT (QD-S-1.1, QD-S-3.3): Defect - no max_items / max size declared.
EXECUTION (QD-S-1.3, QD-S-5.4): Defect - script/hook/Subagent execution with no execution budget (hook timeouts only).
OUTPUT (QD-S-1.2, QD-S-2.3): Defect - unbounded cascade ("ALL downstream nodes") is declared via QD-S-2.1 (QD-S-1.2 is outside the L2 mandatory set).
FAILURE (QD-S-4.x): No defect - a Failure Handling and Edge Case Handling section exists.

### 2.5 Defect list (sorted P0 first)

P0:
- QD-S-1.1 Input Boundary Missing - no upper bound on input number/size.
- QD-S-1.3 Execution Resource Boundary Missing - script/hook execution with no retry/tool-call/execution budget.
- QD-S-2.1 Unbounded Quantity Declaration - "ALL downstream nodes must be incrementally updated".
- QD-S-3.4 Undefined Task Scope - no non_goals declaration.

P1: none reported. P2: none reported.

### 2.6 QC - embedded code contract (QC-0 baseline first)

Embedded snippets: several fenced `bash` blocks and `python` blocks (state-manager invocations and ReportBuilder steps).
QC-0.1 | PASS | the bash/python snippets parse as valid syntax for their declared languages.
QC-0.2 | PASS | language identifiers (`bash`, `python`) are present.
QC-0.3 | PASS | the snippets are complete for their purpose.
QC-1.1 | PASS | `ReportBuilder`/`build_report` are provided by the Skill (`scripts/report_helper`) after `sys.path.insert(0, 'scripts')`.
QC-1.2 | PASS | `from report_helper import ReportBuilder` resolves to a declared Skill dependency (not an undeclared module).
QC-1.3, QC-1.4 | Not Applicable | no deprecated API or type mismatch located in the snippets.
QC-2.1 | FAIL | evidence: TC-146, "Stage Transition Protocol". Excerpt: `json.load(open('{ws}/_state.json'))` - a file is opened without `with` or a corresponding `close()` (P1).
QC-2.2 | Not Applicable | no network/socket connection is opened in the snippets.
QC-2.3 | FAIL | evidence: TC-146, "Stage Transition Protocol". Excerpt: `json.load(open('{ws}/_state.json'))` - a file read is performed without try/except handling (P2).
QC-3.1 | PASS | evidence: TC-146, `import sys, os; sys.path.insert(...)` - both imports are referenced.
QC-3.2 | PASS | no referenced-but-unimported module was located.
QC-3.3 | PASS | no demo/hardcoded credential value was located (the `dk = "dat" + "a"` workaround is not a credential).

## 3. Stage B - Cross-artifact inspection

Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.

## 4. Stage C - Gate-0 (admission to Permission)

- G0-1 (single-artifact inspection has no unfixed P0): NOT satisfied - Stage A records 4 unfixed P0 findings (informational; non-blocking in the lite flow).
- G0-2 (cross-artifact inspection has no unfixed P0): NOT verifiable - Stage B was not executed (informational).
- G0-3 (responsibility boundary statements exist and are locatable): Partially satisfied - the description, opening statement, and "Core Behavioral Rules" state the Skill's role and constraints, but no explicit out-of-scope/responsibility statement exists; recorded.
- G0-4 (each Tool Schema `name`/`description`/parameter descriptions complete): NOT satisfied - no Tool Schema artifacts were supplied, so this condition cannot be met.

Gate-0 result: Not passed - G0-4 (no Tool Schema present to verify name/description/parameter completeness).

## 5. Stage D - Permission proportionality (QD-PM)

Not Executed - incomplete artifact set (a System Prompt + Skill + all Tool Schemas are required; only one Skill artifact was supplied).

## 6. Stage E - Risk Explicit audit (EX)

This section is a risk scan, physically separated from the Inspect verdicts above.

Findings: 0.
No risk expression matching an EX subcategory (NL-A / NL-B / NR-O / NR-S) was located in the static text: no data-exfiltration instruction, no encoded payload, no zero-width/homoglyph obfuscation, no dangerous config flag, no hardcoded credential or PII (hook paths use `${CLAUDE_PLUGIN_ROOT}`/`${CLAUDE_SKILL_DIR}` variables), and no reverse-constraint-removal wording. The Skill states constraints (self-containment, workspace-path prohibition) rather than removing them. This section assesses only statically readable text; Risk Implicit (dynamic exploitability) was NOT run.

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
- Mapping strength: Medium (provisional, lite) - unbudgeted script/hook execution may iterate; needs dynamic verification.

Impact Card: QD-S-2.1 | unbounded quantity declaration | P0
- Candidate Attack Surface: AS-06, AS-07 (candidate association).
- Candidate Failure Mode: FM-08, FM-10 (category-level).
- Candidate RAG-Agent metrics: Completeness, Timeliness, Robustness (candidate).
- Mapping strength: Medium (provisional, lite) - "ALL downstream nodes" cascade may widen work per iteration; needs dynamic verification.

Impact Card: QD-S-3.4 | task scope not defined | P0
- Candidate Attack Surface: AS-01 Instruction and Context Boundary Confusion; AS-05 Tool Misuse and High-Risk Side Effects (candidate association).
- Candidate Failure Mode: FM-02, FM-07, FM-09 (category-level).
- Candidate RAG-Agent metrics: Relevance, Decomposition Capability, Boundary Recognition (candidate).
- Mapping strength: Conditional (provisional, lite) - scope expansion may occur under specific prompts; needs dynamic verification.

Impact Card: QC-2.1 / QC-2.3 | unclosed file handle / missing exception handling | P1 / P2
- Candidate Attack Surface: AS-07 Anomaly Propagation and Cascading Failures (candidate association).
- Candidate Failure Mode: FM-03, FM-04, FM-05 (category-level; Tool structure and parameter defects group).
- Candidate RAG-Agent metrics: Correctness, Traceability, Timeliness (candidate).
- Mapping strength: Conditional (provisional, lite) - a resource/exception gap may surface at runtime; needs dynamic verification.

## 8. Status board

Stage A (Single-artifact):  Executed - Skill (QD-S) minimum set + embedded-code QC.
Stage B (Cross):            Not Executed - single artifact; no Prompt+Skill+Tool set from the same agent available.
Stage C (Gate-0):           Not passed - G0-4 (no Tool Schema present to verify name/description/parameter completeness).
Stage D (Permission QD-PM): Not Executed - incomplete artifact set.
Stage E (Risk Explicit EX): Executed - 0 findings.
Stage F (Impact outlook):   Executed - candidate mapping emitted (advisory).
Stage G (Self-verification): Executed - assembled report self-checked.

Self-verification: ID back-closure OK - red-line wording OK - output contract OK
