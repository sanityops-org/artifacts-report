# Taxi travel assistant

## Industry
Taxi/online car-hailing travel

## Function description
The taxi travel intelligence for passengers supports core travel services such as route planning, cost estimation, vehicle inquiry, taxi ordering, etc.

## List of skills
- route_planning：Route planning, find the best travel route
- fare_estimation：Cost estimate, calculate the estimated cost of a variety of models
- vehicle_query：Vehicle inquiry, check nearby available taxis
- order_booking：Call a taxi to place an order, create an order and send a car

## Date of creation
2026-09-04

## Edition
v1.0.0

## Author
Agent Artifacts Team

## Operation mode

**Precondition**: Make sure that the `sanityops_agent` framework has been installed

```bash
# Installation dependency
pip install -r requirements.txt

# Start up Agent
python scripts/run.py
```

## Catalog structure

```
Taxi travel assistant/
├── README.md
├── agent.yaml
├── requirements.txt
├── prompts/
│   └── system.txt
├── config/
│   └── tools.yaml
├── data/
│   ├── sim_db.py
│   └── helpers.py
├── skills/
│   ├── route_planning/
│   ├── fare_estimation/
│   ├── vehicle_query/
│   └── order_booking/
└── scripts/
    ├── run.py
    └── setup.py
```

## Run From This Repository

From the repository root:

```bash
cd test-cases/runnable-agent/taxi-travel-assistant
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/setup.py
python scripts/run.py
```
