# SanityOps Inspect Lite Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-14
Artifact version: not supplied by the user (using the case's Collection Date as the working label)

---

## 1. Executive summary (Sec. 6.1)

- Stages executed: A (single-artifact), B (cross-artifact, Prompt-Tool only), C (Gate-0), E (Risk Explicit), F (impact outlook), G (self-verification). Stage D did not run (Gate-0 G0-4 not satisfied).
- Finding counts (Stage A + B): Inspect P0 = 32, P1 = 2, P2 = 0.
- Gate-0 result: Not passed (G0-3 passed; G0-4 not satisfied - the Forge Tool Schema lists component names and one-line descriptions, not tool name/description/parameter schemas).
- Risk-Explicit summary (Stage E): Explicit.P0 = 0, Explicit.P1 = 0, Explicit.P2 = 0.
- Top findings (rule ID - one-line defect):
  1. QD-P-2.4.2 / QD-P-1.5.2 - The Prompt injects `{commands}` / `{resources}` placeholders but the Prompt itself defines no resources or tools.
  2. QD-P-2.5.2 / QD-P-2.5.3 - The Prompt declares no security boundaries or permission scopes for the 20 forge components.
  3. QD-T-3.1 / QD-T-3.2 - `code_executor`, `file_manager`, `git_operations` perform writes/execution with no write notice and no parameter schema.
  4. QD-PT-2.2 / QD-PT-2.3 - Prompt invocation JSON schema and Tool Schema parameters are not consistent.
  5. QD-P-1.6.6 - The rule "If a test fails, the bug is in your code, NOT in the test" depends on an unstated assumption.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The lite embedded-code QC was run in Stage A.
- This report never states a security or quality conclusion; Inspect PASS is not Risk PASS and not Quality PASS.
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and version-level evidence chains, use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

---

## 2. Artifact inventory (input preparation, not a stage)

Case TC-035 is a single autonomous agent (AutoGPT Classic) with selectable prompt strategies. All artifacts belong to the same agent. Types present, by structural signature:

- System Prompt (present): OneShotAgentPromptConfiguration `DEFAULT_BODY_TEMPLATE` + `DEFAULT_CHOOSE_ACTION_INSTRUCTION`, and the output schema `AssistantThoughts`. Basis: prose/instruction strings plus the assistant output schema.
- Skill (absent): no markdown with `name`/`description` front matter is shown.
- Tool Schema (present, partial): the Forge component list (20 components) and `FileManagerComponent`. Basis: command-component definitions; no JSON `parameters` schema is shown.
- Out of coverage: the other 6 prompt strategies and the component implementation modules are not quoted; only the shown text is inspected.

---

## 3. Stage A - Single-artifact inspection

### 3.A.1 System Prompt set (OneShot strategy + response schema)

Tier determination: **L3 Complex Agent**. Basis: 4+ tool invocations (20 forge components), autonomous multi-step workflow (> 5 steps), security-sensitive file/shell/browser operations. Scope = L3 (47 items).

- QD-P-1.1.1 | PASS | evidence: TC-035, "These are the ONLY commands you can use" is consistent with the constraints/resources/commands structure.
- QD-P-1.1.2 | PASS | evidence: TC-035, no conflicting directives.
- QD-P-1.1.3 | PASS | evidence: TC-035, no example contradicting a rule.
- QD-P-1.2.1 | PASS | evidence: TC-035, an autonomous coding-agent role matches the declared responsibilities.
- QD-P-1.2.2 | PASS | evidence: TC-035, no style rule mismatch.
- QD-P-1.2.3 | PASS | evidence: TC-035, no constraint prohibits a declared responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-035, no quantifier-scope misuse found.
- QD-P-1.3.2 | PASS | evidence: TC-035, no vague qualifier carries a critical decision.
- QD-P-1.3.3 | FAIL | evidence: TC-035, only `{constraints}` placeholder; no authorization/prohibition scope is declared in the Prompt.
- QD-P-1.4.1 | PASS | evidence: TC-035, no duplicate constraint found.
- QD-P-1.4.2 | PASS | evidence: TC-035, declared branches are reachable.
- QD-P-1.4.3 | PASS | evidence: TC-035, no Skill definition is given in the Prompt (vacuous).
- QD-P-1.5.1 | PASS | evidence: TC-035, the efficiency guidelines support the objective.
- QD-P-1.5.2 | FAIL | evidence: TC-035, the template injects `{commands}` / `{resources}` but defines no resource set inside the Prompt.
- QD-P-1.6.1 | PASS | evidence: TC-035, no vague word carries a security/permission decision.
- QD-P-1.6.2 | PASS | evidence: TC-035, no rule keys on unobservable model internal state.
- QD-P-1.6.3 | PASS | evidence: TC-035, no unresolved implicit Soft-Rule conflict found.
- QD-P-1.6.4 | PASS | evidence: TC-035, no internal reasoning-method constraint found.
- QD-P-1.6.5 | PASS | evidence: TC-035, no self-referential/recursive constraint found.
- QD-P-1.6.6 | FAIL | evidence: TC-035, "If a test fails, the bug is in your code, NOT in the test" assumes the test harness is always correct.
- QD-P-1.6.7 | PASS | evidence: TC-035, no rule requires revising earlier conclusions on new information.
- QD-P-2.1.1 | PASS | evidence: TC-035, prompt formatting is readable.
- QD-P-2.1.2 | PASS | evidence: TC-035, references (JSON schema, commands) are specific.
- QD-P-2.1.3 | PASS | evidence: TC-035, heading hierarchy is reasonable.
- QD-P-2.1.4 | PASS | evidence: TC-035, prose is concise.
- QD-P-2.2.1 | FAIL | evidence: TC-035, no input source (user / system / external data) is declared.
- QD-P-2.2.2 | PASS | evidence: TC-035, input is goal-driven (no structured parser required).
- QD-P-2.2.3 | PASS | evidence: TC-035, no parameterized input declared (not triggered).
- QD-P-2.2.4 | FAIL | evidence: TC-035, no missing-input handling is declared.
- QD-P-2.3.1 | PASS | evidence: TC-035, output format is declared ("respond using the JSON schema specified previously").
- QD-P-2.3.2 | FAIL | evidence: TC-035, only `AssistantThoughts` fields are shown; the action/command output schema is not defined.
- QD-P-2.3.3 | FAIL | evidence: TC-035, no output stability assurance is declared.
- QD-P-2.3.4 | FAIL | evidence: TC-035, no sensitive-data filtering or privacy handling is declared.
- QD-P-2.4.1 | FAIL | evidence: TC-035, no workflow step sequence is defined.
- QD-P-2.4.2 | FAIL | evidence: TC-035, the command/resource set is a placeholder and is not declared.
- QD-P-2.4.3 | FAIL | evidence: TC-035, no tool invocation parameters, sequence, or failure handling are defined.
- QD-P-2.5.1 | PASS | evidence: TC-035, "You have LIMITED steps" bounds the loop.
- QD-P-2.5.2 | FAIL | evidence: TC-035, no prohibited operations or access boundaries are declared.
- QD-P-2.5.3 | FAIL | evidence: TC-035, no permission scope is declared for the forge components.
- QD-P-2.5.4 | PASS | evidence: TC-035, no conflicting soft constraints requiring priority arbitration found.
- QD-P-2.5.5 | FAIL | evidence: TC-035, no resource invocation frequency limits are declared.
- QD-P-2.6.1 | FAIL | evidence: TC-035, no runtime exception handling is declared.
- QD-P-2.6.2 | FAIL | evidence: TC-035, no degradation/recovery strategy is declared.
- QD-P-2.6.3 | PASS | evidence: TC-035, no unreasonable retry mechanism found.
- QD-P-2.7.1 | FAIL | evidence: TC-035, no positive examples are provided.
- QD-P-2.7.2 | FAIL | evidence: TC-035, no counter-examples are provided.
- QD-P-2.7.3 | FAIL | evidence: TC-035, no boundary-case examples are provided.

### 3.A.2 Tool Schema - Forge components

Tier: **L3** (components include `code_executor`, `file_manager`, `git_operations`, `playwright_browser` - execution and irreversible-style operations). Scope = L3 (16 items).

- QD-T-1.1 | FAIL | evidence: TC-035, the Forge list gives component names + one-line descriptions with no `inputSchema`.
- QD-T-1.2 | FAIL | evidence: TC-035, no `properties`/`required` are declared.
- QD-T-1.3 | PASS | evidence: TC-035, no `enum` with duplicate/empty values is present.
- QD-T-1.4 | FAIL | evidence: TC-035, no `additionalProperties` declaration is present.
- QD-T-2.1 | N/A | evidence: TC-035, no typed string parameter is shown (determination basis: no parameter schema).
- QD-T-2.2 | N/A | evidence: TC-035, no typed string parameter is shown (determination basis: no parameter schema).
- QD-T-2.3 | N/A | evidence: TC-035, no typed number parameter is shown (determination basis: no parameter schema).
- QD-T-2.4 | N/A | evidence: TC-035, no typed array parameter is shown (determination basis: no parameter schema).
- QD-T-3.1 | FAIL | evidence: TC-035, `file_manager`/`git_operations`/`code_executor` modify state but declare no write-operation notice.
- QD-T-3.2 | FAIL | evidence: TC-035, `code_executor` "Execute code snippets" accepts raw input for direct execution.
- QD-T-3.3 | FAIL | evidence: TC-035, `code_executor`/`archive_handler` batch-style components declare no operation-count limit.
- QD-T-3.4 | N/A | evidence: TC-035, no control parameter (`tenantId`/`isAdmin`/`token`) is exposed (determination basis: no parameter schema).
- QD-T-3.5 | FAIL | evidence: TC-035, `file_manager` output may feed `code_executor` with no declared data-flow boundary.
- QD-T-4.1 | FAIL | evidence: TC-035, descriptions are terse, e.g. `code_executor` "Execute code snippets".
- QD-T-4.2 | FAIL | evidence: TC-035, side effects of `http_client`/`user_interaction` are not declared.
- QD-T-4.3 | FAIL | evidence: TC-035, near-synonym components (`file_manager` vs `archive_handler`) risk selection confusion.

### 3.A.3 Embedded code snippets (QC)

- QC-0.1 | PASS | evidence: TC-035, the `python` snippets parse as valid syntax.
- QC-0.2 | PASS | evidence: TC-035, snippets are fenced with `python`.
- QC-0.3 | FAIL | evidence: TC-035, `FileManagerComponent.__init__` body is truncated to a docstring.
- QC-1.1 | FAIL | evidence: TC-035, `SystemConfiguration`, `ModelWithSummary`, `Field`, `DirectiveProvider` are undefined in the snippets.
- QC-1.2 | PASS | evidence: TC-035, no unavailable-module import statement present.
- QC-1.3 | PASS | evidence: TC-035, no deprecated API usage present.
- QC-1.4 | PASS | evidence: TC-035, no type-mismatched call present.
- QC-2.1 | N/A | evidence: TC-035, no file-handle pattern in the shown code (determination basis: no such pattern).
- QC-2.2 | N/A | evidence: TC-035, no connection constructor opened without close (determination basis: no such pattern).
- QC-2.3 | N/A | evidence: TC-035, no high-risk file/network/DB call in the shown snippets (determination basis: no such pattern).
- QC-3.1 | PASS | evidence: TC-035, no unused import present.
- QC-3.2 | FAIL | evidence: TC-035, `SystemConfiguration`/`ModelWithSummary` are referenced but never imported/defined.
- QC-3.3 | PASS | evidence: TC-035, no hardcoded demo credential value present.

---

## 4. Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Run condition met: two same-agent artifact types are present (System Prompt + Tool Schema). No Skill is present, so QD-PS / QD-ST are not applicable. Tier = **L3** (Appendix C upgrades applied: Agent L3 -> global P1->P0, P2->P1).

### QD-PT (Prompt -> Tool)

- QD-PT-2.1 Tool Existence | PASS | evidence: Prompt (TC-035, `{commands}` placeholder) and Tool Schema (20 forge components) do not show an evident nonexistent-tool mismatch.
- QD-PT-2.2 Invocation Specification Consistency | FAIL (P0) | evidence: Prompt (TC-035, "respond using the JSON schema specified previously") vs Tool Schema (components with no `inputSchema`) - inconsistent.
- QD-PT-2.3 Parameter Constraint Consistency | FAIL (P0, upgraded from P1 by L3) | evidence: Prompt (TC-035) declares no parameter constraints; Tool Schema declares no parameter schema either.
- QD-PT-2.4 Permission Granularity Consistency | FAIL (P0) | evidence: high-risk Tool (`code_executor`) is present; the Prompt (TC-035) declares no security boundary for it.
- QD-PT-2.5 Error Handling Completeness | FAIL (P0, upgraded from P1 by L3) | evidence: Prompt (TC-035) covers no tool error types; Tool Schema declares none.
- QD-PT-2.6 Invocation Frequency Reasonableness | FAIL (P1, upgraded from P2 by L3) | evidence: Prompt declares no frequency limits; Tool Schema declares none.
- QD-PS-1.x | Not Applicable | evidence: no Skill present.
- QD-ST-3.x | Not Applicable | evidence: no Skill present.

### QD-CYC (circular invocation)

- QD-CYC-1.1 Cross-Artifact Circular Invocation | PASS | evidence: Prompt/Tool invocation relationships (TC-035) show no closed loop.
- QD-CYC-1.2 Multi-Agent Circular Invocation | PASS | evidence: the Prompt defines one agent role (TC-035); no orchestration cycle.

---

## 5. Stage C - Gate-0 (admission)

- G0-1 (no unfixed P0 in Stage A): NOT satisfied - recorded as an informational finding; does not gate this flow.
- G0-2 (no unfixed P0 in Stage B): NOT satisfied - recorded as an informational finding; does not gate this flow.
- G0-3 (responsibility boundary statements exist and are locatable): Passed - the constraints/resources/commands template and the project overview are locatable.
- G0-4 (each Tool Schema's `name`, `description`, parameter descriptions complete): NOT passed - the Forge components carry one-line descriptions and no parameter descriptions.

Gate-0 result: **Not passed - G0-4**.

---

## 6. Stage D - Permission (QD-PM Quick Mode)

Subset: Inspect Permission Governance Specification (QD-PM)
Execution Status: Not Executed
Unsatisfied Conditions: G0-4
Blocking Reasons:
  G0-4 - Tool Schema `name`/`description`/parameter descriptions are not complete (the forge component list has no parameter schemas).
Remediation Actions: Fix the above upstream items, then re-run Gate-0.

(This is not a FAIL and not a permission conclusion.)

---

## 7. Stage E - Risk Explicit audit (EX) - physically separated from Inspect verdicts

Audit object: TC-035 System Prompt set + Tool Schema.

Risk Item Summary:
- Total Risk Items: 0
- Explicit.P0 (Block release): 0 items
- Explicit.P1 (Fix / exemption): 0 items
- Explicit.P2 (Risk ledger): 0 items

No explicitly expressed risk text (NL-A / NL-B / NR-O / NR-S) was found in the shown artifacts. The `SECURITY: Never expose, log, or commit secrets` line is a protective constraint, not a risk expression; `code_executor` is a capability description, not an explicit risk instruction.

Note: This is a static-document risk scan of explicitly declared text only; it is not a confirmed exploit and not a security conclusion. Risk Implicit (dynamic exploitability) was NOT run.

---

## 8. Stage F - Impact outlook (candidate mapping, advisory only)

Advisory context only; it does not change, soften, or escalate any Inspect conclusion. Strength is association confidence, NOT severity. Candidate language only. Risk Implicit and the runtime Quality subsets were NOT run; the lite embedded-code QC ran in Stage A. Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent.

| Defect (FAIL) | Candidate attack surface (AS-*) | Candidate failure modes (FM-*) | Strength (provisional, lite) |
|---|---|---|---|
| QD-P-1.3.3, QD-P-1.6.6 | AS-01, AS-04 | FM-01, FM-02, FM-07, FM-09 | Medium |
| QD-P-1.5.2, QD-P-2.4.2 | AS-05, AS-07, AS-09 | FM-03, FM-04, FM-05 | Strong (resources/commands undeclared) |
| QD-P-2.2.1, QD-P-2.2.4 | AS-01, AS-02 | FM-01, FM-04 | Medium |
| QD-P-2.3.2, QD-P-2.3.3 | AS-03, AS-09 | FM-06 | Conditional |
| QD-P-2.3.4, QD-P-2.5.2, QD-P-2.5.3 | AS-01, AS-03, AS-04, AS-05 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.4.1, QD-P-2.4.3 | AS-05, AS-07, AS-09 | FM-03, FM-04, FM-05 | Strong |
| QD-P-2.5.5, QD-P-2.6.1, QD-P-2.6.2, QD-P-2.7.1, QD-P-2.7.2, QD-P-2.7.3 | AS-06, AS-07 | FM-08, FM-09, FM-10 | Conditional |
| QD-T-1.1, QD-T-1.2, QD-T-1.4 | AS-05, AS-09 | FM-03, FM-04, FM-05 | Strong |
| QD-T-3.1, QD-T-3.2, QD-T-3.3, QD-T-3.5 | AS-02, AS-03, AS-05 | FM-08, FM-09, FM-10 | Strong (exec/write without schema) |
| QD-T-4.1, QD-T-4.2, QD-T-4.3 | AS-05, AS-08 | FM-03, FM-05 | Medium |
| QC-0.3, QC-1.1, QC-3.2 | (no AS-* row in Appendix A; snippet-level only) | (no B.1 group) | Not Applicable (out of Appendix A mapping scope) |
| QD-PT-2.2, QD-PT-2.3 | AS-02, AS-05, AS-09 | FM-04, FM-05, FM-06, FM-08 | Strong |
| QD-PT-2.4 | AS-04, AS-05 | FM-04, FM-05, FM-06, FM-08 | Strong |
| QD-PT-2.5, QD-PT-2.6 | AS-06, AS-07 | FM-04, FM-05, FM-06, FM-08 | Medium |

Candidate RAG-Agent quality metrics (candidate associations only; NOT a quality result): Correctness, Completeness, Robustness, Boundary Recognition, Safety Response, Traceability. Defect chains (SC-*/QC-TA-*/QC-RA-*) are out of scope for lite v1.

---

## 9. Status board

Stage A (Single-artifact):  Executed - QD-P (L3), QD-T (Forge L3), QC.
Stage B (Cross):            Executed - two same-agent artifact types present (Prompt + Tool); QD-PS/QD-ST not applicable.
Stage C (Gate-0):           Not passed - G0-4 (G0-1/G0-2 informational).
Stage D (Permission QD-PM): Not Executed - Gate-0 G0-4 not satisfied.
Stage E (Risk Explicit EX): Executed - 0 findings.
Stage F (Impact outlook):   Executed - candidate mapping for all Stage A/B FAILs.
Stage G (Self-verification): Executed - ID back-closure, red-line wording, output contract checked.

---

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. No in-place self-corrections were required.
