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
- Finding counts (Stage A): System Prompt set (L3) Inspect P0 = 10, P1 = 0, P2 = 0; Tool Schema set (L3) P0 = 2, P1 = 1, P2 = 0. Stage A total P0 = 12, P1 = 1, P2 = 0.
- Gate-0 result: Not passed (G0-3 passed; G0-4 not satisfied - the quoted `@function_tool` schemas carry names and tool descriptions, but no parameter descriptions for the full tool set).
- Risk-Explicit summary (Stage E): Explicit.P0 = 0, Explicit.P1 = 0, Explicit.P2 = 0.
- Top findings (rule ID - one-line defect):
  1. QD-P-2.5.2 / QD-P-2.5.3 - No security boundary or permission-control boundary is declared for agents that can cancel flights and issue compensation.
  2. QD-P-1.5.2 - The prompts route to a "Baggage Agent" that is not defined anywhere in the suite.
  3. QD-P-2.2.2 / QD-P-2.3.1 - The free-form customer message has no declared format, and the conversational agents declare no output format.
  4. QD-T-2.1 / QD-T-3.1 - String parameters carry no length constraint, and write/irreversible tools carry no explicit write-operation notice.
  5. QD-PT-2.4 - A high-risk tool (`cancel_flight`) has no security-boundary declaration in the Prompt.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The lite embedded-code QC was run in Stage A.
- This report never states a security or quality conclusion; Inspect PASS is not Risk PASS and not Quality PASS.
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and version-level evidence chains, use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

---

## 2. Artifact inventory (input preparation, not a stage)

Case TC-092 bundles one multi-agent airline customer-service suite (OpenAI `openai-cs-agents-demo`). Artifact types present, by structural signature:

- System Prompt (present, verbatim): six conversational agent instructions (Seat & Special Services, Flight Information, Booking & Cancellation, Refunds & Compensation, FAQ, Triage) plus two guardrail instructions (Relevance Guardrail, Jailbreak Guardrail). Basis: prose/instruction strings in `agents.py` / `guardrails.py`.
- Tool Schema (present, representative): the `@function_tool` declarations in `tools.py` (`faq_lookup_tool`, `update_seat`, `flight_status_tool`, `get_matching_flights`, `assign_special_service_seat`, `issue_compensation`, `display_seat_map`, `cancel_flight`, plus `get_trip_details`, `baggage_tool`, `book_new_flight`). Basis: function-calling definitions with `name_override`/`description_override` and type-annotated parameters.
- Handoff topology (present): the handoff wiring in `agents.py`. Basis: orchestration declaration, not a standalone artifact type.
- Skill (absent): no markdown file with `name`/`description` front matter defines an invokable capability.
- Embedded code snippets (QC scope): the instruction strings, the `@function_tool` bodies, the guardrail `Agent(...)` definitions.
- Out of coverage: `RECOMMENDED_PROMPT_PREFIX` (imported from the Agents SDK, not part of this repository) and several tool bodies (elided with `...`).

Scope note: all six conversational agents + two guardrails are coordinated by one handoff topology in the same SDK pipeline, so all artifacts belong to the same agent suite and no artifact from another case is mixed in.

---

## 3. Stage A - Single-artifact inspection

### 3.A.1 System Prompt set (six agent instructions + two guardrails)

Tier determination: **L3 Complex Agent**. Basis (any 2 or more of the L3 criteria): 4+ tool invocations; complex workflow exceeding 5 steps (Triage -> specialist -> specialist <-> specialist -> Triage); security/finance-sensitive (cancellations and compensation); input guardrails enforce exception/security handling. Upward-compatible L3 scope = 47 items.

