# TC-153: JoelLewis/finance_skills (Asset Allocation) - Skill Evaluation Case

## Metadata
- **Source Project**: JoelLewis/finance_skills
- **License**: MIT (LICENSE file present; GitHub API reports `spdx_id: MIT`)
- **Artifact Type**: Skill (SKILL.md)
- **Collection Date**: 2026-10-13
- **Collection Method**: Fetched verbatim from https://raw.githubusercontent.com/JoelLewis/finance_skills/main/plugins/wealth-management/skills/asset-allocation/SKILL.md (default branch `main`). Repository README: https://raw.githubusercontent.com/JoelLewis/finance_skills/main/README.md . License file: https://raw.githubusercontent.com/JoelLewis/finance_skills/main/LICENSE . Plugin tree (GitHub API): https://api.github.com/repos/JoelLewis/finance_skills/contents/plugins/wealth-management/skills

## Original Artifact Content

````markdown
---
name: asset-allocation
description: "Determine how to distribute capital across asset classes using strategic and tactical allocation frameworks. Use when the user asks about portfolio allocation, mean-variance optimization, Black-Litterman, risk parity, glide paths, or target-date strategies. Also trigger when users mention 'how much in stocks vs bonds', '60/40 portfolio', 'policy portfolio', 'core-satellite', 'liability-driven investing', 'asset-liability matching', or ask how to split their money across investments."
---

# Asset Allocation

## Core Concepts

### Strategic Asset Allocation (SAA)
The long-term policy portfolio based on an investor's risk tolerance, return objectives, time horizon, and constraints. SAA determines the baseline target weights (e.g., 60% equity / 30% bonds / 10% alternatives) and is the dominant driver of long-term portfolio returns. SAA should be revisited when investor circumstances change, not in response to market movements.

### Tactical Asset Allocation (TAA)
Short-to-medium-term deviations from the SAA based on market views, valuations, or momentum signals. TAA requires a disciplined process to avoid becoming ad hoc market timing. Key considerations:
- Define allowable deviation bands (e.g., +/- 10% from SAA)
- Have a clear signal framework (valuation, momentum, macro)
- Set reversion rules: when to return to SAA weights

### Mean-Variance Optimization (MVO)
Markowitz's framework for finding optimal portfolio weights that maximize risk-adjusted return:

max w'*mu - (lambda/2) * w'*Sigma*w

subject to: sum(w_i) = 1, w_i >= 0 (if long-only), and any additional constraints.

Where:
- w = weight vector
- mu = expected return vector
- Sigma = covariance matrix
- lambda = risk aversion parameter

MVO requires three inputs: expected returns, the covariance matrix, and risk aversion. The solution is highly sensitive to expected return inputs.

### Black-Litterman Model
Combines market equilibrium returns with investor views to produce more stable, intuitive portfolio weights. Two-step process:

**Step 1 — Implied Equilibrium Returns:**
Pi = lambda * Sigma * w_mkt

where w_mkt is the market-capitalization weight vector, lambda is the risk aversion parameter, and Sigma is the covariance matrix. These are the returns the market implicitly expects given current prices.

**Step 2 — Blending with Views:**
E(R) = [(tau*Sigma)^(-1) + P'*Omega^(-1)*P]^(-1) * [(tau*Sigma)^(-1)*Pi + P'*Omega^(-1)*Q]

where:
- tau = scalar (uncertainty of equilibrium, typically 0.025-0.05)
- P = pick matrix (identifies assets in each view)
- Q = view vector (expected returns from views)
- Omega = diagonal matrix of view uncertainties

The result is a posterior expected return vector that tilts away from equilibrium toward the investor's views, proportional to confidence.

### Risk Parity
Equalizes the risk contribution from each asset (or factor) rather than equalizing capital allocation:

RC_i = w_i * (Sigma*w)_i / sigma_p

Set RC_i = RC_j for all i, j.

In a simple two-asset case with no correlation:
w_i is proportional to 1/sigma_i

Risk parity portfolios allocate more capital to lower-volatility assets (typically bonds) and often require leverage to achieve competitive return targets.

### Glide Path
An age-based or time-based allocation that systematically shifts from growth assets to defensive assets as the investor ages or the target date approaches:

Common rule of thumb: Equity % = 110 - Age

Target-date fund glide paths typically:
- Start at 90% equity for young investors
- Decrease by ~1-2% per year
- Reach 30-40% equity at retirement
- Continue to "through" allocation post-retirement

### Core-Satellite
A hybrid approach combining:
- **Core (60-80%):** Low-cost, broadly diversified index funds or ETFs
- **Satellites (20-40%):** Active strategies, factor tilts, alternatives, or concentrated positions

This structure captures the market return efficiently (core) while allowing alpha generation or specific exposures (satellites).

