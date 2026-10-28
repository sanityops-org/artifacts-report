---
name: fare_estimation
description: "Cost Estimation Skills - Calculate the Estimated Cost of Multiple Models"
version: "1.0.0"
---

# Fare Estimation Skill

Calculate the estimated taxi fare of a variety of models, including the starting price, mileage fee, duration fee and surcharge.

## Function

- Calculate the cost of four models: economy, comfort, luxury and SUV
- Support night price increase calculation
- Support long-distance price increase calculation

## Tool

### estimate_fare
Estimate the taxi fee.

Parameter:
- `origin` (required): Starting point ID
- `destination` (required): End point ID
- `category` (optional): Model category, return all models if not provided
- `time_of_day` (optional): Time period (day | night), default day

## Examples of use

```python
from skills.fare_estimation.handler import run

result = run({
    "origin": "L-001",
    "destination": "L-002"
})

print(result["data"]["fares"]["economic"]["total"])  # 139.69
print(result["data"]["fares"]["comfort"]["total"])   # 168.84
```
