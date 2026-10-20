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
- Finding counts (Stage A): System Prompt set (L3) Inspect P0 = 10, P1 = 1, P2 = 0; Tool Schema set (L1) P0 = 0, P1 = 0, P2 = 2. Stage A total P0 = 10, P1 = 1, P2 = 2.
- Gate-0 result: Not passed (G0-3 passed; G0-4 not satisfied - the quoted Tool Schemas carry names and docstrings but no parameter descriptions for the full set, and several tools are shown name-only).
- Risk-Explicit summary (Stage E): Explicit.P0 = 0, Explicit.P1 = 0, Explicit.P2 = 0.
- Top findings (rule ID - one-line defect):
  1. QD-P-2.5.2 / QD-P-2.5.3 - No security boundary or permission-control boundary is declared in any role prompt.
  2. QD-P-2.3.4 - No sensitive-data filtering or privacy output constraint is declared.
  3. QD-P-2.2.2 / QD-P-2.2.3 - The injected reports/context carry no declared format, and no input is marked required or optional.
  4. QD-P-2.4.3 - The prompts name tools but declare no invocation parameter specification.
  5. QD-P-2.7.1 / QD-P-2.7.2 / QD-P-2.7.3 - No positive, counter, or boundary-case example is provided.
- NOT run: Risk Implicit (dynamic exploitability) and the runtime Quality subsets. The lite embedded-code QC was run in Stage A.
- This report never states a security or quality conclusion; Inspect PASS is not Risk PASS and not Quality PASS.
- Upgrade pointer: for the full ruleset plus Risk (Explicit/Implicit), Quality, remediation and version-level evidence chains, use `sanityops-cli` (see https://github.com/sanityops-org/sanityops-framework/blob/main/framework/try-the-tools.md).

---

## 2. Artifact inventory (input preparation, not a stage)

Case TC-084 bundles one coordinated multi-agent suite (TradingAgents v0.6.0). Artifact types present, by structural signature:

- System Prompt (present, 9 verbatim role prompts): Market Analyst, Sentiment Analyst, News Analyst, Fundamentals Analyst, Bull Researcher, Research Manager, Trader, Aggressive Risk Analyst, Portfolio Manager. Basis: prose/instruction strings returned by the agent factories.
- System Prompt (identified, not quoted): Bear Researcher, Neutral Analyst and Conservative Analyst exist per the role table but their prompt bodies were not retrieved; they are therefore not inspected.
- Tool Schema (present, representative): the LangChain `@tool` declarations in `agents/tools.py` (`get_stock_data`, `get_verified_market_snapshot`, `get_macro_indicators` shown with type-annotated signatures and docstrings; the full set listed by name). Basis: function-calling definitions with `name` + `description` + typed parameters.
- Structured-Output Schemas (present): the Pydantic models in `agents/schemas.py` (`ResearchPlan`, `TraderProposal`, `PortfolioDecision`, `SentimentReport`). Basis: not JSON tool-call `parameters`, so classified as embedded code / output contracts, not as Tool Schemas.
- Skill (absent): no markdown file with `name`/`description` front matter defines an invokable capability.
- Orchestration config (reference, not an artifact type): `graph/setup.py`, `graph/conditional_logic.py`, `agents/state.py`, `default_config.py`.
- Embedded code snippets (QC scope): the `system_message` strings, the `@tool` bodies, the Pydantic models and the orchestration/state/config snippets.
- Out of coverage: `bear_researcher.py`, `neutral_analyst.py`, `conservative_analyst.py` and several tool bodies (elided with `[...]`) are described but not quoted.

Scope note: every role is a node/agent of one LangGraph "trading firm" pipeline (analysts -> research debate -> manager -> trader -> risk debate -> portfolio manager), so all artifacts belong to the same agent suite and no artifact from another case is mixed in.

---

## 3. Stage A - Single-artifact inspection

### 3.A.1 System Prompt set (nine role prompts)

Tier determination: **L3 Complex Agent**. Basis (any 2 or more of the L3 criteria): 4+ tool invocations (twelve tools grouped per analyst); complex workflow far exceeding 5 steps (analyze -> debate -> plan -> transact -> risk-debate -> final decision); finance/security-sensitive (it drives a trading decision); requires exception handling (vendor outage, tool-round exhaustion). Upward-compatible L3 scope = 47 items.

- QD-P-1.1.1 | PASS | evidence: TC-084, the nine role prompts, no mutually exclusive attribute or directive found.
- QD-P-1.1.2 | PASS | evidence: TC-084, Market Analyst, data conflicts are arbitrated - "treat it as the source of truth for any exact OHLCV, price-level, or indicator-value claim. If another tool's output conflicts with the verified snapshot, flag the discrepancy rather than inventing a reconciled number."
- QD-P-1.1.3 | PASS | evidence: TC-084, no worked example contradicts a rule (the Trader price example "for example 189.5" matches its stated rule).
- QD-P-1.2.1 | PASS | evidence: TC-084, each role identity (analyst / researcher / manager / trader / risk debator) matches its stated responsibility.
- QD-P-1.2.2 | PASS | evidence: TC-084, each role's voice matches its declared output style (report, debate argument, structured plan).
- QD-P-1.2.3 | PASS | evidence: TC-084, no constraint prohibits a role's core responsibility.
- QD-P-1.3.1 | PASS | evidence: TC-084, Market Analyst quantities are bounded - "choose up to **8 indicators**".
- QD-P-1.3.2 | FAIL | evidence: TC-084, Market Analyst - "select the **most relevant indicators** for a given market condition or trading strategy" - the vague qualifier carries the indicator-selection boundary with no criterion.
- QD-P-1.3.3 | PASS | evidence: TC-084, the shared preamble declares the routing boundary - "Report what your tools support; another agent decides the trade."
- QD-P-1.4.1 | PASS | evidence: TC-084, no duplicate constraint found.
- QD-P-1.4.2 | PASS | evidence: TC-084, the rating-scale branches (Buy/Overweight/Hold/Underweight/Sell) are all reachable.
- QD-P-1.4.3 | PASS | evidence: TC-084, no Skill definition is given in the role prompts (vacuous).
- QD-P-1.5.1 | PASS | evidence: TC-084, each role's responsibilities support its objective (produce a report / plan / decision).
- QD-P-1.5.2 | PASS | evidence: TC-084, the workflow resources (named tools and injected context) are declared per role.
- QD-P-1.6.1 | PASS | evidence: TC-084, the vague words steer analytical selection rather than a security/permission boundary.
- QD-P-1.6.2 | PASS | evidence: TC-084, control flow keys on provided reports and tool outputs, not on unreportable internal state.
- QD-P-1.6.3 | PASS | evidence: TC-084, no soft rules are declared in mutually unreconciled tension.
- QD-P-1.6.4 | PASS | evidence: TC-084, no constraint fixes an internal reasoning method.
- QD-P-1.6.5 | PASS | evidence: TC-084, no self-referential or recursive constraint found.
- QD-P-1.6.6 | PASS | evidence: TC-084, the shared preamble declares fallback - "If you are unable to fully answer, that's OK; another assistant with different tools will help where you left off."
- QD-P-1.6.7 | PASS | evidence: TC-084, the multi-round debate structure provides iterative revision of earlier conclusions.
- QD-P-2.1.1 | PASS | evidence: TC-084, formatting is readable.
- QD-P-2.1.2 | PASS | evidence: TC-084, references (`{instrument_context}`, tool names, `{current_response}`) are named and locatable at runtime.
- QD-P-2.1.3 | PASS | evidence: TC-084, the section hierarchy (role -> data sources -> output fields) is reasonable.
- QD-P-2.1.4 | PASS | evidence: TC-084, prose is concise.
- QD-P-2.2.1 | PASS | evidence: TC-084, data sources are declared through named tools and injected context placeholders.
- QD-P-2.2.2 | FAIL | evidence: TC-084, the injected reports/context carry no declared format, encoding or size limit (e.g. Bull Researcher "Market research report: {market_research_report}").
- QD-P-2.2.3 | FAIL | evidence: TC-084, no input field or placeholder is marked required or optional.
- QD-P-2.2.4 | PASS | evidence: TC-084, the shared preamble declares degraded handling when the agent cannot fully answer.
- QD-P-2.3.1 | PASS | evidence: TC-084, output format declared - "Write these sections, in this order, starting with the recommendation on its own line".
- QD-P-2.3.2 | PASS | evidence: TC-084, the output schema fields are declared (rating enum, rationale, strategic actions; action, reasoning, entry/stop/sizing).
- QD-P-2.3.3 | PASS | evidence: TC-084, explicit section names plus the structured-output schemas bound output format stability.
- QD-P-2.3.4 | FAIL | evidence: TC-084, no sensitive-data filtering, privacy handling, or security output constraint is declared.
- QD-P-2.4.1 | PASS | evidence: TC-084, each role's workflow steps are complete (select inputs -> analyze -> emit the report/plan/decision).
- QD-P-2.4.2 | PASS | evidence: TC-084, the tools used are declared per role (e.g. Market Analyst binds `get_stock_data`, `get_indicators`, `get_verified_market_snapshot`).
- QD-P-2.4.3 | FAIL | evidence: TC-084, the prompts name tools but declare no invocation parameter specification or tool-failure handling (Market Analyst only says "call get_verified_market_snapshot for this ticker and the current date").
- QD-P-2.5.1 | PASS | evidence: TC-084, no loop or recursion is declared in the prompt (vacuous; debate caps live in the orchestration).
- QD-P-2.5.2 | FAIL | evidence: TC-084, no prohibited operation, sensitive-data access boundary, or external-access boundary is declared by any role prompt.
- QD-P-2.5.3 | FAIL | evidence: TC-084, no permission scope or escalation boundary is declared.
- QD-P-2.5.4 | PASS | evidence: TC-084, no soft-constraint conflict requires an arbitration rule.
- QD-P-2.5.5 | FAIL | evidence: TC-084, no external data-API invocation frequency limit is declared (tools route to yfinance/FRED/polymarket with no rate bound in the prompt).
- QD-P-2.6.1 | PASS | evidence: TC-084, the Market Analyst declares tool-data conflict handling ("flag the discrepancy rather than inventing a reconciled number").
- QD-P-2.6.2 | PASS | evidence: TC-084, the shared preamble declares a degraded handoff path when the agent cannot answer.
- QD-P-2.6.3 | PASS | evidence: TC-084, no retry mechanism is declared (vacuous).
- QD-P-2.7.1 | FAIL | evidence: TC-084, no representative worked example is provided (only output section shapes and one price-format illustration).
- QD-P-2.7.2 | FAIL | evidence: TC-084, no counter-examples are provided.
- QD-P-2.7.3 | FAIL | evidence: TC-084, no boundary-case examples are provided.

### 3.A.2 Tool Schema set (LangChain `@tool` data-retrieval tools)

Tier determination: **L1 Low Risk**. Basis: every quoted tool is a read-only data-retrieval tool (`get_stock_data`, `get_verified_market_snapshot`, `get_macro_indicators`, plus the listed news/fundamentals/insider data tools); no write, delete, payment or permission operation is defined. L1 minimal set = 7 items.

- QD-T-1.1 | PASS | evidence: TC-084, the quoted tools carry a name and a docstring description plus typed parameters (e.g. `get_stock_data`); `get_verified_market_snapshot`'s parameters are elided with `[...]` and not assessable.
- QD-T-1.2 | PASS | evidence: TC-084, `get_stock_data` lists `symbol`, `start_date`, `end_date`, `trade_date`, all present in the signature; no `required`/`properties` inconsistency.
- QD-T-1.3 | PASS | evidence: TC-084, no `enum` constraint is declared (`get_macro_indicators` lists aliases in prose, not as an `enum`).
- QD-T-1.4 | PASS | evidence: TC-084, the tools are function-signature definitions, which do not accept unlisted parameters (determination basis: no object-type parameter with uncontrolled `additionalProperties`).
- QD-T-2.1 | FAIL | evidence: TC-084, string parameters carry no length bound - `start_date: Annotated[str, "Start date in yyyy-mm-dd format"]` (and `symbol`, `end_date`, `curr_date`) have no `maxLength`/`minLength`.
- QD-T-2.3 | FAIL | evidence: TC-084, the numeric parameter carries no boundary - `look_back_days: Annotated[int | None, "Trailing window length in days; omit for a 1-year window"] = None` has no `minimum`/`maximum`.
- QD-T-4.1 | PASS | evidence: TC-084, the tool and parameter descriptions are specific and non-ambiguous.

### 3.A.3 Skill

- QD-S-1.x .. QD-S-5.x | N/A | evidence: TC-084 carries no Skill artifact (determination basis: no markdown file with `name`/`description` front matter defines an invokable capability). No QD-S verdict is emitted.

### 3.A.4 Embedded code snippets (QC)

QC-0 baseline: the Python snippets (prompt factories, `@tool` bodies, Pydantic models, orchestration/state/config) are fenced as `python` and are deliberately elided with `[...]`.

- QC-0.1 | PASS | evidence: TC-084, the snippets parse as valid Python syntax.
- QC-0.2 | PASS | evidence: TC-084, the code blocks declare `python`.
- QC-0.3 | PASS | evidence: TC-084, the snippets are marked as elided with `[...]`, which exempts them from standalone parse-completeness.
- QC-0.4 | PASS | evidence: TC-084, the code fences open and close correctly.
- QC-0.5 | PASS | evidence: TC-084, the declared language (`python`) matches the content.
- QC-1.1 | PASS | evidence: TC-084, the only names undefined within the snippets are framework symbols (`tool`, `Annotated`, `InjectedState`) whose imports are elided with `[...]`.
- QC-1.2 | Not Executed | evidence: TC-084, no declared dependency list is available (dependency-context rule); not recorded as FAIL.
- QC-1.3 | Not Executed | evidence: TC-084, no API version database is available (dependency-context rule); not recorded as FAIL.
- QC-1.4 | PASS | evidence: TC-084, the typed calls match their annotations; no type-mismatched call found.
- QC-2.1 .. QC-2.3 | N/A | evidence: TC-084, no file-handle, network-connection or high-risk call pattern is present in the snippets (determination basis: no such pattern).
- QC-3.1 | N/A | evidence: TC-084, imports are elided, so no unused-import determination is made.
- QC-3.2 | PASS | evidence: TC-084, referenced framework symbols are used without visible imports because the snippets are elided with `[...]`.
- QC-3.3 | PASS | evidence: TC-084, the only literals are configuration values (`"gpt-6-sol"`, `"yfinance"`), not credentials or machine-specific secrets.
- QC-4.1 | PASS | evidence: TC-084, the `TOOLS` tuples name tools that exist in the declared tool set.
- QC-4.2 | PASS | evidence: TC-084, no version/API drift between the snippets and the body.

---

## 4. Stage B - Cross-artifact inspection (QD-PS / QD-PT / QD-ST / QD-CYC)

Stage status: **Executed** (Prompt <-> Tool pairs exist). Tier L3 -> L3 full scope; QD-PS and QD-ST are Not Applicable (no Skill artifact).

- QD-PS-1.x (Prompt -> Skill) | N/A | evidence: TC-084, no Skill artifact exists (determination basis: no Prompt <-> Skill pair).
- QD-PT-2.1 | PASS | evidence: TC-084, every tool named in the prompts (get_verified_market_snapshot, get_stock_data, get_news, get_global_news, get_macro_indicators, get_prediction_markets, get_fundamentals, get_balance_sheet, get_cashflow, get_income_statement, get_insider_transactions) exists in `agents/tools.py`.
- QD-PT-2.2 | PASS | evidence: TC-084, the prompt-side tool invocations (names and argument intent) match the Tool Schema names/description.
- QD-PT-2.3 | PASS | evidence: TC-084, the prompt declares no parameter constraints that conflict with the Tool `inputSchema`.
- QD-PT-2.4 | PASS | evidence: TC-084, no RS-3 (high-risk) Tool is present, so no high-risk security-boundary declaration is required in the Prompt (determination basis: all tools are read-only).
- QD-PT-2.5 | FAIL | evidence: TC-084, the prompts do not cover the tools' possible error types - no vendor-outage, timeout or empty-result handling is declared for the data tools.
- QD-PT-2.6 | FAIL | evidence: TC-084, no invocation frequency limit is declared in the prompts for the external data tools.
- QD-ST-3.x (Skill <-> Tool) | N/A | evidence: TC-084, no Skill artifact exists (determination basis: no Skill <-> Tool pair).
- QD-CYC-1.1 | PASS | evidence: TC-084, no cross-artifact circular invocation (Skill output re-entering the Prompt, or a Tool callback re-triggering the Prompt) is declared.
- QD-CYC-1.2 | PASS | evidence: TC-084, the research and risk debates are cyclic role orchestration but are bounded by explicit termination conditions in `conditional_logic.py` (`count >= 2 * max_debate_rounds` / `count >= 3 * max_risk_discuss_rounds`); no unbounded closed loop is declared.

---

## 5. Stage C - Gate-0 (admission)

- G0-1 (no unfixed P0 in Stage A): NOT satisfied - recorded as an informational finding; does not gate this flow.
- G0-2 (no unfixed P0 in Stage B): NOT satisfied (QD-PT-2.5 at L3) - recorded as an informational finding; does not gate this flow.
- G0-3 (responsibility boundary statements exist and are locatable): Passed - each role prompt states its role and scope (e.g. "You are a trading assistant tasked with analyzing financial markets."; "As the Portfolio Manager, synthesize the risk analysts' debate and deliver the final trading decision.").
- G0-4 (each Tool Schema's `name`, `description`, parameter descriptions complete): NOT passed - several tools are shown name-only and `get_verified_market_snapshot`'s parameters are elided, so the parameter descriptions are not complete for the full set.

Gate-0 result: **Not passed - G0-4**.

---

## 6. Stage D - Permission (QD-PM Quick Mode)

Subset: Inspect Permission Governance Specification (QD-PM)
Execution Status: Not Executed
Unsatisfied Conditions: G0-4 (structural admission); additionally the full artifact set is incomplete (no Skill).
Blocking Reasons:
  G0-4 - Tool Schema `name`/`description`/parameter descriptions are not complete (several tools are name-only; one signature is elided).
  Artifact-set precondition - the full set (Prompt + Skill + all Tool Schemas) is not present (no Skill artifact).
Remediation Actions: Fix the above upstream items, then re-run Gate-0.

(The Permission stage was "Not Executed"; this is not a FAIL and not a permission conclusion.)

---

## 7. Stage E - Risk Explicit audit (EX) - physically separated from Inspect verdicts

Audit object: TC-084 System Prompt set (nine role prompts) + Tool Schema set + embedded snippets.
Three-phase scan (NL-A -> NL-B -> NR-O -> NR-S) run over the bundled artifacts.

Risk Item Summary:
- Total Risk Items: 0
- Explicit.P0 (Block release): 0 items
- Explicit.P1 (Fix / exemption): 0 items
- Explicit.P2 (Risk ledger): 0 items

Note: no explicitly declared risk expression (self-contained exfiltration, identity/permission claim, constraint removal, priority override, dangerous flag, hardcoded credential/PII, or abnormal callback) was found in the static artifact text. The "treat it as the source of truth ... flag the discrepancy" rule is a data-grounding constraint, not an instruction-priority override; the `InjectedState` parameters are framework injections, not exposed internal parameters in natural-language text. This is a static-document scan only; it is not a security conclusion. Risk Implicit (dynamic exploitability) was NOT run.

---

## 8. Stage F - Impact outlook (candidate mapping, advisory only)

Advisory context only; it does not change, soften, or escalate any Inspect conclusion. Strength is association confidence, NOT severity. Candidate language only. Risk Implicit and the runtime Quality subsets were NOT run; the lite embedded-code QC ran in Stage A. Per relevance.md Sec. 1.4, no assumption is made that controls outside the artifacts are absent.

| Defect (FAIL) | Candidate attack surface (AS-*) | Candidate failure modes (FM-*) | Strength (provisional, lite) |
|---|---|---|---|
| QD-P-1.3.2 | AS-01, AS-04 | FM-01, FM-02, FM-07, FM-09 | Conditional (qualitative indicator-selection boundary may drift) |
| QD-P-2.2.2, QD-P-2.2.3 | AS-02, AS-07 | FM-01, FM-04 | Medium (input format and necessity undeclared) |
| QD-P-2.3.4 | AS-03 | FM-06 | Conditional |
| QD-P-2.4.3 | AS-05, AS-07, AS-09 | FM-03, FM-04, FM-05 | Medium |
| QD-P-2.5.2, QD-P-2.5.3 | AS-01, AS-03, AS-04, AS-05 | FM-08, FM-09, FM-10 | Medium |
| QD-P-2.5.5 | AS-06 | FM-08, FM-09, FM-10 | Conditional |
| QD-P-2.7.1, QD-P-2.7.2, QD-P-2.7.3 | AS-01, AS-05 | FM-01, FM-07, FM-09 | Conditional |
| QD-T-2.1, QD-T-2.3 | AS-02, AS-06 | FM-03, FM-04, FM-05 | Conditional (parameter constraints absent) |
| QD-PT-2.5 | AS-06, AS-07 | FM-04, FM-05, FM-06, FM-08 | Conditional |
| QD-PT-2.6 | AS-06 | FM-04, FM-05, FM-06, FM-08 | Conditional |

Candidate RAG-Agent quality metrics (candidate associations only; NOT a quality result): Correctness, Completeness, Consistency, Traceability, Robustness, Boundary Recognition, Safety Response. Defect chains (SC-*/QC-TA-*/QC-RA-*) are out of scope for lite v1.

---

## 9. Status board

Stage A (Single-artifact):  Executed - QD-P (L3, 9 role prompts), QD-T (L1, read-only data tools), QD-S (N/A, no Skill), QC (embedded Python snippets).
Stage B (Cross):            Executed - QD-PT (Prompt -> Tool); QD-PS/QD-ST N/A (no Skill); QD-CYC-1.1/1.2 evaluated.
Stage C (Gate-0):           Not passed - G0-4 (G0-1/G0-2 informational).
Stage D (Permission QD-PM): Not Executed - Gate-0 G0-4 not satisfied; full artifact set incomplete (no Skill).
Stage E (Risk Explicit EX): Executed - 0 findings.
Stage F (Impact outlook):   Executed - candidate mapping for all Stage A/B FAILs.
Stage G (Self-verification): Executed - ID back-closure, red-line wording, output contract checked.

---

Self-verification: ID back-closure OK - red-line wording OK - output contract OK. No in-place self-corrections were required.
