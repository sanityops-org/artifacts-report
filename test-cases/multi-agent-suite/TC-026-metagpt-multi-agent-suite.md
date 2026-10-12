# TC-026: MetaGPT - Multi-Agent Suite

## Metadata
- **Source Project**: MetaGPT (geekan/MetaGPT)
- **Commit SHA**: 11cdf466d042aece04fc6cfd13b28e1a70341b1f
- **License**: MIT
- **Artifact Type**: Multi-Agent Framework
- **Collection Date**: 2025-10-12
- **Collection Method**: GitHub API content extraction from verified commit

---

## Project Overview

MetaGPT is a **multi-agent collaborative framework** for software development and simulation. It includes specialized prompt templates for Stanford Town (social simulation), Android Assistant, and AFlow (workflow automation).

### Core Prompt Categories

| Category | Purpose | Primary Artifact Type |
|----------|---------|----------------------|
| **Stanford Town** | Social simulation agent behaviors | System Prompt |
| **Android Assistant** | Mobile device automation | System Prompt |
| **AFlow** | Workflow automation and code generation | System Prompt |

---

## Logical Artifact Inventory

### 1. System Prompts (5)

#### 1.1 Stanford Town - Daily Planning
```text
# metagpt/ext/stanford_town/prompts/daily_planning_v6.txt

Variables: 
!<INPUT 0>! -- Commonset
!<INPUT 1>! -- Lifestyle
!<INPUT 2>! -- Reverie date time now
!<INPUT 3>! -- Persona first names
!<INPUT 4>! -- wake_up_hour

<commentblockmarker>###</commentblockmarker>
!<INPUT 0>!

In general, !<INPUT 1>!
Today is !<INPUT 2>!. Here is !<INPUT 3>!'s plan today in broad-strokes (with the time of the day. e.g., have a lunch at 12:00 pm, watch TV from 7 to 8 pm): 1) wake up and complete the morning routine at !<INPUT 4>!, 2)
```

#### 1.2 Stanford Town - Hourly Schedule Generation
```text
# metagpt/ext/stanford_town/prompts/generate_hourly_schedule_v2.txt

Variables: 
!<INPUT 0>! -- Schedule format
!<INPUT 1>! -- Commonset
!<INPUT 2>! -- prior_schedule
!<INPUT 3>! -- intermission_str
!<INPUT 4>! -- intermission 2
!<INPUT 5>! -- prompt_ending

<commentblockmarker>###</commentblockmarker>
Hourly schedule format: 
!<INPUT 0>!
===
!<INPUT 1>!
!<INPUT 2>!
!<INPUT 3>!!<INPUT 4>!
!<INPUT 5>!
```

#### 1.3 Stanford Town - Event Triple Generation
```text
# metagpt/ext/stanford_town/prompts/generate_event_triple_v1.txt

Variables: 
!<INPUT 0>! -- Persona's full name. 
!<INPUT 1>! -- Current action description
!<INPUT 2>! -- Persona's full name. 

<commentblockmarker>###</commentblockmarker>
Task: Turn the input into (subject, predicate, object). 

Input: Sam Johnson is eating breakfast. 
Output: (Dolores Murphy, eat, breakfast) 
--- 
Input: Joon Park is brewing coffee.
Output: (Joon Park, brew, coffee)
---
Input: Jane Cook is sleeping. 
Output: (Jane Cook, is, sleep)
---
Input: Michael Bernstein is writing email on a computer. 
Output: (Michael Bernstein, write, email)
---
Input: Percy Liang is teaching students in a classroom. 
Output: (Percy Liang, teach, students)
---
Input: Merrie Morris is running on a treadmill. 
Output: (Merrie Morris, run, treadmill)
---
Input: !<INPUT 0>! is !<INPUT 1>!. 
Output: (!<INPUT 2>!,
```