- QD-P-1.1.1 | PASS | evidence: TC-092, the prompts, no mutually exclusive attribute or directive found.
- QD-P-1.1.2 | PASS | evidence: TC-092, the "one handoff per message" rule and the autonomy rules do not conflict in any declared scenario.
- QD-P-1.1.3 | PASS | evidence: TC-092, no worked example contradicts a rule.
- QD-P-1.2.1 | PASS | evidence: TC-092, each agent identity matches its stated responsibility (Seat & Special Services, Flight Information, Booking & Cancellation, Refunds & Compensation, FAQ, Triage).
- QD-P-1.2.2 | PASS | evidence: TC-092, the agent voice matches the declared customer-service style.
- QD-P-1.2.3 | PASS | evidence: TC-092, no constraint prohibits an agent's core responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-092, the handoff count is bounded - "emit at most one handoff".
- QD-P-1.3.2 | PASS | evidence: TC-092, the vague term "clear" gates the autonomy decision, while the primary trigger ("data is present"/"data is available") is concrete.
- QD-P-1.3.3 | PASS | evidence: TC-092, handoff conditions are named (Refunds & Compensation / Baggage / back to Triage).
- QD-P-1.4.1 | PASS | evidence: TC-092, no duplicate constraint found.
- QD-P-1.4.2 | PASS | evidence: TC-092, all declared routing branches are reachable.
- QD-P-1.4.3 | PASS | evidence: TC-092, no Skill definition is given in the prompts (vacuous).
- QD-P-1.5.1 | PASS | evidence: TC-092, the agents' responsibilities support the objective (resolve the customer's airline request).
- QD-P-1.5.2 | FAIL | evidence: TC-092, the Seat and Booking instructions route to an agent that is not defined - "hand off to the Baggage Agent" / "to Baggage if baggage help is pending", although the suite defines only a `baggage_tool`, not a Baggage Agent.
- QD-P-1.6.1 | PASS | evidence: TC-092, no vague word carries a security/permission boundary.
- QD-P-1.6.2 | PASS | evidence: TC-092, decisions key on declared context fields (confirmation, flight, seat) and tool results.
- QD-P-1.6.3 | PASS | evidence: TC-092, no soft rules are declared in mutually unreconciled tension.
- QD-P-1.6.4 | PASS | evidence: TC-092, no constraint fixes an internal reasoning method.
- QD-P-1.6.5 | PASS | evidence: TC-092, no self-referential or recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-092, the assumed presence of confirmation/flight/seat is handled - "If any of these are missing, ask to confirm."
- QD-P-1.6.7 | PASS | evidence: TC-092, handoffs and re-routing allow revision during the conversation.
- QD-P-2.1.1 | PASS | evidence: TC-092, formatting is readable.
- QD-P-2.1.2 | PASS | evidence: TC-092, references (`${confirmation}`, `${flight}`, handoff targets, tool names) are named and locatable.
- QD-P-2.1.3 | PASS | evidence: TC-092, the section hierarchy (role -> numbered routine -> autonomy/handoff rule) is reasonable.
- QD-P-2.1.4 | PASS | evidence: TC-092, prose is concise.
- QD-P-2.2.1 | PASS | evidence: TC-092, the input source is declared (the customer message plus the injected context fields).
- QD-P-2.2.2 | FAIL | evidence: TC-092, the free-form customer message carries no declared format, encoding or size limit.
- QD-P-2.2.3 | PASS | evidence: TC-092, required-ness is handled - "If any of these are missing, ask to confirm. If present, act without re-asking."
- QD-P-2.2.4 | PASS | evidence: TC-092, missing-input handling is declared (ask to confirm / proceed when present).
- QD-P-2.3.1 | FAIL | evidence: TC-092, the six conversational agent instructions declare no output format for the customer reply (the guardrails do declare structured outputs, so the set is mixed).
- QD-P-2.3.2 | PASS | evidence: TC-092, the guardrail agents declare structured output schemas (`RelevanceOutput`, `JailbreakOutput`); the conversational reply is natural language (determination basis: no incomplete declared schema).
- QD-P-2.3.3 | PASS | evidence: TC-092, the "one handoff per message" convention and the guardrail output schemas bound output stability.
- QD-P-2.3.4 | PASS | evidence: TC-092, the declared relevance and jailbreak input guardrails provide a security filtering mechanism (note: they cover relevance/jailbreak, not PII handling).
- QD-P-2.4.1 | PASS | evidence: TC-092, each agent's workflow steps are complete (identify need -> tool calls -> confirm -> handoff).
- QD-P-2.4.2 | PASS | evidence: TC-092, each agent's tools are declared per role (e.g. Triage `get_trip_details`; Seat `update_seat`, `assign_special_service_seat`, `display_seat_map`).
- QD-P-2.4.3 | PASS | evidence: TC-092, the prompts specify which tool to call and when ("Use flight_status_tool immediately"; "use update_seat for standard changes").
- QD-P-2.5.1 | PASS | evidence: TC-092, the "one handoff per message" rule and the capped single-turn prep bound termination.
- QD-P-2.5.2 | FAIL | evidence: TC-092, no prohibited operation, sensitive-data access boundary, or external-access boundary is declared for agents that can cancel flights and issue compensation.
- QD-P-2.5.3 | FAIL | evidence: TC-092, no permission scope or escalation boundary is declared.
- QD-P-2.5.4 | PASS | evidence: TC-092, no soft-constraint conflict requires an arbitration rule.
- QD-P-2.5.5 | FAIL | evidence: TC-092, no tool-invocation frequency limit is declared although the prompts encourage autonomy - "perform multiple tool calls in a single turn without waiting for user replies".
- QD-P-2.6.1 | FAIL | evidence: TC-092, no handling is declared for tool-invocation failures (the case notes `cancel_flight` can raise an assertion failure).
- QD-P-2.6.2 | PASS | evidence: TC-092, the handoff/return-to-Triage path provides a declared recovery route ("otherwise back to Triage" / "transfer back to the Triage Agent").
- QD-P-2.6.3 | PASS | evidence: TC-092, no retry mechanism is declared (vacuous).
- QD-P-2.7.1 | FAIL | evidence: TC-092, no representative worked example is provided.
- QD-P-2.7.2 | FAIL | evidence: TC-092, no counter-examples are provided.
- QD-P-2.7.3 | FAIL | evidence: TC-092, no boundary-case examples are provided.

