---
name: recommendations
description: Recommendations skill
---

# Recommendations Skill

## Overview

Recommendations skill suggests movies and TV shows based on genre and viewing mood.

## When to Use

Use this skill when the user wants to:
- Get suggestions without naming a specific title
- Find something matching a mood ("I want something relaxing")
- Browse the highest-rated titles in a genre

## Available Operations

### get_recommendations
- **Parameters**: `genre` (optional), `mood` (optional: happy/sad/excited/relaxed/thrilled/thoughtful), `limit` (optional)
- **Returns**: Titles ranked by rating, filtered by genre and/or mood

With no filters this returns the highest-rated titles across the whole catalog.

## Data Source

All data loaded from `data/titles.json` via `DataStore`. Recommendations are suggestions
based on simulated data, not real-time trends.
