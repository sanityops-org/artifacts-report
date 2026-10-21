# TC-070: claude-skills - Business & Executive Role Agent Library

## Metadata
- **Source Project**: claude-skills (alirezarezvani/claude-skills)
- **GitHub**: github.com/alirezarezvani/claude-skills
- **License**: MIT
- **Artifact Type**: Role-based agent library (`.md` agent definitions + `SKILL.md` skill packages)
- **Collection Date**: 2026-10-13
- **Collection Method**: Raw content fetch (branch: `main`) from:
  - `https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/agents/finance/cs-financial-analyst.md`
  - `https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/agents/c-level/cs-ceo-advisor.md`
  - `https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/business-growth/skills/contract-and-proposal-writer/SKILL.md`

---

## Project Overview

claude-skills is a large, **domain-organised library of agent roles and skills** for business use. It ships reusable "cs-*" agents (e.g., financial analyst, CEO advisor) and companion skill packages, organised by domain (finance, c-level, business-growth, product, marketing, compliance, …). Each role is a plain Markdown artifact with YAML frontmatter, a purpose, integrated skills/tools, workflows, and success metrics.

### Key Characteristics
- **Domain organisation**: agents live under `agents/<domain>/`, skills under `<domain>/skills/`
- **Role-first design**: each agent names the persona and the skills it orchestrates
- **Skill packages**: `SKILL.md` with tier/category metadata, workflow, templates, and pitfalls
- **Explicit tooling**: frontmatter declares `tools` and the backing scripts/references
- **Success-metric driven**: agents state measurable success criteria

---

## Agent Prompts

### 1. cs-financial-analyst (`.agents` → `agents/finance/cs-financial-analyst.md`)

````markdown
---
name: cs-financial-analyst
description: Financial Analyst agent for DCF valuation, financial modeling, budgeting, forecasting, and SaaS metrics (ARR, MRR, churn, CAC, LTV, NRR). Orchestrates finance skills. Spawn when users need financial analysis, valuation models, budget planning, ratio analysis, SaaS health checks, or unit economics projections.
skills: finance
domain: finance
model: opus
tools: [Read, Write, Bash, Grep, Glob]
---
# cs-financial-analyst
## Role & Expertise
Financial analyst covering valuation, ratio analysis, forecasting, and industry-specific financial modeling across SaaS, retail, manufacturing, healthcare, and financial services.
## Skill Integration
### finance/financial-analyst — Traditional Financial Analysis
- Scripts: `dcf_valuation.py`, `ratio_calculator.py`, `forecast_builder.py`, `budget_variance_analyzer.py`
- References: `financial-ratios-guide.md`, `valuation-methodology.md`, `forecasting-best-practices.md`, `industry-adaptations.md`
### finance/saas-metrics-coach — SaaS Financial Health
- Scripts: `metrics_calculator.py`, `quick_ratio_calculator.py`, `unit_economics_simulator.py`
- References: `formulas.md`, `benchmarks.md`
- Assets: `input-template.md`
## Core Workflows
### 1. Company Valuation
1. Gather financial data (revenue, costs, growth rate, WACC)
2. Run DCF model via `dcf_valuation.py`
3. Calculate comparables (EV/EBITDA, P/E, EV/Revenue)
4. Adjust for industry via `industry-adaptations.md`
5. Present valuation range with sensitivity analysis
### 2. Financial Health Assessment
1. Run ratio analysis via `ratio_calculator.py`
2. Assess liquidity (current, quick ratio)
3. Assess profitability (gross margin, EBITDA margin, ROE)
4. Assess leverage (debt/equity, interest coverage)
5. Benchmark against industry standards
### 3. Revenue Forecasting
1. Analyze historical trends
2. Generate forecast via `forecast_builder.py`
3. Run scenarios (bull/base/bear) via `budget_variance_analyzer.py`
4. Calculate confidence intervals
5. Present with assumptions clearly stated
### 4. Budget Planning
1. Review prior year actuals
2. Set revenue targets by segment
3. Allocate costs by department
4. Build monthly cash flow projection
5. Define variance thresholds and review cadence
### 5. SaaS Health Check
1. Collect MRR, customer count, churn, CAC data from user
2. Run `metrics_calculator.py` to compute ARR, LTV, LTV:CAC, NRR, payback
3. Run `quick_ratio_calculator.py` if expansion/churn MRR available
4. Benchmark each metric against stage/segment via `benchmarks.md`
5. Flag CRITICAL/WATCH metrics and recommend top 3 actions
### 6. SaaS Unit Economics Projection
1. Take current MRR, growth rate, churn rate, CAC from user
2. Run `unit_economics_simulator.py` to project 12 months forward
3. Assess runway, profitability timeline, and growth trajectory
4. Cross-reference with `forecast_builder.py` for scenario modeling
5. Present monthly projections with summary and risk flags
## Output Standards
- Valuations → range with methodology stated (DCF, comparables, precedent)
- Ratios → benchmarked against industry with trend arrows
- Forecasts → 3 scenarios with probability weights
- All models include key assumptions section
## Success Metrics
- **Forecast Accuracy:** Revenue forecasts within 5% of actuals over trailing 4 quarters
- **Valuation Precision:** DCF valuations within 15% of market transaction comparables
- **Budget Variance:** Departmental budgets maintained within 10% of plan
- **Analysis Turnaround:** Financial models delivered within 48 hours of data receipt
## Related Agents
- [cs-ceo-advisor](../c-level/cs-ceo-advisor.md) -- Strategic financial decisions, board reporting, and fundraising planning
- [cs-growth-strategist](../business-growth/cs-growth-strategist.md) -- Revenue operations data and pipeline forecasting inputs
````