### 3.A.2 Tool Schema set (`@function_tool` declarations)

Tier determination: **L3 High Risk**. Basis: the tool set contains irreversible/financial operations - `cancel_flight` (irreversible) and `issue_compensation` (financial support), alongside write tools (`update_seat`, `book_new_flight`, `assign_special_service_seat`) and read-only tools (`faq_lookup_tool`, `flight_status_tool`, `get_matching_flights`, `get_trip_details`). Highest contained operation -> L3; L3 minimal set = 16 items.

- QD-T-1.1 | PASS | evidence: TC-092, each quoted tool has a name and a description (`name_override`/`description_override` or docstring).
- QD-T-1.2 | PASS | evidence: TC-092, the declared parameters match the function signatures (e.g. `update_seat(context, confirmation_number, new_seat)`); no `required`/`properties` inconsistency.
- QD-T-1.3 | PASS | evidence: TC-092, no `enum` constraint is declared.
- QD-T-1.4 | PASS | evidence: TC-092, the tools are function-signature definitions, which do not accept unlisted parameters (determination basis: no object-type parameter with uncontrolled `additionalProperties`).
- QD-T-2.1 | FAIL | evidence: TC-092, string parameters carry no length bound - `update_seat(context, confirmation_number: str, new_seat: str)` (and `flight_number`, `origin`, `destination`, `question`, `reason`) have no `maxLength`/`minLength`.
- QD-T-2.2 | FAIL | evidence: TC-092, format-bearing parameters carry no `pattern`/`format` - `confirmation_number: str` and `flight_number: str` require a specific format but declare none.
- QD-T-2.3 | N/A | evidence: TC-092, no number-type parameter is present (determination basis: no such parameter).
- QD-T-2.4 | N/A | evidence: TC-092, no array-type parameter is present (determination basis: no such parameter).
- QD-T-3.1 | FAIL | evidence: TC-092, write/irreversible tools carry no explicit write-operation notice - `cancel_flight` description "Cancel a flight." and `update_seat` description "Update the seat for a given confirmation number." do not carry a "[This operation will modify data...]" statement.
- QD-T-3.2 | PASS | evidence: TC-092, `faq_lookup_tool(question: str)` matches the free-form question locally rather than passing it through to a backend interpreter.
- QD-T-3.3 | N/A | evidence: TC-092, no batch-operation tool is present (determination basis: no such tool).
- QD-T-3.4 | PASS | evidence: TC-092, no internal control parameter (`tenantId`, `isAdmin`, `token`) is exposed; context is passed via `RunContextWrapper`.
- QD-T-3.5 | PASS | evidence: TC-092, no sensitive-field cross-tool data flow (e.g. email resolution feeding a notifier) is declared.
- QD-T-4.1 | PASS | evidence: TC-092, the tool descriptions are specific and non-ambiguous.
- QD-T-4.2 | PASS | evidence: TC-092, declared side effects are stated (`issue_compensation` "Create a compensation case and issue hotel/meal vouchers."; `display_seat_map` "Trigger the UI to show an interactive seat map").
- QD-T-4.3 | PASS | evidence: TC-092, no two tools have semantically competing names/descriptions among the quoted set.

### 3.A.3 Skill

- QD-S-1.x .. QD-S-5.x | N/A | evidence: TC-092 carries no Skill artifact (determination basis: no markdown file with `name`/`description` front matter defines an invokable capability). No QD-S verdict is emitted.

### 3.A.4 Embedded code snippets (QC)

QC-0 baseline: the Python snippets (instruction factories, `@function_tool` bodies, guardrail `Agent(...)` definitions) are fenced as `python`.

