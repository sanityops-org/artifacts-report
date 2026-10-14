# TC-098: Travel Planner - Multi-Logical-Artifact Suite Evaluation Case

## Metadata
- **Source Project**: travel-planner (rupakc/travel-planner)
- **Submodule**: `.agents/*.md` (21 agent definition files) + `backend/app/agents/*.py` (agent implementations)
- **License**: MIT
- **Artifact Type**: Multi-Agent suite (21 roles × system prompt definitions + tool schemas)
- **Collection Date**: 2026-10-13
- **Collection Method**: GitHub README + raw source retrieval, exact URLs:
  - `https://github.com/rupakc/travel-planner`
  - `https://raw.githubusercontent.com/rupakc/travel-planner/main/.agents/flights.md`
  - `https://raw.githubusercontent.com/rupakc/travel-planner/main/backend/app/agents/itinerary_agent.py`
  - `https://raw.githubusercontent.com/rupakc/travel-planner/main/backend/app/agents/loader.py`
  - `https://api.github.com/repos/rupakc/travel-planner/contents/.agents` (directory listing)

---

## Project Overview

Travel Planner is an **AI-powered end-user trip planning application** (MIT). It uses a team of specialist AI agents that run in parallel to produce a complete trip plan — flights, hotels, activities, visa rules, packing list, emergency contacts, and a day-by-day itinerary — in a single structured, streaming response. The app is live and free to use.

From the project README (verbatim):

> "The app uses a team of specialist AI agents that all run at the same time. Results start appearing on screen within seconds and keep arriving as each agent finishes."

> "**AI** — Anthropic Claude via the Agent SDK, 21 specialist agent definitions (12 parallel search agents, deferred pricing/packing agents, itinerary + adversarial health-check synthesis, chat, layover, and destination discovery)"

### Agent Role Inventory (from README "How it works")

| Phase | Roles | Notes |
|-------|-------|-------|
| **Phase 0 (instant, no AI)** | Pre-computed lookup tables (visa, SIM, tips, emergency, getting-around, confidence score) | static fallback data |
| **Phase 1 (12 parallel agents)** | FlightsAgent, HotelsAgent, ActivitiesAgent, PlacesAgent, VisaAgent, SimAgent, TipsAgent, ForexAgent, GettingAroundAgent, WeatherAgent, EmergencyCardAgent, EventsAgent | run simultaneously, stream as each finishes |
| **Deferred agents** | PricingAdvisorAgent (triggers ≥3 flight prices), PackingListAgent (triggers activities + weather) | start when inputs land |
| **Phase 2 (synthesis)** | ItineraryAgent (day-by-day plan), StressTestAgent (adversarial audit) | itinerary reads hotels + ranked activities |
| **Others** | ChatAgent, LayoverAgent, DiscoveryAgent, Orchestrator | chat / layover optimizer / "Surprise Me" discovery |

---

## Logical Artifact Inventory

### 1. System Prompt Definitions (21 files in `.agents/*.md`, YAML frontmatter + markdown body)

The loader (`backend/app/agents/loader.py`, verbatim) shows the definition format:

```python
@dataclass
class AgentDefinition:
    name: str
    description: str
    tools: list[str] = field(default_factory=list)
    max_turns: int = 5
    system_prompt: str = ""
```

> "Load agent definition from `.agents/<name>.md` … Parse YAML frontmatter (between `---` markers)".

#### 1.1 FlightsAgent — `flights.md` (verbatim excerpt)

```markdown
---
name: flights
description: Expert flight search specialist — finds available round-trip flights with outbound and return legs, prices, airlines, and booking options using multiple sources
tools: WebSearch, WebFetch
max_turns: 4
---
You are an expert flight search specialist for a travel planning application.
## Your Task
Search for **round-trip flights** (outbound AND return) on the given route and return structured results sorted by total price (cheapest first). If no return date is given, search one-way only.
## Search Strategy
Perform 5 targeted searches across multiple platforms:
1. `site:skyscanner.com round trip flights [ORIGIN] to [DESTINATION] [DEPARTURE DATE] return [RETURN DATE]`
2. `site:google.com/travel/flights [ORIGIN] to [DESTINATION] round trip [DEPARTURE DATE] [RETURN DATE]`
3. `cheap round trip flights [ORIGIN] to [DESTINATION] [MONTH YEAR]`
4. `[ORIGIN] [DESTINATION] round trip airline deals price`
5. `best airlines [ORIGIN] [DESTINATION] direct non-stop round trip`
...
## Output Format
Return ONLY a valid JSON object — no prose, no markdown, no explanation:
{
  "results": [
    {
      "price_usd": 1200.0,
      "trip_type": "round_trip",
      "booking_url": "https://www.google.com/travel/flights",
      "source": "google_flights",
      "outbound": { ... },
      "return": { ... }
    }
  ]
}
...
Include 8–12 options from different airlines and sources. **Sort by price_usd ascending** (cheapest first).
```

#### 1.2 ItineraryAgent — inline prompt in `itinerary_agent.py` (verbatim excerpt)

```python
prompt = (
    f"Create a day-by-day travel itinerary for {request.destination} (identify the country).\n"
    f"Traveling from: {request.origin}\n"
    f"Trip dates: {request.departure_date} to {request.return_date} ({nights} nights)\n"
    f"Travelers: {request.traveler_context}\n"
    f"Interests: {interests_str}\n"
    f"Pacing: {pace_guidance}\n"
    f"Hotel: {hotel_name}\n\n"
    f"Available activities:\n{activities_summary}\n\n"
    f"Create a {nights + 1}-day itinerary (arrival day through departure day).\n"
    f"Each day: exactly 3 time slots (morning, afternoon, evening).\n"
    f"Day 1 = arrival from {request.origin}. Last day = departure back to {request.origin}.\n"
    f"Include daily_estimated_cost_usd and total_estimated_cost_usd.\n"
    f"Group geographically close activities on the same day.\n"
    f"Include meal costs (~$50/person/day). Costs are PER PERSON."
    + multi_city_block
)
```