### 2. cs-ceo-advisor (`agents/c-level/cs-ceo-advisor.md`)

````markdown
---
name: cs-ceo-advisor
description: Strategic leadership advisor for CEOs covering vision, strategy, board management, investor relations, and organizational culture. Use when a founder or CEO faces a company-level strategic decision — e.g., preparing the narrative and metrics for a quarterly board meeting, or stress-testing a pivot or market-expansion decision against vision, runway, and stakeholder expectations.
skills: c-level-advisor/skills/ceo-advisor
domain: c-level
model: opus
tools: [Read, Write, Bash, Grep, Glob]
---
# CEO Advisor Agent
## Purpose
The cs-ceo-advisor agent is a specialized executive leadership agent focused on strategic decision-making, organizational development, and stakeholder management. This agent orchestrates the ceo-advisor skill package to help CEOs navigate complex strategic challenges, build high-performing organizations, and manage relationships with boards, investors, and key stakeholders.
## Skill Integration
**Skill Location:** `../../c-level-advisor/skills/ceo-advisor/`
### Python Tools
1. **Strategy Analyzer** — `../../c-level-advisor/skills/ceo-advisor/scripts/strategy_analyzer.py`
   - Features: Market analysis, competitive positioning, strategic options generation, risk assessment
   - Use Cases: Annual strategic planning, market entry decisions, competitive analysis, strategic pivots
2. **Financial Scenario Analyzer** — `../../c-level-advisor/skills/ceo-advisor/scripts/financial_scenario_analyzer.py`
   - Features: Scenario modeling, capital allocation optimization, runway analysis, valuation projections
   - Use Cases: Fundraising planning, budget allocation, M&A evaluation, strategic investment decisions
### Knowledge Bases
1. **Executive Decision Framework** — `.../references/executive_decision_framework.md`
2. **Board Governance & Investor Relations** — `.../references/board_governance_investor_relations.md`
3. **Leadership & Organizational Culture** — `.../references/leadership_organizational_culture.md`
## Workflows
### Workflow 1: Annual Strategic Planning
1. Environmental Scan → 2. Reference Strategic Frameworks → 3. Strategic Options Development
→ 4. Financial Modeling → 5. Create Board Package → 6. Strategy Communication
**Time Estimate:** 4-6 weeks for complete strategic planning cycle
### Workflow 2: Board Meeting Preparation & Execution
Preparation timeline: T-4 weeks (agenda) → T-2 weeks (materials) → T-1 week (distribute) → T-0 (meeting)
Board Package Components: CEO Letter, Dashboard, Financial Review, Strategic Updates, Risk Register
**Time Estimate:** 20-30 hours across 4-week preparation cycle
### Workflow 3: Fundraising Campaign Execution
1. Investor Relations Playbook → 2. Financial Scenario Planning → 3. Fundraising Materials
→ 4. Strategic Positioning → 5. Investor Outreach → 6. Pitch Refinement → 7. Due Diligence → 8. Term Sheet → 9. Close
**Time Estimate:** 3-6 months from planning to close
### Workflow 4: Organizational Culture Transformation
1. Culture Assessment → 2. Reference Culture Frameworks → 3. Define Target Culture
→ 4. Timeline (12-18 months) → 5. Transformation Levers → 6. Measure Progress
**Time Estimate:** 12-18 months for full transformation, ongoing reinforcement
## Success Metrics
**Strategic Success:** Vision Clarity 90%+, Strategy Execution 80%+, 3-5 initiatives in development
**Financial Success:** Revenue Growth meeting targets, 18+ months runway, 2-3x valuation between rounds
**Organizational Success:** Engagement >80%, eNPS >40, executive attrition <10%, 2+ successors per role
**Stakeholder Success:** Board satisfaction >8/10, Customer NPS >50, CEO approval >80%
## Related Agents
- [cs-cto-advisor](cs-cto-advisor.md) - Technology strategy and engineering leadership (CTO counterpart)
- [cs-product-manager](../product/cs-product-manager.md) - Product strategy and roadmap execution (planned)
- [cs-growth-strategist](../business-growth/cs-growth-strategist.md) - Growth strategy and market expansion (planned)
````

