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
- Finding counts (Stage A, System Prompt set): Inspect P0 = 16, P1 = 0, P2 = 0.
- Gate-0 result: Not passed (G0-3 passed; G0-4 not satisfied - no Tool Schema artifact is present; the UI action APIs are injected via the `{apis}` placeholder and no JSON `parameters`/`inputSchema` schema is shown).
- Risk-Explicit summary (Stage E): Explicit.P0 = 0, Explicit.P1 = 0, Explicit.P2 = 0.
- Top findings (rule ID - one-line defect):
  1. QD-P-2.5.2 / QD-P-2.5.3 - No security or permission boundary constraint is declared for an agent that drives the user's Windows UI.
  2. QD-P-2.3.4 - No sensitive-data filtering or privacy output constraint is declared.
  3. QD-P-2.2.2 / QD-P-2.2.3 / QD-P-2.2.4 - Input format, required/optional marking, and missing-input handling are all undeclared.
  4. QD-P-1.1.3 - The worked examples contradict the stated rules (empty `ControlLabel` with a non-empty `ControlText`, and non-parseable JSON examples while `json.loads()` success is required).
  5. QD-P-2.6.1 / QD-P-2.6.2 - Runtime exceptions have no handling or degradation strategy, although the prompt itself warns a parse failure "will crash the system".
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The lite embedded-code QC was run in Stage A.
- This report never states a security or quality conclusion; Inspect PASS is not Risk PASS and not Quality PASS.
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and version-level evidence chains, use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

---

## 2. Artifact inventory (input preparation, not a stage)

Case TC-065 bundles one two-stage Windows office-automation agent suite (Microsoft UFO task instantiation pipeline). Artifact types present, by structural signature:

- System Prompt (present, 2): the task-judge prompt in `filter.yaml` (a `system:` instruction block) and the task-creator/planner prompt in `prefill.yaml` (a `system:` instruction block). Basis: prose/instruction strings in the `system:` YAML field.
- Skill (absent): the case's "Skill Definitions" section holds three reference tables (interactive control vocabulary, judge classification labels, action-call output schema). Basis: none is a markdown file with `name`/`description` front matter defining an invokable capability, so none is a Skill artifact.
- Tool Schema (absent): the case shows the planner's `{apis}` placeholder and an "Action Call Format" but no JSON Schema / function-calling definition with a `parameters`/`inputSchema` block. Basis: no schema object is present.
- Embedded code snippets (QC scope): the two YAML prompt templates and the JSON example objects they contain.
- Out of coverage: `{apis}`, `{examples}`, the doc screenshot and the Doc Control State payloads are runtime-injected and not quoted; no other pipeline file is quoted.

Scope note: the judge and the planner are two stages of one orchestrated office-automation pipeline (judge gate -> planner), so all artifacts belong to the same agent suite and no artifact from another case is mixed in.

---

## 3. Stage A - Single-artifact inspection

### 3.A.1 System Prompt set (task judge + task planner)

Tier determination: **L3 Complex Agent**. Basis (any 2 or more of the L3 criteria): the pipeline drives the user's Windows/Office UI and is security-sensitive (the prompt warns a malformed output "will crash the system and destroy the user's computer"); action plans require a complex, potentially >5-step workflow over a fixed UI-control/action vocabulary; the prompt itself requires exception handling for JSON parseability. Upward-compatible L3 scope = 47 items.

