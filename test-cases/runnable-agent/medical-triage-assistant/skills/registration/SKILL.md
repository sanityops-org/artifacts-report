---
name: registration
description: Registration appointment skills
---

# Registration appointment skills (Registration Skill)

## Brief account

Registration appointment skills provide "complete closed loop after determining the department": record patient information, query number source, registration,
Inquire and cancel the registration. The number source and registration records come from the built-in simulation data and do not involve any real patient information.

## When to use

When the patient has determined the department to be visited and is ready to register, this skill should be used:

- The patient provides or supplements the name, gender, age and mobile phone number.
- Confirm whether the patient's information is complete before registration
- Query the number source and residual number of a department
- Complete the registration, check the registration record, cancel the registration

## Available operation

1. **update_profile** - Record or update patient information
   - Parameters: `name` / `gender` (male|female) / `age` / `phone` (all are optional, give at least one)
   - Back: Patient Information + `is_complete` + `missing_fields`
   - In-session field accumulation, fields with the value `null` will not overwrite the existing value.

2. **get_profile** - Read the patient's information
   - Parameters: None
   - Back: Patient Information + `is_complete` + `missing_fields`
   - **Before registering, you must use it to confirm that the name, gender and age are complete.**

3. **query_slots** - Query number source and residual number
   - Parameter: `department_id` (required)
   - Parameters: `date` (optional, YYYY-MM-DD) / `doctor_id` (optional) / `period` (optional,morning|afternoon)
   - Return: `department_name` / `count` / `slots` (including `slot_id`, doctor, date, period, remainder)
   - Only return the registered number source; **`slot_id` can only use the value returned here, do not make it up.**

4. **create_appointment** - Register
   - Parameter: `slot_id` (required) - return result from `query_slots`
   - Back: `appointment_id` (registration number) / doctor / date / period / `remaining_after` / `hint`
   - Verification order: the patient's information is complete → the number source can be hung up → no duplicate registration; no side effects will be produced if any failure
   - The same patient in the same department on the same day cannot be registered repeatedly.

5. **query_appointment** - Check the registration record
   - Parameter: `appointment_id` (optional) - Omitted will return all registered records of this session
   - Return: `count` / `appointments` (including status `booked` | `cancelled` | `completed`）

6. **cancel_appointment** - Cancel the registration
   - Parameter: `appointment_id` (required)
   - Return:`status` (`cancelled`) / `cancelled_at` / `remaining_after`
   - Only the record of `booked` status and belonging to the current session patient can be canceled; after success, the residual number will be made up.

## Data source

`data/slots.json`、`data/appointments.json`、`data/doctors.json`、`data/departments.json`，
Read and write through `apis/data_store.py`. The patient's information is saved in the process session.（`apis/session_api.py`），
If the disk is not dropped, it will be emptied when the process is restarted.
