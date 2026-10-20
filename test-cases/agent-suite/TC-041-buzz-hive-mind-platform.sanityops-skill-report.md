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
- Finding counts (Stage A + B): Inspect P0 = 25, P1 = 9, P2 = 0.
- Gate-0 result: Not passed (G0-3 passed; G0-4 not satisfied - no Tool Schema is present).
- Risk-Explicit summary (Stage E): Explicit.P0 = 0, Explicit.P1 = 0, Explicit.P2 = 0.
- Top findings (rule ID - one-line defect):
  1. QD-PS-1.3 - The Prompt authorizes no scope while the desktop-screenshot Skill writes to GitHub branches/PRs.
  2. QD-P-2.5.2 / QD-P-2.3.4 - AGENTS.md declares no security boundaries and no privacy filtering.
  3. QD-S-1.3 / QD-S-1.4 - The desktop-screenshot Skill runs `just`/Playwright with no retry/timeout bound and no permission distinction.
  4. QD-P-2.4.2 / QD-P-2.4.3 - AGENTS.md declares no tool/resource set or invocation specification.
  5. QD-S-3.3 / QD-S-4.2 - The desktop-screenshot Skill declares no ambiguous-input or partial-completion handling.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The lite embedded-code QC was run in Stage A.
- This report never states a security or quality conclusion; Inspect PASS is not Risk PASS and not Quality PASS.
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and version-level evidence chains, use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

---

## 2. Artifact inventory (input preparation, not a stage)

Case TC-041 is a single hive-mind platform agent (Buzz). All artifacts belong to the same agent. Types present, by structural signature:

- System Prompt (present): the `AGENTS.md` AI-agent contributor guide. Basis: prose/markdown instructions.
- Skill (present): the `desktop-screenshot` skill (markdown with `name`/`description`/`version` front matter); 5 distinct skills are listed as duplicated across framework directories. Basis: front-matter signature.
- Tool Schema (absent): the Relay/CLI/desktop components are described in a repo tree, not as JSON Schema / function-calling definitions. Basis: no `parameters` + `description` schema.
- Out of coverage: the buzz-cli and managed-agent skill bodies, the Rust crates and the desktop app are not quoted.

---

## 3. Stage A - Single-artifact inspection

### 3.A.1 System Prompt set (AGENTS.md)

Tier determination: **L3 Complex Agent**. Basis: 4+ tool invocations (relay, CLI, MCP, managed agents, Playwright), complex multi-step workflow, security-sensitive (multi-framework agents, PR automation). Scope = L3 (47 items).

