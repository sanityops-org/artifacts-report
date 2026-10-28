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
