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
- Finding counts (Stage A, System Prompt set): Inspect P0 = 11, P1 = 1, P2 = 0.
- Gate-0 result: Not passed (G0-3 passed; G0-4 not satisfied - no Tool Schema artifact is present; the agents own mock "domain databases" but expose no JSON `parameters` schema).
- Risk-Explicit summary (Stage E): Explicit.P0 = 0, Explicit.P1 = 0, Explicit.P2 = 0.
- Top findings (rule ID - one-line defect):
  1. QD-P-2.5.2 / QD-P-2.5.3 - No security boundary or permission-control boundary is declared in any specialized prompt.
  2. QD-P-2.3.4 - No sensitive-data filtering or privacy output constraint is declared for agents handling billing/complaint data.
  3. QD-P-2.2.2 / QD-P-2.2.3 / QD-P-2.2.4 - Input format, required/optional marking and missing-input handling are all undeclared.
  4. QD-P-2.3.1 - No output format is declared for the customer-facing reply.
  5. QD-P-2.7.1 / QD-P-2.7.2 / QD-P-2.7.3 - No positive, counter, or boundary-case example is provided.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The lite embedded-code QC was run in Stage A.
- This report never states a security or quality conclusion; Inspect PASS is not Risk PASS and not Quality PASS.
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and version-level evidence chains, use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

---

## 2. Artifact inventory (input preparation, not a stage)

Case TC-095 bundles one multi-agent customer-service suite (`handsomestWei/customer-service-ai-agent`, `multi_agents/`). Artifact types present, by structural signature:

