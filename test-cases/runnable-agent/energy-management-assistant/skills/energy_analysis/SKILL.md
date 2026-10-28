---
name: energy_analysis
description: Facility-level energy consumption analysis skill for understanding usage patterns, identifying anomalies, identifying diagnostic efficiency opportunities, and calculating carbon footprint for facilities in the built-in database.
invocation:
  - "analyze facility energy consumption"
  - "facility consumption patterns"
  - "facility energy bill analysis"
  - "facility carbon footprint"
  - "facility emissions"
allowed_operations:
  - energy_analyze_consumption
  - energy_identify_efficiency_opportunities
  - energy_calculate_carbon_footprint
allowed_resources:
  - data/consumption_patterns.json
  - data/facilities.json
  - data/equipment.json
side_effects: none
data_sensitivity: non-sensitive (aggregated facility consumption statistics)
non_goals:
  - concrete implementation recommendations (savings-per-measure estimates belong to efficiency_optimization; the estimated_savings_potential percentage this skill reports is a diagnostic indicator only)
  - non-facility emissions (vehicles, products, supply chains)
  - energy markets or policy analysis
  - inferring from conversation history or adding facts that were not provided
partial_result_allowed: true
max_items: 10
max_retries: 3
max_tool_calls: 10
timeout_seconds: 60
tools:
  - energy_analyze_consumption
  - energy_identify_efficiency_opportunities
  - energy_calculate_carbon_footprint
---

# Energy Analysis Skill

## Overview

The Energy Analysis Skill provides diagnostic analysis of facility energy consumption data: pattern identification, anomaly detection, opportunity identification, and carbon footprint calculation. It works only on facility-level data for facilities in the built-in database (facility_id format FAC + 3 digits); do not trigger it for vehicle emissions, product footprints, energy-market or policy questions, or anything without a facility context.

## When to Use

Use this skill when the user:

- Describes concerns about a specific facility's energy consumption or costs
- Asks to analyze a facility's usage patterns or find anomalies
- Wants to calculate a facility's carbon emissions
- Mentions a specific facility's high bills, unusual consumption, or energy cost concerns AND the request is about analyzing usage (not implementing measures)

Do NOT use this skill when:
- The request concerns non-facility emissions (vehicles, products, supply chains)
- The request is about energy markets, policy, or ESG reporting
- No facility is identified and the user cannot provide a facility_id
- The user asks for concrete implementation recommendations or per-measure savings estimates - use the efficiency_optimization skill instead (this skill reports only the diagnostic estimated_savings_potential percentage)

## Input Handling

- Required inputs: facility_id (format FAC + 3 digits, e.g., FAC001) always; plus analysis period (start_date, end_date, YYYY-MM-DD) only for energy_analyze_consumption and energy_calculate_carbon_footprint. facility_id comes from the user; never fabricate it. When input is incomplete or ambiguous, ask the user instead of guessing.
- max_items applies to user-submitted request items: process at most 10 per interaction. One facility per interaction; the tools accept a single facility_id per call. If the user submits multiple facilities, ask them to pick one first.

## Available Operations

### 1. energy_analyze_consumption

Analyze energy consumption data to identify patterns and anomalies.

**Parameters:**
- `facility_id` (required) - Facility identifier from the facility database, sourced from the user (format: FAC + 3 digits, e.g., FAC001)
- `start_date` (required) - Analysis period start (YYYY-MM-DD)
- `end_date` (required) - Analysis period end (YYYY-MM-DD)
- `granularity` (optional) - Data grouping: "hourly", "daily", "monthly" (default: "daily")

**Returns (closed enumeration - do not add extra fields):**
- `facility_id` - Facility identifier that was analyzed
- `facility_name` - Facility display name
- `facility_type` - Facility type category
- `analysis_period` - Object with start and end dates (YYYY-MM-DD)
- `total_consumption_kwh` - Total kWh for the period
- `peak_demand_kw` - Peak demand in kW
- `average_daily_kwh` - Average daily consumption
- `patterns` - Identified usage patterns (peak_hours list, weekday_weekend_ratio, load_factor)
- `anomalies` - Detected anomalies (date, consumption_kwh, expected_kwh, deviation_percent, severity)
- `benchmark_comparison` - Comparison to industry benchmarks (facility_type_average, performance_percentile, assessment), when available

