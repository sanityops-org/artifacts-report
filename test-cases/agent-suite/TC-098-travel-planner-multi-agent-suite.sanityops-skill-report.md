# SanityOps Inspect Lite Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-15
Artifact version: not supplied by the user (using the case's Collection Date 2026-10-13 as the working label)

---

## 1. Executive summary (Sec. 6.1)

- Stages executed: A (single-artifact), C (Gate-0), E (Risk Explicit), F (impact outlook), G (self-verification). Stage B did not run (no same-agent artifact pair). Stage D did not run (Gate-0 G0-4 not satisfied / incomplete artifact set).
- Finding counts (Stage A): Inspect P0 = 8, P1 = 11, P2 = 0 (Skill `flights`: P0 = 3, P1 = 6; System Prompt `itinerary`: P0 = 5, P1 = 5). The embedded-snippet QC adds one P1 finding (QC-3.2).
- Gate-0 result: Not passed (G0-3 passed; G0-4 not satisfied - no Tool Schema artifact is present; tools are declared as bare names such as `WebSearch, WebFetch`, with no JSON `parameters` schema).
- Risk-Explicit summary (Stage E): Explicit·P0 = 0, Explicit·P1 = 0, Explicit·P2 = 0.
- Top findings (rule ID - one-line defect):
  1. QD-S-3.4 - the `flights` Skill declares no `non_goals` (task scope undefined).
  2. QD-S-1.1 / QD-S-4.1 - no input boundary and no failure behavior are declared for the `flights` Skill.
  3. QD-P-2.2.2 / QD-P-2.2.3 / QD-P-2.2.4 - the itinerary prompt declares no input format, required/optional marking, or missing-input handling.
  4. QD-P-2.5.2 / QD-S-1.4 / QD-S-5.1 - no security boundary and no read/write/delete permission distinction are declared.
  5. QD-P-2.3.4 - no sensitive-data filtering or privacy output constraint is declared.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The lite embedded-code QC was run in Stage A.
- This report never states a security or quality conclusion; Inspect PASS is not Risk PASS and not Quality PASS.
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and version-level evidence chains, use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

---

## 2. Artifact inventory (input preparation, not a stage)

Case TC-098 bundles one coordinated multi-agent trip-planning suite (21 specialist agent definitions run in a 3-phase pipeline: 12 parallel search agents, deferred pricing/packing agents, itinerary + adversarial stress-test synthesis). Artifact types present, by structural signature:

- Skill (present, quoted, 1): the `flights` agent definition `.agents/flights.md`. Basis: markdown with `name`/`description` front matter (plus `tools`/`max_turns`), the structural signature of a Skill definition.
- Skill (identified, not quoted, 20): the remaining `.agents/*.md` agent definitions (hotels, activities, places, visa, sim, tips, forex, getting-around, weather, emergency-card, events, pricing-advisor, packing-list, itinerary, stress-test, chat, layover, discovery, orchestrator, and others) exist per the `.agents` directory listing but their bodies were not retrieved; they are therefore not inspected.
- System Prompt (present, quoted, 1): the runtime-assembled itinerary prompt inside `backend/app/agents/itinerary_agent.py` (a `f"...".format` string), with its `pace_guidance` mapping and `multi_city_block` fragment. Basis: a prose/instruction string not carrying front matter.
- Tool Schema (absent): tools are declared as bare names in front matter (`tools: WebSearch, WebFetch`); no JSON `parameters`/`inputSchema` schema is shown.
- Embedded code snippets (QC scope): the `AgentDefinition` dataclass (`loader.py`) and the itinerary prompt-building Python.
- Out of coverage: `web_tools.py`, the SerpAPI flights service and `_url_to_source` mapping, and the `*_agent.py` subclasses are described but not quoted.

Classification note and determination basis: the `.agents/*.md` files carry `name`/`description` front matter and are classified as **Skill** artifacts by the structural-signature rule; the inline itinerary prompt is classified as a **System Prompt**. Both belong to the same suite (one 3-phase pipeline), so no artifact from another case is mixed in.

---

## 3. Stage A - Single-artifact inspection

### 3.A.1 Skill (`flights` agent definition)

Risk-level determination: **L2 Medium Risk** (resource access). Basis: the Skill declares tool invocations (`tools: WebSearch, WebFetch`) and performs read-only web research; it does not perform irreversible operations or handle sensitive data. Applying the L2 minimum rule set (6 mandatory P0 items + 14 recommended P1 items).

QD-S-0 baseline compliance (entry gate):
- QD-S-0.1 | PASS | evidence: TC-098, `.agents/flights.md` front matter, `name` and `description` (plus `tools`/`max_turns`) are present.
- QD-S-0.2 | PASS | evidence: TC-098, `.agents/flights.md`, each field carries non-empty content.
- QD-S-0.3 | PASS | evidence: TC-098, `.agents/flights.md`, the YAML front matter parses as valid syntax between `---` markers.
- QD-S-0.4 | PASS | evidence: TC-098, `.agents/flights.md`, `max_turns: 4` is an integer and `tools: WebSearch, WebFetch` is a well-formed comma-separated tool declaration.
- QD-S-0.5 | PASS | evidence: TC-098, `.agents/flights.md`, no conflicting declarations found.
- QD-S-0.6 | PASS | evidence: TC-098, `.agents/flights.md`, the definition meets the minimum structural completeness of a Skill definition (identity + description + tools + body).
Baseline result: all six items PASS - proceed to QD-S-1..5.

- QD-S-1.1 | FAIL | evidence: TC-098, `.agents/flights.md` body, no upper limit is declared on the number or size of inputs (route, dates, and any additional traveller input are unbounded).
- QD-S-1.2 | PASS | evidence: TC-098, `.agents/flights.md` body, the output is bounded to "8-12 options from different airlines and sources".
- QD-S-1.3 | PASS | evidence: TC-098, `.agents/flights.md`, the invocation count is bounded ("Perform 5 targeted searches") and `max_turns: 4` bounds execution.
- QD-S-3.4 | FAIL | evidence: TC-098, `.agents/flights.md` body, no `non_goals` declaration - the Skill does not state what it does NOT do (no explicit exclusion of booking, payment, or itinerary planning).
- QD-S-4.1 | FAIL | evidence: TC-098, `.agents/flights.md` body, no failure behavior is declared (no instruction for when the searches fail or return nothing).
- QD-S-1.4 | FAIL | evidence: TC-098, `.agents/flights.md` body, no read/write/delete permission distinction and no prohibited-operation declaration are present.
- QD-S-1.5 | PASS | evidence: TC-098, `.agents/flights.md` body, the permitted data sources are named (site-scoped searches against skyscanner.com and google.com/travel/flights).
- QD-S-2.1 | PASS | evidence: TC-098, `.agents/flights.md` body, no unbounded word ("all"/"every"/"entire"/"complete") is present.
- QD-S-2.2 | PASS | evidence: TC-098, `.agents/flights.md` body, no "keep trying"/"until success" wording is present.
- QD-S-2.3 | PASS | evidence: TC-098, `.agents/flights.md` body, the output structure is closed (a fixed JSON object with a `results` array).
- QD-S-2.4 | PASS | evidence: TC-098, `.agents/flights.md` body, the capability verb is narrow ("search for round-trip flights").
- QD-S-3.1 | FAIL | evidence: TC-098, `.agents/flights.md`, no explicit trigger/activation declaration (`allowed_when`) is present; activation is implied only by the `description`.
- QD-S-3.2 | FAIL | evidence: TC-098, `.agents/flights.md`, no deactivation condition (`forbidden_when`) is declared.
- QD-S-3.3 | PASS | evidence: TC-098, `.agents/flights.md` body, ambiguous input is handled - "If no return date is given, search one-way only."
- QD-S-3.6 | PASS | evidence: TC-098, `.agents/flights.md`, the `name` ("flights") and `description` (round-trip flight search) match the body.
- QD-S-4.2 | FAIL | evidence: TC-098, `.agents/flights.md` body, whether partial completion is acceptable is not declared.
- QD-S-4.3 | FAIL | evidence: TC-098, `.agents/flights.md` body, no post-failure prohibited behaviors are declared.
- QD-S-5.1 | FAIL | evidence: TC-098, `.agents/flights.md` body, the Skill operates on data but does not distinguish read, modify, and delete permission scopes.
- QD-S-5.3 | PASS | evidence: TC-098, `.agents/flights.md` body, no environment-sensitive operation is declared (read-only web search).
- QD-S-5.4 | PASS | evidence: TC-098, `.agents/flights.md` body, the Skill does not invoke other Skills (vacuous).

### 3.A.2 System Prompt (runtime itinerary prompt)

Tier determination: **L2 Multi-turn Interactive**. Basis (any 2 or more of the L2 criteria): the prompt is a single synthesis step within a multi-agent pipeline, consumes several structured inputs (request + downstream agent results), and produces a bounded structured itinerary; it declares no tool invocations of its own. Applying the L2 minimum rule set (18 P0 items; the L3-only items QD-P-2.6.x are out of scope at this tier).

- QD-P-1.1.1 | PASS | evidence: TC-098, section 1.2, no mutually exclusive directive found.
- QD-P-1.1.2 | PASS | evidence: TC-098, section 1.2, no conflicting constraints in any declared scenario.
- QD-P-1.1.3 | PASS | evidence: TC-098, section 1.2, no worked example contradicts a rule.
- QD-P-1.2.1 | PASS | evidence: TC-098, section 1.2, the itinerary-planner role matches the day-by-day synthesis responsibility.
- QD-P-1.2.2 | PASS | evidence: TC-098, section 1.2, the role voice matches the declared structured output.
- QD-P-1.2.3 | PASS | evidence: TC-098, section 1.2, the constraints (exact slot count, cost fields) do not prohibit the core synthesis responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-098, section 1.2, quantities are bounded ("exactly 3 time slots", "{nights + 1}-day itinerary").
- QD-P-1.3.2 | PASS | evidence: TC-098, section 1.2, the vague terms ("geographically close") steer grouping, not a security/permission boundary.
- QD-P-1.3.3 | PASS | evidence: TC-098, section 1.2, the pacing and multi-city constraints define the behavioral scope (determination basis: no authorization/handoff morphology).
- QD-P-1.4.1 | PASS | evidence: TC-098, section 1.2, no duplicate constraint found.
- QD-P-1.4.2 | PASS | evidence: TC-098, section 1.2, the pacing branches (relaxed/balanced/packed) are all reachable.
- QD-P-1.4.3 | PASS | evidence: TC-098, section 1.2, the prompt defines no Skill (vacuous).
- QD-P-1.5.1 | PASS | evidence: TC-098, section 1.2, the responsibilities (assign activities to day/slot, estimate costs) support the objective.
- QD-P-1.5.2 | PASS | evidence: TC-098, section 1.2, the required inputs (activities, hotel) are declared as provided.
- QD-P-1.6.1 | PASS | evidence: TC-098, section 1.2, the vague words steer grouping/formatting, not a security/permission decision.
- QD-P-1.6.2 | PASS | evidence: TC-098, section 1.2, control flow keys on provided inputs, not on unobservable model internal state.
- QD-P-1.6.3 | PASS | evidence: TC-098, section 1.2, the pacing soft rules are arbitrated by the `pace_guidance` mapping.
- QD-P-1.6.4 | PASS | evidence: TC-098, section 1.2, no constraint fixes an internal reasoning method.
- QD-P-1.6.5 | PASS | evidence: TC-098, section 1.2, no self-referential or recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-098, section 1.2, the assumed availability of downstream results is handled by the pipeline's fallback (Phase 0 static data / template fallback).
- QD-P-1.6.7 | PASS | evidence: TC-098, section 1.2, the prompt is invoked once per request to synthesise a plan (determination basis: single-shot synthesis, no conversation).
- QD-P-2.1.1 | PASS | evidence: TC-098, section 1.2, formatting is readable.
- QD-P-2.1.2 | PASS | evidence: TC-098, section 1.2, the referenced inputs (`hotel_name`, `activities_summary`, `multi_city_block`) are named and locatable.
- QD-P-2.1.3 | PASS | evidence: TC-098, section 1.2, the input list / schedule rules / cost rules hierarchy is reasonable.
- QD-P-2.1.4 | PASS | evidence: TC-098, section 1.2, prose is concise.
- QD-P-2.2.1 | PASS | evidence: TC-098, section 1.2, the input sources are declared (destination, origin, dates, travelers, interests, pace, hotel, available activities).
- QD-P-2.2.2 | FAIL | evidence: TC-098, section 1.2, the input format is unconstrained - `activities_summary` and `traveler_context` carry no declared format, encoding, or size limit.
- QD-P-2.2.3 | FAIL | evidence: TC-098, section 1.2, no input field is marked required or optional.
- QD-P-2.2.4 | FAIL | evidence: TC-098, section 1.2, handling of missing input is undefined (no behavior is declared when the available-activities list or hotel is absent).
- QD-P-2.3.1 | PASS | evidence: TC-098, section 1.2, output format is declared ({nights + 1} days, exactly 3 slots/day, `daily_estimated_cost_usd`/`total_estimated_cost_usd`).
- QD-P-2.3.2 | PASS | evidence: TC-098, section 1.2, the output fields are declared (day, slots, cost fields, lat/lng for multi-city).
- QD-P-2.3.3 | FAIL | evidence: TC-098, section 1.2, no output-stability assurance mechanism is declared.
- QD-P-2.3.4 | FAIL | evidence: TC-098, section 1.2, no sensitive-data filtering, privacy handling, or security output constraint is declared.
- QD-P-2.4.1 | PASS | evidence: TC-098, section 1.2, the workflow steps are complete (read inputs -> assign activities to slots -> estimate costs -> emit itinerary).
- QD-P-2.4.2 | PASS | evidence: TC-098, section 1.2, the resources used (hotel, activities) are declared as inputs (vacuous - no tool invocation).
- QD-P-2.4.3 | PASS | evidence: TC-098, section 1.2, no tool invocation is declared (vacuous).
- QD-P-2.5.1 | PASS | evidence: TC-098, section 1.2, no loop or recursion is declared (vacuous).
- QD-P-2.5.2 | FAIL | evidence: TC-098, section 1.2, no prohibited operation, sensitive-data access boundary, or external-access boundary is declared.
- QD-P-2.5.3 | FAIL | evidence: TC-098, section 1.2, no permission scope or privilege-escalation boundary is declared.
- QD-P-2.5.4 | PASS | evidence: TC-098, section 1.2, no unarbitrated soft-constraint conflict found.
- QD-P-2.5.5 | PASS | evidence: TC-098, section 1.2, no resource invocation is declared (vacuous).
- QD-P-2.7.1 | FAIL | evidence: TC-098, section 1.2, no positive worked itinerary example is provided.
- QD-P-2.7.2 | FAIL | evidence: TC-098, section 1.2, no counter-examples are provided.
- QD-P-2.7.3 | FAIL | evidence: TC-098, section 1.2, no boundary-case examples are provided.

### 3.A.3 Tool Schema

- QD-T-1.x .. QD-T-4.x | N/A | evidence: TC-098 carries no Tool Schema artifact (determination basis: tools are declared as bare names in front matter, e.g. `tools: WebSearch, WebFetch`, and no JSON `parameters`/`inputSchema` schema is present). No QD-T verdict is emitted.

### 3.A.4 Embedded code snippets (QC)

QC-0 baseline: the `loader.py` dataclass and the itinerary prompt-building Python parse as valid Python and are fenced as `python`.

- QC-0.1 | PASS | evidence: TC-098, sections 1 and 1.2, the snippets parse as valid Python syntax.
- QC-0.2 | PASS | evidence: TC-098, the snippets are fenced as `python`.
- QC-0.3 | PASS | evidence: TC-098, each snippet is complete for its purpose (the dataclass and the prompt-building block are not truncated).
- QC-0.4 | PASS | evidence: TC-098, all code fences open and close correctly.
- QC-0.5 | PASS | evidence: TC-098, the declared language (`python`) matches the content.
- QC-1.1 | PASS | evidence: TC-098, the only names undefined within the snippets are `dataclass`/`field`; recorded once under QC-3.2.
- QC-1.2 | Not Executed | evidence: TC-098, no declared dependency list is available (dependency-context rule); not recorded as FAIL.
- QC-1.3 | Not Executed | evidence: TC-098, no API version database is available (dependency-context rule); not recorded as FAIL.
- QC-1.4 | PASS | evidence: TC-098, `list[str]` and `max_turns: int` annotations are used consistently; no type-mismatched call.
- QC-2.1 | N/A | evidence: TC-098, no file-handle pattern present (determination basis: no such pattern).
- QC-2.2 | N/A | evidence: TC-098, no network-connection constructor present (determination basis: no such pattern).
- QC-2.3 | N/A | evidence: TC-098, no high-risk file/network/DB call present (determination basis: no such pattern).
- QC-3.1 | N/A | evidence: TC-098, no import is present to check for unused modules (determination basis: no import block shown).
- QC-3.2 | FAIL | evidence: TC-098, section 1, `@dataclass` and `field(default_factory=list)` are used in `AgentDefinition` but neither `dataclass` nor `field` is imported in the snippet.
- QC-3.3 | PASS | evidence: TC-098, the literals (`1200.0`, `~$50/person/day`, `"round_trip"`) are functional examples, not demo credentials or machine-specific values.
- QC-4.1 | PASS | evidence: TC-098, the itinerary prompt uses the input field names it declares (`hotel_name`, `routes`, `interests`).
- QC-4.2 | PASS | evidence: TC-098, no version/API drift between the snippets and the body.

---

## 4. Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Stage status: **Not Executed**. Reason: two artifact types are present (Skill and System Prompt), but they belong to different agent modules of the suite - the quoted System Prompt is the `itinerary` agent's runtime prompt, while the quoted Skill is the `flights` agent definition. No same-agent Prompt/Skill/Tool pair exists, and a Tool Schema artifact is absent, so QD-PS, QD-PT, QD-ST, and QD-CYC-1.1 have no in-scope same-agent pair (cross-artifact checks are never run across different agents).

Informational observation (not a Stage B verdict line): QD-CYC-1.2 (Multi-Agent Circular Invocation) was reviewed at suite level - the 3-phase pipeline dispatches 12 search agents in parallel and then two synthesis agents (itinerary, stress-test); the itinerary agent reads hotels + ranked activities and the stress-test agent audits the finished itinerary. No cyclic role invocation (Agent A calling Agent B and back) is declared. No closed loop was found.

---

## 5. Stage C - Gate-0 (admission)

- G0-1 (no unfixed P0 in Stage A): NOT satisfied - recorded as an informational finding; does not gate this flow.
- G0-2 (no unfixed P0 in Stage B): N/A - Stage B did not run; recorded as informational.
- G0-3 (responsibility boundary statements exist and are locatable): Passed - the Skill and the Prompt state their roles (e.g. `.agents/flights.md` "You are an expert flight search specialist for a travel planning application."; the itinerary prompt "Create a day-by-day travel itinerary for {destination}").
- G0-4 (each Tool Schema's `name`, `description`, parameter descriptions complete): NOT passed - no Tool Schema artifact is present (tools are declared as bare names with no parameter schema).

Gate-0 result: **Not passed - G0-4**.

---

## 6. Stage D - Permission (QD-PM Quick Mode)

Subset: Inspect Permission Governance Specification (QD-PM)
Execution Status: Not Executed
Unsatisfied Conditions: G0-4 (structural admission); additionally the full artifact set is incomplete (no Tool Schema, and the Skill set is only partially quoted).
Blocking Reasons:
  G0-4 - Tool Schema `name`/`description`/parameter descriptions are not complete (no Tool Schema artifact is present).
  Artifact-set precondition - the full set (Prompt + Skill + all Tool Schemas) is not present.
Remediation Actions: Fix the above upstream items, then re-run Gate-0.

(The Permission stage was "Not Executed"; this is not a FAIL and not a permission conclusion.)

---

## 7. Stage E - Risk Explicit audit (EX) - physically separated from Inspect verdicts

Audit object: TC-098 Skill (`flights`) + System Prompt (itinerary) + embedded snippets.
Three-phase scan (NL-A -> NL-B -> NR-O -> NR-S) run over the bundled artifacts.

Risk Item Summary:
- Total Risk Items: 0
- Explicit·P0 (Block release): 0 items
- Explicit·P1 (Fix / exemption): 0 items
- Explicit·P2 (Risk ledger): 0 items

Note: no explicitly declared risk expression (self-contained exfiltration, identity/permission claim, constraint removal, priority override, dangerous flag, hardcoded credential/PII, or abnormal callback) was found in the static artifact text. The multi-city order constraint ("do NOT reorder") and the price-sorting rule are behavioural constraints, not risk expressions. This is a static-document scan only; it is not a security conclusion. Risk Implicit (dynamic exploitability) was NOT run.

---

## 8. Stage F - Impact outlook (candidate mapping, advisory only)

Advisory context only; it does not change, soften, or escalate any Inspect conclusion. Strength is association confidence, NOT severity. Candidate language only. Risk Implicit and the runtime Quality subsets were NOT run; the lite embedded-code QC ran in Stage A. Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent.

| Defect (FAIL) | Candidate attack surface (AS-*) | Candidate failure modes (FM-*) | Strength (provisional, lite) |
|---|---|---|---|
| QD-S-1.1, QD-S-1.4 | AS-04, AS-05, AS-06 | FM-05, FM-09 | Medium |
| QD-S-3.4 | AS-01, AS-05 | FM-02, FM-07, FM-09 | Medium |
| QD-S-4.1 | AS-07 | FM-08, FM-09 | Conditional |
| QD-S-3.1, QD-S-3.2, QD-S-4.2, QD-S-4.3, QD-S-5.1 | AS-01, AS-04, AS-05, AS-07 | FM-02, FM-07, FM-08, FM-09 | Conditional |
| QD-P-2.2.2, QD-P-2.2.3, QD-P-2.2.4 | AS-02, AS-07 | FM-01, FM-04 | Medium |
| QD-P-2.3.3, QD-P-2.3.4 | AS-03, AS-09 | FM-06 | Conditional |
| QD-P-2.5.2, QD-P-2.5.3 | AS-01, AS-03, AS-04, AS-05 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.7.1, QD-P-2.7.2, QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |
| QC-3.2 | (no AS-* row in Appendix A; snippet-level only) | (no B.1 group) | Not Applicable (out of Appendix A mapping scope) |

Candidate RAG-Agent quality metrics (candidate associations only; NOT a quality result): Completeness, Timeliness, Robustness, Relevance, Decomposition Capability, Boundary Recognition. Defect chains (SC-*/QC-*) are out of scope for lite v1.

---

## 9. Status board

Stage A (Single-artifact):  Executed - QD-S (L2, `flights` Skill), QD-P (L2, itinerary prompt), QD-T (N/A, no Tool Schema), QC (embedded snippets).
Stage B (Cross):            Not Executed - no same-agent Prompt/Skill/Tool pair (quoted Prompt and Skill belong to different agents of the suite; no Tool Schema).
Stage C (Gate-0):           Not passed - G0-4 (G0-1/G0-2 informational).
Stage D (Permission QD-PM): Not Executed - Gate-0 G0-4 not satisfied; full artifact set incomplete (no Tool Schema).
Stage E (Risk Explicit EX): Executed - 0 findings.
Stage F (Impact outlook):   Executed - candidate mapping for all Stage A FAILs.
Stage G (Self-verification): Executed - ID back-closure, red-line wording, output contract checked.

---

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. No in-place self-corrections were required.
