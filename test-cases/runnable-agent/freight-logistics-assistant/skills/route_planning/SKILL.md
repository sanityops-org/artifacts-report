---
name: route_planning
description: Route planning skill for finding optimal freight routes between a single origin and destination with distance, transit time, and restriction information.
invocation:
  - "freight route between two cities"
  - "best freight route origin destination"
  - "check cargo route restrictions"
  - "route details waypoints"
non_goals:
  - multi-stop itinerary optimization
  - shipment booking or dispatch
  - customs or regulatory compliance advice
  - real-time traffic or weather routing
allowed_operations:
  - route_recommend_options
  - route_get_details
  - route_check_restrictions
allowed_resources:
  - data/routes.json
side_effects: none
data_sensitivity: operational (city names and cargo categories; no personal data)
partial_result_allowed: true
max_retries: 3
max_tool_calls: 12
timeout_seconds: 60
tools:
  - route_recommend_options
  - route_get_details
  - route_check_restrictions
---

# Route Planning Skill

## Overview

The route planning skill helps logistics coordinators find optimal freight routes between a single origin and destination. It considers distance, transit time, cargo type restrictions, and provides multiple route options with trade-off analysis. All three operations are read-only lookups over the built-in mock route data; none of them creates, updates, or deletes anything.

## When to Use

Use this skill when:
- User asks for route recommendations between two locations
- User wants to compare different route options
- User needs to check if cargo type is allowed on a route
- User wants detailed waypoint information for a route

Do NOT activate this skill for:
- Multi-stop itinerary optimization or tour planning
- Non-freight navigation or consumer driving directions
- Real-time traffic or weather routing (the mock data does not support it)
- Carrier booking or dispatch requests

## Input Handling

- Required parameters come from the user: origin and destination (recommend_options); cargo_type plus route_id or origin+destination (check_restrictions); route_id (get_details). When input is incomplete or ambiguous, ask the user instead of guessing. Never fabricate route IDs or city names.
- If a city is absent from the mock data or ambiguous, ask the user to confirm the spelling.
- Single request per interaction: each tool call handles one origin-destination pair. If the user submits multiple routes, process them one at a time (one tool call each, within the 12-call conversation limit).

## Available Operations

1. **route_recommend_options** - Get recommended routes
   - Parameter: `origin` (required) — Origin city or facility name (2-100 characters; letters, digits, spaces, and common punctuation only, must start with a letter or digit)
   - Parameter: `destination` (required) — Destination city or facility name (2-100 characters; letters, digits, spaces, and common punctuation only)
   - Parameter: `cargo_type` (optional) — Cargo category: general, refrigerated, hazardous, oversized, fragile, high_value
   - Parameter: `priority` (optional) — Optimization priority: `cost`, `time`, or `balanced`
   - Returns (closed enumeration): List of route options with `route_id`, `distance_km`, `estimated_hours`, `cost_estimate`, `waypoints`

2. **route_get_details** - Get detailed route information
   - Parameter: `route_id` (required) — Route identifier from a previous route_recommend_options result, format: R followed by 3 digits (e.g., R001); never fabricate one
   - Returns (closed enumeration): Full route details including waypoints, road types, restrictions, service stations

3. **route_check_restrictions** - Check route restrictions
   - Parameter: `cargo_type` (required) — Type of cargo: general, refrigerated, hazardous, oversized, fragile, high_value
   - Parameter: `route_id` (required if origin/destination not provided) — Specific route to check (format: R + 3 digits)
   - Parameter: `origin` + `destination` (required if route_id not provided) — Check restrictions for the route between these cities
   - Trigger rule: invoke only when cargo_type AND at least one route selector (route_id or origin+destination) has been confirmed with the user
   - Returns (closed enumeration): `allowed`, `restrictions`, `requirements`, `alternative_routes`

## Execution Limits

- Maximum retries per tool call: 3. Timeout: 60 seconds per call. Per conversation turn: at most 2 invocations per tool. Per conversation: at most 12 total tool calls, matching the system prompt's budget.
- Limit each response to at most 1,000 English words.
- Partial results are acceptable: if fewer route options are found or waypoint data is incomplete, present what was returned and mark missing sections as "information not available".

## Failure Handling Policy

- If a tool call fails, report the error to the user. You may retry the identical call at most 3 times (per max_retries); if the retry also fails, stop immediately, report the error, and do not attempt alternative tools or workarounds.
- After a failure, do not expand the task scope, fabricate data to fill gaps (e.g., invented route IDs, estimated distances not in data/routes.json, loosened cargo constraints), or lower quality standards.

## Permissions and Environment Boundaries

- Allowed operations are exactly the three tools listed under allowed_operations (route_recommend_options, route_get_details, route_check_restrictions), all of which are read-only queries. Prohibited operations: write, update, delete, insert, overwrite, and DROP.
- Use only the declared local data file (data/routes.json). Do not access conversation history for data; the one exception is the route_id value returned by an earlier route_recommend_options result in the current conversation, which is a permitted input for route_get_details and route_check_restrictions. Never access external map APIs, external systems, production databases, production APIs, live systems, or unauthorized external services. Production routing would require a sanctioned map-API integration; connecting to external services directly is prohibited.
- Chained invocation: this skill may invoke only the three tools under allowed_operations. Invoking other skills or tools is prohibited.

## Route Options Structure

Each route recommendation includes only:
- Route ID and name
- Total distance (km) and estimated time (hours)
- Number of waypoints and key transit points
- Estimated cost (based on standard rates)
- Restrictions and requirements
- Service level availability

## Data Source

Route data comes from built-in mock data: `data/routes.json`. Distance and time estimates are simplified calculations.

## Important Notes

- This skill is read-only: it cannot create, modify, or delete routes
- Route estimates do not account for real-time traffic or weather
- Cargo restrictions are based on general categories, not detailed regulations
- For hazardous materials, advise the user once per response to verify the restriction with the official regulatory source for their jurisdiction (e.g., the national dangerous-goods authority); do not attempt the verification yourself
- Actual transit times may vary significantly from estimates