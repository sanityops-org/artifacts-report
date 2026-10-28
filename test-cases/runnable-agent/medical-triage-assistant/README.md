# Medical guidance assistant

## Project information

| Project | Description |
|------|------|
| **Industry** | Medical and Health (Outpatient Guidance) |
| **Project Name** | Medical Guidance Assistant |
| **Edition** | v1.0.0 |
| **Date of creation** | 2026-09-26 |
| **Author** | Agent Artifacts Team |
| **Technical stack** | Python 3.11+、Pydantic 2.0+、sanityops_agent |
| **Permit** | MIT License |

## Brief account

The medical guidance assistant is an intelligent guidance agent for **self-service use of outpatients**. The patient describes the discomfort in daily oral language. The system first intercepts dangerous symptoms by ** rules **, and then converges the symptoms to no more than 3 candidate departments. Finally, the ** model selects 1 department in the candidate set and explains the reason **, and then queries the source of the number and completes the registration.

**It doesn't make a diagnosis. ** The whole process does not output the name of the disease, does not judge the severity of the disease, does not give medication advice, and only answers "it is recommended to see which department, where this department is, when there is the number, and how to hang up".

## Function description

### Three major abilities

| Ability | Description |
|------|------|
| **Red flag symptom screening** | Identify chest pain, disturbance of consciousness, hemorrhage and other dangerous signals, compulsory guidance to emergency / 120, ** do not enter general triage** |
| **Department recommendation** | The rule converges the symptoms to ≤ 3 candidate departments, and the model selects one in the candidate set and explains the basis. |
| **Registered closed-loop** | Number source inquiry → Complete patient information → Registration → Registered inquiry → Cancel and roll back the number source |

### Three red lines (the prompt word layer is mandatory, and the priority is higher than all other requirements)

| Number | Red Line | Landing Method |
|------|------|----------|
| 1 | Dangerous symptoms must be interrupted immediately | `triage_check_red_flags` hit `hit=true` to stop triage, follow-up and registration, and directly output emergency guidelines |
| 2 | No diagnosis, no medication | Tool return structure ** does not include ** disease / diagnosis / drug field; prompts are prohibited |
| 3 | Departments can only be selected in the candidate set | Recommended departments must be from `candidates` of `triage_shortlist_departments`; candidates are empty `fallback_department` |

### Main process

```
The patient describes the discomfort
  → triage_check_red_flags ──Hit-→ Output emergency/120 guidelines, terminate the process
        │ Not hit
        ↓
  → Structured follow-up 1~3 rounds (main complaint → part/nature/duration → accompanying symptoms)
        ↓
  → triage_shortlist_departments → Candidate departments (≤3, including pediatric age rules)
        ↓
  → Select 1 model in the candidate set and explain
        ↓
  → triage_query_department → Business scope of the department / location / preparation before consultation
        ↓
  → appointment_query_slots → Optional number source
        ↓
  → patient_update_profile（Make up for it first when the information is incomplete)
        ↓
  → appointment_create → Registration number + consultation tips
        ↓
  → appointment_query / appointment_cancel
```

### Red Flag Rules (10)

| rule_id | Name | Level |
|---------|------|------|
| RF001 | Chest pain / squeezing pain in the anterior region | emergency |
| RF002 | Severe shortness of breath | emergency |
| RF003 | DISORDER OF CONSCIOUSNESS / FAINTING / CONVULSIONS | emergency |
| RF004 | Massive haemorrhage | emergency |
| RF005 | Suspected stroke | emergency |
| RF006 | Severe abdominal pain accompanied by abdominal tension | emergency |
| RF007 | High fever convulsions in children | emergency |
| RF008 | Severe allergic reaction | emergency |
| RF009 | Abdominal pain during pregnancy / vaginal bleeding | emergency |
| RF010 | Vomiting after head trauma / change of consciousness | urgent |

`emergency` → `call_120_or_er`；`urgent` → `er_soon`。**Both levels will interrupt the general triage**, and there is no branch of "red flag but continuing triage".

## List of skills

The system contains 2 skills, which are executed through the unified entrance `run(intent, params)` route.

### 1. triage（Guidance and triage skills)

Red flag screening, symptoms converging with candidate departments.

| Intention | Description |
|------|------|
| `check_red_flags` | The original description of the inpatient, return whether the red flag is hit and the corresponding emergency guidelines. |
| `shortlist_departments` | Converge from symptom words to candidate departments (≤3), including pediatric age rules and bottom |
| `query_department` | Inquire about the business scope of the department, the location of the outpatient clinic and the pre-treatment preparation tips |

### 2. registration（Registration appointment skills)

Closed loop of patient information maintenance and registration.

