---
name: pet_matching
description: Pet matching skill
---

# Pet Matching Skill

## Overview

Pet matching skill helps a prospective owner find a suitable breed and browse adoptable animals.

## When to Use

Use this skill when the user wants to:
- Find a breed that suits their home, activity level, or household
- Understand a breed's exercise, grooming, and living-space needs
- Browse adoptable pets
- Get a specific pet's full profile

## Available Operations

### breed_search
- **Parameters**: `species` (optional: dog/cat), `size` (optional: small/medium/large), `temperament` (optional), `query` (optional), `limit` (optional)
- **Returns**: Matching breeds, ordered by name; with no parameters returns the whole catalog

### breed_details
- **Parameters**: `breed_id` (required)
- **Returns**: Exercise needs, grooming level, apartment and kid suitability, lifespan

### pet_list
- **Parameters**: `species` (optional), `size` (optional), `temperament` (optional), `max_age_months` (optional)
- **Returns**: Adoptable pets only, with breed name and size attached

### pet_details
- **Parameters**: `pet_id` (required)
- **Returns**: The pet's profile together with its resolved breed

## Data Source

Breeds and pets load from `data/breeds.json` and `data/pets.json` via `DataStore`. All listings
are simulated — no real adoption process is involved.
