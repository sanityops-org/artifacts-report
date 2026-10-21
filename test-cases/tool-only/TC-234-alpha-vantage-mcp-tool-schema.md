# TC-234: alpha-vantage-mcp Tool Schema - Tool Schema Evaluation Case

## Metadata
- **Source Project**: berlinbra/alpha-vantage-mcp
- **License**: MIT
- **Artifact Type**: Tool Schema (MCP tool definitions: name, description, JSON-Schema `inputSchema`)
- **Collection Date**: 2026-10-13
- **Collection Method**: Fetched raw files from `raw.githubusercontent.com`, `HEAD` of the default branch:
  - `src/alpha_vantage_mcp/server.py` (tool definitions via `@server.list_tools()`) — `https://raw.githubusercontent.com/berlinbra/alpha-vantage-mcp/HEAD/src/alpha_vantage_mcp/server.py`
  - `LICENSE` (license verification) — `https://raw.githubusercontent.com/berlinbra/alpha-vantage-mcp/HEAD/LICENSE`
  - Repository file listing — `https://api.github.com/repos/berlinbra/alpha-vantage-mcp/git/trees/HEAD?recursive=1`

## Original Artifact Content

Verbatim excerpt from `src/alpha_vantage_mcp/server.py` (the tool list):

```python
server = Server("alpha_vantage_finance")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools.
    Each tool specifies its arguments using JSON Schema validation.
    """
    return [
        types.Tool(
            name="get-stock-quote",
            description="Get current stock quote information",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock symbol (e.g., AAPL, MSFT)",
                    },
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name="get-company-info",
            description="Get detailed company information",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock symbol (e.g., AAPL, MSFT)",
                    },
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name="get-crypto-exchange-rate",
            description="Get current cryptocurrency exchange rate",
            inputSchema={
                "type": "object",
                "properties": {
                    "crypto_symbol": {
                        "type": "string",
                        "description": "Cryptocurrency symbol (e.g., BTC, ETH)",
                    },
                    "market": {
                        "type": "string",
                        "description": "Market currency (e.g., USD, EUR)",
                        "default": "USD"
                    }
                },
                "required": ["crypto_symbol"],
            },
        ),
        types.Tool(
            name="get-time-series",
            description="Get daily time series data for a stock with optional date filtering",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock symbol (e.g., AAPL, MSFT)",
                    },
                    "outputsize": {
                        "type": "string",
                        "description": "compact (latest 100 data points) or full (up to 20 years of data). When start_date or end_date is specified, defaults to 'full'",
                        "enum": ["compact", "full"],
                        "default": "compact"
                    },
                    "start_date": {
                        "type": "string",
                        "description": "Optional: Start date in YYYY-MM-DD format for filtering results",
                        "pattern": "^20[0-9]{2}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12][0-9]|3[01])$"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "Optional: End date in YYYY-MM-DD format for filtering results",
                        "pattern": "^20[0-9]{2}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12][0-9]|3[01])$"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Optional: Number of data points to return when no date filtering is applied (default: 5)",
                        "default": 5,
                        "minimum": 1
                    }
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name="get-historical-options",
            description="Get historical options chain data for a stock with advanced filtering and sorting capabilities",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock symbol (e.g., AAPL, MSFT)",
                    },
                    "date": {
                        "type": "string",
                        "description": "Optional: Trading date in YYYY-MM-DD format (defaults to previous trading day, must be after 2008-01-01)",
                        "pattern": "^20[0-9]{2}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12][0-9]|3[01])$"
                    },
                    "expiry_date": {
                        "type": "string",
                        "description": "Optional: Filter by expiration date in YYYY-MM-DD format",
                        "pattern": "^20[0-9]{2}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12][0-9]|3[01])$"
                    },
                    "min_strike": {
                        "type": "number",
                        "description": "Optional: Minimum strike price filter (e.g., 100.00)",
                        "minimum": 0
                    },
                    "max_strike": {
                        "type": "number",
                        "description": "Optional: Maximum strike price filter (e.g., 200.00)",
                        "minimum": 0
                    },
                    "contract_id": {
                        "type": "string",
                        "description": "Optional: Filter by specific contract ID (e.g., MSTR260116C00000500)"
                    },
                    "contract_type": {
                        "type": "string",
                        "description": "Optional: Filter by contract type (call or put)",
                        "enum": ["call", "put", "C", "P"]
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Optional: Number of contracts to return after filtering (default: 10, use -1 for all contracts)",
                        "default": 10,
                        "minimum": -1
                    },
                    "sort_by": {
                        "type": "string",
                        "description": "Optional: Field to sort by",
                        "enum": [
                            "strike",
                            "expiration",
                            "volume",
                            "open_interest",
                            "implied_volatility",
                            "delta",
                            "gamma",
                            "theta",
                            "vega",
                            "rho",
                            "last",
                            "bid",
                            "ask"
                        ],
                        "default": "strike"
                    },
                    "sort_order": {
                        "type": "string",
                        "description": "Optional: Sort order",
                        "enum": ["asc", "desc"],
                        "default": "asc"
                    }
                },
                "required": ["symbol"],
            },
        ),
```