| Intention | Description |
|------|------|
| `update_profile` | Record / Update the name, gender, age and mobile phone number of the patient in the session |
| `get_profile` | Read the patient information in the session and give `is_complete` |
| `query_slots` | By department / date / doctor / period query can register the source and residual number |
| `create_appointment` | Register and verify in order (complete information → valid number source → non-duplicate) |
| `query_appointment` | Check by registration number, or query all registration records of this session |
| `cancel_appointment` | Cancel the registration and make up for the source of the corresponding number |

## Project structure

```
Medical guidance assistant/
├── README.md                  # Project description (this document)
├── requirements.txt           # Dependent package
├── .env.example               # Examples of environment variables
├── tools_schema.json          # 9 Neutral format declaration of tools (for platform paste)
├── prompts/
│   └── system.txt             # System prompts (including three red lines, self-containing)
├── models/                    # Pydantic Data model
│   ├── enums.py               # Enumeration definition
│   ├── department.py          # Department model
│   ├── doctor.py              # Doctor model
│   ├── slot.py                # Number source model
│   ├── appointment.py         # Registered record model
│   └── patient.py             # Patient model
├── apis/                      # Domain service layer
│   ├── data_store.py          # JSON Read and write (general _load_list / _save_list）
│   ├── triage_engine.py       # Core: Red Flag Screening + Candidate Department Convergence
│   └── session_api.py         # Patient conversation in the process
├── data/                      # Simulation data (12 departments / 24 doctors / 240 sources)
│   ├── departments.json
│   ├── doctors.json
│   ├── slots.json
│   ├── red_flag_rules.json
│   ├── symptom_department_map.json
│   └── appointments.json
├── tools/                     # Executable tool (SDK automatic scanning registration, the file name is the tool name)
│   ├── triage_check_red_flags.py
│   ├── triage_shortlist_departments.py
│   ├── triage_query_department.py
│   ├── patient_update_profile.py
│   ├── patient_get_profile.py
│   ├── appointment_query_slots.py
│   ├── appointment_create.py
│   ├── appointment_query.py
│   └── appointment_cancel.py
├── skills/                    # Skill definition (injected by SkillManager at runtime)
│   ├── triage/                # Guidance and triage skills
│   └── registration/          # Registration appointment skills
├── scripts/
│   ├── __init__.py            # Package mark
│   ├── run.py                 # Agent Start the script
│   └── setup.py               # Initialize the check script
└── tests/                     # Cross-layer integration test and contract test
    ├── test_integration.py
    ├── test_prompt_contract.py
    ├── test_tools_schema.py
    ├── test_data_files.py
    └── test_run_wiring.py
```

## Data model

All models are Pydantic v2 `BaseModel`, and JSON reading and writing are unified. `model_validate` / `model_dump(mode="json")`。

- **`Department`** — `department_id`、`name`、`category`（internal/surgical/specialty/emergency）、`description`、`location`、`preparation: list[str]`
- **`Doctor`** — `doctor_id`、`name`、`title`（Chief physician/Deputy Chief Physician/Chief Physician),`department_id`、`specialties`、`clinic_days`
- **`Slot`** — `slot_id`、`department_id`、`doctor_id`、`date`、`period`（morning/afternoon）、`start_time`、`end_time`、`capacity`、`remaining`、`status`（available/full/closed）
- **`Appointment`** — `appointment_id`、`patient_name`、`department_id`、`doctor_id`、`slot_id`、`date`、`period`、`status`（booked/cancelled/completed）、`created_at`、`cancelled_at`
- **`PatientProfile`** — `name`、`gender`、`age`、`phone`；`is_complete` Derived attributes (name + gender + age are complete)
- **Enumerate** — `DepartmentCategory`、`DoctorTitle`、`SlotPeriod`、`SlotStatus`、`AppointmentStatus`、`Gender`、`RedFlagLevel`、`RedFlagAction`

The format of the registration number is `AP{YYYYMMDD}{4-digit serial number}`; the record only changes the status and is never physically deleted, so the order canceled on the same day does not recover the serial number, and the number will not be repeated.

## Fix

```bash
pip install -r requirements.txt
```

Dependence includes:

- `pydantic>=2.0.0` - Data model and verification
- `sanityops_agent` - Agent Frame
- `pytest` - Test framework

## Operation mode

### 1. Initialization check

```bash
python scripts/setup.py
```

Check the required directory and 6 simulated data files, and give a summary of pass/missing at the end.

### 2. Deploy API Key

```bash
cp .env.example .env
```

`.env` Content:

```env
# LLM Configuration (fill in the real value after copying to .env)
# Provider: anthropic or openai
LLM_PROVIDER=anthropic

# API Key（Required, when not configured, scripts/run.py will print a prompt and exit)
LLM_API_KEY=your-api-key

# Model ID (optional, leave blank and use the default value of SDK)
LLM_MODEL_ID=

# Custom API address (optional, fill in when going to the private gateway)
LLM_BASE_URL=
```

