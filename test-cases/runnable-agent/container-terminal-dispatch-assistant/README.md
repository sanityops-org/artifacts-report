# Container terminal dispatch assistant

## Project information

| Project | Description |
|------|------|
| **Industry ** | Port / Logistics (Container Terminal Operation) |
| **Project Name** | Container Terminal Dispatch Assistant |
| **Edition** | v1.0.0 |
| **Date of creation** | 2026-09-14 |
| **Author** | Agent Artifacts Team |
| **Technical stack** | Python 3.11+、Pydantic 2.0+、sanityops_agent |
| **Permit** | MIT License |

## Brief account

Container Terminal Dispatch Assistant is an intelligent dispatching Agent for port container terminal operation scenarios. It covers the four dispatching areas of **berths, storage, equipment and gates**. It supports multi-role users (dispatchers in various fields, operation supervisors, dock managers), provides information query and dispatching instruction issuing capabilities, and forms a complete operation closed loop of "instruction → verification → execution → status change → feedback event" through the built-in execution simulator.

## Function description

### Four major scheduling fields

| Field | Function |
|------|------|
| **Berth scheduling** | Ship arrival plan inquiry, berth occupancy status inquiry, anchorage ship inquiry, berth allocation, berth plan adjustment, departure confirmation |
| **Dyard scheduling** | Box area status inquiry, container location inquiry, box turning task inquiry, box location allocation, box turning task creation, container location update |
| **Equipment dispatch** | Shore bridge/field bridge/card collection and other equipment status inquiry, equipment task inquiry, equipment dispatch, equipment status update, task cancellation |
| **Gate dispatch** | Gate channel status inquiry, port entry appointment inquiry, queue status inquiry, channel opening/closing, card collection entry and exit processing |

### Execute closed loop

```
User instructions → Risk control verification → Issuing instructions → Simulated execution → Status change → Feedback event → Follow-up suggestions
```

### Risk control verification

All instructions are checked by risk control before execution to prevent illegal or dangerous operations:

| Check Type | Trigger Scene | Check Content |
|----------|----------|----------|
| The equipment is idle | Dispatch instructions | The equipment status is idle |
| Berth available | Berth allocation | Berth status is available and the ship type matches |
| Storage capacity | Allocation of box space | Box area is not fully loaded |
| The appointment is valid | entry processing | The appointment status is valid and within the time window |
| The ship has been moored | Loading and unloading operation | The ship's status is berthed |

## List of skills

The system contains 4 field skills (Skill), each skill provides two types of operations: query tools and instruction tools, which are executed through the unified entrance `run(intent, params)` route:

### 1. berth_scheduling（Berth scheduling skills)

Manage the ship's docking plan and berth resources.

| Tools | Type | Description |
|------|------|------|
| `query_vessel_plan` | Query | Query the ship's arrival plan and status, support filtering by ship ID |
| `query_berth_status` | Query | Query berth occupancy and available status, support filtering by status/berth ID |
| `query_anchorage` | Query | Query the list of ships waiting for anchorage |
| `assign_berth` | Instruction | Allocate berths for anchored ships (check the availability of berths to match the ship type) |
| `update_berth_plan` | Instructions | Adjust the mooring plan of the ship |
| `confirm_departure` | Instruction | Confirm the ship's departure and release the berth |

### 2. yard_scheduling（Stacking field scheduling skills)

Manage the resources of the storage box area and the operation of turning boxes.

| Tools | Type | Description |
|------|------|------|
| `query_yard_status` | Query | Query the capacity of the box area, the occupancy, and the available box space, and support filtering by box area ID/box type |
| `query_container_location` | Query | Query the container location, support filtering by box number/box area |
| `query_rehandle_list` | Query | Query the list of pending box-turning tasks |
| `assign_yard_slot` | Instruction | Assign the landing location for the container (check the capacity, status and box type matching of the container area) |
| `create_rehandle_task` | Instruction | Create a box-turning task, which can specify the target box area or automatically select |
| `update_container_location` | INSTRUCTIONS | UPDATE THE POSITION OF THE CONTAINER IN THE STORE (SHELL POSITION/ROW/LAYER) |

### 3. equipment_scheduling（Equipment scheduling skills)

Manage the dispatch and dispatch of quay_crane, rtg/rmg, yard_truck and other equipment.

| Tools | Type | Description |
|------|------|------|
| `query_equipment_status` | Query | Query device status, support filtering by device ID/type/status |
| `query_equipment_task` | Query | Query device tasks, support filtering by device ID/task ID/task status |
| `dispatch_equipment` | Instruction | Dispatch, assign tasks to the equipment (check that the equipment must be idle) |
| `update_equipment_status` | Instructions | Update device status (working/moving/fault, etc.) |
| `cancel_task` | Instruction | Cancel the task and release the associated device |

### 4. gate_scheduling（Gate dispatching skills)

