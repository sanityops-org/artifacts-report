# TC-194: mcp-server-airbnb (openbnb-org) - Tool Schema Evaluation Case

## Metadata
- **Source Project**: openbnb-org/mcp-server-airbnb (MCP server for searching Airbnb listings)
- **License**: MIT (see `LICENSE`)
- **Artifact Type**: Tool Schema (MCP tool definition for the `airbnb_search` tool)
- **Collection Date**: 2026-10-13
- **Collection Method**: Downloaded verbatim from `raw.githubusercontent.com`, branch `main`:
  - `index.ts` — the `AIRBNB_SEARCH_TOOL` `Tool` object (raw JSON Schema `inputSchema`)
  - `LICENSE` — confirmed MIT
  - `README.md` — tool parameter documentation and behavior notes

## Original Artifact Content

### The `airbnb_search` tool (`index.ts`, fetched verbatim)

```typescript
// Tool definitions
const AIRBNB_SEARCH_TOOL: Tool = {
  name: "airbnb_search",
  description: "Search for Airbnb listings with various filters and pagination. Provide direct links to the user",
  inputSchema: {
    type: "object",
    properties: {
      location: {
        type: "string",
        description: "Location to search for (city, state, etc.)"
      },
      placeId: {
        type: "string",
        description: "Google Maps Place ID (overrides the location parameter)"
      },
      checkin: {
        type: "string",
        description: "Check-in date (YYYY-MM-DD)"
      },
      checkout: {
        type: "string",
        description: "Check-out date (YYYY-MM-DD)"
      },
      adults: {
        type: "number",
        description: "Number of adults"
      },
      children: {
        type: "number",
        description: "Number of children"
      },
      infants: {
        type: "number",
        description: "Number of infants"
      },
      pets: {
        type: "number",
        description: "Number of pets"
      },
      minPrice: {
        type: "number",
        description: "Minimum price for the stay"
      },
      maxPrice: {
        type: "number",
        description: "Maximum price for the stay"
      },
      cursor: {
        type: "string",
        description: "Base64-encoded string used for Pagination"
      },
      propertyType: {
        type: "string",
        enum: ["entire_home", "private_room", "shared_room", "hotel_room"],
        description: "Filter by property type: 'entire_home' (entire homes/apartments), 'private_room' (private rooms in shared homes), 'shared_room' (shared/dorm-style rooms), 'hotel_room' (hotel rooms)"
      },
      ignoreRobotsText: {
        type: "boolean",
        description: "Ignore robots.txt rules for this request"
      }
    },
    required: ["location"]
  }
};
```

### Tool registration (`index.ts`, fetched verbatim)

```typescript
const server = new Server(
    {
        name: "airbnb",
```

### Documented defaults (from `README.md`, fetched verbatim)

> - `location` (required): Location to search (e.g., "San Francisco, CA"). When supplied without `placeId`, the server geocodes this string client-side via Photon/Nominatim ...
> - `adults` (optional): Number of adults (default: 1)
> - `children` (optional): Number of children (default: 0)
> - `infants` (optional): Number of infants (default: 0)
> - `pets` (optional): Number of pets (default: 0)

## Evaluation Dimensions

### 1. Schema Completeness
- [ ] The tool exposes a concrete raw JSON Schema (`type: object`, `properties`, `required`)
- [ ] Types are accurate (`string`, `number`, `boolean`)
- [ ] Required vs optional parameters are distinguishable (`location` required; all others optional)
- [ ] Defaults are documented (README states `adults=1`, `children=0`, `infants=0`, `pets=0`)

### 2. Description Clarity
- [ ] The tool description states the capability and the desired output behavior ("Provide direct links to the user")
- [ ] Every parameter has a human-readable `description`
- [ ] `placeId` documents its interaction with `location` ("overrides the location parameter")

### 3. Integration Compatibility
- [ ] Built with the official `@modelcontextprotocol/sdk` `Server` class
- [ ] The raw JSON Schema is standards-compliant and consumable by MCP clients and function-calling LLMs
- [ ] Works as a stdio MCP server, also packaged as an MCPB bundle

### 4. Example Quality
- [ ] Concrete format examples are embedded (`YYYY-MM-DD`, "San Francisco, CA", "Google Maps Place ID")
- [ ] The `propertyType` enum enumerates all valid values with explanations
- [ ] Pagination is documented (`cursor` described as a Base64-encoded string)

### 5. Extensibility
- [ ] Tools are defined as discrete `Tool` objects, so the sibling `airbnb_listing_details` tool is added independently
- [ ] Geocoding opt-out is configuration (`DISABLE_GEOCODING` env var, `--ignore-robots-txt` flag), keeping the tool schema focused
- [ ] Robots.txt compliance and timeouts are enforced by the server rather than exposed as required arguments

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
1. Issue "find an Airbnb in San Francisco for 2 adults next weekend"; verify `airbnb_search` is called with `location: "San Francisco, CA"`, `adults: 2`, and valid `checkin`/`checkout`.
2. Issue "search entire homes in Copenhagen, Denmark"; verify `location: "Copenhagen, Denmark"` and `propertyType: "entire_home"`.
3. Issue "show a listing's details"; verify the model follows up with `airbnb_listing_details` using an `id` from the search results.

### Boundary Test Cases
1. Guest counts at default (omitted) and at explicit zero; verify the documented defaults are applied.
2. `minPrice`/`maxPrice` set to a narrow band; verify the filter is passed through.
3. Pagination: pass the `cursor` from a prior result; verify the next page is fetched.
4. `placeId` supplied together with `location`; verify `placeId` overrides `location`.

### Negative Test Cases
1. `airbnb_search` without the required `location` (and without `placeId`); verify validation rejects the call.
2. `propertyType: "villa"` (not in the enum); verify rejection.
3. `checkin`/`checkout` in a non-`YYYY-MM-DD` format; verify the call is rejected or handled per docs.
4. With robots.txt compliance enabled and a disallowed path; verify the request is not made (unless `ignoreRobotsText`/`--ignore-robots-txt` is set).

## Notes
- This is one logical artifact: the `airbnb_search` tool. The server also exposes `airbnb_listing_details` (quoted only for context).
- The `inputSchema` is an author-written raw JSON Schema (not generated from a type system), quoted verbatim from `index.ts`.
- The open-source server is not affiliated with Airbnb, Inc.; it respects robots.txt by default and may make client-side geocoding calls (Photon/Nominatim) when `placeId` is absent — a relevant schema-behavior interaction.
- License is MIT; verbatim quotation is permissible.