The pace guidance mapping (verbatim):

```python
pace_guidance = {
    "relaxed": ("RELAXED pace: at most one major activity per day plus one light "
                "slot; build in free time, long meals and rest. Never schedule "
                "three big attractions in a day."),
    "balanced": "BALANCED pace: mix of sightseeing and downtime.",
    "packed": ("PACKED pace: maximise sightseeing — fill morning, afternoon and "
               "evening with substantial activities, minimise idle time."),
}.get(request.pace, "BALANCED pace: mix of sightseeing and downtime.")
```

Multi-city constraint block (verbatim excerpt):

```python
multi_city_block = (
    "\n\nThis is a MULTI-CITY trip."
    f"\nThe cities MUST be visited in exactly this order (the order "
    f"the user requested — do NOT reorder): {', '.join(destinations)}.\n"
    ...
    "- Keep all activities geographically within each day's city\n"
    "- Add lat/lng coordinates (decimal degrees) to every slot\n"
)
```

### 2. Tool Schemas (per-agent tool lists)

Agent definitions declare tool permissions via YAML frontmatter, e.g. `tools: WebSearch, WebFetch` (FlightsAgent). The backend `web_tools.py` provides WebSearch/WebFetch implementations; flights additionally use a SerpAPI flights service with a source-mapping layer (`_url_to_source` maps `google.com`, `skyscanner.com`, `kayak.com`, `expedia.com`, `momondo.com` to canonical source tags).

### 3. Orchestration (3-phase pipeline)

From README (verbatim): "the app runs three phases back-to-back — you start seeing results within a second and they keep arriving for the next 15–30 seconds". Phase 1 agents stream via Server-Sent Events (SSE); Phase 2 itinerary has a "60s timeout with template fallback"; the StressTestAgent "audits the finished itinerary for pacing, timing, visa, weather, and budget problems."

---

## Evaluation Dimensions (multi-artifact suite specific)

### 1. Role Clarity
- [ ] 21 agents with granular, non-overlapping responsibilities (flights vs. hotels vs. activities vs. places vs. visa vs. SIM vs. forex vs. tips …)
- [ ] Each `.agents/*.md` has `name`, `description`, `tools`, `max_turns` frontmatter + a focused system prompt
- [ ] Clear producer/consumer dependencies (itinerary consumes hotels + activities; packing consumes activities + weather; pricing consumes flight prices)

### 2. Workflow Completeness
- [ ] 3-phase pipeline covers search → synthesis → adversarial audit
- [ ] Deferred-agent triggering (conditional execution on data availability)
- [ ] Static fallback for non-AI data (Phase 0) and template fallback on timeout

### 3. Prompt Consistency
- [ ] Uniform definition format (YAML frontmatter + markdown body) across all 21 agents
- [ ] Unified output contract (structured JSON; itinerary = 3 slots/day; flights sorted by price)
- [ ] Shared constraints propagated (multi-city stop order, per-city tags, lat/lng)

### 4. Tool Modularity
- [ ] Tool permission declared per agent (e.g. `WebSearch, WebFetch`)
- [ ] `max_turns` bounded per agent
- [ ] Tool-to-role mapping explicit (SerpAPI for flights, web tools for research agents)

### 5. Observability
- [ ] SSE streaming exposes per-agent progress
- [ ] Adversarial health-check agent (StressTest) as quality gate
- [ ] Running cost total tracked in the UI ("My Plan")

### 6. Extensibility
- [ ] Adding an agent = new `.agents/<name>.md` + a thin `*_agent.py` subclass
- [ ] Frontend sections driven by agent results (section-by-section streaming)
- [ ] Multi-city generalization of the single-city pipeline

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Role Clarity | 20% | | |
| Workflow Completeness | 25% | | |
| Prompt Consistency | 15% | | |
| Tool Modularity | 20% | | |
| Observability | 10% | | |
| Extensibility | 10% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### End-to-End Tests
1. **Full flow**: destination + dates + budget → complete plan with flights, hotels, itinerary, packing list
2. **Multi-city**: Paris → Rome → Barcelona with per-leg flights and enforced stop order
3. **Fallback**: force agent failure and verify Phase 0 static data + itinerary template fallback

### Unit Tests
1. **Per-agent independence**: run FlightsAgent alone and validate JSON schema
2. **Deferred triggering**: verify PricingAdvisorAgent fires only at ≥3 flight prices
3. **Definition loading**: verify `.agents/<name>.md` YAML frontmatter parsing

### Stress Tests
1. **Parallel fan-out**: 12 concurrent agents under latency budget (8–15s)
2. **Large itinerary**: multi-week trip with many stops
3. **Adversarial audit**: feed a deliberately over-packed itinerary to StressTestAgent

---

## Notes

- **License**: MIT (README "License" section states `MIT`). Verbatim quotation is permitted.
- **Scope**: end-user travel planning application (travel is an in-scope business domain); agents plan trips, they do not write/review code.
- The `.agents/*.md` files are the canonical prompt artifacts; agent Python files add dynamic prompt fragments (e.g. itinerary assembles its prompt at runtime from request + downstream agent results).
- All quoted text above was retrieved verbatim from the raw URLs in Metadata on 2026-10-13; long prompts are excerpted with ellipses.
