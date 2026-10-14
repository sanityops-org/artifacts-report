# TC-243: Sports MCP Server (cyanheads/sports-mcp-server) - Tool Schema Evaluation Case

## Metadata
- **Source Project**: cyanheads/sports-mcp-server (TypeScript MCP server for live/historical sports data from ESPN, MLB StatsAPI and TheSportsDB)
- **License**: Apache License 2.0 (Copyright 2026 Casey Hand @cyanheads; `LICENSE`)
- **Artifact Type**: Tool Schema (MCP tool definition for the `sports_get_scores` tool)
- **Collection Date**: 2026-10-14
- **Collection Method**: Fetched verbatim from `raw.githubusercontent.com`, branch `main` (via `HEAD`):
  - `src/mcp-server/tools/definitions/sports-get-scores.tool.ts` — the `tool('sports_get_scores', { description, annotations, input, output, enrichment, handler, format })` definition
  - `LICENSE` — confirmed Apache-2.0

## Original Artifact Content

### Tool definition — `sports_get_scores` (`src/mcp-server/tools/definitions/sports-get-scores.tool.ts`, fetched verbatim)

```typescript
import { tool, z } from '@cyanheads/mcp-ts-core';
import { easternToday } from '@/services/date-window.js';
import { getEspnService } from '@/services/espn/espn-service.js';
import { getMlbService } from '@/services/mlb/mlb-service.js';
import { LEAGUE_ROUTES } from '@/services/types.js';
import { inline } from '../formatting.js';

const LEAGUE_ENUM = z.enum([
  'nfl',
  'nba',
  'mlb',
  'nhl',
  'epl',
  'mls',
  'laliga',
  'bundesliga',
  'seriea',
  'ligue1',
  'ucl',
  'ncaaf',
  'ncaab',
]);

export const sportsGetScores = tool('sports_get_scores', {
  description:
    "Live and final scores for a league on a given provider-calendar date, optionally filtered by team name. Returns teams, scores, status, period or clock, and UTC start. Omitted dates use today's US Eastern calendar day, including daylight saving time. NCAAB covers men's Division I; NCAAF covers FBS.",
  annotations: { readOnlyHint: true, openWorldHint: true },
  input: z.object({
    league: LEAGUE_ENUM.describe(
      'League identifier. Supported: nfl, nba, mlb, nhl, epl, mls, laliga, bundesliga, seriea, ligue1, ucl, ncaaf, ncaab.',
    ),
    date: z
      .string()
      .regex(/^\d{4}-\d{2}-\d{2}$/, 'Date must be in YYYY-MM-DD format.')
      .optional()
      .describe("Provider-calendar date in YYYY-MM-DD format. Omit for today's US Eastern day."),
    team_name: z
      .string()
      .max(200, 'Team name must be 200 characters or fewer.')
      .optional()
      .describe(
        'Filter results to games involving this team. Fuzzy match on team name or abbreviation.',
      ),
  }),
  output: z.object({
    games: z
      .array(
        z
          .object({
            id: z
              .string()
              .describe(
                'Source-prefixed game ID, e.g. espn:401872656 or mlb:823457. Pass with this league to sports_get_game.',
              ),
            shortName: z.string().describe('Short matchup string, e.g. "SEA @ NYY".'),
            homeTeam: z
              .object({
                id: z.string().describe('Source-prefixed team ID.'),
                name: z.string().describe('Full team name.'),
                abbreviation: z.string().describe('Team abbreviation, e.g. "SEA" or "NYY".'),
                score: z
                  .string()
                  .nullable()
                  .describe('Current or final score, null if not yet started.'),
              })
              .describe('Home team details and score.'),
            awayTeam: z
              .object({
                id: z.string().describe('Source-prefixed team ID.'),
                name: z.string().describe('Full team name.'),
                abbreviation: z.string().describe('Team abbreviation, e.g. "SEA" or "NYY".'),
                score: z
                  .string()
                  .nullable()
                  .describe('Current or final score, null if not yet started.'),
              })
              .describe('Away team details and score.'),
            status: z
              .enum(['scheduled', 'in-progress', 'final', 'postponed', 'cancelled'])
              .describe('Game status.'),
            period: z
              .number()
              .nullable()
              .describe('Current period, quarter, or inning. Null if not started.'),
            clock: z
              .string()
              .nullable()
              .describe(
                'Game clock or inning half display (e.g. "2:34", "Top"). Null if not applicable.',
              ),
            startTimeUtc: z.string().describe('Game start time in UTC ISO 8601 format.'),
            venue: z.string().nullable().describe('Venue name, if available.'),
            source: z
              .enum(['espn', 'mlbstats'])
              .describe('Source provenance for this game record.'),
          })
          .describe('A single game record.'),
      )
      .describe('List of games for the requested date and league.'),
    date: z.string().describe('The effective date queried (YYYY-MM-DD).'),
    league: z.string().describe('The league queried.'),
    reason: z.string().optional().describe('Human-readable note when no games are found.'),
  }),
  enrichment: {
    emptyReason: z
      .enum(['no_games', 'no_team_matches'])
      .optional()
      .describe('Whether the provider slate was empty or the team filter removed all games.'),
    notice: z
      .string()
      .optional()
      .describe('Explanation of an empty result and the applied filter.'),
    coverage: z.string().optional().describe('College scoreboard coverage when applicable.'),
  },
  async handler(input, ctx) {
    ...
  },
  format: (result) => {
    ...
  },
});
```