#### 1.4 Android Assistant - Screenshot Parse Template
```python
# metagpt/ext/android_assistant/prompts/assistant_prompt.py

screenshot_parse_template = """You are an agent that is trained to perform some basic tasks on a smartphone. You will be given a 
smartphone screenshot. The interactive UI elements on the screenshot are labeled with numeric tags starting from 1. The 
numeric tag of each interactive element is located in the center of the element.

You can call the following functions to control the smartphone:

1. tap(element: int)
This function is used to tap an UI element shown on the smartphone screen.
"element" is a numeric tag assigned to an UI element shown on the smartphone screen.
A simple use case can be tap(5), which taps the UI element labeled with the number 5.

2. text(text_input: str)
This function is used to insert text input in an input field/box. text_input is the string you want to insert and must 
be wrapped with double quotation marks. A simple use case can be text("Hello, world!"), which inserts the string 
"Hello, world!" into the input area on the smartphone screen. This function is usually callable when you see a keyboard 
showing in the lower half of the screen.

3. long_press(element: int)
This function is used to long press an UI element shown on the smartphone screen.
"element" is a numeric tag assigned to an UI element shown on the smartphone screen.
A simple use case can be long_press(5), which long presses the UI element labeled with the number 5.

4. swipe(element: int, direction: str, dist: str)
This function is used to swipe an UI element shown on the smartphone screen, usually a scroll view or a slide bar.
"element" is a numeric tag assigned to an UI element shown on the smartphone screen. "direction" is a string that 
represents one of the four directions: up, down, left, right. "direction" must be wrapped with double quotation 
marks. "dist" determines the distance of the swipe and can be one of the three options: short, medium, long. You should 
choose the appropriate distance option according to your need.
A simple use case can be swipe(21, "up", "medium"), which swipes up the UI element labeled with the number 21 for a 
medium distance.

5. grid()
You should call this function when you find the element you want to interact with is not labeled with a numeric tag and 
other elements with numeric tags cannot help with the task. The function will bring up a grid overlay to divide the 
smartphone screen into small areas and this will give you more freedom to choose any part of the screen to tap, long 
press, or swipe.
{ui_document}
The task you need to complete is to: {task_description}. Your past actions to proceed with this task are summarized as 
follows: {last_act}
Now, given the documentation and the following labeled screenshot, you need to think and call the function needed to 
proceed with the task. Your output should include three parts in the given format:

You can only take one action at a time, so please directly call the function."""
```

#### 1.5 AFlow - Problem Solving Prompts
```python
# metagpt/ext/aflow/scripts/prompts/prompt.py

ANSWER_GENERATION_PROMPT = """
Think step by step and solve the problem.
1. In the "thought" field, explain your thinking process in detail.
2. In the "answer" field, provide the final answer concisely and clearly. The answer should be a direct response to the question, without including explanations or reasoning.
Your task: {input}
"""

FORMAT_PROMPT = """
For the question described as {problem_description},
please extract a short and concise answer contains only one word/few words from the following solution: {solution}.
Make sure there are no additional comments or explanations in your response.
"""

SC_ENSEMBLE_PROMPT = """
Given the question described as follows: {question}
Several solutions have been generated to address the given question. They are as follows:
{solutions}

Carefully evaluate these solutions and identify the answer that appears most frequently across them. This consistency in answers is crucial for determining the most reliable solution.

In the "thought" field, provide a detailed explanation of your thought process. In the "solution_letter" field, output only the single letter ID (A, B, C, etc.) corresponding to the most consistent solution.
"""

PYTHON_CODE_VERIFIER_PROMPT = """
You are a professional Python programmer. Your task is to write complete, self-contained code based on a given mathematical problem and output the answer. The code should include all necessary imports and dependencies, and be ready to run without additional setup or environment configuration.

Problem description: {problem}
Other analysis: {analysis}
{feedback}

Your code should:
1. Implement the calculation steps described in the problem.
2. Define a function named `solve` that performs the calculation and returns the result.
3. `solve` function return the final calculation result.
"""

REFLECTION_ON_PUBLIC_TEST_PROMPT = """
Given a code problem and a python code solution which failed to pass test or execute, you need to analyze the reason for the failure and propose a better code solution.

### problem
{problem}

### Code Solution
{solution}

### Execution Result
{exec_pass}

#### Failed Test Case
{test_fail}

Please provide a reflection on the failed test cases and code solution, followed by a better code solution without any additional text or test cases.
"""

REVIEW_PROMPT = """
Given a problem and a thoughtful solution, your task is to using critical thinking (questioning) to review the solution's correctness and provide a review result in boolean format.

problem: {problem}
solution: {solution}

If you are more than 95 percent confident that the final answer is incorrect, please return False and give a feedback for the error. Otherwise, please return True and give a explanation for the correctness.
"""

REVISE_PROMPT = """
Given a problem and a thoughtful solution which is just reviewed as incorrect, your task is to revise the solution to solve the question and ensure the final code solution is wrapped with ```python```.

problem: {problem}
solution: {solution}
feedback: {feedback}

Ensure the output code is self-contained, and without any additional text or test cases.
"""
```

