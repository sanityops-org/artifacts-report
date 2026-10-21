# TC-199: mcp-server-nationalparks (KyrieTangSheng) - Tool Schema Evaluation Case

## Metadata
- **Source Project**: KyrieTangSheng/mcp-server-nationalparks (MCP server for the U.S. National Park Service API)
- **License**: MIT (Copyright (c) 2025 TangSssss)
- **Artifact Type**: Tool Schema (MCP tool definition for the `findParks` tool)
- **Collection Date**: 2026-10-13
- **Collection Method**: Downloaded verbatim from `raw.githubusercontent.com`, branch `main`:
  - `src/schemas.ts` — the Zod `FindParksSchema` (input schema source)
  - `src/server.ts` — the `ListToolsRequestSchema` handler that registers `findParks` with `zodToJsonSchema(FindParksSchema)`
  - `LICENSE` — confirmed MIT

## Original Artifact Content

### Input schema (`src/schemas.ts`, fetched verbatim)

```typescript
import { z } from 'zod';

// Find Parks Schema
export const FindParksSchema = z.object({
  stateCode: z.string().optional().describe('Filter parks by state code (e.g., "CA" for California, "NY" for New York). Multiple states can be comma-separated (e.g., "CA,OR,WA")'),
  q: z.string().optional().describe('Search term to filter parks by name or description'),
  limit: z.number().optional().describe('Maximum number of parks to return (default: 10, max: 50)'),
  start: z.number().optional().describe('Start position for results (useful for pagination)'),
  activities: z.string().optional().describe('Filter by available activities (e.g., "hiking,camping")')
});
```

### Tool registration (`src/server.ts`, fetched verbatim)

```typescript
  // Register tool definitions
  server.setRequestHandler(ListToolsRequestSchema, async () => {
    return {
      tools: [
        {
          name: "findParks",
          description: "Search for national parks based on state, name, activities, or other criteria",
          inputSchema: zodToJsonSchema(FindParksSchema),
        },
```

### Schema-to-JSON-Schema conversion (`src/server.ts`, fetched verbatim)

```typescript
import { z } from 'zod';
import { zodToJsonSchema } from 'zod-to-json-schema';
```

## Evaluation Dimensions

### 1. Schema Completeness
- [ ] The tool exposes a concrete Zod `inputSchema` (`FindParksSchema`)
- [ ] Types are accurate (`string`, `string`, `number`, `number`, `string`)
- [ ] Required vs optional is explicit (every field uses `.optional()`)
- [ ] Documented bounds exist (`limit` default 10, max 50) even though they are prose-only

### 2. Description Clarity
- [ ] The tool description states the capability ("Search for national parks based on state, name, activities, or other criteria")
- [ ] Every parameter carries a `.describe(...)` string
- [ ] The description names the possible filter dimensions, guiding selection

### 3. Integration Compatibility
- [ ] The Zod schema is converted to JSON Schema via `zodToJsonSchema(...)` for the `inputSchema`
- [ ] Built with the official `@modelcontextprotocol/sdk` `Server` class
- [ ] Invalid arguments raise a `ZodError` that is returned as a structured "Validation error" payload

### 4. Example Quality
- [ ] Concrete examples are embedded in descriptions (`"CA"`, `"CA,OR,WA"`, `"hiking,camping"`)
- [ ] Pagination is documented via `start`
- [ ] `limit` documents both its default and maximum

### 5. Extensibility
- [ ] Input schemas are centralized in `schemas.ts`, decoupled from handlers (`handlers/findParks.ts`)
- [ ] Each tool maps to a dedicated handler with a uniform parse-then-dispatch pattern in `server.ts`
- [ ] The NPS API key is read from `NPS_API_KEY`, keeping the tool surface credential-free

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
1. Issue "find national parks in California"; verify `findParks` is called with `stateCode: "CA"`.
2. Issue "list parks offering hiking and camping"; verify `activities: "hiking,camping"`.
3. Issue "search for Yellowstone"; verify `q: "Yellowstone"`.

### Boundary Test Cases
1. `limit` omitted; verify the documented default (10) is applied.
2. `limit: 50` (documented max) and above; verify the boundary behavior.
3. `stateCode: "CA,OR,WA"`; verify comma-separated multi-state filtering.
4. Pagination: `start` set beyond the first page; verify the correct slice is returned.

### Negative Test Cases
1. `findParks` with an unexpected unknown parameter; verify how the schema handles additional properties.
2. `limit` provided as a string; verify the Zod `number()` constraint rejects it.
3. An empty result set (e.g. `q` matching nothing); verify a graceful "no parks" response.
4. Missing `NPS_API_KEY`; verify the server warns at startup and the handler errors clearly.

## Notes
- This is one logical artifact: the `findParks` tool. The server also exposes `getParkDetails`, `getAlerts`, `getVisitorCenters`, `getCampgrounds`, and `getEvents`.
- The `inputSchema` is authored in Zod and converted with `zodToJsonSchema`; the verbatim Zod source is quoted and labeled as the schema source, per the rule for generated schemas.
- A useful quality discussion point: numeric bounds (`limit` default 10 / max 50) live only in the description text, not as Zod `.min()/.max()` constraints, so they are enforced by prose rather than by the schema.
- License is MIT; verbatim quotation is permissible.
