# TC-245: OpenStreetMap / Nominatim MCP Server (cyanheads/nominatim-mcp-server) - Tool Schema Evaluation Case

## Metadata
- **Source Project**: cyanheads/nominatim-mcp-server (TypeScript MCP server for OpenStreetMap geocoding via Nominatim and Overpass)
- **License**: Apache License 2.0 (Copyright 2026 Casey Hand @cyanheads; `LICENSE`)
- **Artifact Type**: Tool Schema (MCP tool definition for the `openstreetmap_search_places` tool)
- **Collection Date**: 2026-10-14
- **Collection Method**: Fetched verbatim from `raw.githubusercontent.com`, branch `main`:
  - `src/mcp-server/tools/definitions/openstreetmap-search-places.tool.ts` — the `tool('openstreetmap_search_places', { title, description, annotations, input, output, enrichment, handler })` definition
  - `LICENSE` — confirmed Apache-2.0

## Original Artifact Content

### Input-mode schema fragment (`src/mcp-server/tools/definitions/openstreetmap-search-places.tool.ts`, fetched verbatim)

```typescript
const SEARCH_MODE_SCHEMA_META = {
  anyOf: [
    { type: 'object', required: ['query'] },
    { type: 'object', required: ['street'] },
    { type: 'object', required: ['city'] },
    { type: 'object', required: ['county'] },
    { type: 'object', required: ['state'] },
    { type: 'object', required: ['country'] },
    { type: 'object', required: ['postalcode'] },
  ],
};
```

### Tool definition — `openstreetmap_search_places` (`...openstreetmap-search-places.tool.ts`, fetched verbatim)

