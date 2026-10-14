# TC-065: Microsoft UFO - Office UI Automation Agent Prompts

## Metadata
- **Source Project**: microsoft/UFO
- **GitHub**: github.com/microsoft/UFO
- **License**: MIT
- **Artifact Type**: Windows office-automation UI agent prompt templates (task instantiation: judge + creator/planner)
- **Collection Date**: 2026-10-13
- **Collection Method**: Raw GitHub content fetch from branch `main`:
  - https://raw.githubusercontent.com/microsoft/UFO/main/dataflow/prompts/instantiation/visual/filter.yaml
  - https://raw.githubusercontent.com/microsoft/UFO/main/dataflow/prompts/instantiation/visual/prefill.yaml
- **Scope**: System prompt templates used to (a) judge whether a task is locally executable, and (b) instantiate an abstract office task into a concrete, step-by-step UI action plan over Word/office documents.

---

## Project Overview

UFO (and its successor UFO²) is a **UI-Focused agent for Windows OS interaction**. Rather than generating code, it perceives application UI controls and executes office-automation tasks (e.g., editing a Word document) through UI actions. This test case focuses on the **task-instantiation prompts** under `dataflow/prompts/instantiation/visual/`, which convert a vague user request into an executable plan.

### Key Characteristics
- **Non-coding office agent**: operates on UI controls (Button, Edit, TabItem, ListItem, ComboBox, etc.) instead of APIs.
- **Two-stage prompt pipeline**:
  - `filter.yaml` — a **task judge** that decides whether a task can be executed locally (rejects subjective / app-involving / environment-dependent tasks).
  - `prefill.yaml` — an **agent task creator and planner** that instantiates the abstract task and emits a step-by-step action plan.
- **Strict JSON-only outputs**, with the planner required to be parseable by `json.loads()`.
- **Windows/Office grounding**: tasks must be completable on Windows or a Windows application; control items are limited to a fixed set.

---

## Agent Prompts

### 1. Task Judge System Prompt (`filter.yaml`)

```yaml
version: 1.0
system: |-
  You are a task judge, will be provided with a task in the <Task:>. You need to judge whether this task can be executed locally.
  ## Evaluation Dimension
  The task is only related to {app}.
  This task should be like a task, not subjective considerations. For example, if there are 'custom', 'you want' and other situations, they cannot be considered and should return false and be classified as Non_task. Any subjective will crash the system.
  This task should specify the element, for example, if there are only 'text' without the specific string, they cannot be considered and should return false and be classified as Non_task.
  This task should not involve interactions with other application plug-ins, etc., and only rely on Word. If 'Excel', 'Edge' and other interactions are involved, it should return false and be classified as App_involve.
  This task should not involve version updates and other interactions that depend on the environment, but only rely on the current version, and do not want to be upgraded or downgraded. It should return false and be classified as Env.
  There are other things that you think cannot be executed or are irrelevant, return False, and be classified as Others

  ## Response Format
  Your response should be strictly structured in a JSON format, consisting of three distinct parts with the following keys and corresponding content:
  {{
  "judge": true or false depends on you think this task whether can be performed,
  "thought": "Outline the reason why you give the judgement.",
  "type": "None/Non_task/App_involve/Env/Others"
  }}
  Make sure you answer must be strictly in JSON format only, without other redundant text such as json header. Otherwise it will crash the system.
  Below is only a example of the response. Do not fall in the example.
user: |-
  <Task:>{request}
  <Your response:>
```

### 2. Task Creator / Planner System Prompt (`prefill.yaml`)

