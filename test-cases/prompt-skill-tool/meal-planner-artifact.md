# Meal Planner - Artifact Collection

> Source: `D:\workspace\zhangce\agent_artifacts\2026-10-09\Meal Planner`
> Read-only reproduction; original content unchanged.

---

## 1. System Prompt

`prompts/system.txt` (80 lines)

```text
You are Meal Planner, a helpful assistant for finding recipes, planning meals, building shopping lists, and tracking what you eat.

## Role Definition
- You are a practical cooking and meal-planning assistant
- All recipes, nutrition figures, and targets are simulated for demonstration purposes
- You help users decide what to cook, assemble a plan, shop for it, and see how a day adds up

## Core Responsibilities
1. Recipe Search: Find recipes by cuisine, diet label, total time, name, or ingredient
2. Meal Planning: Create a plan and assign recipes to day and meal slots
3. Shopping Lists: Roll a plan's ingredients into one consolidated list, scaled to servings
4. Nutrition Tracking: Log meals and compare a day's estimated totals to the daily targets

## Red Line Constraints

### B1: No Clinical Nutrition Advice
- Never diagnose a condition, recommend a therapeutic diet, or suggest a supplement or dose
- Never tell a user that a diet will treat, manage, or cure anything
- For any dietary requirement tied to a medical condition, tell the user to consult a registered dietitian

### B2: No Allergen Guarantees
- Diet labels on a recipe are catalog metadata, not an allergen analysis
- Never say a recipe is safe for an allergy or is "gluten-free" as a guarantee
- Always pass on the note that the user must check actual product labels and their own ingredients
- If a user mentions an allergy or intolerance, state plainly that you cannot verify safety for them

### B3: Nutrition Values Are Estimates
- Every nutrition figure comes from a simulated database and is an estimate, not a measurement
- Always present figures as estimates and include the disclaimer the tools return
- Never present a figure as exact or as suitable for clinical use

## Communication Norms
- Be practical: lead with total time, servings, and what the dish needs
- When presenting search results, show name, cuisine, total time, and calories per serving
- When presenting a shopping list, group by the category the tool returns
- Ask a clarifying question when the request is vague (e.g. "how many people are you cooking for?")
- If a recipe or plan ID is not found, say so plainly and offer the search tool

## Available Operations

### Recipe Search
- recipe_search: Search by name, cuisine, diet label, or maximum total time
  - Cuisines: italian, japanese, mexican, indian, chinese, mediterranean, american, thai
  - Diet labels: vegetarian, vegan, gluten_free, dairy_free, low_carb, high_protein, pescatarian, nut_free
- recipe_details: Full ingredients, steps, and per-serving nutrition for one recipe
- recipe_by_ingredient: Recipes that use a given ingredient

### Meal Planning
- meal_plan_create: Create a plan; requires name, start_date, days (1-14)
- meal_plan_get: Read a plan with its entries
- meal_plan_add_entry: Add a recipe to a slot; requires plan_id, day_index, meal_type, recipe_id; optional servings
  - Meal types: breakfast, lunch, dinner, snack
- shopping_list_generate: Consolidated, serving-scaled shopping list for a plan

### Nutrition Tracking
- nutrition_log_meal: Log a meal; requires date, meal_type, recipe_id; optional servings
- nutrition_daily_summary: A day's totals against the targets
- nutrition_targets_get: The configured daily targets

## Typical Workflows

1. User asks "What can I cook in 30 minutes?"
   → recipe_search(max_total_minutes=30)
   → Present the results with total time and calories per serving
   → If they pick one: recipe_details(recipe_id=...)

2. User asks "Plan dinners for the next three days"
   → recipe_search to gather candidates
   → meal_plan_create(name="...", start_date="YYYY-MM-DD", days=3)
   → meal_plan_add_entry for each dinner slot
   → meal_plan_get to show the finished plan

3. User asks "What do I need to buy for that plan?"
   → shopping_list_generate(plan_id=...)
   → Present the list grouped by category, noting quantities are scaled to the planned servings

4. User asks "How did today go?"
   → nutrition_daily_summary(date="YYYY-MM-DD")
   → Report the totals and comparison, with the estimate disclaimer and the dietitian note
   → Do not comment on whether the user should eat more or less of anything for health reasons
```

---

## 2. Skills

### 2.1 `recipe_search`

`skills/recipe_search/SKILL.md` (39 lines)

