# TC-084: TradingAgents - Multi-Logical-Artifact Suite Evaluation Case

## Metadata
- **Source Project**: TauricResearch/TradingAgents (owner/repo: `TauricResearch/TradingAgents`)
- **GitHub URL**: https://github.com/TauricResearch/TradingAgents
- **License**: **Apache-2.0** (verified from `LICENSE`; note: the task brief stated "MIT", but the repository's real license file is Apache License 2.0 — see Notes)
- **Artifact Type**: Multi-Agent suite (11 role agents + 1 memory node, across 4 artifact types: System Prompts, Tool Schemas, Structured-Output Schemas, Orchestration Config)
- **Collection Date**: 2026-10-13
- **Collection Method**: Verbatim excerpts fetched from the project's public raw source files (branch `main`, TradingAgents v0.6.0). Exact URLs fetched:
  - https://raw.githubusercontent.com/TauricResearch/TradingAgents/main/tradingagents/agents/analysts/market_analyst.py
  - https://raw.githubusercontent.com/TauricResearch/TradingAgents/main/tradingagents/agents/analysts/news_analyst.py
  - https://raw.githubusercontent.com/TauricResearch/TradingAgents/main/tradingagents/agents/analysts/fundamentals_analyst.py
  - https://raw.githubusercontent.com/TauricResearch/TradingAgents/main/tradingagents/agents/analysts/sentiment_analyst.py
  - https://raw.githubusercontent.com/TauricResearch/TradingAgents/main/tradingagents/agents/analysts/social_media_analyst.py (legacy shim)
  - https://raw.githubusercontent.com/TauricResearch/TradingAgents/main/tradingagents/agents/researchers/bull_researcher.py
  - https://raw.githubusercontent.com/TauricResearch/TradingAgents/main/tradingagents/agents/managers/research_manager.py
  - https://raw.githubusercontent.com/TauricResearch/TradingAgents/main/tradingagents/agents/managers/portfolio_manager.py
  - https://raw.githubusercontent.com/TauricResearch/TradingAgents/main/tradingagents/agents/trader/trader.py
  - https://raw.githubusercontent.com/TauricResearch/TradingAgents/main/tradingagents/agents/risk_mgmt/aggressive_debator.py
  - https://raw.githubusercontent.com/TauricResearch/TradingAgents/main/tradingagents/agents/schemas.py
  - https://raw.githubusercontent.com/TauricResearch/TradingAgents/main/tradingagents/agents/tools.py
  - https://raw.githubusercontent.com/TauricResearch/TradingAgents/main/tradingagents/agents/state.py
  - https://raw.githubusercontent.com/TauricResearch/TradingAgents/main/tradingagents/graph/setup.py
  - https://raw.githubusercontent.com/TauricResearch/TradingAgents/main/tradingagents/graph/conditional_logic.py
  - https://raw.githubusercontent.com/TauricResearch/TradingAgents/main/tradingagents/default_config.py
  - https://github.com/TauricResearch/TradingAgents/blob/main/LICENSE

---

## Project Overview

TradingAgents is a **multi-agent LLM "trading firm" simulation**: a set of specialized LLM agents that debate and cooperate to produce a trading decision for a given instrument (stock or crypto) on a given trade date. It is a **non-coding, end-user-facing agent** — the user supplies a ticker and a date and reads a generated research report and final rating; no code is authored by the agents.

The system is orchestrated as a LangGraph state machine (`tradingagents/graph/setup.py`). The pipeline is:

1. **Analyst team** (runs concurrently) — Market, Sentiment, News, Fundamentals analysts each produce a report.
2. **Research debate** — a Bull Researcher and a Bear Researcher debate; the **Research Manager** (deep-thinking LLM) turns the debate into an investment plan.
3. **Trader** — converts the plan into a concrete transaction proposal (Buy/Hold/Sell with entry/stop/sizing).
4. **Risk debate** — an Aggressive, Conservative and Neutral risk analyst debate the trader's proposal.
5. **Portfolio Manager** (deep-thinking LLM) — synthesizes the risk debate into the final 5-tier rating.
6. **Memory Log** — a node that runs alongside the analysts, settles past decisions and supplies cross-ticker "lessons" to the Portfolio Manager.

Two model tiers are used: a **quick-thinking** LLM for analysts/researchers/debaters/trader and a **deep-thinking** LLM for the two managers (see `default_config.py`: `"quick_think_llm"` / `"deep_think_llm"`).

### Agent Roles

| Role | Responsibility | Primary Artifact Type |
|------|----------------|-----------------------|
| **Market Analyst** | Selects technical indicators and writes a market trend report | System Prompt + Tool Schema |
| **Sentiment Analyst** | Aggregates Yahoo news + StockTwits + Reddit into a sentiment band/score | System Prompt + Structured Schema |
| **News Analyst** | Analyzes company + macro news and prediction markets | System Prompt + Tool Schema |
| **Fundamentals Analyst** | Analyzes financial statements and insider transactions | System Prompt + Tool Schema |
| **Bull Researcher** | Argues the long case in the investment debate | System Prompt |
| **Bear Researcher** | Argues the short case in the investment debate | System Prompt |
| **Research Manager** | Judges the debate → structured investment plan | System Prompt + Structured Schema |
| **Trader** | Turns the plan into a transaction proposal | System Prompt + Structured Schema |
| **Aggressive Analyst** | High-risk risk-debate participant | System Prompt |
| **Neutral Analyst** | Balanced risk-debate participant | System Prompt |
| **Conservative Analyst** | Capital-preservation risk-debate participant | System Prompt |
| **Portfolio Manager** | Final synthesis → 5-tier rating decision | System Prompt + Structured Schema |
| **Memory Log** (node) | Settles past decisions; supplies lessons to the Portfolio Manager | Orchestration Config |

---

## Logical Artifact Inventory

> All excerpts below are **quoted verbatim** from the raw source files listed in the Metadata. Ellipses (`[...]`) mark omitted code; all quoted text is unmodified.

### 1. System Prompts / Role Definitions

#### 1.1 Market Analyst
```python
# tradingagents/agents/analysts/market_analyst.py
system_message = (
 """You are a trading assistant tasked with analyzing financial markets. Your role is to select the **most relevant indicators** for a given market condition or trading strategy from the following list. The goal is to choose up to **8 indicators** that provide complementary insights without redundancy. [...]
[...]
Before writing the final report, call get_verified_market_snapshot for this ticker and the current date, and treat it as the source of truth for any exact OHLCV, price-level, or indicator-value claim. If another tool's output conflicts with the verified snapshot, flag the discrepancy rather than inventing a reconciled number. [...]
Write a very detailed and nuanced report of the trends you observe. Provide specific, actionable insights with supporting evidence to help traders make informed decisions."""
 + """ Make sure to append a Markdown table at the end of the report to organize key points in the report, organized and easy to read."""
 + get_language_instruction()
 )
```
Shared collaboration preamble used by the tool-using analysts:
```python
"system", "You are a helpful AI assistant, collaborating with other assistants."
" Use the provided tools to progress towards answering the question."
" If you are unable to fully answer, that's OK; another assistant with different tools"
" will help where you left off. Execute what you can to make progress."
" Report what your tools support; another agent decides the trade."
" You have access to the following tools: {tool_names}."
" Today's date is {current_date}; treat it as 'now' for all analysis and tool-call date ranges. {instrument_context}\n"
"{system_message}",
```

#### 1.2 Sentiment Analyst
```python
# tradingagents/agents/analysts/sentiment_analyst.py — _build_system_message(...)
"""You are a financial market sentiment analyst. Your task is to produce a comprehensive sentiment report for {ticker} covering the period from {start_date} to {end_date}, drawing on three complementary data sources that have already been collected for you.
## Data sources (pre-fetched, in this prompt)
### News headlines — Yahoo Finance, past 7 days
Institutional framing. Fact-driven, slower-moving signal.
[...]
## Output fields
Fill the following fields:
- **overall_band**: Exactly one of Bullish / Mildly Bullish / Neutral / Mixed / Mildly Bearish / Bearish. [...]
- **overall_score**: A number from 0 (maximally bearish) to 10 (maximally bullish); 5 is neutral. Keep it consistent with overall_band.
- **confidence**: low / medium / high, based on data quality and sample size.
- **narrative**: Full source-by-source breakdown, divergences, dominant narrative themes, catalysts and risks, and a markdown summary table of key sentiment signals [...]
"""
```
Note: the legacy module `social_media_analyst.py` is now a deprecation shim that re-exports `create_sentiment_analyst` from `sentiment_analyst.py`; the internal role key remains `"social"`.

#### 1.3 News Analyst
```python
# tradingagents/agents/analysts/news_analyst.py
f"You are a news researcher tasked with analyzing recent news and trends over the past week. Please write a comprehensive report of the current state of the world that is relevant for trading and macroeconomics. Use the available tools: get_news(start_date, end_date) for news about the {asset_label} under analysis, get_global_news(curr_date, look_back_days, limit) for broader macroeconomic news, get_macro_indicators(indicator, curr_date, look_back_days) to ground macro commentary in actual data from FRED [...], and get_prediction_markets(topic, limit) for live market-implied probabilities of forward-looking events [...]. Provide specific, actionable insights with supporting evidence to help traders make informed decisions."
```

#### 1.4 Fundamentals Analyst
```python
# tradingagents/agents/analysts/fundamentals_analyst.py
"You are a researcher tasked with analyzing fundamental information over the past week about a company. Please write a comprehensive report of the company's fundamental information such as financial documents, company profile, basic company financials, and company financial history to gain a full view of the company's fundamental information to inform traders. [...]
 Use the available tools: `get_fundamentals` for comprehensive company analysis, `get_balance_sheet`, `get_cashflow`, and `get_income_statement` for specific financial statements, and `get_insider_transactions` for recent insider buying and selling."
```

#### 1.5 Bull Researcher
```python
# tradingagents/agents/researchers/bull_researcher.py
prompt = f"""You are a Bull Analyst advocating for investing in the {target_label}. Your task is to build a strong, evidence-based case emphasizing growth potential, competitive advantages, and positive market indicators. Leverage the provided research and data to address concerns and counter bearish arguments effectively.
Key points to focus on:
- Growth Potential: [...]
- Competitive Advantages: [...]
- Positive Indicators: [...]
- Bear Counterpoints: [...]
- Engagement: Present your argument in a conversational style, engaging directly with the bear analyst's points [...]
Resources available:
{instrument_context}
Market research report: {market_research_report}
[...]
Last bear argument: {current_response}
[...]"""
```

#### 1.6 Research Manager
```python
# tradingagents/agents/managers/research_manager.py
prompt = f"""As the Research Manager and debate facilitator, your role is to critically evaluate this round of debate and deliver a clear, actionable investment plan for the trader.
[...]
**Rating Scale** (use exactly one):
- **Buy**: Strong conviction in the bull thesis; recommend taking or growing the position
- **Overweight**: Constructive view; recommend gradually increasing exposure
- **Hold**: Balanced view; recommend maintaining the current position
- **Underweight**: Cautious view; recommend trimming exposure
- **Sell**: Strong conviction in the bear thesis; recommend exiting or avoiding the position
The debate always contains conflicting arguments; deciding which side is stronger is the job, so conflict alone is not a reason to Hold. [...]
## Output
Write these sections, in this order, starting with the recommendation on its own line:
- **Recommendation**: exactly one of Buy / Overweight / Hold / Underweight / Sell
- **Rationale**: which arguments decided it
- **Strategic Actions**: concrete steps for the trader, sized against a standard allocation
{NO_EXTERNAL_TOOLS}"""
```

#### 1.7 Trader
```python
# tradingagents/agents/trader/trader.py — system message ("role": "system")
"You are a trading agent analyzing market data to make investment decisions. "
"Based on your analysis, provide a specific recommendation to buy, sell, or hold. "
[...]
+ "State entry price and stop-loss as absolute price levels in the "
"instrument's quote currency (for example 189.5), never a percentage "
"or a range; convert a percentage distance to the price level it "
"implies, or omit the field if you cannot state a number. "
```
User-message output contract:
```python
"## Output\n\n"
"Write these sections, in this order, starting with the action "
"on its own line:\n\n"
"- **Action**: exactly one of Buy / Hold / Sell. A research "
"recommendation of Overweight is a Buy and Underweight is a Sell, "
"sized by how strong the case is; conflict alone is not a Hold.\n"
"- **Reasoning**: why, against the plan and the price structure\n"
"- **Entry Price**, **Stop Loss**, **Position Sizing**: when you can state them"
```

#### 1.8 Aggressive Risk Analyst (one of three risk debators)
```python
# tradingagents/agents/risk_mgmt/aggressive_debator.py
prompt = f"""As the Aggressive Risk Analyst, your role is to actively champion high-reward, high-risk opportunities, emphasizing bold strategies and competitive advantages. When evaluating the trader's decision or plan, focus intently on the potential upside, growth potential, and innovative benefits—even when these come with elevated risk. [...]
Specifically, respond directly to each point made by the conservative and neutral analysts, countering with data-driven rebuttals and persuasive reasoning. [...]
Output conversationally as if you are speaking without any special formatting."""
```

#### 1.9 Portfolio Manager
```python
# tradingagents/agents/managers/portfolio_manager.py
prompt = f"""As the Portfolio Manager, synthesize the risk analysts' debate and deliver the final trading decision.
[...]
**Rating Scale** (use exactly one):
- **Buy**: Strong conviction to enter or add to position
- **Overweight**: Favorable outlook, gradually increase exposure
- **Hold**: Maintain current position, no action needed
- **Underweight**: Reduce exposure, take partial profits
- **Sell**: Exit position or avoid entry
[...]
## Output
Write these sections, in this order, starting with the rating on its own line:
- **Rating**: exactly one of Buy / Overweight / Hold / Underweight / Sell
- **Executive Summary**: the call and how to act on it
- **Investment Thesis**: the evidence that decided it, and what would change it
{NO_EXTERNAL_TOOLS}{get_language_instruction()}"""
```

---

### 2. Tool Schemas (LangChain `@tool`, `tradingagents/agents/tools.py`)

Tools are grouped by analyst and injected via `InjectedState`. Representative schemas (verbatim signatures/docstrings):

```python
@tool
def get_stock_data(
    symbol: Annotated[str, InjectedState("company_of_interest")],
    start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
    end_date: Annotated[str, "End date in yyyy-mm-dd format"],
    trade_date: Annotated[str, InjectedState("trade_date")] = "",
) -> str:
    """
    Retrieve stock price data (OHLCV) for the instrument under analysis.
    Uses the configured core_stock_apis vendor.
    [...]
    """
```

```python
@tool
def get_verified_market_snapshot(...):
    """Deterministic verification snapshot for exact market-data claims.
    Returns the latest OHLCV row on or before curr_date, common technical
    indicators, and recent closes. [...]
    """
```

```python
@tool
def get_macro_indicators(
    indicator: Annotated[
        str,
        "Macro indicator: a friendly alias such as 'cpi', 'core_pce', "
        "'unemployment', 'fed_funds_rate', '10y_treasury', 'yield_curve', "
        "'real_gdp', 'vix', [...], or a raw FRED series ID such as 'CPIAUCSL'.",
    ],
    curr_date: Annotated[str, "Current date in yyyy-mm-dd format; the end of the window"],
    look_back_days: Annotated[int | None, "Trailing window length in days; omit for a 1-year window"] = None,
    trade_date: Annotated[str, InjectedState("trade_date")] = "",
) -> str:
```

Full tool set defined in `tools.py`: `get_stock_data`, `get_indicators`, `get_verified_market_snapshot`, `get_fundamentals`, `get_balance_sheet`, `get_cashflow`, `get_income_statement`, `get_news`, `get_global_news`, `get_insider_transactions`, `get_macro_indicators`, `get_prediction_markets`. Each analyst binds only its own tuple, e.g.:
```python
# market_analyst.py
TOOLS = (get_stock_data, get_indicators, get_verified_market_snapshot)
# news_analyst.py
TOOLS = (get_news, get_global_news, get_macro_indicators, get_prediction_markets)
# fundamentals_analyst.py
TOOLS = (get_fundamentals, get_balance_sheet, get_cashflow, get_income_statement, get_insider_transactions)
```

---

### 3. Structured-Output Schemas (`tradingagents/agents/schemas.py`, Pydantic)

Applied to the three decision-making agents and the Sentiment Analyst (with free-text fallback).

```python
class PortfolioRating(StrEnum):
    """5-tier rating used by the Research Manager and Portfolio Manager."""
    BUY = "Buy"; OVERWEIGHT = "Overweight"; HOLD = "Hold"
    UNDERWEIGHT = "Underweight"; SELL = "Sell"

class TraderAction(StrEnum):
    BUY = "Buy"; HOLD = "Hold"; SELL = "Sell"

class ResearchPlan(BaseModel):
    recommendation: PortfolioRating = Field(description="The investment recommendation. Exactly one of Buy / Overweight / Hold / Underweight / Sell. [...]")
    rationale: str = Field(description="Conversational summary of the key points from both sides of the debate [...]")
    strategic_actions: str = Field(description="Concrete steps for the trader to implement the recommendation, including sizing guidance relative to a standard allocation. [...]")

class TraderProposal(BaseModel):
    action: TraderAction = Field(description="The transaction direction. Exactly one of Buy / Hold / Sell.")
    reasoning: str = Field(description="The case for this action, anchored in the analysts' reports and the research plan. Two to four sentences.")
    entry_price: float | None = Field(default=None, description="Optional entry price target as an absolute number in the instrument's quote currency (e.g. 189.5), never a percentage or a range. [...]")
    stop_loss: float | None = Field(default=None, description="Optional stop-loss as an absolute price in the instrument's quote currency (e.g. 172.0), never a percentage. [...]")
    position_sizing: str | None = Field(default=None, description="Optional sizing guidance, e.g. '5% of portfolio'.")

class PortfolioDecision(BaseModel):
    rating: PortfolioRating = Field(description="The final position rating. Exactly one of Buy / Overweight / Hold / Underweight / Sell, picked based on the analysts' debate. [...]")
    executive_summary: str = Field(description="A concise action plan covering entry strategy, position sizing, key risk levels, and time horizon. Two to four sentences.")
    investment_thesis: str = Field(description="Detailed reasoning anchored in specific evidence from the analysts' debate. [...]")
    price_target: float | None = Field(default=None, description="Optional target price in the instrument's quote currency.")
    time_horizon: str | None = Field(default=None, description="Optional recommended holding period, e.g. '3-6 months'.")

class SentimentBand(StrEnum):
    BULLISH = "Bullish"; MILDLY_BULLISH = "Mildly Bullish"; NEUTRAL = "Neutral"
    MIXED = "Mixed"; MILDLY_BEARISH = "Mildly Bearish"; BEARISH = "Bearish"

class SentimentReport(BaseModel):
    overall_band: SentimentBand = Field(description="Overall sentiment direction. Exactly one of: Bullish / Mildly Bullish / Neutral / Mixed / Mildly Bearish / Bearish. [...]")
    overall_score: float = Field(ge=0.0, le=10.0, description="Numeric sentiment intensity on a 0–10 scale. 0 = maximally bearish, 5 = neutral, 10 = maximally bullish. [...]")
    confidence: Literal["low", "medium", "high"] = Field(description="Confidence in the assessment based on data quality and sample size. [...]")
    narrative: str = Field(description="Full sentiment report covering, in order: (1) source-by-source breakdown [...] (5) a markdown table summarising key sentiment signals [...]")
```

---

### 4. Orchestration Config (`tradingagents/graph/setup.py` and `conditional_logic.py`)

Node/edge wiring (verbatim excerpt):
```python
workflow.add_node("Bull Researcher", bull_researcher_node)
workflow.add_node("Bear Researcher", bear_researcher_node)
workflow.add_node("Research Manager", research_manager_node)
workflow.add_node("Trader", trader_node)
workflow.add_node("Aggressive Analyst", aggressive_analyst)
workflow.add_node("Neutral Analyst", neutral_analyst)
workflow.add_node("Conservative Analyst", conservative_analyst)
workflow.add_node("Portfolio Manager", portfolio_manager_node)

# The analysts work at the same time; the research debate starts once
# every one of them has filed its report.
first_steps = [spec.agent_node for spec in plan.specs]
if memory_node is not None:
    workflow.add_node("Memory Log", memory_node)
    first_steps.append("Memory Log")
for node in first_steps:
    workflow.add_edge(START, node)
    workflow.add_edge(first_steps, "Bull Researcher")
[...]
workflow.add_edge("Research Manager", "Trader")
workflow.add_edge("Trader", "Aggressive Analyst")
[...]
workflow.add_edge("Portfolio Manager", END)
```

Debate-termination conditions (verbatim):
```python
class ConditionalLogic:
    def __init__(self, max_debate_rounds=1, max_risk_discuss_rounds=1): ...
    def should_continue_debate(self, state: AgentState) -> str:
        if state["investment_debate_state"]["count"] >= 2 * self.max_debate_rounds:
            return "Research Manager"
        if state["investment_debate_state"]["current_response"].startswith("Bull"):
            return "Bear Researcher"
        return "Bull Researcher"
    def should_continue_risk_analysis(self, state: AgentState) -> str:
        if state["risk_debate_state"]["count"] >= 3 * self.max_risk_discuss_rounds:
            return "Portfolio Manager"
        if state["risk_debate_state"]["latest_speaker"].startswith("Aggressive"):
            return "Conservative Analyst"
        if state["risk_debate_state"]["latest_speaker"].startswith("Conservative"):
            return "Neutral Analyst"
        return "Aggressive Analyst"
```

Each analyst is itself compiled as a sub-graph with tools and a `max_tool_rounds` cap (`_analyst_graph`), so analysts run side-by-side without writing the same state key.

---

### 5. State Schema (`tradingagents/agents/state.py`) — Observability

```python
class AgentState(MessagesState):
    company_of_interest: Annotated[str, "Company that we are interested in trading"]
    asset_type: Annotated[str, "Asset type under analysis such as stock or crypto"]
    instrument_context: Annotated[str, "Deterministic ticker identity resolved at run start"]
    trade_date: Annotated[str, "The analysis date; data is served as of it"]
    market_report: Annotated[str, "Report from the Market Analyst"]
    sentiment_report: Annotated[str, "Report from the Sentiment Analyst"]
    news_report: Annotated[str, "Report from the News Analyst on company and world news"]
    fundamentals_report: Annotated[str, "Report from the Fundamentals Analyst"]
    investment_debate_state: Annotated[InvestDebateState, "Current state of the debate on if to invest or not"]
    investment_plan: Annotated[str, "Investment plan from the Research Manager"]
    trader_investment_plan: Annotated[str, "Transaction proposal from the Trader"]
    risk_debate_state: Annotated[RiskDebateState, "Current state of the debate on evaluating risk"]
    final_trade_decision: Annotated[str, "Final decision from the Portfolio Manager"]
    final_rating: Annotated[str, "The Portfolio Manager's 5-tier rating, or REVIEW when it has none"]
    past_context: Annotated[str, "Memory log context for the Portfolio Manager [...]"]
    portfolio_context: Annotated[str, "Caller-supplied holdings and cash, rendered at run start; empty when not provided"]
```

### 6. Extensibility Config (`tradingagents/default_config.py`)

Environment-driven single source of truth (`_ENV_OVERRIDES`), two model tiers with per-tier providers, vendor chains, and debate round caps:
```python
"llm_provider": "openai",
"deep_think_llm": "gpt-6-sol",
"quick_think_llm": "gpt-6-luna",
"max_debate_rounds": 1,
"max_risk_discuss_rounds": 1,
"max_tool_rounds": 20,
"data_vendors": {
    "core_stock_apis": "yfinance",
    "technical_indicators": "yfinance",
    "fundamental_data": "sec_edgar,yfinance",
    "news_data": "yfinance",
    "macro_data": "fred",
    "prediction_markets": "polymarket",
},
```

---

## Evaluation Dimensions

### 1. Role Division Clarity
- [ ] 11 distinct agent roles with non-overlapping mandates (4 analysts / 2 researchers / 2 managers / 1 trader / 3 risk debators)
- [ ] Each role's purpose stated in its own prompt opener
- [ ] Two-tier model assignment (quick vs deep thinking) clearly tied to role criticality

### 2. Workflow Completeness
- [ ] Full lifecycle covered: analyze → debate → plan → transact → risk-debate → final decision
- [ ] LangGraph transitions and debate-termination conditions are explicit
- [ ] Memory/lessons loop feeding the Portfolio Manager

### 3. Prompt Consistency
- [ ] Shared collaboration preamble reused verbatim across tool-using analysts
- [ ] Unified rating scale (Buy/Overweight/Hold/Underweight/Sell) across manager prompts
- [ ] Consistent "no external tools" / language-instruction suffixes appended to prompts

### 4. Tool Schema Modularity
- [ ] Tools grouped by analyst via per-role `TOOLS` tuples
- [ ] Parameter type annotations + docstrings + `InjectedState` for zero-argument state injection
- [ ] Vendor routing decoupled from tool definitions (`data_vendors` config)

### 5. Observability
- [ ] `AgentState` exposes every intermediate report and both debate states
- [ ] `final_rating` and `memory_note` capture decision + settlement status
- [ ] Per-node checkpointing (`checkpoint_enabled`) for crash-resume

### 6. Extensibility
- [ ] New agent roles plug in via `setup.py` node registration
- [ ] New tools extend by adding a `@tool` function and adding it to a `TOOLS` tuple
- [ ] Config-driven behavior (env overrides, vendor chains, round caps)

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Role Division Clarity | 20% | | |
| Workflow Completeness | 25% | | |
| Prompt Consistency | 15% | | |
| Tool Schema Modularity | 20% | | |
| Observability | 10% | | |
| Extensibility | 10% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### Positive
1. **Full flow**: given `(ticker, trade_date)`, produce all four analyst reports, an investment plan, a trader proposal, and a final 5-tier rating.
2. **Debate termination**: verify the research and risk debates end at the configured round counts and hand off to the correct manager.
3. **Structured output**: confirm Research Manager / Trader / Portfolio Manager return schema-valid objects and that the rendered markdown headers match (`**Rating**`, `**Executive Summary**`, `**Investment Thesis**`).

### Boundary
1. **Single analyst selected**: run with only the market analyst; confirm the researcher prompts degrade gracefully (missing reports are reported as absent).
2. **Ticker on a non-US exchange**: verify benchmark auto-detection via `benchmark_map` suffix routing.
3. **Percent-vs-price coercion**: feed `entry_price = "15%"` and confirm `_coerce_optional_float` drops it to `None` rather than failing the whole proposal.

### Negative
1. **Vendor outage**: simulate a data vendor being unavailable; expect a graceful `vendor_unavailable`/`no_data_available` message instead of a run-ending exception.
2. **Conflicting prompt labels**: force a fall-through routing label; confirm the complete `DEBATE_PATH_MAP`/`RISK_ANALYSIS_PATH_MAP` prevents a LangGraph crash.
3. **Tool-round exhaustion**: force a model that keeps calling tools; confirm the `max_tool_rounds` → `wrap_up` path ends the analyst sub-graph.

---

## Notes

- **License**: The repository's actual `LICENSE` file is **Apache License 2.0** (verified 2026-10-13). The task brief said "MIT"; this discrepancy is recorded here because the on-disk license governs. Apache-2.0 permits quotation and modification with attribution.
- All quoted prompts, tool schemas, Pydantic schemas, state fields and orchestration code above are **verbatim excerpts** from the TradingAgents `main` branch (v0.6.0) raw source files listed in the Metadata; `[...]` marks omitted content.
- **Uncertainty note**: The repository structure corresponds to the current `main` (v0.6.0) layout, which differs from older community tutorials (e.g. it has moved analyst tool definitions into a single `agents/tools.py`, introduced `sentiment_analyst.py` and a `Memory Log` node). Older documentation describing a `tradingagents/agents/utils/` layout will not match. The role key `"social"` is retained internally even though the module was renamed to `sentiment_analyst`.
- This suite is a strong evaluation target for **role specialization + adversarial debate + structured-output gating** in a multi-agent system.