**Usage Notes:**
- Requires at least 7 days of data for meaningful pattern analysis; shorter periods return reduced-significance results
- Anomaly detection uses statistical deviation from rolling averages
- Benchmarks are based on facility type and region

### 2. energy_identify_efficiency_opportunities

Identify energy efficiency improvement opportunities based on consumption analysis.

**Parameters:**
- `facility_id` (required) - Facility identifier from the facility database, sourced from the user
- `analysis_results` (optional) - Prior results object returned by energy_analyze_consumption; if not provided, recent data is analyzed

**Returns (closed enumeration - do not add extra fields):**
- `opportunities` - List of identified opportunities, each with only:
  - `opportunity_type` - Category (equipment, operations, scheduling, maintenance)
  - `description` - Detailed description
  - `estimated_savings_potential` - Percentage savings potential
  - `confidence` - Confidence level (high/medium/low)
- `priority_order` - Recommended investigation order

**Usage Notes:**
- Best used after `energy_analyze_consumption` for context
- This operation identifies and diagnoses opportunities; it does not produce implementation recommendations - those come from the efficiency_optimization skill

### 3. energy_calculate_carbon_footprint

Calculate carbon footprint from energy consumption data.

**Parameters:**
- `facility_id` (required) - Facility identifier from the facility database, sourced from the user
- `start_date` (required) - Calculation period start (YYYY-MM-DD)
- `end_date` (required) - Calculation period end (YYYY-MM-DD)
- `include_breakdown` (optional) - Include breakdown by energy source (default: true)

**Returns (closed enumeration - do not add extra fields):**
- `total_emissions_kgco2` - Total carbon emissions in kg CO2 equivalent
- `emission_intensity` - Emissions per square meter and per kWh
- `breakdown` - Emissions by energy source (electricity, natural gas)
- `comparison` - Comparison to previous period (if data available)

**Usage Notes:**
- Uses the tool's built-in US-average emission factors (electricity 0.42 kg CO2/kWh, natural gas 2.0 kg CO2/m3); no region parameter exists
- Scope 2 reporting method (market-based vs location-based) is not a tool parameter and the tool does not distinguish them; do not present dual interpretations

## Execution Limits

- Maximum retries per tool call: 3. Timeout: 60 seconds per call. Maximum tool calls per execution: 10.
- Limit each response to at most 1,000 English words.
- Partial results are acceptable. When information is insufficient for a section, skip it or mark it as "information not available".

## Failure Handling Policy

- If a tool call fails, report the error to the user. You may retry the identical call at most 3 times (per max_retries); if the retry also fails, stop immediately, report the error, and do not attempt alternative tools or workarounds.
- After a failure, do not expand the task scope, fabricate data to fill gaps (e.g., invented anomalies, benchmarks, or emission figures), or lower quality standards.
- The max_items: 10 declaration applies to user-submitted request items only. Tool RESULT payloads may contain up to 50 anomalies or 24 peak-hour entries per the tool schema; when validating findings, review the tool result's data object but limit the presented summary to at most 10 findings.

## Permissions and Environment Boundaries

- Allowed operations: read, list, and query. Prohibited operations: write, update, delete, insert, overwrite, and DROP.
- Use only the declared local data files (data/consumption_patterns.json, data/facilities.json, data/equipment.json). Do not access conversation history, external systems, production databases, production APIs, live systems, or unauthorized external services.
- Chained invocation: this skill may invoke only the three tools under allowed_operations. Invoking other skills or tools is prohibited.

## Data Sources

Consumption data and facility information come from:
- `data/consumption_patterns.json` - Sample consumption records
- `data/facilities.json` - Facility configurations
- `data/equipment.json` - Equipment inventories

Emission factors are built into the tool code itself (not read from these files).

## Important Constraints

- Carbon calculations use the tool's built-in US-average factors; production use should integrate verified regional data
- All findings should be validated against actual operational data before making decisions (bounded by the 10-finding limit above)