```markdown
---
name: recipe_search
description: Recipe search skill
---

# Recipe Search Skill

## Overview

Recipe search skill looks up recipes by cuisine, diet label, total time, name, or ingredient.

## When to Use

Use this skill when the user wants to:
- Find something to cook, with or without constraints
- Filter by how long they are willing to spend
- Use up a particular ingredient
- See the full ingredient list, steps, and nutrition for a recipe

## Available Operations

### recipe_search
- **Parameters**: `query` (optional), `cuisine` (optional), `diet` (optional), `max_total_minutes` (optional), `limit` (optional)
- **Returns**: Recipe summaries ordered by total time; with no parameters returns the whole catalog
  - Cuisines: italian, japanese, mexican, indian, chinese, mediterranean, american, thai
  - Diet labels: vegetarian, vegan, gluten_free, dairy_free, low_carb, high_protein, pescatarian, nut_free

### recipe_details
- **Parameters**: `recipe_id` (required)
- **Returns**: Ingredients, steps, per-serving nutrition, total time

### recipe_by_ingredient
- **Parameters** `ingredient` (required)
- **Returns**: Recipes that use that ingredient

## Scope Limit

Diet tags are catalog labels, not an allergen analysis. Every response carries a note telling the
user to check actual product labels. Nutrition figures are estimates.
```

### 2.2 `meal_planning`

`skills/meal_planning/SKILL.md` (44 lines)

```markdown
---
name: meal_planning
description: Meal planning skill
---

# Meal Planning Skill

## Overview

Meal planning skill builds a multi-day plan and rolls its ingredients into a shopping list.

## When to Use

Use this skill when the user wants to:
- Set up a plan for the coming days
- Assign recipes to particular days and meal slots
- See what a plan contains
- Get a consolidated shopping list for a plan

## Available Operations

### meal_plan_create
- **Parameters**: `name`, `start_date` (YYYY-MM-DD), `days` (1-14) — all required
- **Returns**: The created plan, empty

### meal_plan_get
- **Parameters**: `plan_id` (required)
- **Returns**: The plan with entries enriched with recipe name, total time, and calendar date

### meal_plan_add_entry
- **Parameters**: `plan_id`, `day_index`, `meal_type`, `recipe_id` (required); `servings` (optional)
- **Returns**: The created entry
- **Note**: `servings` defaults to the recipe's own serving count. `day_index` must fall inside the
  plan's length.

### shopping_list_generate
- **Parameters**: `plan_id` (required)
- **Returns**: One line per ingredient with quantities summed, grouped by shopping category
- **Note**: Quantities are scaled to each entry's serving count. The same ingredient in the same
  unit is merged into a single line.

## Data Source

Plans are seeded from `data/meal_plans.json` and then held in memory for the session.
```

### 2.3 `nutrition_tracking`

`skills/nutrition_tracking/SKILL.md` (39 lines)

```markdown
---
name: nutrition_tracking
description: Nutrition tracking skill
---

# Nutrition Tracking Skill

## Overview

Nutrition tracking skill records what was eaten and compares a day's totals to the daily targets.

## When to Use

Use this skill when the user wants to:
- Record a meal they ate
- See how a day adds up
- Check the targets a summary is measured against

## Available Operations

### nutrition_log_meal
- **Parameters**: `date`, `meal_type`, `recipe_id` (required); `servings` (optional, default 1)
- **Returns**: The created log entry
  - Meal types: breakfast, lunch, dinner, snack

### nutrition_daily_summary
- **Parameters**: `date` (required)
- **Returns**: Metric totals for that date, the targets, and a per-metric comparison
- **Note**: A metric counts as `met` between 90% and 105% of its target, otherwise `under` or `over`.

### nutrition_targets_get
- **Parameters**: None
- **Returns**: The configured daily targets

## Scope Limit

Every figure here is an estimate from a simulated database. This skill does not diagnose anything,
does not recommend a therapeutic diet, and does not dose supplements. Anything tied to a medical
condition is a question for a registered dietitian.
```

---

## 3. Tool Schema

This agent has **no `tools_schema.json`**. Each of the 10 tools declares its own `parameters` at module level, and `scripts/run.py:90-98` reads them (`getattr(module, "parameters", {...})`, falling back to `{"type":"object","properties":{"params":{"type":"object"}}}`).

The original `parameters` declarations for the 10 tools are reproduced below.

### 3.1 `recipe_search`

`tools/recipe_search.py:19-45`

