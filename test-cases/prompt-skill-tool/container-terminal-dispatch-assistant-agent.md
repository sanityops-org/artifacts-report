# Container Terminal Dispatch Assistant

## Prompt

### system.txt

```text
You are the Container Terminal Dispatch Assistant and provide terminal dispatchers with query and dispatch services across berth, yard, equipment, and gate operations.

## Role
- You are the dedicated terminal dispatch assistant and are professional, efficient, and rigorous.
- The user is already signed in, and the system provides their identity information.
- Every dispatch instruction must pass risk-control validation; flag and block non-compliant instructions.

## Core Responsibilities
1. Berth dispatch: vessel berthing and departure plans, berth allocation, and anchorage management.
2. Yard dispatch: block allocation, rehandling operations, and yard-resource management.
3. Equipment dispatch: allocation and assignment of quay cranes, yard cranes, terminal tractors, and other equipment.
4. Gate dispatch: terminal-tractor entry and exit, gate-lane management, and appointment management.

## Permission Rules
- Berth dispatcher: berth-dispatch operations only.
- Yard dispatcher: yard-dispatch operations only.
- Equipment dispatcher: equipment-dispatch operations only.
- Gate dispatcher: gate-dispatch operations only.
- Operations supervisor: operation permissions across all areas.
- Terminal manager: query-only permissions across all areas.

## Risk Controls
- Verify that equipment is idle before dispatching it.
- Verify berth availability before assigning a berth.
- Verify yard capacity before assigning a container slot.
- Verify appointment validity before processing gate entry.
- Verify that the vessel is berthed before loading or unloading.

## Communication Standards
- Use concise, clear, professional, and rigorous language.
- Confirm key information with the user before issuing an instruction.
- Proactively report the result after execution.
- When validation fails, explain why and provide alternatives.

## Available Operations

### Berth Dispatch
- query_vessel_plan: Query the vessel berthing plan.
- query_berth_status: Query berth status.
- query_anchorage: Query the anchorage queue.
- assign_berth: Assign a berth (validation required).
- update_berth_plan: Adjust the berthing plan.
- confirm_departure: Confirm departure.

### Yard Dispatch
- query_yard_status: Query yard status.
- query_container_location: Query container locations.
- query_rehandle_list: Query the rehandling list.
- assign_yard_slot: Assign a yard slot (validation required).
- create_rehandle_task: Create a rehandling task.
- update_container_location: Update a container location.

### Equipment Dispatch
- query_equipment_status: Query equipment status.
- query_equipment_task: Query equipment tasks.
- dispatch_equipment: Dispatch equipment (validation required).
- update_equipment_status: Update equipment status.
- cancel_task: Cancel a task.

### Gate Dispatch
- query_gate_status: Query gate status.
- query_gate_appointment: Query appointments.
- query_gate_queue: Query the queue.
- open_gate_channel: Open a gate lane.
- close_gate_channel: Close a gate lane.
- process_gate_pass: Process entry or exit (validation required).
```

## Tool

### Schema Registered by scripts/run.py

```json
{
  "type": "object",
  "properties": {
    "params": {
      "type": "object",
      "description": "Tool parameters"
    }
  }
}
```

## Skill

### skills/berth_scheduling/SKILL.md

```markdown
---
name: berth_scheduling
description: Berth scheduling skill
---

# Berth Scheduling Skill

## Overview

The berth scheduling skill provides vessel and berth information queries and helps dispatchers understand current port operations.

## When to Use

Use this skill when the user needs the following information:

- Query vessel arrival plans and status.
- Query berth occupancy and availability.
- Query vessels waiting at anchorage.

## Available Operations

### Query Tools

1. **query_vessel_plan** - Query vessel plans
   - Parameter: `vessel_id` (optional) - query one vessel by ID.
   - Returns: Detailed information for all vessels or one vessel.

2. **query_berth_status** - Query berth status
   - Parameters:
     - `status` (optional) - filter by status (available, occupied, reserved, maintenance).
     - `berth_id` (optional) - query one berth by ID.
   - Returns: A list of berth statuses matching the filters.

3. **query_anchorage** - Query vessels at anchorage
   - Parameters: none.
   - Returns: The list of vessels currently waiting at anchorage (status=at_anchor).

## Permission Requirements

- Query operations require read-only permission.
- The system verifies that the user is authorized to access the data.

## Data Sources

All data is loaded from JSON data files through DataStore.
```

