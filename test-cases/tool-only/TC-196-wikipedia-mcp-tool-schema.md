# TC-196: wikipedia-mcp (Rudra-ravi) - Tool Schema Evaluation Case

## Metadata
- **Source Project**: Rudra-ravi/wikipedia-mcp (MCP server for retrieving Wikipedia content)
- **License**: MIT (see `LICENSE`; note the copyright line contains a placeholder author string)
- **Artifact Type**: Tool Schema (MCP tool definition for the `search_wikipedia` tool)
- **Collection Date**: 2026-10-13
- **Collection Method**: Downloaded verbatim from `raw.githubusercontent.com`, branch `main`:
  - `wikipedia_mcp/server.py` — the `register_tool(...)` decorator that calls `server.tool(...)` and the `search_wikipedia` function whose signature produces the `inputSchema`
  - `wikipedia_mcp/schemas.py` — the Pydantic `SearchWikipediaResponse` model that backs the tool `output_schema`
  - `LICENSE` — confirmed MIT

## Original Artifact Content

### Tool registration mechanism (`wikipedia_mcp/server.py`, fetched verbatim)

```python
    def register_tool(name: str, output_schema: dict[str, Any]):
        def decorator(func):
            server.tool(
                func,
                name=name,
                annotations=_READ_ONLY_TOOL_ANNOTATIONS,
                output_schema=output_schema,
            )
            server.tool(
                func,
                name=f"wikipedia_{name}",
                annotations=_READ_ONLY_TOOL_ANNOTATIONS,
                output_schema=output_schema,
            )
            return func

        return decorator
```

### The `search_wikipedia` tool (`wikipedia_mcp/server.py`, fetched verbatim)

```python
    @register_tool("search_wikipedia", model_output_schema(SearchWikipediaResponse))
    def search_wikipedia(query: str, limit: int = 10):
        """
        Search Wikipedia for articles matching a query.

        Parameters:
            query: The search term to look up on Wikipedia.
            limit: Maximum number of results to return (1-500).

        Returns a dictionary with the search query, results, status, and
        additional metadata. If the query is empty or invalid, the status
        will be 'error' and an explanatory message is included.
        """
        logger.info("Tool: Searching Wikipedia for '%s' (limit=%d)", query, limit)

        if not query or not query.strip():
            logger.warning("Search tool called with empty query")
            return {
                "query": query,
                "results": [],
                "status": "error",
                "message": "Empty search query provided",
            }

        validated_limit = limit
        if limit <= 0:
            validated_limit = 10
            logger.warning("Invalid limit %d; using default %d", limit, validated_limit)
        elif limit > 500:
            validated_limit = 500
            logger.warning("Limit %d capped to %d", limit, validated_limit)

        results = wikipedia_client.search(query, limit=validated_limit)
        status = "success" if results else "no_results"
        response = {
            "query": query,
            "results": results,
            "status": status,
            "count": len(results),
            "language": wikipedia_client.base_language,
        }

        if not results:
            response["message"] = (
                "No search results found. This could indicate connectivity issues, "
                "API errors, or simply no matching articles."
            )

        return response
```

### Output schema source (`wikipedia_mcp/schemas.py`, fetched verbatim)

```python
class SearchResultItem(MCPBaseModel):
    title: str
    snippet: str = ""
    pageid: int = 0
    wordcount: int = 0
    timestamp: str = ""


class SearchWikipediaResponse(MCPBaseModel):
    query: str
    results: list[SearchResultItem] = []
    status: str
    count: Optional[int] = None
    language: Optional[str] = None
    message: Optional[str] = None


def model_output_schema(model: type[MCPBaseModel]) -> dict[str, Any]:
    """Return object JSON schema suitable for MCP tool outputSchema."""
    return model.model_json_schema()
```

## Evaluation Dimensions

### 1. Schema Completeness
- [ ] The tool exposes a concrete schema (generated from the function signature + type hints)
- [ ] Types are accurate (`string`, `integer`)
- [ ] Required vs optional parameters are distinguishable (`query` required; `limit` has a default)
- [ ] A default is declared (`limit=10`) and a valid range is documented (1–500)

### 2. Description Clarity
- [ ] The tool description states the capability ("Search Wikipedia for articles matching a query")
- [ ] Parameters are documented in a `Parameters:` block
- [ ] The return contract is described (status `error` on empty query; `no_results` when nothing matches)

### 3. Integration Compatibility
- [ ] Registered through FastMCP (`server.tool(func, name=..., annotations=..., output_schema=...)`)
- [ ] The signature-derived `inputSchema` and the Pydantic-derived `outputSchema` are consumable by MCP clients
- [ ] Read-only annotations are applied consistently to the tool

### 4. Example Quality
- [ ] The `limit` description states the accepted range (1–500)
- [ ] Each field returned by the `SearchWikipediaResponse` model is typed and self-describing
- [ ] Error/empty-result states are documented in the description and implemented in the body

### 5. Extensibility
- [ ] A shared `register_tool` helper registers each function under both a bare name and a `wikipedia_`-prefixed alias, avoiding duplication
- [ ] Output schemas are centralized as Pydantic models in `schemas.py`
- [ ] Language/country/caching are configured on the shared `WikipediaClient`, keeping the tool schema minimal

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
1. Issue "search Wikipedia for the Eiffel Tower"; verify `search_wikipedia` is called with `query: "Eiffel Tower"` (default `limit: 10`).
2. Issue "give me the top 25 Wikipedia results for 'quantum computing'"; verify `limit: 25`.
3. Issue "find Wikipedia articles about 'Marie Curie'"; verify results include titles, snippets, and pageids per the output schema.

### Boundary Test Cases
1. `limit` at 1 and at 500 (documented bounds); verify behavior at each boundary.
2. `limit: 0` or negative; verify the documented fallback to 10.
3. `limit: 1000`; verify the documented cap to 500.
4. A query that returns no matches; verify `status: "no_results"` and the explanatory message.

### Negative Test Cases
1. `search_wikipedia` with an empty or whitespace-only `query`; verify `status: "error"` and the "Empty search query provided" message.
2. `search_wikipedia` without the required `query`; verify validation rejects the call.
3. `limit` provided as a string; verify type validation rejects it.
4. Simulated network failure; verify the documented connectivity-error path within the `no_results`/error messaging.

## Notes
- This is one logical artifact: the `search_wikipedia` tool. The server exposes it under both `search_wikipedia` and `wikipedia_search_wikipedia` (via the `register_tool` alias mechanism), plus several sibling tools (`get_article`, `test_wikipedia_connectivity`, etc.).
- The `inputSchema` is **generated** from the Python function signature/type hints by the MCP framework; the verbatim function source is quoted and labeled as the schema source, per the rule for generated schemas. The `output_schema` is generated from the `SearchWikipediaResponse` Pydantic model.
- License is MIT; verbatim quotation is permissible. Note: the `LICENSE` copyright line contains the placeholder text `Copyright (c) 2025 Your Name`, which is a minor documentation defect but does not change the MIT grant.
