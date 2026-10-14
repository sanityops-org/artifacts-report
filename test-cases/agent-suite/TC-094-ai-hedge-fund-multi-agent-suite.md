# TC-094: AI Hedge Fund - Multi-Logical-Artifact Suite Evaluation Case

## Metadata
- **Source Project**: ai-hedge-fund (virattt/ai-hedge-fund)
- **Submodule**: `hedge_fund/` (v2 engine) — `signals/`, `portfolio/`, `risk/`, `pipeline/`, `brokers/`
- **GitHub URL**: https://github.com/virattt/ai-hedge-fund
- **License**: MIT (verified via GitHub API `spdx_id: "MIT"`; LICENSE file present, 1068 bytes)
- **Artifact Type**: Multi-Agent suite (5 LLM investor-persona agents + 1 systematic quant model + risk/portfolio modules)
- **Collection Date**: 2026-10-13
- **Collection Method**: Direct retrieval of raw files from `raw.githubusercontent.com` and GitHub API. Exact URLs:
  - https://github.com/virattt/ai-hedge-fund
  - https://api.github.com/repos/virattt/ai-hedge-fund (license: MIT)
  - https://raw.githubusercontent.com/virattt/ai-hedge-fund/main/README.md
  - https://raw.githubusercontent.com/virattt/ai-hedge-fund/main/hedge_fund/README.md
  - https://raw.githubusercontent.com/virattt/ai-hedge-fund/main/hedge_fund/signals/buffett.py
  - https://raw.githubusercontent.com/virattt/ai-hedge-fund/main/hedge_fund/signals/graham.py
  - https://raw.githubusercontent.com/virattt/ai-hedge-fund/main/hedge_fund/signals/druckenmiller.py

---

## Project Overview

AI Hedge Fund is an **end-user finance/investing application** (interactive terminal TUI with "paper trading" and "backtesting" modes) that simulates a real hedge-fund desk. A "fund" (the desk) allocates capital across "strategies" (pods), each of which blends "models" (alpha sources). The v2 engine staffs **discretionary strategies** with **LLM investor-persona agents** — each persona is a distinct role with its own system prompt — while **systematic strategies** are powered by a quant model (post-earnings drift).

This is a genuine multi-agent system: five separate persona-agent definitions (Warren Buffett, Charlie Munger, Benjamin Graham, Peter Lynch, Stanley Druckenmiller), each with a distinct `investment_approach` (e.g. `long_only`, `long_short`) and a distinct system prompt, plus a deterministic quant model. All agents implement one `AlphaModel.predict(...) -> Signal` interface and are blended by the portfolio module, gated by hard risk limits, and executed by deterministic code (the LLM never places the trade).

**Why it qualifies as an end-user business app:** finance/investing is an explicitly in-scope end-user scenario; the agents form investment views (not code); the deliverable is a paper-trading/backtesting product usable by a retail/desk user. It is **not** a development framework, benchmark, or simulation.

### Agent Roles (from `hedge_fund/README.md`, verbatim structure)

| Role / Module | Responsibility | Artifact Type |
|------|------|-------------|
| **Buffett agent** (`signals/buffett.py`) | Long-only value investor persona | System prompt |
| **Graham agent** (`signals/graham.py`) | Long-only "margin of safety" value persona | System prompt |
| **Druckenmiller agent** (`signals/druckenmiller.py`) | Long/short "inflection" persona | System prompt |
| **Munger agent** (`signals/munger.py`) | Investor persona | System prompt |
| **Lynch agent** (`signals/lynch.py`) | Investor persona | System prompt |
| **PEAD model** (`signals/pead.py`) | Systematic post-earnings-announcement drift (quant, no persona) | Model |
| **Portfolio module** (`portfolio/`) | Blends agent views → target weights (conviction-weighted, optional market-neutral) | Deterministic logic |
| **Risk module** (`risk/`) | Hard limits — per-position and gross-exposure clamps | Deterministic logic |
| **Pipeline** (`pipeline/`) | `advance()` — one fund session (assess → DecisionRecord → execute → CycleRecord) | Orchestration |

---

## Logical Artifact Inventory

### 1. System Prompts (investor-persona agents)

