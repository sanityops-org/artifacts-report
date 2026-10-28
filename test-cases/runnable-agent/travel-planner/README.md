# Travel Planner Agent

An intelligent travel planning assistant that helps users plan trips by providing destination recommendations, itinerary creation, and travel resource information.

## Features

- **Destination Search**: Find destinations by name, country, or travel theme
- **Itinerary Planning**: Generate day-by-day travel itineraries
- **Accommodation Search**: Find hotels, hostels, resorts, and apartments
- **Budget Estimation**: Calculate approximate trip costs

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Copy `.env.example` to `.env` and configure your LLM API key:

```bash
cp .env.example .env
```

Edit `.env` and add your API key:
```
LLM_API_KEY=your-actual-api-key
```

## Usage

```bash
python scripts/run.py
```

## Example Conversations

**User**: I want to plan a beach vacation  
**Assistant**: I'd be happy to help you plan a beach vacation! Let me search for some great beach destinations for you.

**User**: Plan a 5-day trip to Paris  
**Assistant**: I'll create a 5-day itinerary for Paris with cultural attractions and activities.

**User**: How much will a week in Tokyo cost?  
**Assistant**: Let me estimate the budget for a 7-day trip to Tokyo.

## Data

All data is simulated for demonstration purposes. Prices and availability are approximate.

## Tests

```bash
pip install pytest
python -m pytest
```

The suite covers model validation against the shipped data files, the destination, itinerary, and
budget engines, the full search → itinerary → budget workflow through the tools, and two contract
tests — one asserting the system prompt still carries the three red lines and every tool name, one
asserting each tool keeps its schema and docstring shape.

Saved itineraries are held in memory for the session only, so restarting the agent clears them.
Nothing is written back to disk.

## Constraints

- No real bookings or reservations
- No visa/immigration advice
- Budget estimates are approximate

## Run From This Repository

From the repository root:

```bash
cd test-cases/runnable-agent/travel-planner
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
# Edit .env and add the required model endpoint and credentials.
python scripts/setup.py
python scripts/run.py
```
