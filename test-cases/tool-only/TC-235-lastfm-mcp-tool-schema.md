# TC-235: lastfm-mcp Tool Schema - Tool Schema Evaluation Case

## Metadata
- **Source Project**: rianvdm/lastfm-mcp
- **License**: MIT
- **Artifact Type**: Tool Schema (MCP tool definitions using Zod `inputSchema`)
- **Collection Date**: 2026-10-13
- **Collection Method**: Fetched raw files from `raw.githubusercontent.com`, `HEAD` of the default branch:
  - `src/mcp/tools/public.ts` (public/unauthenticated tool definitions) — `https://raw.githubusercontent.com/rianvdm/lastfm-mcp/HEAD/src/mcp/tools/public.ts`
  - `LICENSE` (license verification) — `https://raw.githubusercontent.com/rianvdm/lastfm-mcp/HEAD/LICENSE`
  - Repository file listing — `https://api.github.com/repos/rianvdm/lastfm-mcp/git/trees/HEAD?recursive=1`

## Original Artifact Content

Verbatim excerpt from `src/mcp/tools/public.ts` (selected tool registrations):

```typescript
export function registerPublicTools(server: McpServer, client: CachedLastfmClient, getBaseUrl: () => string): void {
        // ping - Test server connectivity
        server.registerTool(
                'ping',
                {
                        description: 'Test Last.fm MCP server connectivity - Use this to verify the server is working',
                        inputSchema: z.object({
                                message: z.string().optional().describe('Optional message to echo back'),
                        }),
                },
                async ({ message }) => { /* ... */ },
        )

        // server_info - Get server information
        server.registerTool(
                'server_info',
                {
                        description: 'Get Last.fm MCP server information and available capabilities',
                        inputSchema: z.object({}),
                },
                async () => { /* ... */ },
        )

        // get_track_info - Get detailed track information (public data)
        server.registerTool(
                'get_track_info',
                {
                        description:
                                'Get detailed Last.fm information about any track (artist, album, play count, tags, similar tracks) - No authentication required',
                        inputSchema: z.object({
                                artist: z.string().describe('Artist name'),
                                track: z.string().describe('Track name'),
                                username: z.string().optional().describe('Last.fm username (optional, for user-specific data)'),
                        }),
                },
                async ({ artist, track, username }) => { /* ... */ },
        )

        // get_artist_info - Get detailed artist information (public data)
        server.registerTool(
                'get_artist_info',
                {
                        description:
                                'Get detailed Last.fm information about any artist (biography, tags, similar artists, top tracks) - No authentication required',
                        inputSchema: z.object({
                                artist: z.string().describe('Artist name'),
                                username: z.string().optional().describe('Last.fm username (optional, for user-specific data)'),
                        }),
                },
                async ({ artist, username }) => { /* ... */ },
        )

        // get_album_info - Get detailed album information (public data)
        server.registerTool(
                'get_album_info',
                {
                        description: 'Get detailed Last.fm information about any album (track listing, tags, play counts) - No authentication required',
                        inputSchema: z.object({
                                artist: z.string().describe('Artist name'),
                                album: z.string().describe('Album name'),
                                username: z.string().optional().describe('Last.fm username (optional, for user-specific data)'),
                        }),
                },
                async ({ artist, album, username }) => { /* ... */ },
        )

        // get_artist_top_tracks - An artist's globally most-played tracks
        server.registerTool(
                'get_artist_top_tracks',
                {
                        description:
                                "Get an artist's globally most-played tracks on Last.fm (not user-specific) - No authentication required. Useful for finding canonical / signature songs by an artist.",
                        inputSchema: z.object({
                                artist: z.string().describe('Artist name'),
                                limit: z.coerce.number().min(1).max(50).optional().default(10).describe('Number of tracks to return (1-50)'),
                                mbid: z.string().optional().describe('MusicBrainz ID of the artist (optional, more reliable than name)'),
                        }),
                },
                async ({ artist, limit, mbid }) => { /* ... */ },
        )

        // get_similar_artists - Find similar artists
        server.registerTool(
                'get_similar_artists',
                {
                        description: 'Find artists similar to any artist using Last.fm data - No authentication required',
                        inputSchema: z.object({
                                artist: z.string().describe('Artist name'),
                                limit: z.coerce.number().min(1).max(100).optional().default(30).describe('Number of similar artists to return (1-100)'),
                        }),
                },
                async ({ artist, limit }) => { /* ... */ },
        )
```

