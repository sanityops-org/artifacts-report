# SanityOps Inspect Lite Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-14
Artifact version: not supplied by the user (using the case's Collection Date as the working label)

---

## 1. Executive summary (Sec. 6.1)

- Stages executed: A (single-artifact), B (cross-artifact, Prompt-Skill only), C (Gate-0), E (Risk Explicit), F (impact outlook), G (self-verification). Stage D did not run (incomplete artifact set - no Tool Schema).
- Finding counts (Stage A + B): Inspect P0 = 38, P1 = 49, P2 = 0.
- Gate-0 result: Not passed (G0-3 passed; G0-4 not satisfiable - no Tool Schema is present).
- Risk-Explicit summary (Stage E): Explicit.P0 = 0, Explicit.P1 = 0, Explicit.P2 = 1.
- Top findings (rule ID - one-line defect):
  1. QD-S-5.1 / QD-S-1.4 - The forget Skill deletes remote memories without a read/write/delete distinction (confirmation is declared, but scope is not).
  2. QD-P-2.3.4 / QD-P-2.5.2 - The Prompt (TypeScript tool-description strings) declares no privacy filtering or security boundaries.
  3. QD-S-1.1 / QD-S-1.3 (all invoking Skills) - No input-size limit and no retry/timeout/tool-call bound on the CLI-backed Skills.
  4. QD-P-1.3.2 / QD-P-1.3.3 - Vague trigger wording ("may help") and undefined behavioral boundaries.
  5. QD-PS-1.3 - The Prompt authorizes no permission scope while the forget Skill performs deletes.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The lite embedded-code QC was run in Stage A.
- This report never states a security or quality conclusion; Inspect PASS is not Risk PASS and not Quality PASS.
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and version-level evidence chains, use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

---

## 2. Artifact inventory (input preparation, not a stage)

Case TC-034 is a single agent memory-layer plugin (Mem0 agent-plugin-core). All artifacts belong to the same agent. Types present, by structural signature:

- System Prompt (present, partial): the "Prompts (TypeScript)" constants (`SEARCH_WHEN`, `SEARCH_TOOL_DESCRIPTION`, `SEARCH_QUERY_DESCRIPTION`, `RECALL_HEADING`, user variants). Basis: prose/instruction strings.
- Skill (present, 6): remember, search, forget, pause, resume, status (markdown with `name`/`description` front matter). Basis: front-matter signature.
- Tool Schema (absent): `search_memories` is referenced by the search Skill but no `parameters` schema is shown. Basis: no JSON Schema / function-calling definition present.
- Out of coverage: the 10 harness plugins and the 6 top-level `skills/mem0-*` skills are outside this case's scope.

---

## 3. Stage A - Single-artifact inspection

### 3.A.1 System Prompt set (TypeScript prompt constants)

Tier determination: **L2 Multi-turn Interactive**. Basis: the prompt strings drive a bounded RAG-style search behaviour with 1-3 tool invocations (`search_memories`) and no complex workflow. Scope = L2 (40 items).

- QD-P-1.1.1 | PASS | evidence: TC-034, prompt strings are mutually consistent.
- QD-P-1.1.2 | PASS | evidence: TC-034, no conflicting priorities.
- QD-P-1.1.3 | PASS | evidence: TC-034, no examples contradicting a rule.
- QD-P-1.2.1 | PASS | evidence: TC-034, no explicit role identity is defined (not triggered).
- QD-P-1.2.2 | PASS | evidence: TC-034, no style rule conflicts.
- QD-P-1.2.3 | PASS | evidence: TC-034, no constraint prohibits a declared responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-034, no quantifier-scope misuse found.
- QD-P-1.3.2 | FAIL | evidence: TC-034, `SEARCH_WHEN` "or when earlier decisions ... may help" uses a vague qualifier for the trigger.
- QD-P-1.3.3 | FAIL | evidence: TC-034, no authorization/prohibition scope or handoff condition is declared.
- QD-P-1.4.1 | PASS | evidence: TC-034, no duplicate constraint found.
- QD-P-1.4.2 | PASS | evidence: TC-034, declared branches are reachable.
- QD-P-1.4.3 | PASS | evidence: TC-034, no Skill definition is given in the Prompt (vacuous).
- QD-P-1.5.1 | PASS | evidence: TC-034, declared behavior supports the memory-retrieval objective.
- QD-P-1.5.2 | FAIL | evidence: TC-034, the prompt references `search_memories` but defines no corresponding resource.
- QD-P-1.6.1 | PASS | evidence: TC-034, no vague word carries a security/permission decision.
- QD-P-1.6.2 | PASS | evidence: TC-034, no rule keys on unobservable model internal state.
- QD-P-1.6.3 | PASS | evidence: TC-034, no unresolved implicit Soft-Rule conflict found.
- QD-P-1.6.4 | PASS | evidence: TC-034, no internal reasoning-method constraint found.
- QD-P-1.6.5 | PASS | evidence: TC-034, no self-referential/recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-034, no unstated-assumption dependency found.
- QD-P-1.6.7 | PASS | evidence: TC-034, no rule requires revising earlier conclusions on new information.
- QD-P-2.2.1 | FAIL | evidence: TC-034, no input source is declared.
- QD-P-2.2.2 | FAIL | evidence: TC-034, the search query input format is unconstrained.
- QD-P-2.2.3 | FAIL | evidence: TC-034, required vs optional inputs are not distinguished.
- QD-P-2.2.4 | FAIL | evidence: TC-034, no missing-input handling is declared.
- QD-P-2.3.1 | FAIL | evidence: TC-034, no output format is declared.
- QD-P-2.3.2 | FAIL | evidence: TC-034, no output schema/fields are declared.
- QD-P-2.3.3 | FAIL | evidence: TC-034, no output stability assurance is declared.
- QD-P-2.3.4 | FAIL | evidence: TC-034, no sensitive-data filtering or privacy handling is declared.
- QD-P-2.4.1 | FAIL | evidence: TC-034, no workflow step sequence is defined.
- QD-P-2.4.2 | FAIL | evidence: TC-034, the `search_memories` tool is named but not declared as a resource.
- QD-P-2.4.3 | FAIL | evidence: TC-034, no tool invocation parameters, sequence, or failure handling are defined.
- QD-P-2.5.1 | FAIL | evidence: TC-034, no termination/iteration limit is declared.
- QD-P-2.5.2 | FAIL | evidence: TC-034, no prohibited operations or access boundaries are declared.
- QD-P-2.5.3 | FAIL | evidence: TC-034, no permission control boundaries are declared.
- QD-P-2.5.4 | FAIL | evidence: TC-034, no arbitration rules for potential constraint conflicts are declared.
- QD-P-2.5.5 | FAIL | evidence: TC-034, no resource invocation frequency limits are declared.
- QD-P-2.7.1 | FAIL | evidence: TC-034, no positive examples are provided.
- QD-P-2.7.2 | FAIL | evidence: TC-034, no counter-examples are provided.
- QD-P-2.7.3 | FAIL | evidence: TC-034, no boundary-case examples are provided.

### 3.A.2 Skills

Skill risk-level determination: remember = **L1** (text restatement only, no tool invocation); search = **L2** (calls the read-only `search_memories` tool); forget = **L3** (deletes remote memories - irreversible); pause = **L2** (changes capture state, recoverable); resume = **L2** (changes capture state, recoverable); status = **L2** (runs diagnostic commands, read-only).

QD-S-0 baseline (all six skills): QD-S-0.1 PASS (`name`/`description` present in each); QD-S-0.2 PASS (non-empty); QD-S-0.3 PASS (YAML front matter parses); QD-S-0.4 PASS (field types valid, including boolean `disable-model-invocation`); QD-S-0.5 PASS (no conflicting declarations); QD-S-0.6 PASS (minimum structure present). Baseline passes; proceed.

#### Skill: remember (L1; scope = 6 mandatory items)

- QD-S-1.1 | FAIL | evidence: TC-034, remember skill declares no input-size/number limit.
- QD-S-1.2 | FAIL | evidence: TC-034, remember skill declares no output-size limit.
- QD-S-2.1 | PASS | evidence: TC-034, remember skill uses no unbounded words.
- QD-S-3.4 | FAIL | evidence: TC-034, remember skill declares no `non_goals`.
- QD-S-4.1 | PASS | evidence: TC-034, remember skill declares "Do not invent a storage confirmation or a memory ID".
- QD-S-3.6 | PASS | evidence: TC-034, remember name/description are consistent with the body.

#### Skill: search (L2; scope = 6 mandatory + 14 recommended)

- QD-S-1.1 | FAIL | evidence: TC-034, search skill declares no input-size limit.
- QD-S-1.3 | FAIL | evidence: TC-034, search skill invokes `search_memories` with no retry/timeout/tool-call bound.
- QD-S-2.1 | PASS | evidence: TC-034, search skill uses no unbounded words.
- QD-S-2.2 | PASS | evidence: TC-034, search skill uses no "until success" wording.
- QD-S-3.4 | FAIL | evidence: TC-034, search skill declares no `non_goals`.
- QD-S-4.1 | FAIL | evidence: TC-034, search skill declares no failure behaviour.
- QD-S-1.2 | FAIL | evidence: TC-034, search skill declares no output-size limit.
- QD-S-1.4 | FAIL | evidence: TC-034, search skill declares no read/write/delete permission distinction.
- QD-S-1.5 | PASS | evidence: TC-034, search skill declares its data source (repo/dir/mine memory scopes).
- QD-S-2.3 | PASS | evidence: TC-034, search skill uses no open-ended enumeration.
- QD-S-2.4 | PASS | evidence: TC-034, search skill verbs are specific.
- QD-S-3.1 | PASS | evidence: TC-034, search trigger is specific.
- QD-S-3.2 | FAIL | evidence: TC-034, search skill declares no deactivation conditions.
- QD-S-3.3 | PASS | evidence: TC-034, search skill declares handling for omitted args ("Omit `top_k` to use Mem0's configured default").
- QD-S-3.6 | PASS | evidence: TC-034, search name/description are consistent with the body.
- QD-S-4.2 | FAIL | evidence: TC-034, search skill declares no partial-completion policy.
- QD-S-4.3 | FAIL | evidence: TC-034, search skill declares no post-failure prohibited behaviours.
- QD-S-5.1 | FAIL | evidence: TC-034, search skill performs memory operations without distinguishing read/modify/delete.
- QD-S-5.3 | FAIL | evidence: TC-034, search skill declares no environment boundary.
- QD-S-5.4 | FAIL | evidence: TC-034, search skill invokes `search_memories` without declaring permitted downstream scope.

#### Skill: forget (L3; scope = 21 mandatory items)

- QD-S-1.1 | FAIL | evidence: TC-034, forget skill declares no input-size limit.
- QD-S-1.2 | FAIL | evidence: TC-034, forget skill declares no output-size limit.
- QD-S-1.3 | FAIL | evidence: TC-034, forget skill runs a CLI command with no retry/timeout/tool-call bound.
- QD-S-1.4 | FAIL | evidence: TC-034, forget skill performs deletion without a read/write/delete distinction.
- QD-S-1.5 | FAIL | evidence: TC-034, forget skill declares no permitted/prohibited data-source boundary.
- QD-S-2.1 | PASS | evidence: TC-034, forget skill uses no unbounded words.
- QD-S-2.2 | PASS | evidence: TC-034, forget skill uses no "until success" wording.
- QD-S-2.3 | PASS | evidence: TC-034, forget skill uses no open-ended enumeration.
- QD-S-2.4 | PASS | evidence: TC-034, forget skill verbs are specific (delete/forget/clear).
- QD-S-3.1 | PASS | evidence: TC-034, forget trigger is specific.
- QD-S-3.2 | PASS | evidence: TC-034, forget skill declares when NOT to delete ("The repository's project memory ... stays unless the user explicitly asks").
- QD-S-3.4 | PASS | evidence: TC-034, forget description scopes the task ("Delete the Mem0 memories stored for this repository and this user").
- QD-S-3.5 | PASS | evidence: TC-034, forget skill declares branch handling (project memory vs own memory; local vs remote).
- QD-S-3.6 | PASS | evidence: TC-034, forget name/description are consistent with the body.
- QD-S-4.1 | PASS | evidence: TC-034, forget skill declares reporting behaviour ("Report what the command output says was deleted").
- QD-S-4.2 | FAIL | evidence: TC-034, forget skill declares no partial-completion policy.
- QD-S-4.3 | FAIL | evidence: TC-034, forget skill declares no post-failure prohibited behaviours.
- QD-S-5.1 | FAIL | evidence: TC-034, forget skill deletes memories without distinguishing read/modify/delete scopes.
- QD-S-5.2 | PASS | evidence: TC-034, forget declares a confirmation mechanism ("Never pass `--yes` before the user has confirmed").
- QD-S-5.3 | FAIL | evidence: TC-034, forget skill declares no environment boundary.
- QD-S-5.4 | FAIL | evidence: TC-034, forget skill invokes `memory_cli.py` without declaring permitted downstream scope.

#### Skill: pause (L2; scope = 6 mandatory + 14 recommended)

- QD-S-1.1 | FAIL | evidence: TC-034, pause skill declares no input-size limit.
- QD-S-1.3 | FAIL | evidence: TC-034, pause skill runs a CLI command with no retry/timeout bound.
- QD-S-2.1 | PASS | evidence: TC-034, pause skill uses no unbounded words.
- QD-S-2.2 | PASS | evidence: TC-034, pause skill uses no "until success" wording.
- QD-S-3.4 | FAIL | evidence: TC-034, pause skill declares no `non_goals`.
- QD-S-4.1 | FAIL | evidence: TC-034, pause skill declares no failure behaviour.
- QD-S-1.2 | FAIL | evidence: TC-034, pause skill declares no output-size limit.
- QD-S-1.4 | FAIL | evidence: TC-034, pause skill declares no read/write/delete permission distinction.
- QD-S-1.5 | PASS | evidence: TC-034, pause skill declares its data source (local hook capture state).
- QD-S-2.3 | PASS | evidence: TC-034, pause skill uses no open-ended enumeration.
- QD-S-2.4 | PASS | evidence: TC-034, pause skill verb is specific ("Pause memory capture").
- QD-S-3.1 | PASS | evidence: TC-034, pause trigger is specific.
- QD-S-3.2 | FAIL | evidence: TC-034, pause skill declares no deactivation conditions.
- QD-S-3.3 | FAIL | evidence: TC-034, pause skill declares no ambiguous-input handling.
- QD-S-3.6 | PASS | evidence: TC-034, pause name/description are consistent with the body.
- QD-S-4.2 | FAIL | evidence: TC-034, pause skill declares no partial-completion policy.
- QD-S-4.3 | FAIL | evidence: TC-034, pause skill declares no post-failure prohibited behaviours.
- QD-S-5.1 | FAIL | evidence: TC-034, pause skill changes state without distinguishing read/modify/delete.
- QD-S-5.3 | FAIL | evidence: TC-034, pause skill declares no environment boundary.
- QD-S-5.4 | FAIL | evidence: TC-034, pause skill invokes `memory_cli.py` without declaring permitted downstream scope.

#### Skill: resume (L2; scope = 6 mandatory + 14 recommended)

- QD-S-1.1 | FAIL | evidence: TC-034, resume skill declares no input-size limit.
- QD-S-1.3 | FAIL | evidence: TC-034, resume skill runs a CLI command with no retry/timeout bound.
- QD-S-2.1 | PASS | evidence: TC-034, resume skill uses no unbounded words.
- QD-S-2.2 | PASS | evidence: TC-034, resume skill uses no "until success" wording.
- QD-S-3.4 | FAIL | evidence: TC-034, resume skill declares no `non_goals`.
- QD-S-4.1 | FAIL | evidence: TC-034, resume skill declares no failure behaviour.
- QD-S-1.2 | FAIL | evidence: TC-034, resume skill declares no output-size limit.
- QD-S-1.4 | FAIL | evidence: TC-034, resume skill declares no read/write/delete permission distinction.
- QD-S-1.5 | PASS | evidence: TC-034, resume skill declares its data source (local hook capture state).
- QD-S-2.3 | PASS | evidence: TC-034, resume skill uses no open-ended enumeration.
- QD-S-2.4 | PASS | evidence: TC-034, resume skill verb is specific ("Resume memory capture").
- QD-S-3.1 | PASS | evidence: TC-034, resume trigger is specific.
- QD-S-3.2 | FAIL | evidence: TC-034, resume skill declares no deactivation conditions.
- QD-S-3.3 | FAIL | evidence: TC-034, resume skill declares no ambiguous-input handling.
- QD-S-3.6 | PASS | evidence: TC-034, resume name/description are consistent with the body.
- QD-S-4.2 | FAIL | evidence: TC-034, resume skill declares no partial-completion policy.
- QD-S-4.3 | FAIL | evidence: TC-034, resume skill declares no post-failure prohibited behaviours.
- QD-S-5.1 | FAIL | evidence: TC-034, resume skill changes state without distinguishing read/modify/delete.
- QD-S-5.3 | FAIL | evidence: TC-034, resume skill declares no environment boundary.
- QD-S-5.4 | FAIL | evidence: TC-034, resume skill invokes `memory_cli.py` without declaring permitted downstream scope.

#### Skill: status (L2; scope = 6 mandatory + 14 recommended)

- QD-S-1.1 | FAIL | evidence: TC-034, status skill declares no input-size limit.
- QD-S-1.3 | FAIL | evidence: TC-034, status skill runs two CLI commands with no retry/timeout bound.
- QD-S-2.1 | PASS | evidence: TC-034, status skill uses no unbounded words.
- QD-S-2.2 | PASS | evidence: TC-034, status skill uses no "until success" wording.
- QD-S-3.4 | FAIL | evidence: TC-034, status skill declares no `non_goals`.
- QD-S-4.1 | PASS | evidence: TC-034, status skill declares auth-failure handling ("say clearly that the Mem0 API key is invalid or expired").
- QD-S-1.2 | FAIL | evidence: TC-034, status skill declares no output-size limit.
- QD-S-1.4 | FAIL | evidence: TC-034, status skill declares no read/write/delete permission distinction.
- QD-S-1.5 | PASS | evidence: TC-034, status skill declares its data source (the JSON status/doctor output).
- QD-S-2.3 | PASS | evidence: TC-034, status skill uses no open-ended enumeration.
- QD-S-2.4 | PASS | evidence: TC-034, status skill verb is specific ("Show whether Mem0 memory is working").
- QD-S-3.1 | PASS | evidence: TC-034, status trigger is specific.
- QD-S-3.2 | FAIL | evidence: TC-034, status skill declares no deactivation conditions.
- QD-S-3.3 | PASS | evidence: TC-034, status skill declares handling ("using only fields the JSON actually reports").
- QD-S-3.6 | PASS | evidence: TC-034, status name/description are consistent with the body.
- QD-S-4.2 | FAIL | evidence: TC-034, status skill declares no partial-completion policy.
- QD-S-4.3 | FAIL | evidence: TC-034, status skill declares no post-failure prohibited behaviours.
- QD-S-5.1 | FAIL | evidence: TC-034, status skill reads/writes no data without distinguishing scopes (read-only, but undistinguished).
- QD-S-5.3 | FAIL | evidence: TC-034, status skill declares no environment boundary.
- QD-S-5.4 | FAIL | evidence: TC-034, status skill invokes `memory_cli.py` without declaring permitted downstream scope.

### 3.A.3 Embedded code snippets (QC)

No Tool Schema is present; QC runs over the code snippets embedded in the Prompt and Skill artifacts.

- QC-0.1 | PASS | evidence: TC-034, the `typescript`/`bash` snippets parse as valid syntax.
- QC-0.2 | PASS | evidence: TC-034, snippets are fenced with `typescript`/`bash`/`markdown`.
- QC-0.3 | FAIL | evidence: TC-034, the `typescript` block declares exported constants only and references no imports/types (partial standalone).
- QC-1.1 | N/A | evidence: TC-034, no undefined name reference inside the shown snippets (determination basis: only string constants).
- QC-1.2 | N/A | evidence: TC-034, no import statement present (determination basis: no such pattern).
- QC-1.3 | PASS | evidence: TC-034, no deprecated API usage present.
- QC-1.4 | N/A | evidence: TC-034, no typed function call present (determination basis: no such pattern).
- QC-2.1 | N/A | evidence: TC-034, no file-handle pattern in the shown code (determination basis: no such pattern).
- QC-2.2 | N/A | evidence: TC-034, no connection constructor opened without close (determination basis: no such pattern).
- QC-2.3 | N/A | evidence: TC-034, no high-risk file/network/DB call in the shown snippets (determination basis: no such pattern).
- QC-3.1 | N/A | evidence: TC-034, no import statement present (determination basis: no such pattern).
- QC-3.2 | PASS | evidence: TC-034, no referenced-but-unimported name in the constants block.
- QC-3.3 | PASS | evidence: TC-034, the `ntn_your_key_here`-style value is absent; only `~/.config/notion`-style paths appear (no credential placeholder).

---

## 4. Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Run condition met: two same-agent artifact types are present (System Prompt + Skill). No Tool Schema is present, so QD-PT / QD-ST are not applicable. Tier = **L2** (default severities; no Appendix C L3 blanket upgrade).

### QD-PS (Prompt -> Skill)

- QD-PS-1.1 Skill Authorization Consistency | PASS | evidence: Prompt (TC-034, `SEARCH_TOOL_DESCRIPTION`) does not restrict the skill set; no Skill is defined-but-unauthorized.
- QD-PS-1.2 Trigger Condition Consistency | FAIL (P1) | evidence: Prompt (TC-034, `SEARCH_WHEN`) defines a search heuristic; Skill (search SKILL.md) defines its own trigger without alignment.
- QD-PS-1.3 Permission Boundary Consistency | FAIL (P0) | evidence: Prompt (TC-034, prompt constants) authorizes no explicit scope; Skill (forget SKILL.md "permanently deletes remote memories") exceeds it.
- QD-PS-1.4 Resource Access Consistency | FAIL (P1) | evidence: Prompt (TC-034) declares no allowed resources; Skill (search/status SKILL.md) declares repo/remote memory access.
- QD-PT-2.1..2.6 | Not Applicable | evidence: no Tool Schema present.
- QD-ST-3.1..3.7 | Not Applicable | evidence: no Tool Schema present.

### QD-CYC (circular invocation)

- QD-CYC-1.1 Cross-Artifact Circular Invocation | PASS | evidence: Prompt/Skill invocation relationships (TC-034) show no closed loop.
- QD-CYC-1.2 Multi-Agent Circular Invocation | PASS | evidence: the Prompt defines a single agent role (TC-034, no orchestration); no role cycle.

---

## 5. Stage C - Gate-0 (admission)

- G0-1 (no unfixed P0 in Stage A): NOT satisfied - recorded as an informational finding; does not gate this flow.
- G0-2 (no unfixed P0 in Stage B): NOT satisfied - recorded as an informational finding; does not gate this flow.
- G0-3 (responsibility boundary statements exist and are locatable): Passed - the six Skill descriptions (TC-034) define each capability and its scope.
- G0-4 (each Tool Schema's `name`, `description`, parameter descriptions complete): NOT passed - no Tool Schema is present to verify.

Gate-0 result: **Not passed - G0-4**.

---

## 6. Stage D - Permission (QD-PM Quick Mode)

Subset: Inspect Permission Governance Specification (QD-PM)
Execution Status: Not Executed
Unsatisfied Conditions: G0-4; incomplete artifact set
Blocking Reasons:
  G0-4 - no Tool Schema is present, so tool field completeness cannot be verified.
  Incomplete artifact set - the Permission stage requires System Prompt + Skill + all Tool Schemas; no Tool Schema is present.
Remediation Actions: Fix the above upstream items, then re-run Gate-0.

(This is not a FAIL and not a permission conclusion.)

---

## 7. Stage E - Risk Explicit audit (EX) - physically separated from Inspect verdicts

Audit object: TC-034 System Prompt set + Skills.

Risk Item Summary:
- Total Risk Items: 1
- Explicit.P0 (Block release): 0 items
- Explicit.P1 (Fix / exemption): 0 items
- Explicit.P2 (Risk ledger): 1 item

Risk Item Details:

[Risk Item 1]
- EX Classification: NL-A-2
- Risk Expression: "a minimal telemetry ping still fires at session start, under your Mem0 account email, unless `MEM0_TELEMETRY=false`" (TC-034, pause SKILL.md)
- Severity Grade: Explicit.P2
- Reason: The artifact explicitly declares an outbound telemetry transmission tied to the user's account email; it stays within the existing product scope and is opt-outable, matching P2.
- Impact Type Labels: D1
- Trigger Condition Label: unconditional
- Disposition: Record in risk ledger
- Remediation Suggestion: State the telemetry payload and retention explicitly, and keep the opt-out prominent.

Note: This is a static-document risk scan of explicitly declared text only; it is not a confirmed exploit and not a security conclusion. Risk Implicit (dynamic exploitability) was NOT run.

---

## 8. Stage F - Impact outlook (candidate mapping, advisory only)

Advisory context only; it does not change, soften, or escalate any Inspect conclusion. Strength is association confidence, NOT severity. Candidate language only. Risk Implicit and the runtime Quality subsets were NOT run; the lite embedded-code QC ran in Stage A. Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent.

| Defect (FAIL) | Candidate attack surface (AS-*) | Candidate failure modes (FM-*) | Strength (provisional, lite) |
|---|---|---|---|
| QD-P-1.3.2, QD-P-1.3.3 | AS-01, AS-04 | FM-01, FM-02, FM-07, FM-09 | Medium |
| QD-P-1.5.2, QD-P-2.4.2 | AS-05, AS-07, AS-09 | FM-03, FM-04, FM-05 | Strong (referenced tool undeclared) |
| QD-P-2.2.1, QD-P-2.2.2, QD-P-2.2.3, QD-P-2.2.4 | AS-01, AS-02 | FM-01, FM-04 | Medium |
| QD-P-2.3.1, QD-P-2.3.2, QD-P-2.3.3 | AS-03, AS-09 | FM-06 | Conditional |
| QD-P-2.3.4, QD-P-2.5.2, QD-P-2.5.3 | AS-01, AS-03, AS-04, AS-05 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.4.1, QD-P-2.4.3 | AS-05, AS-07, AS-09 | FM-03, FM-04, FM-05 | Strong |
| QD-P-2.5.1, QD-P-2.5.4, QD-P-2.5.5, QD-P-2.7.1, QD-P-2.7.2, QD-P-2.7.3 | AS-06, AS-07 | FM-08, FM-09, FM-10 | Conditional |
| QD-S-1.1, QD-S-1.2, QD-S-1.3 (skills) | AS-06 | Availability | Medium |
| QD-S-1.4, QD-S-5.1 (skills) | AS-04, AS-05 | FM-05, FM-09 | Strong (delete without scope distinction) |
| QD-S-3.2, QD-S-3.3, QD-S-3.4 (skills) | AS-01, AS-05 | FM-02, FM-07, FM-09 | Medium |
| QD-S-4.1, QD-S-4.2, QD-S-4.3 (skills) | AS-07 | FM-08, FM-09 | Medium |
| QD-S-5.3, QD-S-5.4 (skills) | AS-04, AS-05 | FM-05, FM-09 | Strong |
| QC-0.3 | (no AS-* row in Appendix A; snippet-level only) | (no B.1 group) | Not Applicable (out of Appendix A mapping scope) |
| QD-PS-1.2, QD-PS-1.3, QD-PS-1.4 | AS-03, AS-04, AS-09 | FM-04, FM-05, FM-06, FM-08 | Medium |

Candidate RAG-Agent quality metrics (candidate associations only; NOT a quality result): Correctness, Completeness, Robustness, Boundary Recognition, Safety Response, Traceability. Defect chains (SC-*/QC-TA-*/QC-RA-*) are out of scope for lite v1.

---

## 9. Status board

Stage A (Single-artifact):  Executed - QD-P (L2), QD-S (remember L1; search/pause/resume/status L2; forget L3), QC.
Stage B (Cross):            Executed - two same-agent artifact types present (Prompt + Skill); QD-PT/QD-ST not applicable.
Stage C (Gate-0):           Not passed - G0-4 (G0-1/G0-2 informational).
Stage D (Permission QD-PM): Not Executed - incomplete artifact set (no Tool Schema; Gate-0 G0-4 not satisfied).
Stage E (Risk Explicit EX): Executed - 1 finding (Explicit.P2 = 1).
Stage F (Impact outlook):   Executed - candidate mapping for all Stage A/B FAILs.
Stage G (Self-verification): Executed - ID back-closure, red-line wording, output contract checked.

---

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. No in-place self-corrections were required.
