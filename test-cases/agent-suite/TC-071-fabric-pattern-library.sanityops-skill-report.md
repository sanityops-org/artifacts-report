# SanityOps Inspect Lite Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-15
Artifact version: not supplied by the user (using the case's Collection Date 2026-10-13 as the working label)

---

## 1. Executive summary (Sec. 6.1)

- Stages executed: A (single-artifact), C (Gate-0), E (Risk Explicit), F (impact outlook), G (self-verification). Stage B did not run (only one Logic Artifact type is present). Stage D did not run (Gate-0 G0-4 not satisfied / incomplete artifact set).
- Finding counts (Stage A, System Prompt set): Inspect P0 = 2, P1 = 8, P2 = 0.
- Gate-0 result: Not passed (G0-3 passed; G0-4 not satisfied - no Tool Schema artifact is present).
- Risk-Explicit summary (Stage E): Explicit.P0 = 0, Explicit.P1 = 0, Explicit.P2 = 0.
- Top findings (rule ID - one-line defect):
  1. QD-P-2.5.2 - No prohibited-operation, sensitive-data access, or external-access boundary is declared by any pattern.
  2. QD-P-2.3.4 - No sensitive-data filtering or privacy/security output constraint is declared.
  3. QD-P-2.2.2 / QD-P-2.2.3 / QD-P-2.2.4 - The input carried by the `INPUT:` marker has no declared format, no required/optional marking, and no empty-input handling.
  4. QD-P-1.3.2 - Vague qualifiers ("surprising, insightful, and/or interesting") carry the extraction/selection boundary.
  5. QD-P-2.7.1 / QD-P-2.7.2 / QD-P-2.7.3 - No positive, counter, or boundary-case example is provided.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The lite embedded-code QC was run in Stage A.
- This report never states a security or quality conclusion; Inspect PASS is not Risk PASS and not Quality PASS.
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and version-level evidence chains, use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

---

## 2. Artifact inventory (input preparation, not a stage)

Case TC-071 bundles one portable prompt-pattern library (Fabric). Artifact types present, by structural signature:

- System Prompt (present, 4 verbatim): the four `system.md` pattern prompts - `analyze_bill` (legislative analysis), `summarize` (content summarization), `extract_wisdom` (insight extraction) and `create_prd` (PRD generation). Basis: prose/markdown instruction bodies with `# IDENTITY`, `# STEPS`, `# OUTPUT`, `# INPUT` sections.
- Skill (absent): no markdown file with `name`/`description` front matter defines an invokable capability. The folder-name-as-invocation-name convention is a library design detail, not a Skill definition.
- Tool Schema (absent): no JSON Schema / function-calling definition (`parameters` + `description`) is present; the patterns invoke no tools.
- Embedded code snippets (QC scope): the fenced `markdown` blocks that carry the prompt bodies (no executable code).
- Out of coverage: the remaining hundreds of patterns and any `PATTERNS.md` manifest were not fetched; only the four patterns above are inspected.

Scope note: the four patterns are independent single-file artifacts of one library (each self-contained, composable via the OUTPUT/INPUT convention). All belong to the same artifact set; no artifact from another case is mixed in.

---

## 3. Stage A - Single-artifact inspection

### 3.A.1 System Prompt set (four Fabric patterns)

Tier determination: **L1 Single-turn Task**. Basis (any 2 or more of the L1 criteria): each pattern is completed by a single invocation with no state retention; no tool invocations; no multi-turn dialogue; no complex reasoning beyond the listed STEPS. L1 scope = 30 items.

- QD-P-1.1.1 | PASS | evidence: TC-071, all four patterns, no mutually exclusive attribute or directive found.
- QD-P-1.1.2 | PASS | evidence: TC-071, all four patterns, no conflicting directives within any declared scenario.
- QD-P-1.1.3 | PASS | evidence: TC-071, all four patterns, no worked example contradicts a rule (only output-section shapes are shown).
- QD-P-1.2.1 | PASS | evidence: TC-071, each persona (legislative analyst, content summarizer, insight extractor, PRD generator) matches its stated responsibility.
- QD-P-1.2.2 | PASS | evidence: TC-071, the persona voice matches the declared output style.
- QD-P-1.2.3 | PASS | evidence: TC-071, no constraint prohibits the core responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-071, quantities are bounded ("exactly 16 words", "20 to 50", "5-10 16-word bullets").
- QD-P-1.3.2 | FAIL | evidence: TC-071, extract_wisdom - "Extract 20 to 50 of the most surprising, insightful, and/or interesting ideas from the input" - vague qualifiers carry the extraction/selection boundary with no criteria.
- QD-P-1.3.3 | PASS | evidence: TC-071, a single-shot text pattern declares no authorization/prohibition/handoff scope and needs none (vacuous).
- QD-P-1.4.1 | PASS | evidence: TC-071, no duplicate constraint found.
- QD-P-1.4.2 | PASS | evidence: TC-071, every declared output section is reachable.
- QD-P-1.5.1 | PASS | evidence: TC-071, the responsibilities support the objective (produce the requested summary / extraction / PRD).
- QD-P-1.6.1 | PASS | evidence: TC-071, the vague words steer content selection rather than a security/permission boundary.
- QD-P-1.6.2 | PASS | evidence: TC-071, no rule keys on unreportable internal model state.
- QD-P-1.6.3 | PASS | evidence: TC-071, no soft rules are declared in mutual tension.
- QD-P-1.6.4 | FAIL | evidence: TC-071, summarize/extract_wisdom/create_prd - "Take a step back and think step-by-step about how to achieve the best possible results" - a fixed internal reasoning method the model cannot guarantee.
- QD-P-1.6.5 | PASS | evidence: TC-071, no self-referential or recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-071, no rule depends on an unstated assumption left without handling.
- QD-P-1.6.7 | PASS | evidence: TC-071, single-shot patterns declare no multi-turn update path (vacuous).
- QD-P-2.2.1 | PASS | evidence: TC-071, each pattern declares its input insertion point via the trailing `# INPUT` / `INPUT:` marker.
- QD-P-2.2.2 | FAIL | evidence: TC-071, no input data format, encoding or size limit is declared (each pattern terminates at "# INPUT\nINPUT:").
- QD-P-2.2.3 | FAIL | evidence: TC-071, no input field is marked required or optional.
- QD-P-2.2.4 | FAIL | evidence: TC-071, no behavior is declared when the input is empty or missing.
- QD-P-2.3.1 | PASS | evidence: TC-071, output format declared (all four patterns require Markdown output with named sections).
- QD-P-2.3.2 | PASS | evidence: TC-071, output fields are declared (section names plus word and item counts).
- QD-P-2.3.4 | FAIL | evidence: TC-071, no sensitive-data filtering, privacy handling, or security output constraint is declared by any pattern.
- QD-P-2.5.2 | FAIL | evidence: TC-071, no prohibited operation, sensitive-data access boundary, or external-access boundary is declared.
- QD-P-2.7.1 | FAIL | evidence: TC-071, no positive worked example is provided (only output-section shapes are shown).
- QD-P-2.7.2 | FAIL | evidence: TC-071, no counter-examples are provided.
- QD-P-2.7.3 | FAIL | evidence: TC-071, no boundary-case examples are provided.

### 3.A.2 Skill

- QD-S-1.x .. QD-S-5.x | N/A | evidence: TC-071 carries no Skill artifact (determination basis: no markdown file with `name`/`description` front matter defines an invokable capability). No QD-S verdict is emitted.

### 3.A.3 Tool Schema

- QD-T-1.x .. QD-T-4.x | N/A | evidence: TC-071 carries no Tool Schema artifact (determination basis: the patterns invoke no tools and no JSON `parameters` schema is shown). No QD-T verdict is emitted.

### 3.A.4 Embedded code snippets (QC)

QC-0 baseline: the fenced blocks carry Markdown prompt text, not executable code, so QC-1 through QC-4 do not apply.

- QC-0.1 | PASS | evidence: TC-071, the fenced blocks contain prompt text that parses as the declared Markdown.
- QC-0.2 | PASS | evidence: TC-071, each block is fenced with `markdown`.
- QC-0.3 | PASS | evidence: TC-071, each prompt block is structurally complete (IDENTITY through INPUT).
- QC-0.4 | PASS | evidence: TC-071, the code fences open and close correctly.
- QC-0.5 | PASS | evidence: TC-071, the declared language (`markdown`) matches the content.
- QC-1.1 .. QC-4.2 | N/A | evidence: TC-071, no executable code is present (determination basis: the fenced blocks are prompt text only).

---

## 4. Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Stage status: **Not Executed**. Reason: only one Logic Artifact type (System Prompt) is present; no Prompt/Skill/Tool pair exists, so QD-PS (Prompt -> Skill), QD-PT (Prompt -> Tool), QD-ST (Skill <-> Tool), and QD-CYC-1.1 have no counterpart artifact and are Not Applicable.

Informational observation (not a Stage B verdict line): QD-CYC-1.2 (Multi-Agent Circular Invocation) does not apply at L1; the four patterns are independent single-file prompts with no orchestration, so no closed loop was found.

---

## 5. Stage C - Gate-0 (admission)

- G0-1 (no unfixed P0 in Stage A): NOT satisfied - recorded as an informational finding; does not gate this flow.
- G0-2 (no unfixed P0 in Stage B): N/A - Stage B did not run; recorded as informational.
- G0-3 (responsibility boundary statements exist and are locatable): Passed - each pattern states its role and scope (e.g. summarize "You are an expert content summarizer."; create_prd "You are a Product Requirements Document (PRD) Generator.").
- G0-4 (each Tool Schema's `name`, `description`, parameter descriptions complete): NOT passed - no Tool Schema artifact is present.

Gate-0 result: **Not passed - G0-4**.

---

## 6. Stage D - Permission (QD-PM Quick Mode)

Subset: Inspect Permission Governance Specification (QD-PM)
Execution Status: Not Executed
Unsatisfied Conditions: G0-4 (structural admission); additionally the full artifact set is incomplete (no Skill, no Tool Schema).
Blocking Reasons:
  G0-4 - Tool Schema `name`/`description`/parameter descriptions are not complete (no Tool Schema artifact is present).
  Artifact-set precondition - the full set (Prompt + Skill + all Tool Schemas) is not present.
Remediation Actions: Fix the above upstream items, then re-run Gate-0.

(The Permission stage was "Not Executed"; this is not a FAIL and not a permission conclusion.)

---

## 7. Stage E - Risk Explicit audit (EX) - physically separated from Inspect verdicts

Audit object: TC-071 System Prompt set (four patterns) + embedded Markdown blocks.
Three-phase scan (NL-A -> NL-B -> NR-O -> NR-S) run over the bundled artifacts.

Risk Item Summary:
- Total Risk Items: 0
- Explicit.P0 (Block release): 0 items
- Explicit.P1 (Fix / exemption): 0 items
- Explicit.P2 (Risk ledger): 0 items

Note: no explicitly declared risk expression (self-contained exfiltration, identity/permission claim, constraint removal, priority override, dangerous flag, hardcoded credential/PII, or abnormal callback) was found in the static artifact text. The `analyze_bill` persona flourish ("a 3,129 IQ") and the stylistic "think step by step" lines are behavioural/style content, not risk expressions matching a defined EX subcategory. This is a static-document scan only; it is not a security conclusion. Risk Implicit (dynamic exploitability) was NOT run.

---

## 8. Stage F - Impact outlook (candidate mapping, advisory only)

Advisory context only; it does not change, soften, or escalate any Inspect conclusion. Strength is association confidence, NOT severity. Candidate language only. Risk Implicit and the runtime Quality subsets were NOT run; the lite embedded-code QC ran in Stage A. Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent.

| Defect (FAIL) | Candidate attack surface (AS-*) | Candidate failure modes (FM-*) | Strength (provisional, lite) |
|---|---|---|---|
| QD-P-1.3.2 | AS-01, AS-04 | FM-01, FM-02, FM-07, FM-09 | Conditional (qualitative selection boundary may drift) |
| QD-P-1.6.4 | AS-01, AS-06, AS-07 | FM-01, FM-02, FM-07, FM-09 | Conditional |
| QD-P-2.2.2, QD-P-2.2.3, QD-P-2.2.4 | AS-02, AS-07 | FM-01, FM-04 | Medium (input format/necessity/missing handling undeclared) |
| QD-P-2.3.4 | AS-03 | FM-06 | Conditional |
| QD-P-2.5.2 | AS-01, AS-03, AS-04 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.7.1, QD-P-2.7.2, QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |

Candidate RAG-Agent quality metrics (candidate associations only; NOT a quality result): Correctness, Consistency, Robustness, Format Compliance, Boundary Recognition, Safety Response. Defect chains (SC-*/QC-TA-*/QC-RA-*) are out of scope for lite v1.

---

## 9. Status board

Stage A (Single-artifact):  Executed - QD-P (L1, 4 patterns), QD-T (N/A, no Tool Schema), QD-S (N/A, no Skill), QC (embedded Markdown blocks).
Stage B (Cross):            Not Executed - only one artifact type present (System Prompt); no Prompt/Skill/Tool pair exists.
Stage C (Gate-0):           Not passed - G0-4 (G0-1/G0-2 informational).
Stage D (Permission QD-PM): Not Executed - Gate-0 G0-4 not satisfied; full artifact set incomplete (no Skill, no Tool Schema).
Stage E (Risk Explicit EX): Executed - 0 findings.
Stage F (Impact outlook):   Executed - candidate mapping for all Stage A FAILs.
Stage G (Self-verification): Executed - ID back-closure, red-line wording, output contract checked.

---

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. No in-place self-corrections were required.
