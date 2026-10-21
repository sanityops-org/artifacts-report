# TC-231: mcp_weather_server Tool Schema - Tool Schema Evaluation Case

## Metadata
- **Source Project**: isdaniel/mcp_weather_server
- **License**: Apache-2.0
- **Artifact Type**: Tool Schema (MCP tool definitions: name, description, JSON-Schema `inputSchema`)
- **Collection Date**: 2026-10-13
- **Collection Method**: Fetched raw files from `raw.githubusercontent.com`, `HEAD` of the default branch:
  - `src/mcp_weather_server/tools/tools_weather.py` (weather tool definitions) — `https://raw.githubusercontent.com/isdaniel/mcp_weather_server/HEAD/src/mcp_weather_server/tools/tools_weather.py`
  - `LICENSE` (license verification) — `https://raw.githubusercontent.com/isdaniel/mcp_weather_server/HEAD/LICENSE`
  - Repository file listing — `https://api.github.com/repos/isdaniel/mcp_weather_server/git/trees/HEAD?recursive=1`

## Original Artifact Content

Verbatim excerpt from `src/mcp_weather_server/tools/tools_weather.py` (the three weather tool definitions):

```python
class GetCurrentWeatherToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("get_current_weather")
        self.weather_service = WeatherService()

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="""Get current weather information for a specified city.
            It extracts the current hour's temperature and weather code, maps
            the weather code to a human-readable description, and returns a formatted summary.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The name of the city to fetch weather information for, PLEASE NOTE English name only, if the parameter city isn't English please translate to English before invoking this function."
                    }
                },
                "required": ["city"]
            }
        )
```

```python
class GetWeatherByDateRangeToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("get_weather_byDateTimeRange")
        self.weather_service = WeatherService()

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="""Get weather information for a specified city between start and end dates.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The name of the city to fetch weather information for, PLEASE NOTE English name only, if the parameter city isn't English please translate to English before invoking this function."
                    },
                    "start_date": {
                        "type": "string",
                        "description": "Start date in format YYYY-MM-DD, please follow ISO 8601 format"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "End date in format YYYY-MM-DD , please follow ISO 8601 format"
                    }
                },
                "required": ["city", "start_date", "end_date"]
            }
        )
```

```python
class GetWeatherDetailsToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("get_weather_details")
        self.weather_service = WeatherService()

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="""Get detailed weather information for a specified city as structured JSON data.
            This tool provides raw weather data for programmatic analysis and processing.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The name of the city to fetch weather information for, PLEASE NOTE English name only, if the parameter city isn't English please translate to English before invoking this function."
                    },
                    "include_forecast": {
                        "type": "boolean",
                        "description": "Whether to include forecast data (next 24 hours)",
                        "default": False
                    }
                },
                "required": ["city"]
            }
        )
```

Sibling tool modules in the same server: `tools_air_quality.py` (air-quality tools) and `tools_time.py` (time tools).

## Evaluation Dimensions

### 1. Tool Description Clarity (for model tool-selection)
- [ ] Each description states what the tool returns and when to use it
- [ ] Descriptions disambiguate the three tools (`get_current_weather` vs `get_weather_byDateTimeRange` vs `get_weather_details`)
- [ ] No marketing-only text that omits functional capability

### 2. JSON Schema Correctness
- [ ] Valid JSON Schema (`type: object`, `properties`, `required`) for each tool
- [ ] `required` lists are consistent with handler validation (`validate_required_args`)
- [ ] Types (`string`, `boolean`) and `default` values are accurate

### 3. Parameter Description Quality
- [ ] Every parameter has a human-readable `description`
- [ ] Date format (`YYYY-MM-DD` / ISO 8601) is documented inline
- [ ] The English-city-name constraint is stated on every `city` parameter
- [ ] `include_forecast` documents the meaning of `true` (next 24 hours)

### 4. Naming & Consistency
- [ ] Tool `name` values are unique and consistently cased
- [ ] The `get_weather_byDateTimeRange` name is consistent with its camelCase handler/identifier
- [ ] The `city` description is identical across all three tools

### 5. Extensibility & Maintainability
- [ ] Each tool is a self-contained handler class with a `get_tool_description()` accessor
- [ ] Schemas are declared statically (not dynamically generated)
- [ ] Tool registration is separated from business logic (`WeatherService`)

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Tool Description Clarity | 25% | | |
| JSON Schema Correctness | 25% | | |
| Parameter Description Quality | 20% | | |
| Naming & Consistency | 15% | | |
| Extensibility & Maintainability | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Issue "what's the weather in Tokyo right now?"; verify `get_current_weather` is selected with `city: "Tokyo"`.
2. Issue "give me the forecast for Berlin from 2026-11-01 to 2026-11-05"; verify `get_weather_byDateTimeRange` with valid ISO dates.
3. Issue "I need raw JSON weather data for Paris for analysis"; verify `get_weather_details` is selected.

### Boundary Test Cases
1. Non-English city input ("东京"); verify the model translates to English before invoking, per the `city` description.
2. `include_forecast: true`; verify the schema accepts the boolean and the tool returns forecast data.
3. Dates spanning multiple days / a single day; verify the range tool accepts equal start/end.

### Negative Test Cases
1. Call `get_weather_byDateTimeRange` without `start_date`; verify validation rejects the call.
2. Date string `"01/11/2026"` (non-ISO); verify the format expectation causes rejection or a corrective retry.
3. Ambiguous request "weather?" with no city; verify the model asks for a city rather than hallucinating one.

## Notes
- This server sources data from the Open-Meteo API (no API key required) but is a distinct project from the Open-Meteo-specific MCP servers already collected.
- The `get_weather_byDateTimeRange` name mixes snake_case and camelCase (`DateTimeRange`), which is worth flagging as a minor naming-consistency risk.
- License is Apache-2.0; verbatim quotation of the tool schemas is permissible.