- QC-0.1 | PASS | evidence: TC-092, the snippets parse as valid Python syntax.
- QC-0.2 | PASS | evidence: TC-092, the code blocks declare `python`.
- QC-0.3 | PASS | evidence: TC-092, the snippets are marked as elided with `...`, which exempts them from standalone parse-completeness.
- QC-0.4 | PASS | evidence: TC-092, the code fences open and close correctly.
- QC-0.5 | PASS | evidence: TC-092, the declared language (`python`) matches the content.
- QC-1.1 | PASS | evidence: TC-092, the only names undefined within the snippets are framework/app symbols (`Agent`, `RunContextWrapper`, `function_tool`, `RECOMMENDED_PROMPT_PREFIX`) whose imports are elided.
- QC-1.2 | Not Executed | evidence: TC-092, no declared dependency list is available (dependency-context rule); not recorded as FAIL.
- QC-1.3 | Not Executed | evidence: TC-092, no API version database is available (dependency-context rule); not recorded as FAIL.
- QC-1.4 | PASS | evidence: TC-092, no type-mismatched call found.
- QC-2.1 .. QC-2.3 | N/A | evidence: TC-092, no file-handle, network-connection or high-risk call pattern is present in the snippets (determination basis: no such pattern).
- QC-3.1 | N/A | evidence: TC-092, imports are elided, so no unused-import determination is made.
- QC-3.2 | PASS | evidence: TC-092, framework/app symbols are referenced without visible imports because the snippets are elided with `...`.
- QC-3.3 | PASS | evidence: TC-092, the only literals are functional example strings (FAQ answers, "DISPLAY_SEAT_MAP"); no credential or machine-specific secret.
- QC-4.1 | PASS | evidence: TC-092, the tool `name_override` values match the agent `tools=[...]` bindings.
- QC-4.2 | PASS | evidence: TC-092, no version/API drift between the snippets and the body.

---

## 4. Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Stage status: **Executed** (Prompt <-> Tool pairs exist). Tier L3 -> L3 full scope; QD-PS and QD-ST are Not Applicable (no Skill artifact).

- QD-PS-1.x (Prompt -> Skill) | N/A | evidence: TC-092, no Skill artifact exists (determination basis: no Prompt <-> Skill pair).
- QD-PT-2.1 | PASS | evidence: TC-092, every tool named in the prompts (flight_status_tool, get_matching_flights, book_new_flight, cancel_flight, update_seat, assign_special_service_seat, display_seat_map, issue_compensation, faq_lookup_tool, get_trip_details) exists in `tools.py`.
- QD-PT-2.2 | PASS | evidence: TC-092, the prompt-side tool invocations (names and intended arguments) match the Tool Schema names/description.
- QD-PT-2.3 | PASS | evidence: TC-092, the prompt declares no parameter constraints that conflict with the Tool `inputSchema`.
- QD-PT-2.4 | FAIL | evidence: TC-092, the high-risk Tool `cancel_flight` (irreversible) has no security-boundary declaration in the Prompt (the Booking prompt only says "use cancel_flight").
- QD-PT-2.5 | FAIL | evidence: TC-092, the prompts do not cover the tools' possible error types (e.g. cancellation with no flight number).
- QD-PT-2.6 | FAIL | evidence: TC-092, no invocation frequency limit is declared in the prompts for the tool-calling agents.
- QD-ST-3.x (Skill <-> Tool) | N/A | evidence: TC-092, no Skill artifact exists (determination basis: no Skill <-> Tool pair).
- QD-CYC-1.1 | PASS | evidence: TC-092, no cross-artifact circular invocation (Skill output re-entering the Prompt, or a Tool callback re-triggering the Prompt) is declared.
- QD-CYC-1.2 | PASS | evidence: TC-092, although the handoff graph is cyclic (Triage <-> specialists), every instruction caps handoffs at "one handoff per message" and includes a path back to Triage; no unbounded mutual loop is declared.

---

## 5. Stage C - Gate-0 (admission)

