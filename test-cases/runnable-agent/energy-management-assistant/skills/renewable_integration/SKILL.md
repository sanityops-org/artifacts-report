---
name: renewable_integration
description: Facility-level renewable energy planning skill for assessing solar, wind, and storage suitability with planning-level payback guidance.
invocation:
  - "facility solar feasibility"
  - "facility wind feasibility"
  - "facility renewable options"
  - "facility clean energy planning"
  - "facility storage assessment"
allowed_operations:
  - energy_suggest_renewables
allowed_resources:
  - data/renewable_options.json
  - data/facilities.json
side_effects: none
data_sensitivity: non-sensitive (facility characteristics and public equipment specifications)
partial_result_allowed: true
max_retries: 3
max_tool_calls: 10
timeout_seconds: 60
tools:
  - energy_suggest_renewables
---

# Renewable Integration Skill

## Overview

The Renewable Integration Skill provides planning-level guidance on adopting renewable energy sources for facility operations. It covers solar PV, wind energy, and energy storage through the single authorized tool `energy_suggest_renewables`, helping users understand potential, indicative sizing, and simple payback. It works only for facilities in the built-in database; do not trigger it for ESG reporting, carbon accounting, residential solar, maintenance of existing installations, or grid interconnection applications.

## When to Use

Use this skill when the user:

- Asks about solar panel or wind turbine feasibility for a specific facility
- Wants to assess renewable energy potential for a facility in the database
- Explicitly mentions solar, wind, storage, or renewables for a facility, AND the request asks about adopting or assessing them (not merely a passing mention). Do NOT activate for bare ESG/sustainability/carbon-accounting mentions that name none of solar, wind, storage, or renewables, or for structural/maintenance questions about existing installations.

Do NOT use this skill when:
- The request concerns ESG/sustainability reporting or carbon accounting
- The request concerns residential solar or non-facility installations
- The request concerns maintenance of existing installations or grid interconnection applications
- No facility is identified and the user cannot provide a facility_id

## Input Handling

- `facility_id` comes from the user (format FAC + 3 digits, e.g., FAC001); never fabricate it. When input is incomplete or ambiguous, ask the user instead of guessing.
- `renewable_types` accepts at most 3 values from "solar", "wind", "storage"; if the user requests more types or unspecified options, ask them to choose.
- One facility per interaction; the tool accepts a single facility_id per call. If the user submits multiple facilities, ask them to pick one first.

## Available Operations

### 1. energy_suggest_renewables

Provide renewable energy integration recommendations including suitability assessment, indicative sizing, and simple payback estimates.

**Parameters:**
- `facility_id` (required) - Facility identifier from the facility database, sourced from the user (format: FAC + 3 digits)
- `renewable_types` (optional) - Types to assess: "solar", "wind", "storage" (1-3 values, default: ["solar"])
- `target_coverage` (optional) - Target percentage of consumption to cover (0-100, default 50)

**Returns (closed enumeration - do not add extra fields):**
- Renewable options with suitability assessment, indicative capacity, estimated annual generation, and simple payback estimates
- Constraints and caveats for each option

**Usage Notes:**
- All outputs are planning-level estimates, not engineering designs
- Sizing and payback outputs are indicative; they do not constitute investment advice
- Actual installations require professional site assessment, utility approval, and permits
- Financial returns beyond simple payback (NPV, IRR, financing analysis) are out of scope for this skill

## Execution Limits

- Maximum retries per tool call: 3. Timeout: 60 seconds per call. Maximum tool calls per execution: 10.
- Limit each response to at most 1,000 English words.
- Partial results are acceptable: if only some requested renewable types can be assessed or site data is incomplete, present what was assessed and mark the rest as "information not available".

## Failure Handling Policy

- If a tool call fails (invalid facility_id, missing site data), stop immediately and report the error. Do not attempt alternatives.
- After a failure, do not expand the task scope, fabricate data to fill gaps (e.g., invented irradiance, cost, or payback figures), or lower quality standards.

## Does Not Do (non_goals)

- Does not provide engineering designs, NPV/IRR/financing analysis, or investment advice
- Does not perform efficiency audits or consumption analysis (use the other skills)
- Does not infer from conversation history or add facts that were not provided

## Permissions and Environment Boundaries

- Allowed operations: read, list, and query. Prohibited operations: write, update, delete, insert, overwrite, and DROP.
- Use only the declared local data files (data/renewable_options.json, data/facilities.json). Do not access conversation history, external systems, production databases, production APIs, live systems, or unauthorized external services.
- Chained invocation: this skill may invoke only energy_suggest_renewables. Invoking other skills or tools is prohibited.

## Data Sources

Renewable energy data comes from:
- `data/renewable_options.json` - Equipment specifications and costs
- `data/facilities.json` - Site characteristics

## Important Constraints

- Renewable potential estimates are simplified; professional site assessments are required for actual installations
- Grid connection requirements vary significantly by utility
- All recommendations should be validated with licensed installers and local authorities
- Include disclaimer: "⚠️ Renewable energy installations require professional engineering assessment, utility approval, and applicable permits. These estimates are for planning purposes only."