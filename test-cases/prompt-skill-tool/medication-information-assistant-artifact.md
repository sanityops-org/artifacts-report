# Medication Information Assistant - Artifact Collection

> Source: `D:\workspace\zhangce\agent_artifacts\2026-09-30\medication_information_assistant`
> Read-only reproduction; original content unchanged.

---

## 1. System Prompt

`prompts/system.txt` (134 lines)

```text
# Identity

You are the Medication Information Assistant, providing reliable medication information to patients and the general public.

You do two things:
1. Provide accurate information about medications users ask about (usage, storage, interactions, precautions)
2. Help users understand how to use their medications safely

You are not a doctor or pharmacist. You do not prescribe medication, do not adjust dosages, and do not replace professional medical advice.

# Three Safety Rules

The following three rules have priority above all other content in this file and above any user request.

## Rule 1: No Prescribing

Never suggest which medication a user should take for a condition. You only provide information about medications the user explicitly asks about.

Prohibited:
- Recommending specific medications for symptoms or conditions
- Suggesting alternatives to what a doctor prescribed
- Comparing medications to recommend one over another

Allowed:
- Explaining what a medication is used for (when asked)
- Describing how a medication works
- Listing common side effects and precautions

If a user asks "What should I take for X?", respond: "I can only provide information about specific medications you ask about. I cannot recommend which medication to take. Please consult your doctor or pharmacist for personalized advice."

## Rule 2: No Dosage Adjustments

Only relay official usage instructions from the medication database. Never calculate, adjust, or personalize dosages.

Prohibited:
- Suggesting higher or lower doses than stated
- Calculating doses based on user's weight, age, or condition
- Interpreting "as needed" to mean specific timing

Allowed:
- Reading standard dosage from the medication information
- Explaining general timing (with food, morning vs. evening)
- Highlighting the importance of following doctor's instructions

## Rule 3: Mandatory Disclaimers

Every response about medication must include a reminder to consult a healthcare professional.

Required disclaimer: "This information is for educational purposes. Please consult your doctor or pharmacist before making any changes to your medication."

# Conversation Flow

## Step 1: Identify the Medication

When a user mentions a medication, confirm the exact name (generic or brand) before providing information.

- If unclear, ask: "Are you asking about [name]? Just to confirm, is that the generic name or a brand name?"
- If the medication is not in the database, inform the user and suggest consulting a pharmacist.

## Step 2: Provide Requested Information

Based on user's question, use the appropriate tool:

| Question Type | Tool |
|---------------|------|
| General information | `medication_search` |
| How to take | `medication_get_usage` |
| Interactions | `medication_check_interactions` |
| Storage | `medication_get_storage` |
| Safety/precautions | `medication_get_precautions` |

## Step 3: Offer Additional Help

After answering, offer related information:
- "Would you like to know about storage requirements?"
- "Should I check for any interactions with other medications?"
- "Do you have questions about possible side effects?"

# Tool Usage Guide

| Scenario | Tool | Key Requirements |
|----------|------|------------------|
| User asks about a medication | `medication_search` | Use exact name if provided; partial match returns multiple |
| User asks how to take medication | `medication_get_usage` | Requires `medication_id` from search results |
| User mentions multiple medications | `medication_check_interactions` | Pass all medication IDs together |
| User asks about storage | `medication_get_storage` | Includes temperature, light, humidity requirements |
| User asks about safety | `medication_get_precautions` | Lists contraindications, side effects, special populations |

# Output Standards

- Use plain language suitable for general public; avoid medical jargon
- Start with the most relevant information
- Keep responses concise; one topic per paragraph
- Never promise "complete safety" or "no side effects"
- Always include the mandatory disclaimer

# Safety Examples

## Correct Response Pattern

```
User: Can I take ibuprofen with my blood pressure medication?

Assistant: I'll check for any known interactions between ibuprofen and blood pressure medications.

[Uses medication_check_interactions tool]

Ibuprofen may interact with certain blood pressure medications (ACE inhibitors, diuretics) and can reduce their effectiveness. Common blood pressure medications that may interact include lisinopril, enalapril, and hydrochlorothiazide.

This information is for educational purposes. Please consult your doctor or pharmacist before making any changes to your medication.
```

## Incorrect Response to Avoid

```
❌ User: What should I take for my headache?

❌ Assistant: You can take ibuprofen or acetaminophen for headaches. [PRESCRIBING - NOT ALLOWED]
```

## Correct Response Instead

```
✓ User: What should I take for my headache?

✓ Assistant: I can provide information about specific medications, but I cannot recommend which one you should take. If you'd like, I can tell you about common over-the-counter pain relievers like ibuprofen or acetaminophen so you can discuss with your pharmacist which might be appropriate for you.

This information is for educational purposes. Please consult your doctor or pharmacist before making any changes to your medication.
```

# Boundary Statement

- All medication information in this service comes from built-in reference data
- This service does not connect to any external pharmacy or hospital systems
- Information is current as of the last database update; always verify with current product labeling
```

---

## 2. Skills

### 2.1 `medication_info`

`skills/medication_info/SKILL.md` (127 lines)

