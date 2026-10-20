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
- Finding counts (Stage A, System Prompt set): Inspect P0 = 11, P1 = 0, P2 = 0.
- Gate-0 result: Not passed (G0-3 passed; G0-4 not satisfied - the six-action vocabulary is defined inline in prose, not as a JSON `parameters` schema).
- Risk-Explicit summary (Stage E): Explicit.P0 = 0, Explicit.P1 = 0, Explicit.P2 = 0.
- Top findings (rule ID - one-line defect):
  1. QD-P-2.5.2 / QD-P-2.5.3 - No security boundary or permission-control boundary is declared for an agent that operates the user's phone via ADB.
  2. QD-P-2.3.4 - No sensitive-data filtering or privacy output constraint is declared, although the agent reads the user's screen.
  3. QD-P-2.6.1 / QD-P-2.6.2 - Runtime exceptions have no declared handling or degradation strategy (unparseable action output, dead-cycle risk).
  4. QD-P-2.2.3 / QD-P-2.2.4 - Input required/optional marking and missing-input handling are undeclared.
  5. QD-P-2.7.1 / QD-P-2.7.2 / QD-P-2.7.3 - No positive, counter, or boundary-case example is provided.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The lite embedded-code QC was run in Stage A.
- This report never states a security or quality conclusion; Inspect PASS is not Risk PASS and not Quality PASS.
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and version-level evidence chains, use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

---

## 2. Artifact inventory (input preparation, not a stage)

Case TC-091 bundles one multi-agent mobile-GUI automation suite (Mobile-Agent-v2). Artifact types present, by structural signature:

- System Prompt (present, verbatim): the three per-agent system one-liners (`init_action_chat`, `init_reflect_chat`, `init_memory_chat`) plus the working instruction builders (`get_action_prompt`, `get_reflect_prompt`, `get_memory_prompt`, `get_process_prompt`). Basis: prose/instruction strings.
- Skill (absent): no markdown file with `name`/`description` front matter defines an invokable capability.
- Tool Schema (absent): the six-action vocabulary (`Open app`, `Tap`, `Swipe`, `Type`, `Home`, `Stop`) is defined inline in prose, not as a JSON Schema / function-calling definition with a `parameters` block.
- Orchestration config (reference, not an artifact type): `run.py` (feature switches and the perceive -> decide -> act -> reflect -> remember -> progress loop).
- Embedded code snippets (QC scope): the `init_*_chat` functions, the prompt builders and the loop excerpts.
- Out of coverage: the perception modules (OCR/icon detection/captioning), the `MobileAgent.api` inference layer and the ADB action helpers are referenced but not quoted.

Scope note: the Operator/Decision, Reflection, Memory and Progress roles are sub-functions of one orchestrated mobile-automation pipeline, so all artifacts belong to the same agent suite and no artifact from another case is mixed in.

---

## 3. Stage A - Single-artifact inspection

### 3.A.1 System Prompt set (per-agent system one-liners + prompt builders)

