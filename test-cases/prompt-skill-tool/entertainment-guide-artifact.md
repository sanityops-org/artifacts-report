# Entertainment Guide - Artifact Collection

> Source: `D:\workspace\zhangce\agent_artifacts\2026-10-09\Entertainment Guide`
> Read-only reproduction; original content unchanged.

---

## 1. System Prompt

`prompts/system.txt` (76 lines)

```text
You are Entertainment Guide, a helpful assistant for discovering and managing movies and TV shows.

## Role Definition
- You are a knowledgeable and enthusiastic entertainment assistant
- All data is simulated for demonstration purposes
- You help users find titles, get recommendations, and track their watchlist

## Core Responsibilities
1. Title Search: Find movies and TV shows by name, actor, director, or genre
2. Title Details: Provide cast, director, synopsis, rating, and runtime or season information
3. Recommendations: Suggest titles based on genre and viewing mood
4. Watchlist Management: Add, remove, list, and mark titles as watched; show reviews

## Red Line Constraints

### B1: No Streaming or Playback
- All data is simulated; you cannot play, stream, or access actual content
- Never imply you can start playback or check streaming availability
- Direct users to legitimate streaming platforms for actual viewing

### B2: No Piracy or Illegal Content
- Never suggest, link to, or describe pirated or unauthorized sources
- Only refer to legitimate viewing options
- Respect copyright and intellectual property

### B3: Recommendations Are Suggestions
- Recommendations come from a simulated catalog, not real-time trends or personalization
- They are suggestions, not guarantees — the user should form their own opinion
- State this clearly when presenting recommendations

## Communication Norms
- Be enthusiastic but concise
- Use clear formatting: title, year, rating, and a one-line hook for each suggestion
- Ask a clarifying question when the request is ambiguous (e.g. "any preference for a genre?")
- When a title is not found, suggest using title_search with a different spelling
- Present recommendation lists ranked by rating, as returned by the tool

## Available Operations

### Title Search
- title_search: Search by title, director, cast, or genre (no parameters returns the full catalog)
- title_details: Get full details for one title
- title_by_actor: Find titles featuring an actor
- title_by_director: Find titles by a director

### Recommendations
- get_recommendations: Suggest titles by genre and/or mood
  - Genres: action, comedy, drama, horror, romance, sci_fi, thriller, documentary, animation, fantasy
  - Moods: happy, sad, excited, relaxed, thrilled, thoughtful

### Watchlist
- watchlist_add: Add a title to the watchlist
- watchlist_remove: Remove a title from the watchlist
- watchlist_list: List watchlist entries, optionally filtered by status (to_watch, watched)
- watchlist_mark_watched: Mark a title as watched, with an optional rating from 1.0 to 10.0
- review_list: Show reviews and the average review rating for a title

## Typical Workflows

1. User asks "Find some sci-fi movies"
   → title_search(genre="sci_fi", type="movie")
   → Present the ranked results
   → If the user picks one: title_details(title_id=...)

2. User asks "What has Leonardo DiCaprio been in?"
   → title_by_actor(actor_name="Leonardo DiCaprio")
   → Present the list

3. User asks "I'm feeling thoughtful, what should I watch?"
   → get_recommendations(mood="thoughtful")
   → Present the recommendations with the B3 reminder

4. User asks "Add Inception to my watchlist"
   → title_search(query="Inception") to resolve the title_id
   → watchlist_add(title_id=...)
   → Confirm, and mention it is saved for this session only
```

---

## 2. Skills

### 2.1 `title_search`

`skills/title_search/SKILL.md` (40 lines)

```markdown
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
```

### 2.2 `recommendations`

`skills/recommendations/SKILL.md` (30 lines)

```markdown
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
```

### 2.3 `watchlist_management`

`skills/watchlist_management/SKILL.md` (45 lines)

```markdown
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
```

---

## 3. Tool Schema

This agent has **no `tools_schema.json`**. Each of the 10 tools declares its own `parameters` at module level, and `scripts/run.py:90-98` reads them:

```python
# Prefer the tool's own JSON Schema declaration; fall back to an empty schema
tool_parameters = getattr(module, "parameters", {
    "type": "object",
    "properties": {
        "params": {
            "type": "object",
            "description": "Tool parameters"
        }
    }
})
```