- QD-P-1.1.1 | PASS | evidence: TC-041, AGENTS.md statements are mutually consistent.
- QD-P-1.1.2 | PASS | evidence: TC-041, no conflicting directives.
- QD-P-1.1.3 | PASS | evidence: TC-041, no example contradicting a rule.
- QD-P-1.2.1 | PASS | evidence: TC-041, the "AI agent contributor" role matches its directives.
- QD-P-1.2.2 | PASS | evidence: TC-041, no style rule mismatch.
- QD-P-1.2.3 | PASS | evidence: TC-041, no constraint prohibits a declared responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-041, no quantifier-scope misuse found.
- QD-P-1.3.2 | PASS | evidence: TC-041, "aiming for 9/10 on each" is a quality target, not a critical decision word.
- QD-P-1.3.3 | FAIL | evidence: TC-041, AGENTS.md declares no authorization/prohibition scope or handoff condition.
- QD-P-1.4.1 | PASS | evidence: TC-041, no duplicate constraint found.
- QD-P-1.4.2 | PASS | evidence: TC-041, declared branches are reachable.
- QD-P-1.4.3 | PASS | evidence: TC-041, no Skill definition is given in the Prompt (vacuous).
- QD-P-1.5.1 | PASS | evidence: TC-041, the declared behaviour supports the contribution objective.
- QD-P-1.5.2 | FAIL | evidence: TC-041, AGENTS.md refers to `VISION.md`, `TESTING.md` that are not defined in the resource set.
- QD-P-1.6.1 | PASS | evidence: TC-041, no vague word carries a security/permission decision.
- QD-P-1.6.2 | PASS | evidence: TC-041, no rule keys on unobservable model internal state.
- QD-P-1.6.3 | PASS | evidence: TC-041, no unresolved implicit Soft-Rule conflict found.
- QD-P-1.6.4 | PASS | evidence: TC-041, no internal reasoning-method constraint found.
- QD-P-1.6.5 | PASS | evidence: TC-041, no self-referential/recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-041, no unstated-assumption dependency found.
- QD-P-1.6.7 | PASS | evidence: TC-041, no rule requires revising earlier conclusions on new information.
- QD-P-2.1.1 | PASS | evidence: TC-041, prompt formatting is readable.
- QD-P-2.1.2 | PASS | evidence: TC-041, references (file paths, sections) are specific.
- QD-P-2.1.3 | PASS | evidence: TC-041, heading hierarchy is reasonable.
- QD-P-2.1.4 | PASS | evidence: TC-041, prose is concise.
- QD-P-2.2.1 | FAIL | evidence: TC-041, no input source (user / system / external data) is declared.
- QD-P-2.2.2 | PASS | evidence: TC-041, no structured input format is required (not triggered).
- QD-P-2.2.3 | PASS | evidence: TC-041, no parameterized input declared (not triggered).
- QD-P-2.2.4 | FAIL | evidence: TC-041, no missing-input handling is declared.
- QD-P-2.3.1 | FAIL | evidence: TC-041, no output format is declared.
- QD-P-2.3.2 | FAIL | evidence: TC-041, no output schema/fields are declared.
- QD-P-2.3.3 | FAIL | evidence: TC-041, no output stability assurance is declared.
- QD-P-2.3.4 | FAIL | evidence: TC-041, no sensitive-data filtering or privacy handling is declared.
- QD-P-2.4.1 | PASS | evidence: TC-041, the "Before opening a PR" checklist defines a step sequence.
- QD-P-2.4.2 | FAIL | evidence: TC-041, the relay/CLI/MCP tools are not declared as resources.
- QD-P-2.4.3 | FAIL | evidence: TC-041, no tool invocation parameters, sequence, or failure handling are defined.
- QD-P-2.5.1 | FAIL | evidence: TC-041, no loop/recursion termination condition is declared.
- QD-P-2.5.2 | FAIL | evidence: TC-041, no prohibited operations or access boundaries are declared.
- QD-P-2.5.3 | FAIL | evidence: TC-041, no permission scope is declared for the agent capabilities.
- QD-P-2.5.4 | PASS | evidence: TC-041, no conflicting soft constraints requiring priority arbitration found.
- QD-P-2.5.5 | FAIL | evidence: TC-041, no resource invocation frequency limits are declared.
- QD-P-2.6.1 | FAIL | evidence: TC-041, no runtime exception handling is declared.
- QD-P-2.6.2 | FAIL | evidence: TC-041, no degradation/recovery strategy is declared.
- QD-P-2.6.3 | PASS | evidence: TC-041, no unreasonable retry mechanism found.
- QD-P-2.7.1 | FAIL | evidence: TC-041, no positive examples are provided.
- QD-P-2.7.2 | FAIL | evidence: TC-041, no counter-examples are provided.
- QD-P-2.7.3 | FAIL | evidence: TC-041, no boundary-case examples are provided.

### 3.A.2 Skill - desktop-screenshot

Skill risk-level determination: desktop-screenshot = **L2** (captures screenshots and posts them to GitHub PR branches - external system write access, recoverable). Scope = L2 (6 mandatory + 14 recommended).

QD-S-0 baseline: QD-S-0.1 PASS (`name`/`description`/`version` present); QD-S-0.2 PASS (non-empty); QD-S-0.3 PASS (YAML front matter parses); QD-S-0.4 PASS (types valid); QD-S-0.5 PASS (no conflicting declarations); QD-S-0.6 PASS (minimum structure present). Baseline passes; proceed.

