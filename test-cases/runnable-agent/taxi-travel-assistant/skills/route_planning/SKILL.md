---
name: route_planning
description: "Route Planning Skills - Check the Best Travel Route"
version: "1.0.0"
---

# Route Planning Skill

Check the best travel route, including distance, estimated time and toe information.

## Trigger conditions

**Activation conditions:**
- Users request to plan routes and query route information
- The user provides the starting point and the end point.

**Conditions for non-activation:**
- User requests information unrelated to the route

## Boundary constraint

- A single request only processes one route.
- The output limit is 500 characters.
- Only read operation is supported.

## Tool

### plan_route
Check the route information.

Parameter:
- `origin` (required): Starting point ID
- `destination` (required): End point ID

## Examples of use

```python
from skills.route_planning.handler import run

result = run({
    "origin": "L-001",
    "destination": "L-002"
})

print(result["data"]["route"]["distance_km"])   # 35.2
print(result["data"]["route"]["duration_min"])  # 45
```