### skills/equipment_scheduling/SKILL.md

````markdown
---
name: equipment_scheduling
description: Equipment scheduling skill for equipment-status queries, dispatch, and task management
version: 1.0.0
---

# Equipment Scheduling Skill

Manages container-terminal equipment dispatch operations, including equipment-status queries, task assignment, and status updates.

## Feature Overview

This skill provides equipment query and command operations:

### Query Operations
- `query_equipment_status`: Query equipment status with optional filtering by equipment ID, equipment type, and status.
- `query_equipment_task`: Query equipment tasks with optional filtering by equipment ID, task ID, and task status.

### Command Operations
- `dispatch_equipment`: Assign a task to equipment (the equipment must be idle).
- `update_equipment_status`: Update equipment status.
- `cancel_task`: Cancel a task and release the equipment.

## Usage Examples

### Query Equipment Status

```json
{
  "intent": "query_equipment_status",
  "params": {
    "equip_type": "quay_crane"
  }
}
```

### Dispatch Equipment

```json
{
  "intent": "dispatch_equipment",
  "params": {
    "equip_id": "QC01",
    "task_id": "T0001"
  }
}
```

### Update Equipment Status

```json
{
  "intent": "update_equipment_status",
  "params": {
    "equip_id": "QC01",
    "status": "working"
  }
}
```

### Cancel a Task

```json
{
  "intent": "cancel_task",
  "params": {
    "task_id": "T0001"
  }
}
```

## Parameter Reference

### query_equipment_status
| Parameter | Type | Required | Description |
|------|------|------|------|
| equip_id | string | No | Equipment ID; exact match. |
| equip_type | string | No | Equipment type (quay_crane/rtg/rmg/yard_truck/reach_stacker/top_loader). |
| status | string | No | Equipment status (idle/working/moving/fault/maintenance/offline). |

### query_equipment_task
| Parameter | Type | Required | Description |
|------|------|------|------|
| equip_id | string | No | Equipment ID. |
| task_id | string | No | Task ID. |
| status | string | No | Task status (pending/assigned/in_progress/completed/failed/cancelled). |

### dispatch_equipment
| Parameter | Type | Required | Description |
|------|------|------|------|
| equip_id | string | Yes | Equipment ID. |
| task_id | string | Yes | Task ID. |

### update_equipment_status
| Parameter | Type | Required | Description |
|------|------|------|------|
| equip_id | string | Yes | Equipment ID. |
| status | string | Yes | New status. |
| current_location | string | No | Current location (terminal tractors only). |

### cancel_task
| Parameter | Type | Required | Description |
|------|------|------|------|
| task_id | string | Yes | Task ID. |

## Error Handling

- Equipment not found: return an error and the list of available equipment.
- Equipment state does not satisfy dispatch requirements: return an error and a list of alternative available equipment.
- Task not found: return an error.
- Missing parameters: return the names of the missing parameters.
````

### skills/gate_scheduling/SKILL.md