- QD-P-1.1.1 | PASS | evidence: TC-065, filter.yaml + prefill.yaml, no mutually exclusive attribute or directive found.
- QD-P-1.1.2 | PASS | evidence: TC-065, filter.yaml + prefill.yaml, the enumerated judge criteria and the planner rules do not conflict in any declared scenario.
- QD-P-1.1.3 | FAIL | evidence: TC-065, prefill.yaml "Action Call Format" examples contradict the stated rules - example Step 1 uses an empty `ControlLabel` with a non-empty `ControlText` although the rule says "The control text must match exactly with the selected control label", and the examples are not parseable JSON although the prompt requires output "able to be parsed by json.loads()".
- QD-P-1.2.1 | PASS | evidence: TC-065, filter.yaml + prefill.yaml, each role (task judge; task creator/planner) matches its stated responsibilities.
- QD-P-1.2.2 | PASS | evidence: TC-065, prefill.yaml, the role voice matches the declared JSON output style.
- QD-P-1.2.3 | PASS | evidence: TC-065, filter.yaml + prefill.yaml, the constraints (JSON-only, fixed control vocabulary) do not prohibit the core responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-065, prefill.yaml, quantities are bounded ("can only add up to 50 words", "focus on a single action").
- QD-P-1.3.2 | PASS | evidence: TC-065, filter.yaml + prefill.yaml, the vague terms found ("choose the most suitable ones") are secondary descriptors, not a decision boundary.
- QD-P-1.3.3 | FAIL | evidence: TC-065, prefill.yaml, the boundary of an acceptable control target is left undefined where the prompt states "If the function to call need to specify controlText and none of the control item is suitable for the task,you should input a possible control name." - the agent is licensed to invent an out-of-vocabulary control target.
- QD-P-1.4.1 | PASS | evidence: TC-065, filter.yaml + prefill.yaml, no duplicate constraint found.
- QD-P-1.4.2 | PASS | evidence: TC-065, filter.yaml, the classification branches (None/Non_task/App_involve/Env/Others) are all reachable.
- QD-P-1.4.3 | PASS | evidence: TC-065, filter.yaml + prefill.yaml, no Skill definition is given in the prompt set (vacuous).
- QD-P-1.5.1 | PASS | evidence: TC-065, filter.yaml + prefill.yaml, the enumerated responsibilities support the objective (judge local executability; emit a grounded action plan).
- QD-P-1.5.2 | PASS | evidence: TC-065, prefill.yaml, the workflow resources (`{apis}`, screenshot, Doc Control State) are declared as runtime-provided.
- QD-P-1.6.1 | FAIL | evidence: TC-065, filter.yaml, a vague decision word carries a classification decision - "There are other things that you think cannot be executed or are irrelevant, return False, and be classified as Others" defines no criterion.
- QD-P-1.6.2 | PASS | evidence: TC-065, filter.yaml + prefill.yaml, the decision criteria are enumerated in the prompt text, not keyed on unreportable internal state.
- QD-P-1.6.3 | PASS | evidence: TC-065, prefill.yaml, the soft rules (be specific; be non-verbose) are not declared in mutual tension.
- QD-P-1.6.4 | PASS | evidence: TC-065, filter.yaml + prefill.yaml, no constraint fixes an internal reasoning method beyond the given checklist.
- QD-P-1.6.5 | PASS | evidence: TC-065, filter.yaml + prefill.yaml, no self-referential or recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-065, prefill.yaml, the assumed availability of screenshot/control-state inputs is stated in the prompt ("you will also be provided with a screenshot").
- QD-P-1.6.7 | PASS | evidence: TC-065, filter.yaml + prefill.yaml, each stage is invoked once per request and declares no multi-turn update path (determination basis: single-shot judge/planner, no conversation).
- QD-P-2.1.1 | PASS | evidence: TC-065, filter.yaml + prefill.yaml, formatting is readable.
- QD-P-2.1.2 | PASS | evidence: TC-065, prefill.yaml, the references (`<Available Actions>`, `<Doc Control State:>`, `{apis}`) are named and locatable at runtime.
- QD-P-2.1.3 | PASS | evidence: TC-065, filter.yaml + prefill.yaml, the section hierarchy (evaluation dimensions -> response format -> requirements) is reasonable.
- QD-P-2.1.4 | PASS | evidence: TC-065, filter.yaml + prefill.yaml, prose is concise (source typos do not affect conciseness).
- QD-P-2.2.1 | PASS | evidence: TC-065, prefill.yaml, the input source is declared (`<Given Task:> {given_task}`, `<Reference Steps:>`, provided screenshot and control state).
- QD-P-2.2.2 | FAIL | evidence: TC-065, prefill.yaml, the input data format is unconstrained - the abstract `<Given Task>` and the provided screenshot/control state carry no declared format, encoding, or size limit.
- QD-P-2.2.3 | FAIL | evidence: TC-065, prefill.yaml, no input field is marked required or optional (no default handling for the screenshot, control state, `{apis}` or `{examples}`).
- QD-P-2.2.4 | FAIL | evidence: TC-065, prefill.yaml, handling of missing input is undefined - no behavior is declared when the screenshot, Doc Control State, or available-actions list is absent.
- QD-P-2.3.1 | PASS | evidence: TC-065, prefill.yaml, output format is declared ("You are required to response in a JSON format").
- QD-P-2.3.2 | PASS | evidence: TC-065, prefill.yaml, the output schema fields are declared (Observation, Thought, New_task, Actions_plan; Step/Subtask/ControlLabel/ControlText/Function/Args).
- QD-P-2.3.3 | PASS | evidence: TC-065, prefill.yaml, format stability is bounded ("Make sure your answer must be strictly in JSON format only" plus the required `json.loads()`).
- QD-P-2.3.4 | FAIL | evidence: TC-065, filter.yaml + prefill.yaml, no sensitive-data filtering, privacy handling, or security output constraint is declared.
- QD-P-2.4.1 | PASS | evidence: TC-065, prefill.yaml, the workflow steps are complete (given task -> instantiate -> ground in control state -> emit action plan).
- QD-P-2.4.2 | PASS | evidence: TC-065, prefill.yaml, the resources/tools used are declared (`<Available Actions>` / `{apis}` and the control-item vocabulary).
- QD-P-2.4.3 | PASS | evidence: TC-065, prefill.yaml, an invocation specification is given (the Action Call Format with `Function`/`Args`).
- QD-P-2.5.1 | PASS | evidence: TC-065, prefill.yaml, no loop or recursion is declared (vacuous).
- QD-P-2.5.2 | FAIL | evidence: TC-065, filter.yaml + prefill.yaml, no prohibited operation, sensitive-data access boundary, or external-access boundary is declared for an agent that automates the user's OS UI.
- QD-P-2.5.3 | FAIL | evidence: TC-065, filter.yaml + prefill.yaml, no permission scope or escalation boundary is declared.
- QD-P-2.5.4 | FAIL | evidence: TC-065, prefill.yaml, two constraints can conflict with no arbitration declared - rule 5 (">New Task> can only add up to 50 words") versus rule 6 (the target "should be specific and clear").
- QD-P-2.5.5 | FAIL | evidence: TC-065, prefill.yaml, no resource-invocation frequency limit is declared for the UI action APIs.
- QD-P-2.6.1 | FAIL | evidence: TC-065, prefill.yaml, runtime exception handling is not declared although the prompt itself states the failure mode ("Otherwise, it will crash the system and destroy the user's computer.") with no recovery path.
- QD-P-2.6.2 | FAIL | evidence: TC-065, filter.yaml + prefill.yaml, no degradation or recovery strategy is declared.
- QD-P-2.6.3 | PASS | evidence: TC-065, prefill.yaml, no retry mechanism is declared (vacuous).
- QD-P-2.7.1 | FAIL | evidence: TC-065, prefill.yaml, the only positive examples are three single-action formatting samples; no representative end-to-end planner example is provided.
- QD-P-2.7.2 | FAIL | evidence: TC-065, filter.yaml + prefill.yaml, no counter-examples are provided (the judge only shows one response shape).
- QD-P-2.7.3 | FAIL | evidence: TC-065, filter.yaml + prefill.yaml, no boundary-case examples are provided.

