# TC-244: GTFS MCP Server (jdamcd/gtfs-mcp) - Tool Schema Evaluation Case

## Metadata
- **Source Project**: jdamcd/gtfs-mcp (MCP server for public-transit GTFS / GTFS-Realtime data)
- **License**: MIT (Copyright (c) 2026 Jamie McDonald; `LICENSE`)
- **Artifact Type**: Tool Schema (MCP tool definition for the `get_arrivals` tool)
- **Collection Date**: 2026-10-14
- **Collection Method**: Fetched verbatim from `raw.githubusercontent.com`, branch `main`:
  - `src/tools/arrivals.ts` — the `ctx.server.registerTool("get_arrivals", { title, description, inputSchema, outputSchema, annotations }, handler)` call
  - `LICENSE` — confirmed MIT

## Original Artifact Content

### Tool definition — `get_arrivals` (`src/tools/arrivals.ts`, fetched verbatim)

```typescript
export function registerArrivalTools(ctx: ToolContext): void {
  ctx.server.registerTool(
    "get_arrivals",
    {
      title: "Get arrivals at a stop",
      description:
        "Get upcoming arrivals at a stop. Accepts a parent station ID and resolves to all child platforms. Merges realtime data (authoritative within its horizon) with scheduled times (fills beyond). Cancelled trips and skipped stops are excluded; includes services that roll past midnight via yesterday's 24h+ stop_times. Returns data_source indicating which inputs contributed, and `warnings` when a realtime feed could not be fetched.",
      inputSchema: {
        system: z.string().describe("System ID, from list_systems"),
        stop_id: z
          .string()
          .describe("Stop ID (parent station IDs are resolved to child platforms)"),
        route_id: z.string().optional().describe("Filter by route ID"),
        limit: z
          .number()
          .int()
          .min(1)
          .max(100)
          .default(10)
          .describe("Maximum number of arrivals to return"),
      },
      outputSchema: ArrivalsResponseSchema,
      annotations: {
        readOnlyHint: true,
        openWorldHint: true,
      },
    },
    async ({ system, stop_id, route_id, limit }) => {
      ...
    }
  );
}
```

> The `inputSchema` is a Zod object literal; `outputSchema` references the shared `ArrivalsResponseSchema` (from `src/types.ts`). The handler body is abbreviated (`...`) above. Per `README.md`, the `ArrivalsResponse` carries `data_source` (`realtime` / `scheduled` / `mixed` / `none`), an `arrivals` array (`trip_id`, `route_id`, `stop_id`, `arrival_time`, `minutes_away`, `headsign`, `is_realtime`, optional `is_added`) and optional `warnings`.

## Evaluation Dimensions

### 1. Tool Description Clarity (for model tool-selection)
- [ ] The description states the capability ("Get upcoming arrivals at a stop")
- [ ] Non-obvious behaviors are explained (parent station → child platforms; realtime authoritative within horizon; scheduled fills beyond; cancellations/skips excluded; past-midnight services)
- [ ] Return fields are named (`data_source`, `warnings`)
- [ ] Disambiguated from sibling tools (`get_stops`, `get_routes`, `get_trips`, `get_alerts`, ...)

### 2. Schema Correctness
- [ ] Valid JSON Schema generated from Zod (`type: "object"`)
- [ ] Types are accurate (`string`, `number`)
- [ ] `limit` constraints are declared exactly (`int()`, `min(1)`, `max(100)`, `default(10)`)
- [ ] Required vs optional parameters are distinguishable (`system`, `stop_id` required; `route_id`, `limit` optional)
- [ ] An `outputSchema` is declared in addition to the input schema

### 3. Parameter Description Quality
- [ ] Every parameter has a `.describe(...)`
- [ ] `system` documents its source ("from list_systems")
- [ ] `stop_id` documents the parent-to-child resolution behavior
- [ ] Default and bounds of `limit` are documented (10; 1–100)

### 4. Integration Compatibility
- [ ] Conforms to the MCP `registerTool(name, { title, description, inputSchema, outputSchema, annotations }, handler)` API
- [ ] Read-only tools advertise `readOnlyHint`/`openWorldHint`
- [ ] Realtime degradation is surfaced via `warnings` and a `data_source` discriminator rather than an error
- [ ] Works with any GTFS-compatible transit system (system resolved from configuration)

### 5. Extensibility & Maintainability
- [ ] Tools are grouped in per-concern modules (`src/tools/arrivals.ts`, `stops.ts`, `routes.ts`, `trips.ts`, `vehicles.ts`, `alerts.ts`)
- [ ] GTFS queries, realtime helpers and time math are separated into `src/gtfs/*` and `src/time.ts`
- [ ] Shared response schemas live in `src/types.ts`; consistent verb-first naming (`get_arrivals`)

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
1. Issue "when is the next train from <station>?"; verify `get_arrivals` with a valid `system` and `stop_id`.
2. Issue "next 5 arrivals at stop X on route R"; verify `limit: 5` and `route_id: "R"`.
3. Issue "arrivals at a parent station"; verify the parent-station ID is accepted and resolved to child platforms.

### Boundary Test Cases
1. `limit` at its floor (1) and ceiling (100); verify bounds.
2. `limit` omitted; verify the documented default of 10.
3. A stop served only by a service rolling past midnight (GTFS `24:00:00`+ times); verify those arrivals are included from the previous service day.
4. A realtime feed that is unavailable; verify `data_source` degrades (e.g. `scheduled`) and a `warnings` entry explains the schedule-only result.

### Negative Test Cases
1. `get_arrivals` missing the required `system` or `stop_id`; verify schema validation rejects the call.
2. `limit: 0` or `limit: 101`; verify the min/max rejection.
3. `limit` provided as a decimal (e.g. `2.5`); verify the `.int()` constraint rejects it.
4. An unknown `system`; verify the "unknown system" response path rather than a fabricated schedule.

## Notes
- This is one logical artifact: the `get_arrivals` tool. The server registers additional tools for stops, routes, trips, vehicles and service alerts.
- The verbatim `inputSchema` is authored as a Zod object and converted to JSON Schema by the MCP SDK; the `outputSchema` references the shared `ArrivalsResponseSchema`. The Zod source is quoted as the schema source per the rule for generated schemas.
- License is MIT (`LICENSE`: "Copyright (c) 2026 Jamie McDonald"); long verbatim quotation is permissible.
- This is a general-purpose transit-data server (any GTFS feed), which keeps it distinct from city- or agency-specific transit MCP servers.
