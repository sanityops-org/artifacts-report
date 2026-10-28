---
name: severe_weather
description: Severe weather alerts skill
---

# Severe Weather Alerts Skill

## Overview

Severe weather alerts skill provides alert querying and subscription capabilities.

## When to Use

Use this skill when the user wants to:
- Check for active severe weather alerts
- Get alerts for a specific location
- Get details of a specific alert
- Subscribe to alerts for a location

## Available Operations

### alert_query_active
- **Parameters**: None
- **Returns**: All active alerts

### alert_query_by_location
- **Parameters**: `location_id` (string, required)
- **Returns**: Active alerts for location

### alert_get_details
- **Parameters**: `alert_id` (string, required)
- **Returns**: Full alert details

### alert_subscribe
- **Parameters**: `location_id` (string, required)
- **Returns**: Subscription confirmation (simulated)

## Data Source

All data loaded from JSON files via DataStore.