### Asset-Liability Matching
For investors with defined liabilities (pensions, insurance, endowments with spending rules):
- Match asset duration and cash flows to liability duration and timing
- Surplus optimization: optimize the portfolio relative to liabilities, not absolute return
- Liability-driven investing (LDI): hedge liability risk with duration-matched bonds, invest surplus in return-seeking assets

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| MVO Objective | max w'*mu - (lambda/2)*w'*Sigma*w | Optimal portfolio weights |
| Equilibrium Returns | Pi = lambda * Sigma * w_mkt | Black-Litterman starting point |
| BL Posterior | E(R) = [(tau*Sigma)^(-1) + P'*Omega^(-1)*P]^(-1) * [(tau*Sigma)^(-1)*Pi + P'*Omega^(-1)*Q] | Blended expected returns |
| Risk Contribution | RC_i = w_i * (Sigma*w)_i / sigma_p | Risk parity target |
| Risk Parity Condition | RC_i = RC_j for all i, j | Equal risk contribution |
| Glide Path Rule | Equity % = 110 - Age | Age-based allocation |

## Worked Examples

### Example 1: Three-Asset Mean-Variance Optimization
**Given:**
- Assets: US Equity (mu=8%, sigma=16%), Int'l Equity (mu=7%, sigma=18%), US Bonds (mu=3%, sigma=4%)
- Correlations: US/Intl Equity = 0.75, US Equity/Bonds = 0.10, Intl Equity/Bonds = 0.05
- Risk aversion: lambda = 4
- Constraints: long-only, fully invested

**Calculate:** Optimal weights

**Solution:**

Covariance matrix:
- Cov(US,US) = 0.16^2 = 0.0256
- Cov(Intl,Intl) = 0.18^2 = 0.0324
- Cov(Bond,Bond) = 0.04^2 = 0.0016
- Cov(US,Intl) = 0.75 * 0.16 * 0.18 = 0.0216
- Cov(US,Bond) = 0.10 * 0.16 * 0.04 = 0.00064
- Cov(Intl,Bond) = 0.05 * 0.18 * 0.04 = 0.00036

MVO with lambda=4 (solving numerically or via quadratic programming):

Optimal weights (long-only):
- US Equity: 51.9%
- Int'l Equity: 0%
- US Bonds: 48.1%

Portfolio: expected return = 5.60%, volatility = 8.71%

Note: International equity is driven to zero — it is highly correlated with US equity (0.75) but has a lower expected return, so the optimizer sees no reason to hold it. This is classic MVO behavior: small input differences produce corner solutions. Adding a maximum-weight or minimum-allocation constraint would force diversification. The high bond allocation reflects the heavy variance penalty (lambda=4); reducing lambda shifts toward equities.

### Example 2: Black-Litterman with a Relative View
**Given:** The same three assets and covariance matrix as Example 1.
- Market-cap weights: US Equity 55%, Int'l Equity 30%, US Bonds 15%
- Risk aversion lambda = 2.5, tau = 0.05
- Investor view: Int'l Equity will outperform US Bonds by 3% (view uncertainty Omega = [0.001]; lower = higher confidence)

**Calculate:** Equilibrium and posterior expected returns

**Solution:**

Step 1 — Equilibrium returns, Pi = lambda × Sigma × w_mkt:
- US Equity: 5.16%
- Int'l Equity: 5.41%
- US Bonds: 0.18%

Step 2 — View specification: P = [0, 1, -1], Q = [3%].

