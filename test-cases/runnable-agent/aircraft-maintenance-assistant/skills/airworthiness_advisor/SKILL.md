---
name: airworthiness_advisor
description: "Airworthiness decision-making skills - professional aircraft maintenance decision-making support"
version: "1.0.0"
---

# Airworthiness Advisor Skill

Professional aircraft maintenance airworthiness decision-making skills, supporting AD airworthiness status inquiry, parts life tracking, history inquiry, and generating maintenance decision-making plans.

## Trigger conditions

**Activation conditions (must be met at the same time):**
1. Users clearly request repair decision-making, airworthiness assessment or parts status inquiry
2. The user provides the aircraft registration number (such as B-1234) or the part number (such as PN-12345）

**Non-activation conditions (if any one is met, it will not be activated):**
- Debugging, code review, system management requests
- General questions and answers about user requests that are not related to maintenance decision-making
- Users request to modify the database or perform actual maintenance operations

## Boundary constraint

### Enter the boundary
- A single request can process up to **50 parts** or **50 AD**
- Aircraft registration number format: `^[A-Z]-[0-9A-Z]+$` (2-10 characters)
- Part number format: `^[A-Z]{2,4}-[0-9A-Z]+$` (3-30 characters)
- Input must be encoded in UTF-8.

### Output boundary
- The output limit is **1,500 characters**
- When the information is insufficient, skip the section and mark it as "insufficient information", do not fabricate data.

### Execution boundary
- Maximum number of retrials: **3 times**
- Timeout limit: **60 seconds**
- Maximum number of tool calls: **10 times/execution**
- Stop immediately after the call fails and report an error, do not try to replace the path.

### Permission boundary
**Allowed operations:**
- Read the aircraft registration number, parts status and AD status
- Read the resume and legacy defect information
- Generate a decision-making recommendation report

**Prohibited operations:**
- Write, update and delete any data
- Carry out actual maintenance operations
- Access the production database or external system
- Call up other skills or management permission tools

### Data source boundary
- Only use the data explicitly provided in the current request
- Use the built-in analog data source（`data/sim_db.py`）
- **Prohibit ** access to session history, external systems or other data sources

### Environmental boundaries
- Only run in a local test/sandbox environment
- **Prohibit ** access to the production environment, production API, real-time system
- **Prohibit ** access to unauthorized external services

## Function

- **Airworthiness assessment**: Query the AD execution status and judge the airworthiness of the aircraft
- **Part life management**: Track the status of life parts/time controls and warn of over-limit risks
- **Impact analysis of defects**: Evaluate the impact of residual defects on airworthiness
- **Maintenance decision-making support**: Comprehensively generate maintenance plans to assess the impact of downtime

## Don't do things (Non-goals)

This skill is clear **not to perform** the following operations:
- Infer the parameters that are not provided (if the registration number is missing, the user should be asked instead of guessing)
- Extract additional information from the session history
- Extend the task boundaries to unrelated areas such as maintenance quotation and spare parts procurement
- Perform any database writing or system changes
- Call other skills with higher permissions

## Failure to deal with

When the tool call fails or the data is missing:
1. **Stop immediately ** and don't try to replace the path.
2. **Report the error**, including the reason for the failure and suggested follow-up
3. **Don't fabricate data**fill in the missing information
4. **Do not lower the standard** or expand the search scope

Partial result strategy:
- When a part of the information is insufficient, the output part is marked as "insufficient information"
- The obtained valid data can still be output.
- Don't enter the infinite retry because of partial omission.

## Tool

### query_airworthiness
Query the airworthiness status of AD to determine the conformity. Only reading operations are supported.

Parameter:
- `reg_no` (required): Aircraft registration number, such as B-1234
- `ad_id` (optional): AD Number

### query_component_status
Query the status of parts, including the remaining hours of the life part/time control - cycle. Only reading operations are supported.

Parameter:
- `reg_no` (required): Aircraft registration number
- `part_no` (required): Part number

### query_maintenance_history
Query aircraft history, residual defects, and historical AD execution records. Only reading operations are supported.

Parameter:
- `reg_no` (required): Aircraft registration number
- `part_no` (optional): Part number

### generate_decision
Comprehensively generate a maintenance plan decision-making list. Only generate suggestion reports and do not perform actual operations.

Parameter:
- `reg_no` (required): Aircraft registration number
- `assessment_data` (required): Evaluation data (including AD status, part status, resume information)

## Examples of use

```python
from skills.airworthiness_advisor.handler import run

result = run({
    "reg_no": "B-1234",
    "part_no": "PN-12345"
})

print(result["data"]["assessment"])        # airworthy / restricted / grounding
print(result["data"]["open_actions"])      # List of repair actions
print(result["data"]["rationale"])         # Basis for decision-making
```

## Output format

Return to the structured decision-making report (limited to 1,500 characters):

| Field | Description |
|------|------|
| `assessment` | Airworthiness conclusion (airworthy/restricted/grounding) |
| `assessment_text` | Conclusion (Released/Restricted Release/Non-Releable)) |
| `open_actions` | Maintenance actions to be performed (sorted by priority, see below for the priority definition) |
| `parts` | Suggested spare parts list |
| `ground_time_impact` | Impact assessment of suspension |
| `deferred_items` | Retainable items (MEL control) |
| `rationale` | Basis for decision-making |

**Definition of priority (from high to low):**
1. Critical（Key): Affects airworthiness and must be dealt with immediately.
2. High（High): It affects safety and needs to be dealt with as soon as possible.
3. Medium（Middle): Affect the operation efficiency, plan to deal with
4. Low（Low): Suggested improvement, optional processing
