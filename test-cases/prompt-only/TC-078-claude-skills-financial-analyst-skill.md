# TC-078: claude-skills Financial Analyst Agent - Agent Role Definition Evaluation Case

## Metadata
- **Source Project**: alirezarezvani/claude-skills
- **License**: MIT
- **Artifact Type**: Agent Role Definition / System Prompt
- **Collection Date**: 2026-10-13
- **Collection Method**: Fetched verbatim from https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/agents/finance/cs-financial-analyst.md (branch: `main`)

## Original Artifact Content

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
## Integration Examples
```bash
# SaaS health check — full metrics from raw numbers
python ../../finance/skills/saas-metrics-coach/scripts/metrics_calculator.py \
  --mrr 80000 --mrr-last 75000 --customers 200 --churned 3 \
  --new-customers 15 --sm-spend 25000 --gross-margin 72 --json
# Quick ratio — growth efficiency
python ../../finance/skills/saas-metrics-coach/scripts/quick_ratio_calculator.py \
  --new-mrr 10000 --expansion 2000 --churned 3000 --contraction 500
# 12-month projection
python ../../finance/skills/saas-metrics-coach/scripts/unit_economics_simulator.py \
  --mrr 80000 --growth 8 --churn 1.5 --cac 1667 --json
# Traditional ratio analysis
python ../../finance/skills/financial-analyst/scripts/ratio_calculator.py financial_data.json --format json
# DCF valuation
python ../../finance/skills/financial-analyst/scripts/dcf_valuation.py valuation_data.json --format json
```
## Related Agents
- [cs-ceo-advisor](../c-level/cs-ceo-advisor.md) -- Strategic financial decisions, board reporting, and fundraising planning
- [cs-growth-strategist](../business-growth/cs-growth-strategist.md) -- Revenue operations data and pipeline forecasting inputs
````

## Evaluation Dimensions

### 1. Frontmatter & Metadata Completeness
- [ ] YAML frontmatter declares `name`, `description`, `skills`, `domain`, `model`, and `tools`
- [ ] `description` states both the role scope (valuation, modeling, SaaS metrics) and the trigger conditions ("spawn when users need...")
- [ ] The `model` tier (`opus`) and `tools` allow-list are appropriate for a finance-analysis agent

### 2. Role & Scope Definition
- [ ] "Role & Expertise" clearly bounds the analyst's coverage (valuation, ratio analysis, forecasting)
- [ ] The five named industries (SaaS, retail, manufacturing, healthcare, financial services) set expectations
- [ ] The distinction between traditional analysis and SaaS metrics coaching is explicit

### 3. Skill / Tool Integration Accuracy
- [ ] Referenced skills (`finance/financial-analyst`, `finance/saas-metrics-coach`) map to real skill packages
- [ ] Script names, reference files, and asset templates are listed consistently with their usage in workflows
- [ ] Relative script paths in the integration examples are coherent with the described skill locations

### 4. Workflow & Output Standards
- [ ] Six numbered workflows provide ordered, executable steps
- [ ] Output standards specify deliverable format (valuation ranges, benchmarked ratios, scenario forecasts)
- [ ] Every model is required to include a "key assumptions" section

### 5. Success Metrics & Testability
- [ ] Success metrics are quantified (5% forecast accuracy, 15% valuation precision, 10% budget variance, 48h turnaround)
- [ ] Metrics map back to the workflows so a reviewer can score outputs objectively
- [ ] Related-agent cross-references provide routing context

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Frontmatter & Metadata Completeness | 15% | | |
| Role & Scope Definition | 20% | | |
| Skill / Tool Integration Accuracy | 25% | | |
| Workflow & Output Standards | 25% | | |
| Success Metrics & Testability | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Ask the agent to produce a DCF valuation for a company with supplied revenue, cost, growth, and WACC figures; verify it follows the "Company Valuation" workflow and returns a range with sensitivity analysis
2. Provide raw MRR/churn/CAC numbers and request a SaaS health check; verify it computes ARR, LTV:CAC, NRR, and payback and flags CRITICAL/WATCH metrics
3. Request a 12-month unit-economics projection and confirm scenario outputs (bull/base/bear) with stated assumptions

### Boundary Test Cases
1. Missing inputs (e.g., no WACC, no churn figure) — verify the agent requests the missing data instead of inventing it
2. Industry outside the five named sectors — verify whether the agent adapts via `industry-adaptations.md` or flags the gap
3. Very large or sparse time series for forecasting — verify confidence-interval handling

### Negative Test Cases
1. Requests unrelated to finance (e.g., drafting marketing copy) — verify the agent does not activate or route correctly
2. Whether the agent presents a single-point valuation without a range or methodology label
3. Whether it omits the mandatory "key assumptions" section

## Notes
- This is a business-function role definition (finance domain), not code; it is a Markdown agent orchestration file that binds a persona to finance skill packages and Python scripts
- MIT license permits verbatim reproduction and modification
- The frontmatter `description` doubles as the spawn-trigger text, so its precision directly governs when the agent is activated