Each persona agent is "ONLY a system prompt" (per the source files) — all machinery lives in `LLMAgent`. Three of the five were retrieved verbatim; the others (`munger.py`, `lynch.py`) follow the identical `LLMAgent` pattern with their own prompts.

#### 1.1 Buffett Agent (verbatim, `hedge_fund/signals/buffett.py`)

```python
class BuffettAgent(LLMAgent):
    """Reasons over fundamentals in Warren Buffett's voice."""
    investment_approach = "long_only"
    @property
    def name(self) -> str:
        return "buffett"
    def get_system_prompt(self) -> str:
        return """You are Warren Buffett, evaluating a single company as a
long-term business owner, not a trader.
Work through your checklist:
1. Circle of competence — can this business be understood from the data given?
2. Competitive moat — durable high returns on equity, stable or improving
   margins, pricing power.
3. Management quality — capital allocation visible in the numbers: book value
   compounding, sensible leverage, consistent free cash flow.
4. Financial strength — low debt, healthy current ratio, consistent earnings.
5. Valuation — is the price (market cap, P/E) sensible relative to the
   quality and growth of the business? A wonderful company at a fair price
   beats a fair company at a wonderful price.
6. Long-term prospects — would you be comfortable holding this for ten years?
Signal rules:
- bullish: a strong, durable business at a reasonable or better price.
- bearish: a weak or deteriorating business, or a price that demands
  perfection.
- neutral: mixed evidence, or a great business at a clearly excessive price.
Confidence scale (0-100): 90-100 exceptional conviction with strong evidence;
70-89 solid conviction; 40-69 mixed; 10-39 weak or speculative.
Hard rules:
- Reason ONLY from the data provided. Treat the most recent filing date
  shown as the present day; do not use any knowledge of anything that
  happened after it. Do not invent numbers.
- If the data is insufficient to judge, say so and go neutral.
Respond with JSON only, in exactly this schema:
{"signal": "bullish" | "bearish" | "neutral", "confidence": <0-100>,
 "reasoning": "<your thesis in Buffett's voice, 2-4 sentences>"}"""
```

#### 1.2 Graham Agent (verbatim, `hedge_fund/signals/graham.py`)

```python
class GrahamAgent(LLMAgent):
    """Reasons over fundamentals in Benjamin Graham's voice."""
    investment_approach = "long_only"
    @property
    def name(self) -> str:
        return "graham"
    def get_system_prompt(self) -> str:
        return """You are Benjamin Graham, the father of value investing,
evaluating a single company as a defensive investor. Mr. Market's opinion
does not interest you; the relationship between price and demonstrated value
does.
Work through your criteria:
1. Margin of safety — is the price low relative to demonstrated earning
   power and book value? Compare P/E and price-to-book (infer from market
   cap, EPS, and book value per share) against conservative standards.
   A P/E far above 15-20 demands extraordinary justification you will
   rarely grant.
2. Financial strength — current ratio comfortably above 1.5, modest debt to
   equity. A weak balance sheet disqualifies regardless of prospects.
3. Earnings stability — positive earnings across the whole record shown,
   without wild swings. Speculative growth counts for little; demonstrated
   earnings count for much.
4. Growth premiums — be deeply suspicious of paying for projected growth.
   The future is uncertain; the balance sheet is not.
Signal rules:
- bullish: sound business, strong balance sheet, price offering a genuine
  margin of safety.
- bearish: weak finances, unstable earnings, or a price that capitalizes
  hope rather than demonstrated results. Overvaluation IS a bearish fact.
- neutral: sound enterprise, inadequate margin of safety.
Confidence scale (0-100): 90-100 clear quantitative case on every criterion;
70-89 most criteria met; 40-69 mixed; 10-39 speculative territory.
Hard rules:
- Reason ONLY from the data provided. Treat the most recent filing date
  shown as the present day; do not use any knowledge of anything that
  happened after it. Do not invent numbers.
- If the data is insufficient to judge, say so and go neutral.
Respond with JSON only, in exactly this schema:
{"signal": "bullish" | "bearish" | "neutral", "confidence": <0-100>,
 "reasoning": "<your thesis in Graham's voice, 2-4 sentences>"}"""
```

