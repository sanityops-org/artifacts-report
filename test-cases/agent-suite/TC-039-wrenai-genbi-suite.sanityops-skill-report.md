# SanityOps Inspect Lite Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-14
Artifact version: not supplied by the user (using the case's Collection Date as the working label)

---

## 1. Executive summary (Sec. 6.1)

- Stages executed: A (single-artifact), B (cross-artifact, Prompt-Skill only), C (Gate-0), E (Risk Explicit), F (impact outlook), G (self-verification). Stage D did not run (Gate-0 G0-4 not satisfied / incomplete artifact set).
- Finding counts (Stage A + B): Inspect P0 = 36, P1 = 2, P2 = 0.
- Gate-0 result: Not passed (G0-3 passed; G0-4 not satisfied - no Tool Schema is present).
- Risk-Explicit summary (Stage E): Explicit.P0 = 0, Explicit.P1 = 0, Explicit.P2 = 0.
- Top findings (rule ID - one-line defect):
  1. QD-S-5.1 / QD-S-5.2 - The genbi Skill deploys a public app (`wren genbi deploy`) with no read/write/delete distinction and no explicit confirmation mechanism.
  2. QD-P-2.5.2 / QD-P-2.4.2 - AGENTS.md declares no security boundaries and no tool/resource set.
  3. QD-S-1.3 / QD-S-1.4 - The genbi Skill runs `wren` with no retry/timeout bound and no permission distinction.
  4. QD-PS-1.3 - The Prompt authorizes no scope while the genbi Skill deploys/publishes.
  5. QD-S-3.4 / QD-S-4.2 - The genbi Skill declares no `non_goals` and no partial-completion policy.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The lite embedded-code QC was run in Stage A.
- This report never states a security or quality conclusion; Inspect PASS is not Risk PASS and not Quality PASS.
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and version-level evidence chains, use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

---

## 2. Artifact inventory (input preparation, not a stage)

Case TC-039 is a single GenBI platform agent (WrenAI). All artifacts belong to the same agent. Types present, by structural signature:

- System Prompt (present): the Repository `AGENTS.md`. Basis: prose/markdown instructions.
- Skill (present): the `genbi` skill (markdown with `name`/`description`/`license`/`metadata` front matter); the Available Skills table lists 7 skills. Basis: front-matter signature.
- Tool Schema (absent): the `wren` CLI commands are described as a quick-reference table, not as JSON Schema / function-calling definitions. Basis: no `parameters` + `description` schema.
- Out of coverage: the other 6 skills' bodies and the CLI implementation are not quoted; only the shown text is inspected.

---

## 3. Stage A - Single-artifact inspection

### 3.A.1 System Prompt set (Repository AGENTS.md)

Tier determination: **L3 Complex Agent**. Basis: 4+ tool invocations (7 skills via the `wren` CLI), complex multi-step workflow, security-sensitive (warehouse access, public deploy). Scope = L3 (47 items).

- QD-P-1.1.1 | PASS | evidence: TC-039, AGENTS.md statements are mutually consistent.
- QD-P-1.1.2 | PASS | evidence: TC-039, no conflicting directives.
- QD-P-1.1.3 | PASS | evidence: TC-039, no example contradicting a rule.
- QD-P-1.2.1 | PASS | evidence: TC-039, no explicit agent role is defined (not triggered).
- QD-P-1.2.2 | PASS | evidence: TC-039, no style rule mismatch.
- QD-P-1.2.3 | PASS | evidence: TC-039, no constraint prohibits a declared responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-039, no quantifier-scope misuse found.
- QD-P-1.3.2 | PASS | evidence: TC-039, no vague qualifier carries a critical decision.
- QD-P-1.3.3 | FAIL | evidence: TC-039, AGENTS.md declares no authorization/prohibition scope or handoff condition.
- QD-P-1.4.1 | PASS | evidence: TC-039, no duplicate constraint found.
- QD-P-1.4.2 | PASS | evidence: TC-039, declared branches are reachable.
- QD-P-1.4.3 | PASS | evidence: TC-039, no Skill definition is given in the Prompt (vacuous).
- QD-P-1.5.1 | PASS | evidence: TC-039, the declared behaviour supports the contribution objective.
- QD-P-1.5.2 | FAIL | evidence: TC-039, AGENTS.md refers to `.claude/CLAUDE.md` and module guides that are not defined in the resource set.
- QD-P-1.6.1 | PASS | evidence: TC-039, no vague word carries a security/permission decision.
- QD-P-1.6.2 | PASS | evidence: TC-039, no rule keys on unobservable model internal state.
- QD-P-1.6.3 | PASS | evidence: TC-039, no unresolved implicit Soft-Rule conflict found.
- QD-P-1.6.4 | PASS | evidence: TC-039, no internal reasoning-method constraint found.
- QD-P-1.6.5 | PASS | evidence: TC-039, no self-referential/recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-039, no unstated-assumption dependency found.
- QD-P-1.6.7 | PASS | evidence: TC-039, no rule requires revising earlier conclusions on new information.
- QD-P-2.1.1 | PASS | evidence: TC-039, prompt formatting is readable.
- QD-P-2.1.2 | PASS | evidence: TC-039, references (file paths) are specific.
- QD-P-2.1.3 | PASS | evidence: TC-039, heading hierarchy is reasonable.
- QD-P-2.1.4 | PASS | evidence: TC-039, prose is concise.
- QD-P-2.2.1 | FAIL | evidence: TC-039, no input source (user / system / external data) is declared.
- QD-P-2.2.2 | PASS | evidence: TC-039, input is conversational (no structured parser defined).
- QD-P-2.2.3 | PASS | evidence: TC-039, no parameterized input declared (not triggered).
- QD-P-2.2.4 | FAIL | evidence: TC-039, no missing-input handling is declared.
- QD-P-2.3.1 | FAIL | evidence: TC-039, no output format is declared.
- QD-P-2.3.2 | FAIL | evidence: TC-039, no output schema/fields are declared.
- QD-P-2.3.3 | FAIL | evidence: TC-039, no output stability assurance is declared.
- QD-P-2.3.4 | FAIL | evidence: TC-039, no sensitive-data filtering or privacy handling is declared.
- QD-P-2.4.1 | FAIL | evidence: TC-039, no workflow step sequence is defined.
- QD-P-2.4.2 | FAIL | evidence: TC-039, the `wren` CLI tools are not declared as resources.
- QD-P-2.4.3 | FAIL | evidence: TC-039, no tool invocation parameters, sequence, or failure handling are defined.
- QD-P-2.5.1 | FAIL | evidence: TC-039, no loop/recursion termination condition is declared.
- QD-P-2.5.2 | FAIL | evidence: TC-039, no prohibited operations or access boundaries are declared.
- QD-P-2.5.3 | FAIL | evidence: TC-039, no permission scope is declared for the CLI/warehouse capabilities.
- QD-P-2.5.4 | PASS | evidence: TC-039, no conflicting soft constraints requiring priority arbitration found.
- QD-P-2.5.5 | FAIL | evidence: TC-039, no resource invocation frequency limits are declared.
- QD-P-2.6.1 | FAIL | evidence: TC-039, no runtime exception handling is declared.
- QD-P-2.6.2 | FAIL | evidence: TC-039, no degradation/recovery strategy is declared.
- QD-P-2.6.3 | PASS | evidence: TC-039, no unreasonable retry mechanism found.
- QD-P-2.7.1 | FAIL | evidence: TC-039, no positive examples are provided.
- QD-P-2.7.2 | FAIL | evidence: TC-039, no counter-examples are provided.
- QD-P-2.7.3 | FAIL | evidence: TC-039, no boundary-case examples are provided.

### 3.A.2 Skill - genbi

Skill risk-level determination: genbi = **L3** (deploys/publishes a public app and writes application code - irreversible external publishing). Scope = L3 (21 items).

QD-S-0 baseline: QD-S-0.1 PASS (`name`/`description` present); QD-S-0.2 PASS (non-empty); QD-S-0.3 PASS (YAML front matter parses); QD-S-0.4 PASS (types valid); QD-S-0.5 PASS (no conflicting declarations); QD-S-0.6 PASS (minimum structure present). Baseline passes; proceed.

- QD-S-1.1 | FAIL | evidence: TC-039, genbi skill declares no input-size limit.
- QD-S-1.2 | FAIL | evidence: TC-039, genbi skill declares no output-size limit.
- QD-S-1.3 | FAIL | evidence: TC-039, genbi skill runs `wren genbi build/register/verify/deploy` with no retry/timeout/tool-call bound.
- QD-S-1.4 | FAIL | evidence: TC-039, genbi skill deploys and writes app files without a read/write/delete distinction.
- QD-S-1.5 | PASS | evidence: TC-039, genbi skill declares its data source (the Wren project context layer / warehouse).
- QD-S-2.1 | PASS | evidence: TC-039, genbi skill uses no unbounded words.
- QD-S-2.2 | PASS | evidence: TC-039, genbi skill uses no "until success" wording.
- QD-S-2.3 | PASS | evidence: TC-039, genbi skill uses no open-ended enumeration.
- QD-S-2.4 | PASS | evidence: TC-039, genbi skill verbs are specific (build/register/verify/deploy).
- QD-S-3.1 | PASS | evidence: TC-039, genbi trigger is specific ("Use this skill whenever the user wants to: build a dashboard ...").
- QD-S-3.2 | FAIL | evidence: TC-039, genbi skill declares no deactivation conditions ("NOT for ...").
- QD-S-3.4 | FAIL | evidence: TC-039, genbi skill declares no `non_goals`.
- QD-S-3.5 | PASS | evidence: TC-039, genbi skill declares branch handling (snapshot vs live data mode; preconditions).
- QD-S-3.6 | PASS | evidence: TC-039, genbi name/description are consistent with the body.
- QD-S-4.1 | FAIL | evidence: TC-039, genbi skill declares no failure behaviour beyond a `verify` preflight.
- QD-S-4.2 | FAIL | evidence: TC-039, genbi skill declares no partial-completion policy.
- QD-S-4.3 | FAIL | evidence: TC-039, genbi skill declares no post-failure prohibited behaviours.
- QD-S-5.1 | FAIL | evidence: TC-039, genbi skill writes code and deploys without distinguishing read/modify/delete.
- QD-S-5.2 | FAIL | evidence: TC-039, genbi skill `deploy` (public publish) has no explicit confirmation mechanism.
- QD-S-5.3 | PASS | evidence: TC-039, genbi skill distinguishes production deployment via the `--prod` flag.
- QD-S-5.4 | FAIL | evidence: TC-039, genbi skill invokes the `wren` CLI without declaring permitted downstream scope.

### 3.A.3 Embedded code snippets (QC)

- QC-0.1 | PASS | evidence: TC-039, the `bash` snippets parse as valid syntax.
- QC-0.2 | PASS | evidence: TC-039, snippets are fenced with `bash`/`markdown`.
- QC-0.3 | PASS | evidence: TC-039, the `bash` snippets are complete commands.
- QC-1.1 | N/A | evidence: TC-039, no undefined name reference inside the shown snippets (determination basis: shell commands only).
- QC-1.2 | PASS | evidence: TC-039, no unavailable-module import statement present.
- QC-1.3 | PASS | evidence: TC-039, no deprecated API usage present.
- QC-1.4 | N/A | evidence: TC-039, no typed function call present (determination basis: shell commands only).
- QC-2.1 | N/A | evidence: TC-039, no file-handle pattern in the shown code (determination basis: no such pattern).
- QC-2.2 | N/A | evidence: TC-039, no connection constructor opened without close (determination basis: no such pattern).
- QC-2.3 | N/A | evidence: TC-039, no high-risk file/network/DB call in the shown snippets (determination basis: shell commands only).
- QC-3.1 | N/A | evidence: TC-039, no import statement present (determination basis: no such pattern).
- QC-3.2 | PASS | evidence: TC-039, no referenced-but-unimported name in the snippets.
- QC-3.3 | PASS | evidence: TC-039, no hardcoded demo credential value present; the skill explicitly forbids inlining credentials.

---

## 4. Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Run condition met: two same-agent artifact types are present (System Prompt + Skill). No Tool Schema is present, so QD-PT / QD-ST are not applicable. Tier = **L3** (Appendix C upgrades applied: Agent L3 -> global P1->P0, P2->P1).

### QD-PS (Prompt -> Skill)

- QD-PS-1.1 Skill Authorization Consistency | PASS | evidence: Prompt (TC-039, AGENTS.md) does not restrict the skill set; no Skill is defined-but-unauthorized.
- QD-PS-1.2 Trigger Condition Consistency | FAIL (P0, upgraded from P1 by L3) | evidence: Prompt (TC-039, AGENTS.md) declares no skill triggers; Skill (genbi) defines a trigger - inconsistent.
- QD-PS-1.3 Permission Boundary Consistency | FAIL (P0) | evidence: Prompt (TC-039) authorizes no explicit scope; Skill (genbi "deploy ... a shareable URL") exceeds it.
- QD-PS-1.4 Resource Access Consistency | FAIL (P0, upgraded from P1 by L3) | evidence: Prompt (TC-039) declares no allowed resources; Skill (genbi) declares Wren-project/warehouse access.
- QD-PS-1.5 Failure Handling Consistency | FAIL (P0, upgraded from P1 by L3) | evidence: Prompt (TC-039) defines no failure handling; Skill (genbi) leaves FAILURE undefined - inconsistent.
- QD-PS-1.6 Output Constraint Consistency | FAIL (P1, upgraded from P2 by L3) | evidence: Prompt (TC-039) declares no output constraints; Skill declares none either.
- QD-PT-2.x | Not Applicable | evidence: no Tool Schema present.
- QD-ST-3.x | Not Applicable | evidence: no Tool Schema present.

### QD-CYC (circular invocation)

- QD-CYC-1.1 Cross-Artifact Circular Invocation | PASS | evidence: Prompt/Skill invocation relationships (TC-039) show no closed loop.
- QD-CYC-1.2 Multi-Agent Circular Invocation | PASS | evidence: the Prompt defines one agent role (TC-039); no orchestration cycle.

---

## 5. Stage C - Gate-0 (admission)

- G0-1 (no unfixed P0 in Stage A): NOT satisfied - recorded as an informational finding; does not gate this flow.
- G0-2 (no unfixed P0 in Stage B): NOT satisfied - recorded as an informational finding; does not gate this flow.
- G0-3 (responsibility boundary statements exist and are locatable): Passed - the genbi "Division of labor" section and skill preconditions are locatable.
- G0-4 (each Tool Schema's `name`, `description`, parameter descriptions complete): NOT passed - no Tool Schema is present.

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

Audit object: TC-039 System Prompt set + Skill.

Risk Item Summary:
- Total Risk Items: 0
- Explicit.P0 (Block release): 0 items
- Explicit.P1 (Fix / exemption): 0 items
- Explicit.P2 (Risk ledger): 0 items

No explicitly expressed risk text (NL-A / NL-B / NR-O / NR-S) was found in the shown artifacts. The instruction "NEVER inline credentials" and "`verify` scans for them" are protective constraints, not risk expressions.

Note: This is a static-document risk scan of explicitly declared text only; it is not a confirmed exploit and not a security conclusion. Risk Implicit (dynamic exploitability) was NOT run.

---

## 8. Stage F - Impact outlook (candidate mapping, advisory only)

Advisory context only; it does not change, soften, or escalate any Inspect conclusion. Strength is association confidence, NOT severity. Candidate language only. Risk Implicit and the runtime Quality subsets were NOT run; the lite embedded-code QC ran in Stage A. Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent.

| Defect (FAIL) | Candidate attack surface (AS-*) | Candidate failure modes (FM-*) | Strength (provisional, lite) |
|---|---|---|---|
| QD-P-1.3.3, QD-P-1.5.2 | AS-01, AS-04 | FM-01, FM-02, FM-07, FM-09 | Medium |
| QD-P-2.2.1, QD-P-2.2.4 | AS-01, AS-02 | FM-01, FM-04 | Medium |
| QD-P-2.3.1, QD-P-2.3.2, QD-P-2.3.3 | AS-03, AS-09 | FM-06 | Conditional |
| QD-P-2.3.4, QD-P-2.5.2, QD-P-2.5.3 | AS-01, AS-03, AS-04, AS-05 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.4.1, QD-P-2.4.2, QD-P-2.4.3 | AS-05, AS-07, AS-09 | FM-03, FM-04, FM-05 | Strong |
| QD-P-2.5.1, QD-P-2.5.5, QD-P-2.6.1, QD-P-2.6.2, QD-P-2.7.1, QD-P-2.7.2, QD-P-2.7.3 | AS-06, AS-07 | FM-08, FM-09, FM-10 | Conditional |
| QD-S-1.1, QD-S-1.2, QD-S-1.3 (genbi) | AS-06 | Availability | Medium |
| QD-S-1.4, QD-S-5.1 (genbi) | AS-04, AS-05 | FM-05, FM-09 | Strong (deploy/write without scope) |
| QD-S-5.2 (genbi) | AS-05 | FM-05, FM-09 | Strong (unconfirmed public deploy) |
| QD-S-3.2, QD-S-3.4, QD-S-4.1, QD-S-4.2, QD-S-4.3, QD-S-5.4 (genbi) | AS-01, AS-04, AS-05, AS-07 | FM-02, FM-05, FM-07, FM-09 | Medium |
| QD-PS-1.2, QD-PS-1.3, QD-PS-1.4, QD-PS-1.5, QD-PS-1.6 | AS-03, AS-04, AS-09 | FM-04, FM-05, FM-06, FM-08 | Medium |

Candidate RAG-Agent quality metrics (candidate associations only; NOT a quality result): Correctness, Completeness, Traceability, Safety Response, Boundary Recognition. Defect chains (SC-*/QC-TA-*/QC-RA-*) are out of scope for lite v1.

---

## 9. Status board

Stage A (Single-artifact):  Executed - QD-P (L3), QD-S (genbi L3), QC.
Stage B (Cross):            Executed - two same-agent artifact types present (Prompt + Skill); QD-PT/QD-ST not applicable.
Stage C (Gate-0):           Not passed - G0-4 (G0-1/G0-2 informational).
Stage D (Permission QD-PM): Not Executed - incomplete artifact set (no Tool Schema; Gate-0 G0-4 not satisfied).
Stage E (Risk Explicit EX): Executed - 0 findings.
Stage F (Impact outlook):   Executed - candidate mapping for all Stage A/B FAILs.
Stage G (Self-verification): Executed - ID back-closure, red-line wording, output contract checked.

---

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. No in-place self-corrections were required.
