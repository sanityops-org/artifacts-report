# TC-161: tradermonty/claude-trading-skills (Position Sizer) - Skill Evaluation Case

## Metadata
- **Source Project**: tradermonty/claude-trading-skills
- **License**: MIT (GitHub API reports `spdx_id: MIT`; LICENSE file present)
- **Artifact Type**: Skill (SKILL.md)
- **Collection Date**: 2026-10-14
- **Collection Method**: Fetched verbatim from https://raw.githubusercontent.com/tradermonty/claude-trading-skills/HEAD/skills/position-sizer/SKILL.md (resolved default branch). Repository README: https://raw.githubusercontent.com/tradermonty/claude-trading-skills/HEAD/README.md . License file: https://raw.githubusercontent.com/tradermonty/claude-trading-skills/HEAD/LICENSE

## Original Artifact Content

````markdown
---
name: position-sizer
description: Calculate risk-based position sizes for long stock trades. Use when user asks about position sizing, how many shares to buy, risk per trade, Kelly criterion, ATR-based sizing, fractional-share sizing, or portfolio risk allocation. Supports stop-loss distance calculation, volatility scaling, and sector concentration checks.
---

# Position Sizer

## Overview

Calculate the optimal number of shares to buy for a long stock trade based on risk management principles. Supports three sizing methods:

- **Fixed Fractional**: Risk a fixed percentage of account equity per trade (default: 1%)
- **ATR-Based**: Use Average True Range to set volatility-adjusted stop distances
- **Kelly Criterion**: Calculate mathematically optimal risk allocation from historical win/loss statistics

All methods apply portfolio constraints (max position %, max sector %) and output a final recommended share count with full risk breakdown. The default output is whole shares. Use `--fractional` only when the user's broker supports fractional shares for the security and order type.

## When to Use

- User asks "how many shares should I buy?"
- User wants to calculate position size for a specific trade setup
- User mentions risk per trade, stop-loss sizing, or portfolio allocation
- User asks about Kelly Criterion or ATR-based position sizing
- User has a small account where whole-share rounding would under-deploy a defined risk budget
- User wants to check if a position fits within portfolio concentration limits

## Prerequisites

- No API keys required
- Python 3.9+ with standard library only

## Workflow

### Step 1: Gather Trade Parameters

Collect from the user:
- **Required**: Account size (total equity)
- **Mode A (Fixed Fractional)**: Entry price, stop price, risk percentage (default 1%)
- **Mode B (ATR-Based)**: Entry price, ATR value, ATR multiplier (default 2.0x), risk percentage
- **Mode C (Kelly Criterion)**: Win rate, average win, average loss; optionally entry and stop for share calculation
- **Optional constraints**: Max position % of account, max sector %, current sector exposure
- **Optional share mode**: Whole shares by default, or fractional shares with `--fractional --share-precision N` when supported by the broker

If the user provides a stock ticker but not specific prices, use available tools to look up the current price and suggest entry/stop levels based on technical analysis.

### Step 2: Execute Position Sizer Script

Run the position sizing calculation:

```bash
# Fixed Fractional (most common)
python3 skills/position-sizer/scripts/position_sizer.py \
  --account-size 100000 \
  --entry 155 \
  --stop 148.50 \
  --risk-pct 1.0 \
  --output-dir reports/

# Fractional shares for small accounts or high-priced stocks
python3 skills/position-sizer/scripts/position_sizer.py \
  --account-size 1000 \
  --entry 155 \
  --stop 148.50 \
  --risk-pct 1.0 \
  --fractional \
  --share-precision 4 \
  --output-dir reports/

# ATR-Based
python3 skills/position-sizer/scripts/position_sizer.py \
  --account-size 100000 \
  --entry 155 \
  --atr 3.20 \
  --atr-multiplier 2.0 \
  --risk-pct 1.0 \
  --output-dir reports/

# Kelly Criterion (budget mode - no entry)
python3 skills/position-sizer/scripts/position_sizer.py \
  --account-size 100000 \
  --win-rate 0.55 \
  --avg-win 2.5 \
  --avg-loss 1.0 \
  --output-dir reports/

# Kelly Criterion (shares mode - with entry/stop)
python3 skills/position-sizer/scripts/position_sizer.py \
  --account-size 100000 \
  --entry 155 \
  --stop 148.50 \
  --win-rate 0.55 \
  --avg-win 2.5 \
  --avg-loss 1.0 \
  --output-dir reports/
```

### Step 3: Load Methodology Reference

Read `references/sizing_methodologies.md` to provide context on the chosen method, risk guidelines, and portfolio constraint best practices.

### Step 4: Calculate Multiple Scenarios

If the user has not specified a single method, run multiple scenarios for comparison:
- Fixed Fractional at 0.5%, 1.0%, and 1.5% risk
- ATR-based at 1.5x, 2.0x, and 3.0x multipliers
- Present a comparison table showing shares, position value, and dollar risk for each

### Step 5: Apply Portfolio Constraints and Determine Final Size

Add constraints if the user has portfolio context:

```bash
python3 skills/position-sizer/scripts/position_sizer.py \
  --account-size 100000 \
  --entry 155 \
  --stop 148.50 \
  --risk-pct 1.0 \
  --max-position-pct 10 \
  --max-sector-pct 30 \
  --current-sector-exposure 22 \
  --output-dir reports/
```