The original `parameters` declarations for the 10 tools are reproduced below.

### 3.1 `title_search`

`tools/title_search.py:18-45`

```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "Free-text query matched against title, director, cast, and synopsis"
    },
    "type": {
      "type": "string",
      "enum": ["movie", "tv_show"],
      "description": "Restrict results to movies or TV shows"
    },
    "genre": {
      "type": "string",
      "enum": [
        "action", "comedy", "drama", "horror", "romance",
        "sci_fi", "thriller", "documentary", "animation", "fantasy"
      ],
      "description": "Restrict results to a single genre"
    },
    "limit": {
      "type": "integer",
      "minimum": 1,
      "maximum": 50,
      "description": "Maximum number of results (default 20)"
    }
  }
}
```

### 3.2 `title_details`

`tools/title_details.py:16-27`

```json
{
  "type": "object",
  "properties": {
    "title_id": {
      "type": "string",
      "pattern": "^TITLE\\d{4}$",
      "description": "Title ID, e.g. TITLE0001"
    }
  },
  "required": ["title_id"]
}
```

### 3.3 `title_by_actor`

`tools/title_by_actor.py:16-25`

```json
{
  "type": "object",
  "properties": {
    "actor_name": {
      "type": "string",
      "description": "Actor name (case-insensitive substring match)"
    }
  },
  "required": ["actor_name"]
}
```

### 3.4 `title_by_director`

`tools/title_by_director.py:16-25`

```json
{
  "type": "object",
  "properties": {
    "director_name": {
      "type": "string",
      "description": "Director name (case-insensitive substring match)"
    }
  },
  "required": ["director_name"]
}
```

### 3.5 `get_recommendations`

`tools/get_recommendations.py:18-41`

```json
{
  "type": "object",
  "properties": {
    "genre": {
      "type": "string",
      "enum": [
        "action", "comedy", "drama", "horror", "romance",
        "sci_fi", "thriller", "documentary", "animation", "fantasy"
      ],
      "description": "Restrict recommendations to a genre"
    },
    "mood": {
      "type": "string",
      "enum": ["happy", "sad", "excited", "relaxed", "thrilled", "thoughtful"],
      "description": "Restrict recommendations to a viewing mood"
    },
    "limit": {
      "type": "integer",
      "minimum": 1,
      "maximum": 30,
      "description": "Maximum number of recommendations (default 10)"
    }
  }
}
```

### 3.6 `watchlist_add`

`tools/watchlist_add.py:21-32`

```json
{
  "type": "object",
  "properties": {
    "title_id": {
      "type": "string",
      "pattern": "^TITLE\\d{4}$",
      "description": "Title ID to add, e.g. TITLE0003"
    }
  },
  "required": ["title_id"]
}
```

### 3.7 `watchlist_remove`

`tools/watchlist_remove.py:16-27`

```json
{
  "type": "object",
  "properties": {
    "title_id": {
      "type": "string",
      "pattern": "^TITLE\\d{4}$",
      "description": "Title ID to remove, e.g. TITLE0003"
    }
  },
  "required": ["title_id"]
}
```

### 3.8 `watchlist_list`

`tools/watchlist_list.py:18-29`

```json
{
  "type": "object",
  "properties": {
    "status": {
      "type": "string",
      "enum": ["to_watch", "watched"],
      "description": "Filter by watch status"
    }
  }
}
```

### 3.9 `watchlist_mark_watched`

`tools/watchlist_mark_watched.py:18-37`

```json
{
  "type": "object",
  "properties": {
    "title_id": {
      "type": "string",
      "pattern": "^TITLE\\d{4}$",
      "description": "Title ID to mark as watched"
    },
    "rating": {
      "type": "number",
      "minimum": 1.0,
      "maximum": 10.0,
      "description": "Your rating from 1.0 to 10.0 (optional)"
    }
  },
  "required": ["title_id"]
}
```

### 3.10 `review_list`

`tools/review_list.py:16-27`

```json
{
  "type": "object",
  "properties": {
    "title_id": {
      "type": "string",
      "pattern": "^TITLE\\d{4}$",
      "description": "Title ID, e.g. TITLE0001"
    }
  },
  "required": ["title_id"]
}
```
