---
name: shipment_tracking
description: Shipment tracking skill for querying shipment status and history by tracking number, and listing shipments filtered by origin and/or destination city names (with optional status and date-range filters).
invocation:
  - "shipment status by tracking number"
  - "shipment tracking history"
  - "list shipments between two cities"
  - "list shipments between two cities in a date range"
  - "where is my freight shipment"
non_goals:
  - creating or modifying shipments
  - delivery re-scheduling
  - carrier dispute handling
allowed_operations:
  - shipment_get_status
  - shipment_get_history
  - shipment_list_by_route
allowed_resources:
  - data/shipments.json
side_effects: none
max_items: 50
data_sensitivity: low sensitivity - tool results contain only tracking numbers, city names, statuses, carrier names, and dates; no consignee PII is returned
partial_result_allowed: true
max_retries: 3
max_tool_calls: 12
timeout_seconds: 60
tools:
  - shipment_get_status
  - shipment_get_history
  - shipment_list_by_route
---

# Shipment Tracking Skill

## Overview

The shipment tracking skill provides shipment visibility: query current status by tracking number, retrieve full tracking history, and list shipments filtered by origin/destination city names, status, or date range. This skill is read-only and does not support booking or modifying shipments. Tool results contain only operational fields (tracking numbers, cities, statuses, carriers, dates); the system prompt's privacy filtering rules still apply to any personal data the user volunteers. Region-based filtering is not supported — listing works only with city names. When a user supplies a region (e.g., "South China") instead of city names, ask them for the specific origin or destination city instead of passing the region string as a city filter.

## When to Use

Use this skill when:
- User provides a tracking number and asks for status
- User asks where their freight shipment is or when it will arrive
- User wants to see tracking history or delivery timeline
- User wants to list shipments between cities

Do NOT activate this skill for:
- Booking, modifying, or re-scheduling shipments
- Carrier dispute or claim handling
- Non-freight parcel tracking from other services

## Input Handling

- `tracking_number` comes from the user (format: FR + exactly 14 digits). When the tracking number is missing, malformed, or the user says "where is my shipment" without a number, ask the user for the tracking number or origin/destination instead of guessing. Never fabricate tracking numbers.
- max_items: 50 applies to a single shipment_list_by_route call's returned rows (the tool's limit parameter caps results at 50). Each tool call handles one tracking number or one route filter set. If the user submits more tracking numbers than the per-conversation tool-call budget allows (12 total per the system prompt), ask them to prioritize.

## Available Operations

1. **shipment_get_status** - Query current shipment status
   - Parameter: `tracking_number` (required) — Format: FR followed by exactly 14 digits, 16 characters total (e.g., FR20260930000123)
   - Returns (closed enumeration): `status`, `current_location`, `eta`, `carrier`, `origin`, `destination`, `last_update`
   - Status values: `pending`, `picked_up`, `in_transit`, `out_for_delivery`, `delivered`, `exception`

2. **shipment_get_history** - Get full tracking history
   - Parameter: `tracking_number` (required) — Format: FR followed by exactly 14 digits
   - Returns (closed enumeration): List of tracking events with `timestamp`, `location`, `status`, `description`

3. **shipment_list_by_route** - List shipments by route
   - Parameter: `origin` (required if destination not provided) — Filter by origin city (partial match supported)
   - Parameter: `destination` (required if origin not provided) — Filter by destination city (partial match supported)
   - Parameter: `status` (optional) — Filter by status; allowed values only: pending, picked_up, in_transit, out_for_delivery, delivered, exception (user terms like "delayed" map to "exception" only if the user confirms)
   - Parameter: `date_from` / `date_to` (optional) — Date range filter (YYYY-MM-DD format)
   - Parameter: `limit` (optional) — Maximum results, 1-50, default 50
   - Trigger rule: invoke only when at least one of origin or destination has been confirmed with the user
   - Returns (closed enumeration): List of shipments with tracking numbers, status, and routes
   - Note: This operation does not accept a route_id; route-based lookup means filtering by origin and/or destination city names

## Execution Limits

- Maximum retries per tool call: 3. Timeout: 60 seconds per call. Per conversation turn: at most 2 invocations per tool. Per conversation: at most 12 total tool calls, matching the system prompt's budget.
- Limit each response to at most 1,000 English words.
- Partial results are acceptable: empty or partial result sets (e.g., a date filter matching no shipments) are valid answers — report what was found and stop.

## Failure Handling Policy

- If a tool call fails, report the error to the user. You may retry the identical call at most 3 times (per max_retries); if the retry also fails, stop immediately, report the error, and do not attempt alternatives such as guessing partial tracking numbers or dumping all shipments.
- After a failure, do not expand the task scope, fabricate shipment data (e.g., invented status or ETA for an unrecognized tracking number), or lower quality standards.
- Business-level exception states (delayed, damaged, lost) are normal results, not failures: report them and advise the user to contact the carrier.

## Permissions and Environment Boundaries

- Allowed operations: read, list, and query. Prohibited: write, update, delete, insert, and overwrite.
- Use only the declared local data file (data/shipments.json). Do not access conversation history for data. Never access external systems, external carrier APIs, production databases, production APIs, live systems, or unauthorized external services. Allowed operations are exactly the three tools listed under allowed_operations (shipment_get_status, shipment_get_history, shipment_list_by_route), all read-only queries; prohibited operations: write, update, delete, insert, overwrite, and DROP.
- Chained invocation: this skill may invoke only the three tools under allowed_operations. Invoking other skills or tools (booking, modification, notification, export) is prohibited.

## Data Source

Shipment data comes from built-in mock data: `data/shipments.json`. No real carrier APIs are called. Tracking numbers follow format `FR` followed by exactly 14 digits (e.g., FR20260930000123).

## Important Notes

- This skill cannot create, modify, or cancel shipments
- ETA is estimated and may differ from actual delivery
- For exceptions (delayed, damaged, lost), advise user to contact carrier directly
- If a tool result ever contains personal data beyond the operational fields above, redact it per the system prompt's privacy filtering rules