Explain which constraint is binding and why it limits the position.

### Step 6: Generate Position Report

Present the final recommendation including:
- Method used and rationale
- Exact share count and position value
- Dollar risk and percentage of account
- Stop-loss price
- Any binding constraints
- Risk management reminders (portfolio heat, loss-cutting discipline)
- Small-account reminders: fractional shares do not remove broker minimums, spread/slippage, commissions/fees, margin limits, borrow availability, or day-trading controls

## Output Format

### JSON Report

```json
{
  "schema_version": "1.0",
  "mode": "shares",
  "parameters": {
    "entry_price": 155.0,
    "account_size": 100000,
    "stop_price": 148.50,
    "risk_pct": 1.0
  },
  "calculations": {
    "fixed_fractional": {
      "method": "fixed_fractional",
      "shares": 153,
      "risk_per_share": 6.50,
      "dollar_risk": 1000.0,
      "stop_price": 148.50
    },
    "atr_based": null,
    "kelly": null
  },
  "constraints_applied": [],
  "final_recommended_shares": 153,
  "final_position_value": 23715.0,
  "final_risk_dollars": 994.50,
  "final_risk_pct": 0.99,
  "binding_constraint": null
}
```

### Markdown Report

Generated automatically alongside the JSON report. Contains:
- Parameters summary
- Calculation details for the active method
- Constraints analysis (if any)
- Final recommendation with shares, value, and risk

Reports are saved to `reports/` with filenames `position_sizer_YYYY-MM-DD_HHMMSS.json` and `.md`.

## Resources

- `references/sizing_methodologies.md`: Comprehensive guide to Fixed Fractional, ATR-based, and Kelly Criterion methods with examples, comparison table, and risk management principles
- `scripts/position_sizer.py`: Main calculation script (CLI interface)

## Key Principles

1. **Survival first**: Position sizing is about surviving losing streaks, not maximizing winners
2. **The 1% rule**: Default to 1% risk per trade; never exceed 2% without exceptional reason
3. **Default to whole shares**: Existing workflows remain integer-share by default
4. **Floor, never round up**: Whole-share mode floors to an integer; fractional mode floors to the requested precision so risk and concentration budgets are not exceeded
5. **Strictest constraint wins**: When multiple limits apply, the tightest one determines final size
6. **Half Kelly**: Never use full Kelly in practice; half Kelly captures 75% of growth with far less risk
7. **Portfolio heat**: Total open risk should not exceed 6-8% of account equity
8. **Intraday rules are broker-specific**: FINRA replaced the old pattern-day-trader day-count and $25,000 minimum-equity requirements with intraday margin standards effective 2026-06-04, with broker phase-in allowed through 2027-10-20. Check the broker's current rules before repeated same-day trading in a margin account.
9. **Asymmetry of losses**: A 50% loss requires a 100% gain to recover; size accordingly
````

## Evaluation Dimensions

### 1. Skill Metadata Completeness
- [ ] YAML frontmatter contains the required `name` field (`position-sizer`)
- [ ] `description` states trigger conditions (position sizing, how many shares, Kelly, ATR, risk allocation)
- [ ] No in-file `license`, but the repository LICENSE is MIT

### 2. Trigger Condition Clarity
- [ ] A `## When to Use` section lists concrete user phrasings
- [ ] `description` enumerates the supported methods and features
- [ ] Scope boundaries implied by "long stock trades" and broker-support caveats

### 3. Instruction Structure
- [ ] Numbered 6-step workflow from parameter gathering to report generation
- [ ] Separate Overview / Prerequisites / Output Format / Key Principles sections
- [ ] Clear three-method decomposition (Fixed Fractional, ATR, Kelly)

### 4. Example / Output Quality
- [ ] Runnable CLI examples for every method
- [ ] Complete JSON output schema and Markdown report description
- [ ] Quantitative key principles with hard numbers (1%, 6-8% heat, half Kelly)

### 5. Maintainability
- [ ] External dependencies clearly stated (Python 3.9+, standard library only, no API keys)
- [ ] References a companion methodology file (`references/sizing_methodologies.md`)
- [ ] Regulatory note dated (FINRA intraday margin standard effective 2026-06-04) for future review

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
1. "How many shares of a $155 stock should I buy with a $148.50 stop on a $100k account?"; verify fixed-fractional sizing
2. "Size this trade with ATR 3.20 and a 2x multiplier"; verify ATR-based sizing
3. "What size does half Kelly suggest with 55% win rate?"; verify Kelly handling and half-Kelly caution

### Boundary Test Cases
1. A small account where whole-share rounding under-deploys risk; verify it offers `--fractional`
2. Sector exposure near the cap; verify it reports the binding constraint
3. A ticker without given prices; verify it looks up or asks rather than guessing silently

### Negative Test Cases
1. Whether a short-trade or options request triggers this long-only skill incorrectly
2. Whether it ever recommends full Kelly
3. Whether it rounds *up* share counts past the risk budget

## Notes
- End-user investing/risk-management artifact from a Claude Skills-based trading toolkit for individual investors.
- The SKILL.md embeds CLI calls and a JSON output schema; the actual arithmetic lives in `scripts/position_sizer.py`.
- MIT license permits verbatim reproduction.
- Distinct from TC-153 (joellewis finance asset-allocation) and TC-146 (alpha-insights): this is a single-trade risk-based position sizer.