```typescript
export const openstreetmapSearchPlaces = tool('openstreetmap_search_places', {
  title: 'Geocode a place name or address',
  description:
    'Geocode a place name or address to coordinates and structured place data via Nominatim. Send either a free-form query or the structured address fields (street, city, county, state, country, postalcode), never both; results are the best-ranked matches, not every matching object, and matching never uses an OSM attribute tag, so filter or enumerate by tag with openstreetmap_query_nearby, openstreetmap_query_bbox, or openstreetmap_query_raw.',
  annotations: { readOnlyHint: true, idempotentHint: true, openWorldHint: true },
  input: z
    .object({
      query: z
        .string()
        .optional()
        .describe(
          'Free-form search string, e.g. "Space Needle Seattle" or "1600 Pennsylvania Ave NW, Washington DC". Not combinable with the structured address fields. Nominatim reads commas as an address hierarchy, so give the name plus its city or region and nothing in between: "Beinecke Library, New Haven" matches where "Beinecke Library, Yale University, New Haven" returns nothing.',
        ),
      street: z
        .string()
        .optional()
        .describe(
          'House number and street name (structured query). Use with city/state/country fields. Cannot be combined with query.',
        ),
      city: z.string().optional().describe('City name (structured query).'),
      county: z.string().optional().describe('County or district (structured query).'),
      state: z.string().optional().describe('State or province (structured query).'),
      country: z
        .string()
        .optional()
        .describe('Country name or ISO 3166-1 alpha-2 code (structured query).'),
      postalcode: z.string().optional().describe('Postal or ZIP code (structured query).'),
      limit: z
        .number()
        .int()
        .min(1)
        .max(40)
        .default(5)
        .describe(
          'Maximum results to return. Nominatim may return fewer when additional results do not sufficiently match. Max 40.',
        ),
      countrycodes: z
        .union([
          z.literal(''),
          z
            .string()
            .regex(NOMINATIM_COUNTRYCODE_PATTERN)
            .describe(
              'One ISO 3166-1 alpha-2 country code, or a comma-separated list of them, in any casing.',
            ),
        ])
        .optional()
        .describe(
          'Restrict results to one or more countries: comma-separated ISO 3166-1 alpha-2 codes (e.g. "us,ca"), any casing, optional spaces around the commas. Any other form — alpha-3, a semicolon list, a country name — is rejected rather than silently dropped upstream. A well-formed code for a country that does not exist matches nothing. An empty value counts as omitted. Prefer this over the structured country field for filtering.',
        ),
      viewbox: z
        .object({
          west: z
            .number()
            .min(-180)
            .max(180)
            .describe('Western boundary longitude. Must be strictly less than east.'),
          south: z
            .number()
            .min(-90)
            .max(90)
            .describe('Southern boundary latitude. Must be strictly less than north.'),
          east: z
            .number()
            .min(-180)
            .max(180)
            .describe('Eastern boundary longitude. Must be strictly greater than west.'),
          north: z
            .number()
            .min(-90)
            .max(90)
            .describe('Northern boundary latitude. Must be strictly greater than south.'),
        })
        .optional()
        .describe(
          'Rectangular area to bias results toward, disambiguating a name that repeats worldwide (a creek in one watershed, a street in one municipality). Narrower than countrycodes. Bias only by default: a better match outside the box is still returned. Set bounded for a hard restriction. Unlike openstreetmap_query_bbox this box may not cross the antimeridian — west must be less than east and south less than north, or the call is rejected.',
        ),
      bounded: z
        .boolean()
        .optional()
        .describe(
          'Restrict results to the viewbox instead of merely biasing toward it. Requires viewbox — setting it alone is rejected rather than ignored. With it, a match outside the box is dropped even when it scores higher.',
        ),
      layer: z
        .union([
          z.literal(''),
          z
            .string()
            .regex(NOMINATIM_LAYER_PATTERN)
            .describe(
              'One documented layer name, or a comma-separated list of them, in any casing.',
            ),
        ])
        .optional()
        .describe(
          `Filter by data layer: one of ${NOMINATIM_LAYER_VALUES}, or a comma-separated list of them, in any casing. Any other name is rejected here, not upstream; an empty value counts as omitted. Default: no restriction.`,
        ),
      featureType: z
        .enum(['country', 'state', 'city', 'settlement'])
        .optional()
        .describe(
          'Restrict results to a geographic feature type. Automatically implies the address layer.',
        ),
      extratags: z
        .boolean()
        .default(false)
        .describe(
          "Include the matched object's extra OSM tags — contact and metadata (phone, website, opening_hours, wikidata) and physical attributes (surface, tracktype, sac_scale, ele, access). An absent tag describes that object, not OpenStreetMap. Increases response size.",
        ),
      language: z
        .string()
        .optional()
        .describe(
          'Preferred language for result names (BCP 47 code or Accept-Language string, e.g., "en", "de", "fr,en"). Defaults to local OSM language.',
        ),
      exclude_place_ids: z
        .array(
          z
            .union([
              z.literal(''),
              z
                .string()
                .regex(NOMINATIM_EXCLUDE_ID_PATTERN)
                .describe('An OSM ref (N/W/R plus the object id) or a bare Nominatim place_id.'),
            ])
            .describe('One exclusion token, or an empty value that excludes nothing.'),
        )
        .optional()
        .describe(
          "OSM refs (N/W/R + id) or Nominatim place_ids to drop from results; any other token form is rejected here rather than by Nominatim. Entries are trimmed, lowercase ref prefixes uppercased, a blank entry treated as absent. Page toward further matches by passing back a prior full page's nextExcludeIds, which prefers stable OSM refs over volatile place_ids; the walk ends when a page returns zero results with an exhaustion notice — a success, not an error. Best-effort, not a cursor: Nominatim ranking can reorder between calls, so already-seen results may shift.",
        ),
    })
    .strict()
    .meta(SEARCH_MODE_SCHEMA_META),
  output: z.object({
    results: z.array(
      z.object({
        place_id: z.number().describe(
          'Nominatim internal place ID. Stable cross-server reference: osm_type+osm_id.',
        ),
        osm_type: z.enum(['node', 'way', 'relation']).optional().describe('OSM object type.'),
        osm_id: z.number().optional().describe(
          'OSM object ID. Combine with osm_type for openstreetmap_lookup_objects, or pass "R"/"W" + this id as within on openstreetmap_query_bbox ...',
        ),
        lat: z.number().describe('Latitude in WGS84 decimal degrees.'),
        lon: z.number().describe('Longitude in WGS84 decimal degrees.'),
        display_name: z.string().describe('Full human-readable address string.'),
        name: z.string().optional().describe('Feature name; absent for address-only results.'),
        /* ... category, type, importance, address, boundingbox, extratags ... */
      }).describe('A single geocoding result.'),
    ).describe('Geocoding results, ordered by Nominatim relevance (importance score descending).'),
    total: z.number().describe('Number of results returned.'),
    attribution: z
      .string()
      .describe('Required data attribution: Data © OpenStreetMap contributors, ODbL 1.0.'),
  }),
  enrichment: {
    effectiveQuery: z.string().describe(
      'The effective query sent to Nominatim — the free-form query string, or a reconstructed string from the provided structured address fields.',
    ),
    /* ... truncated, shown, cap, nextExcludeIds, notice, effectiveViewbox ... */
  },
  /* handler: z ... */
});
```

> To keep the quoted schema readable, a few `output` result fields (`category`, `type`, `importance`, `address`, `boundingbox`, `extratags`) and most `enrichment` fields (`effectiveQuery`, `truncated`, `shown`, `cap`, `nextExcludeIds`, `notice`, `effectiveViewbox`) are elided with `/* ... */` comments; the `input` object is quoted in full. Fields elided are summarized in `README.md` as structured place data, paging tokens (`nextExcludeIds`) and paging notices.

