# Code Review Assistant

A runnable code-review agent that accepts a code folder, reads the supported source files, and produces a structured review report with reasoning, tool calls, and findings.

## Features

- Detects potential bugs and security vulnerabilities
- Checks code against common best practices and design patterns
- Evaluates readability and maintainability
- Produces concrete refactoring and optimization suggestions
- Prints structured Markdown review output

Typical uses include pull-request review, pre-commit self-review, and team code-quality checks.

## Components

- **System Prompt**: `prompts/system.txt`
- **Skill**: `skills/code_review/`
  - `analyze_code`: scans code and identifies issues
  - `generate_report`: turns findings into a structured review report
- **Primary runner**: `main.py`
- **Configuration template**: `.env.example`

## Requirements

- Python 3.11+
- `sanityops-agent>=0.1.1`
- `pydantic>=2.0.0`
- `pyyaml>=6.0`
- `requests>=2.31.0`

The `sanityops-agent` package may be installed from the configured private Python package index.

## Setup

From the repository root:

```bash
cd test-cases/runnable-agent/code-review-assistant
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Create the local environment file:

```bash
cp .env.example .env
```

Edit `.env` and set at least:

```dotenv
LLM_PROVIDER=anthropic
LLM_API_KEY=your-api-key-here
```

Optional settings:

```dotenv
LLM_BASE_URL=https://api.anthropic.com
LLM_MODEL_ID=claude-sonnet-4-20250514
```

Do not commit `.env` or real API credentials.

## Run

The `main.py` entry point accepts the folder to review:

```bash
python main.py /absolute/path/to/code
```

Relative paths also work:

```bash
python main.py ../../src
python main.py .
```

The runner:

1. Loads `prompts/system.txt`
2. Recursively finds supported source files
3. Registers the `analyze_code` and `generate_report` tools
4. Calls the configured LLM provider
5. Prints thinking, tool-call, token, and final-report output

Use `python main.py --help` to view the command-line help.

### Legacy entry point

`python scripts/run.py` is retained for compatibility, but `main.py` is the primary runnable entry point for this package.

## Example

```bash
python main.py /Users/example/project/src
```

The final report is printed to standard output. The process exits with status `0` on success and a non-zero status on failure.

## Project Structure

```text
code-review-assistant/
├── README.md
├── main.py                 # Primary runnable entry point
├── .env.example            # LLM configuration template
├── agent.yaml
├── requirements.txt
├── prompts/
│   └── system.txt
├── config/
│   └── tools.yaml
├── skills/
│   └── code_review/
│       ├── skill.yaml
│       ├── handler.py
│       ├── tools/
│       │   ├── analyze_code.py
│       │   └── generate_report.py
│       └── tests/
└── scripts/
    ├── run.py              # Legacy entry point
    └── setup.py
```

## Tests

```bash
python -m pytest -q
```

The test suite covers code analysis, report generation, handler wiring, and tool registration.