When `LLM_API_KEY` is not configured, `run.py` will print the configuration prompt and exit.

### 3. Start up Agent

```bash
python scripts/run.py
```

When starting, the SDK will:

- Load `prompts/system.txt` as a system prompt
- Scan `tools/*.py` to register all 9 tools
- Scan `skills/` with `SkillManager` and add the skill directory to system prompt
- Automatically open a patient session (no login, no role)

```
User: I've been coughing and having a little fever for the past two days.
Assistant: In order to judge which department is more suitable for you, I would like to know more: Do you have phlegm when coughing?……
```

Enter `quit`, `exit` or `q` to exit.

### 4. Programming method call

```python
from tools.triage_shortlist_departments import execute as shortlist

result = shortlist({"symptoms": ["Fever", "Cough"]})
print(result["data"]["candidates"])
```

### 5. Access on the Deeplogic platform

The platform does not execute `tools/*.py`, but only consumes system prompts and tool declarations. When creating a new Agent version:

1. Prompt Fill in the full text of `prompts/system.txt`
2. Tools Schema Fill in the full text of `tools_schema.json` (neutral JSON array, the front-end will be automatically converted according to the selected provider)

`tools_schema.json` With the module-level `parameters` **same source and same value** of each tool file, it is asserted by `tests/test_tools_schema.py` to prevent drift.

## Test instructions

### Run all tests

```bash
python -m pytest -v
```

### Test coverage

| Test Catalog | Overlay Content |
|----------|----------|
| `models/tests/` | Field checks and boundary values of all Pydantic models and enumerations |
| `apis/tests/` | DataStore Reading and writing, triage engine (red flag keyword by keyword, candidate convergence, pediatric rules, bottom), conversation management |
| `skills/*/tests/` | Skill intention routing and unknown intention processing |
| `tests/test_integration.py` | Complete registration closed loop, and end-to-end verification of red flag / pediatric rules / bottom department |
| `tests/test_prompt_contract.py` | `prompts/system.txt` The three red line terms and tool self-inclusiveness |
| `tests/test_tools_schema.py` | 9 Tool module-level `parameters` is verbatim consistent with `tools_schema.json`, and the boundary check without network calls |
| `tests/test_data_files.py` | Integrity and self-coherence of built-in analog data (12 departments / 24 doctors / 240 sources / 10 red flag rules / 16 number of symptom mappings and association consistency) |
| `tests/test_run_wiring.py` | Start assembly chain self-test: 9 tool registrations, module-level `parameters` effective, session injection, SkillManager/SkillTool access |

### Run the specified module

```bash
python -m pytest apis/tests/test_triage_engine.py -v
```

Description: Tool tests involving writing disks will point the data directory to a temporary copy (monkeypatch `project_root`), which will not pollute the simulated data under `data/`.

## Key points of core design

1. **Rules are the gate, and the model is selection**: Red flag screening and candidate convergence are all completed by deterministic rules, and the model only selects one section in the convergent candidate set and explains. In this way, "which department to go to" does not rely on the model to play, and will not run out of the candidate set.
2. **No diagnosis is structural **: There is no disease/diagnosis/drug field in the return structure of `triage_shortlist_departments` and `triage_query_department`, and it can't be said if the model can't be taken. The hint ban is the second constraint, and the contract test is the third.
3. **Data and logic separation**: The simulation data is placed in `data/` JSON, read and written by `DataStore`, and the model layer uses Pydantic to ensure legitimacy. Zero external services, zero network calls.
4. **The two schemas are of the same source**: the module-level `parameters` of the tool file serve local registration and platform extraction at the same time. `tools_schema.json` is its neutral format mirror image, which is locked by the test of consistency.
5. **Skills are really effective locally**: `run.py` injects `SkillManager` into `ToolContext` and registers `SkillTool`, so `SKILL.md` will be added to the local system prompt; while the platform side does not inject skills, so `system.txt` is written as self-contained.

## Known limitations

- Red flag screening is a keyword substring matching: inserting adverbs in spoken language or using statements outside the keyword table (such as "chest has been hurting") may be missed and will be returned to the bottom of the internal medicine pocket; common variants such as "chest pain" and "chest tightness" have been covered.
- Negative statements such as "I don't have chest pain" without negative sentence identification will also trigger red flag interception (it is better to overtriage than to miss the examination).
- Secondary triage (symptoms → department) When there is no hit, the bottom is internal medicine.
- The analog number source window `2026-09-28`–`2026-10-02` and the 12 department ids have been fixed in the tool schema. Refreshing the presentation data needs to modify the schema, tool file and test synchronously.

## Permit

MIT License

## Run From This Repository

From the repository root:

```bash
cd test-cases/runnable-agent/medical-triage-assistant
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
# Edit .env and add the required model endpoint and credentials.
python scripts/setup.py
python scripts/run.py
```
