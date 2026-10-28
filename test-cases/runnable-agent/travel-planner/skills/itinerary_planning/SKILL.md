---
name: itinerary_planning
description: Create and manage travel itineraries
---

# Itinerary Planning Skill

## Purpose
Create detailed day-by-day travel itineraries and estimate trip budgets.

## Available Tools

### itinerary_create
Generate a travel itinerary for a destination.

**Parameters:**
- `destination_id` (required): Destination ID
- `duration_days` (required): Trip duration (1-14 days)
- `theme` (optional): Travel theme preference
- `start_date` (optional): Start date (YYYY-MM-DD)

**Example:**
```
User: Plan a 5-day trip to Paris
→ itinerary_create(destination_id="DEST001", duration_days=5)
```

### itinerary_details
View details of a saved itinerary.

**Parameters:**
- `itinerary_id` (required): Itinerary ID

### budget_estimate
Estimate trip budget.

**Parameters:**
- `destination_id` (required): Destination ID
- `duration_days` (required): Trip duration
- `budget_level` (optional): budget/moderate/luxury
- `travelers_count` (optional): Number of travelers

**Example:**
```
User: How much will a week in Tokyo cost?
→ budget_estimate(destination_id="DEST002", duration_days=7)
```

## Workflow

1. User wants to plan a trip
2. Use `destination_search` to find destination
3. User selects destination and duration
4. Use `itinerary_create` to generate plan
5. Present day-by-day itinerary
6. Use `budget_estimate` to show costs
7. Always include disclaimer about approximate estimates
