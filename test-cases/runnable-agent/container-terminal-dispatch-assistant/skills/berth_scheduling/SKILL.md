---
name: berth_scheduling
description: Parking scheduling skills
---

# Parking scheduling skills (Berth Scheduling Skill)

## Brief account

The berth dispatching skill provides the ability to query the relevant information of ships and berths, and helps dispatchers understand the current operation status of the port.

## When to use

When you need to know the following information, you should use this skill:

- Check the ship's arrival plan and status
- Check the occupancy and availability of the berth
- Inquire about the anchorage waiting for the ship

## Available operation

### Query tools

1. **query_vessel_plan** - Inquire about the ship plan
   - Parameter: `vessel_id` (optional) - Specify the ship ID to query a single ship
   - Return: Detailed information of all ships or a single ship

2. **query_berth_status** - Check the berth status
   - Parameters:
     - `status` (Optional) - Filter by status (available, occupied, reserved, maintenance)
     - `berth_id` (Optional) - Specify the berth ID to query a single berth
   - Back: List of eligible parking statuses

3. **query_anchorage** - Query anchorage ships
   - Parameters: None
   - Back: List of ships currently waiting at the anchorage (status=at_anchor)

## Permission requirements

- Query operation requires read-only permission.
- The system will verify whether the user has the right to access the relevant data.

## Data source

All data is loaded from the JSON data file through DataStore.
