---
name: vehicle_query
description: "Vehicle Inquiry Skills - Check Available Taxis Nearby"
version: "1.0.0"
---

# Vehicle Query Skill

Check the available taxis nearby, including the model, driver information and estimated arrival time.

## Function

- Search for nearby available vehicles by location
- Support filtering by car model
- Return vehicle distance and estimated arrival time

## Tool

### query_vehicle
Check the available vehicles nearby.

Parameter:
- `location` (required): Place ID
- `category` (optional): Model category filtering
- `radius_km` (optional): Search radius (km), default 5 km

## Examples of use

```python
from skills.vehicle_query.handler import run

result = run({
    "location": "L-001",
    "category": "comfort"
})

for v in result["data"]["vehicles"]:
    print(f"{v['model']} - {v['eta_min']} Arrive in minutes")
```
