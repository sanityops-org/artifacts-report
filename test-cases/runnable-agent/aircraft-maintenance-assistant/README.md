# Aircraft Maintenance Airworthiness Assistant

A runnable airworthiness review agent for aircraft maintenance (MRO) teams. It queries simulated AD/SB, component-life, time-control, and maintenance-history data and produces a structured airworthiness decision report.

## Features

- Query AD/SB airworthiness status and compliance
- Check component life and time-control limits
- Summarize open defects and maintenance history
- Assess ground-time impact
- Generate a structured maintenance decision report

The agent is read-only: it does not modify aircraft records or execute maintenance actions.

## Components

- **System Prompt**: `prompts/system.txt`
- **Skill**: `skills/airworthiness_advisor/`
  - `query_airworthiness`: check AD/SB status
  - `query_component_status`: check component life and time controls
  - `query_maintenance_history`: load history and open defects
  - `generate_decision`: produce the decision report
- **Primary runner**: `main.py`
- **Configuration template**: `.env.example`

## Requirements

- Python 3.11+
- `sanityops-agent>=0.1.1`
- `pydantic>=2.0.0`
- `pyyaml>=6.0`
- `requests>=2.31.0`

The `sanityops-agent` package may be installed from the configured private Python package index.

## Setup

From the repository root:

```bash
cd test-cases/runnable-agent/aircraft-maintenance-assistant
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

A local `.env` file is included with placeholder values. Replace the API key before running:

```dotenv
LLM_PROVIDER=anthropic
LLM_API_KEY=your-real-api-key
```

Optional settings:

```dotenv
LLM_BASE_URL=https://api.anthropic.com
LLM_MODEL_ID=claude-sonnet-4-20250514
```

To recreate the local configuration file:

```bash
cp .env.example .env
```

Do not commit `.env` or real API credentials.

## Run

The primary entry point is `main.py`. At minimum, pass an aircraft registration number:

```bash
python main.py B-1234
```

Add a component or AD/SB identifier when needed:

```bash
python main.py B-1234 --part-no PN-12345
python main.py B-1234 --ad-id AD-2024-01-001
```

Combine the identifiers with a free-form question:

```bash
python main.py B-1234 \
  --part-no PN-12345 \
  --question "Should this aircraft be released?"
```

The runner:

1. Loads `prompts/system.txt`
2. Validates the aircraft, component, and AD identifiers
3. Registers the four airworthiness tools
4. Calls the configured LLM provider
5. Prints reasoning, tool calls, token usage, and the final report

Use `python main.py --help` to view all CLI options.

### Legacy entry point

`python scripts/run.py` remains available as an interactive compatibility entry point, but `main.py` is the primary command-line runner.

## Example

```bash
python main.py B-1234 --part-no PN-12345
```

The report includes:

1. Airworthiness conclusion
2. Required maintenance actions in priority order
3. Recommended spare parts
4. Ground-time impact
5. Decision rationale and supporting references

## Project Structure

```text
aircraft-maintenance-assistant/
├── README.md
├── main.py                 # Primary runnable entry point
├── .env                    # Local provider configuration (not committed)
├── .env.example            # Provider configuration template
├── agent.yaml
├── requirements.txt
├── prompts/
│   └── system.txt
├── config/
│   └── tools.yaml
├── data/
│   ├── sim_db.py
│   └── helpers.py
├── hooks/
│   └── pretty_output_hook.py
├── skills/
│   └── airworthiness_advisor/
│       ├── skill.yaml
│       ├── SKILL.md
│       ├── handler.py
│       └── tools/
└── scripts/
    ├── run.py              # Legacy entry point
    └── setup.py
```

## Tests

```bash
python -m pytest -q
```

The test suite covers the airworthiness tools, component-status queries, maintenance history, and decision generation.
