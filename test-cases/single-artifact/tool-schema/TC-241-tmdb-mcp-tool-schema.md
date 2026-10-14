# TC-241: Wizzy TMDB MCP Server (drakonkat/wizzy-mcp-tmdb) - Tool Schema Evaluation Case

## Metadata
- **Source Project**: drakonkat/wizzy-mcp-tmdb (JavaScript MCP server exposing The Movie Database (TMDB) search and detail tools)
- **License**: MIT (README "License" section: "licensed under the MIT License"; `LICENSE`)
- **Artifact Type**: Tool Schema (MCP tool definitions for the TMDB tools; `search_tmdb` quoted in full)
- **Collection Date**: 2026-10-14
- **Collection Method**: Fetched verbatim from `raw.githubusercontent.com`, branch `master`:
  - `mcp-tmdb-server.js` — the tool array whose entries each carry `name`, `description`, `inputSchema` and `handler`, declared in the `ListToolsRequestSchema` handler
  - `README.md` — confirmed the tool surface (`search_tmdb`, `get_tmdb_details`, `trending_all`, ...) and MIT license

## Original Artifact Content

### Tool definition — `search_tmdb` (`mcp-tmdb-server.js`, fetched verbatim)

```javascript
    // Tool: search_tmdb
    // Purpose: Perform a multi-type search across movies, TV shows, and people.
    // Input: query (required), page (optional), language (optional), include_adult (optional), region (optional).
    // Output: JSON with paginated results, each item normalized to id, media_type, title, date, etc.
    // Use case: AI agents can perform broad searches to find relevant media content.
    {
        name: "search_tmdb",
        description: "Performs a multi-type search across TMDB for movies, TV shows, and people. Input: query (required search string), page (optional 1-1000), language (optional ISO 639-1), include_adult (optional boolean), region (optional ISO 3166-1). Output: JSON with paginated normalized results (id, media_type, title, date, etc.). Purpose: Enable comprehensive content discovery for AI-driven queries.",
        inputSchema: {
            type: "object",
            properties: {
                query: {type: "string", description: "Search text query"},
                page: {type: "number", minimum: 1, description: "Page number (1-1000)"},
                language: {type: "string", description: "ISO 639-1 code (e.g., en-US)"},
                include_adult: {type: "boolean", description: "Include adult results"},
                region: {type: "string", description: "ISO 3166-1 code (e.g., US)"},
            },
            required: ["query"],
            additionalProperties: false,
        },
        handler: async ({query, page, language, include_adult, region}) => {
            if (!query || typeof query !== "string") {
                throw new Error("query must be a non-empty string");
            }
            const data = await tmdbFetch("/search/multi", {query, page, language, include_adult, region});
            const results = Array.isArray(data.results) ? data.results.map(mapSearchResult) : [];
            return {
                content: [
                    {
                        type: "text",
                        text: JSON.stringify({
                            page: data.page,
                            total_pages: data.total_pages,
                            total_results: data.total_results,
                            results
                        }, null, 2),
                    },
                ],
            };
        },
    },
```

### Sibling tool — `get_tmdb_details` (`mcp-tmdb-server.js`, fetched verbatim)

```javascript
    {
        name: "get_tmdb_details",
        description: "Fetches detailed information for a movie, TV show, or person by type and ID. Input: type (required: movie|tv|person), id (required TMDB ID), language (optional ISO 639-1), append (optional comma-separated fields like credits,images). Output: JSON with full item details. Purpose: Obtain in-depth metadata for targeted content analysis by AI agents.",
        inputSchema: {
            type: "object",
            properties: {
                type: {type: "string", enum: ["movie", "tv", "person"], description: "The TMDB media type"},
                id: {type: "number", description: "TMDB ID"},
                language: {type: "string", description: "ISO 639-1 code (e.g., en-US)"},
                append: {type: "string", description: "Comma-separated append_to_response (e.g., credits,images)"},
            },
            required: ["type", "id"],
            additionalProperties: false,
        },
        handler: async ({type, id, language, append}) => {
            const data = await tmdbFetch(`/${type}/${id}`, {language, append_to_response: append});
            return {content: [{type: "text", text: JSON.stringify(data)}]};
        },
    },
```

