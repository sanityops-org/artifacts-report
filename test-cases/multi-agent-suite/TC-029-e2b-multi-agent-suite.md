# TC-029: E2B - Multi-Agent Suite

## Metadata
- **Source Project**: E2B (e2b-dev/E2B)
- **Commit SHA**: df6c368152b067512702fc677952c0fc4e13c2f0
- **License**: Apache-2.0
- **Artifact Type**: Sandbox Platform
- **Collection Date**: 2026-10-12
- **Collection Method**: GitHub API content extraction from verified commit

---

## Project Overview

E2B is a **sandbox runtime platform** for AI agents, providing secure isolated execution environments. The platform offers SDKs for JavaScript and Python, CLI tools, and a skill system for common workflows.

### Core Capabilities

| Capability | Description | Primary Artifact Type |
|------------|-------------|----------------------|
| **Sandbox API** | Secure code execution environment | Tool Schema |
| **Stripe Projects** | Provisioning workflow integration | Skill |

---

## Logical Artifact Inventory

### 1. System Prompts (0)

Note: E2B is a platform for agent execution rather than an agent framework. It does not include fixed agent prompts.

---

### 2. Tool Schemas (1)

#### 2.1 Sandbox API
```python
# packages/python-sdk/e2b/sandbox_sync/main.py

class Sandbox(SandboxApi):
    """E2B cloud sandbox is a secure and isolated cloud environment.

     The sandbox allows you to:
     - Access Linux OS
     - Create, list, and delete files and directories
     - Run commands
     - Run isolated code
     - Access the internet

     Check docs [here](https://e2b.dev/docs).

     Use the `Sandbox.create()` to create a new sandbox.

     Example:
     ```python
     from e2b import Sandbox

     sandbox = Sandbox.create()
     ```
     """
```

*(Note — the shared base is `class SandboxBase(ClientFactory)` in `packages/python-sdk/e2b/sandbox/main.py`, with the async variant in `e2b/sandbox_async/main.py`; the direct constructor is deprecated in favor of `Sandbox.create()`. `e2b/sandbox/` is a package directory, not a single module.)*

---

### 3. Skills (1)

#### 3.1 Stripe Projects Skill (excerpt — two intermediate passages omitted: an extra credentials-export paragraph with a second `env_value` block after the "Stripe Projects CLI" section, and the `e2b sandbox resume` / `sandbox exec` guidance inside the "E2B CLI" section)
```markdown
# skills/stripe-projects/SKILL.md

---
name: stripe-projects
description: "Use after E2B sandbox/API access has been provisioned through Stripe Projects and the user needs to use the resulting E2B API key with the E2B CLI, JavaScript SDK, Python SDK, or Code Interpreter SDK."
---

# E2B Stripe Projects

Use these patterns after E2B sandbox/API access has been provisioned through Stripe Projects.

## Credentials

- Stripe Projects provisions E2B sandbox/API access and returns an E2B team API key.
- Use that key as `E2B_API_KEY` for sandbox creation, sandbox control, and SDK clients.
- Prefer setting `E2B_API_KEY` explicitly in runtime environments so commands and SDK calls use the intended E2B team.
- Local defaults can also come from `.env.local` or `~/.e2b/config.json`.
- In Stripe Projects checkouts, the E2B CLI may not be globally logged in. Before using `e2b sandbox ...`, prefer a Stripe Projects env pull plus per-command export instead of trying `e2b auth login`.
- Do not print secret values. `stripe projects env --json` can return redacted placeholders, so do not use it as the source for a runnable `E2B_API_KEY`. Pull the managed env file, then read only the needed E2B variables into the command environment without echoing them.

```bash
stripe projects env --pull --yes
env_value() {
  awk -F= -v key="$1" '$1 == key {sub(/^[^=]*=/, ""); gsub(/^"|"$/, ""); print; exit}' .env
}
export E2B_API_KEY="$(env_value E2B_API_KEY)"
export E2B_API_URL="$(env_value E2B_API_URL)"
export E2B_DOMAIN="$(env_value E2B_DOMAIN)"
e2b sandbox create base --detach
```

## Stripe Projects CLI

Add E2B to the current Stripe project:

```bash
stripe projects add e2b/sandboxes
```

Inspect or pull provisioned credentials:

```bash
stripe projects env
stripe projects env --json
stripe projects env --pull --yes
```

## E2B CLI

If the E2B CLI is missing or a shell shim is broken, install it with Node instead of switching to SDK code:

```bash
if ! e2b --version >/dev/null 2>&1; then
  npm install -g @e2b/cli
