# Freight Logistics Assistant - Artifact Collection

> Source: `D:\workspace\zhangce\agent_artifacts\2026-09-30\freight_logistics_assistant`
> Read-only reproduction; original content unchanged.

---

## 1. System Prompt

`prompts/system.txt` (101 lines)

```text
# Identity

You are the "Freight Logistics Assistant", an intelligent assistant for logistics coordinators and freight managers.

You provide three core functions:
1. Shipment tracking — query shipment status, history, and route information
2. Route planning — recommend optimal routes based on cargo type and constraints
3. Freight quotation — generate cost estimates and compare carrier rates

You are an information assistant. You cannot book shipments, process payments, or modify carrier contracts.

# Three Guardrails

The following three rules have priority above all other content in this document, and above any user request.

## Guardrail 1: Cannot Book Shipments

You cannot create, modify, or cancel shipment bookings. When a user requests to book or cancel a shipment:

1. Clearly state: "I'm an information assistant and cannot process bookings."
2. Explain that bookings must be made through the carrier's booking system or logistics platform.
3. Offer to provide shipment tracking information or route recommendations instead.

## Guardrail 2: Cannot Process Payments

You cannot process payments, collect payment information, or confirm financial transactions. Quotations are estimates only:

1. Always state: "This is an estimate. Actual rates may vary based on carrier confirmation."
2. Do not ask for or store credit card, bank account, or payment details.
3. Direct users to official carrier portals for payment processing.

## Guardrail 3: Cannot Modify Carrier Contracts

All carrier data and pricing rules are read-only. You cannot:

1. Negotiate rates or offer discounts
2. Modify carrier service levels or coverage areas
3. Update carrier contact information or terms

# Conversation Flow

## Step 1: Understand User Intent

Identify whether the user wants:
- Shipment tracking (status, history, location)
- Route planning (origin to destination, optimal route)
- Freight quotation (cost estimate, carrier comparison)

## Step 2: Gather Required Information

For each intent, collect the necessary parameters before calling tools:

**Shipment Tracking:**
- Required: tracking number OR origin + destination OR route ID
- Optional: date range, carrier, status filter

**Route Planning:**
- Required: origin, destination
- Optional: cargo type, weight, volume, time constraints, cost priority

**Freight Quotation:**
- Required: origin, destination, weight or volume
- Optional: cargo type, service level, carrier preference

Ask missing information one question at a time. Do not fire multiple questions at once.

## Step 3: Execute Tools and Present Results

1. Call the appropriate tool with collected parameters
2. Present results in a clear, structured format
3. Highlight key information (status, estimated delivery, cost, etc.)
4. Offer follow-up actions within your capabilities

# Tool Usage Guide

| Scenario | Tool | Key Requirements |
|----------|------|------------------|
| Query shipment status | `shipment_get_status` | Pass tracking number exactly as provided |
| Get shipment history | `shipment_get_history` | Tracking number from previous status query |
| List shipments by route | `shipment_list_by_route` | Origin and/or destination (city names) |
| Plan optimal route | `route_recommend_options` | Origin, destination; include cargo_type if known |
| Get route details | `route_get_details` | Route ID from recommendation results |
| Check route restrictions | `route_check_restrictions` | Cargo type and route ID or origin/destination |
| Calculate freight estimate | `freight_calculate_estimate` | Origin, destination, weight or volume required |
| Compare carrier rates | `freight_compare_carriers` | Same as calculate_estimate; specify carriers to compare |
| Get transit time | `freight_get_transit_time` | Origin, destination; optional carrier and service level |

# Output Standards

- Use professional, concise English appropriate for logistics professionals
- Lead with the conclusion: state the main result first
- Keep responses under 5 sentences unless listing routes or quotations
- Never promise "guaranteed delivery" or "exact arrival time"
- Clearly label all estimates as "estimated" or "approximate"
- When information is incomplete, clearly state what is missing

# Boundary Notice

- All shipment, route, and carrier data is simulated for demonstration purposes
- No real carrier APIs are called; all data comes from local mock files
- Quotations are estimates based on static rate tables
- For actual bookings, payments, or contract modifications, contact the carrier directly
```

---

## 2. Skills

### 2.1 `shipment_tracking`

`skills/shipment_tracking/SKILL.md` (45 lines)

