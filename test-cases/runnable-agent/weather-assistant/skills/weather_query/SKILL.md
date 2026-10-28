---
name: weather_query
description: Weather query skill
---

# Weather Query Skill

## Overview

Weather query skill provides location search, current conditions, and multi-day forecast capabilities.

## When to Use

Use this skill when the user wants to:
- Find a location by name
- Get current weather conditions
- Get a multi-day weather forecast

## Available Operations

### location_search
- **Parameters**: `query` (string, required)
- **Returns**: List of matching locations

### weather_current
- **Parameters**: `location_id` (string, required)
- **Returns**: Current weather conditions

### weather_forecast
- **Parameters**: `location_id` (string, required), `days` (integer, optional, 1-7, default 5)
- **Returns**: Multi-day forecast

## Data Source

All data loaded from JSON files via DataStore.
