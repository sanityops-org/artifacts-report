# TC-189: OpenWeather MCP Server (Go) - Tool Schema Evaluation Case

## Metadata
- **Source Project**: mschneider82/mcp-openweather (MCP Weather Service, Go)
- **License**: MIT (Copyright (c) 2025 Matthias Schneider)
- **Artifact Type**: Tool Schema (MCP tool definition for the `weather` tool)
- **Collection Date**: 2026-10-13
- **Collection Method**: Fetched verbatim from `raw.githubusercontent.com`, branch `main`:
  - `main.go` — the `mcp.NewTool("weather", ...)` definition and handler
  - `LICENSE` — confirmed MIT

## Original Artifact Content

### Tool definition (`main.go`, fetched verbatim)

```go
	// Add tool
	tool := mcp.NewTool("weather",
		mcp.WithDescription("Retrieves current and forecast weather information for a given location."),
		mcp.WithString("city",
			mcp.Required(),
			mcp.Description(`The name of the city to get weather for.
Must be in English.
Example: For Saint Petersburg, use "Saint Petersburg", not "Санкт-Петербург".`),
		),
		mcp.WithString("units",
			mcp.DefaultString("c"),
			mcp.Description(`The unit for temperature. Use "c" for Celsius, "f" for Fahrenheit, or "k" for Kelvin. Default: "c".`),
		),
		mcp.WithString("lang",
			mcp.DefaultString("en"),
			mcp.Description(`The language for the weather description text. Use standard two-letter language codes (e.g., "en", "es", "zh_CN"). Default: "en".`),
		),
	)

	// Add tool handler
	s.AddTool(tool, weatherHandler)
```

### Server bootstrap (fetched verbatim, same file)

```go
	// Create MCP server
	s := server.NewMCPServer(
		"weather",
		"1.0.0",
	)
```

## Evaluation Dimensions

### 1. Schema Completeness
- [ ] The tool declares a name (`weather`) and description
- [ ] Parameters are fully typed as `string` (`city`, `units`, `lang`)
- [ ] Required (`city`) vs optional (`units`, `lang`) parameters are distinguished via `mcp.Required()` and `mcp.DefaultString(...)`
- [ ] Defaults are declared (`units="c"`, `lang="en"`)

### 2. Description Clarity
- [ ] The tool description states the capability (current + forecast weather)
- [ ] Each parameter documents accepted values (`"c"`, `"f"`, `"k"`; two-letter language codes)
- [ ] The `city` description gives an explicit example and a non-Latin-script caveat

### 3. Integration Compatibility
- [ ] Built with the `github.com/mark3labs/mcp-go` server framework (`server.NewMCPServer`, `mcp.NewTool`)
- [ ] The tool schema is standards-compliant and consumable by MCP clients and function-calling LLMs
- [ ] Returns a text result via `mcp.NewToolResultText`

### 4. Example Quality
- [ ] Concrete examples are embedded in descriptions ("Saint Petersburg", `"zh_CN"`)
- [ ] A JSON-RPC usage example is included in a trailing comment: `{"method":"tools/call","params":{"name":"weather","arguments":{"city":"Munich","lang":"de","units":"c"}},"jsonrpc":"2.0","id":9}`
- [ ] Output templates are declared (`weatherTemplateTxt`, `forecastTemplateTxt`) so the response shape is documented

### 5. Extensibility
- [ ] The API key is read from the `OWM_API_KEY` environment variable, keeping the tool surface free of credentials
- [ ] Units and language are parameterized rather than hard-coded
- [ ] Go template rendering separates data retrieval from presentation, easing output changes

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
1. Issue "what's the weather in Berlin?"; verify `weather` is called with `city: "Berlin"` (defaults for `units`/`lang`).
2. Issue "give me the 5-day forecast for Munich in Fahrenheit"; verify `city: "Munich"`, `units: "f"`.
3. Issue "éclaircis le temps à Paris" (French); verify `lang: "fr"` is set.

### Boundary Test Cases
1. `units` at each accepted value (`c`, `f`, `k`).
2. `lang` with a regional code such as `"zh_CN"`.
3. A city whose name has non-Latin script; verify it is transliterated to English per the description.
4. A city with multiple matches (e.g. "Springfield"); verify the response/geocoding behavior is clear.

### Negative Test Cases
1. `weather` without `city`; verify validation rejects the call.
2. `units: "x"`; verify the API/parameter handling errors rather than returning wrong units.
3. A nonexistent city; verify the documented "city not found" error path.
4. Missing `OWM_API_KEY`; verify the server fails fast with "FATAL: OWM_API_KEY environment variable not set".

## Notes
- This is a third-party Go MCP weather server. The single `weather` tool is documented here as one logical artifact; the schema is authored with the `mark3labs/mcp-go` fluent builder rather than raw JSON Schema.
- Because `units` and `lang` use free-form strings with documented value sets (rather than a formal `enum`), the schema relies on description text to constrain the model — a useful quality-discussion point.
- License is MIT; verbatim quotation is permissible.
