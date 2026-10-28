---
name: gate_scheduling
description: Gate dispatching skills are used for gate channel management, appointment management, and card collection entry and exit processing.
---

# Gate dispatching skills (Gate Scheduling Skill)

## Brief account

Gate dispatching skills provide gate channel management and card entry and exit processing capabilities to help dispatchers manage gate operations.

## When to use

When you need to perform the following operations, you should use this skill:

- Check the status of the gate channel and the queue
- Check the reservation record of card collection and port entry
- Open/close the gate passage
- Process the entry and exit of the card (check the reservation status)

## Available operation

### Query tools

1. **query_gate_status** - Check the status of the gate channel
   - Parameters:
     - `channel_id` (Optional) - Specify the channel ID to query a single channel
     - `type` (Optional) - Filter by type (inbound, outbound)
     - `status` (Optional) - Filter by status (open, closed, congested)
   - Back: List of eligible gate channel statuses

2. **query_gate_appointment** - Check the appointment record
   - Parameters:
     - `appointment_id` (Optional) - Specify the appointment ID to query a single record
     - `truck_id` (Optional) - Filter by collection card ID
     - `status` (Optional) - Filter by status (pending, valid, expired, completed, cancelled)
   - Back: List of eligible appointment records

3. **query_gate_queue** - Check the queue
   - Parameters: None
   - Back: the total number of queues and the queues of each channel

### Command tools

1. **open_gate_channel** - Open the gate passage
   - Parameters: `channel_id` (required) - the channel to be openedID
   - Return: Operation Result

2. **close_gate_channel** - Close the gate passage
   - Parameters:
     - `channel_id` (Required) - The channel to be closedID
     - `reason` (Optional) - Reason for closing
   - Return: Operation Result

3. **process_gate_pass** - Handle the entry and exit of the collection card
   - Parameters:
     - `truck_id` (Required) - Collecting vehiclesID
     - `channel_id` (Required) - ChannelID
     - `direction` (Required) - Direction of entry and exit (inbound/outbound)
   - Return: Processing results (including appointment verification status)

## Permission requirements

- Query operation requires read-only permission.
- Instruction operation requires write permission.
- The system will verify whether the user has the right to access the relevant data.

## Data source

All data is loaded from the JSON data file through DataStore:
- gate_channels.json - Gate channel data
- appointments.json - Appointment record data
