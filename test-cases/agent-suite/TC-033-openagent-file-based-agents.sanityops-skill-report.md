# SanityOps Inspect Lite Report

Host model: unspecified (host model self-declaration not available in this environment)
Skill package: sanityops-inspect-lite v1.0.0
Specification baseline: SanityOps Framework v1.0 (September 2026)
Non-official-result statement: This result is produced by the skill rule package applied by the host model; it is NOT a conclusion of the official SanityOps engine. For a full inspection use sanityops-cli.
Inspection date: 2026-10-14
Artifact version: not supplied by the user (using the case's Collection Date as the working label)

---

## 1. Executive summary (Sec. 6.1)

- Stages executed: A (single-artifact), B (cross-artifact), C (Gate-0), E (Risk Explicit), F (impact outlook), G (self-verification). Stage D did not run (Gate-0 G0-4 not satisfied).
- Finding counts (Stage A + B): Inspect P0 = 62, P1 = 37, P2 = 0.
- Gate-0 result: Not passed (G0-3 passed; G0-4 not satisfied - the MCP Tool Schema set exposes Go helper functions, not tool name/description/parameter schemas).
- Risk-Explicit summary (Stage E): Explicit.P0 = 1, Explicit.P1 = 0, Explicit.P2 = 1.
- Top findings (rule ID - one-line defect):
  1. QD-S-5.2 / QD-S-5.1 - The obsidian Skill exposes `obsidian-cli delete` with no confirmation and no read/write/delete distinction.
  2. QD-P-2.5.2 / QD-P-2.5.3 - The Prompt (CLAUDE.md / README.md) declares no security boundaries or permission scopes for shell/browser/MCP capabilities.
  3. QD-PT-2.1 - The Prompt references capabilities (shell, browser-use, MCP, office) that are absent from the provided Tool Schema list.
  4. QD-ST-3.1 - The github Skill invokes `gh` / `git` tools that are absent from the known Tool Schema list.
  5. QD-S-1.3 (obsidian / coding-agent) - Tool-invoking Skills declare no retry/timeout/tool-call bound.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The lite embedded-code QC was run in Stage A.
- This report never states a security or quality conclusion; Inspect PASS is not Risk PASS and not Quality PASS.
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and version-level evidence chains, use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

---

## 2. Artifact inventory (input preparation, not a stage)

Case TC-033 is a single Agent suite (OpenAgent). All artifacts belong to the same agent. Types present, by structural signature:

- System Prompt (present): CLAUDE.md (development guidance / repository instructions) and README.md overview. Basis: prose/markdown instructions.
- Skill (present, 5): github, coding-agent, notion, weather, obsidian (markdown with `name`/`description` front matter). Basis: front-matter signature.
- Tool Schema (present, partial): MCP Tools (Go) - `GetToolsFromURL` / `GetToolsFromConfig`. Basis: function/command definitions that produce and consume tool lists; the case shows no JSON `parameters` schema.
- Out of coverage: the Go backend, React frontend and the remaining ~49 skills are not quoted; only the shown text is inspected.

---

## 3. Stage A - Single-artifact inspection

### 3.A.1 System Prompt set (CLAUDE.md + README.md)

Tier determination: **L3 Complex Agent**. Basis: 4+ tool invocations (shell execution, browser-use, web search, office automation, MCP); complex multi-surface workflow; security-sensitive (shell + desktop-class operations). Scope = L3 (47 items).

- QD-P-1.1.1 | PASS | evidence: TC-033, CLAUDE.md and README.md directives are mutually consistent.
- QD-P-1.1.2 | PASS | evidence: TC-033, no conflicting priority directives found.
- QD-P-1.1.3 | PASS | evidence: TC-033, no example contradicting a rule.
- QD-P-1.2.1 | PASS | evidence: TC-033, "provide guidance to Claude Code ... when working with code" matches the directives.
- QD-P-1.2.2 | PASS | evidence: TC-033, the guide's voice matches a repository-guidance role.
- QD-P-1.2.3 | PASS | evidence: TC-033, no constraint prohibits a declared responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-033, no quantifier-scope misuse found.
- QD-P-1.3.2 | PASS | evidence: TC-033, no vague qualifier carries a critical decision.
- QD-P-1.3.3 | FAIL | evidence: TC-033, README.md / CLAUDE.md declare no authorization scope, prohibition scope, or handoff conditions.
- QD-P-1.4.1 | PASS | evidence: TC-033, no duplicate constraint found.
- QD-P-1.4.2 | PASS | evidence: TC-033, declared branches are reachable.
- QD-P-1.4.3 | PASS | evidence: TC-033, no Skill definition is given in the Prompt (vacuous).
- QD-P-1.5.1 | PASS | evidence: TC-033, declared behavior supports the personal-assistant objective.
- QD-P-1.5.2 | FAIL | evidence: TC-033, README lists shell execution / browser-use / MCP capabilities but the Prompt defines no corresponding resources.
- QD-P-1.6.1 | PASS | evidence: TC-033, no vague word carries a security/permission decision.
- QD-P-1.6.2 | PASS | evidence: TC-033, no rule keys on unobservable model internal state.
- QD-P-1.6.3 | PASS | evidence: TC-033, no unresolved implicit Soft-Rule conflict found.
- QD-P-1.6.4 | PASS | evidence: TC-033, no internal reasoning-method constraint found.
- QD-P-1.6.5 | PASS | evidence: TC-033, no self-referential/recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-033, no unstated-assumption dependency found beyond normal environment assumptions.
- QD-P-1.6.7 | PASS | evidence: TC-033, no rule requires revising earlier conclusions on new information.
- QD-P-2.1.1 | PASS | evidence: TC-033, prompt formatting is readable.
- QD-P-2.1.2 | PASS | evidence: TC-033, references (file paths, commands) are specific.
- QD-P-2.1.3 | PASS | evidence: TC-033, heading hierarchy is reasonable.
- QD-P-2.1.4 | PASS | evidence: TC-033, prose is concise.
- QD-P-2.2.1 | FAIL | evidence: TC-033, no input source (user / system / external data) is declared for the agent.
- QD-P-2.2.2 | PASS | evidence: TC-033, input is conversational (no structured parser defined).
- QD-P-2.2.3 | PASS | evidence: TC-033, no parameterized input declared (not triggered).
- QD-P-2.2.4 | FAIL | evidence: TC-033, no missing-input handling is declared.
- QD-P-2.3.1 | FAIL | evidence: TC-033, no output format is declared.
- QD-P-2.3.2 | FAIL | evidence: TC-033, no output schema/fields are declared.
- QD-P-2.3.3 | FAIL | evidence: TC-033, no output stability/consistency assurance is declared.
- QD-P-2.3.4 | FAIL | evidence: TC-033, no sensitive-data filtering or privacy handling is declared.
- QD-P-2.4.1 | FAIL | evidence: TC-033, no command/workflow step sequence is defined for the agent loop.
- QD-P-2.4.2 | FAIL | evidence: TC-033, the shell/browser/MCP capabilities are named but not declared as resources.
- QD-P-2.4.3 | FAIL | evidence: TC-033, no tool invocation parameters, sequence, or failure handling are defined.
- QD-P-2.5.1 | FAIL | evidence: TC-033, no loop/recursion termination conditions are declared.
- QD-P-2.5.2 | FAIL | evidence: TC-033, no prohibited operations or access boundaries are declared.
- QD-P-2.5.3 | FAIL | evidence: TC-033, no permission scope is declared for shell/browser/MCP capabilities.
- QD-P-2.5.4 | PASS | evidence: TC-033, no conflicting soft constraints requiring priority arbitration found.
- QD-P-2.5.5 | FAIL | evidence: TC-033, no resource invocation frequency limits are declared.
- QD-P-2.6.1 | FAIL | evidence: TC-033, no runtime exception handling is declared.
- QD-P-2.6.2 | FAIL | evidence: TC-033, no degradation/recovery strategy is declared.
- QD-P-2.6.3 | PASS | evidence: TC-033, no unreasonable retry mechanism found.
- QD-P-2.7.1 | FAIL | evidence: TC-033, no positive examples are provided.
- QD-P-2.7.2 | FAIL | evidence: TC-033, no counter-examples are provided.
- QD-P-2.7.3 | FAIL | evidence: TC-033, no boundary-case examples are provided.

### 3.A.2 Skills

Skill risk-level determination: github = **L2** (external repository writes; recoverable); coding-agent = **L2** (spawns coding CLIs that modify a worktree; recoverable via VCS); notion = **L2** (external API write access); weather = **L1** (read-only curl); obsidian = **L3** (declares `obsidian-cli delete`, an irreversible file operation).

QD-S-0 baseline (all five skills): QD-S-0.1 PASS (`name`/`description` present in each); QD-S-0.2 PASS (non-empty); QD-S-0.3 PASS (YAML front matter parses); QD-S-0.4 PASS (field types valid); QD-S-0.5 PASS (no conflicting declarations); QD-S-0.6 PASS (minimum structure present). Baseline passes; proceed.

#### Skill: weather (L1; scope = the 6 mandatory items)

- QD-S-1.1 | FAIL | evidence: TC-033, weather skill declares no input-size/number limit.
- QD-S-1.2 | FAIL | evidence: TC-033, weather skill declares no output-size limit.
- QD-S-2.1 | PASS | evidence: TC-033, weather skill uses no unbounded words.
- QD-S-3.4 | FAIL | evidence: TC-033, weather skill declares no `non_goals` field.
- QD-S-4.1 | FAIL | evidence: TC-033, weather skill declares no failure behavior.
- QD-S-3.6 | PASS | evidence: TC-033, weather name/description are consistent with the body.

#### Skill: github (L2; scope = 6 mandatory + 14 recommended)

- QD-S-1.1 | FAIL | evidence: TC-033, github skill declares no input-size limit.
- QD-S-1.3 | FAIL | evidence: TC-033, github skill invokes `gh`/`git` with no retry, tool-call, or timeout bound.
- QD-S-2.1 | PASS | evidence: TC-033, github skill uses no unbounded words.
- QD-S-2.2 | PASS | evidence: TC-033, github skill uses no "until success" wording.
- QD-S-3.4 | FAIL | evidence: TC-033, github skill declares no `non_goals`.
- QD-S-4.1 | PASS | evidence: TC-033, github skill declares a credential fallback ladder ("If `gh` is still unavailable, fall back to Git").
- QD-S-1.2 | FAIL | evidence: TC-033, github skill declares no output-size limit.
- QD-S-1.4 | FAIL | evidence: TC-033, github skill creates repos/pushes without a read/write/delete distinction.
- QD-S-1.5 | PASS | evidence: TC-033, github skill declares its data source (GitHub via `gh`/git remotes).
- QD-S-2.3 | PASS | evidence: TC-033, github skill uses no open-ended enumeration.
- QD-S-2.4 | PASS | evidence: TC-033, github skill verbs are specific (detect/push/create/install).
- QD-S-3.1 | PASS | evidence: TC-033, github trigger is specific.
- QD-S-3.2 | FAIL | evidence: TC-033, github skill declares no deactivation conditions.
- QD-S-3.3 | FAIL | evidence: TC-033, github skill declares no ambiguous-input handling.
- QD-S-3.6 | PASS | evidence: TC-033, github name/description are consistent with the body.
- QD-S-4.2 | FAIL | evidence: TC-033, github skill declares no partial-completion policy.
- QD-S-4.3 | FAIL | evidence: TC-033, github skill declares no post-failure prohibited behaviors.
- QD-S-5.1 | FAIL | evidence: TC-033, github skill performs repo writes without distinguishing read/modify/delete.
- QD-S-5.3 | FAIL | evidence: TC-033, github skill declares no environment boundary.
- QD-S-5.4 | FAIL | evidence: TC-033, github skill invokes `gh`/`git` without declaring permitted downstream scope.

#### Skill: coding-agent (L2; scope = 6 mandatory + 14 recommended)

- QD-S-1.1 | FAIL | evidence: TC-033, coding-agent skill declares no input-size limit.
- QD-S-1.3 | FAIL | evidence: TC-033, coding-agent skill starts background processes with no retry/timeout/tool-call bound.
- QD-S-2.1 | PASS | evidence: TC-033, coding-agent skill uses no unbounded words.
- QD-S-2.2 | PASS | evidence: TC-033, coding-agent skill uses no "until success" wording.
- QD-S-3.4 | PASS | evidence: TC-033, coding-agent description declares "NOT for: simple one-liner fixes".
- QD-S-4.1 | FAIL | evidence: TC-033, coding-agent skill declares no failure behavior for a failed coding run.
- QD-S-1.2 | FAIL | evidence: TC-033, coding-agent skill declares no output-size limit.
- QD-S-1.4 | FAIL | evidence: TC-033, coding-agent skill requests `--permission-mode bypassPermissions` with no permission-type distinction.
- QD-S-1.5 | PASS | evidence: TC-033, coding-agent skill declares its data source (the target worktree/repo).
- QD-S-2.3 | PASS | evidence: TC-033, coding-agent skill uses no open-ended enumeration.
- QD-S-2.4 | PASS | evidence: TC-033, coding-agent skill verbs are specific (build/review/refactor).
- QD-S-3.1 | PASS | evidence: TC-033, coding-agent trigger is specific.
- QD-S-3.2 | PASS | evidence: TC-033, coding-agent description declares deactivation ("NOT for ...").
- QD-S-3.3 | FAIL | evidence: TC-033, coding-agent skill declares no ambiguous-input handling.
- QD-S-3.6 | PASS | evidence: TC-033, coding-agent name/description are consistent with the body.
- QD-S-4.2 | FAIL | evidence: TC-033, coding-agent skill declares no partial-completion policy.
- QD-S-4.3 | FAIL | evidence: TC-033, coding-agent skill declares no post-failure prohibited behaviors.
- QD-S-5.1 | FAIL | evidence: TC-033, coding-agent skill modifies code without distinguishing read/modify/delete.
- QD-S-5.3 | FAIL | evidence: TC-033, coding-agent skill declares no environment boundary.
- QD-S-5.4 | FAIL | evidence: TC-033, coding-agent skill spawns `claude`/`codex` sub-agents without declaring permitted downstream scope.

#### Skill: notion (L2; scope = 6 mandatory + 14 recommended)

- QD-S-1.1 | FAIL | evidence: TC-033, notion skill declares no input-size limit.
- QD-S-1.3 | FAIL | evidence: TC-033, notion skill invokes `curl` with no retry/timeout bound.
- QD-S-2.1 | PASS | evidence: TC-033, notion skill uses no unbounded words.
- QD-S-2.2 | PASS | evidence: TC-033, notion skill uses no "until success" wording.
- QD-S-3.4 | FAIL | evidence: TC-033, notion skill declares no `non_goals`.
- QD-S-4.1 | FAIL | evidence: TC-033, notion skill declares no failure behavior.
- QD-S-1.2 | FAIL | evidence: TC-033, notion skill declares no output-size limit.
- QD-S-1.4 | FAIL | evidence: TC-033, notion skill creates/updates pages without a read/write/delete distinction.
- QD-S-1.5 | PASS | evidence: TC-033, notion skill declares its data source (the Notion API).
- QD-S-2.3 | PASS | evidence: TC-033, notion skill uses no open-ended enumeration.
- QD-S-2.4 | PASS | evidence: TC-033, notion skill verbs are specific (search/create/query).
- QD-S-3.1 | PASS | evidence: TC-033, notion trigger is specific.
- QD-S-3.2 | FAIL | evidence: TC-033, notion skill declares no deactivation conditions.
- QD-S-3.3 | FAIL | evidence: TC-033, notion skill declares no ambiguous-input handling.
- QD-S-3.6 | PASS | evidence: TC-033, notion name/description are consistent with the body.
- QD-S-4.2 | FAIL | evidence: TC-033, notion skill declares no partial-completion policy.
- QD-S-4.3 | FAIL | evidence: TC-033, notion skill declares no post-failure prohibited behaviors.
- QD-S-5.1 | FAIL | evidence: TC-033, notion skill performs writes without distinguishing read/modify/delete.
- QD-S-5.3 | FAIL | evidence: TC-033, notion skill declares no environment boundary.
- QD-S-5.4 | FAIL | evidence: TC-033, notion skill invokes the Notion API without declaring permitted downstream scope.

#### Skill: obsidian (L3; scope = 21 mandatory items)

- QD-S-1.1 | FAIL | evidence: TC-033, obsidian skill declares no input-size limit.
- QD-S-1.2 | FAIL | evidence: TC-033, obsidian skill declares no output-size limit.
- QD-S-1.3 | FAIL | evidence: TC-033, obsidian skill uses `obsidian-cli` with no retry/timeout/tool-call bound.
- QD-S-1.4 | FAIL | evidence: TC-033, obsidian skill creates/moves/deletes notes without a permission-type distinction.
- QD-S-1.5 | PASS | evidence: TC-033, obsidian skill declares its data source (the resolved Obsidian vault).
- QD-S-2.1 | PASS | evidence: TC-033, obsidian skill uses no unbounded words.
- QD-S-2.2 | PASS | evidence: TC-033, obsidian skill uses no "until success" wording.
- QD-S-2.3 | PASS | evidence: TC-033, obsidian skill uses no open-ended enumeration.
- QD-S-2.4 | PASS | evidence: TC-033, obsidian skill verbs are specific (search/create/move/delete).
- QD-S-3.1 | PASS | evidence: TC-033, obsidian trigger is specific.
- QD-S-3.2 | FAIL | evidence: TC-033, obsidian skill declares no deactivation conditions.
- QD-S-3.4 | FAIL | evidence: TC-033, obsidian skill declares no `non_goals`.
- QD-S-3.5 | PASS | evidence: TC-033, obsidian skill declares a default when no vault is set ("read ... the vault entry with `open: true`").
- QD-S-3.6 | PASS | evidence: TC-033, obsidian name/description are consistent with the body.
- QD-S-4.1 | FAIL | evidence: TC-033, obsidian skill declares no failure behavior.
- QD-S-4.2 | FAIL | evidence: TC-033, obsidian skill declares no partial-completion policy.
- QD-S-4.3 | FAIL | evidence: TC-033, obsidian skill declares no post-failure prohibited behaviors.
- QD-S-5.1 | FAIL | evidence: TC-033, obsidian skill performs writes/deletes without distinguishing scopes.
- QD-S-5.2 | FAIL | evidence: TC-033, obsidian skill runs `obsidian-cli delete "path/note"` with no confirmation mechanism.
- QD-S-5.3 | FAIL | evidence: TC-033, obsidian skill declares no environment boundary.
- QD-S-5.4 | FAIL | evidence: TC-033, obsidian skill invokes `obsidian-cli` without declaring permitted downstream scope.

### 3.A.3 Tool Schema - MCP Tools (Go)

Tier: **L2** (external MCP connection with a bearer token; reachable tools may change state and are recoverable). Scope = L2 (12 items).

- QD-T-1.1 | FAIL | evidence: TC-033, `GetToolsFromURL`/`GetToolsFromConfig` are Go functions with no tool `name`/`description`/`inputSchema`.
- QD-T-1.2 | FAIL | evidence: TC-033, no `properties`/`required` field is declared.
- QD-T-1.3 | PASS | evidence: TC-033, no `enum` with duplicate/empty values is present.
- QD-T-1.4 | FAIL | evidence: TC-033, no `additionalProperties: false` declaration is present.
- QD-T-2.1 | FAIL | evidence: TC-033, `url` and `token` string parameters have no length constraint.
- QD-T-2.2 | FAIL | evidence: TC-033, the `url` parameter requires a URL format but declares no `format`/`pattern`.
- QD-T-2.3 | N/A | evidence: TC-033, no number-type parameter is declared (determination basis: no such field).
- QD-T-2.4 | N/A | evidence: TC-033, no array-type parameter is declared (determination basis: no such field).
- QD-T-3.1 | FAIL | evidence: TC-033, downstream tools reachable via the connection may modify data; no write-operation notice is stated.
- QD-T-3.2 | FAIL | evidence: TC-033, `GetToolsFromURL(url, token string)` accepts raw `url`/`token` input for direct backend use.
- QD-T-4.1 | PASS | evidence: TC-033, the doc comment "connects to an HTTP-based MCP server and returns its tool list" is specific.
- QD-T-4.2 | FAIL | evidence: TC-033, the side effect of opening an authenticated external connection is not declared.

### 3.A.4 Embedded code snippets (QC)

- QC-0.1 | PASS | evidence: TC-033, the bash/Go/YAML snippets parse as valid syntax.
- QC-0.2 | PASS | evidence: TC-033, snippets are fenced with `bash`/`go`/`markdown`/`yaml`.
- QC-0.3 | FAIL | evidence: TC-033, the Go snippet references `createClient`, `ServerConfig`, `describeServerConfig` with no definitions shown.
- QC-1.1 | FAIL | evidence: TC-033, `createClient`/`describeServerConfig` are undefined in the snippet.
- QC-1.2 | PASS | evidence: TC-033, imports (`context`, `fmt`, `time`, go-mcp packages) are declared.
- QC-1.3 | PASS | evidence: TC-033, no deprecated API usage present.
- QC-1.4 | PASS | evidence: TC-033, no type-mismatched call present.
- QC-2.1 | N/A | evidence: TC-033, no file-handle pattern in the shown code (determination basis: no such pattern).
- QC-2.2 | N/A | evidence: TC-033, no connection constructor opened without close (determination basis: `cli.Close()` is deferred).
- QC-2.3 | N/A | evidence: TC-033, no high-risk file/network/DB call without handling (determination basis: errors are wrapped).
- QC-3.1 | PASS | evidence: TC-033, no unused import present.
- QC-3.2 | FAIL | evidence: TC-033, `createClient`/`describeServerConfig` are referenced but never defined/imported.
- QC-3.3 | PASS | evidence: TC-033, the `ntn_your_key_here` value is an obvious placeholder, not a weak credential (determination basis: placeholder pattern).

---

## 4. Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Run condition met: all three same-agent artifact types are present (System Prompt + Skill + Tool Schema). Tier = **L3** (Appendix C upgrades applied: Agent L3 -> global P1->P0, P2->P1).

### QD-PS (Prompt -> Skill)

- QD-PS-1.1 Skill Authorization Consistency | PASS | evidence: Prompt (TC-033, README.md "54 skills") does not restrict the skill set; no Skill is defined-but-unauthorized.
- QD-PS-1.2 Trigger Condition Consistency | FAIL (P0, upgraded from P1 by L3) | evidence: Prompt (TC-033, CLAUDE.md) declares no skill triggers; Skill (github/notion SKILL.md) defines workflow triggers - inconsistent.
- QD-PS-1.3 Permission Boundary Consistency | FAIL (P0) | evidence: Prompt (TC-033, README.md) authorizes no explicit scope; Skill (obsidian SKILL.md "obsidian-cli delete") exceeds it.
- QD-PS-1.4 Resource Access Consistency | FAIL (P0, upgraded from P1 by L3) | evidence: Prompt (TC-033, CLAUDE.md) declares no allowed resources; Skill (notion/github SKILL.md) declares external system access.
- QD-PS-1.5 Failure Handling Consistency | FAIL (P0, upgraded from P1 by L3) | evidence: Prompt (TC-033) defines no failure handling; Skills (obsidian/notion SKILL.md) leave FAILURE undeclared - inconsistent.
- QD-PS-1.6 Output Constraint Consistency | FAIL (P1, upgraded from P2 by L3) | evidence: Prompt (TC-033) declares no output constraints; Skills (weather/github SKILL.md) declare none either.

### QD-PT (Prompt -> Tool)

- QD-PT-2.1 Tool Existence | FAIL (P0) | evidence: Prompt (TC-033, README.md "Shell Execution", "Browser-Use", "MCP Integration") references capabilities absent from the Tool Schema list (`GetToolsFromURL`/`GetToolsFromConfig`).
- QD-PT-2.2 Invocation Specification Consistency | FAIL (P0) | evidence: Prompt (TC-033) names capabilities without parameters; Tool Schema (Go helper funcs) defines `url`/`token` fields - inconsistent.
- QD-PT-2.3 Parameter Constraint Consistency | FAIL (P0, upgraded from P1 by L3) | evidence: Prompt (TC-033) declares no parameter constraints; Tool Schema (`GetToolsFromURL(url, token string)`) constrains two parameters.
- QD-PT-2.4 Permission Granularity Consistency | N/A | evidence: no RS-3 (high-risk) Tool among the provided Tool Schema (determination basis: the MCP helper is L2).
- QD-PT-2.5 Error Handling Completeness | FAIL (P0, upgraded from P1 by L3) | evidence: Prompt (TC-033) covers no tool error types; Tool Schema defines only Go `error` returns.
- QD-PT-2.6 Invocation Frequency Reasonableness | FAIL (P1, upgraded from P2 by L3) | evidence: Prompt declares no frequency limits; Tool Schema declares only a 30s context timeout.

### QD-ST (Skill <-> Tool)

- QD-ST-3.1 Tool Existence | FAIL (P0) | evidence: Skill (github SKILL.md "Prefer `gh` over raw GitHub API calls") vs known Tool Schema list (MCP helpers) - the `gh`/`git` tools do not exist there.
- QD-ST-3.2 Input Constraint Consistency | FAIL (P0) | evidence: Skill (obsidian SKILL.md vault path input) declares no input constraint matched by a Tool Schema (no file-tool schema present).
- QD-ST-3.3 Required Parameter Preparation | FAIL (P0) | evidence: Skill (notion SKILL.md requires `NOTION_API_KEY`) has no matching Tool Schema declaring the required parameter source.
- QD-ST-3.4 Invocation Frequency Match | FAIL (P1, upgraded from P2 by L3) | evidence: Skill (github/coding-agent SKILL.md) declares no max call count; no matching Tool capability bound.
- QD-ST-3.5 Output Structure Match | FAIL (P0, upgraded from P1 by L3) | evidence: Skill (coding-agent SKILL.md output from background CLI) declares no output structure matched by a Tool return value.
- QD-ST-3.6 Permission Scope Match | FAIL (P0) | evidence: Skill (obsidian SKILL.md delete side effect) exceeds the Skill's permission declarations (absent).
- QD-ST-3.7 Error Handling Coverage | FAIL (P0, upgraded from P1 by L3) | evidence: Skill (notion/obsidian SKILL.md) FAILURE dimension is undeclared, so tool error types are not covered.

### QD-CYC (circular invocation)

- QD-CYC-1.1 Cross-Artifact Circular Invocation | PASS | evidence: Prompt/Skill/Tool invocation relationships (TC-033) show no closed loop.
- QD-CYC-1.2 Multi-Agent Circular Invocation | PASS | evidence: coding-agent spawns external CLIs one-directionally (TC-033, "Delegate coding tasks to Codex, Claude Code, or Pi agents"); no role cycle.

---

## 5. Stage C - Gate-0 (admission)

- G0-1 (no unfixed P0 in Stage A): NOT satisfied - recorded as an informational finding; does not gate this flow.
- G0-2 (no unfixed P0 in Stage B): NOT satisfied - recorded as an informational finding; does not gate this flow.
- G0-3 (responsibility boundary statements exist and are locatable): Passed - README.md "Next-generation personal AI assistant" and CLAUDE.md conventions are locatable.
- G0-4 (each Tool Schema's `name`, `description`, parameter descriptions complete): NOT passed - the MCP Tool Schema exposes Go helper functions, not tool name/description/parameter schemas.

Gate-0 result: **Not passed - G0-4**.

---

## 6. Stage D - Permission (QD-PM Quick Mode)

Subset: Inspect Permission Governance Specification (QD-PM)
Execution Status: Not Executed
Unsatisfied Conditions: G0-4
Blocking Reasons:
  G0-4 - Tool Schema `name`/`description`/parameter descriptions are not complete (the MCP helper set exposes no tool schema with parameter descriptions).
Remediation Actions: Fix the above upstream items, then re-run Gate-0.

(This is not a FAIL and not a permission conclusion.)

---

## 7. Stage E - Risk Explicit audit (EX) - physically separated from Inspect verdicts

Audit object: TC-033 System Prompt set + Skills + Tool Schema.
Three-phase scan (NL-A -> NL-B -> NR-O -> NR-S) run over the bundled artifacts.

Risk Item Summary:
- Total Risk Items: 2
- Explicit.P0 (Block release): 1 items
- Explicit.P1 (Fix / exemption): 0 items
- Explicit.P2 (Risk ledger): 1 items

Risk Item Details:

[Risk Item 1]
- EX Classification: NL-A-7
- Risk Expression: "claude --permission-mode bypassPermissions --print" and "codex --yolo" (TC-033, coding-agent SKILL.md, The Pattern section)
- Severity Grade: Explicit.P0
- Reason: The skill explicitly instructs launching a coding CLI with permission checks bypassed; security restrictions are completely bypassed, matching P0.
- Impact Type Labels: D3
- Trigger Condition Label: unconditional
- Disposition: Block release
- Remediation Suggestion: Remove the bypass instruction (replace with the CLI's default permission mode and an explicit approval flow)

[Risk Item 2]
- EX Classification: NR-S-9
- Risk Expression: "echo \"ntn_your_key_here\" > ~/.config/notion/api_key" (TC-033, notion SKILL.md, Setup step 3)
- Severity Grade: Explicit.P2
- Reason: A credential-shaped placeholder value is hardcoded in the artifact text; placeholder/demo values are rated P2.
- Impact Type Labels: D1
- Trigger Condition Label: unconditional
- Disposition: Record in risk ledger
- Remediation Suggestion: Replace with a placeholder-only pattern, e.g. `NOTION_API_KEY=<your-token>`

Note: This is a static-document risk scan of explicitly declared text only; it is not a confirmed exploit and not a security conclusion. Risk Implicit (dynamic exploitability) was NOT run.

---

## 8. Stage F - Impact outlook (candidate mapping, advisory only)

Advisory context only; it does not change, soften, or escalate any Inspect conclusion. Strength is association confidence, NOT severity. Candidate language only. Risk Implicit and the runtime Quality subsets were NOT run; the lite embedded-code QC ran in Stage A. Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent.

| Defect (FAIL) | Candidate attack surface (AS-*) | Candidate failure modes (FM-*) | Strength (provisional, lite) |
|---|---|---|---|
| QD-P-1.3.3, QD-P-2.2.1 | AS-01, AS-04 | FM-01, FM-02, FM-07, FM-09 | Medium |
| QD-P-1.5.2, QD-P-2.4.2 | AS-05, AS-07, AS-09 | FM-03, FM-04, FM-05 | Strong (referenced capabilities undeclared) |
| QD-P-2.2.4, QD-P-2.5.1, QD-P-2.5.5 | AS-06, AS-07 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.3.1, QD-P-2.3.2, QD-P-2.3.3 | AS-03, AS-09 | FM-06 | Conditional |
| QD-P-2.3.4 | AS-03 | FM-06 | Conditional |
| QD-P-2.4.3, QD-P-2.5.2, QD-P-2.5.3 | AS-01, AS-04, AS-05 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.6.1, QD-P-2.6.2 | AS-07 | FM-08, FM-10 | Medium |
| QD-P-2.7.1, QD-P-2.7.2, QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |
| QD-S-1.1, QD-S-1.2, QD-S-1.3 (skills) | AS-06 | Availability | Medium |
| QD-S-1.4, QD-S-5.1 (skills) | AS-04, AS-05 | FM-05, FM-09 | Strong (write without permission scope) |
| QD-S-5.2 (obsidian) | AS-05 | FM-05, FM-09 | Strong (unconfirmed delete) |
| QD-S-3.2, QD-S-3.3, QD-S-3.4 (skills) | AS-01, AS-05 | FM-02, FM-07, FM-09 | Medium |
| QD-S-4.1, QD-S-4.2, QD-S-4.3 (skills) | AS-07 | FM-08, FM-09 | Medium |
| QD-S-5.3, QD-S-5.4 (skills) | AS-04, AS-05, AS-07 | FM-05, FM-09 | Strong |
| QD-T-1.1, QD-T-1.2, QD-T-1.4 | AS-05, AS-09 | FM-03, FM-04, FM-05 | Strong |
| QD-T-2.1, QD-T-2.2, QD-T-3.1, QD-T-4.2 | AS-02, AS-06 | FM-03, FM-04, FM-05 | Medium |
| QD-T-3.2 | AS-02 | FM-04, FM-05, FM-06 | Strong (raw url/token passthrough) |
| QC-0.3, QC-1.1, QC-3.2 | (no AS-* row in Appendix A; snippet-level only) | (no B.1 group) | Not Applicable (out of Appendix A mapping scope) |
| QD-PS-1.2, QD-PS-1.3, QD-PS-1.4, QD-PS-1.5, QD-PS-1.6 | AS-03, AS-04, AS-09 | FM-04, FM-05, FM-06, FM-08 | Medium |
| QD-PT-2.1, QD-PT-2.2, QD-PT-2.3 | AS-02, AS-05, AS-09 | FM-04, FM-05, FM-06, FM-08 | Strong |
| QD-PT-2.5, QD-PT-2.6 | AS-06, AS-07 | FM-04, FM-05, FM-06, FM-08 | Medium |
| QD-ST-3.1, QD-ST-3.2, QD-ST-3.3 | AS-02, AS-09 | FM-04, FM-05, FM-06, FM-08 | Strong |
| QD-ST-3.4, QD-ST-3.5, QD-ST-3.6, QD-ST-3.7 | AS-04, AS-05, AS-09 | FM-04, FM-05, FM-06, FM-08 | Medium |

Candidate RAG-Agent quality metrics (candidate associations only; NOT a quality result): Correctness, Completeness, Robustness, Boundary Recognition, Safety Response, Traceability. Defect chains (SC-*/QC-TA-*/QC-RA-*) are out of scope for lite v1.

---

## 9. Status board

Stage A (Single-artifact):  Executed - QD-P (L3), QD-S (weather L1; github/notion/coding-agent L2; obsidian L3), QD-T (MCP L2), QC.
Stage B (Cross):            Executed - all three same-agent artifact types present.
Stage C (Gate-0):           Not passed - G0-4 (G0-1/G0-2 informational).
Stage D (Permission QD-PM): Not Executed - Gate-0 G0-4 not satisfied.
Stage E (Risk Explicit EX): Executed - 2 findings (Explicit.P0 = 1, Explicit.P2 = 1).
Stage F (Impact outlook):   Executed - candidate mapping for all Stage A/B FAILs.
Stage G (Self-verification): Executed - ID back-closure, red-line wording, output contract checked.

---

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. No in-place self-corrections were required.
