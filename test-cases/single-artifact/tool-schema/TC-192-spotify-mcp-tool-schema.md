# TC-192: spotify-mcp (varunneal) - Tool Schema Evaluation Case

## Metadata
- **Source Project**: varunneal/spotify-mcp (MCP server connecting LLMs to the Spotify Web API)
- **License**: MIT (Copyright (c) 2025 Varun Neal Srivastava)
- **Artifact Type**: Tool Schema (MCP tool definition for the `SpotifySearch` tool)
- **Collection Date**: 2026-10-13
- **Collection Method**: Downloaded verbatim from `raw.githubusercontent.com`, branch `main`:
  - `src/spotify_mcp/server.py` — the `ToolModel` base class and the Pydantic `Search` model whose `model_json_schema()` becomes the tool `inputSchema`
  - `LICENSE` — confirmed MIT

## Original Artifact Content

### Tool construction base (`src/spotify_mcp/server.py`, fetched verbatim)

```python
class ToolModel(BaseModel):
    @classmethod
    def as_tool(cls):
        return types.Tool(
            name="Spotify" + cls.__name__,
            description=cls.__doc__,
            inputSchema=cls.model_json_schema()
        )
```

### The `Search` tool model (`src/spotify_mcp/server.py`, fetched verbatim)

```python
class Search(ToolModel):
    """Search for tracks, albums, artists, or playlists on Spotify."""
    query: str = Field(description="query term")
    qtype: Optional[str] = Field(default="track",
                                 description="Type of items to search for (track, album, artist, playlist, " +
                                             "or comma-separated combination)")
    limit: Optional[int] = Field(default=10, description="Maximum number of items to return")
```

### Tool registration (`src/spotify_mcp/server.py`, fetched verbatim)

```python
@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools."""
    logger.info("Listing available tools")
    tools = [
        Playback.as_tool(),
        Search.as_tool(),
        Queue.as_tool(),
        GetInfo.as_tool(),
        Playlist.as_tool(),
    ]
    logger.info(f"Available tools: {[tool.name for tool in tools]}")
    return tools
```

### Tool identity (derived from the source above)

- Registered tool name: `SpotifySearch` (the `as_tool()` classmethod prepends `"Spotify"` to the class name).
- Tool `description`: the class docstring, verbatim: `Search for tracks, albums, artists, or playlists on Spotify.`
- Tool `inputSchema`: generated at runtime by Pydantic `model_json_schema()` from the `Search` fields (a generated schema — labeled as such).

## Evaluation Dimensions

### 1. Schema Completeness
- [ ] The tool exposes a concrete input schema (generated from the `Search` Pydantic model)
- [ ] Types are accurate (`string`, `string`, `integer`)
- [ ] Required vs optional parameters are distinguishable (`query` required; `qtype`/`limit` have defaults)
- [ ] Defaults are declared (`qtype="track"`, `limit=10`)

### 2. Description Clarity
- [ ] The tool has a description (the class docstring)
- [ ] The description states the capability ("Search for tracks, albums, artists, or playlists")
- [ ] Field-level `description=` text is present for every field

### 3. Integration Compatibility
- [ ] Built with the official `mcp` Python SDK (`mcp.types.Tool`, `server.list_tools()`)
- [ ] The generated JSON Schema is consumable by MCP clients and function-calling LLMs
- [ ] The tool is registered in a single `handle_list_tools` list, alongside Playback/Queue/GetInfo/Playlist

### 4. Example Quality
- [ ] The `qtype` description enumerates valid values inline (track, album, artist, playlist, or a comma-separated combination)
- [ ] Optional fields are explicitly described as optional-by-default
- [ ] Sibling tools (`Playback`, `GetInfo`) provide `spotify_uri`-style usage examples for the same server

### 5. Extensibility
- [ ] A shared `ToolModel` base centralizes the `as_tool()` conversion, so every tool is defined once as a typed model
- [ ] Spotify credentials are read from environment variables (`SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`, `SPOTIFY_REDIRECT_URI`), keeping the tool surface credential-free
- [ ] Adding a tool requires only a new `ToolModel` subclass plus one list entry in `handle_list_tools`

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
1. Issue "search Spotify for tracks by Daft Punk"; verify `SpotifySearch` is called with `query: "Daft Punk"` (default `qtype: "track"`).
2. Issue "find playlists about lo-fi study music"; verify `query: "lo-fi study music"` and `qtype: "playlist"`.
3. Issue "show me the top 5 albums by Radiohead"; verify `qtype: "album"` and `limit: 5`.

### Boundary Test Cases
1. `limit` at the top of a practical range (e.g. 50) and at 1; verify the value passes through and result truncation is consistent.
2. `qtype` given as a comma-separated combination (e.g. `"track,album"`); verify the multi-type search path is exercised.
3. `query` as a very long free-text string; verify no truncation is applied silently.
4. `query` containing non-ASCII characters; verify encoding is preserved.

### Negative Test Cases
1. `SpotifySearch` without the required `query`; verify schema validation rejects the call.
2. `limit` provided as a string (e.g. `"ten"`); verify type validation rejects it.
3. An unknown tool name (not `Spotify*`); verify the handler's `assert name[:7] == "Spotify"` fails fast.
4. A request to play music when the user lacks Spotify Premium; verify the documented Spotify error path rather than a silent failure.

## Notes
- This is one logical artifact: the `SpotifySearch` tool. The server also exposes `SpotifyPlayback`, `SpotifyQueue`, `SpotifyGetInfo`, and `SpotifyPlaylist`.
- The `inputSchema` is **generated** at runtime by Pydantic's `model_json_schema()` from the `Search` model; the verbatim model source above is quoted and labeled as the schema source, per the task's rule for generated schemas.
- The upstream README notes the project is inactive as of March 2026 ("[Notice March 2026]: Inactive project"); the license (MIT) remains clear, so citation is permissible.
- License is MIT; verbatim quotation is permissible.