The equilibrium already implies Int'l beats Bonds by 5.23%, so a 3% view is *bearish* relative to equilibrium. Applying the Black-Litterman posterior formula:
- US Equity: 4.28% (pulled down via its 0.75 correlation with Int'l)
- Int'l Equity: 4.07% (down from 5.41%)
- US Bonds: 0.23% (up slightly)

The posterior tilts returns toward the view in proportion to confidence. Fed into MVO, these returns shift weights away from equities and toward bonds relative to market-cap weights — moderately, avoiding the extreme corner solutions that raw MVO produces (compare Example 1). Note that views are always evaluated relative to what equilibrium already implies, not in isolation.

## Common Pitfalls
- MVO is highly sensitive to expected return inputs and has been called an "error maximizer" — small changes in returns produce large changes in weights
- Unconstrained MVO often produces extreme, concentrated positions — always add constraints (long-only, max weight, turnover limits)
- Black-Litterman requires the analyst to specify confidence in views (Omega), which is itself uncertain
- Risk parity portfolios require leverage to achieve equity-like returns, introducing borrowing costs and leverage risk
- Ignoring implementation costs: transaction costs, bid-ask spreads, and taxes can significantly erode theoretical optimal returns
- Ignoring liquidity constraints: some asset classes (private equity, real estate) cannot be rebalanced quickly
- Glide paths assume a generic investor — individual circumstances may require customization
- Over-reliance on historical covariance matrices that may not reflect future relationships

## Cross-References
- **historical-risk** (wealth-management plugin): volatility and correlation inputs for mean-variance optimization
- **forward-risk** (wealth-management plugin): expected return forecasts and scenario analysis for portfolio optimization
- **diversification** (wealth-management plugin): diversification principles underpin all allocation frameworks
- **bet-sizing** (wealth-management plugin): position sizing within the allocated asset classes
- **rebalancing** (wealth-management plugin): maintaining allocation targets over time
- **quantitative-valuation** (wealth-management plugin): valuation signals can inform TAA decisions
- **retirement-decumulation** (wealth-management plugin): decumulation-phase glide paths and the sequence-of-returns risk that allocation choices must manage
- **factor-investing** (wealth-management plugin): sizing factor tilts as deliberate, survivable deviations from the policy portfolio
## Running the Script

```bash
uv run scripts/asset_allocation.py            # run the demo (uses PEP 723 inline deps)
uv run scripts/asset_allocation.py --verify   # check demo outputs against the worked examples (exit 1 on mismatch)
python3 scripts/asset_allocation.py            # alternative (requires: pip install numpy scipy)
```

The demo prints the calculations covered above; its values match the worked examples in this skill. Run `--help` for a list of the classes and functions. For programmatic use, import the module rather than running it — the demo only executes under `python asset_allocation.py`.
````

## Evaluation Dimensions

### 1. Skill Metadata Completeness
- [ ] YAML frontmatter has `name` (`asset-allocation`) and a detailed quoted `description`
- [ ] `description` enumerates frameworks (MVO, Black-Litterman, risk parity, glide paths) and natural-language triggers ("60/40 portfolio", "how much in stocks vs bonds")
- [ ] No in-file `license`, but the repository LICENSE is MIT

### 2. Trigger Condition Clarity
- [ ] `description` states concrete "when to use" questions and quoted phrasings
- [ ] Trigger vocabulary covers both technical and lay users
- [ ] Scope is portfolio allocation, distinct from single-asset trading or tax filing

### 3. Instruction Structure
- [ ] Clear hierarchy: Core Concepts → Key Formulas → Worked Examples → Common Pitfalls → Cross-References → Running the Script
- [ ] A formula reference table consolidating all expressions
- [ ] Cross-references to sibling skills make scope boundaries explicit

### 4. Example / Output Quality
- [ ] Two fully worked numeric examples (MVO and Black-Litterman) with intermediate covariance computations
- [ ] Interpretation notes explaining *why* the output looks the way it does (corner solutions, posterior tilts)
- [ ] A companion verification script (`--verify`) that checks the demo against the worked examples

### 5. Maintainability
- [ ] Companion script uses PEP 723 inline deps and a `--verify` self-check
- [ ] Cross-references a wider wealth-management plugin for inputs/outputs
- [ ] Explicit pitfalls list documents model limitations rather than overclaiming

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Skill Metadata Completeness | 15% | | |
| Trigger Condition Clarity | 20% | | |
| Instruction Structure | 25% | | |
| Example / Output Quality | 25% | | |
| Maintainability | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. "How should I split $500k across stocks and bonds for a 40-year-old?"; verify it applies SAA/glide-path reasoning and states assumptions
2. "Compare a 60/40 portfolio with a risk-parity approach"; verify it explains the trade-offs (leverage, volatility targets)
3. "Use Black-Litterman with my view that int'l will beat bonds"; verify it describes the equilibrium-vs-view comparison rather than treating the view in isolation

### Boundary Test Cases
1. Inputs with no risk aversion stated; verify the skill surfaces the sensitivity to inputs and asks for assumptions
2. A request involving illiquid assets (private equity, real estate); verify it flags rebalancing/liquidity constraints
3. A retail investor with no defined liabilities; verify it steers away from LDI/ALM framing

### Negative Test Cases
1. Whether it presents MVO output as a definitive "optimal" portfolio without the corner-solution caveat
2. Whether it invents specific expected returns not provided by the user
3. Whether it gives personalized investment advice without the "educational, not advice" framing

## Notes
- End-user financial-services artifact authored as a Markdown SKILL.md; the body is concepts, formulas, and worked examples plus an optional companion script.
- MIT license permits verbatim reproduction.
- The repository is a Claude Code plugin library (7 domain plugins, 80+ skills under `plugins/*/skills/*/SKILL.md`); this case captures only `plugins/wealth-management/skills/asset-allocation/SKILL.md`.
- The repository includes an eval workspace (`finance-skills-workspace/`) with graded runs; this case captures the skill artifact only.