Additional tools declared in the same list (names and one-line purpose): `get-crypto-daily`, plus further crypto/earnings/ETF/options tools (`get-realtime-options`,`get-earnings-calendar`, `get-historical-earnings`, `get-earnings-estimates`, `get-etf-profile`, and related market-data endpoints).

## Evaluation Dimensions

### 1. Tool Description Clarity (for model tool-selection)
- [ ] Each description states what data the tool returns
- [ ] Descriptions disambiguate the many closely-related finance tools (quote vs company info vs time series vs options)
- [ ] Descriptions note "optional" filtering semantics where relevant

### 2. JSON Schema Correctness
- [ ] Valid JSON Schema (`type: object`, `properties`, `required`) for each tool
- [ ] `required` correctly lists the mandatory `symbol` (or `crypto_symbol`) and nothing else
- [ ] `enum`, `default`, `minimum`, and `pattern` constraints are internally consistent (`limit` for options allows `-1` while `limit` for time series allows `>= 1`)

### 3. Parameter Description Quality
- [ ] Every parameter has a `description`
- [ ] Date inputs document the `YYYY-MM-DD` format and the ISO `pattern`
- [ ] Enum values are at least named (e.g. sort fields); default values are stated
- [ ] Units/examples are provided where useful (strike price, contract id example)

### 4. Naming & Consistency
- [ ] Tool `name` values use kebab-case consistently (`get-stock-quote`)
- [ ] The identifier key differs between tools (`symbol` vs `crypto_symbol`); verify this is intentional and clear
- [ ] Shared concepts (date, limit, sort) use consistent parameter names and types

### 5. Extensibility & Maintainability
- [ ] All tools are declared in a single `handle_list_tools()` function
- [ ] Request/format helpers live in a separate `tools.py` module
- [ ] API key requirement (`ALPHA_VANTAGE_API_KEY`) is enforced at startup

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Tool Description Clarity | 25% | | |
| JSON Schema Correctness | 25% | | |
| Parameter Description Quality | 20% | | |
| Naming & Consistency | 15% | | |
| Extensibility & Maintainability | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Issue "what is Apple's stock price?"; verify `get-stock-quote` with `symbol: "AAPL"`.
2. Issue "show me Tesla's daily prices for 2026"; verify `get-time-series` with `symbol: "TSLA"`, date filters, and `outputsize: "full"`.
3. Issue "current BTC/USD rate"; verify `get-crypto-exchange-rate` with `crypto_symbol: "BTC"`, `market: "USD"`.

### Boundary Test Cases
1. `limit: -1` on `get-historical-options` (all contracts); verify the `minimum: -1` bound accepts it, while `limit: 0` is rejected.
2. `start_date`/`end_date` at the ISO pattern boundary (e.g. `2026-01-01`); verify accepted and malformed dates rejected.
3. `sort_by` set to each of the 13 enum values; verify all accepted.

### Negative Test Cases
1. Call `get-stock-quote` without `symbol`; verify the required field is enforced.
2. Pass `expiry_date: "01/2026"`; verify the `pattern` rejects it.
3. Ask a market question with no symbol ("how are stocks doing?"); verify the model requests a symbol rather than inventing a ticker.

## Notes
- This artifact is the tool-selection surface an LLM sees for the Alpha Vantage finance server. It is one of the richest examples here in terms of enums and date patterns.
- Note the deliberate inconsistency that `get-historical-options.limit` permits `-1` (meaning "all") while other tools use `limit >= 1`; this is a useful schema-consistency probe.
- License is MIT (per the repository `LICENSE`); verbatim quotation of the tool schemas is permissible.