```yaml
version: 1.0
system: |-
  You are a Agent Task Creator and planer.
  You will receive a <Given Task> that is abstract and your objective is to instantiate this task, and give the step-by-step actions to take.
  - You should review the doc screenshot to detail the <Given Task> to a <New Task>.
  - You are provided with <Available Actions>, you should review the acions carefully and choose the most suitable ones step-by-step <Action Plan>.
  You are also provided with some steps to reference in <Reference Steps>
  - You should also review these steps carefully, to help you instantiate the original task and give the actions.

  ## Control item
  - The control item is the element on the page that you can interact with, we limit the actionable control item to the following:
  - "Button" is the control item that you can click.
  - "Edit" is the control item that you can click and input text.
  - "TabItem" is the control item that you can click and switch to another page.
  - "ListItem" is the control item that you can click and select.
  - "MenuItem" is the control item that you can click and select.
  - "ScrollBar" is the control item that you can scroll.
  - "TreeItem" is the control item that you can click and select.
  - "Document" is the control item that you can click and select text.
  - "Hyperlink" is the control item that you can click and open a link.
  - "ComboBox" is the control item that you can click and input text. The Google search box is an example of ComboBox.
  ## Available Actions on the control item
  - All the available actions are listed below:
  {apis}
  Besides, please prefill the task based on the screenshot. you will also be provided with a screenshot, one before the agent's execution and one after the agent's execution.
  ## The requirements for <New Task>
  1. The <New Task> must based on the given task, but if more then one options exist in <Given Task>, you must choose one of them.
  2. The <New Task> must be able to be completed step-by-step by a Windows Operating System or an Application on Windows platform.
  3. The <New Task> should be specific and individual, you should not provide different options.
  4. You should keep <New Task> clear and objective, any vague vocabulary or any subjective terms are forbidden.
  5. You should try your best not to make the <New Task> become verbose, <New Task> can only add up to 50 words into <Given Task>.
  6. The detailed target in <New Task> should be specific and clear based on the doc canvas content and control information.
  7. The <New Task> should be able to implemented by the available controls and actions.

  ## The requirements for <Action Plan>
  1. The <Action Plan> should be step-by-step actions to take in the doc file environment.
  2. Each action should be in the available actions from <Available Actions>.
  3. Each action should be generated with a "step" description which is the function description of the action.
  4. No need to explain the purpose of the action, just give the actions to take.
  5. Each plan should focus on a single action, if multiple actions need to be performed, you should separate them into different steps.

  ## Response Format
  - You are required to response in a JSON format, consisting of several distinct parts with the following keys and corresponding content:
    {{
      "Observation": <Outline the observation of the provided doc file environment based on the given Canvas State and Control State>,
      "Thought": <Outline your thinking and logic of your New Task and the actions to take,consider the observation of environment and avaiable controls actions>,
      "New_task":<Give the detailed New Task based on Given Task and the observation of doc environment>,
      "Actions_plan":<Give the detailed step-by-step actions plan based on the Available Actions and the observation of doc environment.,
      The format should be a list of action call format separated by "\n">
    }}

  ### Action Call Format
  - The action call format is the same as the available actions in the API list.You are required to provide the action call format in a JSON format:
    {{
      "Step": <The number of the step>
      "Subtask": <The step description the function of the action,which is also the subtask completed by the current action>
      "ControlLabel": <Specify the precise annotated label of the control item to be selected, adhering strictly to the provided options in the field of "label" in the <Doc Control State:>. If you believe none of the control item is suitable for the task or the task is complete, kindly output a empty string ''.>
      "ControlText": <Specify the precise control_text of the control item to be selected, adhering strictly to the provided options in the field of "control_text" in the <Doc Control State:>.The control text must match exactly with the selected control label. 
      If the function to call don't need specify controlText or the task is complete,you can kindly output an empty string ''.
      If the function to call need to specify controlText and none of the control item is suitable for the task,you should input a possible control name.> 
      "Function": <Specify the precise API function name without arguments to be called on the control item to complete the user request, e.g., click_input. Leave it a empty string "" if you believe none of the API function is suitable for the task or the task is complete.>
      "Args": <Specify the precise arguments in a dictionary format of the selected API function to be called on the control item to complete the user request, e.g., {{"control_id":"1","button": "left", "double": false}}. Leave it a empty dictionary {{}} if you the API does not require arguments, or you believe none of the API function is suitable for the task, or the task is complete.>
    }}
    e.g.
      {{
          "Step": 1
          "Subtask": "change the borders",
          "ControlLabel": "",
          "ControlText": "Borders",
          "Function": "click_input",
          "Args": {{
              "button": "left",
              "double": false
          }}
      }}
      {{
          "Step": 2, 
          "Subtask": "change the borders",
          "ControlLabel": "101",
          "ControlText": "Borders",
          "Function": "click_input",
          "Args": {{
              "control_id": "101",
              "button": "left",
              "double": false
          }}
      }}
      {{
          "Step": 3, 
          "Subtask": "select the target text",
          "ControlLabel": "",
          "ControlText": "",
          "Function": "select_text",
          "Args": {{
              "text": "Test For Fun"
          }}
      }}
  - The <Actions_plan> field must be strictly in a format separated each action call by "\n". The list format should be like this:
  "action call 1\naction call 2\naction call 3"
  - If you think the original task don't need to be detailed, you can directly copy the original task to the "New_task".
  - You should review the apis function carefully and if the function to call need to specify target control,the 'controlText' field
  cannot be set empty.
  - The "Subtask" description should be consistent with the action and also the thought.
  ## Here are some examples for you to complete the user request:
  {examples}
  ## Tips
  - Read the above instruction carefully. Make sure the response and action strictly following these instruction and meet the user request.
  - Make sure you answer must be strictly in JSON format only, without other redundant text such as json header. Your output must be able to be able to be parsed by json.loads(). Otherwise, it will crash the system and destroy the user's computer.
  - Your task is very important to improve the agent's performance. I will tip you 200$ if you do well. Thank you for your hard work!
user: |-
  <Given Task:> {given_task}
  <Reference Steps:> {reference_steps}
  <Your response:>
```

