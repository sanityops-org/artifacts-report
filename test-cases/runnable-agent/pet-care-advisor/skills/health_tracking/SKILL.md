---
name: health_tracking
description: Health tracking skill
---

# Health Tracking Skill

## Overview

Health tracking skill keeps a record of vaccinations, vet visits, weight entries, medications, and
known allergies, and flags dates that are coming up.

## When to Use

Use this skill when the user wants to:
- Review a pet's health history
- Log a vaccination, vet visit, weight entry, medication, or allergy
- Check whether anything is due or overdue

## Available Operations

### health_record_list
- **Parameters**: `pet_id` (required)
- **Returns**: The pet's records, newest first, each annotated with `days_until` and `overdue`,
  plus a `due_soon` list covering anything within the next 30 days

### health_record_add
- **Parameters**: `pet_id`, `type`, `date`, `description` (required); `next_due` (optional)
- **Returns**: The created record
- **Note**: The description is stored exactly as supplied by the user. The tool records history
  only — it does not interpret findings or suggest treatment.

## Scope Limit

This skill records what the user reports. It never diagnoses, never recommends medication or
dosage, and never advises on a health condition. Any health question is referred to a licensed
veterinarian.
