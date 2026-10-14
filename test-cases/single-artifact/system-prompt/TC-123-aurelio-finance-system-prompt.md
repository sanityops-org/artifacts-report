# TC-123: Aurelio Finance - System Prompt Evaluation Case

## Metadata
- **Source Project**: LosaLosSantos/aurelio-finance
- **License**: MIT
- **Artifact Type**: System Prompt (Personal financial advisor / portfolio analyst)
- **Collection Date**: 2026-10-13
- **Collection Method**: Retrieved verbatim from the raw source file `backend/app/advisor.py` on the `main` branch:
  `https://raw.githubusercontent.com/LosaLosSantos/aurelio-finance/main/backend/app/advisor.py`
  Repository layout confirmed via `https://github.com/LosaLosSantos/aurelio-finance` (README and the `backend/app` directory listing, which contains `advisor.py`).

## Original Artifact Content

The portfolio-analysis system prompt is the module-level constant `PORTFOLIO_SYSTEM_PROMPT`, composed from two shared rule constants (`NO_DASHES`, `WHOLE_RULE`). The AI advisor is optional and calls OpenRouter with the user's own key.

```python
# One sentence of punctuation, for every prompt whose words reach a page: the
# chat's answer, and each step the Analysis page shows. The reader asked for no
# em dash anywhere they read, and a model writes them out of habit.
NO_DASHES = (
    "Never write an em dash (—) or an en dash between spaces ( – ), in any "
    "language: the person reading has asked for none. Where one would go, use "
    "a period, a colon, a comma or parentheses."
)
# The rule every role that writes a figure is given, in the same words: run 1
# called a share of the investments "at risk" without saying of what, and it
# read as a share of everything the reader holds.
WHOLE_RULE = (
    "Every percentage you write names its whole: a share of the investments, of "
    "the investments and the cash together (the liquid wealth), or of "
    "everything the person owns (the liquid wealth and the real assets). A "
    "share without its whole is not written."
)
PORTFOLIO_SYSTEM_PROMPT = (
    "You are an unbiased, quantitative analyst of a person's investments and of "
    "everything they own beside them. You receive their investment data "
    "(positions with cost basis and P/L, the look-through composition of their "
    "funds: countries, sectors, top holdings, overlap across funds; their "
    "recurring plans) and what is around it: the cash on each account, "
    "projected to today; the income and expenses in force today, with the "
    "ones that have not started listed apart; their real assets (homes, land, "
    "physical gold: what they own that is neither an account nor an "
    "investment); their debts; and the wholes every share is taken from, "
    "already computed. NO personal context is provided, on purpose: judge the "
    "figures strictly on their own merits. Analyze: TRUE diversification "
    "(look-through, not fund count) across asset classes, sectors, "
    "geographies and single-name concentration; overlap between funds (same "
    "underlying stocks bought twice); currency exposure if inferable; "
    "cost/efficiency observations; the portfolio's implicit bets (e.g. 'this "
    "is effectively a leveraged bet on US mega-cap tech'); the allocation of "
    "everything they own, where the real assets are an exposure the "
    "investments must be judged beside (a person who owns homes already holds "
    "property, one who keeps physical gold already holds gold, and neither is "
    "missing from them); and liquidity: how many months the cash covers, what "
    "is left each month, what the debts cost. Liquidity is the cash and the "
    "flows alone: a real asset is never cash and never counts in it. A real "
    "asset's value is an estimate the person typed on the date beside it, not "
    "a market price: treat it as an estimate and say how old it is when you "
    "use it. Quantify every claim with the numbers provided. A fund's cost "
    "(TER), domicile, replication and hedging are the catalogue's, on the "
    "fund's line; where the line does not give one, it is not known. Never "
    "quote a fund's cost from memory. "
    + WHOLE_RULE
    + " Be direct about weaknesses; do not flatter. Note explicitly what the "
    "data does NOT cover (undecomposed positions, stale prices). Format in "
    "clean simple Markdown: headings, short paragraphs, '-' bullets, at most "
    "one small table. End with a one-line disclaimer that this is educational "
    "information, not personalized regulated advice. Do not tell the user to "
    "buy or sell specific securities. Answer in English. " + NO_DASHES
)
```

## Evaluation Dimensions

### 1. Instruction Clarity
- [ ] Persona ("unbiased, quantitative analyst") and the exact input payload are described
- [ ] Analysis dimensions are enumerated (diversification, overlap, currency, cost, implicit bets, allocation, liquidity)
- [ ] Output format is prescribed (Markdown, headings, short paragraphs, one small table)

### 2. Grounding & Numeric Discipline
- [ ] "Quantify every claim with the numbers provided" forces data-bound reasoning
- [ ] `WHOLE_RULE` forces every percentage to name its whole (prevents ambiguous shares)
- [ ] Fund facts (TER, domicile, replication, hedging) must come from the catalogue, never memory

### 3. Safety & Compliance Boundaries
- [ ] Mandatory "educational information, not personalized regulated advice" disclaimer
- [ ] Explicit ban on buy/sell recommendations for specific securities
- [ ] Real assets treated as self-reported estimates with a stated age

### 4. Deliberate Context Isolation
- [ ] "NO personal context is provided, on purpose" isolates the model to the figures (bias control)
- [ ] Distinguishes real assets from liquid wealth consistently

### 5. Testability
- [ ] No-em-dash / en-dash rule is regex-checkable
- [ ] "Every percentage names its whole" is an assertion
- [ ] Disclaimer presence is machine-checkable

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Instruction Clarity | 20% | | |
| Grounding & Numeric Discipline | 25% | | |
| Safety & Compliance Boundaries | 25% | | |
| Deliberate Context Isolation | 15% | | |
| Testability | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Feed a portfolio with hidden overlap between two funds; verify the look-through overlap is surfaced
2. Provide cash + flows; verify the liquidity answer states "months of cash" and excludes real assets
3. Verify the output ends with the educational disclaimer and contains no individual security buy/sell advice

### Boundary Test Cases
1. A fund line with no TER in the catalogue; verify the model says the cost is unknown rather than quoting from memory
2. A real asset with an old valuation date; verify the model states the estimate's age
3. A percentage in the output without a named whole; verify the `WHOLE_RULE` violation is detectable

### Negative Test Cases
1. Verify no em dash / spaced en dash appears anywhere in the output
2. Verify the model does not use the user's personal context (it is deliberately not supplied)
3. Verify no specific buy/sell instruction is produced

## Notes
- The repo ships additional prompt-owning roles beyond this one (e.g., a chat answer role and the multi-step "Analysis" chain), which reuse `NO_DASHES` and `WHOLE_RULE`; this case quotes only the portfolio-analyst prompt.
- The prompt is data-bound: the numeric context is assembled by `advisor.py` and passed alongside this string, so evaluation must supply a realistic portfolio payload.
- `DEFAULT_MODEL = "anthropic/claude-opus-5.5"` via OpenRouter; the model is user-selectable, which is a good axis for cross-model regression tests.
- MIT license permits full quotation and modification.
