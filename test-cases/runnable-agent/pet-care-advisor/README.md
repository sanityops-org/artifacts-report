# Pet Care Advisor Agent

An intelligent assistant for choosing a pet, planning its daily care, and keeping health records.

## Industry
Consumer / Pet Care

## Description
Pet Care Advisor helps prospective adopters and pet owners match to a suitable breed, browse
simulated adoptable animals, build a daily care routine, and track vaccinations and vet visits.
The agent deliberately does not act as a veterinarian — any health concern is referred to a
licensed professional.

## Skills
- pet_matching: Search breeds and browse adoptable pets by species, size, and temperament
- care_scheduling: Create, list, and complete daily care tasks; view today's schedule
- health_tracking: List and add health records, and surface upcoming due dates

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
Pet Care Advisor/
├── prompts/          # System prompt
├── models/           # Pydantic domain models
├── apis/             # Matching engine, care engine, data store
├── data/             # Simulated JSON data (breeds, pets, tasks, records)
├── skills/           # Skill definitions (3 skills)
├── tools/            # Executable tool scripts (10 tools, auto-scanned)
├── tests/            # Integration and contract tests
└── scripts/          # Startup and setup scripts
```

## Data Models

- **Breed**: Species, size, temperament tags, exercise and grooming needs, apartment and kid suitability
- **Pet**: An adoptable animal, referencing a breed, with age and adoption status
- **CareTask**: A scheduled care action (feeding, walk, grooming, medication) with frequency and status
- **HealthRecord**: A vaccination, vet visit, weight, medication, or allergy entry with an optional next-due date

## Tests

```bash
pip install pytest
python -m pytest
```

The suite covers model validation against the shipped data files, the matching and care engines
(with pinned dates so results do not depend on the wall clock), the full care loop through the
tools, and two contract tests — one asserting the system prompt still carries the three red lines
and every tool name, one asserting each tool keeps its schema and docstring shape.

Note that the tools hold session state in memory, so restarting the agent reseeds care tasks and
health records from `data/`. Nothing is written back to disk.

## Core Design Points

1. **No medical advice**: tools return no diagnosis, dosage, prescription, or feed-amount fields,
   and the prompt requires referral to a licensed vet
2. **No real adoption**: all pet listings are simulated, with no contact or payment path
3. **Care schedules are recommendations**: feeding amounts and medication details are never
   invented by the agent — only user-supplied values are recorded
4. **User data stays in memory**: care tasks and health records are not written to disk
5. **Self-contained system prompt**: works without SKILL.md injection on the platform
6. **Platform-compatible**: every tool declares a module-level JSON Schema `parameters`

## Red Line Constraints

- **B1**: No veterinary diagnosis or medical advice — refer to a licensed vet
- **B2**: No real adoption transactions — listings are simulated
- **B3**: Care schedules are recommendations, not prescriptions — confirm with your vet

## Run From This Repository

From the repository root:

```bash
cd test-cases/runnable-agent/pet-care-advisor
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
# Edit .env and add the required model endpoint and credentials.
python scripts/setup.py
python scripts/run.py
```
