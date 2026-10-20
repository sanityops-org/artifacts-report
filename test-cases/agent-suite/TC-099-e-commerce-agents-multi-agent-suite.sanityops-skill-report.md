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
- Finding counts (Stage A, System Prompt set): Inspect P0 = 7, P1 = 0, P2 = 0.
- Gate-0 result: Not passed (G0-3 passed; G0-4 not satisfied - no Tool Schema artifact is present; tools such as `call_specialist_agent` and `search_products` are referenced by name only, with no JSON `parameters` schema).
- Risk-Explicit summary (Stage E): Explicit·P0 = 0, Explicit·P1 = 0, Explicit·P2 = 0.
- Top findings (rule ID - one-line defect):
  1. QD-P-2.5.2 / QD-P-2.5.3 - the prompts declare no security boundary and no permission-control boundary, and the admin role is described only as an identity ("full access to all data and agents").
  2. QD-P-2.3.4 - no sensitive-data filtering or privacy output constraint is declared.
  3. QD-P-2.2.2 / QD-P-2.2.3 - the free-text user-message input has no declared format and no required/optional marking.
  4. QD-P-2.7.2 / QD-P-2.7.3 - no counter-examples or boundary-case examples are provided.
  5. QD-P-2.5.4 / QD-P-2.5.5 - no resource-invocation frequency limit or constraint-priority arbitration is declared (advisory).
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The lite embedded-code QC was run in Stage A.
- This report never states a security or quality conclusion; Inspect PASS is not Risk PASS and not Quality PASS.
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and version-level evidence chains, use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

---

## 2. Artifact inventory (input preparation, not a stage)

Case TC-099 bundles one coordinated multi-agent e-commerce/customer-service suite (6 YAML prompt configs: one orchestrator + five specialists, over the A2A protocol). Artifact types present, by structural signature:

- System Prompt (present, quoted, 2): the orchestrator prompt (`config/prompts/orchestrator.yaml`) and the product-discovery prompt (`config/prompts/product-discovery.yaml`). Basis: prose instruction strings in the `system_prompt.base` YAML field.
- System Prompt (identified, not quoted, 4): the order-management, pricing-promotions, review-sentiment, and inventory-fulfillment prompt configs exist per the directory listing but their bodies were not retrieved; they are therefore not inspected.
- Skill (absent): no markdown file with `name`/`description` front matter defines an invokable capability.
- Tool Schema (absent): specialist tools are referenced by name only (e.g. `call_specialist_agent`, `search_products`, `semantic_search`, `get_my_products`, `recall_memories`); no JSON `parameters`/`inputSchema` schema is shown.
- Embedded code / config snippets (QC scope): the YAML prompt configs and the `shared/prompt_loader.py` composition description.
- Out of coverage: `agents/python/<agent>/tools.py`, the `shared/` grounding/guardrails/HITL utilities, and the `.NET/C#` backend are described but not quoted.

Scope note: all six prompts are roles of the same orchestrated e-commerce suite (one orchestrator routing over A2A to five specialists, with shared grounding/guardrail/HITL fragments). All artifacts belong to the same agent suite, so no artifact from another case is mixed in.

---

## 3. Stage A - Single-artifact inspection

### 3.A.1 System Prompt set (orchestrator + product-discovery)

Tier determination: **L3 Complex Agent**. Basis (any 2 or more of the L3 criteria): the suite is a 6-role multi-agent orchestration (one orchestrator + five specialists over A2A) with multi-intent sequential fan-out (>5 steps in a multi-intent request); it is security-sensitive (JWT auth + RBAC, customer orders, returns/refunds, payments); it requires exception handling (specialist error handling and clarifying-question paths). Upward-compatible L3 scope = 47 items.

