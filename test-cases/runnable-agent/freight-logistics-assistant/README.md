# Freight Logistics Assistant

## Project Information

| Item | Description |
|------|-------------|
| **Industry** | Transportation & Logistics (Freight Management) |
| **Project Name** | Freight Logistics Assistant |
| **Version** | v1.0.0 |
| **Created** | 2026-09-30 |
| **Author** | Agent Artifacts Team |
| **Tech Stack** | Python 3.11+, Pydantic 2.0+, sanityops_agent |
| **License** | MIT License |

## Overview

The Freight Logistics Assistant is an intelligent agent designed for **logistics coordinators and freight managers**. It helps users track shipments, plan optimal routes, and generate freight quotations. The assistant integrates with multiple data sources to provide real-time shipment status, cost-effective route recommendations, and accurate pricing estimates.

**Core Principle: No Booking, No Payment.** This assistant provides information and recommendations only. Actual booking, payment processing, and carrier contracts are handled by external systems.

## Core Capabilities

### Three Main Functions

| Capability | Description |
|------------|-------------|
| **Shipment Tracking** | Query shipment status by tracking number, route, or time range |
| **Route Planning** | Recommend optimal routes based on origin, destination, cargo type, and constraints |
| **Freight Quotation** | Generate cost estimates based on route, weight, volume, and service level |

### Three Guardrails (Enforced at System Prompt Level)

| ID | Guardrail | Implementation |
|----|-----------|----------------|
| 1 | Cannot book shipments | Tools return information only; no booking confirmation fields |
| 2 | Cannot process payments | No payment API integrations; quotation is estimate only |
| 3 | Cannot modify carrier contracts | All carrier data is read-only; displays existing rates |

### Main Workflow

```
User Request
    │
    ├── "Track shipment" → shipment_get_status → shipment_get_history → shipment_list_by_route
    │
    ├── "Plan route" → route_check_restrictions → route_recommend_options → route_get_details
    │
    └── "Get quote" → freight_calculate_estimate → freight_compare_carriers → freight_get_transit_time
```

## Skills Overview

The system includes 3 skills, accessible via unified `run(intent, params)` interface.

### 1. shipment_tracking (Shipment Tracking Skill)

Track and query shipment status and history.

| Intent | Description |
|--------|-------------|
| `get_status` | Query current status by tracking number |
| `get_history` | Get full tracking history for a shipment |
| `list_by_route` | List shipments by origin/destination or route |

### 2. route_planning (Route Planning Skill)

Plan and recommend optimal freight routes.

| Intent | Description |
|--------|-------------|
| `recommend_options` | Get recommended routes between origin and destination |
| `get_details` | Get detailed route information including waypoints |
| `check_restrictions` | Check route restrictions based on cargo type |

### 3. freight_quotation (Freight Quotation Skill)

Generate and compare freight cost estimates.

| Intent | Description |
|--------|-------------|
| `calculate_estimate` | Calculate freight cost estimate |
| `compare_carriers` | Compare quotes from multiple carriers |
| `get_transit_time` | Get estimated transit time for route |

## Project Structure

```
freight_logistics_assistant/
├── README.md                  # Project documentation (this file)
├── requirements.txt           # Dependencies
├── .env.example               # Environment variable template
├── tools_schema.json          # Tool definitions for platform
├── prompts/
│   └── system.txt             # System prompt (self-contained)
├── models/                    # Pydantic data models
│   ├── enums.py               # Enumerations
│   ├── shipment.py            # Shipment model
│   ├── route.py               # Route model
│   ├── carrier.py             # Carrier model
│   ├── quotation.py           # Quotation model
│   └── cargo.py               # Cargo model
├── apis/                      # Domain service layer
│   ├── data_store.py          # JSON read/write utilities
│   ├── tracking_engine.py     # Shipment tracking logic
│   ├── route_optimizer.py     # Route planning logic
│   └── pricing_engine.py      # Freight quotation logic
├── data/                      # Mock data
│   ├── shipments.json
│   ├── routes.json
│   ├── carriers.json
│   ├── pricing_rules.json
│   └── cargo_types.json
├── tools/                     # Executable tools (auto-scanned by SDK)
│   ├── shipment_get_status.py
│   ├── shipment_get_history.py
│   ├── shipment_list_by_route.py
│   ├── route_recommend_options.py
│   ├── route_get_details.py
│   ├── route_check_restrictions.py
│   ├── freight_calculate_estimate.py
│   ├── freight_compare_carriers.py
│   └── freight_get_transit_time.py
├── skills/                    # Skill definitions
│   ├── shipment_tracking/
│   ├── route_planning/
│   └── freight_quotation/
├── scripts/
│   ├── __init__.py
│   ├── run.py                 # Agent startup script
│   └── setup.py               # Initialization script
└── tests/                     # Integration tests
    ├── test_integration.py
    ├── test_prompt_contract.py
    └── test_tools_schema.py
```

