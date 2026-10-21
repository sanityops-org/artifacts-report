# TC-054: Foundry Hosted Agents Workshop Travel-Assistant Skill - Skill Evaluation Case

## Metadata
- **Source Project**: Azure-Samples/foundry-hosted-agents-workshop
- **License**: MIT
- **Artifact Type**: Skill (SKILL.md) + Agent tool definition (agent.yaml)
- **Collection Date**: 2026-10-13
- **Collection Method**: Fetched from `raw.githubusercontent.com`, branch `main`:
  - `.workshop/solutions/06-skills/travel_assistant/skills/travel-guide/SKILL.md`
  - `.workshop/solutions/06-skills/travel_assistant/agent.yaml`

## Original Artifact Content

### 1. `.../travel_assistant/skills/travel-guide/SKILL.md` (fetched)

```markdown
---
name: travel-guide
description: Creates a colorful, downloadable PDF travel guide that bundles a day-by-day itinerary, local highlights, and practical tips for a destination, grounded in the destinations index. Use when the traveler wants a shareable trip guide, a day-by-day plan, or a printable trip outline.
---
# Travel guide skill
Use this skill when the traveler wants a downloadable, shareable trip guide or a
day-by-day itinerary. It renders a multi-page PDF that combines a cover, grounded
local notes, a day-by-day itinerary, and practical tips.
## Workflow
1. Identify the destination city, trip length, interests, and tone/audience.
2. Prefer retrieved destination knowledge from the destinations index. Summarize the
   most relevant retrieved facts and pass them as `source_summary` so the right city
   context is rendered into the guide.
3. If the user did not specify a trip length, use `3` days (maximum `7`).
4. Run the travel-guide script:
   - skill name: `travel-guide`
   - script name: `scripts/create_travel_guide.py`
   - args: a JSON array of string CLI flags and their values. Supported flags:
     - `--city <city>`: destination city, required
     - `--days <number>`: number of itinerary days (1-7), optional, defaults to `3`
     - `--interests <list>`: comma-separated interests, optional
     - `--tone <style>`: guide style or audience, optional
     - `--source-summary <text>`: concise summary of retrieved destination facts to ground the guide, optional
5. After the script returns JSON, tell the traveler the guide was created, share the
   `path`, and summarize what is inside.
## Output contract
The script returns JSON with `city`, `days`, `interests`, `pages`, `path`, `grounded`,
and `message`.
## Available scripts
`scripts/create_travel_guide.py` - Generates a colorful PDF travel guide and returns a JSON with the saved file path.
## Attribution
`scripts/create_travel_guide.py` is adapted from the Microsoft Foundry samples
`07-skills` travel-guide sample and is used under the MIT License
(Copyright (c) 2025 Microsoft Corporation). See the license header in the script.
## Example script arguments
```json
["--city", "Lisbon", "--days", "4", "--interests", "food,viewpoints,history,neighborhoods", "--tone", "first-time visitors who like walking", "--source-summary", "The index highlights Alfama, Belem, miradouros, seafood, and day trips to Sintra."]
```
```

### 2. `.../travel_assistant/agent.yaml` (fetched)

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/microsoft/AgentSchema/refs/heads/main/schemas/v1.0/ContainerAgent.yaml
kind: hosted
name: ${WORKSHOP_RESOURCE_PREFIX}-travel-buddy
protocols:
  - protocol: responses
    version: 2.0.0
resources:
  cpu: "0.25"
  memory: "0.5Gi"
environment_variables:
  - name: AZURE_AI_PROJECT_ENDPOINT
    value: ${AZURE_AI_PROJECT_ENDPOINT}
  - name: AZURE_AI_MODEL_DEPLOYMENT_NAME
    value: ${AZURE_AI_MODEL_DEPLOYMENT_NAME}
  - name: WORKSHOP_RESOURCE_PREFIX
    value: ${WORKSHOP_RESOURCE_PREFIX}
  - name: TOOLBOX_ENDPOINT
    value: ${TOOLBOX_ENDPOINT}
  - name: AZURE_AI_SEARCH_ENDPOINT
    value: ${AZURE_AI_SEARCH_ENDPOINT}
  - name: AZURE_AI_SEARCH_INDEX_NAME
    value: ${AZURE_AI_SEARCH_INDEX_NAME}
  - name: FOUNDRY_SKILL_NAMES
    value: ${FOUNDRY_SKILL_NAMES}
