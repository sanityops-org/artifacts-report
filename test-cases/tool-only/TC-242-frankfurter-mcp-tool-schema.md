# TC-242: Frankfurter MCP (anirbanbasu/frankfurtermcp) - Tool Schema Evaluation Case

## Metadata
- **Source Project**: anirbanbasu/frankfurtermcp (Python MCP server for currency exchange rates and conversion via the Frankfurter API)
- **License**: MIT (Copyright (c) 2025--present, The Project Contributors; `LICENSE`)
- **Artifact Type**: Tool Schema (FastMCP tool definition for `convert_currency_latest`; a Python-tool system generated from annotations)
- **Collection Date**: 2026-10-14
- **Collection Method**: Fetched verbatim from `raw.githubusercontent.com`, branch `master`:
  - `src/frankfurtermcp/server.py` — the `FrankfurterMCP` FastMCP application: the `tools` metadata list and the `async def` tool functions whose typed signatures + docstrings produce the MCP `inputSchema`/description
  - `LICENSE` — confirmed MIT

## Original Artifact Content

### Tool metadata (`src/frankfurtermcp/server.py`, fetched verbatim)

```python
class FrankfurterMCP(MCPMixin, HTTPHelperMixin):
    """A FastMCP application that provides currency exchange rate functionalities using the Frankfurter API."""
    tools = [
        {
            "fn": "get_supported_currencies",
            "tags": ["currency-rates", "supported-currencies"],
            "annotations": {
                "readOnlyHint": True,
                "openWorldHint": True,
            },
        },
        {
            "fn": "get_latest_exchange_rates",
            "tags": ["currency-rates", "exchange-rates"],
            "annotations": {
                "readOnlyHint": True,
                "openWorldHint": True,
            },
        },
        {
            "fn": "convert_currency_latest",
            "tags": ["currency-rates", "currency-conversion"],
            "annotations": {
                "readOnlyHint": True,
                "openWorldHint": True,
            },
        },
        ...
    ]
```

### Tool definition — `convert_currency_latest` (`src/frankfurtermcp/server.py`, fetched verbatim)

```python
    async def convert_currency_latest(
        self,
        ctx: Context,
        amount: Annotated[
            PositiveFloat,
            Field(description="The amount in the source currency to convert."),
        ],
        from_currency: Annotated[ISO4217, Field(description="The source currency ISO4217 code.")],
        to_currency: Annotated[ISO4217, Field(description="The target currency ISO4217 code.")],
    ):
        """Converts an amount from one currency to another using the latest exchange rates."""
        if from_currency.lower() == to_currency.lower():
            # If the source and target currencies are the same, no conversion is needed
            raise ValueError(
                f"Source currency '{from_currency}' and target currency '{to_currency}' are the same. No conversion needed."
            )
        await ctx.info(
            f"Obtaining latest exchange rates for {from_currency} to {to_currency} from Frankfurter API at {self.frankfurter_api_url}"
        )
        ...
        converted_amount = amount * float(rate)
        result = CurrencyConversionResponse(
            from_currency=from_currency,
            to_currency=to_currency,
            amount=amount,
            converted_amount=converted_amount,
            exchange_rate=rate,
            rate_date=latest_rates["date"],
        )
        return self.get_response_content(response=result, http_response=http_response, cached_response=cache_hit)
```

### Sibling tool — `convert_currency_specific_date` (fetched verbatim, abbreviated)

```python
    async def convert_currency_specific_date(
        self,
        ctx: Context,
        amount: Annotated[
            PositiveFloat,
            Field(description="The amount in the source currency to convert."),
        ],
        from_currency: Annotated[ISO4217, Field(description="The source currency ISO4217 code.")],
        to_currency: Annotated[ISO4217, Field(description="The target currency ISO4217 code.")],
        specific_date: Annotated[
            date,
            Field(description="The specific date for which the conversion is requested in the YYYY-MM-DD format."),
        ],
    ):
        """Convert an amount from one currency to another using the exchange rates for a specific date.
        If there is no exchange rate available for the specific date, the rate for the closest available date before
        the specified date will be used.
        """
```