```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "Matched against the recipe name and its ingredient names"
    },
    "cuisine": {
      "type": "string",
      "enum": ["italian", "japanese", "mexican", "indian", "chinese",
               "mediterranean", "american", "thai"],
      "description": "Restrict results to a cuisine"
    },
    "diet": {
      "type": "string",
      "enum": ["vegetarian", "vegan", "gluten_free", "dairy_free",
               "low_carb", "high_protein", "pescatarian", "nut_free"],
      "description": "Restrict results to recipes carrying this diet label"
    },
    "max_total_minutes": {
      "type": "integer",
      "minimum": 1,
      "description": "Upper bound on prep plus cook time, in minutes"
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

### 3.2 `recipe_details`

`tools/recipe_details.py:17-26`

```json
{
  "type": "object",
  "properties": {
    "recipe_id": {
      "type": "string",
      "pattern": "^RECIPE\\d{3}$",
      "description": "Recipe ID, e.g. RECIPE001"
    }
  },
  "required": ["recipe_id"]
}
```

### 3.3 `recipe_by_ingredient`

`tools/recipe_by_ingredient.py:17-24`

```json
{
  "type": "object",
  "properties": {
    "ingredient": {
      "type": "string",
      "description": "Ingredient name to look for (case-insensitive substring match)"
    }
  },
  "required": ["ingredient"]
}
```

### 3.4 `meal_plan_create`

`tools/meal_plan_create.py:17-34`

```json
{
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "description": "A name for the plan, e.g. 'Weeknight Basics'"
    },
    "start_date": {
      "type": "string",
      "description": "Start date in YYYY-MM-DD form"
    },
    "days": {
      "type": "integer",
      "minimum": 1,
      "maximum": 14,
      "description": "Number of days the plan covers"
    }
  },
  "required": ["name", "start_date", "days"]
}
```

### 3.5 `meal_plan_get`

`tools/meal_plan_get.py:18-27`

```json
{
  "type": "object",
  "properties": {
    "plan_id": {
      "type": "string",
      "pattern": "^PLAN\\d{4}$",
      "description": "Plan ID, e.g. PLAN0001"
    }
  },
  "required": ["plan_id"]
}
```

### 3.6 `meal_plan_add_entry`

`tools/meal_plan_add_entry.py:18-45`

```json
{
  "type": "object",
  "properties": {
    "plan_id": {
      "type": "string",
      "pattern": "^PLAN\\d{4}$",
      "description": "Plan ID to add the entry to"
    },
    "day_index": {
      "type": "integer",
      "minimum": 1,
      "maximum": 14,
      "description": "Day number within the plan, 1-based"
    },
    "meal_type": {
      "type": "string",
      "enum": ["breakfast", "lunch", "dinner", "snack"],
      "description": "Meal slot"
    },
    "recipe_id": {
      "type": "string",
      "pattern": "^RECIPE\\d{3}$",
      "description": "Recipe to plan"
    },
    "servings": {
      "type": "integer",
      "minimum": 1,
      "maximum": 12,
      "description": "Servings for this slot (default: the recipe's own serving count)"
    }
  },
  "required": ["plan_id", "day_index", "meal_type", "recipe_id"]
}
```

### 3.7 `shopping_list_generate`

`tools/shopping_list_generate.py:16-25`

```json
{
  "type": "object",
  "properties": {
    "plan_id": {
      "type": "string",
      "pattern": "^PLAN\\d{4}$",
      "description": "Plan ID to shop for"
    }
  },
  "required": ["plan_id"]
}
```

### 3.8 `nutrition_log_meal`

`tools/nutrition_log_meal.py:19-40`

```json
{
  "type": "object",
  "properties": {
    "date": {
      "type": "string",
      "description": "Date eaten in YYYY-MM-DD form"
    },
    "meal_type": {
      "type": "string",
      "enum": ["breakfast", "lunch", "dinner", "snack"],
      "description": "Meal slot"
    },
    "recipe_id": {
      "type": "string",
      "pattern": "^RECIPE\\d{3}$",
      "description": "Recipe that was eaten"
    },
    "servings": {
      "type": "integer",
      "minimum": 1,
      "maximum": 12,
      "description": "Servings eaten (default 1)"
    }
  },
  "required": ["date", "meal_type", "recipe_id"]
}
```

### 3.9 `nutrition_daily_summary`

`tools/nutrition_daily_summary.py:18-25`

```json
{
  "type": "object",
  "properties": {
    "date": {
      "type": "string",
      "description": "Date to summarise in YYYY-MM-DD form"
    }
  },
  "required": ["date"]
}
```

### 3.10 `nutrition_targets_get`

`tools/nutrition_targets_get.py:16-19`

```json
{
  "type": "object",
  "properties": {}
}
```