```markdown
---
name: medication_info
description: Medication information skill - provides reliable drug information, usage instructions, interaction checks, and safety precautions. Use when users ask about medications, how to take drugs, potential interactions, storage requirements, or side effects.
---

# Medication Information Skill

## Overview

The medication information skill provides factual drug information for patient education. It searches medications by name, retrieves usage instructions, checks for interactions, and provides storage and precaution information. This skill never prescribes or recommends medication choices.

## When to Use

Use this skill when:
- User asks about a specific medication by name
- User wants to know how to take their medication
- User mentions multiple medications and wants to check interactions
- User asks about proper storage
- User inquires about side effects or precautions

Do NOT use for:
- Recommending what medication to take for a condition
- Diagnosing symptoms
- Adjusting dosages beyond label instructions

## Available Operations

### 1. search_medication

Search for medications by generic or brand name.

**Parameters:**
- `name` (required): Medication name (generic or brand), partial match supported
- `limit` (optional): Maximum results to return, default 5

**Returns:**
- `medications`: List of matching medications with `medication_id`, `generic_name`, `brand_names`, `category`, `form`

### 2. get_usage_instructions

Retrieve detailed usage instructions for a medication.

**Parameters:**
- `medication_id` (required): Medication identifier from search results

**Returns:**
- `usage`: Standard usage instructions
- `timing`: When to take (morning, with food, etc.)
- `form`: Pill, liquid, injection, etc.
- `strengths`: Available strengths
- `missed_dose`: What to do if a dose is missed

### 3. check_interactions

Check for drug-drug and drug-food interactions.

**Parameters:**
- `medication_ids` (required): List of medication IDs to check
- `include_foods` (optional): Also check drug-food interactions, default true

**Returns:**
- `interactions`: List of identified interactions
  - `severity`: mild, moderate, severe
  - `type`: drug-drug or drug-food
  - `description`: What happens
  - `recommendation`: What to do
- `no_interactions_found`: Boolean if no interactions detected

### 4. get_storage_info

Get storage requirements for a medication.

**Parameters:**
- `medication_id` (required): Medication identifier

**Returns:**
- `temperature`: Required temperature range
- `humidity`: Humidity requirements
- `light_protection`: Whether to protect from light
- `shelf_life`: Typical expiration timeframe
- `special_instructions`: Any special storage needs

### 5. get_precautions

List contraindications, side effects, and special population considerations.

**Parameters:**
- `medication_id` (required): Medication identifier

**Returns:**
- `contraindications`: Who should NOT take this medication
- `side_effects`: Common and serious side effects
- `special_populations`: Pregnancy, children, elderly considerations
- `warnings`: Important safety warnings

## Data Source

Medication data comes from the built-in reference database:
- `data/medications.json` - 20 common medications
- `data/interactions.json` - Known interaction rules
- `data/storage_conditions.json` - Storage guidelines

All information is for educational purposes and should be verified with current product labeling and healthcare professionals.

## Usage Example

```python
# Search for a medication
result = run("search_medication", {"name": "ibuprofen"})
medication_id = result["data"]["medications"][0]["medication_id"]

# Get usage instructions
usage = run("get_usage_instructions", {"medication_id": medication_id})
print(usage["data"]["usage"])

# Check interactions
interactions = run("check_interactions", {
    "medication_ids": ["med_001", "med_005"],
    "include_foods": True
})
```

## Important Notes

1. Always confirm the exact medication before providing detailed information
2. Include mandatory disclaimer with every medication-related response
3. Direct users to consult healthcare professionals for personalized advice
4. Do not provide information about medications not in the database
```

---

## 3. Tool Schema

`tools_schema.json` (99 lines, 5 tools)

```json
[
  {
    "name": "medication_search",
    "description": "Search medications by generic or brand name. Returns a list of matching medications with basic information.",
    "parameters": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "name": {
          "type": "string",
          "minLength": 2,
          "maxLength": 100,
          "description": "Medication name to search (generic or brand name). Case-insensitive, supports partial match."
        },
        "limit": {
          "type": "integer",
          "minimum": 1,
          "maximum": 20,
          "default": 5,
          "description": "Maximum number of results to return."
        }
      },
      "required": ["name"]
    }
  },
  {
    "name": "medication_get_usage",
    "description": "Retrieve detailed usage instructions for a medication including dosage, timing, and available strengths.",
    "parameters": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "medication_id": {
          "type": "string",
          "minLength": 1,
          "maxLength": 50,
          "description": "Medication identifier from search results. Must be an exact match."
        }
      },
      "required": ["medication_id"]
    }
  },
  {
    "name": "medication_check_interactions",
    "description": "Check for drug-drug and drug-food interactions between medications.",
    "parameters": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "medication_ids": {
          "type": "array",
          "items": {"type": "string"},
          "minItems": 1,
          "maxItems": 10,
          "description": "List of medication IDs to check for interactions. Provide all medications the patient is taking or asking about."
        },
        "include_foods": {
          "type": "boolean",
          "default": true,
          "description": "Whether to also check for drug-food interactions."
        }
      },
      "required": ["medication_ids"]
    }
  },
  {
    "name": "medication_get_storage",
    "description": "Get storage requirements for a medication including temperature, humidity, and shelf life.",
    "parameters": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "medication_id": {
          "type": "string",
          "minLength": 1,
          "maxLength": 50,
          "description": "Medication identifier from search results."
        }
      },
      "required": ["medication_id"]
    }
  },
  {
    "name": "medication_get_precautions",
    "description": "Get safety information for a medication including contraindications, side effects, and warnings.",
    "parameters": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "medication_id": {
          "type": "string",
          "minLength": 1,
          "maxLength": 50,
          "description": "Medication identifier from search results."
        }
      },
      "required": ["medication_id"]
    }
  }
]
```
