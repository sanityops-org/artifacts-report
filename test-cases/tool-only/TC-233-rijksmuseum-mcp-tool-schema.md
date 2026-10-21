# TC-233: rijksmuseum-mcp Tool Schema - Tool Schema Evaluation Case

## Metadata
- **Source Project**: r-huijts/rijksmuseum-mcp
- **License**: MIT
- **Artifact Type**: Tool Schema (MCP tool definitions: name, description, JSON-Schema `inputSchema`)
- **Collection Date**: 2026-10-13
- **Collection Method**: Fetched raw files from `raw.githubusercontent.com`, `HEAD` of the default branch:
  - `src/index.ts` (tool registration via `ListToolsRequestSchema`) — `https://raw.githubusercontent.com/r-huijts/rijksmuseum-mcp/HEAD/src/index.ts`
  - `LICENSE` (license verification) — `https://raw.githubusercontent.com/r-huijts/rijksmuseum-mcp/HEAD/LICENSE`
  - Repository file listing — `https://api.github.com/repos/r-huijts/rijksmuseum-mcp/git/trees/HEAD?recursive=1`

## Original Artifact Content

Verbatim excerpt from `src/index.ts` (the `search_artwork` tool definition):

```typescript
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: "search_artwork",
          description: "Search and filter artworks in the Rijksmuseum collection. This tool provides extensive filtering options including artist name, type of artwork, materials, techniques, time periods, colors, and more. Results can be sorted in various ways and are paginated.",
          inputSchema: {
            type: "object",
            properties: {
              q: {
                type: "string",
                description: "General search query that will match against artist names, artwork titles, descriptions, materials, techniques, etc. Use this for broad searches like 'sunflowers', 'portrait', 'landscape', etc."
              },
              involvedMaker: {
                type: "string",
                description: "Search for artworks by a specific artist. Must be case-sensitive and exact, e.g., 'Rembrandt+van+Rijn', 'Vincent+van+Gogh'. Use + for spaces in names."
              },
              type: {
                type: "string",
                description: "Filter by the type of artwork. Common values include 'painting', 'print', 'drawing', 'sculpture', 'photograph', 'furniture'. Use singular form."
              },
              material: {
                type: "string",
                description: "Filter by the material used in the artwork. Examples: 'canvas', 'paper', 'wood', 'oil paint', 'marble'. Matches exact material names from the museum's classification."
              },
              technique: {
                type: "string",
                description: "Filter by the technique used to create the artwork. Examples: 'oil painting', 'etching', 'watercolor', 'photography'. Matches specific techniques from the museum's classification."
              },
              century: {
                type: "integer",
                description: "Filter artworks by the century they were created in. Use negative numbers for BCE, positive for CE. Range from -1 (100-1 BCE) to 21 (2000-2099 CE). Example: 17 for 17th century (1600-1699).",
                minimum: -1,
                maximum: 21
              },
              color: {
                type: "string",
                description: "Filter artworks by predominant color. Use hexadecimal color codes without the # symbol. Examples: 'FF0000' for red, '00FF00' for green, '0000FF' for blue. The API will match artworks containing this color."
              },
              imgonly: {
                type: "boolean",
                description: "When true, only returns artworks that have associated images. Set to true if you need to show or analyze the visual aspects of artworks.",
                default: false
              },
              toppieces: {
                type: "boolean",
                description: "When true, only returns artworks designated as masterpieces by the Rijksmuseum. These are the most significant and famous works in the collection.",
                default: false
              },
              sortBy: {
                type: "string",
                enum: ["relevance", "objecttype", "chronologic", "achronologic", "artist", "artistdesc"],
                description: "Determines the order of results. Options: 'relevance' (best matches first), 'objecttype' (grouped by type), 'chronologic' (oldest to newest), 'achronologic' (newest to oldest), 'artist' (artist name A-Z), 'artistdesc' (artist name Z-A).",
                default: "relevance"
              },
              p: {
                type: "integer",
                description: "Page number for paginated results, starting at 0. Use in combination with 'ps' to navigate through large result sets. Note: p * ps cannot exceed 10,000.",
                minimum: 0,
                default: 0
              },
              ps: {
                type: "integer",
                description: "Number of artworks to return per page. Higher values return more results but take longer to process. Maximum of 100 items per page.",
                minimum: 1,
                maximum: 100,
                default: 10
              },
              culture: {
                type: "string",
                enum: ["nl", "en"],
                description: "Language for the search and returned data. Use 'en' for English or 'nl' for Dutch (Nederlands). Affects artwork titles, descriptions, and other text fields.",
                default: "en"
              }
            }
          }
        },
```

Verbatim excerpt from `src/index.ts` (the `get_artwork_details` tool schema):