Additional public tool declared in the same file: `get_artist_top_albums` (description: "Get an artist's globally most-played albums on Last.fm (not user-specific) - No authentication required. Useful for finding the canonical record by an artist."; schema: `artist`, `limit` 1-50 default 10, `mbid`). Authenticated tools live in `src/mcp/tools/authenticated.ts`.

## Evaluation Dimensions

### 1. Tool Description Clarity (for model tool-selection)
- [ ] Each description states what the tool returns and when to use it
- [ ] Descriptions disambiguate public vs authenticated behavior ("No authentication required")
- [ ] Descriptions note the non-user-specific nature of `get_artist_top_tracks`/`_albums`

### 2. JSON Schema Correctness
- [ ] Zod schemas compile to valid JSON Schema objects
- [ ] `optional()`/`default()` are applied consistently (`limit`, `mbid`, `username`)
- [ ] `z.coerce.number()` bounds (`min`/`max`) are declared for `limit`

### 3. Parameter Description Quality
- [ ] Every field has `.describe()`
- [ ] `limit` documents its range inline (e.g. "(1-50)") in addition to the Zod bounds
- [ ] `mbid` explains why it is preferred over a name ("more reliable than name")
- [ ] `username` documents its purpose (user-specific stats)

### 4. Tool Identity & Annotation Consistency
- [ ] Tool `name` values are unique, stable snake_case
- [ ] Related tools use parallel naming (`get_artist_top_tracks` / `get_artist_top_albums`)
- [ ] Read-only nature of public tools is implied by descriptions (no explicit annotations here)

### 5. Extensibility & Maintainability
- [ ] Public and authenticated tools are split into separate modules
- [ ] Shared client (`CachedLastfmClient`) and formatters are reused across tools
- [ ] Tools emit "next steps" breadcrumbs to guide chaining

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Tool Description Clarity | 25% | | |
| JSON Schema Correctness | 25% | | |
| Parameter Description Quality | 20% | | |
| Tool Identity & Annotation Consistency | 15% | | |
| Extensibility & Maintainability | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Issue "tell me about the song Bohemian Rhapsody by Queen"; verify `get_track_info` with `artist` and `track`.
2. Issue "who sounds like Radiohead?"; verify `get_similar_artists` with `artist: "Radiohead"` and an in-range `limit`.
3. Issue "what are Beyoncé's most-played songs?"; verify `get_artist_top_tracks` with `artist: "Beyoncé"`.

### Boundary Test Cases
1. `limit: 1` and `limit: 100` on `get_similar_artists`; verify the Zod bounds accept the edges and reject `0`/`101`.
2. Provide `mbid` instead of a name for an artist tool; verify it is accepted as the more reliable identifier.
3. Omit `username`; verify the response still succeeds and notes that personal stats require sign-in.

### Negative Test Cases
1. Call `get_track_info` without `track`; verify the required field is enforced.
2. `limit: 0` on `get_artist_top_albums`; verify the `.min(1)` bound rejects it.
3. Ambiguous request "play me something"; verify the model does not fabricate an artist/track and instead asks for one.

## Notes
- This artifact is the tool-selection surface an LLM sees for the Last.fm server's public (unauthenticated) tools.
- The schemas are expressed in Zod and surfaced to clients as JSON Schema by the MCP SDK; the tool descriptions embed strong chaining hints via breadcrumbs.
- License is MIT; verbatim quotation of the tool schemas is permissible.