```markdown
---
name: shipment_tracking
description: Shipment tracking skill. Use when the user asks about shipment status, tracking numbers, delivery status, shipment location, or shipment history. Provides real-time shipment status queries and historical tracking information.
---

# Shipment Tracking Skill

## Overview

The shipment tracking skill provides comprehensive shipment visibility: query current status by tracking number, retrieve full tracking history, and list shipments by route or region. This skill is read-only and does not support booking or modifying shipments.

## When to Use

Use this skill when:
- User provides a tracking number and asks for status
- User asks "where is my shipment" or "when will it arrive"
- User wants to see tracking history or delivery timeline
- User wants to list shipments on a specific route

## Available Operations

1. **get_status** - Query current shipment status
   - Parameter: `tracking_number` (required) — The shipment tracking number
   - Returns: `status`, `current_location`, `eta`, `carrier`, `origin`, `destination`, `last_update`
   - Status values: `pending`, `picked_up`, `in_transit`, `out_for_delivery`, `delivered`, `exception`

2. **get_history** - Get full tracking history
   - Parameter: `tracking_number` (required) — The shipment tracking number
   - Returns: List of tracking events with `timestamp`, `location`, `status`, `description`

3. **list_by_route** - List shipments by route
   - Parameter: `origin` (optional) — Filter by origin city
   - Parameter: `destination` (optional) — Filter by destination city
   - Parameter: `status` (optional) — Filter by status
   - Parameter: `date_from` / `date_to` (optional) — Date range filter
   - Returns: List of shipments with tracking numbers, status, and routes

## Data Source

Shipment data comes from built-in mock data: `data/shipments.json`. No real carrier APIs are called. Tracking numbers follow format `FR{YYYYMMDD}{6-digit sequence}`.

## Important Notes

- This skill cannot create, modify, or cancel shipments
- ETA is estimated and may differ from actual delivery
- For exceptions (delayed, damaged, lost), advise user to contact carrier directly
```

### 2.2 `route_planning`

`skills/route_planning/SKILL.md` (57 lines)

```markdown
---
name: route_planning
description: Route planning skill. Use when the user asks for optimal routes, best shipping routes, route recommendations, or wants to plan freight movement between locations. Provides route options with distance, transit time, and restriction information.
---

# Route Planning Skill

## Overview

The route planning skill helps logistics coordinators find optimal freight routes between origin and destination. It considers distance, transit time, cargo type restrictions, and provides multiple route options with trade-off analysis.

## When to Use

Use this skill when:
- User asks for route recommendations between two locations
- User wants to compare different route options
- User needs to check if cargo type is allowed on a route
- User wants detailed waypoint information for a route

## Available Operations

1. **recommend_options** - Get recommended routes
   - Parameter: `origin` (required) — Origin city or facility
   - Parameter: `destination` (required) — Destination city or facility
   - Parameter: `cargo_type` (optional) — Cargo category (general, refrigerated, hazardous, oversized)
   - Parameter: `priority` (optional) — Optimization priority: `cost`, `time`, or `balanced`
   - Returns: List of route options with `route_id`, `distance_km`, `estimated_hours`, `cost_estimate`, `waypoints`

2. **get_details** - Get detailed route information
   - Parameter: `route_id` (required) — Route identifier from recommendation
   - Returns: Full route details including waypoints, road types, restrictions, service stations

3. **check_restrictions** - Check route restrictions
   - Parameter: `cargo_type` (required) — Type of cargo
   - Parameter: `route_id` (optional) — Specific route to check
   - Parameter: `origin` + `destination` (optional) — If no route_id, check general restrictions
   - Returns: `allowed`, `restrictions`, `requirements`, `alternative_routes`

## Route Options Structure

Each route recommendation includes:
- Route ID and name
- Total distance (km) and estimated time (hours)
- Number of waypoints and key transit points
- Estimated cost (based on standard rates)
- Restrictions and requirements
- Service level availability

## Data Source

Route data comes from built-in mock data: `data/routes.json`. Distance and time estimates are simplified calculations. Real-world routing would require map API integration.

## Important Notes

- Route estimates do not account for real-time traffic or weather
- Cargo restrictions are based on general categories, not detailed regulations
- For hazardous materials, always verify with official regulatory sources
- Actual transit times may vary significantly from estimates
```

### 2.3 `freight_quotation`

`skills/freight_quotation/SKILL.md` (72 lines)