> The `handler` and `format` bodies are abbreviated (`...`) above; the schema-bearing `description`, `annotations`, `input`, `output` and `enrichment` blocks are quoted in full. The `input`/`output` are authored as Zod and converted to the advertised JSON Schema by `@cyanheads/mcp-ts-core`.

## Evaluation Dimensions

### 1. Tool Description Clarity (for model tool-selection)
- [ ] The description states the capability ("Live and final scores for a league on a given provider-calendar date") and the return fields
- [ ] Ambiguous behaviors are spelled out (omitted dates use today's US Eastern day; NCAAB = men's Division I; NCAAF = FBS)
- [ ] Disambiguated from sibling tools (`sports_get_schedule`, `sports_get_game`, `sports_get_standings`)
- [ ] The optional team filter is described as a fuzzy match on name or abbreviation

### 2. Schema Correctness
- [ ] Valid JSON Schema generated from Zod (`type: "object"` inputs/outputs; `enum`s; `nullable()` for scores/period/clock)
- [ ] Types are accurate (`string`, `number`, `boolean`, `array`)
- [ ] The `league` enum is closed and explicit (13 league identifiers)
- [ ] Constraints are declared (`date` regex `^\d{4}-\d{2}-\d{2}$`; `team_name` `max(200)`)
- [ ] Required vs optional parameters are distinguishable (`date`, `team_name` optional)

### 3. Parameter Description Quality
- [ ] Every parameter has a Zod `.describe(...)`
- [ ] Supported enum values are listed inline in the `league` description
- [ ] Formats are documented (`YYYY-MM-DD`; UTC ISO 8601 for `startTimeUtc`)
- [ ] Empty-result semantics are documented and typed (`reason`, `emptyReason`, `notice`)

### 4. Integration Compatibility
- [ ] Conforms to the `@cyanheads/mcp-ts-core` `tool(name, {...})` API
- [ ] Read-only tools advertise `readOnlyHint`/`openWorldHint`
- [ ] Output schema is exposed alongside the input, enabling structured tool results
- [ ] No API keys required (ESPN and MLB StatsAPI are keyless; TheSportsDB ships a free key)

### 5. Extensibility & Maintainability
- [ ] One tool per file under `src/mcp-server/tools/definitions/`, aggregated by `definitions/index.ts`
- [ ] Cross-source league routing is centralized in `src/services/types.ts` (`LEAGUE_ROUTES`)
- [ ] Consistent `sports_<verb>` naming (`sports_get_scores`, `sports_find_team`, ...)
- [ ] Provider provenance is attached to every record (`source: 'espn' | 'mlbstats'`)

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
1. Issue "what were last night's NBA scores?"; verify `sports_get_scores` with `league: "nba"` and an appropriate `date`.
2. Issue "any MLB games today?"; verify `league: "mlb"` with `date` omitted (today's US Eastern day).
3. Issue "show the Seattle Mariners' game"; verify `team_name: "Seattle Mariners"` (or an abbreviation such as "SEA").

### Boundary Test Cases
1. `date` at a valid `YYYY-MM-DD` boundary (e.g. across a daylight-saving transition); verify the US Eastern calendar day handling.
2. `team_name` exactly 200 characters vs 201; verify the documented maximum.
3. A date with no games; verify the typed empty result (`emptyReason: "no_games"`, `reason`/`notice`).
4. A team filter that matches nothing; verify `emptyReason: "no_team_matches"`.
5. Each of the 13 `league` enum values.

### Negative Test Cases
1. `league` set to an unsupported value (e.g. `"ncaaw"` or `"premier"`); verify enum rejection.
2. `date` in a non-`YYYY-MM-DD` format (e.g. `"10/14/2026"`); verify regex rejection.
3. `sports_get_scores` missing the required `league`; verify schema validation rejects the call.
4. An in-progress game missing `period`/`clock`; verify those fields return `null` as documented rather than being absent.

## Notes
- This is one logical artifact: the `sports_get_scores` tool. The server exposes eight tools (`sports_find_team`, `sports_find_player`, `sports_get_scores`, `sports_get_game`, `sports_get_schedule`, `sports_get_standings`, `sports_get_team`, `sports_get_player`); `sports_get_scores` is quoted in full as representative.
- The `input`/`output` are authored as Zod schemas (`tool(name, { input: z.object({...}), output: z.object({...}) })`) and converted to JSON Schema by the framework; the verbatim Zod source is quoted as the schema source.
- License is Apache-2.0 (`LICENSE`: "Copyright 2026 Casey Hand @cyanheads"); long verbatim quotation is permissible.
