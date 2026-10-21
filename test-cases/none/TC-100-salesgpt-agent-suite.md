# TC-100: SalesGPT - Agent Suite Evaluation Case

## Metadata
- **Source Project**: SalesGPT (filip-michalsky/SalesGPT)
- **Submodule**: `salesgpt/prompts.py` (3 prompt templates) + `salesgpt/tools.py` (4 tool schemas) + `salesgpt/stages.py` (conversation-stage definitions) + `salesgpt/agents.py` (ReAct orchestration)
- **License**: MIT
- **Artifact Type**: Single-Agent suite (sales-agent system prompt + inception prompt + stage-analyzer prompt + tool schemas)
- **Collection Date**: 2026-10-13
- **Collection Method**: GitHub API metadata + README + raw source retrieval, exact URLs:
  - `https://github.com/filip-michalsky/SalesGPT`
  - `https://raw.githubusercontent.com/filip-michalsky/SalesGPT/main/README.md`
  - `https://raw.githubusercontent.com/filip-michalsky/SalesGPT/main/salesgpt/prompts.py`
  - `https://raw.githubusercontent.com/filip-michalsky/SalesGPT/main/salesgpt/tools.py`
  - `https://api.github.com/repos/filip-michalsky/SalesGPT` (repository metadata, license = MIT)
  - `https://api.github.com/repos/filip-michalsky/SalesGPT/contents/salesgpt` (directory listing)

---

## Project Overview

SalesGPT is a **context-aware AI sales agent** that automates sales outreach across voice, email and messaging channels. It is an end-user-facing business application (sales automation), packaged both as a Python library and as a deployable agent with a chat UI and backend.

From the project README (verbatim):

> "This repo is an implementation of a **context-aware** AI Agent for Sales using LLMs and can work across voice, email and texting (SMS, WhatsApp, WeChat, Weibo, Telegram, etc.)."

> "SalesGPT is *context-aware*, which means it can understand what stage of a sales conversation it is in and act accordingly."

> "Morever, SalesGPT has access to tools, such as your own pre-defined product knowledge base, significantly reducing hallucinations."

### Conversation Stage Model (from README, verbatim)

> - "Introduction: Start the conversation by introducing yourself and your company."
> - "Qualification: Qualify the prospect by confirming if they are the right person to talk to regarding your product/service."
> - "Value Proposition: Briefly explain how your product/service can benefit the prospect."
> - "Needs Analysis: Ask open-ended questions to uncover the prospect's needs and pain points."
> - "Solution Presentation: Based on the prospect's needs, present your product/service as the solution that can address their pain points."
> - "Objection Handling: Address any objections that the prospect may have regarding your product/service."
> - "Close: Ask for the sale by proposing a next step."
> - "End Conversation: The user does not want to continue the conversation, so end the call."

---

## Logical Artifact Inventory

### 1. System Prompts (`salesgpt/prompts.py`, 3 templates)

#### 1.1 `SALES_AGENT_TOOLS_PROMPT` (verbatim excerpt)

```
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
1: Introduction: ...
...
8: End conversation: ...
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
...
When you have a response to say to the Human, or if you do not need to use a tool, or if tool did not help, you MUST use the format:
```
Thought: Do I need to use a tool? No
{salesperson_name}: [your response here, if previously used a tool, rephrase latest observation, if unable to find the answer, say it]
```
...
```

#### 1.2 `SALES_AGENT_INCEPTION_PROMPT` (verbatim, tail)

```
...
Example 1:
Conversation history:
{salesperson_name}: Hey, good morning! <END_OF_TURN>
User: Hello, who is this? <END_OF_TURN>
{salesperson_name}: This is {salesperson_name} calling from {company_name}. How are you?
User: I am well, why are you calling? <END_OF_TURN>
{salesperson_name}: I am calling to talk about options for your home insurance. <END_OF_TURN>
User: I am not interested, thanks. <END_OF_TURN>
{salesperson_name}: Alright, no worries, have a good day! <END_OF_TURN> <END_OF_CALL>
End of example 1.
You must respond according to the previous conversation history and the stage of the conversation you are at.
Only generate one response at a time and act as {salesperson_name} only! When you are done generating, end with '<END_OF_TURN>' to give the user a chance to respond.
```

#### 1.3 `STAGE_ANALYZER_INCEPTION_PROMPT` (verbatim)

```
You are a sales assistant helping your sales agent to determine which stage of a sales conversation should the agent stay at or move to when talking to a user.
...
Now determine what should be the next immediate conversation stage for the agent in the sales conversation by selecting only from the following options:
{conversation_stages}
The answer needs to be one number only from the conversation stages, no words.
Only use the current conversation stage and conversation history to determine your answer!
If the conversation history is empty, always start with Introduction!
```

