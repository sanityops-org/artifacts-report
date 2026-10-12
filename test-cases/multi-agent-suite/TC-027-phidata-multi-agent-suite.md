# TC-027: Agno (formerly Phidata) - Multi-Agent Suite

## Metadata
- **Source Project**: Agno (agno-agi/agno; formerly phidatahq/phidata)
- **Commit SHA**: 7decd1e45f6a67890ee6a5aa03f3fe9c356be972
- **License**: Apache-2.0
- **Artifact Type**: Multi-Agent Platform
- **Collection Date**: 2026-10-12
- **Collection Method**: GitHub API content extraction from verified commit

---

## Project Overview

Agno, formerly Phidata, is an **agent platform** that provides a streamlined way to build AI agents with instructions, tools, and skills. The framework emphasizes simplicity and modularity for building production-ready agents. (At the pinned commit the package, imports, and README all use the `agno` identity; phidatahq/phidata redirects to agno-agi/agno.)

### Core Capabilities

| Capability | Description | Primary Artifact Type |
|------------|-------------|----------------------|
| **Agent Instructions** | Declarative agent behavior definition | System Prompt |
| **Callable Tools** | Dynamic tool loading based on context | Tool Schema |
| **Session State** | Per-user/session tool customization | Tool Schema |
| **Skills** | Reusable behavior patterns | Skill |

---

## Logical Artifact Inventory

### 1. System Prompts (1)

#### 1.1 Agent with Instructions
```python
# cookbook/02_agents/01_quickstart/agent_with_instructions.py

"""
Agent With Instructions
=============================

Agent With Instructions Quickstart.
"""

from agno.agent import Agent
from agno.models.openai import OpenAIResponses

# ---------------------------------------------------------------------------
# Agent Instructions
# ---------------------------------------------------------------------------
instructions = """\
You are a concise assistant.
Answer with exactly 3 bullet points when possible.\
"""

# ---------------------------------------------------------------------------
# Create Agent
# ---------------------------------------------------------------------------
agent = Agent(
    name="Instruction-Tuned Agent",
    model=OpenAIResponses(id="gpt-5.2"),
    instructions=instructions,
)

# ---------------------------------------------------------------------------
# Run Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent.print_response("How can I improve my Python debugging workflow?", stream=True)
```

---

### 2. Tool Schemas (2)

#### 2.1 Callable Tools Factory
```python
# cookbook/02_agents/04_tools/01_callable_tools.py

"""
Callable Tools Factory
======================
Pass a function as `tools` instead of a list. The function is called
at the start of each run, so the toolset can vary per user or session.

The factory receives parameters by name via signature inspection:
- agent: the Agent instance
- run_context: the current RunContext (has user_id, session_id, etc.)
- session_state: the current session state dict

Results are cached per user_id (or session_id) by default.
"""

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.run import RunContext

# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


def search_web(query: str) -> str:
    """Search the web for information."""
    return f"Search results for: {query}"


def search_internal_docs(query: str) -> str:
    """Search internal documentation (admin only)."""
    return f"Internal doc results for: {query}"


def get_account_balance(account_id: str) -> str:
    """Get account balance (finance only)."""
    return f"Balance for {account_id}: $42,000"


# ---------------------------------------------------------------------------
# Callable Factory
# ---------------------------------------------------------------------------


def tools_for_user(run_context: RunContext):
    """Return different tools based on the user's role stored in session_state."""
    role = (run_context.session_state or {}).get("role", "viewer")
    print(f"--> Resolving tools for role: {role}")

    base_tools = [search_web]
    if role == "admin":
        base_tools.append(search_internal_docs)
    if role in ("admin", "finance"):
        base_tools.append(get_account_balance)

    return base_tools


# ---------------------------------------------------------------------------
# Create Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=OpenAIResponses(id="gpt-5-mini"),
    tools=tools_for_user,
    instructions=[
        "You are a helpful assistant.",
        "Use the tools available to you to answer the user's question.",
    ],
)


# ---------------------------------------------------------------------------
# Run Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Run 1: viewer role - only search_web available
    # Each user_id gets its own cached toolset
    print("=== Run as viewer ===")
    agent.print_response(
        "Search for recent news about AI agents",
        user_id="viewer_user",
        session_state={"role": "viewer"},
        stream=True,
    )

    # Run 2: admin role - all tools available
    # Different user_id means the factory is called again with new context
    print("\n=== Run as admin ===")
    agent.print_response(
        "Search internal docs for the deployment guide and check account balance for ACC-001",
        user_id="admin_user",
        session_state={"role": "admin"},
        stream=True,
    )
```