> The MCP `inputSchema` for each tool is **generated** by FastMCP from the typed, `Annotated[...]` function parameters (Pydantic `Field` descriptions, `PositiveFloat`, `ISO4217`, `date`), and the tool `description` comes from the function docstring. The verbatim source above is quoted as the schema source.

## Evaluation Dimensions

### 1. Tool Description Clarity (for model tool-selection)
- [ ] Each docstring states the capability ("Converts an amount from one currency to another using the latest exchange rates")
- [ ] `convert_currency_latest` (latest rates) is disambiguated from `convert_currency_specific_date` (a named date) and `get_historical_exchange_rates`
- [ ] The specific-date tool explains its fallback ("the rate for the closest available date before the specified date will be used")

### 2. Schema Correctness (generated from typed signatures)
- [ ] Parameter types are accurate and constrained (`PositiveFloat` for `amount`; `ISO4217` for currency codes; `date` for the date parameter)
- [ ] Required vs optional parameters are distinguishable from the signature (no defaults → required)
- [ ] The generated JSON Schema is consumable by MCP clients (Pydantic/`Annotated`-derived)

### 3. Parameter Description Quality
- [ ] Every parameter carries a `Field(description=...)`
- [ ] Formats are documented inline ("ISO4217 code"; "YYYY-MM-DD format")
- [ ] Behavior for invalid/same-currency input is documented and implemented (same-currency raises a clear error)

### 4. Integration Compatibility
- [ ] Conforms to the FastMCP tool model (`tools` list of `fn` names with `tags` and `annotations`)
- [ ] Read-only tools advertise `readOnlyHint`/`openWorldHint`
- [ ] The `ctx: Context` parameter is injected and excluded from the schema
- [ ] Middleware adds rate limiting and argument hygiene (`RateLimitingMiddleware`, `StripUnknownArgumentsMiddleware`)

### 5. Extensibility & Maintainability
- [ ] Tool metadata (name, tags, annotations) is centralized in the `tools` list
- [ ] Shared response helpers (`get_response_content`) and cached internal methods (`_get_latest_exchange_rates`) are separated from the tool surface
- [ ] Consistent domain-verb naming (`convert_currency_latest`, `get_latest_exchange_rates`, ...)

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Tool Description Clarity | 25% | | |
| Schema Correctness | 25% | | |
| Parameter Description Quality | 20% | | |
| Integration Compatibility | 15% | | |
| Extensibility & Maintainability | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Issue "convert 100 USD to EUR"; verify `convert_currency_latest` is called with `amount: 100`, `from_currency: "USD"`, `to_currency: "EUR"`.
2. Issue "how many Japanese yen is 50 euros today?"; verify `amount: 50`, `from_currency: "EUR"`, `to_currency: "JPY"`.
3. Issue "what was 200 GBP in CHF on 2024-06-01?"; verify `convert_currency_specific_date` with `specific_date: "2024-06-01"`.

### Boundary Test Cases
1. `amount` set to a very small positive value (e.g. `0.01`); verify `PositiveFloat` accepts it.
2. `amount` set to `0` or negative; verify `PositiveFloat` rejects it.
3. Lowercase currency codes (`"usd"`, `"eur"`); verify the code's case-insensitive handling.
4. A holiday/weekend date for `convert_currency_specific_date`; verify the documented closest-prior-date fallback.

### Negative Test Cases
1. `convert_currency_latest` missing `from_currency` or `to_currency`; verify schema validation rejects the call.
2. `from_currency == to_currency` (e.g. both `"USD"`); verify the "same currency ... No conversion needed" error path.
3. An invalid ISO4217 code such as `"USDD"`; verify type validation rejects it.
4. `amount` provided as a string; verify type validation rejects it.

## Notes
- This is one logical artifact: the `convert_currency_latest` tool. The server also exposes `get_supported_currencies`, `get_latest_exchange_rates`, `get_historical_exchange_rates`, `convert_currency_specific_date` and `greet`.
- Because the tool is a Python FastMCP `async def`, its schema is **generated** from the typed signature and Pydantic `Field` annotations, and its description from the docstring; the verbatim function source is quoted and labeled as the schema source, per the rule for generated schemas.
- License is MIT (`LICENSE`: "Copyright (c) 2025--present, The Project Contributors"); long verbatim quotation is permissible.
