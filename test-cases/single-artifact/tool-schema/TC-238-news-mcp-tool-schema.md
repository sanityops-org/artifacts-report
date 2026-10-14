# TC-238: News MCP Server (guangxiangdebizi/news-mcp) - Tool Schema Evaluation Case

## Metadata
- **Source Project**: guangxiangdebizi/news-mcp (MCP news-search server with automatic multi-API failover)
- **License**: Apache License 2.0 (README badge and `LICENSE`; "Licensed under the Apache License 2.0")
- **Artifact Type**: Tool Schema (MCP tool definition for the `search_news` tool)
- **Collection Date**: 2026-10-14
- **Collection Method**: Fetched verbatim from `raw.githubusercontent.com`, branch `main`:
  - `src/tools/newsSearch.ts` — the exported `newsSearch` object whose `name`, `description` and `parameters` (JSON Schema) form the tool definition, followed by its `run` handler
  - `README.md` — confirmed the tool surface and Apache-2.0 license

## Original Artifact Content

### Tool definition (`src/tools/newsSearch.ts`, fetched verbatim)

```typescript
// Smart news search with automatic API switching
export const newsSearch = {
  name: "search_news",
  description: "Search for news articles using multiple news APIs with automatic failover. The system intelligently switches between different news APIs when one reaches its limit or fails.",
  parameters: {
    type: "object",
    properties: {
      query: {
        type: "string",
        description: "Search query for news articles (keywords, topics, etc.)"
      },
      language: {
        type: "string",
        description: "Language code for news articles (e.g., 'en', 'zh', 'es')",
        default: "en"
      },
      limit: {
        type: "number",
        description: "Maximum number of articles to return (1-10)",
        minimum: 1,
        maximum: 10,
        default: 5
      }
    },
    required: ["query"]
  },

  async run(args: { query: string; language?: string; limit?: number }) {
    try {
      // Validate input
      if (!args.query || args.query.trim().length === 0) {
        throw new Error("Search query cannot be empty");
      }
      ...
```

> The `run` handler continues with quota tracking, per-API request building and result formatting; only the schema-bearing head of the object is quoted here. The example below shows how the tool is registered on the FastMCP/MCP server (`README.md`).

```typescript
// Search for technology news
{
  "query": "artificial intelligence",
  "language": "en",
  "limit": 5
}
```

## Evaluation Dimensions

### 1. Tool Description Clarity (for model tool-selection)
- [ ] The description states the capability ("Search for news articles") and the mechanism ("using multiple news APIs with automatic failover")
- [ ] The failover behavior is explained ("intelligently switches between different news APIs when one reaches its limit or fails")
- [ ] No marketing-only text that omits functional capability

### 2. JSON Schema Correctness
- [ ] Valid JSON Schema (`type: "object"`, `properties`, `required`)
- [ ] Types are accurate (`string`, `number`)
- [ ] `required: ["query"]` matches the handler's validation (empty query is rejected)
- [ ] Constraints are declared (`limit` `minimum: 1`, `maximum: 10`)

### 3. Parameter Description Quality
- [ ] Every parameter has a human-readable `description`
- [ ] Defaults are documented inline (`language` default `en`; `limit` default `5`)
- [ ] Accepted ranges/examples are given (`limit` 1–10; language examples `en`, `zh`, `es`)

### 4. Integration Compatibility
- [ ] Conforms to the MCP tool model (a named tool with a JSON-Schema `inputSchema`/`parameters` and a `run` handler)
- [ ] Parameter schema is a plain JSON-Schema object, portable across MCP and other function-calling clients
- [ ] Configuration is environment-driven (at least one of `THE_NEWS_API_KEY`, `NEWSDATA_IO_KEY`, `NEWSAPI_ORG_KEY`, `GNEWS_API_KEY`, `TWINGLY_API_KEY`)

### 5. Extensibility & Maintainability
- [ ] Tool definition is centralized in one module (`src/tools/newsSearch.ts`)
- [ ] API providers are configured separately (`src/config.ts`) with a priority order, so new providers can be added without touching the schema
- [ ] Consistent, verb-only naming (`search_news`)

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Tool Description Clarity | 25% | | |
| JSON Schema Correctness | 25% | | |
| Parameter Description Quality | 20% | | |
| Integration Compatibility | 15% | | |
| Extensibility & Maintainability | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Issue "what's the latest news on artificial intelligence?"; verify `search_news` is called with a non-empty `query`.
2. Issue "busca noticias en español sobre el clima"; verify `language: "es"` and a valid `query`.
3. Issue "give me the top 3 headlines about the election"; verify `limit: 3`.

### Boundary Test Cases
1. `limit` at its floor (1) and ceiling (10); verify bounds are respected.
2. `limit` omitted; verify the documented default of 5 applies.
3. `language` omitted; verify the documented default of `en` applies.
4. Only one provider key configured; verify the failover path still returns results.

### Negative Test Cases
1. `search_news` without the required `query`; verify schema validation rejects the call.
2. `query` set to an empty string; verify the handler's "Search query cannot be empty" error path.
3. `limit: 50` (above `maximum: 10`); verify rejection or clamping.
4. No news API keys configured at all; verify the tool returns the "No News APIs Configured" guidance rather than a fabricated result.

## Notes
- This is one logical artifact: the `search_news` tool. The server also exposes `run`-level behavior (quota tracking, provider failover) that is not part of the schema.
- The schema is hand-written JSON Schema declared on the exported object's `parameters` field, rather than generated from a validation library.
- License is Apache-2.0 (`LICENSE`, README badge `License-Apache%202.0`); long verbatim quotation is permissible.