- System Prompt (present, verbatim): one shared base context-enhancement instruction (`BaseAgent._enhance_system_prompt_with_context`) plus five specialized agent prompt templates (General, Billing, Complaint, Product, Tech). Basis: prose/instruction strings. **Language note**: the prompt bodies are authored in Chinese (the repository's native language); every excerpt quoted in this report is rendered as an English translation and is marked as such.
- Skill (absent): no markdown file with `name`/`description` front matter defines an invokable capability.
- Tool Schema (absent): each agent owns a scoped mock "domain database" (service hours, billing, complaints, products, tech) but no JSON Schema / function-calling definition with a `parameters` block is shown. The `response` / `current_agent` / `tools_used` fields are a shared state contract, not Tool Schemas.
- Base class (present): `BaseAgent` provides conversation-context injection, session management and prompt augmentation.
- Embedded code snippets (QC scope): the `super().__init__(...)` registrations, the base-class context instruction, and the shared state-write pattern.
- Out of coverage: the classifier/router node (`multi_agent_customer_service.py`) and the mock domain databases were identified by name but not fully quoted.

Scope note: all five specialized agents are dispatched by one router over one shared `BaseAgent`, so all artifacts belong to the same agent suite and no artifact from another case is mixed in.

---

## 3. Stage A - Single-artifact inspection

### 3.A.1 System Prompt set (five specialized prompts + shared base instruction)

Tier determination: **L3 Complex Agent**. Basis (any 2 or more of the L3 criteria): 4+ tool/data-resource invocations at suite level (five scoped domain databases); complex multi-agent routing (classifier -> one of five specialists -> handoff/escalation); security-sensitive (billing/refund/complaint data); requires exception handling (the base class declares a graceful error fallback and the prompts declare out-of-scope handoff). Upward-compatible L3 scope = 47 items.

- QD-P-1.1.1 | PASS | evidence: TC-095, the five prompts, no mutually exclusive attribute or directive found.
- QD-P-1.1.2 | PASS | evidence: TC-095, the prompts do not conflict in any declared scenario.
- QD-P-1.1.3 | PASS | evidence: TC-095, no worked example contradicts a rule.
- QD-P-1.2.1 | PASS | evidence: TC-095, each agent identity matches its responsibility (translation: "You are {name}, specializing in {role}." for each of the five roles).
- QD-P-1.2.2 | PASS | evidence: TC-095, the role voice matches the declared friendly/professional service style (translation).
- QD-P-1.2.3 | PASS | evidence: TC-095, no constraint prohibits an agent's core responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-095, no misused quantifier found.
- QD-P-1.3.2 | FAIL | evidence: TC-095, the handoff trigger is carried by a vague qualifier (translation) - "if the problem is complex or needs specialized knowledge, explain and suggest transferring to the appropriate specialized agent" - with no criterion for "complex".
- QD-P-1.3.3 | PASS | evidence: TC-095, the handoff boundary is declared (translation: "if out of scope, suggest handoff to a specialist"; "if beyond your authority, explain and suggest handoff").
- QD-P-1.4.1 | PASS | evidence: TC-095, no duplicate constraint found.
- QD-P-1.4.2 | PASS | evidence: TC-095, the declared branches (answer / clarify / handoff) are all reachable.
- QD-P-1.4.3 | PASS | evidence: TC-095, no Skill definition is given in the prompts (vacuous).
- QD-P-1.5.1 | PASS | evidence: TC-095, the agents' responsibilities support the objective (resolve the customer's query in-domain).
- QD-P-1.5.2 | PASS | evidence: TC-095, the workflow resources (domain databases, conversation context, base-class machinery) are declared.
- QD-P-1.6.1 | PASS | evidence: TC-095, no vague word carries a security/permission boundary.
- QD-P-1.6.2 | PASS | evidence: TC-095, decisions key on the customer query and domain scope, not on unreportable internal state.
- QD-P-1.6.3 | PASS | evidence: TC-095, no soft rules are declared in mutually unreconciled tension.
- QD-P-1.6.4 | PASS | evidence: TC-095, no constraint fixes an internal reasoning method.
- QD-P-1.6.5 | PASS | evidence: TC-095, no self-referential or recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-095, the assumed presence of conversation history is handled (translation: "In multi-turn conversations, refer to prior content"; the base prompt degrades to answering from the query alone).
- QD-P-1.6.7 | PASS | evidence: TC-095, the shared context instruction declares a revision mechanism (translation: "based on the customer's new question provide supplementary information").
- QD-P-2.1.1 | PASS | evidence: TC-095, formatting is readable.
- QD-P-2.1.2 | PASS | evidence: TC-095, references ({self.name}, {self.role}, expertise) are named and filled deterministically.
- QD-P-2.1.3 | PASS | evidence: TC-095, the section hierarchy (identity -> expertise -> numbered guidance -> tone -> escalation) is reasonable.
- QD-P-2.1.4 | PASS | evidence: TC-095, prose is concise.
- QD-P-2.2.1 | PASS | evidence: TC-095, the input source is declared (the customer query plus the injected conversation history).
- QD-P-2.2.2 | FAIL | evidence: TC-095, no input data format, encoding or size limit is declared for the customer query.
- QD-P-2.2.3 | FAIL | evidence: TC-095, no input field is marked required or optional.
- QD-P-2.2.4 | FAIL | evidence: TC-095, no behavior is declared when the customer query is empty or missing (the only fallback is an out-of-scope handoff).
- QD-P-2.3.1 | FAIL | evidence: TC-095, no output format is declared; the prompts only declare a tone (translation: "Answer in a friendly, professional manner").
- QD-P-2.3.2 | PASS | evidence: TC-095, no output schema is declared, so "incompleteness" is not assessable; the missing format is recorded under QD-P-2.3.1 (determination basis).
- QD-P-2.3.3 | PASS | evidence: TC-095, no structured output is declared, so no stability mechanism is applicable (determination basis).
- QD-P-2.3.4 | FAIL | evidence: TC-095, no sensitive-data filtering, privacy handling, or security output constraint is declared for agents that handle billing/complaint data.
- QD-P-2.4.1 | PASS | evidence: TC-095, the workflow is complete (classify -> dispatch -> answer -> record `current_agent`/`tools_used`).
- QD-P-2.4.2 | PASS | evidence: TC-095, the resources used (each agent's scoped domain database) are declared.
- QD-P-2.4.3 | PASS | evidence: TC-095, the agents invoke no tool at LLM level (the domain lookup happens in the framework), so no invocation specification is required (vacuous).
- QD-P-2.5.1 | PASS | evidence: TC-095, no loop or recursion is declared (vacuous).
- QD-P-2.5.2 | FAIL | evidence: TC-095, no prohibited operation, sensitive-data access boundary, or external-access boundary is declared.
- QD-P-2.5.3 | FAIL | evidence: TC-095, no permission scope or escalation boundary is declared.
- QD-P-2.5.4 | PASS | evidence: TC-095, no soft-constraint conflict requires an arbitration rule.
- QD-P-2.5.5 | PASS | evidence: TC-095, the agents invoke no external resource at LLM level, so no frequency limit is required (vacuous).
- QD-P-2.6.1 | FAIL | evidence: TC-095, no handling is declared in the prompt text for runtime exceptions (e.g. LLM failure or data-lookup failure).
- QD-P-2.6.2 | PASS | evidence: TC-095, the declared out-of-scope handoff/escalation provides a recovery path (translation: "explain and suggest transferring to the appropriate specialized agent").
- QD-P-2.6.3 | PASS | evidence: TC-095, no retry mechanism is declared (vacuous).
- QD-P-2.7.1 | FAIL | evidence: TC-095, no representative worked example is provided.
- QD-P-2.7.2 | FAIL | evidence: TC-095, no counter-examples are provided.
- QD-P-2.7.3 | FAIL | evidence: TC-095, no boundary-case examples are provided.

### 3.A.2 Skill

- QD-S-1.x .. QD-S-5.x | N/A | evidence: TC-095 carries no Skill artifact (determination basis: no markdown file with `name`/`description` front matter defines an invokable capability). No QD-S verdict is emitted.

### 3.A.3 Tool Schema

- QD-T-1.x .. QD-T-4.x | N/A | evidence: TC-095 carries no Tool Schema artifact (determination basis: the agents own mock domain databases but expose no JSON `parameters`/`inputSchema` schema; the `response`/`current_agent`/`tools_used` fields are a state contract). No QD-T verdict is emitted.

### 3.A.4 Embedded code snippets (QC)

QC-0 baseline: the Python snippets (`super().__init__(...)` registrations, the base-class context instruction, the state-write pattern) are fenced as `python`.

- QC-0.1 | PASS | evidence: TC-095, the snippets parse as valid Python syntax.
- QC-0.2 | PASS | evidence: TC-095, the code blocks declare `python`.
- QC-0.3 | PASS | evidence: TC-095, the base class is elided with `...` and the shown methods are complete within their excerpts.
- QC-0.4 | PASS | evidence: TC-095, the code fences open and close correctly.
- QC-0.5 | PASS | evidence: TC-095, the declared language (`python`) matches the content.
- QC-1.1 | PASS | evidence: TC-095, the only names undefined within the snippets are framework symbols (`ABC`, `LangChainSessionManager`) whose imports are outside the excerpt.
- QC-1.2 | Not Executed | evidence: TC-095, no declared dependency list is available (dependency-context rule); not recorded as FAIL.
- QC-1.3 | Not Executed | evidence: TC-095, no API version database is available (dependency-context rule); not recorded as FAIL.
- QC-1.4 | PASS | evidence: TC-095, no type-mismatched call found.
- QC-2.1 .. QC-2.3 | N/A | evidence: TC-095, no file-handle, network-connection or high-risk call pattern is present in the snippets (determination basis: no such pattern).
- QC-3.1 | N/A | evidence: TC-095, imports are outside the excerpt, so no unused-import determination is made.
- QC-3.2 | PASS | evidence: TC-095, framework symbols are referenced without visible imports because the excerpt omits the module header.
- QC-3.3 | PASS | evidence: TC-095, no literal credential or machine-specific value is present (the `self.llm = None  # injected at runtime` comment carries no secret).
- QC-4.1 | PASS | evidence: TC-095, the shared state-write pattern (`response`, `current_agent`, `tools_used`) matches the declared state contract across all five agents.
- QC-4.2 | PASS | evidence: TC-095, no version/API drift between the snippets and the body.

---

## 4. Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Stage status: **Not Executed**. Reason: only one Logic Artifact type (System Prompt) is present; the domain "databases" are not Tool Schemas, so no Prompt/Skill/Tool pair exists and QD-PS (Prompt -> Skill), QD-PT (Prompt -> Tool), QD-ST (Skill <-> Tool) and QD-CYC-1.1 have no counterpart artifact.

Informational observation (not a Stage B verdict line): QD-CYC-1.2 (Multi-Agent Circular Invocation) was reviewed at suite level - the router dispatches each message to one specialized agent, and the agents only "suggest" a handoff (they do not call each other); no closed loop was found.

---

## 5. Stage C - Gate-0 (admission)

- G0-1 (no unfixed P0 in Stage A): NOT satisfied - recorded as an informational finding; does not gate this flow.
- G0-2 (no unfixed P0 in Stage B): N/A - Stage B did not run; recorded as informational.
- G0-3 (responsibility boundary statements exist and are locatable): Passed - each prompt states its role (translation: "You are {name}, specializing in {role}." for each of the five agents, with an explicit scope and handoff clause).
- G0-4 (each Tool Schema's `name`, `description`, parameter descriptions complete): NOT passed - no Tool Schema artifact is present (the agents own mock domain databases with no parameter schema).

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

Audit object: TC-095 System Prompt set (base context instruction + five specialized prompts) + embedded snippets.
Three-phase scan (NL-A -> NL-B -> NR-O -> NR-S) run over the bundled artifacts.

Risk Item Summary:
- Total Risk Items: 0
- Explicit.P0 (Block release): 0 items
- Explicit.P1 (Fix / exemption): 0 items
- Explicit.P2 (Risk ledger): 0 items

Note: no explicitly declared risk expression (self-contained exfiltration, identity/permission claim, constraint removal, priority override, dangerous flag, hardcoded credential/PII, or abnormal callback) was found in the static artifact text. The permission-related phrasing in the billing prompt (translation: "if beyond your authority, explain and suggest handoff") is a scope statement, not an identity/permission claim. This is a static-document scan only; it is not a security conclusion. Risk Implicit (dynamic exploitability) was NOT run.

---

## 8. Stage F - Impact outlook (candidate mapping, advisory only)

Advisory context only; it does not change, soften, or escalate any Inspect conclusion. Strength is association confidence, NOT severity. Candidate language only. Risk Implicit and the runtime Quality subsets were NOT run; the lite embedded-code QC ran in Stage A. Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent.

| Defect (FAIL) | Candidate attack surface (AS-*) | Candidate failure modes (FM-*) | Strength (provisional, lite) |
|---|---|---|---|
| QD-P-1.3.2 | AS-01, AS-04 | FM-01, FM-02, FM-07, FM-09 | Conditional (handoff trigger may drift) |
| QD-P-2.2.2, QD-P-2.2.3, QD-P-2.2.4 | AS-02, AS-07 | FM-01, FM-04 | Medium (input format/necessity/missing handling undeclared) |
| QD-P-2.3.1 | AS-03, AS-09 | FM-06 | Conditional |
| QD-P-2.3.4 | AS-03 | FM-06 | Conditional |
| QD-P-2.5.2, QD-P-2.5.3 | AS-01, AS-03, AS-04, AS-05 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.6.1 | AS-07 | FM-08, FM-10 | Conditional |
| QD-P-2.7.1, QD-P-2.7.2, QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |

Candidate RAG-Agent quality metrics (candidate associations only; NOT a quality result): Correctness, Completeness, Consistency, Boundary Recognition, Safety Response. Defect chains (SC-*/QC-TA-*/QC-RA-*) are out of scope for lite v1.

---

## 9. Status board

Stage A (Single-artifact):  Executed - QD-P (L3, 5 specialized prompts + shared base instruction), QD-T (N/A, no Tool Schema), QD-S (N/A, no Skill), QC (embedded Python snippets).
Stage B (Cross):            Not Executed - only one artifact type present (System Prompt); no Prompt/Skill/Tool pair exists.
Stage C (Gate-0):           Not passed - G0-4 (G0-1/G0-2 informational).
Stage D (Permission QD-PM): Not Executed - Gate-0 G0-4 not satisfied; full artifact set incomplete (no Skill, no Tool Schema).
Stage E (Risk Explicit EX): Executed - 0 findings.
Stage F (Impact outlook):   Executed - candidate mapping for all Stage A FAILs.
Stage G (Self-verification): Executed - ID back-closure, red-line wording, output contract checked.

---

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. No in-place self-corrections were required.
