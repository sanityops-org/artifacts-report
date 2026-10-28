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
