---
name: triage
description: Guidance and triage skills
---

# Guidance and triage skills (Triage Skill)

## Brief account

The guidance and triage skills provide the triage ability of "from oral description to candidate department": first use the rules to do compulsory screening for dangerous symptoms,
Then converge the symptoms to the limited candidate departments, and finally check the medical information of the department. This skill only involves the department level,
It does not involve number source and registration (see the registration appointment skills for that part).

## When to use

This skill should be used when the patient describes physical discomfort and asks "which department should be hung":

- The patient describes discomfort for the first time, or after each round of supplementary description - dangerous symptoms screening must be done first.
- The dangerous symptoms were not hit, and enough information has been inquired - convergent candidate department
- Recommended department has been determined - check the location of the department and prepare before consultation

## Available operation

1. **check_red_flags** - Red flag symptom screening (compulsory gate)
   - Parameters: `text` (required) - The patient's original oral description in this round, as it is, do not rewrite
   - Parameters: `symptoms` (optional) - List of extracted normalized symptom words
   - Return:`hit` / `rule_id` / `name` / `level` / `action` / `advice` / `matched_keywords`
   - **`hit` When it is true, the triage and registration must be stopped immediately, and the `advice` guideline must be directly output.**

2. **shortlist_departments** - Convergent candidate departments (up to 3)
   - Parameters: `symptoms` (required) - List of normalized symptom words
   - Parameters: `age` (optional) - the age of the patient; when under 14 years old, the selection is forced to converge to pediatrics
   - Parameters: `max_candidates` (optional) - the maximum number of candidates, default 3
   - Return:`candidates`（`department_id` / `name` / `score` / `matched_symptoms`）/
     `fallback_department` / `age_rule_applied` / `note`
   - **In the end, only one section can be selected from `candidates`; `candidates` are recommended when empty.
     `fallback_department`**

3. **query_department** - Check the department information
   - Parameters: `department_id` (required) - must use the identification in the candidate return, do not use the display name
   - Return:`name` / `category` / `description` / `location` / `preparation`

## Data source

The rule table and department table come from the built-in simulation data:`data/red_flag_rules.json`、
`data/symptom_department_map.json`、`data/departments.json`，Warp `apis/data_store.py`
Read, `apis/triage_engine.py` execute rules. This skill does not output the name of the disease, diagnostic conclusions or medication suggestions.
