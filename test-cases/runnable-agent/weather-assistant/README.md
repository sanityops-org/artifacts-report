# Weather Assistant

An intelligent weather information assistant covering current conditions, multi-day forecasts, and
severe weather alerts.

## Industry
Meteorology / Public Safety

## Description
Weather Assistant answers natural-language questions about the weather in a set of simulated
locations. It reports current conditions, produces 1-7 day forecasts, and surfaces active severe
weather alerts ordered by severity. All data is local and simulated — no live weather service is
contacted.

## Skills
- weather_query: Location search, current conditions, and multi-day forecasts
- severe_weather: Active alerts, alerts by location, alert details, and alert subscription

## Creation Date
2026-10-09

## Version
v1.0.0

## Author
Agent Artifacts Team

## How to Run

**Prerequisites**: Ensure `sanityops_agent` framework is installed

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your LLM API key

# Start Agent
python scripts/run.py
```

## Project Structure

```
Weather Assistant/
├── prompts/          # System prompt
├── models/           # Pydantic domain models
├── apis/             # Data store, weather engine, alert engine
├── data/             # Simulated JSON data (10 locations, forecasts, alerts)
├── skills/           # Skill definitions (2 skills)
├── tools/            # Executable tool scripts (7 tools, auto-scanned)
├── tests/            # Integration and contract tests
└── scripts/          # Startup and setup scripts
```

## Data Models

- **Location**: A supported place with coordinates and elevation
- **CurrentConditions**: Latest observation for a location
- **DailyForecast**: One day of forecast with high/low and precipitation chance
- **Alert**: A severe weather alert with severity, affected areas, and validity window

## Core Design Points

1. **All data is simulated**: no external weather API is called (B1)
2. **No health advice**: the agent reports meteorological facts only, never medical guidance (B2)
3. **Alerts follow a fixed severity hierarchy**: warning > watch > advisory (B3)
4. **Unified tool interface**: every tool returns `{"status", "data"|"error"}`
5. **Self-contained system prompt**: works without SKILL.md injection on the platform
6. **Platform-compatible**: every tool declares a module-level JSON Schema `parameters`

## Tests

```bash
pip install pytest
python -m pytest
```

## Red Line Constraints

- **B1**: No real API calls — all data is simulated from local JSON
- **B2**: No health or medical advice
- **B3**: Alerts are always presented in severity order

## Run From This Repository

From the repository root:

```bash
cd test-cases/runnable-agent/weather-assistant
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
# Edit .env and add the required model endpoint and credentials.
python scripts/setup.py
python scripts/run.py
```