#### 2.2 Session State Tools
```python
# cookbook/02_agents/04_tools/02_session_state_tools.py

"""
Session State Tools
===================
Use `session_state` as a parameter name in your factory to receive
the session state dict directly (no need for run_context).

Set `cache_callables=False` so the factory runs fresh every time,
picking up any session_state changes between runs.
"""


def get_tools(session_state: dict):
    """Pick tools based on the 'mode' key in session_state."""
    mode = session_state.get("mode", "greet")

    if mode == "greet":
        return [get_greeting]
    else:
        return [get_farewell]


agent = Agent(
    model=OpenAIResponses(id="gpt-5-mini"),
    tools=get_tools,
    cache_callables=False,
    instructions=["Use the available tool to respond."],
)
```

*(Note — each sample skill under `cookbook/02_agents/16_skills/sample_skills/` also ships `references/` and `scripts/` (e.g., code-review/references/style-guide.md, code-review/scripts/check_style.py, git-workflow/references/commit-types.md, git-workflow/scripts/commit_message.py), and cookbook/02_agents/16_skills/basic_skills.py demonstrates `agno.skills.LocalSkills`.)*

---

### 3. Skills (2)

#### 3.1 Code Review Skill
```markdown
# cookbook/02_agents/16_skills/sample_skills/code-review/SKILL.md

---
name: code-review
description: Code review assistance with linting, style checking, and best practices
license: Apache-2.0
metadata:
  version: "1.0.0"
  author: agno-team
  tags: ["quality", "review", "linting"]
---
# Code Review Skill

You are a code review assistant. When reviewing code, follow these steps:

## Review Process
1. **Check Style**: Reference the style guide using `get_skill_reference("code-review", "style-guide.md")`
2. **Run Style Check**: Use `get_skill_script("code-review", "check_style.py")` for automated style checking
3. **Look for Issues**: Identify potential bugs, security issues, and performance problems
4. **Provide Feedback**: Give structured feedback with severity levels

## Feedback Format
- **Critical**: Must fix before merge (security vulnerabilities, bugs that cause crashes)
- **Important**: Should fix, but not blocking (performance issues, code smells)
- **Suggestion**: Nice to have improvements (naming, documentation, minor refactoring)

## Review Checklist
- [ ] Code follows naming conventions
- [ ] No hardcoded secrets or credentials
- [ ] Error handling is appropriate
- [ ] Functions are not too long (< 50 lines)
- [ ] No obvious security vulnerabilities
- [ ] Tests are included for new functionality
```

#### 3.2 Git Workflow Skill (excerpt)
```markdown
# cookbook/02_agents/16_skills/sample_skills/git-workflow/SKILL.md

---
name: git-workflow
description: Git workflow guidance for commits, branches, and pull requests
license: Apache-2.0
metadata:
  version: "1.0.0"
  author: agno-team
  tags: ["git", "version-control", "workflow"]
---
# Git Workflow Skill

You are a Git workflow assistant. Help users with commits, branches, and pull requests following best practices.

## Commit Message Guidelines

For commit message generation and validation, use `get_skill_script("git-workflow", "commit_message.py")`.

### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation only
- **style**: Formatting, no code change
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **perf**: Performance improvement
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

(The file continues with commit message examples, Branch Naming (`<type>/<ticket-id>-<short-description>`), Pull Request Guidelines with a description template, and Common Commands.)
```

---

## Evaluation Dimensions

### 1. Role Clarity
- [ ] Clear separation between instructions, tools, and skills
- [ ] Role-based tool access control
- [ ] Session-specific agent behavior

### 2. Workflow Completeness
- [ ] Dynamic tool loading based on context
- [ ] Session state management
- [ ] Per-user tool caching

### 3. Prompt Consistency
- [ ] Declarative instruction format
- [ ] String-based instruction definition
- [ ] Multi-instruction support

### 4. Tool Modularity
- [ ] Callable tool factory pattern
- [ ] Function-based tool definitions
- [ ] Role-based tool filtering

### 5. Observability
- [ ] Streaming response support
- [ ] Run context tracking
- [ ] User/session identification

### 6. Extensibility
- [ ] Custom skill creation
- [ ] Tool factory pattern
- [ ] Session state injection

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
1. **Role-based tool access**: Test viewer vs admin tool availability
2. **Session state propagation**: Verify session_state reaches tools
3. **Skill activation**: Test skill-based code review

### Unit Tests
1. **Tool factory resolution**: Verify correct tools returned per role
2. **Instruction assembly**: Test instruction string construction
3. **Session caching**: Verify tool caching per user_id

### Integration Tests
1. **Multi-user sessions**: Test concurrent users with different roles
2. **Tool execution**: Verify tool call with session context
3. **Skill loading**: Test skill disclosure and execution

---

## Notes

- **Apache-2.0 license** allows full quotation and modification
- Agno (formerly Phidata) emphasizes **simplicity and modularity** in agent construction
- The callable tools factory enables **context-aware tool loading**
- Session state provides **per-user personalization**