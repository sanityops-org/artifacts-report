---
name: destination_search
description: Search and explore travel destinations
---

# Destination Search Skill

## Purpose
Help users find and learn about travel destinations based on their preferences.

## Available Tools

### destination_search
Search destinations by query, country, or travel theme.

**Parameters:**
- `query` (optional): Search term
- `country` (optional): Filter by country
- `theme` (optional): Filter by theme (beach, mountain, city, culture, adventure, family, romantic, foodie)

**Example:**
```
User: I want to visit a beach destination
→ destination_search(theme="beach")
```

### destination_details
Get detailed information about a specific destination.

**Parameters:**
- `destination_id` (required): Destination ID

**Example:**
```
User: Tell me more about Paris
→ destination_details(destination_id="DEST001")
```

### attraction_list
List attractions in a destination.

**Parameters:**
- `destination_id` (required): Destination ID
- `category` (optional): Filter by category
- `min_rating` (optional): Minimum rating

**Example:**
```
User: What attractions are in Tokyo?
→ attraction_list(destination_id="DEST002")
```

### attraction_details
Get detailed information about a specific attraction.

**Parameters:**
- `attraction_id` (required): Attraction ID

## Workflow

1. User expresses interest in a destination or theme
2. Use `destination_search` to find matching destinations
3. Present options to user
4. User selects a destination
5. Use `destination_details` to show full information
6. Use `attraction_list` to show available activities
