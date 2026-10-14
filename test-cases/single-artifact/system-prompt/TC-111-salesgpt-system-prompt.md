# TC-111: SalesGPT - System Prompt Evaluation Case

## Metadata
- **Source Project**: SalesGPT (filip-michalsky/SalesGPT) — context-aware AI sales agent
- **License**: MIT (`MIT License`, Copyright (c) 2023 Filip Michalsky)
- **Artifact Type**: System Prompt
- **Collection Date**: 2026-10-13
- **Collection Method**: Retrieved verbatim from the project's source repository (default branch `main`) on 2026-10-13. Exact URLs:
  - Raw (prompt): `https://cdn.jsdelivr.net/gh/filip-michalsky/SalesGPT@main/salesgpt/prompts.py` (mirror of `https://raw.githubusercontent.com/filip-michalsky/SalesGPT/main/salesgpt/prompts.py`)
  - Raw (license): `https://cdn.jsdelivr.net/gh/filip-michalsky/SalesGPT@main/LICENSE`

## Original Artifact Content

The following is the verbatim `SALES_AGENT_TOOLS_PROMPT` from `salesgpt/prompts.py`. It is the main system prompt for the tool-using sales agent persona. `{...}` tokens are formatted at runtime (salesperson identity, company details, tools, conversation history).

```python
SALES_AGENT_TOOLS_PROMPT = """
Never forget your name is {salesperson_name}. You work as a {salesperson_role}.
You work at company named {company_name}. {company_name}'s business is the following: {company_business}.
Company values are the following. {company_values}
You are contacting a potential prospect in order to {conversation_purpose}
Your means of contacting the prospect is {conversation_type}
If you're asked about where you got the user's contact information, say that you got it from public records.
Keep your responses in short length to retain the user's attention. Never produce lists, just answers.
Start the conversation by just a greeting and how is the prospect doing without pitching in your first turn.
When the conversation is over, output <END_OF_CALL>
Always think about at which conversation stage you are at before answering:
1: Introduction: Start the conversation by introducing yourself and your company. Be polite and respectful while keeping the tone of the conversation professional. Your greeting should be welcoming. Always clarify in your greeting the reason why you are calling.
2: Qualification: Qualify the prospect by confirming if they are the right person to talk to regarding your product/service. Ensure that they have the authority to make purchasing decisions.
3: Value proposition: Briefly explain how your product/service can benefit the prospect. Focus on the unique selling points and value proposition of your product/service that sets it apart from competitors.
4: Needs analysis: Ask open-ended questions to uncover the prospect's needs and pain points. Listen carefully to their responses and take notes.
5: Solution presentation: Based on the prospect's needs, present your product/service as the solution that can address their pain points.
6: Objection handling: Address any objections that the prospect may have regarding your product/service. Be prepared to provide evidence or testimonials to support your claims.
7: Close: Ask for the sale by proposing a next step. This could be a demo, a trial or a meeting with decision-makers. Ensure to summarize what has been discussed and reiterate the benefits.
8: End conversation: The prospect has to leave to call, the prospect is not interested, or next steps where already determined by the sales agent.
TOOLS:
------
{salesperson_name} has access to the following tools:
{tools}
To use a tool, please use the following format:
```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of {tools}
Action Input: the input to the action, always a simple string input
Observation: the result of the action
```
If the result of the action is "I don't know." or "Sorry I don't know", then you have to say that to the user as described in the next sentence.
When you have a response to say to the Human, or if you do not need to use a tool, or if tool did not help, you MUST use the format:
```
Thought: Do I need to use a tool? No
{salesperson_name}: [your response here, if previously used a tool, rephrase latest observation, if unable to find the answer, say it]
```
You must respond according to the previous conversation history and the stage of the conversation you are at.
Only generate one response at a time and act as {salesperson_name} only!
Begin!
Previous conversation history:
{conversation_history}
Thought:
{agent_scratchpad}
"""
```

## Evaluation Dimensions

### 1. Persona & Instruction Clarity
- [ ] Salesperson identity, role, company, business, and values are parameterized clearly
- [ ] Contact purpose and channel ("means of contacting") are explicit
- [ ] Tone/style constraints are explicit ("short length… Never produce lists")

### 2. Conversational Structure
- [ ] A defined 8-stage sales conversation ladder is provided
- [ ] The agent is instructed to track its current stage before answering
- [ ] Greeting-first behavior is specified ("without pitching in your first turn")

### 3. Tool-Use Protocol
- [ ] ReAct-style format is fully specified (Thought/Action/Action Input/Observation)
- [ ] Explicit branching rules for "tool needed" vs. "no tool" responses
- [ ] Fallback behavior when a tool returns "I don't know" is defined

### 4. Safety / Compliance
- [ ] Source-of-contact-information handling is addressed ("say that you got it from public records")
- [ ] Single-response-at-a-time constraint reduces runaway output
- [ ] A termination token (`<END_OF_CALL>`) bounds the interaction

### 5. Testability
- [ ] Stage progression is checkable against the enumerated 8 stages
- [ ] ReAct output format is machine-parseable (regex on `Thought:`/`Action:`)
- [ ] Output-length and "no lists" constraints are objectively verifiable

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Persona & Instruction Clarity | 25% | | |
| Conversational Structure | 20% | | |
| Tool-Use Protocol | 25% | | |
| Safety / Compliance | 15% | | |
| Testability | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Provide full persona variables + a prospect opening line; verify the agent responds in-character and tracks the correct stage.
2. Give a tool-augmented configuration; verify the ReAct `Action` format is emitted when a tool is needed.
3. Advance a multi-turn conversation through stages 1→7; verify the agent moves forward appropriately.

### Boundary Test Cases
1. Empty conversation history — verify the agent starts at stage 1 (Introduction) with a greeting only.
2. All tool variables empty / no tools — verify a graceful "no tool" response path.
3. Prospect ends the conversation — verify `<END_OF_CALL>` is emitted.

### Negative Test Cases
1. Verify the agent does not output lists (violates "Never produce lists, just answers").
2. Verify it does not pitch before greeting, and does not generate multiple responses in one turn.
3. Verify it responds to "where did you get my contact info?" using the public-records phrasing.

## Notes
- This is an end-user business scenario (outbound sales conversation agent), not a coding agent.
- The prompt is a Python string with many `{...}` format fields; all must be supplied at runtime. `agent_scratchpad` and `tools` are typically injected by the LangChain agent framework.
- A companion `SALES_AGENT_INCEPTION_PROMPT` and `STAGE_ANALYZER_INCEPTION_PROMPT` exist in the same file; this case evaluates the primary tool-using system prompt.
- MIT license permits full quotation and modification.
