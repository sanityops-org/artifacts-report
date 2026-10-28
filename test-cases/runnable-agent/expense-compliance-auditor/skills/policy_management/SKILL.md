---
name: policy_management
description: Show the effective expense policy rules and apply user-specified overrides to thresholds. Use when the user asks "what is the meal limit", "show me the expense policy", "change the hotel cap to 200", "our receipt threshold is 50", or wants to know which rules apply before running an audit.
---

# Policy Management Skill

## When to Use

- User asks what a specific limit or threshold is
- User wants to see the full set of rules that will be applied
- User states a company-specific threshold that differs from the default
- User wants to confirm which policy was used for a previous audit

## Workflow

1. Call `get_policy` with no arguments to show the defaults, or with the user's stated
   overrides to show the merged result.
2. Present the effective rules as a table: rule ID, plain-English description, and the
   active value.
3. When an override is applied, state clearly which rule changed, the old value, and the
   new value.

## Important: Overrides Are Session-Scoped

Overrides supplied to `get_policy` apply to the calls you make in this conversation.
They are not persisted to disk. Tell the user this when they set one — the agent has no
policy file and does not remember overrides between sessions.

## Output Format

```
Effective Expense Policy — version 2026.1 (USD)

| Rule                    | Description                                   | Active Value |
|-------------------------|-----------------------------------------------|--------------|
| meal_limit_per_person   | Meals must not exceed $75 per person          | $75.00       |
| hotel_limit_per_night   | Lodging must not exceed $250 per night        | $200.00 *    |
| receipt_required_above  | Receipts required for expenses of $25 or more | $25.00       |
| prohibited_category     | Never reimbursable                            | alcohol, gambling, personal_items, fines |
| submission_window       | Submit within 60 days of the expense date     | 60 days      |
| approval_required_above | Expenses of $500 or more need an approval ID  | $500.00      |
| weekend_non_travel_meal | Weekend non-travel meals need review          | flagged      |

* Overridden in this session (default: $250.00)
```

## Error Handling

- Unknown rule ID in an override: relay the error and list the valid rule IDs
- Non-numeric value for a threshold: ask the user to restate it as a number
- Override that would make a limit zero or negative: point this out and ask for confirmation
  before applying