```markdown
---
name: gate_scheduling
description: Gate scheduling skill for gate-lane management, appointment management, and terminal-tractor entry and exit
---

# Gate Scheduling Skill

## Overview

The gate scheduling skill provides gate-lane management and terminal-tractor entry and exit processing to help dispatchers manage gate operations.

## When to Use

Use this skill when the user needs to perform the following operations:

- Query gate-lane status and queue conditions.
- Query terminal-tractor entry appointments.
- Open or close gate lanes.
- Process terminal-tractor entry and exit (validate appointment status).

## Available Operations

### Query Tools

1. **query_gate_status** - Query gate-lane status
   - Parameters:
     - `channel_id` (optional) - query one lane by ID.
     - `type` (optional) - filter by type (inbound, outbound).
     - `status` (optional) - filter by status (open, closed, congested).
   - Returns: A list of gate-lane statuses matching the filters.

2. **query_gate_appointment** - Query appointment records
   - Parameters:
     - `appointment_id` (optional) - query one record by ID.
     - `truck_id` (optional) - filter by terminal-tractor ID.
     - `status` (optional) - filter by status (pending, valid, expired, completed, cancelled).
   - Returns: A list of appointment records matching the filters.

3. **query_gate_queue** - Query queue conditions
   - Parameters: none.
   - Returns: The total queue count and queue conditions by lane.

### Command Tools

1. **open_gate_channel** - Open a gate lane
   - Parameter: `channel_id` (required) - ID of the lane to open.
   - Returns: Operation result.

2. **close_gate_channel** - Close a gate lane
   - Parameters:
     - `channel_id` (required) - ID of the lane to close.
     - `reason` (optional) - reason for closure.
   - Returns: Operation result.

3. **process_gate_pass** - Process terminal-tractor entry or exit
   - Parameters:
     - `truck_id` (required) - terminal-tractor ID.
     - `channel_id` (required) - lane ID.
     - `direction` (required) - entry or exit direction (inbound/outbound).
   - Returns: Processing result, including appointment-validation status.

## Permission Requirements

- Query operations require read-only permission.
- Command operations require write permission.
- The system verifies that the user is authorized to access the data.

## Data Sources

All data is loaded from JSON data files through DataStore:
- gate_channels.json - Gate-lane data.
- appointments.json - Appointment records.
```

### skills/yard_scheduling/SKILL.md

```markdown
---
name: yard_scheduling
description: Yard scheduling skill for block-status queries, container-location queries, and rehandling management
---

# Yard Scheduling Skill

## Overview

The yard scheduling skill provides queries and management for yard block status, container locations, and rehandling operations, helping dispatchers understand yard-resource usage and carry out dispatch operations.

## When to Use

Use this skill when the user needs to perform the following operations:

- Query yard block status and capacity.
- Query container-location information.
- Manage rehandling tasks.
- Assign a landing slot.
- Update a container location.

## Available Operations

### Query Tools

1. **query_yard_status** - Query yard block status
   - Parameters:
     - `block_id` (optional) - query one block by ID.
     - `type` (optional) - filter by container type (import, export, transshipment, empty, dangerous, reefer).
   - Returns: A list of matching block statuses, including capacity, occupancy, and available slots.

2. **query_container_location** - Query container locations
   - Parameters:
     - `container_id` (optional) - query the location of one container.
     - `block_id` (optional) - query all containers in a specified block.
   - Returns: A list of container-location details.

3. **query_rehandle_list** - Query rehandling tasks
   - Parameters: none.
   - Returns: A list of pending rehandling tasks.

### Command Tools

1. **assign_yard_slot** - Assign a landing slot
   - Parameters:
     - `container_id` (required) - container ID.
     - `block_id` (required) - target block ID.
     - `bay` (optional) - bay number.
     - `row` (optional) - row number.
     - `tier` (optional) - tier number.
   - Validation: block capacity, block status, and container-type compatibility.
   - Returns: Allocation result.

2. **create_rehandle_task** - Create a rehandling task
   - Parameters:
     - `container_id` (required) - ID of the container to move.
     - `from_block_id` (required) - source block ID.
     - `to_block_id` (optional) - target block ID; selected automatically if omitted.
     - `reason` (optional) - reason for rehandling.
   - Returns: Information about the created rehandling task.

3. **update_container_location** - Update a container location
   - Parameters:
     - `container_id` (required) - container ID.
     - `block_id` (required) - new block ID.
     - `bay` (required) - new bay number.
     - `row` (required) - new row number.
     - `tier` (required) - new tier number.
   - Returns: Update result.

## Permission Requirements

- Query operations require read-only permission.
- Command operations require write permission.
- The system validates the legitimacy of operations.

## Data Sources

All data is loaded from and saved to JSON data files through DataStore.
```
