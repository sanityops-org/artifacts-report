# Taxi Travel Assistant - Logical Artifact Collection

**Collection date**: 2025-01-09
**Agent ID**: taxi_assistant
**Version**: 1.0.0

---

## 1. System Prompt (verbatim in full)

```text
You are the Taxi Travel Assistant, dedicated to providing passengers with convenient travel services.

## Role
You are the passenger's travel advisor and help users with route planning, fare estimation, vehicle search, and taxi booking.

## Capability Boundaries
- You can query routes, estimate fares, find nearby vehicles, book a taxi, and cancel an order.
- You cannot handle payments, complaints, or account issues. Direct users to customer service for these matters.

## Interaction Style
- Be concise and friendly, and proactively provide useful information.
- When the user provides only an origin or destination, ask for the missing information.
- When estimating a fare, proactively show multiple vehicle categories for comparison.

## Safety Guidance
- Do not proactively request private user information, such as payment passwords.
- Confirm the origin and destination before booking.
```

---

## 2. Skill Definitions (verbatim in full)

### fare_estimation skill.yaml

```yaml
name: fare_estimation
version: "1.0.0"
description: "Estimate taxi fares and return fare details for multiple vehicle categories."

handler:
  script: handler.py
  entry_point: main
```

### order_booking skill.yaml

```yaml
name: order_booking
version: "1.0.0"
description: "Taxi order management skill."

handler:
  script: handler.py
  entry_point: main
```

### route_planning skill.yaml

```yaml
name: route_planning
version: "1.0.0"
description: "Route planning skill."

handler:
  script: handler.py
  entry_point: main
```

### vehicle_query skill.yaml

```yaml
name: vehicle_query
version: "1.0.0"
description: "Vehicle search skill."

handler:
  script: handler.py
  entry_point: main
```

---

## 3. Tool Schemas (verbatim in full)

```yaml
# Tool registration configuration
tools:
  # Route planning
  - name: plan_route
    description: "Find the optimal travel route and return distance, duration, and tolls."
    script: skills/route_planning/tools/plan_route.py
    entry_point: execute
    inputSchema:
      type: object
      properties:
        origin:
          type: string
          description: "Origin location ID, such as L-001 (Beijing West Railway Station)."
          minLength: 1
          maxLength: 20
        destination:
          type: string
          description: "Destination location ID, such as L-002 (Beijing Capital Airport Terminal 3)."
          minLength: 1
          maxLength: 20
      required: [origin, destination]
      additionalProperties: false

  # Fare estimation
  - name: estimate_fare
    description: "Estimate taxi fares and return fare details for multiple vehicle categories."
    script: skills/fare_estimation/tools/estimate_fare.py
    entry_point: execute
    inputSchema:
      type: object
      properties:
        origin:
          type: string
          description: "Origin location ID."
          minLength: 1
          maxLength: 20
        destination:
          type: string
          description: "Destination location ID."
          minLength: 1
          maxLength: 20
        category:
          type: string
          description: "Vehicle category (economic | comfort | premium | suv). If omitted, return all categories."
          enum: [economic, comfort, premium, suv]
        time_of_day:
          type: string
          description: "Time period (day | night). Defaults to day."
          enum: [day, night]
          default: day
      required: [origin, destination]
      additionalProperties: false

  # Vehicle search
  - name: query_vehicle
    description: "Find nearby available taxis and return the vehicle list and estimated arrival times."
    script: skills/vehicle_query/tools/query_vehicle.py
    entry_point: execute
    inputSchema:
      type: object
      properties:
        location:
          type: string
          description: "Location ID."
          minLength: 1
          maxLength: 20
        category:
          type: string
          description: "Vehicle category filter (economic | comfort | premium | suv)."
          enum: [economic, comfort, premium, suv]
        radius_km:
          type: number
          description: "Search radius in kilometers."
          minimum: 0.5
          maximum: 50
          default: 5.0
      required: [location]
      additionalProperties: false

  # Booking
  - name: place_order
    description: "Create a taxi order and automatically match a nearby vehicle."
    script: skills/order_booking/tools/place_order.py
    entry_point: execute
    inputSchema:
      type: object
      properties:
        user_id:
          type: string
          description: "User ID."
          minLength: 1
          maxLength: 50
        origin:
          type: string
          description: "Origin location ID."
          minLength: 1
          maxLength: 20
        destination:
          type: string
          description: "Destination location ID."
          minLength: 1
          maxLength: 20
        phone:
          type: string
          description: "Contact phone number."
          minLength: 1
          maxLength: 20
        category:
          type: string
          description: "Preferred vehicle category (economic | comfort | premium | suv)."
          enum: [economic, comfort, premium, suv]
      required: [user_id, origin, destination, phone]
      additionalProperties: false

  # Cancel order
  - name: cancel_order
    description: "Cancel a taxi order."
    script: skills/order_booking/tools/cancel_order.py
    entry_point: execute
    inputSchema:
      type: object
      properties:
        order_id:
          type: string
          description: "Order number."
          minLength: 1
          maxLength: 20
        reason:
          type: string
          description: "Cancellation reason (optional)."
          maxLength: 200
      required: [order_id]
      additionalProperties: false
```

---

## Logical Artifact Inventory

| Type | File path |
|------|-----------|
| System Prompt | prompts/system.txt |
| Skill Definition | skills/fare_estimation/skill.yaml |
| Skill Definition | skills/order_booking/skill.yaml |
| Skill Definition | skills/route_planning/skill.yaml |
| Skill Definition | skills/vehicle_query/skill.yaml |
| Tool Schema | config/tools.yaml |
