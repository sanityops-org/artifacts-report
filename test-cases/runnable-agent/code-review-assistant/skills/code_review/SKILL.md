---
name: code_review
description: "Code Review Skills - Professional Code Quality Inspection"
version: "1.0.0"
---

# Code Review Skill

Professional code review skills can identify potential problems in the code and provide suggestions for improvement.

## Function

- **Security review**: Detect security risks such as SQL injection, sensitive information leakage, dynamic code execution, etc.
- **Readability check**: Check variable naming, code line length and other readability issues
- **Maintainability check**: Check the function length, document string and other maintainability issues
- **Performance check**: Check performance problems such as inefficient cycle

## Tool

### analyze_code
Analyze code files to identify potential problems.

Parameter:
- `code` (required): The content of the code to be analyzed
- `language` (required): Programming language (python, javascript, typescript, java, go, rust, cpp, csharp, ruby, php)
- `focus_areas` (optional): List of areas of concern (security, performance, readability, maintainability)

### generate_report
Generate a structured code review report.

Parameter:
- `findings` (required): Review the list of problems found
- `include_examples` (optional): Whether to include sample code, default true

## Examples of use

```python
from skills.code_review.handler import run

result = run({
    "code": "def hello(): print('hello')",
    "language": "python",
    "focus_areas": ["security", "readability"]
})

print(result["data"]["report"])
```

## Output format

Return to the structured review report, including:

1. Overall evaluation
2. Problem statistics (Critical/High/Medium/Low)
3. Details of the problem
4. Suggestions for improvement
5. Positive feedback