---

### 2. Tool Schemas (2)

#### 2.1 Custom Tool Example
```python
# examples/di/custom_tool.py

# Custom tool definitions for domain-specific tasks
```

#### 2.2 Android Assistant Schema
```python
# metagpt/ext/android_assistant/utils/schema.py

# Schema definitions for Android automation actions:
# - tap(element: int)
# - text(text_input: str)
# - long_press(element: int)
# - swipe(element: int, direction: str, dist: str)
# - grid()
```

---

### 3. Skills (0)

Note: MetaGPT does not include bundled SKILL.md files. The framework focuses on prompt templates and code-based agent definitions.

---

## Evaluation Dimensions

### 1. Role Clarity
- [ ] Clear separation between simulation, automation, and workflow domains
- [ ] Specialized prompts for each agent type
- [ ] Variable substitution system for prompt customization

### 2. Workflow Completeness
- [ ] Stanford Town: Daily planning → Hourly schedule → Event triples
- [ ] Android Assistant: Screenshot parsing → Action execution → Reflection
- [ ] AFlow: Problem → Solution → Review → Revision

### 3. Prompt Consistency
- [ ] Standardized variable format (!<INPUT N>!)
- [ ] Example-driven prompts (few-shot learning)
- [ ] Structured output requirements

### 4. Tool Modularity
- [ ] Function-based action schema for Android
- [ ] Custom tool integration pattern
- [ ] Code execution capabilities

### 5. Observability
- [ ] Logging and tracking of agent actions
- [ ] Reflection prompts for self-evaluation
- [ ] Review mechanism for solution validation

### 6. Extensibility
- [ ] Custom prompt template creation
- [ ] New agent type integration
- [ ] Domain-specific extension patterns

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|-----------|--------|-------------|-------|
| Role Clarity | 20% | | |
| Workflow Completeness | 25% | | |
| Prompt Consistency | 15% | | |
| Tool Modularity | 20% | | |
| Observability | 10% | | |
| Extensibility | 10% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### End-to-End Tests
1. **Stanford Town simulation**: Test complete daily planning workflow
2. **Android automation**: Test screenshot parsing and action execution
3. **AFlow problem solving**: Test code generation and review cycle

### Unit Tests
1. **Prompt variable substitution**: Verify correct variable replacement
2. **Action schema validation**: Test Android action parameter validation
3. **Solution review**: Test REVIEW_PROMPT correctness evaluation

### Integration Tests
1. **Multi-domain workflow**: Test agent switching between domains
2. **Code execution**: Verify Python code verifier functionality
3. **Reflection cycle**: Test solution revision after failed tests

---

## Notes

- **MIT license** allows full quotation and modification
- MetaGPT demonstrates **domain-specific prompt engineering**
- The Stanford Town prompts enable **social simulation** scenarios
- Android Assistant provides **mobile automation** capabilities
- AFlow demonstrates **iterative problem solving** with reflection