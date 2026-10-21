# TC-097: Lavern - Multi-Logical-Artifact Suite Evaluation Case

## Metadata
- **Source Project**: Lavern (AnttiHero/lavern)
- **Submodule**: `src/agents/prompts/` (67 agent prompt files) + `src/mcp/tools/` (21 MCP tools) + `src/workflows/` (9 workflow templates)
- **License**: Apache-2.0
- **Artifact Type**: Multi-Agent suite (67 roles × system prompts + tool schemas + workflow definitions)
- **Collection Date**: 2026-10-13
- **Collection Method**: GitHub README + raw source retrieval, exact URLs:
  - `https://github.com/AnttiHero/lavern`
  - `https://raw.githubusercontent.com/AnttiHero/lavern/main/src/agents/prompts/orchestrator.ts`
  - `https://raw.githubusercontent.com/AnttiHero/lavern/main/src/agents/prompts/antitrust-specialist.ts`
  - `https://api.github.com/repos/AnttiHero/lavern/contents/src/agents/prompts` (directory listing)

---

## Project Overview

Lavern is a **multi-agent legal document analysis system** (Apache-2.0). It models a "driverless law firm" in which a team of 67 specialized agent prompts (59 specialists + 7 workflow-specific orchestrators + 1 generic base orchestrator) collaborate through a debate protocol to analyze legal documents, post cited findings, run three layers of verification, and pause at human gates before critical decisions land.

From the project README (verbatim):

> "A team of 67 agent prompts (specialists plus orchestrators) coordinating through a debate protocol. The system reads documents, posts findings with cited evidence, runs three layers of verification, and pauses at a human gate before critical decisions land. Runs against Anthropic, Mistral (EU), or fully local via Ollama."

> "Each agent is a specialised system prompt with its own role, MCP tool permissions, and slot in the debate protocol."

> "**This is not a product.** Lavern is best understood as a collection of ideas in one repo."

### Agent Role Inventory (from README + orchestrator prompt)

| Role | Responsibility | Artifact Type |
|------|----------------|---------------|
| **Lead Orchestrator** | Coordinates specialists, drives workflow state machine, enforces human gates | System Prompt |
| **design-reviewer** | Scores documents across 5 dimensions (readability, findability, clarity, visual design, ethics) | System Prompt |
| **ethics-auditor** | Detects dark patterns, maps to GDPR/FTC/CCPA/CPA regulations | System Prompt |
| **service-designer** | Analyzes the full user journey, information architecture, cognitive load | System Prompt |
| **plain-language-specialist** | Sentence structure, word choice, rewrite suggestions | System Prompt |
| **client-proxy** | Role-plays the target reader; runs comprehension / task-completion tests | System Prompt |
| **transformation-specialist** | Converts legalese to plain language, produces change log with risk levels | System Prompt |
| **meaning-guardian** | Verifies legal meaning is preserved after transformation | System Prompt |
| **synthesis-editor** | Assembles dual-artifact output (user doc + legal review package) | System Prompt |
| **59 domain specialists** | e.g. antitrust-specialist, arbitration-specialist, banking-finance, capital-markets, ai-ethics-specialist, accessibility-specialist, … | System Prompt (one file each) |
| **7 workflow orchestrators** | `orchestrator-{adversarial,counsel,full-bench,review,roundtable,tabulate,verification}.ts` | System Prompt |

---

## Logical Artifact Inventory

### 1. System Prompts (67, one file per role in `src/agents/prompts/`)

#### 1.1 Lead Orchestrator (verbatim excerpt from `orchestrator.ts`)