Manage the gate passage and the collection card entry and exit operation.

| Tools | Type | Description |
|------|------|------|
| `query_gate_status` | Query | Query the status of the gate channel, support filtering by channel ID/type/status |
| `query_gate_appointment` | Query | Query the reservation record of card entry, support filtering by appointment ID/card ID/status |
| `query_gate_queue` | Query | Query the total number of queues at the gate and the queues of each channel |
| `open_gate_channel` | INSTRUCTION | OPEN THE DESIGNATED GATE CHANNEL |
| `close_gate_channel` | Instruction | Close the designated gate channel (the reason for closing can be attached) |
| `process_gate_pass` | Instructions | Process the entry and exit of the card (check the reservation status and time window) |

## Roles and permissions

The system realizes login and session management through the TOS simulation interface (`apis/tos_api.py`), and controls the accessible domains and command permissions by role:

| Role | Operable Area | Instruction Permission |
|------|------------|----------|
| Berth Dispatcher | Berth Dispatcher (Query + Instruction) | Yes |
| Field Dispatcher | Field Dispatch (Query + Instruction) | Yes |
| Equipment Dispatcher | Equipment Dispatch (Query + Instruction) | Yes |
| Gate Dispatcher | Gate Dispatcher (Query + Instruction) | Yes |
| Operation Supervisor | All fields (query + instructions + approval of high-risk operations) | Yes |
| Dock Manager | All Fields (Query Only) | None |

### Identity transmission mechanism

When starting Agent, users need to select the login role. Session information is transmitted to each tool through `ToolContext`:

1. **Log in at startup**: `run.py` Call `select_role()` to let the user select the role and generate a session
2. **Context Injection**: Session deposit `ToolContext.set("session", session_data)`
3. **Tool acquisition**: Get the session from `self.context.get("session")` when the tool is executed
4. **Permission check**: `tools/_permission.py` provides `check_tool_permission()` for instruction tools to call

```python
# Get the session example in the tool
session = params.get("_session")  # Automatically injected by run.py
if session:
    role = session.get("role")
    permissions = session.get("permissions")
```

## Project structure

```
Container terminal dispatch assistant/
├── README.md              # Project description (this document)
├── requirements.txt       # Dependent package
├── prompts/               # System prompts
│   └── system.txt         # Agent System prompts
├── models/                # Pydantic Data model
│   ├── enums.py           # Enumeration definition (ship/berth/box area/equipment/task/appointment status, etc.)
│   ├── vessel.py          # Ship, berth model
│   ├── yard.py            # Box area, container model
│   ├── equipment.py       # Equipment and task model
│   ├── gate.py            # Gate passage, reservation model
│   └── execution.py       # Execution record, event model
├── apis/                  # Public system interface
│   ├── data_store.py      # Data persistence (JSON reading and writing)
│   └── tos_api.py         # TOS Simulated interface (login, session, permission verification)
├── data/                  # Simulated data
│   ├── vessels.json       # Ship data
│   ├── berths.json        # Parking data
│   ├── containers.json    # Container data
│   ├── yard_blocks.json   # Data of the storage box area
│   ├── equipment.json     # Device data
│   ├── tasks.json         # Task data
│   ├── gate_channels.json # Gate channel data
│   └── appointments.json  # Reservation data for entering Hong Kong
├── tools/                 # Executable tool (SDK automatic scanning registration)
│   ├── berth_*.py         # Parking scheduling tools (6)
│   ├── yard_*.py          # Stacking site scheduling tools (6)
│   ├── equipment_*.py     # Equipment scheduling tools (5)
│   └── gate_*.py          # Gate dispatching tools (6)
├── simulator/             # Execution simulator
│   ├── executor.py        # Main actuator (loading Skill handler, routing execution request)
│   ├── event_bus.py       # Event bus (feedback event release)
│   └── time_controller.py # Simulated time control
├── skills/                # Skill definition (Agent reads by himself when running)
│   ├── berth_scheduling/  # Parking scheduling SKILL.md
│   ├── yard_scheduling/   # Field dispatch SKILL.md
│   ├── equipment_scheduling/  # Equipment scheduling SKILL.md
│   └── gate_scheduling/   # Gate dispatch SKILL.md
├── scripts/               # Run the script
│   ├── run.py             # Agent Start the script（sanityops_agent SDK）
│   └── setup.py           # Initialize the check script
└── tests/                 # Integrated test
    └── test_integration.py
```

## Data model

All data models are defined in Pydantic, including enumeration constraints and numerical range checks:

- **Ship model**: `Vessel` - Ship ID, ship name, ship type, size, status, etc.
- **Berth model**: `Berth` - Berth ID, length, water limit, status, etc.
- **Yard model**: `YardBlock` - Box area ID, capacity, occupancy rate, status, etc.
- **Container model**: `Container` - box number, size, type, location, etc.
- **Equipment model**: `Equipment` - Equipment ID, type, status, efficiency, etc.
- **Task model**: `Task` - Task ID, type, status, associated resources, etc.
- **Gate Model**: `GateChannel`, `Appointment` - Gate Channel and Port Reservation Management
- **Execution model**: execution record, feedback event, etc.

