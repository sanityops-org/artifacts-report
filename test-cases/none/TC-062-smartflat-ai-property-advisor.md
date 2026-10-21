# TC-062: SmartFlat AI - HDB Property Advisor (Agent Base & Data Tool)

## Metadata
- **Source Project**: smartflat-ai (seehiong/smartflat-ai)
- **GitHub**: github.com/seehiong/smartflat-ai
- **License**: MIT
- **Artifact Type**: Singapore HDB property/home advisor — multi-agent base class + domain data tools
- **Collection Date**: 2026-10-13
- **Collection Method**: GitHub raw-content fetch on branch `main` — `https://raw.githubusercontent.com/seehiong/smartflat-ai/main/agent/agents/base_agent.py` and `https://raw.githubusercontent.com/seehiong/smartflat-ai/main/agent/tools/data_commons_tool.py`; project overview cross-checked against `https://raw.githubusercontent.com/seehiong/smartflat-ai/main/README.md` (which describes the project as "HDB Multi-Agent Advisor")
- **Scope**: The advisor-agent base contract (`BaseAgent`) and one concrete domain tool (`DataCommonsTool` / `get_singapore_statistics`) that grounds property answers in official Singapore statistics

---

## Project Overview

SmartFlat AI (documented in-repo as the "HDB Multi-Agent Advisor") is a phased **multi-agent property-advisory system** for Singapore HDB flats, built on AWS Bedrock AgentCore and the official AWS supervisor-agent pattern. Its purpose is to advise a home-seeker on HDB flats — searching real resale transactions, computing price statistics and trends, and answering demographic questions — rather than to write code.

### Key Characteristics
- **Supervisor + specialists**: an AgentCore supervisor (Amazon Nova Lite) routes each query to the Demographics Agent, the Property Agent, or the PostgreSQL Agent
- **Dual data sources**: the same HDB resale data is available via PostgreSQL (fast, cost-optimized) and Athena (complex analytics)
- **Domain tools**: e.g. Data Commons integration for live Singapore government statistics
- **Self-contained agents**: "No complex imports or inheritance - each agent is self-contained"
- **Memory-first**: AgentCore Memory for conversation history and user preferences
- **Example advisor queries**: *"Find 4-room flat in Bishan under $600k"*, *"Average HDB prices in Tampines?"*, *"Singapore population breakdown"*

---

## Agent Prompts

### 1. Agent Base Class (`agent/agents/base_agent.py`)

Every specialised advisor agent derives from a single abstract base that fixes the shared contract — a name, a description, a tool list, an async `execute`, a capability list, and a default system prompt:

```python
# agent/agents/base_agent.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseAgent(ABC):
    """Base class for all specialized agents"""
    
    def __init__(self, name: str, description: str, tools: List[Any] = None):
        self.name = name
        self.description = description
        self.tools = tools or []
    
    @abstractmethod
    async def execute(self, query: str, context: Dict = None) -> Dict:
        """Execute agent's main task"""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Return list of what this agent can do"""
        pass
    
    def get_system_prompt(self) -> str:
        """Return agent-specific system prompt"""
        return f"You are the {self.name}. {self.description}"
```

**Observations on the prompt layer:**
- Each agent is identified by a **name** and a one-sentence **description**, and the default system prompt is the composition of the two (`"You are the {name}. {description}"`). Concrete agents override `get_system_prompt` for richer instructions.
- The **tools** list is injected at construction time, so routing the right tool set to each specialist is a caller responsibility — consistent with the supervisor's job.
- `execute` is **async** and takes a `query` plus an optional `context` dict (conversation/memory), returning a dict result; this is what lets the supervisor fan out to specialists within one turn.
- `get_capabilities` forces every agent to declare its scope in plain language, which supports the router's routing decision.

### 2. Data Commons Tool (`agent/tools/data_commons_tool.py`)

The demographics capability is packaged as a `strands` `@tool` that queries the Data Commons API for Singapore statistics. The tool wrapper keeps a name and description, and the decorated function is the model-callable surface:

```python
"""
Data Commons Tool - Singapore Statistics Integration
Extracted from the proven Phase 1 implementation
"""
import os
from strands import tool

class DataCommonsTool:
    """Data Commons API integration for Singapore statistics"""
    
    def __init__(self):
        self.name = "Data Commons Tool"
        self.description = "Singapore demographics and statistics via Data Commons API"
    
    def get_statistics(self, query: str) -> str:
        """Get Singapore statistics from Data Commons API"""
        return get_singapore_statistics(query)

@tool
def get_singapore_statistics(query: str) -> str:
    """
    Get Singapore demographic and housing statistics from Data Commons API.
    
    Args:
        query: What statistics to retrieve (e.g., "population", "housing", "demographics")
    
    Returns:
        Relevant Singapore statistics from official data sources
    """
```

The tool degrades explicitly when its dependency or data is missing — it never silently fabricates a number:

```python
    try:
        import datacommons as dc
        
        # Set API key if available
        api_key = os.getenv("DATA_COMMONS_API_KEY")
        if api_key:
            dc.set_api_key(api_key)
        
        dc_available = True
    except ImportError:
        dc_available = False
    
    if not dc_available:
        return f"TOOL_UNAVAILABLE: Data Commons API not available. Query was: {query}"
```