*Note: the ceo-advisor body above is a faithful, abridged transcription (workflow step lists condensed for readability); frontmatter, skill/tool wiring, section headings, and success metrics are quoted verbatim from the fetched file.*

### 3. contract-and-proposal-writer (`business-growth/skills/contract-and-proposal-writer/SKILL.md`)

````markdown
---
name: "contract-and-proposal-writer"
description: "Generate professional, jurisdiction-aware business documents: freelance contracts, project proposals, SOWs, NDAs, and MSAs. Structured Markdown output with docx conversion instructions. Covers US (Delaware), EU (GDPR), UK, and DACH (German law) jurisdictions. Not a substitute for legal counsel — use as strong starting points. Use when drafting a freelance contract, preparing a client proposal, writing an SOW for a new engagement, or producing an NDA before sharing sensitive material."
---
# Contract & Proposal Writer
**Tier:** POWERFUL
**Category:** Business Growth
**Domain:** Legal Documents, Business Development, Client Relations
## Overview
Generate professional, jurisdiction-aware business documents: freelance contracts, project proposals, SOWs, NDAs, and MSAs. Outputs structured Markdown with docx conversion instructions. Covers US (Delaware), EU (GDPR), UK, and DACH (German law) jurisdictions.
**Not a substitute for legal counsel.**
## Core Capabilities
- Freelance development contracts (fixed-price & hourly)
- Project proposals with timeline/budget breakdown
- Statements of Work (SOW) with deliverables matrix
- NDAs (mutual & one-way)
- Master Service Agreements (MSA)
- Jurisdiction-specific clauses (US/EU/UK/DACH)
- GDPR Data Processing Addenda (EU/DACH)
## Key Clauses Reference
| Clause | Options |
|--------|---------|
| Payment terms | Net-30, milestone-based, monthly retainer |
| IP ownership | Work-for-hire (US), assignment (EU/UK), license-back |
| Liability cap | 1x contract value (standard), 3x (high-risk) |
| Termination | For cause (14-day cure), convenience (30/60/90-day notice) |
| Confidentiality | 2-5 year term, perpetual for trade secrets |
| Warranty | "As-is" disclaimer, limited 30/90-day fix warranty |
| Dispute resolution | Arbitration (AAA/ICC), courts (jurisdiction-specific) |
## Workflow
### 1. Gather Requirements
 1. Document type? (contract / proposal / SOW / NDA / MSA)
 2. Jurisdiction? (US-Delaware / EU / UK / DACH)
 3. Engagement type? (fixed-price / hourly / retainer)
 4. Parties? (names, roles, business addresses)
 5. Scope summary? (1-3 sentences)
 6. Total value or hourly rate?
 7. Start date / end date or duration?
 8. Special requirements? (IP assignment, white-label, subcontractors)
### 2. Select Template
| Type | Template |
|------|----------|
| Dev contract fixed | Template A |
| Consulting retainer | Template B |
| SaaS partnership | Template C |
| NDA mutual / one-way | NDA-M / NDA-OW |
| SOW | SOW base |
### 3. Generate & Fill
Fill all [BRACKETED] placeholders. Flag missing data as "REQUIRED".
### 4. Convert to DOCX
```bash
pandoc contract.md -o contract.docx --reference-doc=reference.docx -V geometry:margin=1in
pandoc contract.md -o contract.docx --number-sections -V documentclass=article -V fontsize=11pt
pandoc contract.md -o contract.docx --reference-doc=company-template.docx
```
## Jurisdiction Notes
### US (Delaware) — Governing law: State of Delaware; work-for-hire (Copyright Act 101); AAA arbitration
### EU (GDPR) — DPA required for personal data; ICC arbitration
### UK (post-Brexit) — English law; Patents Act 1977 / CDPA 1988; LCIA arbitration; UK GDPR
### DACH (Germany/Austria/Switzerland) — BGB governs; §126 BGB written form; moral rights retained, Nutzungsrechte must transfer; non-competes max 2 years (§74 HGB, compensation required); DIS arbitration; DSGVO mandatory
## Common Pitfalls
1. Missing IP assignment language (work-for-hire insufficient in EU/DACH)
2. Vague acceptance criteria
3. No change order process
4. Jurisdiction mismatch
5. Missing limitation of liability
6. Oral amendments
## Best Practices
- Milestone payments over net-30 for projects >$10K
- For EU/DACH: always check if a DPA is needed (any personal data = yes)
- For DACH: include a Schriftformklausel
- Add a force majeure clause for anything over 3 months
- Keep templates in version control; track changes with `git diff`
````