### 3.A.2 Skill

- QD-S-1.x .. QD-S-5.x | N/A | evidence: TC-065 carries no Skill artifact (determination basis: no markdown file with `name`/`description` front matter defines an invokable capability; the "Skill Definitions" tables are reference material). No QD-S verdict is emitted.

### 3.A.3 Tool Schema

- QD-T-1.x .. QD-T-4.x | N/A | evidence: TC-065 carries no Tool Schema artifact (determination basis: the `{apis}` placeholder and the Action Call Format describe UI action functions but show no JSON `parameters`/`inputSchema` schema). No QD-T verdict is emitted.

### 3.A.4 Embedded code snippets (QC)

QC-0 baseline: the snippets inside the two YAML templates are the JSON example objects and the JSON "Response Format" block; each is marked as illustrative ("Below is only a example of the response", "e.g."), so the illustrative-snippet rule exempts them from the QC-0.1 / QC-0.3 parse-completeness requirement.

- QC-0.1 | PASS | evidence: TC-065, prefill.yaml, the snippets are illustrative examples (exempt); the enclosing YAML templates parse.
- QC-0.2 | PASS | evidence: TC-065, filter.yaml + prefill.yaml, the templates are fenced as `yaml`.
- QC-0.3 | PASS | evidence: TC-065, the JSON examples are illustrative and exempt from structural completeness (recorded: they are not standalone-parseable JSON, which is reported under QD-P-1.1.3, not re-scored here).
- QC-0.4 | PASS | evidence: TC-065, the code fences open and close correctly.
- QC-0.5 | PASS | evidence: TC-065, the declared languages (`yaml`) match the fence content.
- QC-1.1 | N/A | evidence: TC-065, no executable code with name references is present (determination basis: the snippets are data/example JSON only).
- QC-1.2 | Not Executed | evidence: TC-065, no declared dependency list is available (dependency-context rule); not recorded as FAIL.
- QC-1.3 | Not Executed | evidence: TC-065, no API version database is available (dependency-context rule); not recorded as FAIL.
- QC-1.4 | N/A | evidence: TC-065, no function call with typed arguments is present (determination basis: data-only snippets).
- QC-2.1 | N/A | evidence: TC-065, no file-handle pattern present (determination basis: no such pattern).
- QC-2.2 | N/A | evidence: TC-065, no network-connection constructor present (determination basis: no such pattern).
- QC-2.3 | N/A | evidence: TC-065, no high-risk file/network/DB call present (determination basis: no such pattern).
- QC-3.1 | N/A | evidence: TC-065, no imports present (determination basis: data-only snippets).
- QC-3.2 | N/A | evidence: TC-065, no referenced symbols requiring imports (determination basis: data-only snippets).
- QC-3.3 | PASS | evidence: TC-065, the only literal strings are functional examples ("Test For Fun", "Borders"); no credential, local path or machine-specific value.
- QC-4.1 | PASS | evidence: TC-065, the examples use the same field names as the declared output schema.
- QC-4.2 | PASS | evidence: TC-065, no version/API drift between the snippets and the body.