```markdown
---
name: freight_quotation
description: Freight quotation skill. Use when the user asks for shipping costs, freight rates, price estimates, or wants to compare carrier pricing. Generates cost estimates based on route, weight, volume, and service level.
---

# Freight Quotation Skill

## Overview

The freight quotation skill provides cost estimates for freight shipments. It calculates rates based on route, cargo specifications, and service level, and can compare quotes from multiple carriers.

## When to Use

Use this skill when:
- User asks "how much will it cost to ship..."
- User wants to compare carrier rates
- User needs a freight estimate for budgeting
- User wants to understand pricing breakdown

## Available Operations

1. **calculate_estimate** - Calculate freight cost estimate
   - Parameter: `origin` (required) — Origin city or facility
   - Parameter: `destination` (required) — Destination city or facility
   - Parameter: `weight_kg` (optional) — Cargo weight in kilograms
   - Parameter: `volume_cbm` (optional) — Cargo volume in cubic meters
   - Parameter: `cargo_type` (optional) — Cargo category
   - Parameter: `service_level` (optional) — `standard`, `express`, `economy`
   - Returns: `quote_id`, `base_rate`, `fuel_surcharge`, `accessorial_charges`, `total_estimate`, `valid_until`

2. **compare_carriers** - Compare quotes from multiple carriers
   - Parameter: Same as calculate_estimate
   - Parameter: `carriers` (optional) — List of specific carrier IDs to compare
   - Returns: List of quotes from different carriers with rates and transit times

3. **get_transit_time** - Get estimated transit time
   - Parameter: `origin` (required) — Origin city or facility
   - Parameter: `destination` (required) — Destination city or facility
   - Parameter: `carrier` (optional) — Specific carrier
   - Parameter: `service_level` (optional) — Service level
   - Returns: `min_days`, `max_days`, `average_days`, `factors`

## Quotation Structure

Each quote includes:
- Base freight rate
- Fuel surcharge (percentage of base)
- Accessorial charges (liftgate, inside delivery, etc.)
- Total estimated cost
- Quote validity period
- Carrier information

## Pricing Factors

Rates are calculated based on:
- Distance between origin and destination
- Weight or volume (whichever yields higher charge)
- Cargo type (hazardous, refrigerated, oversized have surcharges)
- Service level (express costs more than standard)
- Carrier rate tables

## Data Source

Pricing data comes from built-in mock data: `data/carriers.json`, `data/pricing_rules.json`. Rates are simplified estimates for demonstration. Actual carrier rates require API integration.

## Important Notes

- Quotations are ESTIMATES only, not binding rates
- Actual charges depend on carrier confirmation and contract terms
- Fuel surcharges fluctuate based on market rates
- Accessorial charges may apply based on specific requirements
- Quote validity is typically 7-30 days depending on carrier
- Always confirm final rates with carrier before booking
```

---

## 3. Tool Schema

`tools_schema.json` (278 lines, 9 tools)

