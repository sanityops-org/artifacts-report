# TC-186: Time MCP Server - Tool Schema Evaluation Case

## Metadata
- **Source Project**: modelcontextprotocol/servers (reference server `src/time`, package `mcp-server-time`)
- **License**: MIT / Apache-2.0 (repository is transitioning from MIT to Apache-2.0; see `LICENSE`)
- **Artifact Type**: Tool Schema (MCP tool definitions: `get_current_time`, `convert_time`)
- **Collection Date**: 2026-10-13
- **Collection Method**: Fetched verbatim from `raw.githubusercontent.com`, branch `main`:
  - `src/time/src/mcp_server_time/server.py` — tool list handler with `Tool(...)` definitions
  - `LICENSE` — confirmed MIT/Apache-2.0

## Original Artifact Content

### Tool definitions (`src/time/src/mcp_server_time/server.py`, fetched verbatim)

```python
    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available time tools."""
        return [
            Tool(
                name=TimeTools.GET_CURRENT_TIME.value,
                description="Get current time in a specific timezone",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "timezone": {
                            "type": "string",
                            "description": f"IANA timezone name (e.g., 'America/New_York', 'Europe/London'). Use '{local_tz}' as local timezone if no timezone provided by the user.",
                        }
                    },
                    "required": ["timezone"],
                },
                annotations=ToolAnnotations(
                    readOnlyHint=True,
                    destructiveHint=False,
                    idempotentHint=True,
                    openWorldHint=False,
                ),
            ),
            Tool(
                name=TimeTools.CONVERT_TIME.value,
                description="Convert time between timezones",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "source_timezone": {
                            "type": "string",
                            "description": f"Source IANA timezone name (e.g., 'America/New_York', 'Europe/London'). Use '{local_tz}' as local timezone if no source timezone provided by the user.",
                        },
                        "time": {
                            "type": "string",
                            "description": "Time to convert in 24-hour format (HH:MM)",
                        },
                        "target_timezone": {
                            "type": "string",
                            "description": f"Target IANA timezone name (e.g., 'Asia/Tokyo', 'America/San_Francisco'). Use '{local_tz}' as local timezone if no target timezone provided by the user.",
                        },
                    },
                    "required": ["source_timezone", "time", "target_timezone"],
                },
                annotations=ToolAnnotations(
                    readOnlyHint=True,
                    destructiveHint=False,
                    idempotentHint=True,
                    openWorldHint=False,
                ),
            ),
        ]
```

### Enum and result models (fetched verbatim, same file)

```python
class TimeTools(str, Enum):
    GET_CURRENT_TIME = "get_current_time"
    CONVERT_TIME = "convert_time"

class TimeResult(BaseModel):
    timezone: str
    datetime: str
    day_of_week: str
    is_dst: bool

class TimeConversionResult(BaseModel):
    source: TimeResult
    target: TimeResult
    time_difference: str
```

## Evaluation Dimensions

### 1. Schema Completeness
- [ ] Both tools declare `type: "object"`, `properties`, and `required`
- [ ] Types are accurate (`string` for all parameters)
- [ ] Required parameters are marked (`timezone`; `source_timezone`, `time`, `target_timezone`)
- [ ] Return shape is modeled by `TimeResult` / `TimeConversionResult`, documenting the fields the model will receive

### 2. Description Clarity
- [ ] Each tool has a short functional description ("Get current time in a specific timezone", "Convert time between timezones")
- [ ] The `timezone` parameters explain the expected IANA format with examples
- [ ] The `time` parameter documents the exact format ("24-hour format (HH:MM)")

### 3. Integration Compatibility
- [ ] Uses the MCP `Tool` type with a raw JSON-Schema `inputSchema`
- [ ] `ToolAnnotations` (`readOnlyHint`, `idempotentHint`, `openWorldHint=False`) describe side-effect behavior
- [ ] Local timezone is injected into descriptions via `local_tz`, so the schema is environment-aware

### 4. Example Quality
- [ ] Concrete examples embedded in descriptions (`'America/New_York'`, `'Europe/London'`, `'Asia/Tokyo'`)
- [ ] The fallback instruction ("Use '{local_tz}' ... if no timezone provided by the user") gives the model a default policy
- [ ] Format for `time` is unambiguous

### 5. Extensibility
- [ ] Tool names are enumerated in a `TimeTools` enum, reducing string drift
- [ ] Shared result models (`TimeResult`) are reused between the two tools
- [ ] New time tools can reuse the `get_zoneinfo`/validation helpers

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
1. Issue "what time is it in Tokyo?"; verify `get_current_time` is called with `timezone: "Asia/Tokyo"`.
2. Issue "if it's 09:00 in New York, what time is it in Berlin?"; verify `convert_time` with `source_timezone`, `time`, `target_timezone`.
3. Issue "what's the local time?" with no timezone; verify the `local_tz` default guidance is followed.

### Boundary Test Cases
1. A fractional-offset timezone (e.g. `Asia/Kathmandu`, UTC+5:45); verify `convert_time` computes a fractional difference.
2. A DST spring-forward wall-clock time that does not exist; verify the documented error behavior.
3. Case-variant zone keys (e.g. `europe/warsaw`); verify the server rejects non-exact IANA keys.
4. `time` at `"00:00"` and `"23:59"`.

### Negative Test Cases
1. `convert_time` with `time: "9am"` (wrong format); verify it is rejected in favor of HH:MM.
2. `get_current_time` without `timezone`; verify validation rejects the call.
3. An invalid IANA name such as `"Mars/Olympus"`; verify an `INVALID_PARAMS` error is surfaced.
4. Ambiguous request "convert 3pm"; verify the model asks for the source/target timezones rather than guessing.

## Notes
- This is the official MCP Time reference server; the two tools are a tightly-related group defined in one `list_tools` handler and are documented as one logical artifact.
- The `inputSchema` is a literal JSON Schema; note that descriptions are f-strings interpolating `local_tz`, so the emitted schema text depends on the host's local timezone.
- License is MIT/Apache-2.0; verbatim quotation is permissible.