### 2. Tool Schemas (`salesgpt/tools.py`, 4 tools — verbatim `get_tools()`)

```
Tool(
    name="ProductSearch",
    func=knowledge_base.run,
    description="useful for when you need to answer questions about product information or services offered, availability and their costs.",
),
Tool(
    name="GeneratePaymentLink",
    func=generate_stripe_payment_link,
    description="useful to close a transaction with a customer. You need to include product name and quantity and customer name in the query input.",
),
Tool(
    name="SendEmail",
    func=send_email_tool,
    description="Sends an email based on the query input. The query should specify the recipient, subject, and body of the email.",
),
Tool(
    name="SendCalendlyInvitation",
    func=generate_calendly_invitation_link,
    description='''Useful for when you need to create invite for a personal meeting in Sleep Heaven shop.
    Sends a calendly invitation based on the query input.''',
)
```

### 3. Orchestration Surface (`salesgpt/agents.py`, from README quickstart, verbatim)

```
sales_agent = SalesGPT.from_llm(llm, use_tools=True, verbose=False,
                            product_catalog = "examples/sample_product_catalog.txt",
                            salesperson_name="Ted Lasso",
                            salesperson_role="Sales Representative",
                            company_name="Sleep Haven",
                            company_business='''...''')
sales_agent.seed_agent()
sales_agent.determine_conversation_stage() # optional for demonstration, built into the prompt
sales_agent.step()
sales_agent.human_step(user_input)
```

---

## Evaluation Dimensions

### 1. Persona & Role Clarity
- [ ] Salesperson name / role / company / value set are parameterized, not hard-coded
- [ ] The agent's contact channel and purpose are declared to the model
- [ ] Stage-analyzer role is clearly separated from the salesperson role

### 2. Workflow / Stage Completeness
- [ ] 8-stage sales conversation model is explicit and ordered (Introduction → Close → End)
- [ ] Stage transitions are decided by a dedicated analyzer prompt, not ad hoc
- [ ] `<END_OF_CALL>` / `<END_OF_TURN>` turn-control tokens defined

### 3. Prompt Consistency
- [ ] Shared placeholders (`{salesperson_name}`, `{company_name}`, `{conversation_history}`) are consistent across templates
- [ ] ReAct output contract (`Thought / Action / Action Input / Observation`) is applied uniformly
- [ ] Anti-hallucination instruction ("got it from public records", "don't make up") present

### 4. Tool Modularity
- [ ] 4 tools with distinct, non-overlapping descriptions
- [ ] Tool inputs are simple strings; tool names appear in the prompt `{tools}` slot
- [ ] `product_catalog` grounding tool reduces hallucination independently of the LLM

### 5. Guardrails & Safety
- [ ] Human-in-the-loop mode supported
- [ ] Answer length constrained ("Keep your responses in short length... Never produce lists")
- [ ] Payment/email/Calendly side effects are gated behind explicit tool calls

### 6. Extensibility
- [ ] LLM-agnostic via LiteLLM (50+ providers)
- [ ] Custom stages definable by the user
- [ ] Backend API + frontend UI can run separately

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Persona & Role Clarity | 15% | | |
| Workflow / Stage Completeness | 25% | | |
| Prompt Consistency | 15% | | |
| Tool Modularity | 20% | | |
| Guardrails & Safety | 15% | | |
| Extensibility | 10% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### End-to-End Tests
1. **Full sales call**: seed a prospect, run Introduction → Close, and confirm the stage analyzer advances monotonically.
2. **Tool grounding**: ask "What pricing do you have?" and verify `ProductSearch` is invoked and the answer quotes the product catalog.
3. **Close**: confirm `GeneratePaymentLink` produces a payment link and the agent summarizes the offer.

### Unit Tests
1. **Stage analyzer**: empty history must return stage `1` (Introduction).
2. **Inception prompt**: verify `<END_OF_TURN>` is appended to every emitted turn.
3. **Tool registry**: `get_tools()` returns exactly the four named tools with non-empty descriptions.

### Stress Tests
1. **Objection loops**: repeated "not interested" must terminate with `<END_OF_CALL>`, not loop.
2. **Prompt-injection**: attempt to make the agent ignore stage constraints.
3. **Multi-channel**: swap `conversation_type` (voice/email/SMS) and check instruction adherence.

---

## Notes

- **License**: MIT (verified via GitHub API `license.spdx_id = "MIT"`). Verbatim quotation is permitted.
- **Scope**: sales outreach is an end-user business scenario; the agent does not generate or review code.
- **Caveat**: repository is feature-complete but the last push was 2024-09-17; treat as a stable baseline rather than an actively evolving suite.
- All quoted text was retrieved verbatim from the raw URLs listed in Metadata on 2026-10-13; long prompts are excerpted with ellipses.
