# TC-091: Mobile-Agent-v2 - Multi-Logical-Artifact Suite Evaluation Case

## Metadata
- **Source Project**: X-PLUG/MobileAgent (sub-directory `Mobile-Agent-v2/`)
- **GitHub URL**: https://github.com/X-PLUG/MobileAgent
- **License**: MIT (repository root license, indicated by the GitHub license page for `X-PLUG/MobileAgent`)
- **Artifact Type**: Multi-Agent suite (per-agent system prompts in Python + action/reflection/memory prompt builders + orchestration loop)
- **Collection Date**: 2026-10-13
- **Collection Method**: Direct raw-file fetches of the public source. Exact URLs used:
  - https://raw.githubusercontent.com/X-PLUG/MobileAgent/main/Mobile-Agent-v2/MobileAgent/prompt.py
  - https://raw.githubusercontent.com/X-PLUG/MobileAgent/main/Mobile-Agent-v2/MobileAgent/chat.py
  - https://raw.githubusercontent.com/X-PLUG/MobileAgent/main/Mobile-Agent-v2/run.py
  - https://github.com/X-PLUG/MobileAgent/tree/main/Mobile-Agent-v2 (README)
  - https://github.com/X-PLUG/MobileAgent/blob/main/LICENSE (license page → MIT)

---

## Project Overview

Mobile-Agent-v2 is a **multi-agent mobile GUI automation assistant** from Alibaba's X-PLUG group (NeurIPS 2024). The user gives a natural-language instruction (e.g. "open the app and book a ride"), and the system operates a real Android/HarmonyOS phone through ADB to complete it. It is an **end-user device-operating agent**, not a coding assistant.

The v2 architecture explicitly decomposes the task into **role-specialised agents** that address the "navigation in long-context input" problem:

| Role | Responsibility | Artifact |
|------|------|-------------|
| **Operator / Decision Agent** | Chooses exactly one action per step from the screenshot | `init_action_chat` system prompt + `get_action_prompt` |
| **Reflection Agent** | Compares before/after screenshots and judges whether the last action matched its intent (A/B/C) | `init_reflect_chat` system prompt + `get_reflect_prompt` |
| **Memory Unit** | Extracts task-relevant content from the current screen for later steps | `init_memory_chat` system prompt + `get_memory_prompt` |
| **Progress / Completion (Process) Module** | Maintains a rolling "Completed contents" summary of what has been achieved | `get_process_prompt` |
| *(Perception modules)* | OCR + icon detection/captioning feed textual screen descriptions to the agents | `text_localization.ocr`, `icon_localization.det`, icon caption model (Qwen-VL) |

The orchestration loop (`run.py`) alternates Operator → action execution → screenshot refresh → Reflection → Memory → Progress tracking.

---

## Logical Artifact Inventory

### 1. Per-Agent System Prompts (verbatim from `MobileAgent/chat.py`)

```python
def init_action_chat():
    operation_history = []
    sysetm_prompt = "You are a helpful AI mobile phone operating assistant. You need to help me operate the phone to complete the user\'s instruction."
    operation_history.append(["system", [{"type": "text", "text": sysetm_prompt}]])
    return operation_history


def init_reflect_chat():
    operation_history = []
    sysetm_prompt = "You are a helpful AI mobile phone operating assistant."
    operation_history.append(["system", [{"type": "text", "text": sysetm_prompt}]])
    return operation_history


def init_memory_chat():
    operation_history = []
    sysetm_prompt = "You are a helpful AI mobile phone operating assistant."
    operation_history.append(["system", [{"type": "text", "text": sysetm_prompt}]])
    return operation_history
```
> Note: the three agents share an almost identical one-line persona; role differentiation is carried almost entirely by the **user prompts** below, not by the system prompts.

### 2. Operator / Decision Agent prompt builder (verbatim from `MobileAgent/prompt.py`)

`get_action_prompt(...)` — the full multi-section prompt; key excerpts:

