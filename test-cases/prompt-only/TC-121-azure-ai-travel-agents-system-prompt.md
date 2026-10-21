# TC-121: Azure AI Travel Agents - System Prompt Evaluation Case

## Metadata
- **Source Project**: Azure-Samples/azure-ai-travel-agents
- **License**: MIT (Azure-Samples default; see repo `LICENSE`)
- **Artifact Type**: System Prompt (Multi-agent travel planning - per-agent `instructions`)
- **Collection Date**: 2026-10-13
- **Collection Method**: Retrieved verbatim from the raw source files on the `main` branch:
  `https://raw.githubusercontent.com/Azure-Samples/azure-ai-travel-agents/main/packages/api-maf-python/src/orchestrator/agents/customer_query_agent/__init__.py`
  `https://raw.githubusercontent.com/Azure-Samples/azure-ai-travel-agents/main/packages/api-maf-python/src/orchestrator/agents/itinerary_planning_agent/__init__.py`
  Repository layout confirmed via the repo `llms.txt` and `https://github.com/Azure-Samples/azure-ai-travel-agents`. Agent prompts are passed as the `instructions=` argument of a Microsoft Agent Framework `ChatAgent`.

## Original Artifact Content

Each agent defines its system prompt inline as `instructions=`. Two are quoted below (the repo also ships a `destination_recommendation_agent`, a `triage_agent`, and an `echo_agent` in the same directory).

### Agent: `CustomerQueryAgent` (`.../customer_query_agent/__init__.py`)

```python
agent = ChatAgent(
    name="CustomerQueryAgent",
    description="Analyzes customer travel preferences and requirements",
    instructions="""You are a customer service agent for a travel planning system.
Your role is to understand and analyze customer travel preferences, requirements, and constraints.
Key responsibilities:
- Extract travel preferences (destinations, activities, accommodations)
- Identify budget constraints
- Understand time constraints and travel dates
- Clarify any ambiguous requirements
- Provide personalized recommendations
Always be empathetic, patient, and thorough in understanding customer needs.""",
    chat_client=AzureOpenAIChatClient(
        api_key=os.environ.get("AZURE_OPENAI_API_KEY", ""),
    ),
    tools=[create_mcp_tool(["CustomerQueryAgent"])],
)
```

### Agent: `ItineraryPlanningAgent` (`.../itinerary_planning_agent/__init__.py`)

```python
agent = ChatAgent(
    name="ItineraryPlanningAgent",
    description="Creates detailed travel itineraries",
    instructions="""You are an itinerary planning expert for a travel planning system.
Your role is to create detailed, optimized travel itineraries.
Key responsibilities:
- Create day-by-day itineraries
- Optimize travel routes and timing
- Schedule activities and experiences
- Estimate costs and budgets
- Account for travel time and logistics
- Use available tools for planning assistance
Be detail-oriented, practical, and create realistic, enjoyable itineraries.""",
    chat_client=AzureOpenAIChatClient(
        api_key=os.environ.get("AZURE_OPENAI_API_KEY", ""),
    ),
    tools=[create_mcp_tool(["ItineraryPlanningAgent"])],
)
```

## Evaluation Dimensions

### 1. Instruction Clarity
- [ ] Each agent has a single, well-scoped role (preference analysis vs. itinerary construction)
- [ ] Responsibilities are enumerated as concrete bullet items
- [ ] Tool delegation is explicit (each agent declares its MCP tool set)

### 2. Role Separation (Multi-Agent Design)
- [ ] Overlap between agents is low; each owns a distinct sub-task
- [ ] `description` fields are usable by an orchestrator for routing
- [ ] A `triage_agent` exists to coordinate the flow

### 3. Tone & Behavioral Guidance
- [ ] Interpersonal guidance is present ("empathetic, patient, thorough")
- [ ] Output-quality guidance is present ("realistic, enjoyable", "detail-oriented, practical")
- [ ] Ambiguity handling ("clarify any ambiguous requirements") is instructed

### 4. Coverage
- [ ] Budget, dates, and activity preferences are all captured by at least one agent
- [ ] Cost estimation and logistics are assigned
- [ ] Personalization is requested

### 5. Testability
- [ ] Each prompt is short and static, enabling exact-snapshot regression tests
- [ ] Prompt/response pairing is inspectable per agent in traces (OpenTelemetry instrumentation)
- [ ] MCP-tool wiring per agent is verifiable

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Instruction Clarity | 25% | | |
| Role Separation (Multi-Agent Design) | 25% | | |
| Tone & Behavioral Guidance | 15% | | |
| Coverage | 20% | | |
| Testability | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Send a vague request ("plan a 7-day trip to Japan"); verify `CustomerQueryAgent` extracts preferences before planning
2. Send a fully specified request; verify `ItineraryPlanningAgent` produces a day-by-day itinerary with cost estimates
3. Verify the orchestrator routes to the correct agent for each sub-task

### Boundary Test Cases
1. A request with contradictory constraints (budget vs. dates); verify clarification is sought
2. A request with zero preference detail; verify the agent asks targeted questions
3. Verify each agent only calls the MCP tools it declares

### Negative Test Cases
1. Verify the agent does not fabricate availability/pricing not returned by the tools
2. Verify the agent stays within its role and does not perform another agent's job
3. Verify the agent does not expose internal orchestration details to the end user

## Notes
- This is a "modular reference application"; the same prompts are wired across three orchestrators (LangChain.js, LlamaIndex.TS, Microsoft Agent Framework). The version quoted here is the Python MAF implementation.
- Prompts are intentionally terse one-liners plus bullet lists; they are the clearest example in this batch of "thin" per-agent prompts embedded directly in agent-construction code.
- Other agents (`destination_recommendation_agent`, `triage_agent`, `echo_agent`) live in the same `agents/` directory and were not fetched; if a full-suite case is desired, retrieve them from the same path pattern. Layout note: the repo `llms.txt` packs only `packages/` and `infra/`, so agent prompts must be read from the individual `__init__.py` files.
- MIT license permits full quotation and modification. Layout/ownership: verify the `LICENSE` file at repo root (`main`) if a stricter legal read is required.