```typescript
        {
          name: "get_artwork_details",
          description: "Retrieve comprehensive details about a specific artwork from the Rijksmuseum collection. Returns extensive information including:\n\n" +
                      "- Basic details (title, artist, dates)\n" +
                      "- Physical properties (dimensions, materials, techniques)\n" +
                      "- Historical context (dating, historical persons, documentation)\n" +
                      "- Visual information (colors, image data)\n" +
                      "- Curatorial information (descriptions, labels, location)\n" +
                      "- Acquisition details\n" +
                      "- Exhibition history\n\n" +
                      "This is the primary tool for in-depth research on a specific artwork, providing all available museum documentation and metadata.",
          inputSchema: {
            type: "object",
            properties: {
              objectNumber: {
                type: "string",
                description: "The unique identifier of the artwork in the Rijksmuseum collection. Format is typically a combination of letters and numbers (e.g., 'SK-C-5' for The Night Watch, 'SK-A-3262' for Van Gogh's Self Portrait). Case-sensitive. This ID can be obtained from search results."
              },
              culture: {
                type: "string",
                enum: ["nl", "en"],
                description: "Language for the artwork details. Use 'en' for English or 'nl' for Dutch (Nederlands). Affects all textual information including descriptions, titles, and historical documentation.",
                default: "en"
              }
            },
            required: ["objectNumber"]
          }
        },
```

Verbatim excerpt from `src/index.ts` (the `get_artist_timeline` tool definition):

```typescript
        {
          name: "get_artist_timeline",
          description: "Generate a chronological timeline of an artist's works in the Rijksmuseum collection. This tool is perfect for studying an artist's development, analyzing their artistic periods, or understanding their contribution to art history over time.",
          inputSchema: {
            type: "object",
            properties: {
              artist: {
                type: "string",
                description: "The name of the artist to create a timeline for. Must match the museum's naming convention (e.g., 'Rembrandt van Rijn', 'Vincent van Gogh'). Case sensitive and exact match required."
              },
              maxWorks: {
                type: "number",
                description: "Maximum number of works to include in the timeline. Works are selected based on significance and quality of available images. Higher numbers give a more complete picture but may include less significant works.",
                minimum: 1,
                maximum: 50,
                default: 10
              }
            },
            required: ["artist"]
          }
        }
```

Additional tools declared in the same `tools` array (names and one-line purpose): `get_artwork_image` (deep-zoom tile data), `get_user_sets` (Rijksstudio user collections), `get_user_set_details` (one user set), `open_image_in_browser` (open a high-res image URL).

## Evaluation Dimensions

### 1. Tool Description Clarity (for model tool-selection)
- [ ] Each description states what the tool returns and when to use it
- [ ] Descriptions disambiguate `search_artwork` from `get_artwork_details` and `get_artist_timeline`
- [ ] Long descriptions remain scannable and avoid duplicating parameter documentation

### 2. JSON Schema Correctness
- [ ] Valid JSON Schema (`type: object`, `properties`, `required`)
- [ ] `required` is set on tools that need an identifier (`get_artwork_details`) but omitted on `search_artwork` (search allows filtering by any field)
- [ ] Numeric bounds (`century` -1..21, `ps` 1..100, `maxWorks` 1..50) are declared
- [ ] `type` choices are consistent (`number` vs `integer` across tools)

### 3. Parameter Description Quality
- [ ] Every parameter has a human-readable `description`
- [ ] Defaults (`culture: "en"`, `p: 0`, `ps: 10`, `sortBy: "relevance"`) are documented
- [ ] Enum values are explained, not just listed
- [ ] Format constraints are stated (e.g. `color` hex without `#`, `involvedMaker` uses `+` for spaces, `objectNumber` case sensitivity)

### 4. Tool Identity & Pagination Consistency
- [ ] Tool `name` values are unique and stable (snake_case)
- [ ] Pagination parameters are named consistently (`p`/`ps` vs `page`/`pageSize` across tools)
- [ ] The `p * ps <= 10,000` limit is stated where pagination applies

### 5. Extensibility & Maintainability
- [ ] Tools are declared in a single list-handler block
- [ ] Business logic is delegated to a separate `ToolHandler`
- [ ] Language selection (`culture` enum) is applied uniformly across tools

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Tool Description Clarity | 25% | | |
| JSON Schema Correctness | 25% | | |
| Parameter Description Quality | 20% | | |
| Tool Identity & Pagination Consistency | 15% | | |
| Extensibility & Maintainability | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Issue "show me Rembrandt's paintings with images"; verify `search_artwork` with `involvedMaker: "Rembrandt+van+Rijn"`, `type: "painting"`, `imgonly: true`.
2. Issue "tell me everything about The Night Watch"; verify `get_artwork_details` with `objectNumber: "SK-C-5"` after a search.
3. Issue "timeline of Van Gogh's works here"; verify `get_artist_timeline` with `artist: "Vincent van Gogh"`.

### Boundary Test Cases
1. `century: -1` and `century: 21`; verify the boundary values are accepted per `minimum`/`maximum`.
2. `ps: 100` at maximum; verify accepted, and `ps: 0` rejected.
3. `sortBy` set to each enum member; verify all are accepted and undocumented ones rejected.

### Negative Test Cases
1. `get_artwork_details` without `objectNumber`; verify the required field is enforced.
2. `culture: "de"` (out of enum); verify rejection.
3. `involvedMaker: "van gogh"` (wrong case, no `+`); verify the documented exact-match expectation surfaces an empty/poor result rather than silently matching.

## Notes
- This artifact is the tool-selection surface an LLM sees for the Rijksmuseum collection server; it is a strong example of enum- and bound-rich schemas.
- Parameter documentation is notably rich (examples, units, format constraints), which makes it a good positive-control case for parameter-description quality.
- License is MIT; verbatim quotation of the tool schemas is permissible.
