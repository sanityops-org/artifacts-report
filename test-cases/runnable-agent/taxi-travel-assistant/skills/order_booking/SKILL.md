---
name: order_booking
description: "Taxi Ordering Skills - Create Orders and Dispatch Cars"
version: "1.0.0"
---

# Order Booking Skill

Create a taxi order and send a car automatically, and support order cancellation.

## Function

- Create an order: Match the vehicle according to the starting point and car model to generate an order
- Cancel the order: cancel the unstarted order

## Tool

### place_order
Create an order.

Parameter:
- `user_id` (required): Consumer ID
- `origin` (required): Starting point ID
- `destination` (required): End point ID
- `phone` (required): Contact number
- `category` (optional): Model preference

### cancel_order
Cancel the order.

Parameter:
- `order_id` (required): Order number

## Examples of use

```python
from skills.order_booking.handler import run

# Place an order
result = run({
    "action": "place_order",
    "params": {
        "user_id": "U-123",
        "origin": "L-001",
        "destination": "L-002",
        "phone": "138****1234",
        "category": "comfort"
    }
})

print(result["data"]["order_id"])
print(result["data"]["vehicle"]["driver_name"])

# Cancel
cancel_result = run({
    "action": "cancel_order",
    "params": {"order_id": result["data"]["order_id"]}
})
```