- QD-S-1.1 | FAIL | evidence: TC-041, desktop-screenshot skill declares no input-size limit.
- QD-S-1.3 | FAIL | evidence: TC-041, desktop-screenshot skill runs `just desktop-screenshot`/Playwright with no retry/timeout/tool-call bound.
- QD-S-2.1 | PASS | evidence: TC-041, desktop-screenshot skill uses no unbounded words.
- QD-S-2.2 | PASS | evidence: TC-041, desktop-screenshot skill uses no "until success" wording.
- QD-S-3.4 | PASS | evidence: TC-041, desktop-screenshot skill scopes the task (host PNGs on a per-developer branch for PR screenshots).
- QD-S-4.1 | PASS | evidence: TC-041, desktop-screenshot skill declares the fallback path (`scripts/post-screenshots.sh`).
- QD-S-1.2 | FAIL | evidence: TC-041, desktop-screenshot skill declares no output-size limit.
- QD-S-1.4 | FAIL | evidence: TC-041, desktop-screenshot skill captures and posts without a read/write/delete distinction.
- QD-S-1.5 | PASS | evidence: TC-041, desktop-screenshot skill declares its data source (the desktop app preview).
- QD-S-2.3 | PASS | evidence: TC-041, desktop-screenshot skill uses no open-ended enumeration.
- QD-S-2.4 | PASS | evidence: TC-041, desktop-screenshot verbs are specific (capture/post/build).
- QD-S-3.1 | PASS | evidence: TC-041, desktop-screenshot trigger is specific.
- QD-S-3.2 | PASS | evidence: TC-041, desktop-screenshot declares forbidden hosts ("NEVER use `buzz upload` ... or any third-party image host").
- QD-S-3.3 | FAIL | evidence: TC-041, desktop-screenshot skill declares no ambiguous-input handling.
- QD-S-3.6 | PASS | evidence: TC-041, desktop-screenshot name/description are consistent with the body.
- QD-S-4.2 | FAIL | evidence: TC-041, desktop-screenshot skill declares no partial-completion policy.
- QD-S-4.3 | FAIL | evidence: TC-041, desktop-screenshot skill declares no post-failure prohibited behaviours.
- QD-S-5.1 | FAIL | evidence: TC-041, desktop-screenshot skill performs writes/PR posts without distinguishing read/modify/delete.
- QD-S-5.3 | FAIL | evidence: TC-041, desktop-screenshot skill declares no environment boundary.
- QD-S-5.4 | FAIL | evidence: TC-041, desktop-screenshot skill invokes `scripts/post-screenshots.sh`/`just` without declaring permitted downstream scope.

### 3.A.3 Embedded code snippets (QC)

- QC-0.1 | PASS | evidence: TC-041, the `bash` snippets parse as valid syntax.
- QC-0.2 | PASS | evidence: TC-041, snippets are fenced with `bash`/`markdown`.
- QC-0.3 | PASS | evidence: TC-041, the `bash` snippets are complete commands.
- QC-1.1 | N/A | evidence: TC-041, no undefined name reference inside the shown snippets (determination basis: shell commands only).
- QC-1.2 | PASS | evidence: TC-041, no unavailable-module import statement present.
- QC-1.3 | PASS | evidence: TC-041, no deprecated API usage present.
- QC-1.4 | N/A | evidence: TC-041, no typed function call present (determination basis: shell commands only).
- QC-2.1 | N/A | evidence: TC-041, no file-handle pattern in the shown code (determination basis: no such pattern).
- QC-2.2 | N/A | evidence: TC-041, no connection constructor opened without close (determination basis: no such pattern).
- QC-2.3 | N/A | evidence: TC-041, no high-risk file/network/DB call in the shown snippets (determination basis: shell commands only).
- QC-3.1 | N/A | evidence: TC-041, no import statement present (determination basis: no such pattern).
- QC-3.2 | PASS | evidence: TC-041, no referenced-but-unimported name in the snippets.
- QC-3.3 | PASS | evidence: TC-041, no hardcoded demo credential value present.

---

## 4. Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Run condition met: two same-agent artifact types are present (System Prompt + Skill). No Tool Schema is present, so QD-PT / QD-ST are not applicable. Tier = **L3** (Appendix C upgrades applied: Agent L3 -> global P1->P0, P2->P1).

### QD-PS (Prompt -> Skill)

