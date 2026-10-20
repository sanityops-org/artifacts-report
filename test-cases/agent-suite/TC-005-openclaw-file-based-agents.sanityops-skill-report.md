# SanityOps Inspect Lite Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-14
Artifact version: not supplied by the user (using the case's Collection Date as the working label)

---

## 1. Executive summary (Sec. 6.1)

- Stages executed: A (single-artifact), C (Gate-0), E (Risk Explicit), F (impact outlook), G (self-verification). Stage B did not run (only one artifact type present); Stage D did not run (incomplete artifact set).
- Finding counts (Stage A): Inspect P0 = 1, P1 = 7, P2 = 1.
- Gate-0 result: Passed (G0-3 satisfied; G0-4 vacuously satisfied - no Tool Schema in the set).
- Risk-Explicit summary (Stage E): Explicit.P0 = 0, Explicit.P1 = 0, Explicit.P2 = 0.
- Top findings (rule ID - one-line defect):
  1. QD-P-2.4.3 - The declared Skills (browser, memory, file, shell) have no invocation specification (parameters, sequence, failure handling).
  2. QD-P-1.6.2 - "Ask clarifying questions if needed" is a rule keyed on unobservable model judgment.
  3. QD-P-2.7.3 - No boundary-case examples (empty/anomalous input) are provided.
  4. QD-P-2.7.1 - The only positive examples are tone examples, not representative of the core tasks.
  5. QD-P-2.3.3 - No output stability/consistency assurance is declared.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The lite embedded-code QC was run in Stage A.
- This report never states a security or quality conclusion; Inspect PASS is not Risk PASS and not Quality PASS.
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and version-level evidence chains, use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

---

## 2. Artifact inventory (input preparation, not a stage)

Case TC-005 is a file-based, config-first agent suite. Artifact types present, by structural signature:

- System Prompt (present, 6 files): SOUL.md (personality + boundaries), AGENTS.md (multi-agent routing configuration), USER.md (user model), IDENTITY.md (agent identity), HEARTBEAT.md (scheduled-task configuration with embedded JavaScript), MEMORY.md (runtime memory). Basis: prose/markdown instructions and configuration that govern agent behavior.
- Skill (absent): no markdown file with `name`/`description` front matter defining an invokable capability. (SOUL.md has front matter, but its body is a persona/boundary prompt, so it is classified as a System Prompt, not a Skill.)
- Tool Schema (absent): no JSON Schema / function-calling definition with `parameters` + `description`.
- Edge case recorded: SOUL.md carries YAML front matter (`name`/`description`/`model`). It was still classified as a System Prompt because its body defines the agent persona and boundaries rather than a discrete invokable capability. If needed, the user may re-declare this classification.

Multi-agent note: AGENTS.md defines several routed agents (support-main, sales-assistant, onboarding-guide). Only the support persona (SOUL.md + IDENTITY.md) is given a full set of prompt files, so the inspection is scoped to that single agent's prompt set; no cross-artifact checks were run across different agents.

---

## 3. Stage A - Single-artifact inspection

### 3.A.1 System Prompt set (SOUL.md, AGENTS.md, IDENTITY.md, HEARTBEAT.md, USER.md, MEMORY.md)

Tier determination: **L2 Multi-turn Interactive**. Basis (any 2 or more of the L2 criteria): multi-turn dialogue is required (messaging support); the response workflow is a simple 5-step sequence (Acknowledge -> Clarify -> Solve -> Confirm -> Offer); limited state management (per-agent SQLite/workspace). The 4 declared Skills (browser/memory/file/shell) are borderline, but only one L3 criterion (4+ tool invocations) is met, and L3 requires any 2 - so L3 does not apply. Scope = L2 (40 items).

- QD-P-1.1.1 | PASS | evidence: TC-005, SOUL.md, no mutually exclusive attributes found.
- QD-P-1.1.3 | PASS | evidence: TC-005, SOUL.md "Tone Examples" are consistent with the stated rules.
- QD-P-1.2.1 | PASS | evidence: TC-005, SOUL.md Identity "Customer support specialist for SaaS products" matches the responsibilities.
- QD-P-1.2.3 | PASS | evidence: TC-005, SOUL.md constraints do not prohibit core responsibilities.
- QD-P-1.5.1 | PASS | evidence: TC-005, SOUL.md responsibilities support the support objective.
- QD-P-2.2.1 | PASS | evidence: TC-005, AGENTS.md declares channel bindings (whatsapp/telegram/slack) as the message source.
- QD-P-2.3.4 | PASS | evidence: TC-005, SOUL.md "NEVER share internal documentation or system details" is a security output constraint.
- QD-P-2.5.2 | PASS | evidence: TC-005, SOUL.md "NEVER share internal documentation or system details" and "shell: Run diagnostic commands (read-only)" set boundaries.
- QD-P-1.3.3 | PASS | evidence: TC-005, SOUL.md "Stay within support scope (technical issues, usage questions, billing)" defines the boundary; add boundaries in AGENTS.md "handoff_rules".
- QD-P-1.5.2 | PASS | evidence: TC-005, SOUL.md skills (browser/memory/file/shell) support the response guidelines.
- QD-P-1.6.1 | PASS | evidence: TC-005, SOUL.md "Escalate billing issues to human team immediately" is a clear decision rule.
- QD-P-2.2.2 | PASS | evidence: TC-005, input is natural-language conversation (no structured parser defined), so no format constraint is required.
- QD-P-2.2.3 | PASS | evidence: TC-005, no parameterized input is declared (not triggered).
- QD-P-2.2.4 | PASS | evidence: TC-005, SOUL.md "Ask clarifying questions if needed" handles missing input.
- QD-P-2.3.1 | PASS | evidence: TC-005, SOUL.md output is a natural-language reply (no downstream structured parser).
- QD-P-2.3.2 | PASS | evidence: TC-005, no structured output schema is required for a conversational reply.
- QD-P-2.4.2 | PASS | evidence: TC-005, SOUL.md "## Skills" section declares browser/memory/file/shell.
- QD-P-2.4.3 | FAIL | evidence: TC-005, SOUL.md "browser: Search knowledge base articles" declares the Skill by name only, with no invocation parameters, sequence, or failure handling.
- QD-P-1.2.2 | PASS | evidence: TC-005, SOUL.md tone matches the support role output style.
- QD-P-1.3.1 | PASS | evidence: TC-005, SOUL.md, no quantifier-scope error found.
- QD-P-1.3.2 | PASS | evidence: TC-005, SOUL.md, no excessive vague qualifier found.
- QD-P-1.4.1 | PASS | evidence: TC-005, SOUL.md, no duplicate constraint found.
- QD-P-1.4.2 | PASS | evidence: TC-005, SOUL.md response guidelines are all reachable.
- QD-P-1.4.3 | PASS | evidence: TC-005, the declared Skills are named with one-line descriptions and are not shown as broken (no invalid Skill definition found).
- QD-P-1.6.2 | FAIL | evidence: TC-005, SOUL.md "Ask clarifying questions if needed" is keyed on unobservable model judgment ("if needed").
- QD-P-1.6.3 | PASS | evidence: TC-005, SOUL.md "Clear explanations without jargon" does not conflict with the other soft rules.
- QD-P-1.6.4 | PASS | evidence: TC-005, SOUL.md, no internal reasoning-method constraint found.
- QD-P-1.6.5 | PASS | evidence: TC-005, SOUL.md, no self-referential/recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-005, SOUL.md, no unstated-assumption dependency found beyond normal chat assumptions.
- QD-P-1.6.7 | PASS | evidence: TC-005, SOUL.md, no rule requires revising earlier conclusions on new information.
- QD-P-2.3.3 | FAIL | evidence: TC-005, SOUL.md defines tone but declares no output stability/consistency assurance mechanism.
- QD-P-2.4.1 | PASS | evidence: TC-005, SOUL.md "Response Guidelines" 1-5 form a complete workflow.
- QD-P-2.5.1 | PASS | evidence: TC-005, SOUL.md "Confirm resolution before closing" provides a termination step.
- QD-P-2.5.3 | PASS | evidence: TC-005, SOUL.md "shell: Run diagnostic commands (read-only)" bounds the permission scope.
- QD-P-2.5.4 | PASS | evidence: TC-005, SOUL.md, no conflicting soft constraints requiring priority arbitration.
- QD-P-2.5.5 | PASS | evidence: TC-005, SOUL.md, no resource-abuse-prone invocation declared (not triggered).
- QD-P-2.7.1 | FAIL | evidence: TC-005, SOUL.md "Tone Examples" are the only positive examples and do not represent the core tasks (billing, escalation, troubleshooting).
- QD-P-2.7.2 | PASS | evidence: TC-005, SOUL.md provides two counter-examples under "Tone Examples".
- QD-P-2.7.3 | FAIL | evidence: TC-005, SOUL.md provides no boundary-case examples (empty/anomalous input).

### 3.A.2 Embedded code snippets (QC) - HEARTBEAT.md JavaScript

QC-0 baseline: the JavaScript snippets parse (QC-0.1 PASS) and carry the `javascript` language identifier (QC-0.2 PASS); QC-0.3 fails (undefined symbols), so QC-1..QC-3 are advisory for the parsable snippets.

- QC-0.1 | PASS | evidence: TC-005, HEARTBEAT.md, the `const`/`await` snippets are syntactically valid JavaScript.
- QC-0.2 | PASS | evidence: TC-005, HEARTBEAT.md, fenced blocks declare `javascript`.
- QC-0.3 | FAIL | evidence: TC-005, HEARTBEAT.md `await fetchTickets({...})` references undefined functions with no definitions or imports.
- QC-1.1 | FAIL | evidence: TC-005, HEARTBEAT.md `fetchTickets`, `notify`, `countResolved`, `getAvgResponseTime`, `countEscalations`, `postToSlack`, `formatSummary`, `findUsers`, `sendEmail` are all undefined.
- QC-1.2 | PASS | evidence: TC-005, HEARTBEAT.md, no import statement present.
- QC-1.3 | PASS | evidence: TC-005, HEARTBEAT.md, no deprecated API usage present.
- QC-1.4 | PASS | evidence: TC-005, HEARTBEAT.md, no type-mismatched call present.
- QC-2.1 | N/A | evidence: TC-005, HEARTBEAT.md, no file-handle pattern (determination basis: no such pattern).
- QC-2.2 | N/A | evidence: TC-005, HEARTBEAT.md, no explicit connection constructor without close (determination basis: no such pattern).
- QC-2.3 | FAIL | evidence: TC-005, HEARTBEAT.md `sendEmail(user.email, ...)` / `await fetchTickets(...)` network calls have no try/catch.
- QC-3.1 | PASS | evidence: TC-005, HEARTBEAT.md, no unused import present.
- QC-3.2 | FAIL | evidence: TC-005, HEARTBEAT.md references `notify`/`postToSlack`/`sendEmail` without any import or definition in the snippet.
- QC-3.3 | PASS | evidence: TC-005, HEARTBEAT.md, no hardcoded demo credential present.

---

## 4. Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Not Executed - fewer than two same-agent artifact types present (only the System Prompt type is present; no Skill and no Tool Schema).

---

## 5. Stage C - Gate-0 (admission)

- G0-1 (no unfixed P0 in Stage A): NOT satisfied (QD-P-2.4.3) - recorded as an informational finding; does not gate this flow.
- G0-2 (no unfixed P0 in Stage B): N/A - Stage B did not run.
- G0-3 (responsibility boundary statements exist and are locatable): Passed - SOUL.md "## Rules & Boundaries" and "Stay within support scope (...)" are locatable.
- G0-4 (each Tool Schema's `name`, `description`, parameter descriptions complete): satisfied vacuously - no Tool Schema is present in the artifact set.

Gate-0 result: **Passed** (G0-3 satisfied; G0-4 vacuously satisfied).

---

## 6. Stage D - Permission (QD-PM Quick Mode)

Subset: Inspect Permission Governance Specification (QD-PM)
Execution Status: Not Executed
Unsatisfied Conditions: none at Gate-0; blocking precondition is the artifact set.
Blocking Reasons:
  The full artifact set required for permission quick mode is incomplete - no Skill and no Tool Schema are present (only the System Prompt type).
Remediation Actions: Provide the Skill and all Tool Schemas for the same agent, then re-run Gate-0.

(The Permission stage was "Not Executed"; this is not a FAIL and not a permission conclusion.)

---

## 7. Stage E - Risk Explicit audit (EX) - physically separated from Inspect verdicts

Audit object: TC-005 System Prompt set (including HEARTBEAT.md embedded code) + configuration files.
Three-phase scan (NL-A -> NL-B -> NR-O -> NR-S) run over the bundled artifacts.

Risk Item Summary:
- Total Risk Items: 0
- Explicit.P0 (Block release): 0 items
- Explicit.P1 (Fix / exemption): 0 items
- Explicit.P2 (Risk ledger): 0 items

Note: no explicitly declared risk expression was found in the static artifact text. Items such as automated outbound email in HEARTBEAT.md are control/boundary observations, not EX-classified risk expressions, and are not graded here. This is a static-document scan only; it is not a security conclusion. Risk Implicit (dynamic exploitability) was NOT run.

---

## 8. Stage F - Impact outlook (candidate mapping, advisory only)

Advisory context only; it does not change, soften, or escalate any Inspect conclusion. Strength is association confidence, NOT severity. Candidate language only. Risk Implicit and the runtime Quality subsets were NOT run; the lite embedded-code QC ran in Stage A. Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent.

| Defect (FAIL) | Candidate attack surface (AS-*) | Candidate failure modes (FM-*) | Strength (provisional, lite) |
|---|---|---|---|
| QD-P-2.4.3 | AS-05, AS-07, AS-09 | FM-03, FM-04, FM-05 | Medium (Skill invocation spec absent) |
| QD-P-1.6.2 | AS-01, AS-07 | FM-01, FM-02, FM-07, FM-09 | Medium |
| QD-P-2.3.3 | AS-03, AS-09 | FM-06 | Conditional |
| QD-P-2.7.1, QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |
| QC-0.3, QC-1.1, QC-3.2 | (no AS-* row in Appendix A; snippet-level only) | (no B.1 group) | Not Applicable (out of Appendix A mapping scope) |
| QC-2.3 | (no AS-* row in Appendix A; snippet-level only) | (no B.1 group) | Not Applicable (out of Appendix A mapping scope) |

Candidate RAG-Agent quality metrics (candidate associations only; NOT a quality result): Correctness, Robustness, Boundary Recognition, Format Compliance, Safety Response. Defect chains (SC-*/QC-TA-*/QC-RA-*) are out of scope for lite v1.

---

## 9. Status board

Stage A (Single-artifact):  Executed - QD-P (L2, System Prompt set) + QC (HEARTBEAT.md JavaScript).
Stage B (Cross):            Not Executed - fewer than two same-agent artifact types present.
Stage C (Gate-0):           Passed - G0-3 satisfied; G0-4 vacuously satisfied (G0-1 informational).
Stage D (Permission QD-PM): Not Executed - incomplete artifact set (no Skill, no Tool Schema).
Stage E (Risk Explicit EX): Executed - 0 findings.
Stage F (Impact outlook):   Executed - candidate mapping for all Stage A FAILs.
Stage G (Self-verification): Executed - ID back-closure, red-line wording, output contract checked.

---

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. No in-place self-corrections were required.