```

## Evaluation Dimensions

### 1. Skill Metadata Completeness
- [ ] YAML frontmatter contains the required `name` field
- [ ] `description` states the deliverable (a downloadable PDF guide) and the trigger conditions ("Use when the traveler wants...")
- [ ] The description makes the skill's output artifact type unambiguous

### 2. Trigger Condition Clarity
- [ ] Trigger phrases cover shareable guide, day-by-day plan, and printable outline
- [ ] Scope is narrow enough not to fire on generic travel chit-chat
- [ ] Naming (`travel-guide`) aligns with the directory and script it wraps

### 3. Workflow / Procedural Rigor
- [ ] Steps are numbered and ordered (identify → retrieve → default → run → report)
- [ ] Defaults are explicit (3 days, maximum 7)
- [ ] Grounding to the destinations index via `source_summary` is clearly instructed

### 4. Script Invocation Contract
- [ ] The script name and its argument format (JSON array of CLI flags) are specified
- [ ] Every supported flag is documented with type and required/optional status
- [ ] A concrete example argument array is provided
- [ ] The JSON output contract lists all returned fields

### 5. Agent / Deployment Definition Integrity
- [ ] `agent.yaml` declares a valid `kind: hosted` agent with a name and protocol
- [ ] Environment variables align with the tools the skill needs (search index endpoint, skill names)
- [ ] Resource requests and placeholders (`${...}`) are consistent and parameterized

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Skill Metadata Completeness | 15% | | |
| Trigger Condition Clarity | 15% | | |
| Workflow / Procedural Rigor | 20% | | |
| Script Invocation Contract | 30% | | |
| Agent / Deployment Definition Integrity | 20% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. User asks "make me a 4-day Lisbon guide focused on food and viewpoints"; verify the skill sets `--city Lisbon --days 4 --interests food,viewpoints`, retrieves grounding facts, and reports the generated PDF path.
2. User asks for a printable itinerary without naming a city; verify the skill asks for the missing destination (required `--city`).
3. Verify the returned JSON fields (`city`, `days`, `pages`, `path`, `grounded`, `message`) are surfaced to the traveler, including the file path.

### Boundary Test Cases
1. User specifies no trip length; verify the default of `3` days is applied.
2. User requests 10 days; verify the maximum of `7` is enforced/clamped.
3. No destination facts are retrievable from the index; verify `grounded` reflects this and the guide does not fabricate local facts.
4. Multi-word `--tone` or `--interests` values; verify correct quoting/array packaging in the JSON argument array.

### Negative Test Cases
1. User asks for something unrelated to travel (e.g. "write me a Python script"); verify the travel-guide skill does not trigger.
2. Destination city is an arbitrary/injection-like string; verify it is treated as data passed to the script, not as instructions.
3. Required `--city` omitted when calling the script directly; verify the invocation fails cleanly rather than generating an empty guide.
4. `agent.yaml` deployed with a missing environment variable (e.g. `AZURE_AI_SEARCH_ENDPOINT`); verify grounding degrades gracefully instead of crashing.

## Notes
- This is a consumer travel-planning / lifestyle assistant (non-coding): a hosted agent that produces a shareable, grounded travel guide PDF rather than code.
- The case bundles two coupled artifacts: the skill definition (`SKILL.md`) that tells the agent when and how to use the guide generator, and the agent deployment manifest (`agent.yaml`) that wires up the hosted agent, its model, and its Azure AI Search grounding.
- The two artifacts are cross-referenced through `FOUNDRY_SKILL_NAMES` in `agent.yaml` and the `travel-guide` skill name in `SKILL.md`; `TOOLBOX_ENDPOINT` / `AZURE_AI_SEARCH_*` variables supply the destinations index the skill grounds on.
- The bundled Python script (`scripts/create_travel_guide.py`) is itself adapted from Microsoft's Foundry `07-skills` sample under the MIT License; it is referenced here but not quoted.
- License is MIT; both quoted files are reproduced verbatim from the fetched `main`-branch files.
