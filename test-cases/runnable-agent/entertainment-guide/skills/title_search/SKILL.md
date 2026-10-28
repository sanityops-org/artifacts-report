---
name: title_search
description: Title search skill
---

# Title Search Skill

## Overview

Title search skill provides lookup of movies and TV shows by name, director, cast, or genre.

## When to Use

Use this skill when the user wants to:
- Find a movie or TV show by name
- See everything an actor or director has worked on
- Browse titles within a genre
- Get full details for a specific title

## Available Operations

### title_search
- **Parameters**: `query` (optional), `type` (optional: movie/tv_show), `genre` (optional), `limit` (optional)
- **Returns**: Matching titles ranked by rating; with no parameters returns the whole catalog

### title_details
- **Parameters**: `title_id` (required)
- **Returns**: Full details for one title (cast, director, synopsis, rating, runtime or seasons)

### title_by_actor
- **Parameters**: `actor_name` (required)
- **Returns**: Titles featuring that actor

### title_by_director
- **Parameters**: `director_name` (required)
- **Returns**: Titles by that director

## Data Source

All data loaded from `data/titles.json` via `DataStore` — 30 simulated titles.
