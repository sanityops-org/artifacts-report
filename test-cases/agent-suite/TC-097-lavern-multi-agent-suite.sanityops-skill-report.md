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
- Finding counts (Stage A, System Prompt set): Inspect P0 = 8, P1 = 0, P2 = 0. The embedded-snippet QC adds one P1 finding (QC-0.2).
- Gate-0 result: Not passed (G0-3 passed; G0-4 not satisfied - no Tool Schema artifact is present; the 21 MCP tools are referenced by name only and show no JSON `parameters` schema).
- Risk-Explicit summary (Stage E): Explicit·P0 = 0, Explicit·P1 = 0, Explicit·P2 = 0.
- Top findings (rule ID - one-line defect):
  1. QD-P-2.5.2 / QD-P-2.5.3 - the prompts declare no security boundary and no permission-control boundary for a system that processes confidential legal documents.
  2. QD-P-2.3.4 - no sensitive-data filtering or privacy output constraint is declared.
  3. QD-P-2.2.2 / QD-P-2.2.3 - the matter/document input has no declared format and no required/optional marking.
  4. QD-P-2.7.1 / QD-P-2.7.2 / QD-P-2.7.3 - no positive, counter, or boundary-case example is provided.
  5. QC-0.2 - the quoted TS prompt-template snippets carry no code-fence language identifier.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The lite embedded-code QC was run in Stage A.
- This report never states a security or quality conclusion; Inspect PASS is not Risk PASS and not Quality PASS.
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and version-level evidence chains, use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

---

## 2. Artifact inventory (input preparation, not a stage)

Case TC-097 bundles one coordinated multi-agent legal-document-analysis suite (Lavern: 67 specialised system prompts, a debate protocol, three verification layers, and mandatory human gates). Artifact types present, by structural signature:

- System Prompt (present, quoted, 2): the Lead Orchestrator prompt (`src/agents/prompts/orchestrator.ts`) and the antitrust-specialist prompt (`src/agents/prompts/antitrust-specialist.ts`). Basis: prose/instruction strings returned from `export const ...Prompt = \`...\`` template literals.
- System Prompt (identified, not quoted, 65): the remaining 66 prompts (other domain specialists and the 6 other workflow orchestrators) exist per the directory listing but their bodies were not retrieved; they are therefore not inspected.
- Skill (absent): no markdown file with `name`/`description` front matter defines an invokable capability.
- Tool Schema (absent): the 21 MCP tools are referenced by name only (e.g. `get_current_step`, `advance_step`, `mcp__shem__request_approval`); no JSON `parameters`/`inputSchema` schema is shown.
- Embedded code snippets (QC scope): the TS prompt-template literals quoted in sections 1.1 and 1.2.
- Out of coverage: `src/workflows/` (9 templates), `src/mcp/tools/` (21 tools), and `src/types/verification.ts` are described but not quoted.

Scope note: every prompt is a role of the same orchestrated legal suite (one debate board, one workflow state machine, one verification pipeline, one human-gate protocol). All artifacts belong to the same agent suite, so no artifact from another case is mixed in.

---

## 3. Stage A - Single-artifact inspection

### 3.A.1 System Prompt set (lead orchestrator + specialist)

Tier determination: **L3 Complex Agent**. Basis (any 2 or more of the L3 criteria): the suite is a 67-role multi-agent orchestration with a 10-step state machine, a debate protocol and three verification layers (>5 steps); it is security-sensitive (confidential legal documents, a "human gate before critical decisions"); the orchestrator declares exception handling (uncertainty gate, `decline_to_find` handling, fail-closed verification). Upward-compatible L3 scope = 47 items.