- QD-P-1.1.1 | PASS | evidence: TC-099, sections 1.1-1.2, no mutually exclusive attribute or directive found.
- QD-P-1.1.2 | PASS | evidence: TC-099, sections 1.1-1.2, the routing rules and the structured-card pass-through rules do not conflict in any declared scenario.
- QD-P-1.1.3 | PASS | evidence: TC-099, section 1.1, the intent examples ("Show me laptops under $1000", "Where is my order?") match their routing rules.
- QD-P-1.2.1 | PASS | evidence: TC-099, sections 1.1-1.2, each role identity (orchestrator; product-discovery specialist) matches its stated responsibilities.
- QD-P-1.2.2 | PASS | evidence: TC-099, sections 1.1-1.2, the role voice matches the declared conversational reply style.
- QD-P-1.2.3 | PASS | evidence: TC-099, sections 1.1-1.2, the constraints (never expose internal agent names; do not ask for the email) do not prohibit the core routing/answering responsibilities.
- QD-P-1.3.1 | PASS | evidence: TC-099, section 1.1, no misused quantifier found (intents are enumerated 1-9).
- QD-P-1.3.2 | PASS | evidence: TC-099, section 1.1, the vague terms ("clear, specific context", "friendly, helpful, professional") are secondary style descriptors.
- QD-P-1.3.3 | PASS | evidence: TC-099, section 1.1, the routing/handoff conditions and the prohibition scope ("Never expose internal agent names or routing details to the customer") are declared.
- QD-P-1.4.1 | PASS | evidence: TC-099, sections 1.1-1.2, no duplicate constraint found.
- QD-P-1.4.2 | PASS | evidence: TC-099, section 1.1, all nine intent branches are reachable.
- QD-P-1.4.3 | PASS | evidence: TC-099, sections 1.1-1.2, no Skill definition is given in the prompts (vacuous).
- QD-P-1.5.1 | PASS | evidence: TC-099, sections 1.1-1.2, the routing/synthesis responsibilities support the objective (resolve the customer need through the right specialist).
- QD-P-1.5.2 | PASS | evidence: TC-099, section 1.1, the resources used (`call_specialist_agent` and the five specialists) are declared.
- QD-P-1.6.1 | PASS | evidence: TC-099, section 1.1, the routing decision is enumerated by intent; "if action is needed" is a minor qualifier, not a security/permission boundary.
- QD-P-1.6.2 | PASS | evidence: TC-099, section 1.1, control flow keys on the user message and the declared intents, not on unobservable model internal state.
- QD-P-1.6.3 | PASS | evidence: TC-099, section 1.1, the soft rules (friendly/professional vs never expose internals) are not declared in mutual tension.
- QD-P-1.6.4 | PASS | evidence: TC-099, sections 1.1-1.2, no constraint fixes an internal reasoning method.
- QD-P-1.6.5 | PASS | evidence: TC-099, sections 1.1-1.2, no self-referential or recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-099, section 1.1, the availability of the User Context is stated ("their name, email, role, loyalty tier, and recent orders are in the User Context below").
- QD-P-1.6.7 | PASS | evidence: TC-099, sections 1.1-1.2, the orchestrator synthesises per-message and the memory tools (recall/store) provide the declared update path (determination basis: an update mechanism exists).
- QD-P-2.1.1 | PASS | evidence: TC-099, sections 1.1-1.2, formatting is readable.
- QD-P-2.1.2 | PASS | evidence: TC-099, section 1.1, the referenced card blocks (```product, ```order, ```checkout) and tools are named and locatable.
- QD-P-2.1.3 | PASS | evidence: TC-099, sections 1.1-1.2, the identity / specialist-list / intent-classification / guidelines / card-blocks hierarchy is reasonable.
- QD-P-2.1.4 | PASS | evidence: TC-099, sections 1.1-1.2, prose is concise (excerpted with ellipses).
- QD-P-2.2.1 | PASS | evidence: TC-099, section 1.1, the input sources are declared (the User Context and the user's free-text message).
- QD-P-2.2.2 | FAIL | evidence: TC-099, section 1.1, the free-text user-message input format is unconstrained (no declared format, encoding, or size limit).
- QD-P-2.2.3 | FAIL | evidence: TC-099, section 1.1, no input field is marked required or optional.
- QD-P-2.2.4 | PASS | evidence: TC-099, section 1.1, ambiguous input is handled - "If you're unsure which agent to route to, ask a clarifying question."
- QD-P-2.3.1 | PASS | evidence: TC-099, section 1.1, output format is declared (a conversational reply plus verbatim `product`/`products`/`order`/`checkout`/`return`/`sentiment`/`inventory`/`pricing` card blocks).
- QD-P-2.3.2 | PASS | evidence: TC-099, section 1.1, the structured-card payload types are enumerated ("with items, totals, address"; "rating distribution, trend, pros/cons").
- QD-P-2.3.3 | PASS | evidence: TC-099, section 1.1, format stability is bounded for the card blocks ("you MUST include them in your reply verbatim, byte-for-byte ... never invent your own").
- QD-P-2.3.4 | FAIL | evidence: TC-099, sections 1.1-1.2, no sensitive-data filtering, privacy handling, or security output constraint is declared.
- QD-P-2.4.1 | PASS | evidence: TC-099, section 1.1, the workflow steps are complete (classify intent -> route -> synthesise -> emit cards).
- QD-P-2.4.2 | PASS | evidence: TC-099, section 1.1, the resources/tools used (`call_specialist_agent` and the five specialists) are declared.
- QD-P-2.4.3 | PASS | evidence: TC-099, section 1.1, an invocation specification is given (call the relevant specialists sequentially with clear context).
- QD-P-2.5.1 | PASS | evidence: TC-099, sections 1.1-1.2, no loop or recursion is declared (vacuous).
- QD-P-2.5.2 | FAIL | evidence: TC-099, sections 1.1-1.2, no prohibited operation, sensitive-data access boundary, or external-access boundary is declared.
- QD-P-2.5.3 | FAIL | evidence: TC-099, section 1.1, no permission scope or privilege-escalation boundary is declared (the admin path is stated only as an identity: "This user is an admin with full access to all data and agents.").
- QD-P-2.5.4 | PASS | evidence: TC-099, sections 1.1-1.2, no unarbitrated soft-constraint conflict found.
- QD-P-2.5.5 | PASS | evidence: TC-099, section 1.1, no resource-invocation frequency limit is needed beyond the sequential specialist fan-out (determination basis: no unbounded invocation declared).
- QD-P-2.6.1 | PASS | evidence: TC-099, section 1.1, the tool-error path is handled - "If a specialist returns an error, apologize and offer alternatives".
- QD-P-2.6.2 | PASS | evidence: TC-099, section 1.1, degradation is defined (on specialist error, apologise and offer alternatives).
- QD-P-2.6.3 | PASS | evidence: TC-099, sections 1.1-1.2, no retry mechanism is declared (vacuous).
- QD-P-2.7.1 | PASS | evidence: TC-099, section 1.1, representative positive examples are provided for the intent classification ("Show me laptops under $1000", "Compare these two phones").
- QD-P-2.7.2 | FAIL | evidence: TC-099, sections 1.1-1.2, no counter-examples are provided.
- QD-P-2.7.3 | FAIL | evidence: TC-099, sections 1.1-1.2, no boundary-case examples are provided.

### 3.A.2 Skill

- QD-S-1.x .. QD-S-5.x | N/A | evidence: TC-099 carries no Skill artifact (determination basis: the configs are YAML prompt files; no markdown file with `name`/`description` front matter defines an invokable capability). No QD-S verdict is emitted.

### 3.A.3 Tool Schema

- QD-T-1.x .. QD-T-4.x | N/A | evidence: TC-099 carries no Tool Schema artifact (determination basis: tools are referenced by name only, with no JSON `parameters`/`inputSchema` schema). No QD-T verdict is emitted.

### 3.A.4 Embedded code / config snippets (QC)

QC-0 baseline: the quoted snippets are YAML prompt configs, fenced as `yaml`, and parse as valid YAML.

- QC-0.1 | PASS | evidence: TC-099, sections 1.1-1.2, the YAML configs parse as valid syntax.
- QC-0.2 | PASS | evidence: TC-099, the snippets are fenced as `yaml`.
- QC-0.3 | PASS | evidence: TC-099, the configs are complete for their purpose (base prompt + role instructions + schema/tool refs).
- QC-0.4 | PASS | evidence: TC-099, all code fences open and close correctly.
- QC-0.5 | PASS | evidence: TC-099, the declared language (`yaml`) matches the content.
- QC-1.1 | N/A | evidence: TC-099, the snippets are configuration text; no executable name references (determination basis: data/config-only snippets).
- QC-1.2 | Not Executed | evidence: TC-099, no declared dependency list is available (dependency-context rule); not recorded as FAIL.
- QC-1.3 | Not Executed | evidence: TC-099, no API version database is available (dependency-context rule); not recorded as FAIL.
- QC-1.4 | N/A | evidence: TC-099, no function call with typed arguments is present (determination basis: config-only snippets).
- QC-2.1 | N/A | evidence: TC-099, no file-handle pattern present (determination basis: no such pattern).
- QC-2.2 | N/A | evidence: TC-099, no network-connection constructor present (determination basis: no such pattern).
- QC-2.3 | N/A | evidence: TC-099, no high-risk file/network/DB call present (determination basis: no such pattern).
- QC-3.1 | N/A | evidence: TC-099, no imports present (determination basis: config-only snippets).
- QC-3.2 | N/A | evidence: TC-099, no referenced symbols requiring imports (determination basis: config-only snippets).
- QC-3.3 | PASS | evidence: TC-099, the only literals are functional examples ("Show me laptops under $1000", "SAVE10"); no credential, local path, or machine-specific value.
- QC-4.1 | PASS | evidence: TC-099, the card-block names referenced in the orchestrator prompt match the specialist card contract.
- QC-4.2 | PASS | evidence: TC-099, no version/API drift between the snippets and the body.

---

## 4. Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Stage status: **Not Executed**. Reason: only one Logic Artifact type (System Prompt) is present; no Prompt/Skill/Tool pair exists, so QD-PS (Prompt -> Skill), QD-PT (Prompt -> Tool), QD-ST (Skill <-> Tool), and QD-CYC-1.1 have no counterpart artifact and are Not Applicable.

Informational observation (not a Stage B verdict line): QD-CYC-1.2 (Multi-Agent Circular Invocation) was reviewed at suite level - the orchestrator routes one-way to five specialists via `call_specialist_agent`; no specialist calls the orchestrator back, and no cyclic role orchestration is declared. No closed loop was found.

---

## 5. Stage C - Gate-0 (admission)

- G0-1 (no unfixed P0 in Stage A): NOT satisfied - recorded as an informational finding; does not gate this flow.
- G0-2 (no unfixed P0 in Stage B): N/A - Stage B did not run; recorded as informational.
- G0-3 (responsibility boundary statements exist and are locatable): Passed - the prompts state their roles and scope (e.g. section 1.1 "You are the Customer Support orchestrator for this e-commerce platform."; section 1.2 "You are a Product Discovery specialist for this e-commerce platform.").
- G0-4 (each Tool Schema's `name`, `description`, parameter descriptions complete): NOT passed - no Tool Schema artifact is present (tools are referenced by name only, with no parameter schema).

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

Audit object: TC-099 System Prompt set (orchestrator + product-discovery) + embedded YAML snippets.
Three-phase scan (NL-A -> NL-B -> NR-O -> NR-S) run over the bundled artifacts.

Risk Item Summary:
- Total Risk Items: 0
- Explicit·P0 (Block release): 0 items
- Explicit·P1 (Fix / exemption): 0 items
- Explicit·P2 (Risk ledger): 0 items

Note: no explicitly declared risk expression (self-contained exfiltration, identity/permission claim, constraint removal, priority override, dangerous flag, hardcoded credential/PII, or abnormal callback) was found in the static artifact text. The role statements (customer/seller/admin) and the "Never expose internal agent names" rule were reviewed: the admin line is a role description ("full access to all data and agents") rather than an injected permission-escalation instruction, so it is recorded as a design concern of the Inspect layer (QD-P-2.5.3), not an EX risk expression. This is a static-document scan only; it is not a security conclusion. Risk Implicit (dynamic exploitability) was NOT run.

---

## 8. Stage F - Impact outlook (candidate mapping, advisory only)

Advisory context only; it does not change, soften, or escalate any Inspect conclusion. Strength is association confidence, NOT severity. Candidate language only. Risk Implicit and the runtime Quality subsets were NOT run; the lite embedded-code QC ran in Stage A. Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent.

| Defect (FAIL) | Candidate attack surface (AS-*) | Candidate failure modes (FM-*) | Strength (provisional, lite) |
|---|---|---|---|
| QD-P-2.2.2, QD-P-2.2.3 | AS-02, AS-07 | FM-01, FM-04 | Medium (input format/necessity undeclared) |
| QD-P-2.3.4 | AS-03 | FM-06 | Conditional |
| QD-P-2.5.2, QD-P-2.5.3 | AS-01, AS-03, AS-04, AS-05 | FM-08, FM-09, FM-10 | Medium (broad admin identity, no permission boundary) |
| QD-P-2.7.2, QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |

Candidate RAG-Agent quality metrics (candidate associations only; NOT a quality result): Correctness, Relevance, Consistency, Format Compliance, Boundary Recognition, Safety Response. Defect chains (SC-*/QC-*) are out of scope for lite v1.

---

## 9. Status board

Stage A (Single-artifact):  Executed - QD-P (L3, orchestrator + product-discovery), QD-S (N/A, no Skill), QD-T (N/A, no Tool Schema), QC (embedded YAML configs).
Stage B (Cross):            Not Executed - only one artifact type present (System Prompt); no Prompt/Skill/Tool pair exists.
Stage C (Gate-0):           Not passed - G0-4 (G0-1/G0-2 informational).
Stage D (Permission QD-PM): Not Executed - Gate-0 G0-4 not satisfied; full artifact set incomplete (no Skill, no Tool Schema).
Stage E (Risk Explicit EX): Executed - 0 findings.
Stage F (Impact outlook):   Executed - candidate mapping for all Stage A FAILs.
Stage G (Self-verification): Executed - ID back-closure, red-line wording, output contract checked.

---

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. No in-place self-corrections were required.
