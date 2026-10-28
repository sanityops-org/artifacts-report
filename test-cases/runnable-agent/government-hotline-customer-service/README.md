# Government Hotline Intelligent Customer Service

## Industry
Government/Government Affairs

## Function description
The intelligent customer service of the government service hotline for the public supports the creation and inquiry of complaints/suggestions/consultation work orders, intelligently matches the undertaking department, marks the urgency, and realizes the "first response, rapid transfer""。

## List of skills
- **government_ticket**：Work order skills
  - create_ticket：Create a complaint/suggestion/consultation work order
  - query_ticket：Query by work order number
  - query_ticket_list：Query historical work orders by mobile phone number

## Core competence
- **Intelligent distribution**: Automatically match the undertaking department according to the content of the work order (12+ department coverage)
- **Emergency classification**: Third-level urgency determination (emergency/emergency/ordinary)
- **Real-name/Anonymous**: Support real-name complaints and anonymous complaints

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
Government Hotline Intelligent Customer Service/
├── README.md
├── agent.yaml              # Agent Deploy
├── requirements.txt        # Be dependent on
├── prompts/
│   └── system.txt          # System prompts
├── config/
│   └── tools.yaml          # Tool configuration
├── data/                   # Analog data layer
│   ├── sim_db.py           # Department Library/Keyword Mapping/Leveling Rules
│   └── helpers.py          # Assecation algorithm/work order number generation
├── skills/
│   └── government_ticket/
│       ├── skill.yaml      # Definition of skills
│       ├── handler.py      # Skill processing script
│       ├── tools/          # Tool script
│       │   ├── dispatch_engine.py
│       │   └── ticket_store.py
│       └── tests/          # Test script
│           ├── test_handler.py
│           ├── test_dispatch_engine.py
│           └── test_ticket_store.py
└── scripts/
    ├── run.py              # Start the script
    └── setup.py            # Initialize the script
```

## Examples of use

### Create a complaint work order
```
User: I want to complain about the noise of construction at night in the community.
Assistant: A complaint work order has been created for you.
Work order number:GH-20260904-0001
Hosting Department: Ecology and Environment Bureau
Degree of urgency: urgent
Expected response time limit: 24 hours
```

### Query the work order
```
User: Query the work order GH-20260904-0001
Assistant: Work order status: to be accepted
Hosting Department: Ecology and Environment Bureau
Creation time:2026-09-04 10:30:00
```

## Test

```bash
# Run all the tests
cd test-cases/runnable-agent/government-hotline-customer-service
python3 -m pytest skills/government_ticket/tests/ -v

# Run the data layer test
python3 -m pytest data/tests/ -v
```

## Run From This Repository

From the repository root:

```bash
cd test-cases/runnable-agent/government-hotline-customer-service
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/setup.py
python scripts/run.py
```
