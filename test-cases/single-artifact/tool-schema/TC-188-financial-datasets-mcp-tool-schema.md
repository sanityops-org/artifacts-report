# TC-188: Financial Datasets MCP Server - Tool Schema Evaluation Case

## Metadata
- **Source Project**: financial-datasets/mcp-server (Financial Datasets MCP server)
- **License**: MIT (Copyright (c) 2025 Financial Datasets)
- **Artifact Type**: Tool Schema (FastMCP tool definitions for stock/crypto/SEC data tools)
- **Collection Date**: 2026-10-13
- **Collection Method**: Fetched verbatim from `raw.githubusercontent.com`, branch `main`:
  - `server.py` — `@mcp.tool()`-decorated function definitions that define each tool's name, description (docstring) and parameters
  - `LICENSE` — confirmed MIT

## Original Artifact Content

### Tool definitions (`server.py`, fetched verbatim)

```python
@mcp.tool()
async def get_income_statements(
    ticker: str,
    period: str = "annual",
    limit: int = 4,
) -> str:
    """Get income statements for a company.
    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
        period: Period of the income statement (e.g. annual, quarterly, ttm)
        limit: Number of income statements to return (default: 4)
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/financials/income-statements/?ticker={ticker}&period={period}&limit={limit}"
    data = await make_request(url)
    # Check if data is found
    if not data:
        return "Unable to fetch income statements or no income statements found."
    # Extract the income statements
    income_statements = data.get("income_statements", [])
    # Check if income statements are found
    if not income_statements:
        return "Unable to fetch income statements or no income statements found."
    # Stringify the income statements
    return json.dumps(income_statements, indent=2)

@mcp.tool()
async def get_current_stock_price(ticker: str) -> str:
    """Get the current / latest price of a company.
    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/prices/snapshot/?ticker={ticker}"
    data = await make_request(url)
    # Check if data is found
    if not data:
        return "Unable to fetch current price or no current price found."
    # Extract the current price
    snapshot = data.get("snapshot", {})
    # Check if current price is found
    if not snapshot:
        return "Unable to fetch current price or no current price found."
    # Stringify the current price
    return json.dumps(snapshot, indent=2)

@mcp.tool()
async def get_historical_stock_prices(
    ticker: str,
    start_date: str,
    end_date: str,
    interval: str = "day",
    interval_multiplier: int = 1,
) -> str:
    """Gets historical stock prices for a company.
    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
        start_date: Start date of the price data (e.g. 2020-01-01)
        end_date: End date of the price data (e.g. 2020-12-31)
        interval: Interval of the price data (e.g. minute, hour, day, week, month)
        interval_multiplier: Multiplier of the interval (e.g. 1, 2, 3)
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/prices/?ticker={ticker}&interval={interval}&interval_multiplier={interval_multiplier}&start_date={start_date}&end_date={end_date}"
    data = await make_request(url)
    # Check if data is found
    if not data:
        return "Unable to fetch prices or no prices found."
    # Extract the prices
    prices = data.get("prices", [])
    # Check if prices are found
    if not prices:
        return "Unable to fetch prices or no prices found."
    # Stringify the prices
    return json.dumps(prices, indent=2)

@mcp.tool()
async def get_company_news(ticker: str) -> str:
    """Get news for a company.
    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/news/?ticker={ticker}"
    data = await make_request(url)
    # Check if data is found
    if not data:
        return "Unable to fetch news or no news found."
    # Extract the news
    news = data.get("news", [])
    # Check if news are found
    if not news:
        return "Unable to fetch news or no news found."
    return json.dumps(news, indent=2)

@mcp.tool()
async def get_sec_filings(
    ticker: str,
    limit: int = 10,
    filing_type: str | None = None,
) -> str:
    """Get all SEC filings for a company.
    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
        limit: Number of SEC filings to return (default: 10)
        filing_type: Type of SEC filing (e.g. 10-K, 10-Q, 8-K)
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/filings/?ticker={ticker}&limit={limit}"
    if filing_type:
        url += f"&filing_type={filing_type}"
 
    # Call the API
    data = await make_request(url)
    # Extract the SEC filings
    filings = data.get("filings", [])
    # Check if SEC filings are found
    if not filings:
        return f"Unable to fetch SEC filings or no SEC filings found."
    # Stringify the SEC filings
    return json.dumps(filings, indent=2)
```