- QD-P-1.1.1 | PASS | evidence: TC-097, sections 1.1-1.2, no mutually exclusive attribute or directive found.
- QD-P-1.1.2 | PASS | evidence: TC-097, sections 1.1-1.2, the workflow-state-machine rules and the human-gate rules do not conflict in any declared scenario.
- QD-P-1.1.3 | PASS | evidence: TC-097, sections 1.1-1.2, no worked example contradicts a rule (only the output schema summary is shown).
- QD-P-1.2.1 | PASS | evidence: TC-097, sections 1.1-1.2, each role identity (Lead Orchestrator; Antitrust Specialist "The Strategist") matches its stated responsibilities.
- QD-P-1.2.2 | PASS | evidence: TC-097, section 1.2, the role voice matches the declared structured-JSON output style.
- QD-P-1.2.3 | PASS | evidence: TC-097, sections 1.1-1.2, the constraints (cite specific text, do not provide legal advice) do not prohibit the core analysis responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-097, sections 1.1-1.2, quantities are bounded ("5 dimensions", "10 passes", "confidence below 0.6", "0-4 scale").
- QD-P-1.3.2 | PASS | evidence: TC-097, section 1.1, the vague terms found ("critical decisions") are qualified by concrete gate conditions (RED findings, CRITICAL-risk changes, confidence below 0.6).
- QD-P-1.3.3 | PASS | evidence: TC-097, sections 1.1-1.2, a prohibition scope is declared ("This system does not provide legal advice - flag for legal counsel, don't determine") and the workflow/verification boundaries are defined.
- QD-P-1.4.1 | PASS | evidence: TC-097, sections 1.1-1.2, no duplicate constraint found.
- QD-P-1.4.2 | PASS | evidence: TC-097, section 1.1, the workflow branches and gate conditions are all reachable.
- QD-P-1.4.3 | PASS | evidence: TC-097, sections 1.1-1.2, no Skill definition is given in the prompts (vacuous).
- QD-P-1.5.1 | PASS | evidence: TC-097, sections 1.1-1.2, the specialist/verification responsibilities support the objective (dual-artifact delivery after verification).
- QD-P-1.5.2 | PASS | evidence: TC-097, section 1.1, the workflow resources (workflow-engine tools, approval gate tool) are declared.
- QD-P-1.6.1 | PASS | evidence: TC-097, sections 1.1-1.2, decision words are bounded by explicit thresholds (confidence 0-1, confidence below 0.6, GREEN/YELLOW/RED), not vague.
- QD-P-1.6.2 | PASS | evidence: TC-097, section 1.1, the gate conditions key on declared findings/severity/confidence outputs, not on unobservable model internal state.
- QD-P-1.6.3 | PASS | evidence: TC-097, sections 1.1-1.2, the soft rules ("Debate is a feature", "Legal effect preservation") are arbitrated by the debate-resolution and verification layers.
- QD-P-1.6.4 | PASS | evidence: TC-097, sections 1.1-1.2, no constraint fixes an internal reasoning method.
- QD-P-1.6.5 | PASS | evidence: TC-097, sections 1.1-1.2, no self-referential or recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-097, section 1.1, the workflow-engine and tool availability assumptions are stated and the state machine enforces preconditions.
- QD-P-1.6.7 | PASS | evidence: TC-097, sections 1.1-1.2, the debate/challenge/resolution protocol is the declared conclusion-revision mechanism (determination basis: explicit arbitration exists).
- QD-P-2.1.1 | PASS | evidence: TC-097, sections 1.1-1.2, formatting is readable.
- QD-P-2.1.2 | PASS | evidence: TC-097, section 1.1, the referenced tools (`get_current_step`, `advance_step`, `mcp__shem__request_approval`) are named and locatable.
- QD-P-2.1.3 | PASS | evidence: TC-097, sections 1.1-1.2, the agents / state-machine / human-gates / key-principles hierarchy is reasonable.
- QD-P-2.1.4 | PASS | evidence: TC-097, sections 1.1-1.2, prose is concise (excerpted with ellipses).
- QD-P-2.2.1 | PASS | evidence: TC-097, section 1.2, the input source is declared (the "matter" is classified by Type, Parties, Jurisdictions, Urgency).
- QD-P-2.2.2 | FAIL | evidence: TC-097, sections 1.1-1.2, the input document format is unconstrained - the parsed document text, its encoding, and its size limit are not declared.
- QD-P-2.2.3 | FAIL | evidence: TC-097, sections 1.1-1.2, no input field is marked required or optional (the classification fields Type/Parties/Jurisdictions/Urgency carry no required marking).
- QD-P-2.2.4 | PASS | evidence: TC-097, section 1.1, insufficient/absent findings are handled - agents use `decline_to_find` and the uncertainty gate surfaces it to a human.
- QD-P-2.3.1 | PASS | evidence: TC-097, section 1.2, output format is declared ("Your output MUST be structured JSON matching the antitrust-specialist schema").
- QD-P-2.3.2 | PASS | evidence: TC-097, section 1.2, the output schema fields are declared (marketDefinition, competitiveAssessment, filingMatrix, riskAssessment, remediesAnalysis, timeline, findings, confidence, summary).
- QD-P-2.3.3 | PASS | evidence: TC-097, sections 1.1-1.2, format stability is bounded by the mandatory structured-JSON contract and the fail-closed verification layers.
- QD-P-2.3.4 | FAIL | evidence: TC-097, sections 1.1-1.2, no sensitive-data filtering, privacy handling, or security output constraint is declared for confidential legal documents.
- QD-P-2.4.1 | PASS | evidence: TC-097, section 1.1, the workflow state machine is a complete step sequence (INTAKE -> ... -> FINAL GATE).
- QD-P-2.4.2 | PASS | evidence: TC-097, section 1.1, the resources/tools used (workflow engine, approval gate, specialist dispatch) are declared.
- QD-P-2.4.3 | PASS | evidence: TC-097, section 1.1, an invocation specification is given ("Call `get_current_step` at the start ... Call `advance_step` after completing each step").
- QD-P-2.5.1 | PASS | evidence: TC-097, sections 1.1-1.2, no unbounded loop or recursion is declared (the state machine and debate resolution are bounded).
- QD-P-2.5.2 | FAIL | evidence: TC-097, sections 1.1-1.2, no prohibited operation, sensitive-data access boundary, or external-access boundary is declared.
- QD-P-2.5.3 | FAIL | evidence: TC-097, sections 1.1-1.2, no permission scope or privilege-escalation boundary is declared (per-agent MCP tool permissions are referenced in the README, not stated in the prompt).
- QD-P-2.5.4 | PASS | evidence: TC-097, sections 1.1-1.2, no unarbitrated soft-constraint conflict found.
- QD-P-2.5.5 | PASS | evidence: TC-097, sections 1.1-1.2, no resource-invocation frequency limit is needed beyond the workflow-engine's bounded step sequence.
- QD-P-2.6.1 | PASS | evidence: TC-097, section 1.1, agent-level anomalies (no finding, low confidence) are covered by `decline_to_find`, the uncertainty gate, and the fail-closed verification layers.
- QD-P-2.6.2 | PASS | evidence: TC-097, section 1.1, degradation is defined (fail-closed layers and mandatory human gates rather than silent continuation).
- QD-P-2.6.3 | PASS | evidence: TC-097, sections 1.1-1.2, no retry mechanism is declared (vacuous).
- QD-P-2.7.1 | FAIL | evidence: TC-097, sections 1.1-1.2, no positive worked example of a valid finding or output object is provided.
- QD-P-2.7.2 | FAIL | evidence: TC-097, sections 1.1-1.2, no counter-examples are provided.
- QD-P-2.7.3 | FAIL | evidence: TC-097, sections 1.1-1.2, no boundary-case examples are provided.