- G0-1 (no unfixed P0 in Stage A): NOT satisfied - recorded as an informational finding; does not gate this flow.
- G0-2 (no unfixed P0 in Stage B): NOT satisfied (QD-PT-2.4/2.5 at L3) - recorded as an informational finding; does not gate this flow.
- G0-3 (responsibility boundary statements exist and are locatable): Passed - each agent states its role (e.g. "You are the Seat & Special Services Agent. Handle seat changes and medical/special service requests."; "You are a helpful triaging agent.").
- G0-4 (each Tool Schema's `name`, `description`, parameter descriptions complete): NOT passed - the quoted tools carry names and tool descriptions but no parameter descriptions for the full tool set.

Gate-0 result: **Not passed - G0-4**.

---

## 6. Stage D - Permission (QD-PM Quick Mode)

Subset: Inspect Permission Governance Specification (QD-PM)
Execution Status: Not Executed
Unsatisfied Conditions: G0-4 (structural admission); additionally the full artifact set is incomplete (no Skill).
Blocking Reasons:
  G0-4 - Tool Schema `name`/`description`/parameter descriptions are not complete (parameters are typed but not described).
  Artifact-set precondition - the full set (Prompt + Skill + all Tool Schemas) is not present (no Skill artifact).
Remediation Actions: Fix the above upstream items, then re-run Gate-0.

(The Permission stage was "Not Executed"; this is not a FAIL and not a permission conclusion.)

---

## 7. Stage E - Risk Explicit audit (EX) - physically separated from Inspect verdicts

Audit object: TC-092 System Prompt set (six agents + two guardrails) + Tool Schema set + embedded snippets.
Three-phase scan (NL-A -> NL-B -> NR-O -> NR-S) run over the bundled artifacts.

Risk Item Summary:
- Total Risk Items: 0
- Explicit.P0 (Block release): 0 items
- Explicit.P1 (Fix / exemption): 0 items
- Explicit.P2 (Risk ledger): 0 items

Note: no explicitly declared risk expression (self-contained exfiltration, identity/permission claim, constraint removal, priority override, dangerous flag, hardcoded credential/PII, or abnormal callback) was found in the static artifact text. The jailbreak-guardrail instruction quotes "drop table users;" only as a detection example, not as an instruction to execute; the relevance/jailbreak guardrails are defensive controls, not risk expressions. This is a static-document scan only; it is not a security conclusion. Risk Implicit (dynamic exploitability) was NOT run.

---

## 8. Stage F - Impact outlook (candidate mapping, advisory only)

Advisory context only; it does not change, soften, or escalate any Inspect conclusion. Strength is association confidence, NOT severity. Candidate language only. Risk Implicit and the runtime Quality subsets were NOT run; the lite embedded-code QC ran in Stage A. Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent.

| Defect (FAIL) | Candidate attack surface (AS-*) | Candidate failure modes (FM-*) | Strength (provisional, lite) |
|---|---|---|---|
| QD-P-1.5.2 | AS-05, AS-07, AS-09 | FM-03, FM-04, FM-05 | Medium (workflow step references an undefined agent) |
| QD-P-2.2.2 | AS-02, AS-07 | FM-01, FM-04 | Conditional |
| QD-P-2.3.1 | AS-03, AS-09 | FM-06 | Conditional |
| QD-P-2.5.2, QD-P-2.5.3 | AS-01, AS-03, AS-04, AS-05 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.5.5, QD-P-2.6.1 | AS-06, AS-07 | FM-08, FM-10 | Conditional |
| QD-P-2.7.1, QD-P-2.7.2, QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |
| QD-T-2.1, QD-T-2.2 | AS-02, AS-06 | FM-03, FM-04, FM-05 | Conditional (parameter constraints absent) |
| QD-T-3.1 | AS-05 | FM-08, FM-09, FM-10 | Medium (write/irreversible operation not flagged) |
| QD-PT-2.4 | AS-04, AS-05 | FM-04, FM-05, FM-06, FM-08 | Medium |
| QD-PT-2.5, QD-PT-2.6 | AS-06, AS-07 | FM-04, FM-05, FM-06, FM-08 | Conditional |

Candidate RAG-Agent quality metrics (candidate associations only; NOT a quality result): Correctness, Completeness, Consistency, Robustness, Boundary Recognition, Safety Response. Defect chains (SC-*/QC-TA-*/QC-RA-*) are out of scope for lite v1.

---

## 9. Status board

Stage A (Single-artifact):  Executed - QD-P (L3, 6 agents + 2 guardrails), QD-T (L3, function tools), QD-S (N/A, no Skill), QC (embedded Python snippets).
Stage B (Cross):            Executed - QD-PT (Prompt -> Tool); QD-PS/QD-ST N/A (no Skill); QD-CYC-1.1/1.2 evaluated.
Stage C (Gate-0):           Not passed - G0-4 (G0-1/G0-2 informational).
Stage D (Permission QD-PM): Not Executed - Gate-0 G0-4 not satisfied; full artifact set incomplete (no Skill).
Stage E (Risk Explicit EX): Executed - 0 findings.
Stage F (Impact outlook):   Executed - candidate mapping for all Stage A/B FAILs.
Stage G (Self-verification): Executed - ID back-closure, red-line wording, output contract checked.

---

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. No in-place self-corrections were required.
