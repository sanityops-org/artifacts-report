---
name: care_scheduling
description: Care scheduling skill
---

# Care Scheduling Skill

## Overview

Care scheduling skill builds and runs a pet's daily routine — feeding, walks, grooming, play,
training, and booked vet visits.

## When to Use

Use this skill when the user wants to:
- See what care is due today
- Add a recurring or one-off care task
- Mark a task as done or skipped
- Review all tasks for one pet

## Available Operations

### care_task_list
- **Parameters**: `pet_id` (optional), `status` (optional: pending/done/skipped)
- **Returns**: Tasks ordered by time, each enriched with the pet's name

### care_task_create
- **Parameters**: `pet_id`, `type`, `scheduled_time` (required); `frequency`, `scheduled_date`, `notes` (optional)
- **Returns**: The created task
- **Note**: `scheduled_date` is required when frequency is `once` or `weekly`. The tool stores only
  what the user supplies — it never proposes a feeding amount, medication name, or dose.

### care_task_complete
- **Parameters**: `task_id` (required), `skipped` (optional)
- **Returns**: The updated task; rejects tasks that are already resolved

### care_schedule_today
- **Parameters**: `include_done` (optional), `date` (optional)
- **Returns**: The day's outstanding tasks across all pets

## Data Source

Tasks are seeded from `data/care_tasks.json` and held in memory for the session. Nothing is
written back to disk.
