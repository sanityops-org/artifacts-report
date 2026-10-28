---
name: accommodation_search
description: Find and compare accommodations
---

# Accommodation Search Skill

## Purpose
Help users find suitable accommodations for their trips.

## Available Tools

### accommodation_search
Search accommodations with filters.

**Parameters:**
- `destination_id` (required): Destination ID
- `type` (optional): hotel/hostel/resort/apartment
- `max_price` (optional): Maximum price per night (USD)
- `min_rating` (optional): Minimum rating (1.0-5.0)

**Example:**
```
User: Find hotels in Barcelona under $150
→ accommodation_search(destination_id="DEST005", type="hotel", max_price=150)
```

### accommodation_details
Get detailed information about a specific accommodation.

**Parameters:**
- `accommodation_id` (required): Accommodation ID

## Workflow

1. User needs accommodation
2. Use `accommodation_search` with filters
3. Present options sorted by rating
4. User selects accommodation
5. Use `accommodation_details` for full information
