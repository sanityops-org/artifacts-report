---
name: yard_scheduling
description: The storage field scheduling skills are used for box area status inquiry, container location inquiry, and box turning operation management.
---

# Stacking field scheduling skills (Yard Scheduling Skill)

## Brief account

The storage field dispatching skill provides the query and management ability of the storage box area status, container location and box turning operation, and helps dispatchers grasp the use of storage field resources and perform scheduling operations.

## When to use

When you need to perform the following operations, you should use this skill:

- Query the status and capacity of the storage box area
- Check the location information of the container
- Manage the task of turning over boxes
- Assign the location of the box
- Update the container location

## Available operation

### Query tools

1. **query_yard_status** - Query the status of the storage box area
   - Parameters:
     - `block_id` (Optional) - Specify the box area ID to query a single box area
     - `type` (Optional) - Filter by container type (import, export, transshipment, empty, dangerous, reefer)
   - Return: List of eligible box status, including capacity, occupancy, available box and other information

2. **query_container_location** - Check the location of the container
   - Parameters:
     - `container_id` (Optional) - Specify the container ID query location
     - `block_id` (Optional) - Check all containers in the designated box area
   - Back: Detailed list of container locations

3. **query_rehandle_list** - Query the list of box-turning tasks
   - Parameters: None
   - Back: List of pending box-turning tasks

### Command tools

1. **assign_yard_slot** - Assign the location of the box
   - Parameters:
     - `container_id` (Necessary) - ContainerID
     - `block_id` (Required) - Target box areaID
     - `bay` (Optional) - Shell number
     - `row` (Optional) - Row number
     - `tier` (Optional) - Floor number
   - Verification: box area capacity, box area status, container type matching
   - Return: Assign results

2. **create_rehandle_task** - Create a box-turning task
   - Parameters:
     - `container_id` (Necessary) - Containers that need to be turned overID
     - `from_block_id` (Required) - Original box areaID
     - `to_block_id` (Optional) - Target box area ID, automatically selected if not specified
     - `reason` (Optional) - Reason for turning over the box
   - Back: Created box-turning task information

3. **update_container_location** - Update the container location
   - Parameters:
     - `container_id` (Necessary) - ContainerID
     - `block_id` (Required) - New Box AreaID
     - `bay` (Required) - New Beibit number
     - `row` (Required) - New queue number
     - `tier` (Required) - New layer number
   - Return: Update the result

## Permission requirements

- Query operation requires read-only permission.
- Instruction operation requires write permission.
- The system will verify the legality of the operation.

## Data source

All data is loaded and saved from JSON data files through DataStore.