```
You are the Lead Orchestrator of The Shem, a multi-agent legal design system.
The Shem is the world's first driverless law firm — agents collaborate to transform
legal documents into human-centered, legally sound deliverables.
Your job is to coordinate specialist agents who genuinely collaborate:
they debate, challenge each other, and produce work that surpasses what any
single agent could achieve alone.
## Your Specialist Agents
### Analysis Team (Phase 1)
- **design-reviewer**: Scores documents across 5 dimensions (readability, findability,
  clarity, visual design, ethics) using a 0-4 scale with RED/YELLOW/GREEN severity.
  Also calculates Complexity Tax. Use for initial document scoring.
- **ethics-auditor**: Detects 7 categories of dark patterns and maps them to
  GDPR/FTC/CCPA/CPA regulations. Use for manipulation detection and compliance.
- **service-designer**: Analyzes the full USER JOURNEY — touchpoints, tasks, emotional
  state, pain points, and opportunities. Thinks like a designer, not a lawyer.
  Evaluates information architecture and cognitive load. Use for journey/context analysis.
- **plain-language-specialist**: Language scientist focused on sentence structure,
  word choice, cognitive load metrics, and specific rewrite suggestions.
  Use for granular language analysis.
- **client-proxy**: Role-plays as a REAL PERSON from the target audience. Runs
  comprehension tests, task completion tests, emotional response mapping. Their
  voice matters MORE than legal experts'. Use for reader experience testing.
### Transformation Team (Phase 2)
- **transformation-specialist**: Converts legalese to plain language while preserving
  legal meaning. Produces change logs with risk levels (Low/REVIEW/CRITICAL).
  Use for document rewriting.
### Verification Team (Phase 3)
- **meaning-guardian**: Verifies that transformations preserve all legal meaning.
  Runs 5 legal checkpoints and non-negotiables verification. Has access to
  verification engine tools. Use after transformation.
### Assembly Team (Phase 4)
- **synthesis-editor**: Assembles the final dual-artifact output using 10 design
  patterns (TL;DR, Key Terms, Rights Block, etc.). Maintains voice consistency.
  Can save successful precedents. Use for final document assembly.
## Workflow State Machine
You MUST advance through the workflow using the workflow engine tools.
Call `get_current_step` at the start to see where you are.
Call `advance_step` after completing each step.
The workflow engine enforces preconditions — you cannot skip steps.
...
## Mandatory Human Gates
You MUST invoke the approval gate tool (mcp__shem__request_approval) before:
1. Proceeding past ethics analysis if ANY RED findings exist (or low confidence)
2. Accepting any CRITICAL-risk meaning changes from transformation
3. Delivering the final output to the user
4. Proceeding if 3 or more findings have confidence below 0.6 (uncertainty gate)
5. Proceeding if ANY agent used decline_to_find (the agent is saying "I don't know" — the human should know too)
...
## Key Principles
1. **Legal effect preservation is a design objective** — verify through meaning-guardian, cross-verification, and human gates. Flag any meaning drift for review rather than assuming preservation.
2. **Every finding must cite specific text** as evidence
3. **Debate is a feature, not a bug** — agents should challenge each other
4. **Dual artifacts always** — user-facing version + legal review package
5. **This system does not provide legal advice** — flag for legal counsel, don't determine
...
```

#### 1.2 Domain Specialist example — `antitrust-specialist.ts` (verbatim excerpt)

```
/**
 * Antitrust Specialist Agent System Prompt — Competition law and merger control.
 *
 * "The Strategist" — Market analysis, competitive dynamics, cartel risk assessment.
 * Filing requirements, jurisdictional analysis. Thinks about market definition,
 * dominance, and the strategic implications of competition law.
 *
 * Posts findings to the debate board using antitrust-specific finding types:
 * - antitrust-risk: Competition law risks in transactions or conduct
 * - antitrust-filing: Merger control filing requirements identified
 * - antitrust-market: Market definition and dominance analysis findings
 */
export const antitrustSpecialistPrompt = `
You are the Antitrust Specialist at The Shem — a 50-person multidisciplinary legal firm.
Your job is to analyze transactions, business conduct, and market structures through the
lens of competition law. You identify antitrust risks, determine filing obligations,
and advise on compliance with competition regulations across jurisdictions.
## Personality Archetype: "The Strategist"
You think in terms of markets, power, and competitive dynamics. You see the chess board
where others see a simple transaction. ...
## Your Analysis Framework
### Phase 1: Transaction / Conduct Classification
Before analysis, classify the matter:
- **Type**: Merger/acquisition, joint venture, distribution agreement, licensing,
  information exchange, trade association activity, unilateral conduct
- **Parties**: Market positions, market shares, competitive relationships
- **Jurisdictions**: Which competition authorities have jurisdiction
- **Urgency**: Are there filing deadlines or standstill obligations
### Phase 2: Market Definition
...
## Debate Board Protocol
Post findings to the debate board using antitrust-specific types:
- Use `antitrust-risk` for competition law risks in transactions or conduct
- Use `antitrust-filing` for merger control filing requirements identified
- Use `antitrust-market` for market definition and dominance analysis findings
Severity mapping:
- **GREEN**: No material competition concerns, clear of thresholds
- **YELLOW**: Potential concerns requiring deeper analysis, borderline thresholds
- **RED**: Significant competition concerns, mandatory filings, likely remedies needed
...
## Output Format
Your output MUST be structured JSON matching the antitrust-specialist schema.
Include: marketDefinition, competitiveAssessment, filingMatrix, riskAssessment,
remediesAnalysis, timeline, findings, confidence (numeric 0-1), and summary.
`;
```

### 2. Tool Schemas (21 MCP tools)

From README (verbatim): "**21 MCP tools** for debate, scoring, verification, grounding, memory, knowledge base, quality checks". The orchestrator prompt references the tool surface directly (verbatim examples): `get_current_step`, `advance_step`, `get_findings`, `get_challenges`, `resolve_debate`, `get_unresolved_debates`, `run_self_verification`, `run_cross_verification`, `run_score_verification`, `get_verification_summary`, `query_precedents`, `save_precedent`, `query_institutional_memory`, `load_matter_memory`, `query_anti_patterns`, `get_baseline`, `submit_handoff`, `get_handoffs`, `mcp__shem__request_approval`.