```python
def get_action_prompt(instruction, clickable_infos, width, height, keyboard, summary_history, action_history, last_summary, last_action, add_info, error_flag, completed_content, memory):
    prompt = "### Background ###\n"
    prompt += f"This image is a phone screenshot. Its width is {width} pixels and its height is {height} pixels. The user\'s instruction is: {instruction}.\n\n"

    prompt += "### Screenshot information ###\n"
    prompt += "In order to help you better perceive the content in this screenshot, we extract some information on the current screenshot through system files. "
    prompt += "This information consists of two parts: coordinates; content. "
    prompt += "The format of the coordinates is [x, y], x is the pixel from left to right and y is the pixel from top to bottom; the content is a text or an icon description respectively. "
    ...
    prompt += "### Response requirements ###\n"
    prompt += "Now you need to combine all of the above to perform just one action on the current page. You must choose one of the six actions below:\n"
    prompt += "Open app (app name): If the current page is desktop, you can use this action to open the app named \"app name\" on the desktop.\n"
    prompt += "Tap (x, y): Tap the position (x, y) in current page.\n"
    prompt += "Swipe (x1, y1), (x2, y2): Swipe from position (x1, y1) to position (x2, y2).\n"
    if keyboard:
        prompt += "Type (text): Type the \"text\" in the input box.\n"
    else:
        prompt += "Unable to Type. You cannot use the action \"Type\" because the keyboard has not been activated. ...\n"
    prompt += "Home: Return to home page.\n"
    prompt += "Stop: If you think all the requirements of user\'s instruction have been completed and no further operation is required, you can choose this action to terminate the operation process."
    prompt += "\n\n"

    prompt += "### Output format ###\n"
    prompt += "Your output consists of the following three parts:\n"
    prompt += "### Thought ###\nThink about the requirements ...\n"
    prompt += "### Action ###\nYou can only choose one from the six actions above. Make sure that the coordinates or text in the \"()\".\n"
    prompt += "### Operation ###\nPlease generate a brief natural language description for the operation in Action based on your Thought."

    return prompt
```
This is effectively the **tool/action schema** for the Operator agent: a fixed vocabulary of six actions (`Open app`, `Tap`, `Swipe`, `Type`, `Home`, `Stop`) with a strict three-part output contract.

### 3. Reflection Agent prompt builder (verbatim, excerpt)

```python
def get_reflect_prompt(instruction, clickable_infos1, clickable_infos2, width, height, keyboard1, keyboard2, summary, action, add_info):
    prompt = f"These images are two phone screenshots before and after an operation. Their widths are {width} pixels and their heights are {height} pixels.\n\n"
    ...
    prompt += "### Response requirements ###\n"
    prompt += "Now you need to output the following content based on the screenshots before and after the current operation:\n"
    prompt += "Whether the result of the \"Operation action\" meets your expectation of \"Operation thought\"?\n"
    prompt += "A: The result of the \"Operation action\" meets my expectation of \"Operation thought\".\n"
    prompt += "B: The \"Operation action\" results in a wrong page and I need to return to the previous page.\n"
    prompt += "C: The \"Operation action\" produces no changes."
    prompt += "\n\n"

    prompt += "### Output format ###\n"
    prompt += "Your output format is:\n"
    prompt += "### Thought ###\nYour thought about the question\n"
    prompt += "### Answer ###\nA or B or C"

    return prompt
```

### 4. Memory Unit prompt builder (verbatim)

```python
def get_memory_prompt(insight):
    if insight != "":
        prompt  = "### Important content ###\n"
        prompt += insight
        prompt += "\n\n"

        prompt += "### Response requirements ###\n"
        prompt += "Please think about whether there is any content closely related to ### Important content ### on the current page? If there is, please output the content. If not, please output \"None\".\n\n"

    else:
        prompt  = "### Response requirements ###\n"
        prompt += "Please think about whether there is any content closely related to user\'s instrcution on the current page? If there is, please output the content. If not, please output \"None\".\n\n"

    prompt += "### Output format ###\n"
    prompt += "Your output format is:\n"
    prompt += "### Important content ###\nThe content or None. Please do not repeatedly output the information in ### Memory ###."

    return prompt
```

### 5. Progress / Completion module (verbatim, excerpt from `get_process_prompt`)

```python
def get_process_prompt(instruction, thought_history, summary_history, action_history, completed_content, add_info):
    prompt = "### Background ###\n"
    prompt += f"There is an user\'s instruction which is: {instruction}. You are a mobile phone operating assistant and are operating the user\'s mobile phone.\n\n"
    ...
    prompt += "### Output format ###\n"
    prompt += "Your output format is:\n"
    prompt += "### Completed contents ###\nUpdated Completed contents. Don\'t output the purpose of any operation. Just summarize the contents that have been actually completed in the ### History operations ###."
    ...
    return prompt
```

### 6. Orchestration config (verbatim excerpts from `run.py`)

