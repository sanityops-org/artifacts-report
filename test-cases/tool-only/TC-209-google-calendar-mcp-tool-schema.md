# TC-209: Google Calendar MCP Server - Tool Schema Evaluation Case

## Metadata
- **Source Project**: nspady/google-calendar-mcp (MCP server for the Google Calendar API)
- **License**: MIT (Copyright (c) 2025 nspady)
- **Artifact Type**: Tool Schema (MCP tool definition for the `list-events` tool)
- **Collection Date**: 2026-10-14
- **Collection Method**: Fetched verbatim from `raw.githubusercontent.com` / `cdn.jsdelivr.net`, branch `main`:
  - `src/tools/registry.ts` — the shared validation helpers and the `ToolSchemas['list-events']` Zod schema
  - `src/handlers/core/ListEventsHandler.ts` — the handler and its `ListEventsArgs` parameter interface
  - `src/server.ts` — the `ToolRegistry` import that registers the schemas
  - `LICENSE` — confirmed MIT

## Original Artifact Content

### Shared validation helpers (`src/tools/registry.ts`, fetched verbatim)

```typescript
import { z } from "zod";

// ============================================================================
// SHARED VALIDATION PATTERNS
// ============================================================================
// Note: We use validation functions instead of shared schemas to avoid $ref
// generation in JSON schema output, which can cause issues with some MCP clients.
const INVALID_TIME_ZONE_MESSAGE = "Must be an IANA time zone name, e.g. 'America/Los_Angeles' or 'Europe/London'";

// IANA time zone field. A factory, not a shared instance, to avoid $ref (see note above).
// Empty strings keep meaning "not provided" (handlers fall back to the calendar's zone).
const ianaTimeZone = () => z.string().refine(
  (timeZone) => timeZone === '' || isValidTimeZone(timeZone),
  INVALID_TIME_ZONE_MESSAGE
);

// ISO 8601 datetime regex patterns
const ISO_DATETIME_WITH_TZ = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(Z|[+-]\d{2}:\d{2})$/;
const ISO_DATETIME_WITHOUT_TZ = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$/;
const ISO_DATE_ONLY = /^\d{4}-\d{2}-\d{2}$/;

const timeMinSchema = z.string()
  .refine(isValidIsoDateTime, "Must be ISO 8601 format: '2026-01-01T00:00:00'")
  .describe("Start of time range (ISO 8601, e.g., '2024-01-01T00:00:00').")
  .optional();
const timeMaxSchema = z.string()
  .refine(isValidIsoDateTime, "Must be ISO 8601 format: '2026-01-01T00:00:00'")
  .describe("End of time range (ISO 8601, e.g., '2024-01-31T23:59:59').")
  .optional();
const timeZoneSchema = ianaTimeZone().optional().describe(
  "IANA timezone (e.g., 'America/Los_Angeles'). Defaults to calendar's timezone."
);

const fieldsSchema = z.preprocess(
  parseJsonStringArray,
  z.array(z.enum(ALLOWED_EVENT_FIELDS))
).optional().describe(
  "Additional fields to include beyond defaults (id, summary, start, end, status, htmlLink, location, attendees)."
);

const privateExtendedPropertySchema = z
  .array(z.string().regex(/^[^=]+=[^=]+$/, "Must be in key=value format"))
  .optional()
  .describe(
    "Filter by private extended properties (key=value). Matches events that have all specified properties."
  );
const sharedExtendedPropertySchema = z
  .array(z.string().regex(/^[^=]+=[^=]+$/, "Must be in key=value format"))
  .optional()
  .describe(
    "Filter by shared extended properties (key=value). Matches events that have all specified properties."
  );

// Multi-account schema - for read operations (list, search, get)
const multiAccountSchema = z.preprocess(
  parseJsonStringArray,
  z.union([
    z.string()
      .regex(accountIdRegex, "Account nickname must be 1-64 characters: lowercase letters, numbers, dashes, underscores only"),
    z.array(z.string()
      .regex(accountIdRegex, "Account nickname must be 1-64 characters: lowercase letters, numbers, dashes, underscores only"))
      .min(1, "At least one account nickname is required")
      .max(10, "Maximum 10 accounts allowed per request")
  ])
)
  .optional()
  .describe(
    "Account nickname(s) to query (e.g., 'work' or ['work', 'personal']). Omit to query all accounts."
  );
```

### Tool schema (`src/tools/registry.ts`, fetched verbatim)

```typescript
// Define all tool schemas with TypeScript inference
export const ToolSchemas = {
  'list-calendars': z.object({
    account: multiAccountSchema
  }),
  'list-events': z.object({
    account: multiAccountSchema,
    calendarId: z.union([
      z.string().describe(
        "Calendar identifier(s) to query. Accepts calendar IDs (e.g., 'primary', 'user@gmail.com') OR calendar names (e.g., 'Work', 'Personal'). Single calendar: 'primary'. Multiple calendars: array ['Work', 'Personal'] or JSON string '[\"Work\", \"Personal\"]'"
      ),
      z.array(z.string().min(1))
        .min(1, "At least one calendar ID is required")
        .max(50, "Maximum 50 calendars allowed per request")
        .refine(
          (arr) => new Set(arr).size === arr.length,
          "Duplicate calendar IDs are not allowed"
        )
        .describe("Array of calendar IDs to query events from (max 50, no duplicates)")
    ]),
    timeMin: timeMinSchema,
    timeMax: timeMaxSchema,
    timeZone: timeZoneSchema,
    fields: fieldsSchema,
    privateExtendedProperty: privateExtendedPropertySchema,
    sharedExtendedProperty: sharedExtendedPropertySchema
  }),
```

