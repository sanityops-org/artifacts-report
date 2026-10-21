# TC-206: Open-Meteo MCP Server - Tool Schema Evaluation Case

## Metadata
- **Source Project**: cmer81/open-meteo-mcp (MCP server for the Open-Meteo weather API)
- **License**: MIT (the `LICENSE` file reads "Copyright (c)" with the holder line left blank)
- **Artifact Type**: Tool Schema (MCP tool definition for the `weather_forecast` tool)
- **Collection Date**: 2026-10-14
- **Collection Method**: Fetched verbatim from `raw.githubusercontent.com` (and `cdn.jsdelivr.net` for large files), branch `main`:
  - `src/tools.ts` — the `WEATHER_FORECAST_TOOL` metadata (name, title, description, annotations)
  - `src/types.ts` — the shared Zod building blocks and the `ForecastParamsSchema` input schema
  - `src/index.ts` — the `registerReadOnlyTool(server, WEATHER_FORECAST_TOOL, ForecastParamsSchema, ...)` registration
  - `LICENSE` — confirmed MIT

## Original Artifact Content

### Tool metadata (`src/tools.ts`, fetched verbatim)

```typescript
export interface ToolDefinition {
  name: string;
  title: string;
  description: string;
  annotations: ToolAnnotations;
}

// All 17 tools are pure read-only queries against Open-Meteo endpoints.
const READ_ONLY_ANNOTATIONS = {
  readOnlyHint: true,
  destructiveHint: false,
  idempotentHint: true,
  openWorldHint: true,
} as const;

export const WEATHER_FORECAST_TOOL: ToolDefinition = {
  name: 'weather_forecast',
  title: 'Weather Forecast',
  annotations: READ_ONLY_ANNOTATIONS,
  description:
    'Get weather forecast data for coordinates using Open-Meteo API. Supports hourly and daily data with various weather variables. When no `models` parameter is provided, the API automatically selects the best model for the given location (recommended). Only one model per request is supported — for multi-model comparison, use provider-specific tools with parallel calls.',
};
```

### Shared parameter building blocks (`src/types.ts`, fetched verbatim)

```typescript
// Base parameter schemas
export const CoordinateSchema = z
  .object({
    latitude: z.number().min(-90).max(90),
    longitude: z.number().min(-180).max(180),
  })
  .strict();

export const TemperatureUnitSchema = z.enum(['celsius', 'fahrenheit']).default('celsius');
export const WindSpeedUnitSchema = z.enum(['kmh', 'ms', 'mph', 'kn']).default('kmh');
export const PrecipitationUnitSchema = z.enum(['mm', 'inch']).default('mm');
export const TimeFormatSchema = z.enum(['iso8601', 'unixtime']).default('iso8601');

export const CellSelectionSchema = z
  .enum(['land', 'sea', 'nearest'])
  .describe(
    'Grid cell to use near a coastline: prefer "land", prefer "sea", or the "nearest" cell.',
  );

export const TiltSchema = z
  .number()
  .min(0)
  .max(90)
  .describe(
    'Solar panel tilt in degrees (0 = flat, 90 = vertical); with `azimuth`, sets global_tilted_irradiance.',
  );

export const AzimuthSchema = z
  .number()
  .min(-180)
  .max(180)
  .describe(
    'Solar panel azimuth in degrees (0 = south, -90 = east, 90 = west, ±180 = north); used with `tilt`.',
  );

const DATE_FORMAT_MESSAGE = 'Must be a date in YYYY-MM-DD format (e.g. "2024-03-15").';
export const DateStringSchema = z
  .string()
  .regex(/^\d{4}-\d{2}-\d{2}$/, DATE_FORMAT_MESSAGE)
  .describe('Date in YYYY-MM-DD format.');
```

### Input schema (`src/types.ts`, fetched verbatim)

```typescript
export const ForecastParamsSchema = CoordinateSchema.extend({
  hourly: HourlyVariablesSchema,
  daily: DailyVariablesSchema,
  minutely_15: MinutelyVariablesSchema.describe(MINUTELY_15_DESCRIPTION),
  current_weather: z
    .boolean()
    .describe('Legacy current-conditions summary; prefer `current`.')
    .optional(),
  current: HourlyVariablesSchema.describe(CURRENT_DESCRIPTION),
  temperature_unit: TemperatureUnitSchema,
  wind_speed_unit: WindSpeedUnitSchema,
  precipitation_unit: PrecipitationUnitSchema,
  timeformat: TimeFormatSchema,
  timezone: TimezoneSchema.optional(),
  past_days: z.number().int().min(1).max(92).describe(PAST_DAYS_DESCRIPTION).optional(),
  past_hours: z.number().int().min(0).describe(PAST_HOURS_DESCRIPTION).optional(),
  forecast_days: z.number().int().min(1).max(16).describe(FORECAST_DAYS_DESCRIPTION).optional(),
  forecast_hours: z.number().int().min(0).describe(FORECAST_HOURS_DESCRIPTION).optional(),
  start_date: DateStringSchema.optional(),
  end_date: DateStringSchema.optional(),
  start_hour: HourlyTimestampSchema.optional(),
  end_hour: HourlyTimestampSchema.optional(),
  cell_selection: CellSelectionSchema.optional(),
  tilt: TiltSchema.optional(),
  azimuth: AzimuthSchema.optional(),
  models: ForecastModelsSchema,
});
```