> The same tool array continues with `search_tmdb_movies`, `search_keywords`, `movie_reviews`, `movie_credits` and others. Only the two structurally representative tools `search_tmdb` and `get_tmdb_details` are quoted here (one cohesive registry).

## Evaluation Dimensions

### 1. Tool Description Clarity (for model tool-selection)
- [ ] The description states capability ("multi-type search across TMDB for movies, TV shows, and people")
- [ ] Inputs are enumerated with types and formats ("page (optional 1-1000)", "ISO 639-1", "ISO 3166-1")
- [ ] Output is described ("paginated normalized results (id, media_type, title, date, etc.)")
- [ ] `search_tmdb` (multi-type) is disambiguated from `search_tmdb_movies` (movies only) and `get_tmdb_details` (by ID)

### 2. JSON Schema Correctness
- [ ] Valid JSON Schema (`type: "object"`, `properties`, `required`, `additionalProperties: false`)
- [ ] Types are accurate (`string`, `number`, `boolean`, and `enum` for `type`)
- [ ] `required: ["query"]` matches the handler's non-empty-string guard
- [ ] Constraint present (`page` `minimum: 1`)

### 3. Parameter Description Quality
- [ ] Every parameter has a human-readable `description`
- [ ] Formats and example codes are documented inline (`en-US`, `US`)
- [ ] The `page` bound (1-1000) is stated both on the property and in the tool description
- [ ] `append` explains its comma-separated `append_to_response` semantics with an example

### 4. Integration Compatibility
- [ ] Conforms to the MCP tool model (`ListToolsRequestSchema` returns tools with `name`/`description`/`inputSchema`)
- [ ] Built on the standard MCP TypeScript SDK `Server` / `StdioServerTransport`
- [ ] Requires `TMDB_AUTH_TOKEN` for the configured TMDB proxy, surfaced by a clear startup error when unset

### 5. Extensibility & Maintainability
- [ ] Tools are declared centrally in one array, each with a colocated `handler`
- [ ] A shared `mapSearchResult` normalizes heterogeneous TMDB payloads to a compact, agent-friendly shape
- [ ] Consistent context-prefixed naming (`search_tmdb`, `get_tmdb_details`)

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
1. Issue "search TMDB for Dune"; verify `search_tmdb` is called with `query: "Dune"`.
2. Issue "show me details for movie 438631, including credits and images"; verify `get_tmdb_details` with `type: "movie"`, `id: 438631`, `append: "credits,images"`.
3. Issue "find Spanish-language results for 'amor'"; verify `query: "amor"` and `language` set to a valid ISO 639-1 tag such as `es-ES`.

### Boundary Test Cases
1. `page` at its floor (1); verify the documented bound.
2. `include_adult` omitted vs `false`; verify both behave as the default.
3. `region: "US"` supplied for a multi-search; verify it is accepted as documented.
4. `type` set to each enum value (`movie`, `tv`, `person`) with a valid `id`.

### Negative Test Cases
1. `search_tmdb` without the required `query`; verify schema validation rejects the call.
2. `query` set to an empty string; verify the handler's "query must be a non-empty string" error path.
3. `get_tmdb_details` with `type: "book"` (out of enum); verify rejection.
4. An extra undeclared property in the arguments; verify `additionalProperties: false` behavior (rejection by strict clients).

## Notes
- This is one logical artifact: a single MCP server's tool registry; `search_tmdb` is quoted in full as the representative multi-type search tool, with `get_tmdb_details` shown for disambiguation.
- The `inputSchema`s are hand-written JSON Schema declared inline on each array entry (not generated from a validation library).
- License is MIT (`README.md`, `LICENSE`). Note the server routes TMDB calls through a proxy (`production-api.tnl.one`) gated by `TMDB_AUTH_TOKEN`; this is a configuration detail and does not affect the schema under evaluation.