## Data Models

All models are Pydantic v2 `BaseModel` with JSON serialization via `model_validate` / `model_dump(mode="json")`.

- **Shipment** — `tracking_number`, `origin`, `destination`, `status`, `carrier_id`, `cargo_type`, `weight_kg`, `volume_cbm`, `pickup_date`, `eta`, `current_location`
- **Route** — `route_id`, `origin`, `destination`, `distance_km`, `estimated_hours`, `waypoints`, `restrictions`
- **Carrier** — `carrier_id`, `name`, `service_type`, `coverage_regions`, `rating`
- **Quotation** — `quote_id`, `carrier_id`, `route_id`, `base_rate`, `fuel_surcharge`, `total_estimate`, `valid_until`
- **Cargo** — `cargo_type`, `category`, `hazard_class`, `weight_limits`, `volume_limits`

Tracking number format: `FR{YYYYMMDD}{6-digit sequence}`.

## Installation

```bash
pip install -r requirements.txt
```

Dependencies:

- `pydantic>=2.0.0` — Data models and validation
- `sanityops_agent` — Agent framework
- `pytest` — Testing framework

## Running

### 1. Initialization Check

```bash
python scripts/setup.py
```

Verifies required directories and mock data files.

### 2. Configure API Key

```bash
cp .env.example .env
```

`.env` content:

```env
# LLM Configuration
LLM_PROVIDER=anthropic
LLM_API_KEY=your-api-key
LLM_MODEL_ID=
LLM_BASE_URL=
```

### 3. Start Agent

```bash
python scripts/run.py
```

The SDK will:

- Load `prompts/system.txt` as system prompt
- Scan `tools/*.py` to register all 9 tools
- Use `SkillManager` to inject skills into system prompt
- Start an interactive session

```
User: Track shipment FR202609300001234
Assistant: Let me look up that shipment for you...
```

Enter `quit`, `exit`, or `q` to exit.

### 4. Programmatic Usage

```python
from tools.shipment_get_status import execute as get_status

result = get_status({"tracking_number": "FR202609300001234"})
print(result["data"]["status"])  # in_transit, delivered, etc.
```

## Testing

### Run All Tests

```bash
python -m pytest -v
```

### Test Coverage

| Directory | Coverage |
|-----------|----------|
| `models/tests/` | Pydantic models and enums |
| `apis/tests/` | DataStore, tracking/route/pricing engines |
| `skills/*/tests/` | Skill intent routing |
| `tests/` | Integration, prompt contract, tools schema |

## Design Principles

1. **Information Only, No Transactions**: All tools return read-only data. No booking, payment, or contract modification capabilities.
2. **Estimates, Not Guarantees**: Quotations are estimates only. Actual rates depend on carrier confirmation.
3. **Mock Data, No External Services**: All data is simulated. No real carrier APIs are called.
4. **Schema Parity**: Tool definitions in `tools/*.py` match `tools_schema.json` exactly, verified by tests.
5. **Skills Injected Locally**: `run.py` injects SkillManager for local testing; `system.txt` is self-contained for platform deployment.

## Known Limitations

- Tracking data is simulated with fixed mock shipments
- Route optimization uses simplified distance calculations
- Pricing estimates are based on static rate tables
- No real-time carrier API integration
- Transit times are estimates without traffic/weather factors

## License

MIT License

## Run From This Repository

From the repository root:

```bash
cd test-cases/runnable-agent/freight-logistics-assistant
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
# Edit .env and add the required model endpoint and credentials.
python scripts/setup.py
python scripts/run.py
```
