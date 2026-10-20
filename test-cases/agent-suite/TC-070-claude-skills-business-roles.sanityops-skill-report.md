# SanityOps Inspect Lite Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-15
Artifact version: not supplied by the user (using the case's Collection Date 2026-10-13 as the working label)

---

## 1. Executive summary (Sec. 6.1)

- Stages executed: A (single-artifact), B (cross-artifact), C (Gate-0), E (Risk Explicit), F (impact outlook), G (self-verification). Stage D did not run (Gate-0 G0-4 not satisfied / incomplete artifact set).
- Finding counts (Stage A): Inspect P0 = 16, P1 = 1, P2 = 0 (System Prompt set `cs-financial-analyst` + `cs-ceo-advisor`: 13 P0; Skill `contract-and-proposal-writer`: 3 P0 + 1 P1). Stage B: P0 = 1.
- Gate-0 result: Not passed (G0-3 passed; G0-4 not satisfied - no Tool Schema artifact is present).
- Risk-Explicit summary (Stage E): Explicit.P0 = 0, Explicit.P1 = 0, Explicit.P2 = 0.
- Top findings (rule ID - one-line defect):
  1. QD-PS-1.1 - Skill Authorization Consistency: the `contract-and-proposal-writer` Skill is defined but is outside the authorization scope of the two inspected agent prompts.
  2. QD-P-2.4.3 / QD-P-2.5.3 - The agent prompts name backing scripts and grant `Bash`/`Write` with no invocation specification and no permission-control boundary.
  3. QD-P-2.2.2 / QD-P-2.2.3 / QD-P-2.2.4 - The user-supplied financial inputs have no declared format, required/optional marking, or missing-input handling.
  4. QD-S-1.1 / QD-S-1.3 / QD-S-2.1 - The contract skill declares no input boundary, no execution resource boundary (it runs `pandoc`), and uses unbounded wording ("Fill all [BRACKETED] placeholders").
  5. QD-P-2.3.4 / QD-P-2.5.2 - No sensitive-data filtering and no security boundary constraint are declared.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The lite embedded-code QC was run in Stage A (a `bash` pandoc snippet was present).
- This report never states a security or quality conclusion; Inspect PASS is not Risk PASS and not Quality PASS.
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and version-level evidence chains, use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

---

## 2. Artifact inventory (input preparation, not a stage)

Case TC-070 bundles one role-based business/executive agent library (claude-skills). Artifact types present, by structural signature:

- System Prompt (present, 2): `agents/finance/cs-financial-analyst.md` and `agents/c-level/cs-ceo-advisor.md`, role/agent definitions (front matter with `name`/`description`/`domain`/`skills`/`model`/`tools` plus role, workflows and success metrics). Classification basis: they are role/orchestration agent definitions (prose role instructions that declare skills, tools and workflows), so they are treated as System Prompts rather than capability Skills; an alternative reading (front matter -> Skill) is noted and does not change the cross-artifact result.
- Skill (present, 1): `business-growth/skills/contract-and-proposal-writer/SKILL.md`, markdown with `name`/`description` front matter plus tier/category/workflow/templates/pitfalls. Basis: the SKILL.md front-matter signature.
- Tool Schema (absent): the agents name tools by name only (`tools: [Read, Write, Bash, Grep, Glob]`) and reference backing scripts by path; no JSON `parameters`/`inputSchema` is present. Basis: no schema object.
- Embedded code snippets (QC scope): a `bash` code block in the contract skill (`pandoc ...` conversion commands).
- Out of coverage: the referenced skill packages, scripts and references (e.g. `dcf_valuation.py`, `ceo-advisor` scripts, `financial-analyst` references) were not fetched and are not quoted. The ceo-advisor body is an abridged transcription in the case file (front matter and headings verbatim).

Scope note: all three artifacts belong to the same role library and are inspected as one suite; no artifact from another case is mixed in.

Tier/level determinations:
- System Prompt set (`cs-financial-analyst` + `cs-ceo-advisor`): **L3 Complex Agent** - the roles orchestrate tool-backed skill packages (scripts + knowledge bases), declare `Bash`, and are security-sensitive (finance and board/investor material). Upward-compatible L3 scope = 47 items.
- Skill (`contract-and-proposal-writer`): **L2 (Medium Risk)** - it runs a tool (`pandoc` via `bash`) to convert generated documents; recoverable, non-sensitive output. Applied set = QD-S-0 + L2 mandatory (6 P0) + recommended (14 P1).

---

## 3. Stage A - Single-artifact inspection

### 3.A.1 System Prompt set (`cs-financial-analyst` + `cs-ceo-advisor`)

- QD-P-1.1.1 | PASS | evidence: TC-070, cs-financial-analyst.md + cs-ceo-advisor.md, no mutually exclusive attribute or directive found.
- QD-P-1.1.2 | PASS | evidence: TC-070, cs-ceo-advisor.md, the strategic/financial/organisational success-metric directives do not conflict in any declared scenario.
- QD-P-1.1.3 | PASS | evidence: TC-070, the two prompts, no worked example contradicts a rule (no worked examples are given).
- QD-P-1.2.1 | PASS | evidence: TC-070, the two prompts, each role identity (financial analyst; CEO advisor) matches its stated responsibilities.
- QD-P-1.2.2 | PASS | evidence: TC-070, the two prompts, the voice matches the declared professional output standards.
- QD-P-1.2.3 | PASS | evidence: TC-070, the two prompts, the constraints (assumptions must be stated; disclaimers) do not prohibit the core responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-070, the two prompts, quantities are bounded ("within 5%", "3 scenarios", "1x contract value").
- QD-P-1.3.2 | PASS | evidence: TC-070, the two prompts, the vague terms found ("strategic challenges", "high-performing organizations") are secondary descriptors, not a decision boundary.
- QD-P-1.3.3 | PASS | evidence: TC-070, the two prompts, role and handoff boundaries are defined (Related Agents cross-links).
- QD-P-1.4.1 | PASS | evidence: TC-070, the two prompts, no duplicate constraint found.
- QD-P-1.4.2 | PASS | evidence: TC-070, cs-financial-analyst.md, the workflow branches (bull/base/bear; CRITICAL/WATCH flags) are reachable.
- QD-P-1.4.3 | PASS | evidence: TC-070, the two prompts, no Skill definition is given in the prompt text (vacuous).
- QD-P-1.5.1 | PASS | evidence: TC-070, the two prompts, the responsibilities support the objectives (valuation/health/forecast; strategy/board/fundraising).
- QD-P-1.5.2 | PASS | evidence: TC-070, the two prompts, the workflow resources (scripts + references + knowledge bases) are declared with paths.
- QD-P-1.6.1 | PASS | evidence: TC-070, the two prompts, the critical decision conditions are numeric (variance thresholds, time estimates, success metrics).
- QD-P-1.6.2 | PASS | evidence: TC-070, the two prompts, the decision criteria are declared, not keyed on unreportable internal state.
- QD-P-1.6.3 | PASS | evidence: TC-070, the two prompts, the soft rules (be precise + state assumptions) are not in declared tension.
- QD-P-1.6.4 | PASS | evidence: TC-070, the two prompts, no constraint fixes an internal reasoning method beyond the given workflows.
- QD-P-1.6.5 | PASS | evidence: TC-070, the two prompts, no self-referential or recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-070, the two prompts, the assumed availability of user-supplied data and skill packages is declared in the workflows.
- QD-P-1.6.7 | PASS | evidence: TC-070, the two prompts, each role runs a bounded workflow and declares no multi-turn conclusion-revision path (determination basis: bounded role workflows).
- QD-P-2.1.1 | PASS | evidence: TC-070, the two prompts, formatting is readable.
- QD-P-2.1.2 | PASS | evidence: TC-070, the two prompts, the references (script and reference paths, related-agent links) are specific.
- QD-P-2.1.3 | PASS | evidence: TC-070, the two prompts, the hierarchy (role -> skill integration -> workflows -> output -> metrics) is reasonable.
- QD-P-2.1.4 | PASS | evidence: TC-070, the two prompts, prose is concise.
- QD-P-2.2.1 | PASS | evidence: TC-070, cs-financial-analyst.md, the input source is declared ("Collect MRR, customer count, churn, CAC data from user"; "Gather financial data").
- QD-P-2.2.2 | FAIL | evidence: TC-070, the two prompts, the input format is unconstrained - "Gather financial data (revenue, costs, growth rate, WACC)" declares no format, encoding or size limit.
- QD-P-2.2.3 | FAIL | evidence: TC-070, the two prompts, no required/optional marking for the financial/board inputs.
- QD-P-2.2.4 | FAIL | evidence: TC-070, the two prompts, handling of missing input is not declared.
- QD-P-2.3.1 | PASS | evidence: TC-070, cs-financial-analyst.md, the output format is declared (valuation as a range with methodology; forecasts as 3 scenarios; tables).
- QD-P-2.3.2 | PASS | evidence: TC-070, cs-financial-analyst.md + cs-ceo-advisor.md, the output structure is described (output standards; success metrics).
- QD-P-2.3.3 | PASS | evidence: TC-070, cs-financial-analyst.md, output stability is bounded by the declared output standards.
- QD-P-2.3.4 | FAIL | evidence: TC-070, the two prompts, no sensitive-data filtering, privacy handling, or security output constraint is declared.
- QD-P-2.4.1 | PASS | evidence: TC-070, the two prompts, the numbered workflow steps are complete.
- QD-P-2.4.2 | PASS | evidence: TC-070, the two prompts, the resources (scripts and references) are declared by path.
- QD-P-2.4.3 | FAIL | evidence: TC-070, cs-financial-analyst.md + cs-ceo-advisor.md, no tool invocation specification is given - scripts are invoked by name ("Run DCF model via `dcf_valuation.py`") with no parameter/sequence specification.
- QD-P-2.5.1 | PASS | evidence: TC-070, the two prompts, no loop or recursion is declared (vacuous).
- QD-P-2.5.2 | FAIL | evidence: TC-070, the two prompts, no prohibited operation, sensitive-data access boundary, or external-access boundary is declared.
- QD-P-2.5.3 | FAIL | evidence: TC-070, the two prompts, no permission scope or escalation boundary is declared although `Bash`/`Write` are granted.
- QD-P-2.5.4 | PASS | evidence: TC-070, the two prompts, the constraints do not declare a potential conflict (determination basis: no competing SHOULD constraints identified).
- QD-P-2.5.5 | FAIL | evidence: TC-070, the two prompts, no resource-invocation frequency limit is declared for the backing scripts.
- QD-P-2.6.1 | FAIL | evidence: TC-070, the two prompts, runtime exception handling is not declared (script/data failure has no defined behavior).
- QD-P-2.6.2 | FAIL | evidence: TC-070, the two prompts, no degradation or recovery strategy is declared.
- QD-P-2.6.3 | PASS | evidence: TC-070, the two prompts, no retry mechanism is declared (vacuous).
- QD-P-2.7.1 | FAIL | evidence: TC-070, the two prompts, no positive worked example is provided.
- QD-P-2.7.2 | FAIL | evidence: TC-070, the two prompts, no counter-examples are provided (Common Pitfalls are in the contract skill, not in these prompts).
- QD-P-2.7.3 | FAIL | evidence: TC-070, the two prompts, no boundary-case examples are provided.

### 3.A.2 Skill (`contract-and-proposal-writer`, L2)

QD-S-0 baseline: `name`/`description` present, non-empty, parseable, typed, non-conflicting, structurally complete - all six PASS.

- QD-S-1.1 Input Boundary Missing | FAIL | evidence: TC-070, contract-and-proposal-writer SKILL.md, no upper limit on input size or count is declared for the requirements-gathering step.
- QD-S-1.3 Execution Resource Boundary Missing | FAIL | evidence: TC-070, contract-and-proposal-writer SKILL.md, the skill invokes a tool/command but declares no retry count, tool-invocation count, or execution timeout - the conversion block "pandoc contract.md -o contract.docx --reference-doc=reference.docx -V geometry:margin=1in" has no execution limits.
- QD-S-2.1 Unbounded Quantity Declaration | FAIL | evidence: TC-070, contract-and-proposal-writer SKILL.md, unbounded wording with no cap - "Fill all [BRACKETED] placeholders."
- QD-S-2.2 Unterminated Execution Declaration | PASS | evidence: TC-070, contract-and-proposal-writer SKILL.md, no "keep trying / until success" wording (determination basis: absent).
- QD-S-3.4 Undefined Task Scope | PASS | evidence: TC-070, contract-and-proposal-writer SKILL.md, the role boundary is declared ("Not a substitute for legal counsel"; explicit document types).
- QD-S-4.1 Undefined Failure Behavior | PASS | evidence: TC-070, contract-and-proposal-writer SKILL.md, missing-data behavior is declared ("Flag missing data as 'REQUIRED'").
- QD-S-1.2 Output Size Missing | FAIL | evidence: TC-070, contract-and-proposal-writer SKILL.md, no output-size cap is declared.
- QD-S-1.4 Permission Boundary Missing | PASS | evidence: TC-070, contract-and-proposal-writer SKILL.md, the skill generates documents and declares no data read/write/delete operations (determination basis: document generation).
- QD-S-1.5 Data Source Boundary Missing | PASS | evidence: TC-070, contract-and-proposal-writer SKILL.md, the data source is bounded to user-provided requirements.
- QD-S-2.3 Open-Ended Enumeration in Structure | PASS | evidence: TC-070, contract-and-proposal-writer SKILL.md, the capabilities are enumerated (freelance contracts, proposals, SOWs, NDAs, MSAs) with no "etc.".
- QD-S-2.4 Broad Capability Verbs | PASS | evidence: TC-070, contract-and-proposal-writer SKILL.md, the capability is bounded by explicit document types and the legal-counsel disclaimer.
- QD-S-3.1 Vague Trigger Conditions | PASS | evidence: TC-070, contract-and-proposal-writer SKILL.md, triggers are specific ("Use when drafting a freelance contract, preparing a client proposal, writing an SOW ...").
- QD-S-3.2 Missing Deactivation Conditions | PASS | evidence: TC-070, contract-and-proposal-writer SKILL.md, the disclaimer bounds non-activation ("Not a substitute for legal counsel").
- QD-S-3.3 Missing Ambiguous Input Handling | PASS | evidence: TC-070, contract-and-proposal-writer SKILL.md, incomplete input is handled ("Flag missing data as 'REQUIRED'").
- QD-S-3.6 Metadata Expression Defects | PASS | evidence: TC-070, contract-and-proposal-writer SKILL.md, `name`/`description` are consistent with the body.
- QD-S-4.2 Undeclared Partial Completion Legitimacy | PASS | evidence: TC-070, contract-and-proposal-writer SKILL.md, partial handling is declared ("Flag missing data as 'REQUIRED'").
- QD-S-4.3 Missing Post-Failure Prohibited Behaviors | PASS | evidence: TC-070, contract-and-proposal-writer SKILL.md, prohibited behaviors are declared (the "Common Pitfalls" list).
- QD-S-5.1 Read/Write/Delete Not Distinguished | PASS | evidence: TC-070, contract-and-proposal-writer SKILL.md, no data-operation path is declared (determination basis: document generation).
- QD-S-5.3 Undeclared Environment Boundaries | PASS | evidence: TC-070, contract-and-proposal-writer SKILL.md, local markdown-to-docx conversion; no environment boundary needed (determination basis: local-only).
- QD-S-5.4 Undeclared Chained Invocation Permissions | PASS | evidence: TC-070, contract-and-proposal-writer SKILL.md, no downstream Skill invocation is declared (the `pandoc` command is a tool, not a chained Skill).

### 3.A.3 Tool Schema

- QD-T-1.x .. QD-T-4.x | N/A | evidence: TC-070 carries no Tool Schema artifact (determination basis: the agents name tools and scripts by name/path; no JSON `parameters`/`inputSchema` is present). No QD-T verdict is emitted.

### 3.A.4 Embedded code snippets (QC)

QC-0 baseline: the only embedded snippet is the `bash` `pandoc` conversion block in the contract skill.

- QC-0.1 | PASS | evidence: TC-070, contract-and-proposal-writer SKILL.md, the `bash` block is syntactically valid shell.
- QC-0.2 | PASS | evidence: TC-070, contract-and-proposal-writer SKILL.md, the block is fenced with a language identifier (`bash`).
- QC-0.3 | PASS | evidence: TC-070, contract-and-proposal-writer SKILL.md, the block is a set of complete alternative commands (no mid-command truncation).
- QC-0.4 | PASS | evidence: TC-070, contract-and-proposal-writer SKILL.md, the fence opens and closes correctly.
- QC-0.5 | PASS | evidence: TC-070, contract-and-proposal-writer SKILL.md, the declared language (`bash`) matches the content.
- QC-1.1 | PASS | evidence: TC-070, contract-and-proposal-writer SKILL.md, the commands reference only `pandoc` and file names; no undefined name reference.
- QC-1.2 | Not Executed | evidence: TC-070, no declared dependency list is available (dependency-context rule); not recorded as FAIL.
- QC-1.3 | Not Executed | evidence: TC-070, no API version database is available (dependency-context rule); not recorded as FAIL.
- QC-1.4 | N/A | evidence: TC-070, no function call with typed arguments is present (determination basis: shell commands).
- QC-2.1 | N/A | evidence: TC-070, no file-handle pattern present (determination basis: no such pattern).
- QC-2.2 | N/A | evidence: TC-070, no network-connection constructor present (determination basis: no such pattern).
- QC-2.3 | N/A | evidence: TC-070, no high-risk file/network/DB call in the snippet (determination basis: local doc conversion only).
- QC-3.1 | N/A | evidence: TC-070, no imports present (determination basis: shell commands).
- QC-3.2 | N/A | evidence: TC-070, no referenced symbols requiring imports (determination basis: shell commands).
- QC-3.3 | PASS | evidence: TC-070, contract-and-proposal-writer SKILL.md, the snippet uses generic example file names (`contract.md`, `reference.docx`); no credential or machine-specific value.
- QC-4.1 | PASS | evidence: TC-070, contract-and-proposal-writer SKILL.md, the snippet's input file (`contract.md`) matches the workflow's generate-and-fill step.
- QC-4.2 | PASS | evidence: TC-070, contract-and-proposal-writer SKILL.md, no version/API drift between the snippet and the body.

---

## 4. Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Agent tier for scope: L3. Evaluation scope = L3 full item set; blocking core = the Appendix B P0 set. QD-PT and QD-ST have no Tool Schema counterpart (N/A).

QD-PS (Prompt -> Skill):
- QD-PS-1.1 | FAIL (P0) | evidence: TC-070, both sides - the Prompt set declares `skills: finance` (cs-financial-analyst) and `skills: c-level-advisor/skills/ceo-advisor` (cs-ceo-advisor), while the Skill `contract-and-proposal-writer` is defined (`business-growth/skills/contract-and-proposal-writer/SKILL.md`) but is absent from that authorization scope.
- QD-PS-1.2 | PASS | evidence: TC-070, the agent triggers and the contract skill triggers are distinct and non-contradictory.
- QD-PS-1.3 | PASS | evidence: TC-070, the Skill permission scope (document generation) does not exceed the Prompt authorization.
- QD-PS-1.4 | PASS | evidence: TC-070, no resource-access contradiction between the Prompt and the Skill.
- QD-PS-1.5 | PASS | evidence: TC-070, the Skill FAILURE handling ("Flag missing data as 'REQUIRED'") does not contradict the Prompt.
- QD-PS-1.6 | PASS | evidence: TC-070, no output-constraint contradiction between the Prompt output standards and the Skill output structure.

QD-PT (Prompt -> Tool): N/A - no Tool Schema artifact.
QD-ST (Skill <-> Tool): N/A - no Tool Schema artifact.

QD-CYC (L2/L3):
- QD-CYC-1.1 | PASS | evidence: TC-070, no Skill output re-enters the Prompt workflow and no Tool callback re-triggers the Prompt is declared.
- QD-CYC-1.2 | PASS | evidence: TC-070, the Related Agents cross-links are one-directional references; no cyclic A <-> B role orchestration is declared.

Stage B result: P0 = 1 (QD-PS-1.1). Any P0 present -> cross-stage evaluation FAIL (recorded as a cross-stage result; it does not halt the flow).

---

## 5. Stage C - Gate-0 (admission)

- G0-1 (no unfixed P0 in Stage A): NOT satisfied - recorded as an informational finding; does not gate this flow.
- G0-2 (no unfixed P0 in Stage B): NOT satisfied - recorded as an informational finding; does not gate this flow.
- G0-3 (responsibility boundary statements exist and are locatable): Passed - each agent states its role and scope (e.g. cs-financial-analyst.md "Financial analyst covering valuation, ratio analysis, forecasting ..."; cs-ceo-advisor.md "The cs-ceo-advisor agent is a specialized executive leadership agent focused on strategic decision-making ...").
- G0-4 (each Tool Schema's `name`, `description`, parameter descriptions complete): NOT passed - no Tool Schema artifact is present.

Gate-0 result: **Not passed - G0-4**.

---

## 6. Stage D - Permission (QD-PM Quick Mode)

Subset: Inspect Permission Governance Specification (QD-PM)
Execution Status: Not Executed
Unsatisfied Conditions: G0-4 (structural admission); additionally the full artifact set is incomplete (no Tool Schema).
Blocking Reasons:
  G0-4 - Tool Schema `name`/`description`/parameter descriptions are not complete (no Tool Schema artifact is present).
  Artifact-set precondition - the full set (Prompt + Skill + all Tool Schemas) is not present.
Remediation Actions: Fix the above upstream items, then re-run Gate-0.

(The Permission stage was "Not Executed"; this is not a FAIL and not a permission conclusion.)

---

## 7. Stage E - Risk Explicit audit (EX) - physically separated from Inspect verdicts

Audit object: TC-070 System Prompt set (cs-financial-analyst, cs-ceo-advisor) + the contract skill + its embedded snippet.
Three-phase scan (NL-A -> NL-B -> NR-O -> NR-S) run over the bundled artifacts.

Risk Item Summary:
- Total Risk Items: 0
- Explicit.P0 (Block release): 0 items
- Explicit.P1 (Fix / exemption): 0 items
- Explicit.P2 (Risk ledger): 0 items

Note: no explicitly declared risk expression was found in the static artifact text. The agents' front matter declares `tools: [Read, Write, Bash, Grep, Glob]`; examined against the EX subcategories this is a capability-list declaration and does not meet a defined one (not a permission-level field NR-S-1, not a boolean dangerous flag NR-S-2, not an abnormal callback NR-S-7, not a hardcoded credential/PII value NR-S-9/NR-S-10). The legal-content tables (liability caps, IP ownership) are substantive content, not risk expressions. This is a static-document scan only; it is not a security conclusion. Risk Implicit (dynamic exploitability) was NOT run.

---

## 8. Stage F - Impact outlook (candidate mapping, advisory only)

Advisory context only; it does not change, soften, or escalate any Inspect conclusion. Strength is association confidence, NOT severity. Candidate language only. Risk Implicit and the runtime Quality subsets were NOT run; the lite embedded-code QC ran in Stage A. Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent.

| Defect (FAIL) | Candidate attack surface (AS-*) | Candidate failure modes (FM-*) | Strength (provisional, lite) |
|---|---|---|---|
| QD-PS-1.1 | AS-04, AS-09 | FM-04, FM-05, FM-06, FM-08 | Medium (defined skill outside the agents' authorization scope) |
| QD-P-2.2.2, QD-P-2.2.3, QD-P-2.2.4 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.3.4 | AS-03 | FM-06 | Conditional |
| QD-P-2.4.3 | AS-05, AS-07, AS-09 | FM-03, FM-04, FM-05 | Conditional |
| QD-P-2.5.2, QD-P-2.5.3, QD-P-2.5.5 | AS-01, AS-03, AS-04, AS-05 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.6.1, QD-P-2.6.2 | AS-07 | FM-08, FM-10 | Conditional |
| QD-P-2.7.1, QD-P-2.7.2, QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |
| QD-S-1.1, QD-S-1.2, QD-S-1.3, QD-S-2.1 | AS-06, AS-07 | FM-08, FM-10 | Conditional |
| QC (no FAIL) | (no AS-* mapping emitted for PASS items) | (no B.1 group) | Not Applicable |

Candidate RAG-Agent quality metrics (candidate associations only; NOT a quality result): Correctness, Completeness, Consistency, Traceability, Robustness, Boundary Recognition, Safety Response. Defect chains (SC-*/QC-*) are out of scope for lite v1.

---

## 9. Status board

Stage A (Single-artifact):  Executed - QD-P (L3, cs-financial-analyst + cs-ceo-advisor), QD-S (L2, contract-and-proposal-writer), QD-T (N/A, no Tool Schema), QC (bash pandoc snippet).
Stage B (Cross):            Executed - L3 scope; QD-PS run, QD-PT/QD-ST N/A; 1 P0 (QD-PS-1.1).
Stage C (Gate-0):           Not passed - G0-4 (G0-1/G0-2 informational).
Stage D (Permission QD-PM): Not Executed - Gate-0 G0-4 not satisfied; full artifact set incomplete (no Tool Schema).
Stage E (Risk Explicit EX): Executed - 0 findings.
Stage F (Impact outlook):   Executed - candidate mapping for all Stage A/B FAILs.
Stage G (Self-verification): Executed - ID back-closure, red-line wording, output contract checked.

---

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. No in-place self-corrections were required.
