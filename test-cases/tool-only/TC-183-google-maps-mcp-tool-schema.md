# TC-183: Google Maps MCP Server - Tool Schema Evaluation Case

## Metadata
- **Source Project**: modelcontextprotocol/servers-archived (reference server `src/google-maps`)
- **License**: MIT (Copyright (c) 2024 Anthropic, PBC)
- **Artifact Type**: Tool Schema (MCP tool definitions: `maps_geocode`, `maps_reverse_geocode`, `maps_search_places`, `maps_place_details`, `maps_distance_matrix`, `maps_elevation`, `maps_directions`)
- **Collection Date**: 2026-10-13
- **Collection Method**: Fetched verbatim from `raw.githubusercontent.com`, branch `main`:
  - `src/google-maps/index.ts` — tool definitions, request handler and server setup
  - `LICENSE` — confirmed MIT

## Original Artifact Content

### Tool definitions (`src/google-maps/index.ts`, fetched verbatim)

```typescript
// Tool definitions
const GEOCODE_TOOL: Tool = {
    name: "maps_geocode",
    description: "Convert an address into geographic coordinates",
    inputSchema: {
      type: "object",
      properties: {
        address: {
          type: "string",
          description: "The address to geocode"
        }
      },
      required: ["address"]
    }
  };

const REVERSE_GEOCODE_TOOL: Tool = {
  name: "maps_reverse_geocode",
  description: "Convert coordinates into an address",
  inputSchema: {
    type: "object",
    properties: {
      latitude: {
        type: "number",
        description: "Latitude coordinate"
      },
      longitude: {
        type: "number",
        description: "Longitude coordinate"
      }
    },
    required: ["latitude", "longitude"]
  }
};

const SEARCH_PLACES_TOOL: Tool = {
  name: "maps_search_places",
  description: "Search for places using Google Places API",
  inputSchema: {
    type: "object",
    properties: {
      query: {
        type: "string",
        description: "Search query"
      },
      location: {
        type: "object",
        properties: {
          latitude: { type: "number" },
          longitude: { type: "number" }
        },
        description: "Optional center point for the search"
      },
      radius: {
        type: "number",
        description: "Search radius in meters (max 50000)"
      }
    },
    required: ["query"]
  }
};

const PLACE_DETAILS_TOOL: Tool = {
  name: "maps_place_details",
  description: "Get detailed information about a specific place",
  inputSchema: {
    type: "object",
    properties: {
      place_id: {
        type: "string",
        description: "The place ID to get details for"
      }
    },
    required: ["place_id"]
  }
};

const DISTANCE_MATRIX_TOOL: Tool = {
  name: "maps_distance_matrix",
  description: "Calculate travel distance and time for multiple origins and destinations",
  inputSchema: {
    type: "object",
    properties: {
      origins: {
        type: "array",
        items: { type: "string" },
        description: "Array of origin addresses or coordinates"
      },
      destinations: {
        type: "array",
        items: { type: "string" },
        description: "Array of destination addresses or coordinates"
      },
      mode: {
        type: "string",
        description: "Travel mode (driving, walking, bicycling, transit)",
        enum: ["driving", "walking", "bicycling", "transit"]
      }
    },
    required: ["origins", "destinations"]
  }
};

const ELEVATION_TOOL: Tool = {
  name: "maps_elevation",
  description: "Get elevation data for locations on the earth",
  inputSchema: {
    type: "object",
    properties: {
      locations: {
        type: "array",
        items: {
          type: "object",
          properties: {
            latitude: { type: "number" },
            longitude: { type: "number" }
          },
          required: ["latitude", "longitude"]
        },
        description: "Array of locations to get elevation for"
      }
    },
    required: ["locations"]
  }
};

const DIRECTIONS_TOOL: Tool = {
  name: "maps_directions",
  description: "Get directions between two points",
  inputSchema: {
    type: "object",
    properties: {
      origin: {
        type: "string",
        description: "Starting point address or coordinates"
      },
      destination: {
        type: "string",
        description: "Ending point address or coordinates"
      },
      mode: {
        type: "string",
        description: "Travel mode (driving, walking, bicycling, transit)",
        enum: ["driving", "walking", "bicycling", "transit"]
      }
    },
    required: ["origin", "destination"]
  }
};

const MAPS_TOOLS = [
  GEOCODE_TOOL,
  REVERSE_GEOCODE_TOOL,
  SEARCH_PLACES_TOOL,
  PLACE_DETAILS_TOOL,
  DISTANCE_MATRIX_TOOL,
  ELEVATION_TOOL,
  DIRECTIONS_TOOL,
] as const;
```

