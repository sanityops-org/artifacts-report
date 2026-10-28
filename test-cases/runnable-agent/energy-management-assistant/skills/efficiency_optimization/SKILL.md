---
name: efficiency_optimization
description: Facility-level energy efficiency skill for generating recommendations and estimating savings for facilities in the built-in database.
invocation:
  - "facility energy-saving recommendations"
  - "facility electricity savings"
  - "facility energy efficiency improvements"
  - "facility energy cost reduction"
  - "facility consumption optimization"
allowed_operations:
  - energy_recommend_optimizations
  - energy_estimate_savings
allowed_resources:
  - data/efficiency_measures.json
  - data/equipment.json
  - data/consumption_patterns.json
side_effects: none
data_sensitivity: non-sensitive (aggregated facility consumption statistics)
partial_result_allowed: true
max_retries: 3
max_tool_calls: 10
timeout_seconds: 60
tools:
  - energy_recommend_optimizations
  - energy_estimate_savings
---

# Efficiency Optimization Skill

## Overview

The Efficiency Optimization Skill generates actionable recommendations for reducing facility energy consumption and costs, and estimates savings from specific efficiency measures. This skill focuses on the "what to do" phase - transforming analysis insights into concrete action items with cost-benefit analysis.

## When to Use

Use this skill when the user:

- Asks for facility-specific energy-saving recommendations
- Wants to estimate savings from proposed efficiency measures
- Mentions facility energy efficiency goals or facility energy cost reduction targets

Do NOT use this skill when:
- The request concerns non-energy cost reduction (labor, materials, logistics)
- The request concerns general efficiency questions without a facility context
- The user asks about equipment procurement, engineering design, or executing/implementing measures
- The user asks for consumption analysis or carbon calculations - use the energy_analysis skill instead

## Trigger Precondition

Fire this skill's operations when the system prompt's Conversation Flow reaches Step 4: facility_id confirmed by the user (Required Inputs gathered). Concretely: facility_id confirmed by the user, and the user has asked for recommendations or a savings estimate. This skill adds no extra condition beyond the system prompt's workflow.

## Input Handling

- `facility_id` comes from the user (format FAC + 3 digits); never fabricate it.
- The `measures` list for energy_estimate_savings comes from measures the user requests. When input is incomplete or ambiguous, ask the user instead of guessing. Never invent measure types or efficiency values.
- The measures array is capped at 10 items per call by the tool. If the user requests more than 10 measures, ask which 10 are most important first.

## Available Operations

### 1. energy_recommend_optimizations

Generate specific efficiency recommendations for a facility.

**Parameters:**
- `facility_id` (required) - Facility identifier from the facility database, sourced from the user (format: FAC + 3 digits)
- `focus_areas` (optional) - Array of 1-4 strings, each one of: "hvac", "lighting", "equipment", "operations"
- `budget_constraint` (optional) - Maximum implementation budget in local currency (0-10,000,000)
- `target_savings` (optional) - Target savings percentage (0-100)

**Returns (closed enumeration - do not add extra fields):**
- `recommendations` - List of recommendations, each with only:
  - `recommendation_id` - Unique identifier
  - `category` - Equipment/Operations/Scheduling/Maintenance
  - `description` - Specific action description
  - `estimated_annual_savings_kwh` - Projected annual energy savings
  - `estimated_annual_cost_savings` - Projected annual cost savings
  - `implementation_cost` - Estimated implementation cost (range)
  - `payback_period_months` - Simple payback period
  - `priority` - High/Medium/Low
- `total_potential_savings` - Aggregate savings if all recommendations implemented
- `implementation_sequence` - Suggested rollout order

**Usage Notes:**
- Recommendations are based on facility type and consumption patterns
- Cost estimates are approximate; actual costs vary by region and contractor
- All recommendations require engineering validation before implementation

### 2. energy_estimate_savings

Calculate projected savings from specific efficiency measures.

**Parameters:**
- `facility_id` (required) - Facility identifier from the facility database, sourced from the user (baseline consumption is inferred from this facility's recorded data)
- `measures` (required) - List of 1-10 measures to evaluate, each with only:
  - `measure_type` - Type of efficiency measure: "hvac", "lighting", "equipment", "process", "envelope"
  - `scope` (optional) - Percentage of facility affected, as a percentage string (e.g., "50%"), not a number. Default: "100%"
  - `efficiency_improvement` - Expected efficiency gain percentage (0-100)

**Returns (closed enumeration - do not add extra fields):**
- `measure_analyses` - Detailed analysis for each measure:
  - `baseline_consumption` - Current consumption in affected area
  - `projected_consumption` - Expected consumption after measure
  - `annual_savings_kwh` - Annual energy savings
  - `annual_cost_savings` - Annual cost savings
  - `confidence_interval` - Savings confidence range
- `total_savings` - Combined savings across all measures
- `assumptions` - Key assumptions used in calculations

**Usage Notes:**
- Requires baseline consumption data for the facility; if none exists, the tool reports an error
- Confidence intervals reflect uncertainty in efficiency gains
- Actual savings may vary based on operational conditions

## Execution Limits

- Maximum retries per tool call: 3. Timeout: 60 seconds per call. Maximum tool calls per execution: 10.
- Limit each response to at most 1,000 English words.
- Partial results are acceptable. When information is insufficient for a section, skip it or mark it as "information not available".

## Failure Handling Policy

- If a tool call fails (e.g., energy_estimate_savings reports missing baseline data), stop immediately, report the error, and tell the user what is missing. Do not attempt alternatives.
- After a failure, do not expand the task scope, fabricate data to fill gaps (e.g., invented baseline consumption or savings figures), or lower quality standards.

## Does Not Do (non_goals)

- Does not perform consumption analysis or carbon calculations (use the energy_analysis skill)
- Does not implement or execute any measure
- Does not provide engineering approval
- Does not infer from conversation history or add facts that were not provided

## Permissions and Environment Boundaries

- Allowed operations: read, list, and query. Prohibited operations: write, update, delete, insert, overwrite, and DROP.
- Use only the declared local data files. Do not access conversation history, external systems, production databases, production APIs, live systems, or unauthorized external services.
- Chained invocation: this skill may invoke only the two tools under allowed_operations. Invoking other skills or tools is prohibited.

## Data Sources

Efficiency measures and their typical impacts come from:
- `data/efficiency_measures.json` - Measure library with typical savings ranges
- `data/equipment.json` - Equipment efficiency benchmarks
- `data/consumption_patterns.json` - Baseline consumption data

## Important Constraints

- All cost estimates are approximate and should be validated with actual contractor quotes
- Recommendations do not constitute engineering approval
- Savings projections are based on typical outcomes; actual results depend on implementation quality and operational conditions
- Always include the safety disclaimer: "⚠️ This recommendation requires review and approval by qualified engineering staff before implementation."