> The repository also defines `get_balance_sheets`, `get_cash_flow_statements`, `get_available_crypto_tickers`, `get_crypto_prices`, `get_historical_crypto_prices` and `get_current_crypto_price` using the same `@mcp.tool()` pattern; the representative five above are quoted verbatim from `server.py`.

### Server bootstrap (fetched verbatim, same file)

```python
# Initialize FastMCP server
mcp = FastMCP("financial-datasets")
# Constants
FINANCIAL_DATASETS_API_BASE = "https://api.financialdatasets.ai"
```

## Evaluation Dimensions

### 1. Schema Completeness
- [ ] Each tool exposes parameters through its typed signature (FastMCP converts the signature into a JSON Schema)
- [ ] Types are accurate (`str`, `int`, `int | None`)
- [ ] Defaults are declared in the signature (`period="annual"`, `limit=4`, `limit=10`, `interval="day"`, `interval_multiplier=1`)
- [ ] Optional parameters (e.g. `filing_type: str | None = None`) are distinguishable from required ones

### 2. Description Clarity
- [ ] Each tool has a docstring used as its description
- [ ] The `Args:` section documents each parameter with examples
- [ ] Domain vocabulary (ticker, period, interval) is explained inline

### 3. Integration Compatibility
- [ ] Built on `mcp.server.fastmcp.FastMCP`, the standard Python MCP server framework
- [ ] Signature-derived schemas are standards-compliant and consumable by any MCP client
- [ ] Return values are JSON strings, giving the model structured, parseable content

### 4. Example Quality
- [ ] Parameter examples are embedded in docstrings (`AAPL`, `GOOGL`, `2020-01-01`, `10-K`)
- [ ] Error branches return human-readable messages instead of raising
- [ ] A tool-for-tool hint exists: `get_historical_crypto_prices` docstring points to `get_available_crypto_tickers` for the valid ticker list

### 5. Extensibility
- [ ] A shared `make_request` helper centralizes API access and error handling
- [ ] A single `FINANCIAL_DATASETS_API_BASE` constant keeps endpoints consistent
- [ ] New tools are added by decorating one function, with no separate schema file to maintain

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Schema Completeness | 25% | | |
| Description Clarity | 20% | | |
| Integration Compatibility | 25% | | |
| Example Quality | 20% | | |
| Extensibility | 10% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Issue "what is Apple's latest stock price?"; verify `get_current_stock_price` with `ticker: "AAPL"`.
2. Issue "show Tesla's quarterly income statements"; verify `get_income_statements` with `period: "quarterly"`.
3. Issue "get MSFT prices from 2024-01-01 to 2024-12-31"; verify `get_historical_stock_prices` with `start_date`, `end_date`.

### Boundary Test Cases
1. `interval` set to each supported value (minute/hour/day/week/month) with a matching `interval_multiplier`.
2. `limit` at a large value; verify behavior is defined.
3. `get_sec_filings` with `filing_type` omitted vs provided.
4. A crypto ticker (e.g. `BTC-USD`) passed to crypto tools after listing available tickers.

### Negative Test Cases
1. A tool called without `ticker`; verify validation rejects the call.
2. An unknown ticker; verify the API error path returns a readable message.
3. `interval_multiplier` given a non-integer; verify type validation rejects it.
4. Ambiguous request "how's the market?"; verify the model asks which ticker/company rather than fabricating one.

## Notes
- This server uses FastMCP, where tool schemas are derived from function signatures and docstrings. The quoted functions are the authoritative, verbatim schema source; the JSON Schema the client receives is generated from them.
- The tool set spans equities, crypto and SEC filings; the five representative equity/filing tools are quoted above (one tightly-related group from a single file).
- License is MIT; long verbatim quotation is permissible.
