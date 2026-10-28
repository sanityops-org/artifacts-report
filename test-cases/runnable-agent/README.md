# Runnable Agent Collection

This folder contains 18 runnable agent packages copied from the internal `agent_artifacts` collection. Each package retains its prompts, skills, tools, data, tests, and original entry point.



## Included Agents

| Agent | Collection date | Entry point | Run guide |
|---|---|---|---|
| [aircraft-maintenance-assistant](aircraft-maintenance-assistant/) | 2026-09-03 | `python main.py B-1234` | Included in the agent README |
| [code-review-assistant](code-review-assistant/) | 2026-09-02 | `python main.py <code-folder>` | Included in the agent README |
| [container-terminal-dispatch-assistant](container-terminal-dispatch-assistant/) | 2026-09-14 | `python scripts/run.py` | Included in the agent README |
| [data-quality-validator](data-quality-validator/) | 2026-10-09 | `python scripts/run.py` | Included in the agent README |
| [dependency-security-auditor](dependency-security-auditor/) | 2026-10-08 | `python scripts/run.py` | Included in the agent README |
| [energy-management-assistant](energy-management-assistant/) | 2026-09-30 | `python scripts/run.py` | Included in the agent README |
| [entertainment-guide](entertainment-guide/) | 2026-10-09 | `python scripts/run.py` | Included in the agent README |
| [expense-compliance-auditor](expense-compliance-auditor/) | 2026-10-09 | `python scripts/run.py` | Included in the agent README |
| [food-delivery-customer-service](food-delivery-customer-service/) | 2026-09-04 | `python scripts/run.py` | Included in the agent README |
| [freight-logistics-assistant](freight-logistics-assistant/) | 2026-09-30 | `python scripts/run.py` | Included in the agent README |
| [government-hotline-customer-service](government-hotline-customer-service/) | 2026-09-04 | `python scripts/run.py` | Included in the agent README |
| [meal-planner](meal-planner/) | 2026-10-09 | `python scripts/run.py` | Included in the agent README |
| [medical-triage-assistant](medical-triage-assistant/) | 2026-09-26 | `python scripts/run.py` | Included in the agent README |
| [pet-care-advisor](pet-care-advisor/) | 2026-10-09 | `python scripts/run.py` | Included in the agent README |
| [securities-customer-service](securities-customer-service/) | 2026-09-03 | `python scripts/run.py` | Included in the agent README |
| [taxi-travel-assistant](taxi-travel-assistant/) | 2026-09-04 | `python scripts/run.py` | Included in the agent README |
| [travel-planner](travel-planner/) | 2026-10-09 | `python scripts/run.py` | Included in the agent README |
| [weather-assistant](weather-assistant/) | 2026-10-09 | `python scripts/run.py` | Included in the agent README |

## Standard Run Pattern

Use the instructions in each agent's README. Most packages follow this pattern:

```bash
cd <agent-directory>
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/run.py
```

Some packages use a setup step, a custom dependency installation command, or a different interpreter entry point. Follow the commands in the corresponding agent README when they differ from the standard pattern.

## Runtime Configuration

Agents that call an LLM use environment variables or `.env` files. A shared configuration can be placed at `test-cases/runnable-agent/.env`; all runners load it automatically and give it precedence over an agent-local `.env`. Agent-local files remain supported as a fallback. Do not commit local `.env` files or API keys.

## Tests

Most packages include tests. Use the test command documented in the individual README, or run `python -m pytest` from the agent directory after installing the test dependencies.
