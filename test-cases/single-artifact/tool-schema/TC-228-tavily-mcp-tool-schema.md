# TC-228: Tavily MCP Server - Tool Schema Evaluation Case

## Metadata
- **Source Project**: tavily-ai/tavily-mcp (official Tavily MCP server)
- **License**: MIT (Copyright (c) 2024 Alpha AI Technologies Inc.)
- **Artifact Type**: Tool Schema (MCP tool definitions for the `tavily_search` and `tavily_extract` tools)
- **Collection Date**: 2026-10-14
- **Collection Method**: Fetched verbatim from `raw.githubusercontent.com`, branch `main`:
  - `src/index.ts` — the `ListToolsRequestSchema` handler that declares the `Tool[]` array with each tool's `name`, `description` and `inputSchema`
  - `LICENCE` — confirmed MIT

## Original Artifact Content

### Tool declarations (`src/index.ts`, fetched verbatim)

```typescript
  private setupToolHandlers(): void {
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      // Define available tools: tavily_search and tavily_extract
      const tools: Tool[] = [
        {
          name: "tavily_search",
          description: "Search the web for current information on any topic. Use for news, facts, or data beyond your knowledge cutoff. Returns snippets and source URLs.",
          inputSchema: {
            type: "object",
            properties: {
              query: { 
                type: "string", 
                description: "Search query" 
              },
              search_depth: {
                type: "string",
                enum: ["basic","advanced","fast","ultra-fast"],
                description: "The depth of the search. 'basic' for generic results, 'advanced' for more thorough search, 'fast' for optimized low latency with high relevance, 'ultra-fast' for prioritizing latency above all else",
                default: "basic"
              },
              topic : {
                type: "string",
                enum: ["general"],
                description: "The category of the search. This will determine which of our agents will be used for the search",
                default: "general"
              },
              time_range: {
                type: "string",
                description: "The time range back from the current date to include in the search results",
                enum: ["day", "week", "month", "year"]
              },
              start_date: {
                type: "string",
                description: "Will return all results after the specified start date. Required to be written in the format YYYY-MM-DD.",
                default: "",
              },
              end_date: { 
                type: "string",
                description: "Will return all results before the specified end date. Required to be written in the format YYYY-MM-DD",
                default: "",
              },
              max_results: { 
                type: "number", 
                description: "The maximum number of search results to return",
                default: 5,
                minimum: 5,
                maximum: 20
              },
              include_images: { 
                type: "boolean", 
                description: "Include a list of query-related images in the response",
                default: false,
              },
              include_image_descriptions: { 
                type: "boolean", 
                description: "Include a list of query-related images and their descriptions in the response",
                default: false
              },
              include_raw_content: {
                type: "boolean",
                description: "Include the cleaned and parsed HTML content of each search result",
                default: false
              },
              include_domains: {
                type: "array",
                items: { type: "string" },
                description: "A list of domains to specifically include in the search results, if the user asks to search on specific sites set this to the domain of the site",
                default: []
              },
              exclude_domains: {
                type: "array",
                items: { type: "string" },
                description: "List of domains to specifically exclude, if the user asks to exclude a domain set this to the domain of the site",
                default: []
              },
              country: {
                type: "string",
                description: "Boost search results from a specific country. Must be a full country name (e.g., 'United States', 'Japan', 'Germany'). ISO country codes (e.g., 'us', 'jp') are not supported. Available only if topic is general. See https://docs.tavily.com/documentation/api-reference/search for the full list of supported countries.",
                default: ""
              },
              include_favicon: {
                type: "boolean",
                description: "Whether to include the favicon URL for each result",
                default: false
              },
              exact_match: {
                type: "boolean",
                description: "Only return results containing the exact phrase(s) in quotes in your query"
              }
            },
            required: ["query"]
          }
        },
        {
          name: "tavily_extract",
          description: "Extract content from URLs. Returns raw page content in markdown or text format.",
          inputSchema: {
            type: "object",
            properties: {
              urls: { 
                type: "array",
                items: { type: "string" },
                description: "List of URLs to extract content from"
              },
              extract_depth: { 
                type: "string",
                enum: ["basic", "advanced"],
                description: "Use 'advanced' for LinkedIn, protected sites, or tables/embedded content",
                default: "basic"
              },
              include_images: {
                type: "boolean",
                description: "Include images from pages",
                default: false
              },
              format: {
                type: "string",
                enum: ["markdown", "text"],
                description: "Output format",
                default: "markdown"
              },
              include_favicon: {
                type: "boolean",
                description: "Include favicon URLs",
                default: false
              },
              query: {
                type: "string",
                description: "Query to rerank content chunks by relevance"
              }
            },
            required: ["urls"]
          }
        },
```