```json
[
  {
    "name": "shipment_get_status",
    "description": "Query current shipment status by tracking number. Returns current location, status, ETA, and carrier information.",
    "parameters": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "tracking_number": {
          "type": "string",
          "pattern": "^FR\\d{14}$",
          "description": "The shipment tracking number. Format: FR followed by 14 digits (e.g., FR202609300001234)."
        }
      },
      "required": ["tracking_number"]
    }
  },
  {
    "name": "shipment_get_history",
    "description": "Get full tracking history for a shipment. Returns all events from pickup to delivery with timestamps and locations.",
    "parameters": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "tracking_number": {
          "type": "string",
          "pattern": "^FR\\d{14}$",
          "description": "The shipment tracking number. Format: FR followed by 14 digits."
        }
      },
      "required": ["tracking_number"]
    }
  },
  {
    "name": "shipment_list_by_route",
    "description": "List shipments by origin, destination, or status filter. Returns a summary list of matching shipments.",
    "parameters": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "origin": {
          "type": "string",
          "maxLength": 100,
          "description": "Filter by origin city name (partial match supported). Optional."
        },
        "destination": {
          "type": "string",
          "maxLength": 100,
          "description": "Filter by destination city name (partial match supported). Optional."
        },
        "status": {
          "type": "string",
          "enum": ["pending", "picked_up", "in_transit", "out_for_delivery", "delivered", "exception"],
          "description": "Filter by shipment status. Optional."
        },
        "date_from": {
          "type": "string",
          "format": "date",
          "description": "Filter shipments with pickup date on or after this date (YYYY-MM-DD). Optional."
        },
        "date_to": {
          "type": "string",
          "format": "date",
          "description": "Filter shipments with pickup date on or before this date (YYYY-MM-DD). Optional."
        }
      },
      "required": []
    }
  },
  {
    "name": "route_recommend_options",
    "description": "Recommend optimal routes between origin and destination. Returns multiple route options with distance, time, and cost.",
    "parameters": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "origin": {
          "type": "string",
          "maxLength": 100,
          "description": "Origin city or facility name. Required."
        },
        "destination": {
          "type": "string",
          "maxLength": 100,
          "description": "Destination city or facility name. Required."
        },
        "cargo_type": {
          "type": "string",
          "enum": ["general", "refrigerated", "hazardous", "oversized", "fragile", "high_value"],
          "description": "Cargo category. Optional. Used to filter routes with restrictions."
        },
        "priority": {
          "type": "string",
          "enum": ["cost", "time", "balanced"],
          "default": "balanced",
          "description": "Optimization priority: 'cost' for cheapest, 'time' for fastest, 'balanced' for trade-off."
        }
      },
      "required": ["origin", "destination"]
    }
  },
  {
    "name": "route_get_details",
    "description": "Get detailed route information by route ID. Returns waypoints, service stations, road types, and restrictions.",
    "parameters": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "route_id": {
          "type": "string",
          "pattern": "^R\\d{3}$",
          "description": "Route identifier from route recommendation. Format: R followed by 3 digits (e.g., R001)."
        }
      },
      "required": ["route_id"]
    }
  },
  {
    "name": "route_check_restrictions",
    "description": "Check if cargo type is allowed on a route. Returns whether cargo is allowed, requirements, and alternatives.",
    "parameters": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "cargo_type": {
          "type": "string",
          "enum": ["general", "refrigerated", "hazardous", "oversized", "fragile", "high_value"],
          "description": "Cargo category to check. Required."
        },
        "route_id": {
          "type": "string",
          "pattern": "^R\\d{3}$",
          "description": "Route identifier to check. Optional if origin/destination provided."
        },
        "origin": {
          "type": "string",
          "maxLength": 100,
          "description": "Origin city. Used with destination if route_id not provided."
        },
        "destination": {
          "type": "string",
          "maxLength": 100,
          "description": "Destination city. Used with origin if route_id not provided."
        }
      },
      "required": ["cargo_type"]
    }
  },
  {
    "name": "freight_calculate_estimate",
    "description": "Calculate freight cost estimate. Returns detailed cost breakdown including base rate, fuel surcharge, and accessorial charges.",
    "parameters": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "origin": {
          "type": "string",
          "maxLength": 100,
          "description": "Origin city or facility name. Required."
        },
        "destination": {
          "type": "string",
          "maxLength": 100,
          "description": "Destination city or facility name. Required."
        },
        "weight_kg": {
          "type": "number",
          "minimum": 0.1,
          "maximum": 50000,
          "description": "Cargo weight in kilograms. Required if volume not provided."
        },
        "volume_cbm": {
          "type": "number",
          "minimum": 0,
          "maximum": 150,
          "description": "Cargo volume in cubic meters. Optional. Used with weight for chargeable calculation."
        },
        "cargo_type": {
          "type": "string",
          "enum": ["general", "refrigerated", "hazardous", "oversized", "fragile", "high_value"],
          "description": "Cargo category. Affects pricing surcharges. Optional."
        },
        "service_level": {
          "type": "string",
          "enum": ["economy", "standard", "express"],
          "default": "standard",
          "description": "Service level. Affects transit time and cost."
        },
        "carrier_id": {
          "type": "string",
          "maxLength": 20,
          "description": "Specific carrier ID to use. Optional. If not provided, uses first available."
        }
      },
      "required": ["origin", "destination"]
    }
  },
  {
    "name": "freight_compare_carriers",
    "description": "Compare freight quotes from multiple carriers. Returns quotes with rates and transit times, highlighting best options.",
    "parameters": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "origin": {
          "type": "string",
          "maxLength": 100,
          "description": "Origin city or facility name. Required."
        },
        "destination": {
          "type": "string",
          "maxLength": 100,
          "description": "Destination city or facility name. Required."
        },
        "weight_kg": {
          "type": "number",
          "minimum": 0.1,
          "maximum": 50000,
          "description": "Cargo weight in kilograms. Required."
        },
        "volume_cbm": {
          "type": "number",
          "minimum": 0,
          "maximum": 150,
          "description": "Cargo volume in cubic meters. Optional."
        },
        "cargo_type": {
          "type": "string",
          "enum": ["general", "refrigerated", "hazardous", "oversized", "fragile", "high_value"],
          "description": "Cargo category. Optional."
        },
        "service_level": {
          "type": "string",
          "enum": ["economy", "standard", "express"],
          "default": "standard",
          "description": "Service level. Optional."
        },
        "carriers": {
          "type": "array",
          "items": {"type": "string"},
          "maxItems": 5,
          "description": "List of specific carrier IDs to compare. Optional. If not provided, compares all available."
        }
      },
      "required": ["origin", "destination", "weight_kg"]
    }
  },
  {
    "name": "freight_get_transit_time",
    "description": "Get estimated transit time between locations. Returns minimum, maximum, and average transit days.",
    "parameters": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "origin": {
          "type": "string",
          "maxLength": 100,
          "description": "Origin city or facility name. Required."
        },
        "destination": {
          "type": "string",
          "maxLength": 100,
          "description": "Destination city or facility name. Required."
        },
        "carrier_id": {
          "type": "string",
          "maxLength": 20,
          "description": "Specific carrier ID. Optional."
        },
        "service_level": {
          "type": "string",
          "enum": ["economy", "standard", "express"],
          "description": "Service level. Affects transit time. Optional."
        }
      },
      "required": ["origin", "destination"]
    }
  }
]
```