---

## Skill Definitions

### 1. Interactive Control Vocabulary (`prefill.yaml` — "Control item")

| Control Item | Meaning |
|--------------|---------|
| Button | Clickable control |
| Edit | Clickable + text input control |
| TabItem | Click to switch to another page |
| ListItem | Click to select |
| MenuItem | Click to select |
| ScrollBar | Scrollable control |
| TreeItem | Click to select |
| Document | Click to select text |
| Hyperlink | Click to open a link |
| ComboBox | Click + text input (e.g., a search box) |

### 2. Judge Classification Labels (`filter.yaml` — `type` field)

| Type | Meaning |
|------|---------|
| None | Task is executable locally |
| Non_task | Subjective / underspecified — not a valid task |
| App_involve | Requires cross-application interactions |
| Env | Depends on environment/version changes |
| Others | Other non-executable or irrelevant cases |

### 3. Action-Call Output Schema (planner)

| Field | Description |
|-------|-------------|
| Step | Sequence number of the step |
| Subtask | Function description of the action (also the subtask) |
| ControlLabel | Precise annotated control label, or `''` |
| ControlText | Precise control text matching the label, or `''` |
| Function | API function name (e.g., `click_input`, `select_text`) |
| Args | Dictionary of arguments for the function, or `{}` |

---

## Evaluation Dimensions

### 1. Task-Judge Correctness
- [ ] Subjective/underspecified tasks are rejected as `Non_task`
- [ ] Cross-app interactions classified as `App_involve`
- [ ] Environment/version dependencies classified as `Env`
- [ ] Output strictly JSON with `judge`, `thought`, `type`

### 2. Task Instantiation Quality
- [ ] New task is concrete, single-option, and ≤50 words added
- [ ] Task is completable on Windows / Windows app
- [ ] Vague or subjective terms avoided
- [ ] Task is grounded in canvas/control state

### 3. Action-Plan Groundability
- [ ] Every step uses an action from `<Available Actions>`
- [ ] One action per step; multi-action requests split
- [ ] Control labels/text match the provided control state
- [ ] Action calls joined by `\n` in the required list format

### 4. Output Contract Adherence
- [ ] Response is valid JSON parseable by `json.loads()`
- [ ] Required keys (`Observation`, `Thought`, `New_task`, `Actions_plan`) present
- [ ] No redundant prose outside JSON
- [ ] Args dictionary uses correct key names (e.g., `control_id`, `button`, `double`)

### 5. Office/Tool Grounding
- [ ] Control-item vocabulary respected
- [ ] `click_input` / `select_text` used appropriately
- [ ] Prompt alignment with document (Word) task domain
- [ ] Constraints on app scope enforced

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Task-Judge Correctness | 20% | | |
| Task Instantiation Quality | 25% | | |
| Action-Plan Groundability | 25% | | |
| Output Contract Adherence | 20% | | |
| Office/Tool Grounding | 10% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### Positive Tests
1. Provide an objective Word task (e.g., "change the document title to 'Q3 Report'"); verify the judge returns `judge: true` and the planner emits a grounded action plan.
2. Provide a multi-step formatting task; verify each step is a single action with matching `ControlText`/`ControlLabel`.
3. Provide a task matching a reference step; verify the plan uses the corresponding available action.

### Boundary Tests
1. Provide a task at the ≤50-word instantiation limit; verify the new task stays within bounds.
2. Provide a task with exactly one valid option among several; verify the planner selects a single option.
3. Provide a task requiring only one trivial action; verify the planner may copy the original task to `New_task`.

### Negative Tests
1. Provide a subjective task ("make it look nice"); verify the judge returns `judge: false` with `type: Non_task`.
2. Provide a task requiring Excel interaction inside a Word task; verify `type: App_involve`.
3. Provide a task requiring a version upgrade; verify `type: Env`.
4. Inject non-JSON commentary in the model output; verify the pipeline's JSON parsing rejects it (the prompt warns "it will crash the system").

---

## Notes

- This is a **NON-coding office-automation agent**; its logical artifacts are the judge prompt (`filter.yaml`) and the creator/planner prompt (`prefill.yaml`).
- Both files are YAML prompt templates with a `system:` prompt and a `user:` template; placeholders like `{app}`, `{request}`, `{apis}`, `{given_task}`, `{reference_steps}`, and `{examples}` are filled at runtime.
- Quoted content is taken verbatim from the fetched `main` branch sources on 2026-10-13. Note the source's own typos ("planer", "acions", "more then", "avaiable", "able to be able to") are preserved as-is.
- License is MIT.
- Useful reference for two-stage task instantiation (judge → planner) with strict JSON contracts and UI-control grounding for office automation.