> The same `tools` array continues with `tavily_crawl`, `tavily_map`, `tavily_research` and `tavily_feedback`. Only the two structurally representative tools `tavily_search` and `tavily_extract` are quoted here (a single cohesive registry, mirroring TC-188).

## Evaluation Dimensions

### 1. Tool Description Clarity (for model tool-selection)
- [ ] Each description states what the tool does and when to use it ("Use for news, facts, or data beyond your knowledge cutoff")
- [ ] Return shape is stated ("Returns snippets and source URLs"; "Returns raw page content in markdown or text format")
- [ ] `tavily_search` and `tavily_extract` are disambiguated (search vs extract-from-URLs)

### 2. Schema Correctness
- [ ] Valid JSON Schema (`type: "object"`, `properties`, `required`)
- [ ] Types are accurate (`string`, `number`, `boolean`, `array`)
- [ ] Required parameters are declared (`query`; `urls`) and match the description
- [ ] Constraints are declared (`max_results` minimum 5, maximum 20)

### 3. Parameter Description Quality
- [ ] Every parameter has a human-readable `description`
- [ ] Defaults and formats are documented inline (`YYYY-MM-DD`, default search depth `basic`, default `max_results` 5)
- [ ] Constraints are explained (full country names only; ISO codes unsupported; `include_domains` recommended for site-scoped queries)

### 4. Integration Compatibility
- [ ] Conforms to the MCP tool model (`ListToolsRequestSchema` returns `Tool[]`)
- [ ] Built on the standard MCP TypeScript SDK `Server` / `StdioServerTransport`
- [ ] Supports keyless operation (`IS_KEYLESS`) and optional `DEFAULT_PARAMETERS` injection

### 5. Extensibility & Maintainability
- [ ] Tools are declared centrally in one handler array
- [ ] Consistent naming convention (`tavily_<verb>`)
- [ ] Parameter defaults are merged from environment-provided `DEFAULT_PARAMETERS`

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
1. Issue "what happened in the news today?"; verify `tavily_search` with a `query` and a `time_range` of `day` or `week`.
2. Issue "extract the key points from https://example.com/article"; verify `tavily_extract` with `urls`.
3. Issue "search only on arxiv.org for diffusion models"; verify `tavily_search` with `query` and `include_domains: ["arxiv.org"]`.

### Boundary Test Cases
1. `max_results` at its floor (5) and ceiling (20); verify bounds are respected.
2. `search_depth` at each enum value (`basic`, `advanced`, `fast`, `ultra-fast`).
3. `country: "Japan"` (full name) vs `country: "jp"` (ISO code); verify only the full name is accepted as documented.
4. `start_date`/`end_date` with the `YYYY-MM-DD` format.

### Negative Test Cases
1. `tavily_search` without `query`; verify schema validation rejects the call.
2. `tavily_extract` without `urls`; verify rejection.
3. `search_depth: "deep"` (out of enum); verify rejection.
4. `max_results: 3` (below `minimum: 5`); verify rejection.

## Notes
- Tavily is a search API designed for LLM agents; this case quotes the two structurally representative tools from the official Tavily MCP server registry.
- Schemas are hand-written JSON Schema (not derived from Zod), declared inline in the `ListToolsRequestSchema` handler.
- License is MIT (the repository's license file is named `LICENCE`); long verbatim quotation is permissible.
