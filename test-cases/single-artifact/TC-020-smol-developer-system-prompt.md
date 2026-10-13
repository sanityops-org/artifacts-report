# TC-020: smol-developer - System Prompt Evaluation Case

## Metadata
- **Source Project**: smol-ai/developer
- **License**: MIT
- **Artifact Type**: System Prompts & Tool Definitions
- **Collection Date**: 2026-10-12
- **Collection Method**: Extracted from smol_dev/prompts.py at commit a6747d1a6ccd983c54a483c4a4fb1fa4bf740e82 (excerpt — streaming-loop bodies and `generate_code_sync()` are omitted; see the source file for the complete implementations)

## Original Artifact Content

### prompts.py (System Prompts and Tool)

```python
SMOL_DEV_SYSTEM_PROMPT = """
You are a top tier AI developer who is trying to write a program that will generate code for the user based on their intent.
Do not leave any todos, fully implement every feature requested.

When writing code, add comments to explain what you intend to do and why it aligns with the program plan and specific instructions from the original prompt.
"""


@openai_function
def file_paths(files_to_edit: List[str]) -> List[str]:
    """
    Construct a list of strings.
    """
    return files_to_edit


def specify_file_paths(prompt: str, plan: str, model: str = 'gpt-3.5-turbo-0613'):
    completion = openai.ChatCompletion.create(
        model=model,
        temperature=0.7,
        functions=[file_paths.openai_schema],
        function_call={"name": "file_paths"},
        messages=[
            {
                "role": "system",
                "content": f"""{SMOL_DEV_SYSTEM_PROMPT}
      Given the prompt and the plan, return a list of strings corresponding to the new files that will be generated.
                  """,
            },
            {
                "role": "user",
                "content": f""" I want a: {prompt} """,
            },
            {
                "role": "user",
                "content": f""" The plan we have agreed on is: {plan} """,
            },
        ],
    )
    result = file_paths.from_response(completion)
    return result


def plan(prompt: str, stream_handler: Optional[Callable[[bytes], None]] = None, model: str='gpt-3.5-turbo-0613', extra_messages: List[Any] = []):
    completion = openai.ChatCompletion.create(
        model=model,
        temperature=0.7,
        stream=True,
        messages=[
            {
                "role": "system",
                "content": f"""{SMOL_DEV_SYSTEM_PROMPT}

    In response to the user's prompt, write a plan using GitHub Markdown syntax. Begin with a YAML description of the new files that will be created.
  In this plan, please name and briefly describe the structure of code that will be generated, including, for each file we are generating, what variables they export, data schemas, id names of every DOM elements that javascript functions will use, message names, and function names.
                Respond only with plans following the above schema.
                  """,
            },
            {
                "role": "user",
                "content": f""" the app prompt is: {prompt} """,
            },
            *extra_messages,
        ],
    )


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
async def generate_code(prompt: str, plan: str, current_file: str, stream_handler: Optional[Callable[Any, Any]] = None,
                        model: str = 'gpt-3.5-turbo-0613') -> str:
    completion = openai.ChatCompletion.acreate(
        model=model,
        temperature=0.7,
        messages=[
            {
                "role": "system",
                "content": f"""{SMOL_DEV_SYSTEM_PROMPT}

  In response to the user's prompt,
  Please name and briefly describe the structure of the app we will generate, including, for each file we are generating, what variables they export, data schemas, id names of every DOM elements that javascript functions will use, message names, and function names.

  We have broken up the program into per-file generation.
  Now your job is to generate only the code for the file: {current_file}

  only write valid code for the given filepath and file type, and return only the code.
  do not add any other explanation, only return valid code for that file type.
                  """,
            },
            {
                "role": "user",
                "content": f""" the plan we have agreed on is: {plan} """,
            },
            {
                "role": "user",
                "content": f""" the app prompt is: {prompt} """,
            },
            {
                "role": "user",
                "content": f"""
    Make sure to have consistent filenames if you reference other files we are also generating.

    Remember that you must obey 3 things:
       - you are generating code for the file {current_file}
       - do not stray from the names of the files and the plan we have decided on
       - MOST IMPORTANT OF ALL - every line of code you generate must be valid code. Do not include code fences in your response, for example

    Bad response (because it contains the code fence):
    ```javascript
    console.log("hello world")
    ```

    Good response (because it only contains the code):
    console.log("hello world")

    Begin generating the code now.
    """,
            },
        ],
        stream=True,
    )
```

## Evaluation Dimensions

### 1. Three-Phase Code Generation
- [ ] Plan phase with YAML file description
- [ ] File specification phase
- [ ] Per-file code generation phase

### 2. No-Todo Guarantee
- [ ] Explicit instruction to fully implement
- [ ] No placeholders or todos allowed
- [ ] Complete feature implementation

### 3. Plan-Driven Development
- [ ] YAML file structure in plan
- [ ] Variable exports documented
- [ ] DOM IDs, message names, function names specified
- [ ] GitHub Markdown syntax

### 4. Code Quality Requirements
- [ ] Valid code only (no code fences)
- [ ] Comments for intent explanation
- [ ] Consistent filenames across files
- [ ] Stream-based output

### 5. Tool Integration
- [ ] OpenAI function calling for file_paths
- [ ] Function schema injection
- [ ] Structured response extraction

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Three-Phase Code Generation | 25% | | |
| No-Todo Guarantee | 20% | | |
| Plan-Driven Development | 25% | | |
| Code Quality Requirements | 20% | | |
| Tool Integration | 10% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Simple app generation flow
2. Multi-file code generation
3. Plan with complete specifications
4. Code fence removal validation

### Boundary Test Cases
1. Large application generation
2. Complex DOM structures
3. Many interdependent files
4. Streaming output handling

### Negative Test Cases
1. Incomplete features with todos
2. Inconsistent filenames
3. Code fences in output
4. Missing plan alignment

## Notes
- smol-developer is a minimal but effective code generation agent
- Three-phase approach: Plan -> Specify Files -> Generate Code
- Strong emphasis on no placeholders and complete implementation
- MIT license allows full quotation and modification