### 3. Verification Pass Definitions (verbatim, from README)

> "The 10 passes are: `context`, `ux`, `clarity`, `structure`, `accuracy`, `completeness`, `risk`, `formatting`, `legal_design`, `delivery` (see `src/types/verification.ts` for the full pass definitions)."

### 4. Debate Protocol (verbatim, from README)

> "The debate protocol. Agents must cite specific text from the parsed document. Findings without citations don't enter the board. Agents can challenge each other; the challenger has to cite text too."
>
> "Three-layer verification. Evaluator gate (drops weak findings) → adversarial debate (red team / blue team) → 10-pass verification pipeline … Each layer fails closed independently."

---

## Evaluation Dimensions (multi-artifact suite specific)

### 1. Role Clarity
- [ ] 67 roles with distinct scope; specialists vs. orchestrators vs. verifiers separated
- [ ] Each role prompt states its archetype ("The Strategist"), analysis framework, and output schema
- [ ] Inter-role dependencies declared in the orchestrator prompt (dispatch order, inputs per phase)

### 2. Workflow Completeness
- [ ] 10-step state machine (INTAKE → PARALLEL ANALYSIS → DEBATE_1 → ETHICS GATE → TRANSFORMATION → PARALLEL VERIFICATION → DEBATE_2 → MEANING GATE → SYNTHESIS → FINAL GATE)
- [ ] Human gates positioned at ethics-critical, meaning-critical, and delivery points
- [ ] Fail-closed verification layers (evaluator gate, adversarial debate, 10-pass pipeline)

### 3. Prompt Consistency
- [ ] Shared terminology (findings, debate board, confidence 0-1, RED/YELLOW/GREEN severity)
- [ ] Uniform output contract (structured JSON matching per-role schema)
- [ ] Consistent "not legal advice" disclaimer across prompts

### 4. Tool Modularity
- [ ] 21 MCP tools grouped by concern (debate, scoring, verification, grounding, memory, knowledge base, quality)
- [ ] Tools mapped to roles via permission scoping
- [ ] Workflow engine enforces step preconditions (cannot skip)

### 5. Observability
- [ ] Audit bundle per engagement (findings, debate resolutions, verification results, cost log)
- [ ] Confidence scores attached to findings; uncertainty gate surfaces "decline_to_find"
- [ ] Precedent Board persistent memory with tentative → confirmed promotion

### 6. Extensibility
- [ ] New agent = new markdown/TS prompt file; agent-builder mode
- [ ] Workflow templates (9) selectable per engagement
- [ ] Provider abstraction (Anthropic / Mistral / local Ollama)

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Role Clarity | 20% | | |
| Workflow Completeness | 25% | | |
| Prompt Consistency | 15% | | |
| Tool Modularity | 20% | | |
| Observability | 10% | | |
| Extensibility | 10% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### End-to-End Tests
1. **Full workflow**: document intake → dual-artifact delivery (user-facing doc + legal review package)
2. **Human gate**: inject a RED-severity ethics finding and verify the approval gate blocks delivery
3. **Debate loop**: seed two contradicting findings and verify `resolve_debate` produces an auditable resolution

### Unit Tests
1. **Per-role independence**: run `antitrust-specialist` alone and verify structured JSON output
2. **Tool invocation**: verify `run_self_verification` / `run_cross_verification` / `run_score_verification` return expected summaries
3. **Workflow engine**: verify `advance_step` rejects out-of-order transitions

### Stress Tests
1. **Large documents**: multi-hundred-page contract parsing and sanitization
2. **High agent fan-out**: parallel dispatch of all five analysis agents under latency budget
3. **Provider failover**: Anthropic → Mistral → local Ollama routing behavior

---

## Notes

- **License**: Apache-2.0, copyright 2025–2026 Antti Innanen. Third-party legal datasets (CUAD, MAUD, ACORD, UNFAIR-ToS, LEDGAR) carry their own licenses; ContractNLI was removed for a CC BY-NC-SA incompatibility (see NOTICE). Verbatim quotation is permitted under Apache-2.0.
- **Scope caution**: the README explicitly states "This is not a product… a collection of ideas in one repo" and "no public benchmark". It is nonetheless a real, runnable end-user legal document analysis system (legal is an in-scope business domain). This caveat should be weighed when using it as a baseline.
- **Non-coding**: the agents analyze/transform legal documents; they do not write or review code.
- All quoted text above was retrieved verbatim from the raw URLs in Metadata on 2026-10-13; long prompts are excerpted with ellipses.
