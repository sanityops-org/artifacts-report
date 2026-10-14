# TC-201: mealdb-mcp (traves-theberge) - Tool Schema Evaluation Case

## Metadata
- **Source Project**: traves-theberge/mealdb-mcp (MCP server for TheMealDB recipe API)
- **License**: MIT (Copyright (c) 2025 Traves Theberge)
- **Artifact Type**: Tool Schema (MCP tool definition for the `search_meals` tool)
- **Collection Date**: 2026-10-13
- **Collection Method**: Downloaded verbatim from `raw.githubusercontent.com`, branch `main`:
  - `src/index.ts` — the `ListToolsRequestSchema` handler listing all tools, including the `search_meals` tool (raw JSON Schema `inputSchema`)
  - `LICENSE` — confirmed MIT

## Original Artifact Content

### The `search_meals` tool (`src/index.ts`, fetched verbatim)

```typescript
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "search_meals",
        description: "Search for meals by name",
        inputSchema: {
          type: "object",
          properties: {
            query: {
              type: "string",
              description: "Name of the meal to search for"
            }
          },
          required: ["query"]
        }
      },
```

### Server bootstrap (`src/index.ts`, fetched verbatim)

```typescript
const MEALDB_BASE_URL = "https://www.themealdb.com/api/json/v1/1";

// Create an MCP server
const server = new Server(
  {
    name: "mealdb-server",
    version: "1.0.0",
  },
```

### Sibling tools in the same array (fetched verbatim, headers only)

```typescript
      { name: "get_meal_details", description: "Get detailed information about a specific meal by ID", ... },
      { name: "get_random_meal", description: "Get a random meal suggestion", ... },
      { name: "list_categories", description: "Get all meal categories", ... },
      { name: "search_by_ingredient", description: "Find meals that contain a specific ingredient", ... }
```

## Evaluation Dimensions

### 1. Schema Completeness
- [ ] The tool exposes a concrete raw JSON Schema (`type: object`, `properties`, `required`)
- [ ] The parameter type is accurate (`string`)
- [ ] Required vs optional is explicit (`query` required; no optional fields)
- [ ] Zero-argument sibling tools use `additionalProperties: false` consistently

### 2. Description Clarity
- [ ] The tool description states the capability ("Search for meals by name")
- [ ] The parameter has a human-readable `description`
- [ ] Sibling tools' descriptions each state their distinct purpose

### 3. Integration Compatibility
- [ ] Built with the official `@modelcontextprotocol/sdk` `Server` class
- [ ] The raw JSON Schema is standards-compliant and consumable by MCP clients and function-calling LLMs
- [ ] Uses the stdio transport (`StdioServerTransport`) with no API key required (free TheMealDB tier)

### 4. Example Quality
- [ ] The `query` description states the expected semantic ("Name of the meal")
- [ ] The success response is a structured JSON payload (`message` + `results[]` with id/name/category/area/thumbnail/tags)
- [ ] The no-match path returns a clear message (`No meals found for "<query>"`)

### 5. Extensibility
- [ ] Tools are declared in one `tools` array, so each recipe capability is added as a discrete entry
- [ ] Search, detail, random, categories, and ingredient-based discovery are separate tools the model can compose
- [ ] The TheMealDB base URL is a single constant, so endpoint changes are localized

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
1. Issue "find a recipe for chicken curry"; verify `search_meals` is called with `query: "Chicken Curry"`.
2. Issue "search for pasta dishes"; verify `query` reflects the dish name and results include `id`, `name`, and `category`.
3. Issue "show me the recipe for Arrabiata"; verify the model follows up with `get_meal_details` using the `id` from the search results.

### Boundary Test Cases
1. A query returning more than 10 matches; verify the documented 10-result slice is applied.
2. A broad single-word query (e.g. "soup"); verify a usable result set is returned.
3. A query with special characters/spaces; verify URL encoding is applied.
4. A dish name differing in case (e.g. "pizza" vs "Pizza"); verify matching behavior.

### Negative Test Cases
1. `search_meals` without the required `query`; verify the handler throws "Query parameter is required".
2. A nonsense query (e.g. "zzzzq"); verify the "No meals found for ..." path.
3. `query` provided as a non-string (e.g. a number); verify `String(...)` coercion behavior is understood and does not silently corrupt the request.
4. A TheMealDB API/network failure; verify the handler returns `isError: true` with an error message.

## Notes
- This is one logical artifact: the `search_meals` tool. The server also exposes `get_meal_details`, `get_random_meal`, `list_categories`, and `search_by_ingredient`.
- The `inputSchema` is an author-written raw JSON Schema, quoted verbatim from `src/index.ts`.
- A useful quality discussion point: `search_meals` returns a truncated list (first 10) with an `id` per meal, and the `search_by_ingredient` tool explicitly instructs the model to chain into `get_meal_details` — an example of cross-tool guidance expressed in the result payload rather than the schema.
- License is MIT; verbatim quotation is permissible.