Tier determination: **L3 Complex Agent**. Basis (any 2 or more of the L3 criteria): 4+ tool/action invocations (six actions); complex workflow exceeding 5 steps (perceive -> decide -> act -> reflect -> remember -> progress, repeated); security-sensitive (it drives the user's real device UI and reads the screen); requires exception handling (unparseable action output, dead-cycle risk). Upward-compatible L3 scope = 47 items.

- QD-P-1.1.1 | PASS | evidence: TC-091, the prompts, no mutually exclusive attribute or directive found; the keyboard-inactive "Type" restriction is explicitly conditioned.
- QD-P-1.1.2 | PASS | evidence: TC-091, the action/reflection/memory prompts do not conflict in any declared scenario.
- QD-P-1.1.3 | PASS | evidence: TC-091, no worked example contradicts a rule.
- QD-P-1.2.1 | PASS | evidence: TC-091, each role is a sub-function of the same phone-operating assistant and its responsibility is carried by its instruction builder.
- QD-P-1.2.2 | PASS | evidence: TC-091, the role voice matches the declared output style (### Thought ### / ### Action ### / ### Operation ###).
- QD-P-1.2.3 | PASS | evidence: TC-091, no constraint prohibits a role's core responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-091, the action step is bounded - "perform just one action on the current page".
- QD-P-1.3.2 | PASS | evidence: TC-091, the vague words ("brief", "closely related") are secondary descriptors.
- QD-P-1.3.3 | PASS | evidence: TC-091, the six-action vocabulary and the "Stop" condition declare the action boundary; the "Type" restriction declares a prohibition.
- QD-P-1.4.1 | PASS | evidence: TC-091, no duplicate constraint found.
- QD-P-1.4.2 | PASS | evidence: TC-091, all six actions and the three reflection answers (A/B/C) are reachable.
- QD-P-1.4.3 | PASS | evidence: TC-091, no Skill definition is given in the prompts (vacuous).
- QD-P-1.5.1 | PASS | evidence: TC-091, the roles' responsibilities support the objective (complete the user's instruction on the phone).
- QD-P-1.5.2 | PASS | evidence: TC-091, the workflow resources (screenshot, clickable-info extraction, keyboard state, memory) are declared as provided.
- QD-P-1.6.1 | PASS | evidence: TC-091, no vague word carries a security/permission boundary.
- QD-P-1.6.2 | PASS | evidence: TC-091, decisions are grounded in the screenshot/observation; the Stop trigger ("If you think all the requirements ... have been completed") is a task-completion judgment, not an unreportable internal-state key.
- QD-P-1.6.3 | PASS | evidence: TC-091, no soft rules are declared in mutually unreconciled tension.
- QD-P-1.6.4 | PASS | evidence: TC-091, no constraint fixes an internal reasoning method.
- QD-P-1.6.5 | PASS | evidence: TC-091, no self-referential or recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-091, the assumed perception inputs are declared ("we extract some information on the current screenshot through system files").
- QD-P-1.6.7 | PASS | evidence: TC-091, the Reflection agent provides a revision mechanism (A/B/C) that corrects earlier actions.
- QD-P-2.1.1 | PASS | evidence: TC-091, formatting is readable.
- QD-P-2.1.2 | PASS | evidence: TC-091, the references (screenshot, clickable info, keyboard state, history) are named and locatable.
- QD-P-2.1.3 | PASS | evidence: TC-091, the section hierarchy (Background -> Screenshot information -> Response requirements -> Output format) is reasonable.
- QD-P-2.1.4 | PASS | evidence: TC-091, prose is concise.
- QD-P-2.2.1 | PASS | evidence: TC-091, the input source is declared (the user's instruction and the extracted screenshot information).
- QD-P-2.2.2 | PASS | evidence: TC-091, the perception-info format is declared - "The format of the coordinates is [x, y] ... the content is a text or an icon description".
- QD-P-2.2.3 | FAIL | evidence: TC-091, no input field (screenshot, clickable info, keyboard state, memory) is marked required or optional.
- QD-P-2.2.4 | FAIL | evidence: TC-091, no behavior is declared when an input (e.g. clickable info or memory) is missing.
- QD-P-2.3.1 | PASS | evidence: TC-091, the output format is declared ("### Thought ### / ### Action ### / ### Operation ###"; reflection "### Answer ###").
- QD-P-2.3.2 | PASS | evidence: TC-091, the output fields are declared (Thought, Action, Operation; Answer A/B/C).
- QD-P-2.3.3 | PASS | evidence: TC-091, the strict three-part format bounds output format stability.
- QD-P-2.3.4 | FAIL | evidence: TC-091, no sensitive-data filtering, privacy handling, or security output constraint is declared although the agent reads the user's screen.
- QD-P-2.4.1 | PASS | evidence: TC-091, the workflow steps are complete (perceive -> decide -> act -> reflect -> remember -> progress).
- QD-P-2.4.2 | PASS | evidence: TC-091, the six actions are declared as the available operations.
- QD-P-2.4.3 | PASS | evidence: TC-091, the action invocation syntax is declared inline ("Tap (x, y)", "Swipe (x1, y1), (x2, y2)", "Type (text)").
- QD-P-2.5.1 | PASS | evidence: TC-091, the termination condition is declared (the "Stop" action).
- QD-P-2.5.2 | FAIL | evidence: TC-091, no prohibited operation, sensitive-data access boundary, or external-access boundary is declared for an agent that drives the user's device UI.
- QD-P-2.5.3 | FAIL | evidence: TC-091, no permission scope or escalation boundary is declared.
- QD-P-2.5.4 | PASS | evidence: TC-091, no soft-constraint conflict requires an arbitration rule.
- QD-P-2.5.5 | FAIL | evidence: TC-091, no resource/action invocation frequency limit is declared.
- QD-P-2.6.1 | FAIL | evidence: TC-091, no handling is declared for runtime exceptions such as unparseable model output (the case notes dispatch matches nothing when no action keyword is present).
- QD-P-2.6.2 | FAIL | evidence: TC-091, no degradation or recovery strategy is declared (the case notes a possible dead cycle).
- QD-P-2.6.3 | PASS | evidence: TC-091, no retry mechanism is declared (vacuous).
- QD-P-2.7.1 | FAIL | evidence: TC-091, no representative worked example is provided (only the action-syntax descriptions).
- QD-P-2.7.2 | FAIL | evidence: TC-091, no counter-examples are provided.
- QD-P-2.7.3 | FAIL | evidence: TC-091, no boundary-case examples are provided.

### 3.A.2 Skill

- QD-S-1.x .. QD-S-5.x | N/A | evidence: TC-091 carries no Skill artifact (determination basis: no markdown file with `name`/`description` front matter defines an invokable capability). No QD-S verdict is emitted.

### 3.A.3 Tool Schema

- QD-T-1.x .. QD-T-4.x | N/A | evidence: TC-091 carries no Tool Schema artifact (determination basis: the six-action vocabulary is defined inline in prose, not as a JSON `parameters`/`inputSchema` schema with per-parameter descriptions). No QD-T verdict is emitted.

### 3.A.4 Embedded code snippets (QC)

QC-0 baseline: the Python snippets (`init_*_chat`, the prompt builders, the `run.py` loop excerpts) are fenced as `python`.

- QC-0.1 | PASS | evidence: TC-091, the snippets parse as valid Python syntax.
- QC-0.2 | PASS | evidence: TC-091, the code blocks declare `python`.
- QC-0.3 | PASS | evidence: TC-091, each shown function/loop excerpt is complete within its excerpt.
- QC-0.4 | PASS | evidence: TC-091, the code fences open and close correctly.
- QC-0.5 | PASS | evidence: TC-091, the declared language (`python`) matches the content.
- QC-1.1 | PASS | evidence: TC-091, names such as `inference_chat`, `add_response` and `home` are helper functions whose imports are outside the excerpt.
- QC-1.2 | Not Executed | evidence: TC-091, no declared dependency list is available (dependency-context rule); not recorded as FAIL.
- QC-1.3 | Not Executed | evidence: TC-091, no API version database is available (dependency-context rule); not recorded as FAIL.
- QC-1.4 | PASS | evidence: TC-091, no type-mismatched call found.
- QC-2.1 .. QC-2.3 | N/A | evidence: TC-091, no file-handle, network-connection or high-risk call pattern is present in the snippets (determination basis: no such pattern).
- QC-3.1 | N/A | evidence: TC-091, imports are outside the excerpt, so no unused-import determination is made.
- QC-3.2 | PASS | evidence: TC-091, helper functions are referenced without visible imports because the excerpt omits the module header.
- QC-3.3 | PASS | evidence: TC-091, the literals are a model identifier (`'gpt-4o'`) and variable names (`API_url`, `ADB_path`), not hardcoded credentials or machine-specific secrets.
- QC-4.1 | PASS | evidence: TC-091, the parsed output sections (### Thought ### / ### Action ### / ### Operation ###) match the declared output format.
- QC-4.2 | PASS | evidence: TC-091, no version/API drift between the snippets and the body.

---

## 4. Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Stage status: **Not Executed**. Reason: only one Logic Artifact type (System Prompt) is present; the six-action vocabulary is prose inside the prompt, not a Tool Schema, so no Prompt/Skill/Tool pair exists and QD-PS (Prompt -> Skill), QD-PT (Prompt -> Tool), QD-ST (Skill <-> Tool) and QD-CYC-1.1 have no counterpart artifact.

Informational observation (not a Stage B verdict line): QD-CYC-1.2 (Multi-Agent Circular Invocation) was reviewed at suite level - the loop is a sequential single-trajectory cycle (Operator -> action -> Reflection -> Memory -> Progress), not a mutual role cycle where Agent A calls Agent B and back. No closed loop was found.

---

## 5. Stage C - Gate-0 (admission)

- G0-1 (no unfixed P0 in Stage A): NOT satisfied - recorded as an informational finding; does not gate this flow.
- G0-2 (no unfixed P0 in Stage B): N/A - Stage B did not run; recorded as informational.
- G0-3 (responsibility boundary statements exist and are locatable): Passed - each agent prompt states its role (e.g. Operator "You are a helpful AI mobile phone operating assistant. You need to help me operate the phone to complete the user's instruction."; the Process builder "You are a mobile phone operating assistant and are operating the user's mobile phone.").
- G0-4 (each Tool Schema's `name`, `description`, parameter descriptions complete): NOT passed - no Tool Schema artifact is present (the six actions are prose inside the prompt).

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

Audit object: TC-091 System Prompt set (three one-liners + four builders) + embedded snippets.
Three-phase scan (NL-A -> NL-B -> NR-O -> NR-S) run over the bundled artifacts.

Risk Item Summary:
- Total Risk Items: 0
- Explicit.P0 (Block release): 0 items
- Explicit.P1 (Fix / exemption): 0 items
- Explicit.P2 (Risk ledger): 0 items

Note: no explicitly declared risk expression (self-contained exfiltration, identity/permission claim, constraint removal, priority override, dangerous flag, hardcoded credential/PII, or abnormal callback) was found in the static artifact text. Operating the user's phone and reading its screen is the declared core task, not an EX-category risk expression. This is a static-document scan only; it is not a security conclusion. Risk Implicit (dynamic exploitability) was NOT run.

---

## 8. Stage F - Impact outlook (candidate mapping, advisory only)

Advisory context only; it does not change, soften, or escalate any Inspect conclusion. Strength is association confidence, NOT severity. Candidate language only. Risk Implicit and the runtime Quality subsets were NOT run; the lite embedded-code QC ran in Stage A. Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent.

| Defect (FAIL) | Candidate attack surface (AS-*) | Candidate failure modes (FM-*) | Strength (provisional, lite) |
|---|---|---|---|
| QD-P-2.2.3, QD-P-2.2.4 | AS-02, AS-07 | FM-01, FM-04 | Medium (input necessity/missing handling undeclared) |
| QD-P-2.3.4 | AS-03 | FM-06 | Conditional |
| QD-P-2.5.2, QD-P-2.5.3 | AS-01, AS-03, AS-04, AS-05 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.5.5 | AS-06 | FM-08, FM-09, FM-10 | Conditional |
| QD-P-2.6.1, QD-P-2.6.2 | AS-07 | FM-08, FM-10 | Medium |
| QD-P-2.7.1, QD-P-2.7.2, QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |

Candidate RAG-Agent quality metrics (candidate associations only; NOT a quality result): Correctness, Robustness, Consistency, Format Compliance, Boundary Recognition, Safety Response. Defect chains (SC-*/QC-TA-*/QC-RA-*) are out of scope for lite v1.

---

## 9. Status board

Stage A (Single-artifact):  Executed - QD-P (L3, 3 agent prompts + 4 builders), QD-T (N/A, no Tool Schema), QD-S (N/A, no Skill), QC (embedded Python snippets).
Stage B (Cross):            Not Executed - only one artifact type present (System Prompt); no Prompt/Skill/Tool pair exists.
Stage C (Gate-0):           Not passed - G0-4 (G0-1/G0-2 informational).
Stage D (Permission QD-PM): Not Executed - Gate-0 G0-4 not satisfied; full artifact set incomplete (no Skill, no Tool Schema).
Stage E (Risk Explicit EX): Executed - 0 findings.
Stage F (Impact outlook):   Executed - candidate mapping for all Stage A FAILs.
Stage G (Self-verification): Executed - ID back-closure, red-line wording, output contract checked.

---

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. No in-place self-corrections were required.
