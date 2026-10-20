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
- Finding counts (Stage A, System Prompt set): Inspect P0 = 14, P1 = 0, P2 = 0.
- Gate-0 result: Not passed (G0-3 passed; G0-4 not satisfied - no Tool Schema artifact is present; the roles attach toolkit references, not JSON `parameters` schemas).
- Risk-Explicit summary (Stage E): Explicit.P0 = 0, Explicit.P1 = 0, Explicit.P2 = 0.
- Top findings (rule ID - one-line defect):
  1. QD-P-2.5.2 / QD-P-2.5.3 - No security boundary or permission-control boundary is declared in the leader/role/order templates or the role profiles.
  2. QD-P-2.3.4 - No sensitive-data filtering or privacy output constraint is declared.
  3. QD-P-2.3.1 / QD-P-2.3.2 / QD-P-2.3.3 - No output format, output schema, or output-stability mechanism is declared for the subordinate role prompt ("Reply TERMINATE").
  4. QD-P-2.2.2 / QD-P-2.2.3 / QD-P-2.2.4 - Input format, required/optional marking and missing-input handling are all undeclared.
  5. QD-P-2.7.1 / QD-P-2.7.2 / QD-P-2.7.3 - No positive, counter, or boundary-case example is provided.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The lite embedded-code QC was run in Stage A.
- This report never states a security or quality conclusion; Inspect PASS is not Risk PASS and not Quality PASS.
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and version-level evidence chains, use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

---

## 2. Artifact inventory (input preparation, not a stage)

Case TC-090 bundles one financial-analysis multi-agent suite (FinRobot V0, the AutoGen generation). Artifact types present, by structural signature:

- System Prompt (present, verbatim): three templates in `agents/prompts.py` (`leader_system_message`, `role_system_message`, `order_template`) plus ten role profiles in `agents/agent_library.py` (e.g. `Data_Analyst`, `Market_Analyst`, `Expert_Investor`). Basis: prose/instruction strings assembled into each agent's `profile`.
- Skill (absent): no markdown file with `name`/`description` front matter defines an invokable capability. The "role library" is a data list, not a Skill.
- Tool Schema (absent): the roles carry `toolkits` lists of function/class references (e.g. `FinnHubUtils.get_company_news`); no JSON Schema / function-calling definition with a `parameters`/`description` block is shown.
- Orchestration config (reference, not an artifact type): `workflow.py` (`MultiAssistant`, `MultiAssistantWithLeader`, speaker-selection and nested-chat wiring).
- Embedded code snippets (QC scope): the `dedent` template strings, the `_preprocess_config` assembly, the speaker-selection function and the nested-chat registration.
- Out of coverage: `finrobot/agents/utils.py` (`order_trigger` / `order_message`), the toolkit implementations, and the elided portions of the `Expert_Investor` profile.

Scope note: all ten roles plus the leader are agents of one orchestrated FinRobot suite (one role library, two topologies sharing the same agents), so all artifacts belong to the same agent suite and no artifact from another case is mixed in.

---

## 3. Stage A - Single-artifact inspection

### 3.A.1 System Prompt set (leader/role/order templates + ten role profiles)

Tier determination: **L3 Complex Agent**. Basis (any 2 or more of the L3 criteria): 4+ tool invocations at suite level (the roles attach finhub/yfinance/FMP/ReportLab toolkits); complex workflow far exceeding 5 steps (leader issues ordered sub-tasks through nested chats, each up to `max_turns=10`); finance-sensitive (equity research, annual-report generation); requires exception handling/termination discipline (the `TERMINATE` convention and the nested-chat turn caps). Upward-compatible L3 scope = 47 items.