### 3.A.2 Skill

- QD-S-1.x .. QD-S-5.x | N/A | evidence: TC-097 carries no Skill artifact (determination basis: no markdown file with `name`/`description` front matter; the prompts are TS template literals). No QD-S verdict is emitted.

### 3.A.3 Tool Schema

- QD-T-1.x .. QD-T-4.x | N/A | evidence: TC-097 carries no Tool Schema artifact (determination basis: the 21 MCP tools are referenced by name only, with no JSON `parameters`/`inputSchema` schema). No QD-T verdict is emitted.

### 3.A.4 Embedded code snippets (QC)

QC-0 baseline: the quoted TS prompt-template literals are syntactically valid (`export const x = \`...\`;`). The fences carry no explicit language identifier.

- QC-0.1 | PASS | evidence: TC-097, sections 1.1-1.2, the template literals are syntactically valid TypeScript.
- QC-0.2 | FAIL | evidence: TC-097, sections 1.1-1.2, the code blocks carry no explicit language identifier (no ` ```ts ` or equivalent).
- QC-0.3 | PASS | evidence: TC-097, sections 1.1-1.2, each template literal is complete (opens and closes its backtick), not truncated mid-statement.
- QC-0.4 | PASS | evidence: TC-097, all code fences open and close correctly.
- QC-0.5 | N/A | evidence: TC-097, no language identifier is declared, so a language-content match cannot be assessed (determination basis: no declared language).
- QC-1.1 | N/A | evidence: TC-097, the snippets are prompt text inside template literals; no executable name references (determination basis: data/text-only snippets).
- QC-1.2 | Not Executed | evidence: TC-097, no declared dependency list is available (dependency-context rule); not recorded as FAIL.
- QC-1.3 | Not Executed | evidence: TC-097, no API version database is available (dependency-context rule); not recorded as FAIL.
- QC-1.4 | N/A | evidence: TC-097, no function call with typed arguments is present (determination basis: text-only snippets).
- QC-2.1 | N/A | evidence: TC-097, no file-handle pattern present (determination basis: no such pattern).
- QC-2.2 | N/A | evidence: TC-097, no network-connection constructor present (determination basis: no such pattern).
- QC-2.3 | N/A | evidence: TC-097, no high-risk file/network/DB call present (determination basis: no such pattern).
- QC-3.1 | N/A | evidence: TC-097, no imports present (determination basis: text-only snippets).
- QC-3.2 | N/A | evidence: TC-097, no referenced symbols requiring imports (determination basis: text-only snippets).
- QC-3.3 | PASS | evidence: TC-097, the only literals are role/severity labels (GREEN/YELLOW/RED, confidence 0-1); no credential, local path, or machine-specific value.

---

## 4. Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Stage status: **Not Executed**. Reason: only one Logic Artifact type (System Prompt) is present; no Prompt/Skill/Tool pair exists, so QD-PS (Prompt -> Skill), QD-PT (Prompt -> Tool), QD-ST (Skill <-> Tool), and QD-CYC-1.1 have no counterpart artifact and are Not Applicable.

Informational observation (not a Stage B verdict line): QD-CYC-1.2 (Multi-Agent Circular Invocation) was reviewed at suite level - the Lead Orchestrator dispatches specialists through a one-way workflow state machine with a debate board and fail-closed verification; although agents "challenge each other" via the debate board, no cyclic role invocation (Agent A calling Agent B and back) is explicitly declared. No closed loop was found.

---

## 5. Stage C - Gate-0 (admission)

- G0-1 (no unfixed P0 in Stage A): NOT satisfied - recorded as an informational finding; does not gate this flow.
- G0-2 (no unfixed P0 in Stage B): N/A - Stage B did not run; recorded as informational.
- G0-3 (responsibility boundary statements exist and are locatable): Passed - the orchestrator and specialist prompts state their roles and scope (e.g. section 1.1 "You are the Lead Orchestrator of The Shem, a multi-agent legal design system."; section 1.2 "You are the Antitrust Specialist at The Shem").
- G0-4 (each Tool Schema's `name`, `description`, parameter descriptions complete): NOT passed - no Tool Schema artifact is present (the 21 MCP tools are named only, with no parameter schema).

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

Audit object: TC-097 System Prompt set (lead orchestrator + antitrust specialist) + embedded TS snippets.
Three-phase scan (NL-A -> NL-B -> NR-O -> NR-S) run over the bundled artifacts.

Risk Item Summary:
- Total Risk Items: 0
- Explicit·P0 (Block release): 0 items
- Explicit·P1 (Fix / exemption): 0 items
- Explicit·P2 (Risk ledger): 0 items

Note: no explicitly declared risk expression (self-contained exfiltration, identity/permission claim, constraint removal, priority override, dangerous flag, hardcoded credential/PII, or abnormal callback) was found in the static artifact text. The human-gate and fail-closed rules are risk-reducing controls, not risk expressions. This is a static-document scan only; it is not a security conclusion. Risk Implicit (dynamic exploitability) was NOT run.

---

## 8. Stage F - Impact outlook (candidate mapping, advisory only)

Advisory context only; it does not change, soften, or escalate any Inspect conclusion. Strength is association confidence, NOT severity. Candidate language only. Risk Implicit and the runtime Quality subsets were NOT run; the lite embedded-code QC ran in Stage A. Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent.

| Defect (FAIL) | Candidate attack surface (AS-*) | Candidate failure modes (FM-*) | Strength (provisional, lite) |
|---|---|---|---|
| QD-P-2.2.2, QD-P-2.2.3 | AS-02, AS-07 | FM-01, FM-04 | Medium (input format/necessity undeclared) |
| QD-P-2.3.4 | AS-03 | FM-06 | Conditional |
| QD-P-2.5.2, QD-P-2.5.3 | AS-01, AS-03, AS-04, AS-05 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.7.1, QD-P-2.7.2, QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |
| QC-0.2 | (no AS-* row in Appendix A; snippet-level only) | (no B.1 group) | Not Applicable (out of Appendix A mapping scope) |

Candidate RAG-Agent quality metrics (candidate associations only; NOT a quality result): Correctness, Completeness, Traceability, Format Compliance, Boundary Recognition, Safety Response. Defect chains (SC-*/QC-*) are out of scope for lite v1.

---

## 9. Status board

Stage A (Single-artifact):  Executed - QD-P (L3, lead orchestrator + antitrust specialist), QD-S (N/A, no Skill), QD-T (N/A, no Tool Schema), QC (embedded TS snippets).
Stage B (Cross):            Not Executed - only one artifact type present (System Prompt); no Prompt/Skill/Tool pair exists.
Stage C (Gate-0):           Not passed - G0-4 (G0-1/G0-2 informational).
Stage D (Permission QD-PM): Not Executed - Gate-0 G0-4 not satisfied; full artifact set incomplete (no Skill, no Tool Schema).
Stage E (Risk Explicit EX): Executed - 0 findings.
Stage F (Impact outlook):   Executed - candidate mapping for all Stage A FAILs.
Stage G (Self-verification): Executed - ID back-closure, red-line wording, output contract checked.

---

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. No in-place self-corrections were required.