### Registration (`src/index.ts`, fetched verbatim)

```typescript
    this.registerReadOnlyTool(
      server,
      WEATHER_FORECAST_TOOL,
      ForecastParamsSchema,
      (params: ForecastParams, signal) => this.client.getForecast(params, signal),
    );
```

## Evaluation Dimensions

### 1. Schema Completeness
- [ ] The tool exposes a concrete Zod `inputSchema` (`ForecastParamsSchema`) composed by extending `CoordinateSchema`
- [ ] Types and bounds are declared (`latitude` ±90, `longitude` ±180, `past_days` 1–92, `forecast_days` 1–16)
- [ ] Required vs optional is distinguishable (`.strict()` coordinates are required; most other fields are `.optional()` with defaults)
- [ ] A structured output serializer (`serializeToolResponse`) is applied to keep responses bounded

### 2. Description Clarity
- [ ] The tool describes what it does ("Get weather forecast data for coordinates using Open-Meteo API")
- [ ] It documents the default behaviour ("When no `models` parameter is provided, the API automatically selects the best model...")
- [ ] It states a constraint ("Only one model per request is supported") and a workaround ("use provider-specific tools with parallel calls")
- [ ] Shared fields carry `.describe(...)` text explaining their meaning (`cell_selection`, `tilt`, `azimuth`)

### 3. Integration Compatibility
- [ ] Registered through the MCP SDK via a shared `registerReadOnlyTool(...)` helper
- [ ] Declares `ToolAnnotations` (`readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`) for client-side risk display
- [ ] Zod schemas are converted to JSON Schema by the SDK, so they are consumable by MCP clients and function-calling LLMs

### 4. Example Quality
- [ ] Enum units are documented inline (`celsius`/`fahrenheit`, `kmh`/`ms`/`mph`/`kn`, `mm`/`inch`)
- [ ] Date formats include a concrete example (`"2024-03-15"`) via `DATE_FORMAT_MESSAGE`
- [ ] Deprecated fields are flagged with a preferred replacement (`current_weather` → "prefer `current`")

### 5. Extensibility
- [ ] Tool metadata (`ToolDefinition`) is separated from the Zod parameter schemas, so descriptions and schemas evolve independently
- [ ] Shared building-block schemas (`CoordinateSchema`, unit schemas, `DateStringSchema`) are reused across all 17 tools
- [ ] Provider-specific tools reuse `ForecastParamsSchema.omit({ models: true }).extend({ models: ... })`, so only the model namespace changes per provider

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
1. Issue "will it rain in Berlin tomorrow?"; verify `weather_forecast` is called with `latitude`/`longitude` (via geocoding) and `daily`/`hourly` variables.
2. Issue "forecast for Paris for the next 3 days in Fahrenheit"; verify `forecast_days: 3` and `temperature_unit: "fahrenheit"`.
3. Issue "give me the hourly forecast for 2026-10-15 in New York"; verify `start_date`/`end_date` are ISO dates.

### Boundary Test Cases
1. `latitude: 90` / `longitude: 180` and the negative extremes; verify the bounds are respected and out-of-range values are rejected.
2. `past_days: 92` and `forecast_days: 16` (maximums); verify acceptance, and that `93` / `17` are rejected.
3. Omit `models`; verify the server relies on the documented automatic model selection.
4. Provide both `timezone` and `cell_selection`; verify both optional fields are accepted.

### Negative Test Cases
1. Call without `latitude`/`longitude`; verify the `.strict()` coordinate schema rejects the call.
2. `models` set to two models simultaneously; verify the "only one model per request" constraint is enforced.
3. `start_date` set to `"15/03/2026"`; verify the `YYYY-MM-DD` regex rejects it.
4. `temperature_unit: "kelvin"` (out of enum); verify rejection.

## Notes
- This case quotes the `weather_forecast` tool, its shared parameter building blocks, and the `ForecastParamsSchema` verbatim. The metadata lives in `src/tools.ts` and the Zod parameter schemas in `src/types.ts`; `src/index.ts` wires them together via `registerReadOnlyTool`.
- Some referenced sub-schemas (`HourlyVariablesSchema`, `DailyVariablesSchema`, `TimezoneSchema`, `ForecastModelsSchema`) are defined elsewhere in `src/types.ts` and are referenced but not quoted here; the composition (`CoordinateSchema.extend({...})`) is what is quoted verbatim.
- The server exposes 17 read-only tools; only the primary `weather_forecast` tool is quoted here (one logical artifact per case).
- License is MIT; the `LICENSE` file's copyright holder line is blank, so the holder is not asserted here. Verbatim quotation is permissible.