Feature switches at the top of the file (the user edits these):
```python
# Reflection Setting: If you want to improve the operating speed, you can disable the reflection agent. This may reduce the success rate.
reflection_switch = True
# Memory Setting: If you want to improve the operating speed, you can disable the memory unit. This may reduce the success rate.
memory_switch = True
```
Main loop (task decomposition / action execution / reflection / memory):
```python
while True:
    iter += 1
    ...
    prompt_action = get_action_prompt(instruction, perception_infos, width, height, keyboard, summary_history, action_history, summary, action, add_info, error_flag, completed_requirements, memory)
    chat_action = init_action_chat()
    chat_action = add_response("user", prompt_action, chat_action, screenshot_file)
    output_action = inference_chat(chat_action, 'gpt-4o', API_url, token)
    thought = output_action.split("### Thought ###")[-1].split("### Action ###")[0]...
    summary = output_action.split("### Operation ###")[-1]...
    action  = output_action.split("### Action ###")[-1].split("### Operation ###")[0]...
    ...
    if memory_switch:
        prompt_memory = get_memory_prompt(insight)
        ...
    if "Open app" in action:
        ...
    elif "Tap" in action:
        ...
    elif "Swipe" in action:
        ...
    elif "Type" in action:
        ...
    elif "Home" in action:
        home(adb_path)
    elif "Stop" in action:
        break
    ...
    if reflection_switch:
        prompt_reflect = get_reflect_prompt(instruction, last_perception_infos, perception_infos, width, height, last_keyboard, keyboard, summary, action, add_info)
        chat_reflect = init_reflect_chat()
        chat_reflect = add_response_two_image("user", prompt_reflect, chat_reflect, [last_screenshot_file, screenshot_file])
        output_reflect = inference_chat(chat_reflect, 'gpt-4o', API_url, token)
        reflect = output_reflect.split("### Answer ###")[-1].replace("\n", " ").strip()
        ...
        if 'A' in reflect:
            thought_history.append(thought)
```
Action dispatch is by **natural-language substring matching** (`if "Tap" in action`) rather than a structured function-call schema — a notable fragility for tool-schema evaluation.

---

## Evaluation Dimensions

### 1. Role Clarity
- [ ] Four functional roles are described in the README, but the three system prompts in `chat.py` are near-identical one-liners.
- [ ] Role separation relies on the user prompt builders, not on distinct personas.

### 2. Workflow Completeness
- [ ] Loop covers perceive → decide → act → reflect → remember → progress.
- [ ] `Stop` action and `reflection_switch` / `memory_switch` toggles define termination and optionality.

### 3. Prompt Consistency
- [ ] Shared `### Thought ### / ### Action ### / ### Operation ###` and `### Answer ###` formats.
- [ ] Typo present in source (`instrcution` in `get_memory_prompt`) — consistency/quality defect to flag.

### 4. Tool Schema Modularity
- [ ] Actions are a **closed vocabulary of six** defined inline in prose, not a structured schema.
- [ ] Parsing is substring-based (`action.split(...)`, `"Tap" in action`) → brittle.

### 5. Observability
- [ ] `thought_history`, `summary_history`, `action_history`, `memory`, `completed_requirements` are kept, but only as loose locals.
- [ ] Structured status printing (`"#"*50 + " Decision " ...`) provides limited tracing.

### 6. Extensibility
- [ ] Adding a new action requires editing the prompt text **and** the `if/elif` dispatch chain **and** the parser.
- [ ] No configuration object; switches are module-level globals in `run.py`.

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Role Clarity | 15% | | |
| Workflow Completeness | 25% | | |
| Prompt Consistency | 15% | | |
| Tool Schema Modularity | 20% | | |
| Observability | 10% | | |
| Extensibility | 15% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### Positive Tests
1. **Simple instruction** ("open Settings and turn on Wi-Fi"): verify Operator picks `Open app` then `Tap/Swipe` and eventually `Stop`.
2. **Reflection correction**: force a wrong action and confirm the Reflection agent returns `B`/`C` and the loop retries.
3. **Memory carry-over**: instruction needing cross-screen recall (e.g. copy a code from screen 1, paste on screen 3) and verify the Memory unit output is reused.

### Boundary Tests
1. **Keyboard state**: instruction requiring typing while `keyboard == False` → verify the prompt forbids `Type` and instructs to open the input box first.
2. **Switches off**: `reflection_switch = False` and `memory_switch = False` → verify the loop still runs end-to-end.
3. **Max iterations / dead-cycle**: instruction where reflection never returns `A` (the README warns it "may cause operation to fall into a dead cycle").

### Negative Tests
1. **Unparseable action**: model returns text not containing any of the six actions → dispatch matches nothing; verify behavior.
2. **Ambiguous substring**: action string that contains two keywords (e.g. "Tap to Open app") → substring dispatch may mis-route.
3. **`Stop` too early**: model emits `Stop` before completing the instruction.

---

## Notes

- Mobile-Agent is licensed **MIT** (repository root; the license page for `X-PLUG/MobileAgent` shows MIT). MIT permits quoting with attribution.
- All prompts and orchestration snippets above are **quoted verbatim** from `Mobile-Agent-v2/MobileAgent/prompt.py`, `chat.py`, and `run.py` at the URLs listed in Metadata. Elided sections are marked with `...`.
- The `mobile_agent.py` (`MobileAgent/`) module referenced by `run.py` imports (`from MobileAgent.api import inference_chat`, etc.) is the v1 layout; this case documents **Mobile-Agent-v2**.
- Dead-cycle risk and substring-based action dispatch are **real defects observable in source**, not invented.
