# TC-187: Fetch MCP Server - Tool Schema Evaluation Case

## Metadata
- **Source Project**: modelcontextprotocol/servers (reference server `src/fetch`, package `mcp-server-fetch`)
- **License**: MIT / Apache-2.0 (repository is transitioning from MIT to Apache-2.0; see `LICENSE`)
- **Artifact Type**: Tool Schema (MCP tool definition for the `fetch` tool)
- **Collection Date**: 2026-10-13
- **Collection Method**: Fetched verbatim from `raw.githubusercontent.com`, branch `main`:
  - `src/fetch/src/mcp_server_fetch/server.py` — the `Fetch` Pydantic model (source of the input schema) and the `Tool(...)` registration
  - `LICENSE` — confirmed MIT/Apache-2.0

## Original Artifact Content

### Input-schema model (`src/fetch/src/mcp_server_fetch/server.py`, fetched verbatim)

```python
class Fetch(BaseModel):
 """Parameters for fetching a URL."""

 url: Annotated[AnyUrl, Field(description="URL to fetch")]
 max_length: Annotated[
  int,
  Field(
   default=5000,
   description="Maximum number of characters to return.",
   # ge/le rather than gt/lt: the inclusive bounds emit minimum/maximum,
   # which every client accepts, while exclusiveMinimum/exclusiveMaximum
   # are rejected by some (Gemini, #1624). Same range for an int.
   ge=1,
   le=999999,
  ),
 ]
 start_index: Annotated[
  int,
  Field(
   default=0,
   description="On return output starting at this character index, useful if a previous fetch was truncated and more context is required.",
   ge=0,
  ),
 ]
 raw: Annotated[
  bool,
  Field(
   default=False,
   description="Get the actual HTML content of the requested page, without simplification.",
  ),
 ]
```

### Tool registration (`src/fetch/src/mcp_server_fetch/server.py`, fetched verbatim)

```python
 @server.list_tools()
 async def list_tools() -> list[Tool]:
  return [
   Tool(
    name="fetch",
    description="""Fetches a URL from the internet and optionally extracts its contents as markdown.

Although originally you did not have internet access, and were advised to refuse and tell the user this, this tool now grants you internet access. Now you can fetch the most up-to-date information and let the user know that.""",
    inputSchema=Fetch.model_json_schema(),
    # Reads only, changes nothing, and repeating a request has no
    # further side effect; it reaches arbitrary hosts on the
    # internet (#3572).
    annotations=ToolAnnotations(
     readOnlyHint=True,
     destructiveHint=False,
     idempotentHint=True,
     openWorldHint=True,
    ),
   )
  ]
```

## Evaluation Dimensions

### 1. Schema Completeness
- [ ] A single tool exposes a complete JSON Schema generated via `Fetch.model_json_schema()`
- [ ] Types are accurate (`AnyUrl`, `int`, `bool`)
- [ ] Defaults are declared for all optional fields (`max_length=5000`, `start_index=0`, `raw=False`)
- [ ] Bounds are declared as inclusive `minimum`/`maximum` (`ge=1`, `le=999999`, `ge=0`)

### 2. Description Clarity
- [ ] The tool description states what it does ("Fetches a URL from the internet and optionally extracts its contents as markdown")
- [ ] The description corrects the model's prior assumption that it lacks internet access
- [ ] Every field has a human-readable description, including the purpose of `start_index` for pagination

### 3. Integration Compatibility
- [ ] Schema is derived from a Pydantic model, guaranteeing valid JSON Schema
- [ ] A comment documents cross-client compatibility choices (inclusive bounds instead of `exclusiveMinimum`, which some clients such as Gemini reject)
- [ ] `ToolAnnotations` model side effects (`readOnlyHint=True`, `openWorldHint=True`)

### 4. Example Quality
- [ ] Pagination behavior is described textually and surfaced at runtime ("Call the fetch tool with a start_index of {next_start} to get more content")
- [ ] `raw` flag documents the alternative (unsimplified HTML) output mode
- [ ] The description explains the tool's role change so the model uses it confidently

### 5. Extensibility
- [ ] The schema is centralized in a single Pydantic `Fetch` model, reused for validation and schema emission
- [ ] A companion prompt (`fetch`) mirrors the tool for manual user-driven fetches
- [ ] Security-relevant configuration (`--allow-private-ips`, robots.txt handling) is external to the schema, keeping the tool surface minimal

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
1. Issue "summarize the content at https://example.com/article"; verify `fetch` is called with `url` and default `max_length`.
2. Issue "get the raw HTML of this page"; verify `raw: true` is set.
3. Issue "continue where you left off"; verify `start_index` is advanced based on the truncation notice.

### Boundary Test Cases
1. `max_length` at floor (1) and ceiling (999999).
2. A page longer than `max_length`; verify the truncation notice and `start_index` continuation.
3. `start_index` exactly equal to the content length; verify the "No more content available" behavior.
4. `url` provided in a scheme the client supports (http/https).

### Negative Test Cases
1. `fetch` without `url`; verify schema validation rejects the call.
2. `url` pointing at a private/loopback address; verify the server refuses per its SSRF guard.
3. `start_index` a negative integer; verify the `ge=0` bound rejects it.
4. A site whose robots.txt disallows autonomous fetching; verify the error is surfaced to the user with the manual-fetch suggestion.

## Notes
- This is the official MCP Fetch reference server. The single `fetch` tool is documented here as one logical artifact.
- The `inputSchema` is generated from the Pydantic `Fetch` model (`Fetch.model_json_schema()`); the model source is quoted verbatim so the schema can be reconstructed exactly.
- License is MIT/Apache-2.0; verbatim quotation is permissible.