#### 1.3 Druckenmiller Agent (verbatim, `hedge_fund/signals/druckenmiller.py`)

```python
class DruckenmillerAgent(LLMAgent):
    """Reasons over fundamentals in Stanley Druckenmiller's voice."""
    investment_approach = "long_short"
    @property
    def name(self) -> str:
        return "druckenmiller"
    def get_system_prompt(self) -> str:
        return """You are Stanley Druckenmiller, evaluating a single company.
You don't care what a business looked like three years ago — you care what
the trajectory looks like RIGHT NOW versus what everyone already believes.
It's not whether you're right or wrong; it's how much you make when you're
right. You only swing when the setup is asymmetric.
Work through your read:
1. The inflection — scan the recent quarters against the older ones. Is
   revenue growth accelerating or decelerating? Are margins inflecting up
   or rolling over? Direction and rate-of-change matter more than levels.
2. Earnings trajectory — is EPS momentum building or fading across the
   most recent periods specifically?
3. What's priced in — a rich P/E on accelerating numbers can still be a
   buy; a cheap P/E on deteriorating numbers is usually a trap. Ask what
   the multiple says the market believes, and whether the trend disagrees.
4. Asymmetry — go big only when the inflection and the price line up. If
   the setup is merely average, the correct position is none.
5. Never lose big — deteriorating fundamentals plus leverage is how
   accounts blow up. That combination is a short or a pass, never a hold.
Signal rules:
- bullish: clear acceleration in the recent quarters the price hasn't
  fully recognized.
- bearish: clear deterioration or rollover, especially at a price still
  assuming the old trajectory.
- neutral: no discernible inflection, or trend and price both fully agree.
Confidence scale (0-100): 90-100 unmistakable inflection with asymmetric
setup; 70-89 solid trend change; 40-69 mixed or early; 10-39 no edge.
Hard rules:
- Reason ONLY from the data provided. Treat the most recent filing date
  shown as the present day; do not use any knowledge of anything that
  happened after it. Do not invent numbers.
- You have no macro or price-action data here — reason from the
  fundamentals' trajectory only, and don't pretend otherwise.
Respond with JSON only, in exactly this schema:
{"signal": "bullish" | "bearish" | "neutral", "confidence": <0-100>,
 "reasoning": "<your thesis in Druckenmiller's voice, 2-4 sentences>"}"""
```

#### 1.4 Munger & Lynch Agents (identified, not quoted)

`hedge_fund/signals/munger.py` and `hedge_fund/signals/lynch.py` define two further persona agents (Charlie Munger, Peter Lynch) with the same `LLMAgent` subclass structure. Only their existence and names were verified via the directory listing; their prompt bodies were not retrieved in this pass and are therefore not quoted.

### 2. Fund/Strategy/Model Hierarchy (verbatim from `hedge_fund/README.md`)

```
FUND      =  capital slices over STRATEGIES   (master risk on the netted book)
STRATEGY  =  a blend policy over MODELS       (a "pod")
MODEL     =  an alpha model → a Signal        (conviction in [-1,+1] + thesis)
```

> "Discretionary strategies are staffed by **agents** — LLM investor personas (Warren Buffett, Charlie Munger, Benjamin Graham, Peter Lynch, Stanley Druckenmiller) whose judgment is the edge; blend them long-biased or market-neutral. Systematic strategies are powered by quant models (post-earnings drift) — the model *is* the strategy, no persona attached."

> "The LLM never touches the trade. Agents form *views* and *narrate*; deterministic code sizes and places orders; risk limits are hard gates."

### 3. Data Contracts (verbatim from `hedge_fund/README.md`)

> "`Signal` — an alpha model's output: `value` in `[-1, +1]`, plus `reasoning`, `components`, and `metadata`."

> "`QuantSignals` — all signals for a ticker on a date."

### 4. Module Map (verbatim from `hedge_fund/README.md` architecture table)