## Fix

```bash
# Installation dependency
pip install -r requirements.txt
```

Dependence includes:

- `pydantic>=2.0.0` - Data model and verification
- `sanityops_agent` - Agent Frame

## Operation mode

### 1. Initialization check

Before running for the first time, check whether the directory structure and data file are complete:

```bash
python scripts/setup.py
```

The script will check the required directories (data, models, skills, simulator, prompts, apis, tools, etc.) and 8 simulation data files, and prompt the check to pass when all of them are ready.

### 2. Deploy API Key

Agent LLM API is required to run. Support two configuration methods:

**Method 1: Use the .env file (recommended)**

```bash
# Copy the sample configuration file
cp .env.example .env

# Edit the .env file and fill in the actual API Key
```

`.env` Example of file content:

```env
# LLM Provider Deploy
LLM_PROVIDER=anthropic  # Someone openai
LLM_API_KEY=your-api-key
LLM_MODEL_ID=claude-sonnet-5-20250514  # Selectable

# Custom Base URL (optional, for proxy or private deployment)
# LLM_BASE_URL=https://api.anthropic.com
```

**Method 2: Use environment variables**

```bash
export LLM_PROVIDER=anthropic
export LLM_API_KEY=your-api-key
export LLM_MODEL_ID=claude-sonnet-5-20250514  # Selectable
```

### 3. Start up Agent

Use sanityops_agent SDK to start the scheduling assistant:

```bash
python scripts/run.py
```

SDK Automatically:
- Load `prompts/system.txt` as a system prompt
- Scan `tools/*.py` to register all tools (23 in total)
- Create an Agent instance and enter the interaction mode

After starting, enter the question to talk to the Agent:

```
User: Check which ships are in the current anchorage?
Assistant: At present, there are 3 ships waiting for anchorage....
```

Enter `quit` or `exit` to exit the program.

### 4. Programming method call

The tool function can be called directly:

```python
from tools import berth_query_vessel_plan, equipment_dispatch

# Query all ships
result = berth_query_vessel_plan({})
print(result)

# Dispatch
result = equipment_dispatch({"equip_id": "QC01", "task_type": "load"})
```

## Test instructions

### Run all tests

```bash
# Run in the root directory of the project
python -m pytest -v
```

### Test coverage

The current test suite has a total of **310** use cases, all of which have passed, covering:

| Test Catalog | Cover Content | Number of Use Cases |
|----------|----------|--------|
| `models/tests/` | All Pydantic data models and enumeration definitions | 117 |
| `apis/tests/` | DataStore Data persistence, TOS login and permissions | 26 |
| `simulator/tests/` | Time controller, event bus, execution simulator | 20 |
| `skills/berth_scheduling/` | Parking space scheduling handler and query/instruction tool | 36 |
| `skills/yard_scheduling/` | Stacking scheduling handler and query/instruction tool | 23 |
| `skills/equipment_scheduling/` | Device scheduling handler and query/instruction tool | 32 |
| `skills/gate_scheduling/` | Gate scheduling handler and query/instruction tool | 22 |
| `tests/` | Full-skill integrated testing and execution closed-loop | 34 |
| **Amount to** | | **310** |

### Run the test of the specified module

```bash
# Only run the model test
python -m pytest models/tests -v

# Only run the berth scheduling skill test
python -m pytest skills/berth_scheduling -v

# Only run the integration test
python -m pytest tests/test_integration.py -v
```

Description: Some instruction tests will reset the simulation data file under `data/` (the initial data will be restored before and after the test) to ensure that the test can be repeated.

## Key points of core design

1. **Skilled architecture**: Each scheduling field is encapsulated as an independent Skill, including `SKILL.md` (skill description), `handler.py` (unified entrance routing), `tools/` (specific tool implementation), which is convenient for expanding new fields.
2. **Data and logic separation**: All simulation data is stored in the `data/` JSON file, read and written through `DataStore`, and the model layer uses Pydantic to ensure the legitimacy of the data.
3. **Built-in permissions**: TOS simulation interface provides login, session and role permission verification, and the command operation requires the role to have the corresponding domain permissions and instruction permissions.
4. **Closed-loop simulation**: The simulator updates the data status after the instruction is executed, and generates feedback events through the event bus to support the complete interaction of "query-instruction-feedback".

## Permit

MIT License

## Run From This Repository

From the repository root:

```bash
cd test-cases/runnable-agent/container-terminal-dispatch-assistant
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
# Edit .env and add the required model endpoint and credentials.
python scripts/setup.py
python scripts/run.py
```