- QD-PS-1.1 Skill Authorization Consistency | PASS | evidence: Prompt (TC-041, AGENTS.md) does not restrict the skill set; no Skill is defined-but-unauthorized.
- QD-PS-1.2 Trigger Condition Consistency | FAIL (P0, upgraded from P1 by L3) | evidence: Prompt (TC-041, AGENTS.md) declares no skill triggers; Skill (desktop-screenshot) defines a trigger - inconsistent.
- QD-PS-1.3 Permission Boundary Consistency | FAIL (P0) | evidence: Prompt (TC-041) authorizes no explicit scope; Skill (desktop-screenshot pushes to a git branch and posts a PR comment) exceeds it.
- QD-PS-1.4 Resource Access Consistency | FAIL (P0, upgraded from P1 by L3) | evidence: Prompt (TC-041) declares no allowed resources; Skill (desktop-screenshot) declares GitHub branch/PR access.
- QD-PS-1.5 Failure Handling Consistency | FAIL (P0, upgraded from P1 by L3) | evidence: Prompt (TC-041) defines no failure handling; Skill (desktop-screenshot) leaves FAILURE undefined - inconsistent.
- QD-PS-1.6 Output Constraint Consistency | FAIL (P1, upgraded from P2 by L3) | evidence: Prompt (TC-041) declares no output constraints; Skill declares none either.
- QD-PT-2.x | Not Applicable | evidence: no Tool Schema present.
- QD-ST-3.x | Not Applicable | evidence: no Tool Schema present.

### QD-CYC (circular invocation)

- QD-CYC-1.1 Cross-Artifact Circular Invocation | PASS | evidence: Prompt/Skill invocation relationships (TC-041) show no closed loop.
- QD-CYC-1.2 Multi-Agent Circular Invocation | PASS | evidence: the AGENTS.md review flow is human-gated and one-directional (TC-041, "A human then tested it themselves"); no role cycle.

---

## 5. Stage C - Gate-0 (admission)

- G0-1 (no unfixed P0 in Stage A): NOT satisfied - recorded as an informational finding; does not gate this flow.
- G0-2 (no unfixed P0 in Stage B): NOT satisfied - recorded as an informational finding; does not gate this flow.
- G0-3 (responsibility boundary statements exist and are locatable): Passed - the AGENTS.md "Product Contract" and reviewing responsibilities are locatable.
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

Audit object: TC-041 System Prompt set + Skill.

Risk Item Summary:
- Total Risk Items: 0
- Explicit.P0 (Block release): 0 items
- Explicit.P1 (Fix / exemption): 0 items
- Explicit.P2 (Risk ledger): 0 items

No explicitly expressed risk text (NL-A / NL-B / NR-O / NR-S) was found in the shown artifacts. The "NEVER use `buzz upload` ... or any third-party image host" line is a protective constraint, not a risk expression.

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
| QD-P-2.4.2, QD-P-2.4.3 | AS-05, AS-07, AS-09 | FM-03, FM-04, FM-05 | Strong |
| QD-P-2.5.1, QD-P-2.5.5, QD-P-2.6.1, QD-P-2.6.2, QD-P-2.7.1, QD-P-2.7.2, QD-P-2.7.3 | AS-06, AS-07 | FM-08, FM-09, FM-10 | Conditional |
| QD-S-1.1, QD-S-1.2, QD-S-1.3 (desktop-screenshot) | AS-06 | Availability | Medium |
| QD-S-1.4, QD-S-5.1 (desktop-screenshot) | AS-04, AS-05 | FM-05, FM-09 | Strong (write without scope distinction) |
| QD-S-3.3, QD-S-4.2, QD-S-4.3, QD-S-5.3, QD-S-5.4 (desktop-screenshot) | AS-01, AS-04, AS-05, AS-07 | FM-02, FM-05, FM-07, FM-09 | Medium |
| QD-PS-1.2, QD-PS-1.3, QD-PS-1.4, QD-PS-1.5, QD-PS-1.6 | AS-03, AS-04, AS-09 | FM-04, FM-05, FM-06, FM-08 | Medium |

Candidate RAG-Agent quality metrics (candidate associations only; NOT a quality result): Correctness, Completeness, Robustness, Boundary Recognition, Safety Response. Defect chains (SC-*/QC-TA-*/QC-RA-*) are out of scope for lite v1.

---

## 9. Status board

Stage A (Single-artifact):  Executed - QD-P (L3), QD-S (desktop-screenshot L2), QC.
Stage B (Cross):            Executed - two same-agent artifact types present (Prompt + Skill); QD-PT/QD-ST not applicable.
Stage C (Gate-0):           Not passed - G0-4 (G0-1/G0-2 informational).
Stage D (Permission QD-PM): Not Executed - incomplete artifact set (no Tool Schema; Gate-0 G0-4 not satisfied).
Stage E (Risk Explicit EX): Executed - 0 findings.
Stage F (Impact outlook):   Executed - candidate mapping for all Stage A/B FAILs.
Stage G (Self-verification): Executed - ID back-closure, red-line wording, output contract checked.

---

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. No in-place self-corrections were required.
