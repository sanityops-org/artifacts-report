# Energy Management Assistant

## Project Information

| Item | Description |
|------|-------------|
| **Industry** | Energy (Enterprise Energy Management) |
| **Project Name** | Energy Management Assistant |
| **Version** | v1.0.0 |
| **Created** | 2026-09-30 |
| **Author** | Agent Artifacts Team |
| **Tech Stack** | Python 3.11+, Pydantic 2.0+, sanityops_agent |
| **License** | MIT License |

## Overview

The Energy Management Assistant is an intelligent agent designed for **enterprise energy managers and facility operators**. It helps users analyze energy consumption patterns, identify inefficiencies, recommend optimization strategies, and provide guidance on renewable energy adoption.

**It does not control physical equipment.** All recommendations are advisory - actual implementation requires human approval and engineering validation.

## Core Capabilities

| Capability | Description |
|------------|-------------|
| **Consumption Analysis** | Parse and analyze energy consumption data, identify patterns and anomalies |
| **Efficiency Recommendations** | Suggest energy-saving measures based on consumption patterns and industry best practices |
| **Renewable Integration** | Provide guidance on solar, wind, and other renewable energy options |
| **Carbon Footprint Tracking** | Calculate and track carbon emissions from energy usage |

## Three Core Principles

| ID | Principle | Implementation |
|----|-----------|----------------|
| 1 | Safety First | Never recommend actions that could compromise equipment safety; all suggestions require engineering validation |
| 2 | Data-Driven | All recommendations must be based on actual consumption data; no speculative advice without supporting metrics |
| 3 | Regulatory Compliance | Ensure recommendations align with local energy regulations and standards |

## Main Workflow

```
User Query / Data Upload
  → energy_analyze_consumption ──→ Consumption patterns & anomalies
        ↓
  → energy_identify_efficiency_opportunities ──→ Potential savings areas
        ↓
  → energy_recommend_optimizations ──→ Specific action items with ROI estimates
        ↓
  → energy_calculate_carbon_footprint ──→ Emissions baseline
        ↓
  → energy_suggest_renewables ──→ Renewable integration options
```

## Skill Inventory

### 1. energy_analysis (Energy Analysis Skill)

Analyze consumption data and identify patterns.

| Intent | Description |
|--------|-------------|
| `analyze_consumption` | Parse consumption data, return usage patterns and anomalies |
| `identify_opportunities` | Identify efficiency improvement opportunities |
| `calculate_carbon` | Calculate carbon footprint from energy usage |

### 2. efficiency_optimization (Efficiency Optimization Skill)

Generate actionable optimization recommendations.

| Intent | Description |
|--------|-------------|
| `recommend_optimizations` | Generate specific efficiency measures with cost-benefit analysis |
| `estimate_savings` | Project energy and cost savings from proposed measures |
| `prioritize_actions` | Rank recommendations by impact and feasibility |

### 3. renewable_integration (Renewable Integration Skill)

Guide renewable energy adoption decisions.

| Intent | Description |
|--------|-------------|
| `assess_renewable_potential` | Evaluate site suitability for renewables |
| `size_system` | Calculate optimal system capacity |
| `estimate_roi` | Project financial returns for renewable investments |

## Project Structure

```
Energy Management Assistant/
├── README.md                  # Project documentation (this file)
├── requirements.txt           # Dependencies
├── .env.example               # Environment variables template
├── tools_schema.json          # Tool schema for platform integration
├── prompts/
│   └── system.txt             # System prompt
├── models/                    # Pydantic data models
│   ├── enums.py               # Enumerations
│   ├── consumption.py         # Energy consumption models
│   ├── facility.py            # Facility models
│   ├── recommendation.py      # Recommendation models
│   └── carbon.py              # Carbon footprint models
├── apis/                      # Domain service layer
│   ├── data_store.py          # Data persistence
│   ├── analysis_engine.py     # Core analysis logic
│   └── recommendation_engine.py # Recommendation generation
├── data/                      # Sample data
│   ├── facilities.json
│   ├── equipment.json
│   ├── consumption_patterns.json
│   ├── efficiency_measures.json
│   └── renewable_options.json
├── tools/                     # Executable tools (auto-registered by SDK)
│   ├── energy_analyze_consumption.py
│   ├── energy_identify_efficiency_opportunities.py
│   ├── energy_recommend_optimizations.py
│   ├── energy_calculate_carbon_footprint.py
│   ├── energy_suggest_renewables.py
│   └── energy_estimate_savings.py
├── skills/                    # Skill definitions
│   ├── energy_analysis/
│   ├── efficiency_optimization/
│   └── renewable_integration/
├── scripts/
│   ├── __init__.py
│   ├── run.py                 # Agent startup script
│   └── setup.py               # Initialization script
└── tests/                     # Integration and contract tests
    ├── test_integration.py
    ├── test_prompt_contract.py
    ├── test_tools_schema.py
    └── test_data_files.py
```

## Data Models

All models use Pydantic v2 `BaseModel` with JSON serialization via `model_validate` / `model_dump(mode="json")`.

- **Facility** — `facility_id`, `name`, `type` (manufacturing/office/warehouse/data_center), `location`, `floor_area`, `operating_hours`
- **Equipment** — `equipment_id`, `name`, `type` (hvac/lighting/machinery/computing), `facility_id`, `rated_power`, `efficiency_rating`
- **ConsumptionRecord** — `record_id`, `facility_id`, `timestamp`, `electricity_kwh`, `gas_m3`, `water_m3`, `source` (grid/renewable)
- **Recommendation** — `recommendation_id`, `type`, `description`, `estimated_savings_kwh`, `estimated_cost_savings`, `implementation_cost`, `payback_period_months`, `priority`
- **CarbonFootprint** — `facility_id`, `period`, `electricity_emissions_kgco2`, `gas_emissions_kgco2`, `total_emissions_kgco2`, `emission_intensity`

## Installation

```bash
pip install -r requirements.txt
```

Dependencies include:

- `pydantic>=2.0.0` - Data modeling and validation
- `sanityops_agent` - Agent framework
- `pytest` - Testing framework

## Running

### 1. Initialization Check

```bash
python scripts/setup.py
```

Verifies required directories and data files.

### 2. Configure API Key

```bash
cp .env.example .env
```

Edit `.env`:

```env
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
- Scan `tools/*.py` to register all tools
- Use `SkillManager` to scan `skills/` and append skill prompts

```
User: Our factory's electricity bill has increased 20% this quarter. Can you help analyze why?
Assistant: I'll help you analyze the consumption increase. Let me start by examining your facility's consumption patterns...
```

Enter `quit`, `exit`, or `q` to exit.

## Key Design Principles

1. **Analysis Before Recommendation**: Always analyze actual data before suggesting changes; no generic advice without context
2. **Safety Through Human Validation**: All recommendations explicitly state they require engineering review before implementation
3. **Transparent ROI**: Every optimization suggestion includes estimated costs, savings, and payback period
4. **Regulatory Awareness**: Recommendations note relevant energy standards and regulations

## Known Limitations

- Energy prices and emission factors are based on built-in sample data; production deployments should integrate real utility rates
- Renewable energy potential estimates use simplified models; detailed site assessments require professional engineering studies
- Equipment efficiency ratings are illustrative; actual measurements should be used for precise analysis
- Sample data window: 2026-09-01 to 2026-09-30 for demonstration purposes

## License

MIT License

## Run From This Repository

From the repository root:

```bash
cd test-cases/runnable-agent/energy-management-assistant
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
# Edit .env and add the required model endpoint and credentials.
python scripts/setup.py
python scripts/run.py
```