fi
```

The CLI package requires Node 20 or newer.

Prefer detached sandboxes for non-interactive work so the command returns a sandbox ID and does not attach an interactive terminal:

```bash
e2b sandbox create --detach
e2b sandbox create base --detach
```

Run shell commands in a sandbox with `--` before shell flags so the CLI does not parse them:

```bash
e2b sandbox exec <sandbox_id> -- bash -lc 'pwd && ls -la'
```

For long-running processes, run them in the background and write a PID file in the sandbox:

```bash
e2b sandbox exec <sandbox_id> -- bash -lc 'nohup python server.py >server.log 2>&1 & echo $! >server.pid'
```

## JavaScript SDK

Use `Sandbox.create()` with `E2B_API_KEY` for a fresh sandbox:

```ts
import Sandbox from 'e2b'

const sandbox = await Sandbox.create('base')
const result = await sandbox.commands.run('echo "hello from e2b"')
console.log(result.stdout)
```

Use lifecycle options when the sandbox should pause on timeout and resume on later activity:

```ts
const sandbox = await Sandbox.create('base', {
  lifecycle: { onTimeout: 'pause', autoResume: true },
})
```

Use `Sandbox.connect()` when a CLI step already created the sandbox:

```ts
import Sandbox from 'e2b'

const sandbox = await Sandbox.connect(process.env.SANDBOX_ID!)
const result = await sandbox.commands.run('cat important_file.md')
console.log(result.stdout)
```

## Python SDK

Use the context manager with `E2B_API_KEY` for short-lived tasks:

```py
from e2b import Sandbox

with Sandbox.create("base") as sandbox:
    result = sandbox.commands.run('echo "hello from e2b"')
    print(result.stdout)
```

Use lifecycle options when the sandbox should pause on timeout and resume on later activity:

```py
sandbox = Sandbox.create(
    "base",
    lifecycle={"on_timeout": "pause", "auto_resume": True},
)
```

For workflows that share a sandbox across steps, keep the sandbox ID and connect to it later:

```py
from e2b import Sandbox

sandbox = Sandbox.connect(sandbox_id)
result = sandbox.commands.run("cat important_file.md")
print(result.stdout)
```

## Practical Defaults

- Use the `base` template unless a task requires a specific template.
- Prefer `bash -lc` for multi-command CLI execution.
- Put temporary files under `/tmp` or the current working directory inside the sandbox unless the task requires a specific path.
- For workloads that need code execution with `run_code` or `runCode`, use the Code Interpreter SDK.
```

---

## Evaluation Dimensions

### 1. Role Clarity
- [ ] Clear separation between sandbox creation, control, and SDK usage
- [ ] Lifecycle management (pause/resume) well-defined
- [ ] CLI vs SDK usage patterns clearly distinguished

### 2. Workflow Completeness
- [ ] Sandbox creation with templates
- [ ] Command execution and process management
- [ ] Credential provisioning through Stripe Projects

### 3. Prompt Consistency
- [ ] Standardized skill format with name and description
- [ ] Clear code examples for each SDK
- [ ] Practical defaults documented

### 4. Tool Modularity
- [ ] Python SDK with context manager pattern
- [ ] JavaScript SDK with async/await
- [ ] CLI for shell-based workflows

### 5. Observability
- [ ] Sandbox ID tracking
- [ ] Process output capture
- [ ] Timeout and lifecycle events

### 6. Extensibility
- [ ] Custom templates
- [ ] Additional SDK methods
- [ ] Integration patterns

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
1. **Sandbox lifecycle**: Test create, pause, resume, and destroy
2. **Multi-language execution**: Test Python and JavaScript SDKs
3. **CLI workflow**: Test sandbox creation and command execution via CLI

### Unit Tests
1. **Sandbox creation**: Verify template selection and configuration
2. **Command execution**: Test various command types and outputs
3. **Lifecycle management**: Test timeout and auto-resume

### Integration Tests
1. **Stripe Projects**: Test credential provisioning flow
2. **Long-running processes**: Test background execution
3. **File operations**: Test file read/write in sandbox

---

## Notes

- **Apache-2.0 license** allows full quotation and modification
- E2B is a **platform** for secure sandbox execution, not an agent framework
- The Stripe Projects skill demonstrates **provisioning integration**
- SDKs support both **Python and JavaScript** with similar APIs