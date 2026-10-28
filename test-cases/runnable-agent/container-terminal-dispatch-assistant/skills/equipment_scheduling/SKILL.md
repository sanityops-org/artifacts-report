---
name: equipment_scheduling
description: Equipment scheduling skills are used for equipment status inquiry, dispatching and task management.
version: 1.0.0
---

# Equipment scheduling skills

Manage the equipment dispatching operation of the container terminal, including equipment status inquiry, task assignment, status update, etc.

## Overview of functions

This skill provides device-related queries and instruction operations:

### Query operation
- `query_equipment_status`: Query device status, support device ID, device type, status filtering
- `query_equipment_task`: Query device tasks, support device ID, task ID, task status filtering

### Command operation
- `dispatch_equipment`: Dispatch and assign tasks to the equipment (check that the equipment must be idle)
- `update_equipment_status`: Update the device status
- `cancel_task`: Cancel the task and release the device

## Examples of use

### Check the status of the device

```json
{
  "intent": "query_equipment_status",
  "params": {
    "equip_type": "quay_crane"
  }
}
```

### Dispatch

```json
{
  "intent": "dispatch_equipment",
  "params": {
    "equip_id": "QC01",
    "task_id": "T0001"
  }
}
```

### Update the device status

```json
{
  "intent": "update_equipment_status",
  "params": {
    "equip_id": "QC01",
    "status": "working"
  }
}
```

### Cancel the task

```json
{
  "intent": "cancel_task",
  "params": {
    "task_id": "T0001"
  }
}
```

## Parameter description

### query_equipment_status
| Parameter | Type | Required | Description |
|------|------|------|------|
| equip_id | string | No | Device ID, exact matching |
| equip_type | string | No | Device Type（quay_crane/rtg/rmg/yard_truck/reach_stacker/top_loader） |
| status | string | No | Device Status（idle/working/moving/fault/maintenance/offline） |

### query_equipment_task
| Parameter | Type | Required | Description |
|------|------|------|------|
| equip_id | string | No | EquipmentID |
| task_id | string | No | TaskID |
| status | string | No | Task Status（pending/assigned/in_progress/completed/failed/cancelled） |

### dispatch_equipment
| Parameter | Type | Required | Description |
|------|------|------|------|
| equip_id | string | Yes | EquipmentID |
| task_id | string | Yes | TaskID |

### update_equipment_status
| Parameter | Type | Required | Description |
|------|------|------|------|
| equip_id | string | Yes | EquipmentID |
| status | string | Yes | New status |
| current_location | string | No | Current location (for card collection only) |

### cancel_task
| Parameter | Type | Required | Description |
|------|------|------|------|
| task_id | string | Yes | TaskID |

## Error handling

- The device does not exist: return the error message and the list of available devices
- The device status does not meet the dispatch conditions: return the list of errors and available alternative devices
- The task does not exist: return an error message
- Missing parameter: return the specific missing parameter name
