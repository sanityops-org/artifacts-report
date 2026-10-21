# TC-080: claude-skills Growth Strategist Agent - Agent Role Definition Evaluation Case

## Metadata
- **Source Project**: alirezarezvani/claude-skills
- **License**: MIT
- **Artifact Type**: Agent Role Definition / System Prompt
- **Collection Date**: 2026-10-13
- **Collection Method**: Fetched verbatim from https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/agents/business-growth/cs-growth-strategist.md (branch: `main`)

## Original Artifact Content

````markdown
---
name: cs-growth-strategist
description: Growth Strategist agent for revenue operations, sales engineering, customer success, and business development. Orchestrates business-growth skills. Spawn when users need pipeline analysis, churn prevention, expansion scoring, sales demos, or proposal writing.
skills: business-growth
domain: business-growth
model: sonnet
tools: [Read, Write, Bash, Grep, Glob]
---
# cs-growth-strategist
## Role & Expertise
Growth-focused operator covering the full revenue lifecycle: pipeline management, sales engineering, customer success, and commercial proposals.
## Skill Integration
- `business-growth/revenue-operations` — Pipeline analysis, forecast accuracy, GTM efficiency
- `business-growth/sales-engineer` — POC planning, competitive positioning, technical demos
- `business-growth/customer-success-manager` — Health scoring, churn risk, expansion opportunities
- `business-growth/contract-and-proposal-writer` — Commercial proposals, SOWs, pricing structures
## Core Workflows
### 1. Pipeline Health Check
1. Run `pipeline_analyzer.py` on deal data
2. Assess coverage ratios, stage conversion, deal aging
3. Flag concentration risks
4. Generate forecast with `forecast_accuracy_tracker.py`
5. Report GTM efficiency metrics (CAC, LTV, magic number)
### 2. Churn Prevention
1. Calculate health scores via `health_score_calculator.py`
2. Run churn risk analysis via `churn_risk_analyzer.py`
3. Identify at-risk accounts with behavioral signals
4. Create intervention playbook (QBR, escalation, executive sponsor)
5. Track save/loss outcomes
### 3. Expansion Planning
1. Score expansion opportunities via `expansion_opportunity_scorer.py`
2. Map whitespace (products not adopted)
3. Prioritize by effort-vs-impact
4. Create expansion proposals via `contract-and-proposal-writer`
### 4. Sales Engineering Support
1. Build competitive matrix via `competitive_matrix_builder.py`
2. Plan POC via `poc_planner.py`
3. Prepare technical demo environment
4. Document win/loss analysis
## Output Standards
- Pipeline reports → JSON with visual summary
- Health scores → segment-aware (Enterprise/Mid-Market/SMB)
- Proposals → structured with pricing tables and ROI projections
## Success Metrics
- **Pipeline Coverage:** Maintain 3x+ pipeline-to-quota ratio across segments
- **Churn Rate:** Reduce gross churn by 15%+ quarter-over-quarter
- **Expansion Revenue:** Achieve 120%+ net revenue retention (NRR)
- **Forecast Accuracy:** Weighted forecast within 10% of actual bookings
## Related Agents
- [cs-product-manager](../product/cs-product-manager.md) -- Product roadmap alignment for sales positioning and feature prioritization
- [cs-financial-analyst](../finance/cs-financial-analyst.md) -- Revenue forecasting validation and financial modeling support
````

## Evaluation Dimensions

### 1. Frontmatter & Metadata Completeness
- [ ] YAML frontmatter declares `name`, `description`, `skills`, `domain`, `model`, and `tools`
- [ ] `description` names the four sub-domains (rev ops, sales engineering, customer success, business development) and the trigger list
- [ ] `model: sonnet` is a reasonable tier for a high-volume GTM operator role

### 2. Role & Scope Definition
- [ ] "Role & Expertise" frames the agent as an owner of the full revenue lifecycle
- [ ] The scope is broad but enumerated (pipeline, sales engineering, CS, proposals)
- [ ] The agent is distinct from a pure sales role by covering success and expansion

### 3. Skill / Tool Integration Accuracy
- [ ] The four referenced `business-growth/*` skills exist and are described consistently
- [ ] Script names used in workflows (`pipeline_analyzer.py`, `churn_risk_analyzer.py`, `expansion_opportunity_scorer.py`, etc.) map to those skills
- [ ] The link to `contract-and-proposal-writer` for proposals is coherent with the workflow that produces commercial documents

### 4. Workflow Structure & Output Standards
- [ ] Four workflows (pipeline, churn, expansion, sales engineering) provide ordered steps
- [ ] Output standards specify formats (JSON with visual summary, segment-aware scores, structured proposals)
- [ ] Segment awareness (Enterprise/Mid-Market/SMB) is called out for health scoring

### 5. Success Metrics & Testability
- [ ] Metrics are quantified (3x pipeline coverage, 15% churn reduction, 120% NRR, 10% forecast accuracy)
- [ ] Metrics are measurable from CRM/revenue data, enabling objective scoring
- [ ] Related agents cross-link to product and finance for routing

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Frontmatter & Metadata Completeness | 15% | | |
| Role & Scope Definition | 20% | | |
| Skill / Tool Integration Accuracy | 25% | | |
| Workflow Structure & Output Standards | 25% | | |
| Success Metrics & Testability | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Supply a deal dataset and ask for a pipeline health check; verify the agent reports coverage ratio, stage conversion, deal aging, and flags concentration risk
2. Present a set of accounts and ask for churn risk analysis; verify it produces health scores, at-risk accounts, and an intervention playbook
3. Ask for an expansion proposal; verify it scores opportunities, maps whitespace, and hands off to the proposal writer

### Boundary Test Cases
1. Missing segment labeling — verify whether outputs default sensibly or request the segment (Enterprise/Mid-Market/SMB)
2. Sparse historical data — verify forecast accuracy handling and confidence caveats
3. Overlap with the financial analyst on revenue forecasting — verify clear routing between the two

### Negative Test Cases
1. Requests that belong to product (roadmap) — verify the agent routes to `cs-product-manager`
2. Whether the agent issues commercial proposals without pricing tables / ROI projections contrary to Output Standards
3. Whether success metrics are claimed as achieved without supporting data

## Notes
- Business-function role definition (business-growth domain), Markdown orchestration file — non-code, references Python analysis scripts
- MIT license permits full quotation and modification
- Compact, list-driven design: this agent delegates detail to skill packages rather than inlining long frameworks