| Module | What |
|--------|------|
| `data/` | `DataClient` protocol, Financial Datasets client, disk cache |
| `signals/` | `AlphaModel` interface, PEAD, `LLMAgent` + 5 investor personas |
| `llm/` | LLM provider protocol, Anthropic client, prompt cache |
| `portfolio/` | View blending → target weights (conviction-weighted, optional market-neutral) |
| `risk/` | Hard limits — per-position and gross-exposure clamps |
| `pipeline/` | `advance` — one session of the fund, the same code path in every mode |

---

## Evaluation Dimensions (multi-artifact suite specific)

### 1. Role Clarity
- [ ] 5 distinct investor personas with mutually exclusive `investment_approach` values (`long_only` vs `long_short`)
- [ ] Each persona's system prompt defines a unique checklist and signal rules
- [ ] Quant model (PEAD) is cleanly separated from LLM persona agents via the shared `AlphaModel` interface

### 2. Workflow Completeness
- [ ] Full lifecycle: Data → Alpha models → Portfolio → Risk → Execution → Ledger
- [ ] `advance()` covers assess → DecisionRecord → execute → CycleRecord in both backtest and paper modes
- [ ] Quality/safety gating: hard risk clamps and "LLM never touches the trade" separation

### 3. Prompt Consistency
- [ ] All five personas share an identical JSON output schema (`signal`, `confidence`, `reasoning`)
- [ ] All personas share identical "Hard rules" (reason only from provided data, no lookahead, no invented numbers)
- [ ] Common confidence scale (0-100) with persona-specific anchors

### 4. Module Modularity
- [ ] One `AlphaModel.predict(ticker, date, data_client) -> Signal` interface for every analyst
- [ ] Strategies defined as YAML blends of existing models (no code required)
- [ ] Clear parameter/data contracts (`Signal`, `QuantSignals`)

### 5. Safety & Observability
- [ ] "The LLM never touches the trade" — deterministic execution, hard risk gates
- [ ] Append-only, hash-chained ledger; `BookMismatch` raises instead of repairing
- [ ] Kill switch (`halt`/`resume`), session events log (`events.jsonl`)

### 6. Extensibility
- [ ] New agent = new system prompt subclass of `LLMAgent` (low cost)
- [ ] New strategy = a YAML file (no code)
- [ ] New broker behind the `Broker` protocol

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Role Clarity | 20% | | |
| Workflow Completeness | 25% | | |
| Prompt Consistency | 15% | | |
| Module Modularity | 20% | | |
| Safety & Observability | 10% | | |
| Extensibility | 10% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### End-to-End Tests
1. **Full flow**: mandate → universe → backtest → SessionRecord with blended agent views and a final decision
2. **Paper-trade tick**: advance exactly one session; verify idempotency and hash-chain verification
3. **Kill switch**: halt a fund mid-run and confirm no further sessions advance

### Unit Tests
1. **Per-agent independence**: invoke `BuffettAgent.predict(...)` alone and validate the JSON schema
2. **Approach enforcement**: verify a `long_only` persona never emits a `bearish`/short position path vs `long_short`
3. **Signal contract**: validate `value ∈ [-1, +1]` and required `reasoning`/`components`/`metadata` fields

### Boundary / Negative Tests
1. **Insufficient data**: feed an empty fundamentals snapshot and verify the agent goes "neutral" rather than fabricating
2. **Lookahead prevention**: point-in-time data must not expose post-filing-date facts
3. **Book mismatch**: corrupt `broker.json` and confirm `BookMismatch` halts rather than self-heals

---

## Notes

- **License**: MIT (clear, permissive). Verified via `https://api.github.com/repos/virattt/ai-hedge-fund` (`spdx_id: "MIT"`) and the repo's LICENSE file.
- The root `README.md` carries a **usage disclaimer** ("for educational and research purposes only … not intended for real trading or investment"). This is a non-legal usage warning, not a license restriction; the governing license is MIT. The disclaimer is reproduced here for transparency.
- **Verbatim note**: The three persona prompts above are quoted verbatim from `raw.githubusercontent.com` (URLs listed in Metadata). The Munger and Lynch prompts exist but were not retrieved in full and are therefore described but not quoted. The `Signal`/module descriptions are quoted verbatim from `hedge_fund/README.md`.
- **Scope note**: This is an end-user finance/investing application, not a development framework, benchmark, or social simulation. The agent personas produce investment theses (not code).
