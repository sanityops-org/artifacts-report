# Entertainment Guide Agent

An intelligent assistant for discovering and managing movies and TV shows.

## Industry
Entertainment & Media

## Description
Entertainment Guide helps users discover movies and TV shows through personalized
recommendations, detailed title information, and watchlist management. All data is
simulated for demonstration purposes.

## Skills
- title_search: Search and discover movies/TV shows by title, actor, director, or genre
- recommendations: Personalized entertainment recommendations by genre or mood
- watchlist_management: Manage your personal watchlist and view reviews

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

# Verify setup
python scripts/setup.py

# Start Agent
python scripts/run.py
```

## Project Structure

```
Entertainment Guide/
├── prompts/          # System prompt
├── models/           # Pydantic domain models
├── apis/             # Search and recommendation engines
├── data/             # Simulated JSON data (30 titles, reviews)
├── skills/           # Skill definitions (3 skills)
├── tools/            # Executable tool scripts (10 tools, auto-scanned)
├── tests/            # Integration and contract tests
└── scripts/          # Startup and setup scripts
```

## Data Models

- **Title**: Movie or TV show with genres, cast, director, rating, and mood tags
- **WatchlistItem**: Watchlist entry with status (to_watch / watched) and optional user rating
- **Review**: User review with rating and comment

## Core Design Points

1. **All data is simulated**: No external API calls, local JSON only
2. **Unified tool interface**: Every tool returns `{"status", "data"|"error"}`
3. **Watchlist is session-scoped**: In-memory only, no PII written to disk
4. **Self-contained system prompt**: `system.txt` works without SKILL.md injection
5. **Platform-compatible**: Every tool declares a module-level JSON Schema `parameters`

## Tests

```bash
pip install pytest
python -m pytest
```

The suite covers model validation against the shipped data files, the search and recommendation
engines, the full watchlist flow through the tools, and two contract tests — one asserting the
system prompt still carries the three red lines and every tool name, one asserting each tool keeps
its schema and docstring shape.

The watchlist is held in memory for the session only, so restarting the agent clears it. Nothing
is written back to disk.

## Red Line Constraints

- **B1**: No streaming or playback — the agent cannot access actual content
- **B2**: No piracy — never suggest or link to illegal viewing options
- **B3**: Recommendations are suggestions based on simulated data, not real-time trends

## Run From This Repository

From the repository root:

```bash
cd test-cases/runnable-agent/entertainment-guide
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
# Edit .env and add the required model endpoint and credentials.
python scripts/setup.py
python scripts/run.py
```
