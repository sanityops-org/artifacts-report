# Meal Planner Agent

An intelligent assistant for finding recipes, planning meals, generating shopping lists, and
tracking what you eat.

## Industry
Consumer / Food & Nutrition

## Description
Meal Planner searches a simulated recipe catalog, assembles a day-by-day meal plan, rolls the plan's
ingredients up into a single shopping list, and totals logged meals against daily nutrition targets.
It reports nutrition figures as estimates, never claims a recipe is allergen-free, and refers any
clinical question to a registered dietitian.

## Skills
- recipe_search: Find recipes by name, cuisine, diet tag, time, or ingredient; view full details
- meal_planning: Create a plan, add recipes to day/meal slots, and generate a shopping list
- nutrition_tracking: Log meals and compare a day's totals against nutrition targets

## Creation Date
2026-10-09

## Version
v1.0.0

## Author
Agent Artifacts Team

## How to Run

**Prerequisites**: Ensure `sanityops_agent` framework is installed

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your LLM API key

# Verify setup
python scripts/setup.py

# Start Agent
python scripts/run.py
```

## Project Structure

```
Meal Planner/
├── prompts/          # System prompt
├── models/           # Pydantic domain models
├── apis/             # Recipe, plan and nutrition engines + data store
├── data/             # Simulated JSON data (12 recipes, targets, one seeded plan)
├── skills/           # Skill definitions (3 skills)
├── tools/            # Executable tool scripts (10 tools, auto-scanned)
├── tests/            # Integration and contract tests
└── scripts/          # Startup and setup scripts
```

## Data Models

- **Ingredient**: Name, quantity, unit, and shopping category
- **NutritionInfo**: Calories, protein, carbs, fat, fibre, and sodium per serving
- **Recipe**: Cuisine, diet tags, prep/cook time, servings, ingredients, steps, per-serving nutrition
- **MealPlan** / **PlanEntry**: A multi-day plan with recipes assigned to day and meal slots
- **NutritionLogEntry**: A meal eaten on a date, with a serving count
- **NutritionTargets**: The daily targets a summary is compared against

## Core Design Points

1. **No clinical nutrition advice**: tools carry no condition, treatment, or supplement dosing (B1)
2. **No allergen guarantees**: diet tags are catalog labels, and every recipe response carries a
   note telling the user to verify actual product labels (B2)
3. **Nutrition is estimated**: every nutrition response is flagged as an estimate (B3)
4. **User data stays in memory**: meal plans and nutrition logs are not written to disk (B4)
5. **Ingredient scaling is real**: a plan entry contributes ingredients and calories in proportion
   to its serving count, not the recipe's default
6. **Self-contained system prompt** and platform-compatible tool schemas

## Tests

```bash
pip install pytest
python -m pytest
```

## Red Line Constraints

- **B1**: No clinical or medical nutrition advice — refer to a registered dietitian
- **B2**: Never claim a recipe is allergen-free — verify product labels
- **B3**: Nutrition figures are estimates from a simulated database, not measured values

## Run From This Repository

From the repository root:

```bash
cd test-cases/runnable-agent/meal-planner
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
# Edit .env and add the required model endpoint and credentials.
python scripts/setup.py
python scripts/run.py
```