## Evaluation Dimensions

### 1. Tool Description Clarity (for model tool-selection)
- [ ] The description states the capability ("Geocode a place name or address to coordinates and structured place data via Nominatim")
- [ ] It states the two input modes and the mutual-exclusion rule ("Send either a free-form query or the structured address fields ... never both")
- [ ] It clarifies result semantics ("best-ranked matches, not every matching object") and that tags never filter matches
- [ ] It redirects tag-based work to sibling tools (`openstreetmap_query_nearby`, `..._query_bbox`, `..._query_raw`)

### 2. Schema Correctness
- [ ] Valid JSON Schema generated from Zod, with an added `anyOf` over required-sets (`.meta()`) so an empty-argument call is not advertised as valid
- [ ] `integer`-style constraint via `.int()` and `min`/`max` on `limit` (1–40, default 5)
- [ ] `enum` for `featureType`; regex-validated `countrycodes` and `layer`; numeric ranges on `viewbox`
- [ ] `.strict()` rejects undeclared properties
- [ ] The `anyOf` expresses "at least one mode field present" but not mutual exclusivity — the handler remains the enforcement point (documented in source comments)

### 3. Parameter Description Quality
- [ ] Every parameter has a `.describe(...)`, many including concrete examples ("Space Needle Seattle", `"us,ca"`)
- [ ] Non-obvious constraints are explained (`viewbox` may not cross the antimeridian; `bounded` requires `viewbox`; empty-string layers/countrycodes count as omitted)
- [ ] Formats are documented (ISO 3166-1 alpha-2; BCP 47 / Accept-Language; WGS84 decimal degrees)
- [ ] Required data attribution is stated and returned (`attribution`)

### 4. Integration Compatibility
- [ ] Conforms to the `@cyanheads/mcp-ts-core` `tool(name, {...})` API
- [ ] Read-only tools advertise `readOnlyHint`, `idempotentHint` and `openWorldHint`
- [ ] Typed error codes are surfaced (`conflicting_query_mode`, `missing_query_mode`) as tool results
- [ ] No API key required (Nominatim / Overpass are public)

### 5. Extensibility & Maintainability
- [ ] One tool per file under `src/mcp-server/tools/definitions/`, with shared schema fragments in `openstreetmap-nominatim-input.ts` / `openstreetmap-tag-input.ts`
- [ ] Services (Nominatim, Overpass) are isolated under `src/services/`
- [ ] Consistent `openstreetmap_<verb>` naming across the tool set
- [ ] `lint:mcp` enforces the `schema-anyof-needs-type` convention referenced in the source comments

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
1. Issue "where is the Space Needle?"; verify `openstreetmap_search_places` with a free-form `query: "Space Needle Seattle"`.
2. Issue "1600 Pennsylvania Ave NW, Washington DC"; verify a structured query (`street` + `city`/`state`) or an equivalent free-form `query` — not both.
3. Issue "find cities named Springfield"; verify `query: "Springfield"` with `featureType: "city"`.
4. Issue "search for 'Paris' but only in France"; verify `countrycodes: "fr"`.

### Boundary Test Cases
1. `limit` at its floor (1) and ceiling (40); verify bounds.
2. `limit` omitted; verify the documented default of 5.
3. `bounded: true` supplied without `viewbox`; verify the documented rejection rather than silent ignore.
4. A `viewbox` whose west ≥ east (antimeridian-crossing); verify rejection.
5. `countrycodes` with mixed casing and spaces (e.g. `"US, ca"`); verify it is normalized rather than rejected.

### Negative Test Cases
1. A call providing both `query` and `city`; verify the documented `conflicting_query_mode` rejection (the `anyOf` alone does not prevent it).
2. A call providing no mode field at all; verify the documented `missing_query_mode` rejection.
3. `countrycodes: "USA"` (alpha-3) or a country name; verify the regex rejection.
4. `layer: "banana"`; verify rejection at the tool boundary, not upstream.

## Notes
- This is one logical artifact: the `openstreetmap_search_places` tool (forward geocoding). The server also exposes `openstreetmap_reverse_geocode`, `openstreetmap_query_nearby`, `openstreetmap_query_bbox`, `openstreetmap_query_raw` and `openstreetmap_lookup_objects`.
- The `input`/`output` are authored as Zod schemas and converted to JSON Schema, with an injected `anyOf` fragment (via `.meta()`) that lands verbatim in the advertised `inputSchema`; the verbatim Zod source is quoted as the schema source per the rule for generated schemas.
- The repository publishes as `@cyanheads/nominatim-mcp-server` while the internal package/directory is named `openstreetmap-mcp-server`; both refer to the same project.
- License is Apache-2.0 (`LICENSE`: "Copyright 2026 Casey Hand @cyanheads"); long verbatim quotation is permissible.