---

## 4. Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Stage status: **Not Executed**. Reason: only one Logic Artifact type (System Prompt) is present; no Prompt/Skill/Tool pair exists, so QD-PS (Prompt -> Skill), QD-PT (Prompt -> Tool), QD-ST (Skill <-> Tool), and QD-CYC-1.1 have no counterpart artifact and are Not Applicable.

Informational observation (not a Stage B verdict line): QD-CYC-1.2 (Multi-Agent Circular Invocation) was reviewed at suite level - the judge and the planner are sequential stages of one pipeline (judge -> planner) with no cyclic role orchestration declared. No closed loop was found.

---

## 5. Stage C - Gate-0 (admission)

- G0-1 (no unfixed P0 in Stage A): NOT satisfied - recorded as an informational finding; does not gate this flow.
- G0-2 (no unfixed P0 in Stage B): N/A - Stage B did not run; recorded as informational.
- G0-3 (responsibility boundary statements exist and are locatable): Passed - each prompt states its role and scope (e.g. filter.yaml "You are a task judge, will be provided with a task in the <Task:>."; prefill.yaml "You are a Agent Task Creator and planer.").
- G0-4 (each Tool Schema's `name`, `description`, parameter descriptions complete): NOT passed - no Tool Schema artifact is present (UI action APIs are injected via `{apis}` with no parameter schema).

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

Audit object: TC-065 System Prompt set (task judge + task planner) + embedded example snippets.
Three-phase scan (NL-A -> NL-B -> NR-O -> NR-S) run over the bundled artifacts.

Risk Item Summary:
- Total Risk Items: 0
- Explicit.P0 (Block release): 0 items
- Explicit.P1 (Fix / exemption): 0 items
- Explicit.P2 (Risk ledger): 0 items

Note: no explicitly declared risk expression (self-contained exfiltration, identity/permission claim, constraint removal, priority override, dangerous flag, hardcoded credential/PII, or abnormal callback) was found in the static artifact text. The reward line ("I will tip you 200$ if you do well") and the crash warning ("it will crash the system and destroy the user's computer") are pressure/error warnings, not risk expressions matching a defined EX subcategory. This is a static-document scan only; it is not a security conclusion. Risk Implicit (dynamic exploitability) was NOT run.

---

## 8. Stage F - Impact outlook (candidate mapping, advisory only)

Advisory context only; it does not change, soften, or escalate any Inspect conclusion. Strength is association confidence, NOT severity. Candidate language only. Risk Implicit and the runtime Quality subsets were NOT run; the lite embedded-code QC ran in Stage A. Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent.

| Defect (FAIL) | Candidate attack surface (AS-*) | Candidate failure modes (FM-*) | Strength (provisional, lite) |
|---|---|---|---|
| QD-P-1.1.3 | AS-01, AS-05 | FM-01, FM-02, FM-07, FM-09 | Conditional (examples may override body rules) |
| QD-P-1.3.3 | AS-01, AS-04 | FM-01, FM-02, FM-07, FM-09 | Medium (out-of-vocabulary control target allowed) |
| QD-P-1.6.1 | AS-01, AS-04 | FM-01, FM-02, FM-07, FM-09 | Conditional |
| QD-P-2.2.2, QD-P-2.2.3, QD-P-2.2.4 | AS-02, AS-07 | FM-01, FM-04 | Medium (input format/necessity/missing handling undeclared) |
| QD-P-2.3.4 | AS-03 | FM-06 | Conditional |
| QD-P-2.5.2, QD-P-2.5.3 | AS-01, AS-03, AS-04, AS-05 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.5.4, QD-P-2.5.5 | AS-01, AS-06, AS-07 | FM-08, FM-09, FM-10 | Conditional |
| QD-P-2.6.1, QD-P-2.6.2 | AS-07 | FM-08, FM-10 | Conditional |
| QD-P-2.7.1, QD-P-2.7.2, QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |

Candidate RAG-Agent quality metrics (candidate associations only; NOT a quality result): Correctness, Robustness, Consistency, Format Compliance, Boundary Recognition, Safety Response. Defect chains (SC-*/QC-*) are out of scope for lite v1.

---

## 9. Status board

Stage A (Single-artifact):  Executed - QD-P (L3, task judge + task planner), QD-T (N/A, no Tool Schema), QD-S (N/A, no Skill), QC (embedded YAML/JSON snippets).
Stage B (Cross):            Not Executed - only one artifact type present (System Prompt); no Prompt/Skill/Tool pair exists.
Stage C (Gate-0):           Not passed - G0-4 (G0-1/G0-2 informational).
Stage D (Permission QD-PM): Not Executed - Gate-0 G0-4 not satisfied; full artifact set incomplete (no Skill, no Tool Schema).
Stage E (Risk Explicit EX): Executed - 0 findings.
Stage F (Impact outlook):   Executed - candidate mapping for all Stage A FAILs.
Stage G (Self-verification): Executed - ID back-closure, red-line wording, output contract checked.

---

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. No in-place self-corrections were required.