### Server / list-tools wiring (fetched verbatim, same file)

```typescript
// Server setup
const server = new Server(
  {
    name: "mcp-server/google-maps",
    version: "0.1.0",
  },
  {
    capabilities: {
      tools: {},
    },
  },
);

// Set up request handlers
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: MAPS_TOOLS,
}));
```

## Evaluation Dimensions

### 1. Schema Completeness
- [ ] Every tool declares `type: "object"`, `properties`, and `required`
- [ ] Types are accurate (`string`, `number`, `array`, nested `object`)
- [ ] Required vs optional parameters are marked (e.g. `location`/`radius` optional in `maps_search_places`)
- [ ] `maps_distance_matrix` and `maps_directions` share a consistent `mode` enum

### 2. Description Clarity
- [ ] Each tool has a one-line functional description
- [ ] Parameter descriptions are present for the principal arguments
- [ ] Enumerated values are explained inline (`mode` lists driving/walking/bicycling/transit)

### 3. Integration Compatibility
- [ ] Declared via the MCP `Tool` type and returned by `ListToolsRequestSchema`
- [ ] JSON-Schema-based `inputSchema` is directly usable by MCP clients and function-calling LLMs
- [ ] Tool names are namespaced with a `maps_` prefix, avoiding collisions with other servers

### 4. Example Quality
- [ ] Parameter descriptions give acceptable input forms ("address or coordinates")
- [ ] Bounds are hinted (`radius` "max 50000")
- [ ] Related tools (geocode → details → directions) form a discoverable workflow

### 5. Extensibility
- [ ] Tools are separated into individual `const` definitions and collected in a `MAPS_TOOLS` array
- [ ] Adding a tool requires only a new definition + array entry + `switch` case
- [ ] Nested object shapes (`location`, `locations[]`) demonstrate reusable sub-schema patterns

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
1. Issue "what are the coordinates of the Eiffel Tower?"; verify `maps_geocode` is called with `address`.
2. Issue "how long does it take to drive from Berlin to Munich?"; verify `maps_distance_matrix` with `origins`, `destinations` and `mode: "driving"`.
3. Issue "get me directions from the airport to the hotel by transit"; verify `maps_directions` with `origin`, `destination`, `mode: "transit"`.

### Boundary Test Cases
1. `maps_search_places` with `location` and `radius` provided vs omitted; verify optional handling.
2. `maps_distance_matrix` with multiple origins and destinations (arrays).
3. `maps_elevation` with several coordinate pairs in `locations[]`.
4. `radius` at its documented maximum (50000 meters).

### Negative Test Cases
1. `maps_geocode` without `address`; verify rejection.
2. `maps_directions` with `mode: "flying"` (out of enum); verify rejection.
3. `maps_place_details` without `place_id`; verify rejection.
4. Ambiguous request "where is it?" that lacks a resolvable place; verify the model requests clarification rather than fabricating coordinates.

## Notes
- This server is an archived MCP reference implementation; it is quoted verbatim from `src/google-maps/index.ts`. The seven tools together form one tightly-related tool group from a single file, so they are documented as one logical artifact.
- The schemas here are hand-written JSON Schema (not code-generated), which makes them a clean example of explicit `inputSchema` authoring.
- License is MIT; long verbatim quotation is permissible.