Intent routing is keyword-based against the query, pinned to the Singapore country DCID:

```python
        query_lower = query.lower()
        singapore_dcid = "country/SGP"
        
        if "population" in query_lower:
            total_pop = dc.get_stat_value(singapore_dcid, "Count_Person")
            
            result = "Singapore Population (Data Commons API):\n"
            if total_pop and str(total_pop) != 'nan':
                result += f"• Total Population: {int(total_pop):,} people\n"
                ...
                return result + "\nSource: Data Commons (official government data)"
```

It supports three query families — `population`, `housing`/`hdb`, and `demographics`/`age`/`ethnic` — and returns a typed error string for anything else or on any exception:

```python
        else:
            return f"TOOL_ERROR: Unsupported statistics query. Supported queries: population, housing, demographics. Query was: {query}"
    
    except Exception as e:
        return f"TOOL_ERROR: Data Commons API error - {str(e)}. Query was: {query}"
```

---

## Skill Definitions

This project packages its advisor capabilities as **agents + tools** rather than SKILL.md manifests, so the closest analogue to a skill entry here is the tool contract and the agent's declared capabilities.

### 1. Data-Commons Tool Contract

| Property | Value |
|-------|-------------|
| Tool name | `Data Commons Tool` |
| Model-facing function | `get_singapore_statistics(query: str) -> str` |
| Description | "Singapore demographics and statistics via Data Commons API" |
| Supported queries | `population`, `housing` / `hdb`, `demographics` / `age` / `ethnic` |
| Data source | Data Commons (official government data); country DCID `country/SGP` |
| Auth | Optional `DATA_COMMONS_API_KEY` environment variable |
| Failure modes | `TOOL_UNAVAILABLE:` (dependency missing), `TOOL_ERROR:` (bad query / API error) |

### 2. Agent Capability Surface (per README)

| Agent | Responsibility | Primary data source |
|-------|-------------|-------------|
| Supervisor Agent | Intelligent query routing (Amazon Nova Lite) | — |
| Demographics Agent | Singapore population/statistics | Data Commons API |
| Property Agent | Complex HDB analytics | Athena + S3 |
| PostgreSQL Agent | Cost-optimized HDB queries | RDS Proxy + PostgreSQL |

---

## Evaluation Dimensions

### 1. Agent Contract Clarity
- [ ] Abstract base defines name/description/tools/execute/capabilities
- [ ] `execute` signature supports async, context-aware, dict-returning runs
- [ ] Default system prompt derives from name + description; overridable

### 2. Tool Grounding & Honesty
- [ ] Every stated figure originates from a real data source (no invention)
- [ ] Missing dependency is surfaced as `TOOL_UNAVAILABLE`, not a guess
- [ ] Unsupported queries return a typed, user-readable error

### 3. Routing & Specialisation
- [ ] Agents are self-contained with clear, non-overlapping scopes
- [ ] Capabilities are declarative, supporting the supervisor's routing
- [ ] Domain tools map cleanly to the agent that owns them

### 4. Extensibility
- [ ] New agents can subclass `BaseAgent` without touching others
- [ ] New tools follow the same `@tool` wrapper + name/description pattern
- [ ] Configuration (API keys) is via environment, not hard-coded

### 5. Safety & Cost Awareness
- [ ] Secrets are read from the environment, never inlined
- [ ] Cost-optimal data source is chosen per query complexity
- [ ] Context/memory is threaded explicitly through `execute`

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Agent Contract Clarity | 25% | | |
| Tool Grounding & Honesty | 25% | | |
| Routing & Specialisation | 20% | | |
| Extensibility | 15% | | |
| Safety & Cost Awareness | 15% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### Agent Contract Tests
1. Instantiate a subclass and confirm `get_system_prompt()` returns `"You are the {name}. {description}"`
2. Verify `execute` is genuinely async and returns a dict for a sample query
3. Confirm `get_capabilities()` is implemented for each specialist

### Tool Behaviour Tests
1. Uninstall the `datacommons` package and confirm the tool returns `TOOL_UNAVAILABLE: …`
2. Query `"population"` / `"housing"` / `"demographics"` and confirm the correct DCID and stat props are used
3. Query an unsupported term and confirm the `TOOL_ERROR: Unsupported statistics query …` message
4. Force an API exception and confirm `TOOL_ERROR: Data Commons API error …` (no crash, no fabricated value)

### Routing Tests
1. Feed a demographics query and confirm the Supervisor routes to the Demographics Agent
2. Feed a simple price query and confirm cost-optimized routing to PostgreSQL; feed a complex analytics query and confirm Athena routing
3. Verify a query is never answered without a data source

---

## Notes

- **MIT license** permits full quotation and modification.
- SmartFlat AI is a **property/home advisor**, a non-coding agent: its artifacts concern HDB flats, Singapore statistics and cost-aware data routing.
- The `BaseAgent` is a compact example of a **supervisor-compatible specialist contract** (async execute + declarative capabilities).
- `get_singapore_statistics` is a good example of **grounded answers**: real government data, explicit `TOOL_UNAVAILABLE` / `TOOL_ERROR` states, and no invented numbers.
- Only `base_agent.py` and `data_commons_tool.py` were quoted; the concrete `demographics_agent.py`, `property_agent.py`, `postgres_agent.py` and supervisor were referenced from the README but not quoted.
