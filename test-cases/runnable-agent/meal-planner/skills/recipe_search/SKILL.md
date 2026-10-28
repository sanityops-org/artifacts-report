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
  - Cuisines: italian, japanese, mexican, indian, asian, mediterranean, american, thai
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