### Handler parameter interface (`src/handlers/core/ListEventsHandler.ts`, fetched verbatim)

```typescript
interface ListEventsArgs {
  calendarId: string | string[];
  timeMin?: string;
  timeMax?: string;
  timeZone?: string;
  fields?: string[];
  privateExtendedProperty?: string[];
  sharedExtendedProperty?: string[];
  account?: string | string[];
}
```

## Evaluation Dimensions

### 1. Schema Completeness
- [ ] The tool exposes a concrete Zod `inputSchema` (`ToolSchemas['list-events']`)
- [ ] Types are accurate and expressive (`union` of a calendar-id string or an array of strings; nested enums via `ALLOWED_EVENT_FIELDS`)
- [ ] Required vs optional is distinguishable (`calendarId` is required; the rest are `.optional()`)
- [ ] Constraints are declared (`max 50` calendars, no duplicates, `max 10` accounts, `key=value` regex)

### 2. Description Clarity
- [ ] The `calendarId` description explains all accepted forms (IDs, names, primary, array, JSON-string array)
- [ ] Time fields document ISO 8601 formats with concrete examples
- [ ] The `fields` description lists the default fields and explains the parameter's purpose
- [ ] Extended-property filters explain the matching semantics ("Matches events that have all specified properties")

### 3. Integration Compatibility
- [ ] Schemas are exported as a registry (`ToolSchemas`) consumed by `ToolRegistry` in `src/server.ts`
- [ ] Deliberately avoids `$ref` generation (a documented compatibility measure for RE2-based validators such as OpenAI/Gemini)
- [ ] Zod schemas are converted to JSON Schema by the MCP SDK, so they are consumable by MCP clients and function-calling LLMs

### 4. Example Quality
- [ ] Concrete examples are embedded throughout (`'primary'`, `'user@gmail.com'`, `'Work'`, `'America/Los_Angeles'`, `'2024-01-31T23:59:59'`)
- [ ] Union alternatives are shown explicitly (`['Work', 'Personal']` or the JSON-string form)
- [ ] The account description shows single and multi-account usage (`'work'` or `['work', 'personal']`)

### 5. Extensibility
- [ ] Field-level schemas (`timeMinSchema`, `timeZoneSchema`, `fieldsSchema`, ...) are reused across tools (`list-events`, `search-events`, ...)
- [ ] `parseJsonStringArray` preprocessing lets callers pass either native arrays or JSON-string arrays without schema duplication
- [ ] The schema registry and the handler interface (`ListEventsArgs`) mirror each other, keeping validation and execution aligned

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
1. Issue "what's on my calendar this week?"; verify `list-events` is called with a `calendarId` (e.g. `"primary"`) and a `timeMin`/`timeMax` pair in ISO 8601.
2. Issue "list events on the 'Work' calendar for January 2024 in Los Angeles time"; verify `calendarId: "Work"` and `timeZone: "America/Los_Angeles"`.
3. Issue "show events from both my Work and Personal calendars"; verify the `calendarId` array form (`["Work", "Personal"]`).

### Boundary Test Cases
1. `calendarId` as a JSON string array (`'["Work", "Personal"]'`); verify the union/preprocess accepts it.
2. An array of exactly 50 calendars (the maximum); verify acceptance, and that 51 is rejected.
3. An array containing duplicate calendar IDs; verify the `refine` rejects it ("Duplicate calendar IDs are not allowed").
4. `account` omitted; verify the documented behaviour (query all accounts) and that single vs array forms both validate.

### Negative Test Cases
1. Call `list-events` without `calendarId`; verify schema validation rejects the call.
2. `timeMin: "next Monday"` (non-ISO); verify the `refine` rejects it.
3. `timeZone: "GMT+2"` (not an IANA name); verify `isValidTimeZone` rejects it.
4. `privateExtendedProperty: ["project"]` (no `=`); verify the `key=value` regex rejects it.

## Notes
- This case quotes the `list-events` schema and its shared field schemas verbatim from `src/tools/registry.ts`, plus the matching handler interface from `src/handlers/core/ListEventsHandler.ts`. The schema is authored in Zod; `src/server.ts` imports `ToolRegistry` (which consumes `ToolSchemas`) and the MCP SDK converts the Zod schemas to JSON Schema, so the schema the LLM receives is generated from this source.
- Some referenced helpers (`isValidTimeZone`, `parseJsonStringArray`, `ALLOWED_EVENT_FIELDS`, `accountIdRegex`) are defined elsewhere in the same files; the schema composition that uses them is what is quoted verbatim.
- The server exposes many calendar tools (create/get/update/delete event, search-events, free-busy, list-calendars, ...); only the `list-events` tool is quoted here (one logical artifact per case).
- License is MIT; verbatim quotation is permissible.
