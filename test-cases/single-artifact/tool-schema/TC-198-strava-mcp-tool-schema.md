# TC-198: strava-mcp (r-huijts) - Tool Schema Evaluation Case

## Metadata
- **Source Project**: r-huijts/strava-mcp (MCP server exposing Strava athlete/fitness data)
- **License**: MIT (Copyright (c) 2025 r-huijts)
- **Artifact Type**: Tool Schema (MCP tool definition for the `get-athlete-stats` tool)
- **Collection Date**: 2026-10-13
- **Collection Method**: Downloaded verbatim from `raw.githubusercontent.com`, branch `main`:
  - `src/tools/getAthleteStats.ts` — the Zod `GetAthleteStatsInputSchema` and the exported `getAthleteStatsTool` object
  - `LICENSE` — confirmed MIT

## Original Artifact Content

### Input schema (`src/tools/getAthleteStats.ts`, fetched verbatim)

```typescript
import { z } from "zod";
import {
    getAthleteStats as fetchAthleteStats,
    StravaStats
} from "../stravaClient.js";

const GetAthleteStatsInputSchema = z.object({
    athleteId: z.number().int().positive().describe("The unique identifier of the athlete to fetch stats for. Obtain this ID first by calling the get-athlete-profile tool.")
});

type GetAthleteStatsInput = z.infer<typeof GetAthleteStatsInputSchema>;
```

### Tool object (`src/tools/getAthleteStats.ts`, fetched verbatim)

```typescript
export const getAthleteStatsTool = {
    name: "get-athlete-stats",
    description: "Fetches the activity statistics (recent, YTD, all-time) for a specific athlete using their ID. Requires the athleteId obtained from the get-athlete-profile tool.",
    inputSchema: GetAthleteStatsInputSchema,
    execute: async ({ athleteId }: GetAthleteStatsInput) => {
        const token = process.env.STRAVA_ACCESS_TOKEN;

        if (!token) {
             console.error("Missing STRAVA_ACCESS_TOKEN environment variable.");
             return {
                content: [{ type: "text" as const, text: "Configuration error: Missing Strava access token." }],
                isError: true
            };
        }
        // ... (fetchAthleteStats + formatStats)
    }
};
```

*(The `execute` body is elided after the authentication check; the schema and tool identity are quoted fully.)*

## Evaluation Dimensions

### 1. Schema Completeness
- [ ] The tool exposes a concrete Zod `inputSchema` (`GetAthleteStatsInputSchema`)
- [ ] The parameter type is specific (`z.number().int().positive()`)
- [ ] Required vs optional is explicit (the single parameter is required — no `.optional()`)
- [ ] Numeric constraints are declared (`int`, `positive`) rather than described only in prose

### 2. Description Clarity
- [ ] The tool description states the capability ("Fetches the activity statistics (recent, YTD, all-time) ...")
- [ ] The description states the precondition ("Requires the athleteId obtained from the get-athlete-profile tool")
- [ ] The parameter has a `.describe(...)` string that repeats the cross-tool dependency

### 3. Integration Compatibility
- [ ] The Zod schema is converted to JSON Schema by the MCP SDK at registration, consumable by MCP clients and function-calling LLMs
- [ ] Follows the server's `{ name, description, inputSchema, execute }` tool-tool interface
- [ ] Returns MCP `content` blocks and sets `isError` on failure

### 4. Example Quality
- [ ] The parameter description names the producing tool (`get-athlete-profile`), giving a concrete usage sequence
- [ ] Error messaging distinguishes "not found" (404 / "Record Not Found") from generic failures
- [ ] The formatted output uses labelled periods (Recent / Year-to-Date / All-Time)

### 5. Extensibility
- [ ] Each Strava tool lives in its own module under `src/tools/`, so tools are added independently
- [ ] The access token is read from `STRAVA_ACCESS_TOKEN` at call time, keeping the tool schema credential-free
- [ ] Shared formatting helpers (`formatStat`, `formatStats`) separate presentation from tool definition

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
1. Issue "show my Strava stats"; verify the model first calls `get-athlete-profile` to obtain `athleteId`, then calls `get-athlete-stats` with a positive integer.
2. Issue "how far did I run this year?"; verify `get-athlete-stats` is called and the YTD run totals are surfaced.
3. Issue "what's my all-time biggest ride distance?"; verify the response includes the "Biggest Ride Distance" field.

### Boundary Test Cases
1. `athleteId` at 1 (smallest positive integer); verify acceptance.
2. `athleteId: 0` or a negative value; verify the `.positive()` constraint rejects it.
3. `athleteId` as a float (e.g. `1.5`); verify the `.int()` constraint rejects it.
4. A valid-format `athleteId` that does not exist; verify the documented "not found" message path.

### Negative Test Cases
1. `get-athlete-stats` without the required `athleteId`; verify validation rejects the call.
2. `athleteId` provided as a string (e.g. `"12345"`); verify type validation rejects it.
3. Missing `STRAVA_ACCESS_TOKEN`; verify the "Configuration error: Missing Strava access token." path with `isError: true`.
4. A Strava API 429 (rate limit); verify the error is surfaced rather than misreported.

## Notes
- This is one logical artifact: the `get-athlete-stats` tool. The server also exposes many focused tools (e.g. `get-athlete-profile`, `get-all-activities`, `get-segment-leaderboard`), each in its own module.
- The `inputSchema` is authored in Zod and converted to JSON Schema at registration; the verbatim Zod source is quoted and labeled as the schema source, per the rule for generated schemas.
- A useful quality discussion point: the schema encodes constraints (`int`, `positive`) machine-checkably, while the cross-tool dependency (`athleteId` comes from another tool) is expressed only in natural language — the model must sequence the calls correctly.
- License is MIT; verbatim quotation is permissible.
