---
name: watchlist_management
description: Watchlist management skill
---

# Watchlist Management Skill

## Overview

Watchlist management skill tracks what the user plans to watch and what they have already seen.

## When to Use

Use this skill when the user wants to:
- Save a title for later
- See what is on their watchlist
- Mark something as watched and rate it
- Read reviews for a title

## Available Operations

### watchlist_add
- **Parameters**: `title_id` (required)
- **Returns**: The created watchlist entry; rejects duplicates and unknown titles

### watchlist_remove
- **Parameters**: `title_id` (required)
- **Returns**: Confirmation; rejects titles not on the watchlist

### watchlist_list
- **Parameters**: `status` (optional: to_watch/watched)
- **Returns**: Watchlist entries enriched with title name, type, and year

### watchlist_mark_watched
- **Parameters**: `title_id` (required), `rating` (optional, 1.0-10.0)
- **Returns**: The updated entry

### review_list
- **Parameters**: `title_id` (required)
- **Returns**: Reviews for the title plus the average review rating

## Data Source

Titles and reviews load from JSON via `DataStore`. The watchlist itself is held in memory
for the session only — nothing is written back to disk.