- QD-P-1.1.1 | PASS | evidence: TC-090, the templates + role profiles, no mutually exclusive attribute or directive found.
- QD-P-1.1.2 | PASS | evidence: TC-090, the leader rules (one order at a time; check results before the next order) do not conflict in any declared scenario.
- QD-P-1.1.3 | PASS | evidence: TC-090, no worked example contradicts a rule.
- QD-P-1.2.1 | PASS | evidence: TC-090, each role's title/identity matches its responsibility (leader coordinates; roles execute assigned tasks).
- QD-P-1.2.2 | PASS | evidence: TC-090, the role voice matches the declared reply style (ordered task responses ending in TERMINATE).
- QD-P-1.2.3 | PASS | evidence: TC-090, no constraint prohibits a role's core responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-090, the leader enforces one order at a time; no misused quantifier found.
- QD-P-1.3.2 | PASS | evidence: TC-090, the leader instruction "effectively and efficiently" is a secondary descriptor, not a decision boundary.
- QD-P-1.3.3 | PASS | evidence: TC-090, the order format and the nested-chat routing declare the hand-off boundary ("Orders should be follow the format: \"[<name of staff>] <order>\"").
- QD-P-1.4.1 | PASS | evidence: TC-090, no duplicate constraint found.
- QD-P-1.4.2 | PASS | evidence: TC-090, the declared branches (order / report-blocked / TERMINATE) are all reachable.
- QD-P-1.4.3 | PASS | evidence: TC-090, no Skill definition is given in the prompts (vacuous).
- QD-P-1.5.1 | PASS | evidence: TC-090, the roles' responsibilities support the objective (produce an ordered financial-analysis deliverable).
- QD-P-1.5.2 | PASS | evidence: TC-090, the workflow resources (role toolkits, executor, nested chats) are declared.
- QD-P-1.6.1 | PASS | evidence: TC-090, no vague word carries a security/permission boundary.
- QD-P-1.6.2 | PASS | evidence: TC-090, control flow keys on received orders and execution results, not unreportable internal state.
- QD-P-1.6.3 | PASS | evidence: TC-090, no soft rules are declared in mutually unreconciled tension.
- QD-P-1.6.4 | PASS | evidence: TC-090, no constraint fixes an internal reasoning method.
- QD-P-1.6.5 | PASS | evidence: TC-090, no self-referential or recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-090, the executor/local-save assumptions are stated in the order template ("executor will run it for you", "Save your results ... locally").
- QD-P-1.6.7 | PASS | evidence: TC-090, the leader declares a revision step - "After receiving feedback from a team member, check the results of the task, and make sure it has been well completed before proceding to th next order."
- QD-P-2.1.1 | PASS | evidence: TC-090, formatting is readable.
- QD-P-2.1.2 | PASS | evidence: TC-090, references (`{group_desc}`, `{title}`, `{responsibilities}`, `{order}`) are named and filled deterministically.
- QD-P-2.1.3 | PASS | evidence: TC-090, the section hierarchy (leader instructions / role responsibilities / order template) is reasonable.
- QD-P-2.1.4 | PASS | evidence: TC-090, prose is concise.
- QD-P-2.2.1 | PASS | evidence: TC-090, the input source is declared - the order template begins "Follow leader's order and complete the following task with your group members: {order}".
- QD-P-2.2.2 | FAIL | evidence: TC-090, no input data format, encoding or size limit is declared for the `{order}`/`{responsibilities}` inputs.
- QD-P-2.2.3 | FAIL | evidence: TC-090, no input field or placeholder is marked required or optional.
- QD-P-2.2.4 | FAIL | evidence: TC-090, no behavior is declared when the input is empty or missing (only the "task cannot be done" branch is defined).
- QD-P-2.3.1 | FAIL | evidence: TC-090, the subordinate role prompt declares no output format - role_system_message ends "Reply \"TERMINATE\" in the end when everything is done."
- QD-P-2.3.2 | FAIL | evidence: TC-090, no output schema is declared for the role/leader outputs.
- QD-P-2.3.3 | FAIL | evidence: TC-090, no output format/content stability or consistency-check mechanism is declared.
- QD-P-2.3.4 | FAIL | evidence: TC-090, no sensitive-data filtering, privacy handling, or security output constraint is declared.
- QD-P-2.4.1 | PASS | evidence: TC-090, the leader template declares the coordination workflow steps (summarize status -> issue one order -> verify results -> terminate).
- QD-P-2.4.2 | PASS | evidence: TC-090, the resources/tools used are declared per role via the `toolkits` lists.
- QD-P-2.4.3 | FAIL | evidence: TC-090, the roles name toolkits but declare no invocation parameter specification or tool-failure handling (only "For coding tasks, provide python scripts and executor will run it for you.").
- QD-P-2.5.1 | PASS | evidence: TC-090, the `TERMINATE` convention declares the termination condition (no loop declared in the prompt itself).
- QD-P-2.5.2 | FAIL | evidence: TC-090, no prohibited operation, sensitive-data access boundary, or external-access boundary is declared by any template or profile.
- QD-P-2.5.3 | FAIL | evidence: TC-090, no permission scope or escalation boundary is declared.
- QD-P-2.5.4 | PASS | evidence: TC-090, no soft-constraint conflict requires an arbitration rule.
- QD-P-2.5.5 | FAIL | evidence: TC-090, no external data/toolkit invocation frequency limit is declared.
- QD-P-2.6.1 | PASS | evidence: TC-090, the order template declares failure handling - "If the task cannot be done currently or need assistance from other members, report the reasons or requirements to group leader ended with TERMINATE."
- QD-P-2.6.2 | PASS | evidence: TC-090, the same template declares a recovery path (report reasons/requirements back to the leader).
- QD-P-2.6.3 | PASS | evidence: TC-090, no retry mechanism is declared (vacuous).
- QD-P-2.7.1 | FAIL | evidence: TC-090, no representative worked example is provided (only the leader's order-format skeleton).
- QD-P-2.7.2 | FAIL | evidence: TC-090, no counter-examples are provided.
- QD-P-2.7.3 | FAIL | evidence: TC-090, no boundary-case examples are provided.

### 3.A.2 Skill

- QD-S-1.x .. QD-S-5.x | N/A | evidence: TC-090 carries no Skill artifact (determination basis: no markdown file with `name`/`description` front matter defines an invokable capability; the role library is a data list). No QD-S verdict is emitted.

### 3.A.3 Tool Schema

- QD-T-1.x .. QD-T-4.x | N/A | evidence: TC-090 carries no Tool Schema artifact (determination basis: the `toolkits` lists reference functions/classes but show no JSON `parameters`/`inputSchema` schema or per-parameter description). No QD-T verdict is emitted.

### 3.A.4 Embedded code snippets (QC)

QC-0 baseline: the Python snippets (template strings, `_preprocess_config`, speaker-selection, nested-chat registration) are fenced as `python`.

- QC-0.1 | PASS | evidence: TC-090, the snippets parse as valid Python syntax.
- QC-0.2 | PASS | evidence: TC-090, the code blocks declare `python`.
- QC-0.3 | PASS | evidence: TC-090, each shown function/assignment is complete within its excerpt.
- QC-0.4 | PASS | evidence: TC-090, the code fences open and close correctly.
- QC-0.5 | PASS | evidence: TC-090, the declared language (`python`) matches the content.
- QC-1.1 | PASS | evidence: TC-090, the only names undefined within the snippets are framework symbols (`autogen`, `partial`) whose imports are outside the excerpt.
- QC-1.2 | Not Executed | evidence: TC-090, no declared dependency list is available (dependency-context rule); not recorded as FAIL.
- QC-1.3 | Not Executed | evidence: TC-090, no API version database is available (dependency-context rule); not recorded as FAIL.
- QC-1.4 | PASS | evidence: TC-090, no type-mismatched call found.
- QC-2.1 .. QC-2.3 | N/A | evidence: TC-090, no file-handle, network-connection or high-risk call pattern is present in the snippets (determination basis: no such pattern).
- QC-3.1 | N/A | evidence: TC-090, imports are outside the excerpt, so no unused-import determination is made.
- QC-3.2 | PASS | evidence: TC-090, framework symbols (`autogen`, `partial`) are referenced without visible imports because the excerpt omits the module header.
- QC-3.3 | PASS | evidence: TC-090, the only literals are configuration values (turn caps, format strings), not credentials or machine-specific secrets.
- QC-4.1 | PASS | evidence: TC-090, the order-format string `[<name of staff>] <order>` matches the nested-chat trigger pattern `f\"[{agent.name}]\"`.
- QC-4.2 | PASS | evidence: TC-090, no version/API drift between the snippets and the body.

---

## 4. Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Stage status: **Not Executed**. Reason: only one Logic Artifact type (System Prompt) is present; the role `toolkits` are references without a Tool Schema, so no Prompt/Skill/Tool pair exists and QD-PS (Prompt -> Skill), QD-PT (Prompt -> Tool), QD-ST (Skill <-> Tool) and QD-CYC-1.1 have no counterpart artifact.

Informational observation (not a Stage B verdict line): QD-CYC-1.2 (Multi-Agent Circular Invocation) was reviewed at suite level - the GroupChat speaker-selection round-robins (`groupchat.next_agent(last_speaker, groupchat.agents[:-1])`) and the leader-based topology issues nested-chat orders; both terminate on the `TERMINATE` token, and no unbounded bidirectional role cycle (Agent A calls Agent B and back) is declared. No closed loop was found.

---

## 5. Stage C - Gate-0 (admission)

- G0-1 (no unfixed P0 in Stage A): NOT satisfied - recorded as an informational finding; does not gate this flow.
- G0-2 (no unfixed P0 in Stage B): N/A - Stage B did not run; recorded as informational.
- G0-3 (responsibility boundary statements exist and are locatable): Passed - the leader template ("You are the leader of the following group members:") and each role profile ("As a {title}, your reponsibilities are as follows:") state role and scope.
- G0-4 (each Tool Schema's `name`, `description`, parameter descriptions complete): NOT passed - no Tool Schema artifact is present (the roles attach toolkit references with no parameter schema).

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

Audit object: TC-090 System Prompt set (leader/role/order templates + ten role profiles) + embedded snippets.
Three-phase scan (NL-A -> NL-B -> NR-O -> NR-S) run over the bundled artifacts.

Risk Item Summary:
- Total Risk Items: 0
- Explicit.P0 (Block release): 0 items
- Explicit.P1 (Fix / exemption): 0 items
- Explicit.P2 (Risk ledger): 0 items

Note: no explicitly declared risk expression (self-contained exfiltration, identity/permission claim, constraint removal, priority override, dangerous flag, hardcoded credential/PII, or abnormal callback) was found in the static artifact text. The order template's instruction to write local intermediate files and let the executor run generated Python scripts is an ordinary workflow instruction, not a risk expression matching a defined EX subcategory. This is a static-document scan only; it is not a security conclusion. Risk Implicit (dynamic exploitability) was NOT run.

---

## 8. Stage F - Impact outlook (candidate mapping, advisory only)

Advisory context only; it does not change, soften, or escalate any Inspect conclusion. Strength is association confidence, NOT severity. Candidate language only. Risk Implicit and the runtime Quality subsets were NOT run; the lite embedded-code QC ran in Stage A. Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent.

| Defect (FAIL) | Candidate attack surface (AS-*) | Candidate failure modes (FM-*) | Strength (provisional, lite) |
|---|---|---|---|
| QD-P-2.2.2, QD-P-2.2.3, QD-P-2.2.4 | AS-02, AS-07 | FM-01, FM-04 | Medium (input format/necessity/missing handling undeclared) |
| QD-P-2.3.1, QD-P-2.3.2, QD-P-2.3.3 | AS-03, AS-09 | FM-06 | Medium |
| QD-P-2.3.4 | AS-03 | FM-06 | Conditional |
| QD-P-2.4.3 | AS-05, AS-07, AS-09 | FM-03, FM-04, FM-05 | Medium |
| QD-P-2.5.2, QD-P-2.5.3 | AS-01, AS-03, AS-04, AS-05 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.5.5 | AS-06 | FM-08, FM-09, FM-10 | Conditional |
| QD-P-2.7.1, QD-P-2.7.2, QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |

Candidate RAG-Agent quality metrics (candidate associations only; NOT a quality result): Correctness, Completeness, Consistency, Traceability, Robustness, Format Compliance, Boundary Recognition, Safety Response. Defect chains (SC-*/QC-TA-*/QC-RA-*) are out of scope for lite v1.

---

## 9. Status board

Stage A (Single-artifact):  Executed - QD-P (L3, leader/role/order templates + 10 profiles), QD-T (N/A, no Tool Schema), QD-S (N/A, no Skill), QC (embedded Python snippets).
Stage B (Cross):            Not Executed - only one artifact type present (System Prompt); no Prompt/Skill/Tool pair exists.
Stage C (Gate-0):           Not passed - G0-4 (G0-1/G0-2 informational).
Stage D (Permission QD-PM): Not Executed - Gate-0 G0-4 not satisfied; full artifact set incomplete (no Skill, no Tool Schema).
Stage E (Risk Explicit EX): Executed - 0 findings.
Stage F (Impact outlook):   Executed - candidate mapping for all Stage A FAILs.
Stage G (Self-verification): Executed - ID back-closure, red-line wording, output contract checked.

---

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. No in-place self-corrections were required.