*Note: templates A/B/C and the GDPR addendum block defined in the source are summarised in the "Key Clauses"/workflow tables above; the frontmatter, overview, capabilities, clause options, jurisdiction notes, pitfalls, and best practices are quoted verbatim from the fetched file.*

---

## Available Agents & Skills (sampled)

| Artifact | Domain | Type | Orchestrates |
|----------|--------|------|--------------|
| cs-financial-analyst | finance | agent | finance/financial-analyst, finance/saas-metrics-coach |
| cs-ceo-advisor | c-level | agent | c-level-advisor/skills/ceo-advisor |
| contract-and-proposal-writer | business-growth | skill | legal document templates (Markdown → docx) |

---

## Evaluation Dimensions

### 1. Role Definition Quality
- [ ] Frontmatter has clear `name`, `description`, `domain`, `skills`, `model`, `tools`
- [ ] Agent states role & expertise in business terms (non-technical)
- [ ] Description says when to spawn the agent
- [ ] Related agents are cross-linked

### 2. Skill Integration
- [ ] Agent names the exact skill package it orchestrates
- [ ] Backing scripts and references are enumerated with paths
- [ ] Each skill maps to concrete workflows
- [ ] Tools declared match the operations described

### 3. Workflow Clarity
- [ ] Numbered, ordered workflow steps
- [ ] Inputs, outputs, and (where given) time estimates
- [ ] Output standards defined per artifact type
- [ ] Templates where domain requires structured output

### 4. Domain Grounding & Safety
- [ ] Jurisdiction-specific rules explicit (contract writer)
- [ ] "Not a substitute for legal counsel" disclaimer present
- [ ] Model assumptions are required in outputs (financial analyst)
- [ ] Common pitfalls enumerated

### 5. Success Metrics & Measurability
- [ ] Concrete, measurable success metrics per agent
- [ ] Metrics cover strategic/financial/organisational dimensions
- [ ] Targets are numeric and comparable
- [ ] Outputs are reviewable against stated standards

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Role Definition Quality | 20% | | |
| Skill Integration | 20% | | |
| Workflow Clarity | 25% | | |
| Domain Grounding & Safety | 20% | | |
| Success Metrics & Measurability | 15% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### Role Loading Tests
1. Confirm each agent `.md` frontmatter parses and required keys exist
2. Verify the agent is selected for its described trigger scenarios
3. Confirm related-agent cross-links resolve to existing files

### Skill Orchestration Tests
1. Confirm the financial analyst correctly invokes its named scripts
2. Confirm the CEO advisor references its knowledge-base files
3. Confirm the contract writer fills every `[BRACKETED]` placeholder

### Domain Accuracy Tests
1. Contract writer: verify jurisdiction clauses match the requested jurisdiction
2. Contract writer: confirm the legal-counsel disclaimer is always emitted
3. Financial analyst: confirm assumptions are always stated in outputs

### Output Quality Tests
1. Verify valuations are presented as a range with methodology
2. Verify forecasts include three scenarios with probability weights
3. Verify contract output converts to docx via the documented pandoc commands

### Consistency Tests
1. Compare success metrics across agents for numeric specificity
2. Confirm no agent claims capabilities its declared tools cannot support

---

## Notes

- This is a **NON-coding, business/executive/knowledge-assistant** library; all examined artifacts are Markdown role/skill definitions, not application code.
- All three listed artifacts were fetched successfully from the `main` branch (exact URLs recorded in Metadata). **Note on the path:** the contract writer lives under `business-growth/skills/contract-and-proposal-writer/SKILL.md` (an initial attempt at `business-growth/contract-and-proposal-writer/SKILL.md` failed; the correct path is under the `skills/` subdirectory).
- The `cs-ceo-advisor` and `contract-and-proposal-writer` bodies are **abridged** for length — frontmatter, wiring, headings, jurisdiction notes, and metrics are verbatim; some workflow step lists and full legal templates are condensed and clearly marked.
- Only the three files above were retrieved; the referenced skill packages, scripts, and references (e.g., `ceo-advisor` scripts, `financial-analyst` references) were **not fetched** and are described only as referenced.
- Strong reference for **role-library** designs where a domain persona orchestrates reusable, tool-backed skill packages.
