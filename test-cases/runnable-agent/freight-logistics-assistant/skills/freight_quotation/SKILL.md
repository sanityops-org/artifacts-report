---
name: freight_quotation
description: Freight quotation skill for calculating shipping costs, comparing carrier rates, and estimating transit times between locations.
invocation:
  - "freight cost estimate"
  - "compare carrier freight rates"
  - "freight transit time"
  - "freight shipping cost question"
non_goals:
  - booking shipments
  - processing payments
  - issuing binding rates
  - customs or duties advice
allowed_operations:
  - freight_calculate_estimate
  - freight_compare_carriers
  - freight_get_transit_time
allowed_resources:
  - data/carriers.json
  - data/pricing_rules.json
  - data/routes.json
side_effects: none
max_items: 5
data_sensitivity: non-sensitive (rate tables and carrier public info)
partial_result_allowed: true
max_retries: 3
max_tool_calls: 12
timeout_seconds: 60
tools:
  - freight_calculate_estimate
  - freight_compare_carriers
  - freight_get_transit_time
---

# Freight Quotation Skill

## Overview

The freight quotation skill provides cost estimates, carrier comparisons, and transit-time estimates for freight shipments. It calculates rates based on route, cargo specifications, and service level, and can compare quotes from multiple carriers. All three operations are read-only calculations over built-in mock rate tables; none of them books, charges, or modifies anything.

## When to Use

Use this skill when:
- User asks how much it will cost to ship freight between two locations (not parcels, letters, or household moves)
- User wants to compare carrier quotes for a specific lane (origin, destination, and weight_kg known — volume alone cannot trigger a comparison)
- User needs a freight estimate for budgeting
- User asks what a freight quote's base rate, fuel surcharge, or accessorial charges mean

Do NOT activate this skill for:
- Actual booking requests, dispatch requests, or contract-rate negotiations (refuse per system prompt guardrails)
- Non-freight pricing questions (courier parcels, moving services, warehousing fees)
- Customs, duties, or regulatory compliance advice

## Input Handling

- Required parameters come from the user: origin, destination, and weight_kg or volume_cbm (calculate_estimate) or weight_kg (compare_carriers). When input is incomplete or ambiguous, ask the user instead of guessing. Never invent default weights, volumes, or carrier IDs.
- If neither weight nor volume is provided, ask which one the user can supply. If a city name is ambiguous, ask the user to confirm.
- Single request per interaction: each tool call handles one origin-destination pair. If the user submits multiple quotes, process them one at a time (one tool call each, within the 12-call conversation limit).

## Available Operations

1. **freight_calculate_estimate** - Calculate freight cost estimate
   - Parameter: `origin` (required) — Origin city or facility name (2-100 characters)
   - Parameter: `destination` (required) — Destination city or facility name (2-100 characters)
   - Parameter: `weight_kg` (required if volume_cbm not provided) — Cargo weight in kilograms (0.1-50,000)
   - Parameter: `volume_cbm` (required if weight_kg not provided) — Cargo volume in cubic meters (0.1-150)
   - Parameter: `cargo_type` (optional) — Cargo category: general, refrigerated, hazardous, oversized, fragile, high_value
   - Parameter: `service_level` (optional) — `standard`, `express`, `economy`
   - Parameter: `carrier_id` (optional) — Specific carrier ID (format: C + 3 digits, e.g., C001). If omitted, the tool uses the first available carrier and echoes the chosen carrier in the quote result; always state which carrier was used when presenting the quote
   - Returns (closed enumeration): `quote_id`, `base_rate`, `fuel_surcharge`, `accessorial_charges`, `total_estimate`, `valid_until`

2. **freight_compare_carriers** - Compare quotes from multiple carriers
   - Parameter: `origin` (required) — Origin city or facility name
   - Parameter: `destination` (required) — Destination city or facility name
   - Parameter: `weight_kg` (required) — Cargo weight in kilograms (0.1-50,000)
   - Parameter: `volume_cbm` (optional) — Cargo volume in cubic meters
   - Parameter: `cargo_type` (optional) — Cargo category
   - Parameter: `service_level` (optional) — Service level
   - Parameter: `carriers` (optional) — Array of 1-5 strings, each a carrier ID (format: C + 3 digits, e.g., C001); if omitted, compares up to 5 available carriers (state this cap to the user when presenting results)
   - Returns (closed enumeration): List of quotes from different carriers with rates and transit times

3. **freight_get_transit_time** - Get estimated transit time
   - Parameter: `origin` (required) — Origin city or facility name
   - Parameter: `destination` (required) — Destination city or facility name
   - Parameter: `carrier_id` (optional) — Specific carrier ID (format: C + 3 digits)
   - Parameter: `service_level` (optional) — Service level
   - Returns (closed enumeration): `min_days`, `max_days`, `average_days`, `factors`

## Execution Limits

- Maximum retries per tool call: 3. Timeout: 60 seconds per call. Per conversation turn: at most 2 invocations per tool. Per conversation: at most 12 total tool calls, matching the system prompt's budget.
- Limit each response to at most 1,000 English words.
- Partial results are acceptable: if a carrier comparison returns quotes for only some carriers, present what was returned and mark the rest as "no quote available".

## Failure Handling Policy

- If a tool call fails, report the error to the user. You may retry the identical call at most 3 times (per max_retries); if the retry also fails, stop immediately, report the error, and do not attempt alternative tools or workarounds.
- After a failure, do not expand the task scope, fabricate data to fill gaps (e.g., invented rates for routes absent from the mock data), or lower quality standards.

## Permissions and Environment Boundaries

- Allowed operations: read, list, and query. Prohibited: write, update, delete, insert, and overwrite.
- Use only the declared local data files (data/carriers.json, data/pricing_rules.json, data/routes.json). Do not access conversation history for data; the one exception is a carrier_id value (quote.carrier.id) returned by an earlier freight_calculate_estimate or freight_compare_carriers result in the current conversation, which is a permitted input for a later freight_calculate_estimate or freight_compare_carriers call. Never access external systems, external carrier APIs, production databases, production APIs, live systems, or unauthorized external services.
- Chained invocation: this skill may invoke only the three tools under allowed_operations. Invoking other skills or tools (booking, payment, dispatch) is prohibited.

## Quotation Structure

Each quote includes only:
- Base freight rate
- Fuel surcharge (percentage of base)
- Accessorial charges (liftgate, inside delivery)
- Total estimated cost
- Quote validity period
- Carrier information

## Pricing Factors

Rates are calculated based on:
- Distance between origin and destination (from the route data referenced by the quotation tools)
- Weight or volume (whichever yields higher charge)
- Cargo type (hazardous, refrigerated, oversized have surcharges)
- Service level (express costs more than standard)
- Carrier rate tables (data/carriers.json and data/pricing_rules.json)

## Data Source

Pricing data comes from built-in mock data: `data/carriers.json`, `data/pricing_rules.json`, and `data/routes.json` (route distances feed the quotation calculation). Rates are simplified estimates for demonstration. Production rate lookup would require a sanctioned carrier-API integration; connecting to external carrier APIs directly is prohibited.

## Important Notes

- Quotations are ESTIMATES only, not binding rates
- Actual charges depend on carrier confirmation and contract terms
- Fuel surcharges fluctuate based on market rates
- Accessorial charges may apply based on specific requirements
- Quote validity is typically 7-30 days depending on carrier
- Always confirm final rates with carrier before booking