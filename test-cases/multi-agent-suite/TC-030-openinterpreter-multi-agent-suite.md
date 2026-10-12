# TC-030: Open Interpreter - Multi-Agent Suite

## Metadata
- **Source Project**: Open Interpreter (openinterpreter/openinterpreter)
- **Commit SHA**: ac1fcc8fe57aba51fcc3c79afd57a0883237fe87
- **License**: Apache-2.0
- **Artifact Type**: Code Execution Agent
- **Collection Date**: 2025-10-12
- **Collection Method**: GitHub API content extraction from verified commit

---

## Project Overview

Open Interpreter is a **code execution agent** that enables natural language control of computers through code execution. It includes an approval system for safe execution and skills for code review and PR workflows.

### Core Capabilities

| Capability | Description | Primary Artifact Type |
|------------|-------------|----------------------|
| **Approval System** | Policy-based execution approval | Tool Schema |
| **Code Review** | Multi-aspect code review orchestration | Skill |
| **PR Body Generation** | Pull request documentation | Skill |

---

## Logical Artifact Inventory

### 1. System Prompts (0)

Note: Open Interpreter core system prompts are defined in the codebase. This test case focuses on the **approval system and bundled skills**.

---

### 2. Tool Schemas (1)

#### 2.1 Approvals System
```rust
// codex-rs/core/src/tools/approvals.rs

//! Central approval policy-stage execution and reviewer routing.

#[derive(Clone)]
pub(crate) struct ApprovalContext {
    pub(crate) review_context: GuardianReviewContext,
    pub(crate) cancellation_token: Option<CancellationToken>,
    pub(crate) call_id: String,
    pub(crate) tool_name: ToolName,
    pub(crate) strict_auto_review: bool,
    pub(crate) approval_reason: Option<String>,
    pub(crate) retry_reason: Option<String>,
    pub(crate) network_approval_context: Option<NetworkApprovalContext>,
}

#[derive(Clone, Debug, PartialEq, serde::Serialize)]
#[serde(tag = "tool", rename_all = "snake_case")]
pub(crate) enum ApprovalAction {
    ExecCommand {
        id: String,
        environment_id: String,
        command: Vec<String>,
        #[serde(skip_serializing)]
        hook_command: String,
        cwd: PathUri,
        sandbox_permissions: SandboxPermissions,
        additional_permissions: Option<AdditionalPermissionProfile>,
        justification: Option<String>,
        tty: bool,
        proposed_execpolicy_amendment: Option<ExecPolicyAmendment>,
    },
    WriteStdin {
        id: String,
        approval_id: String,
        environment_id: String,
        process_id: i32,
        input: String,
        cwd: PathUri,
        tty: bool,
        sandbox_permissions: SandboxPermissions,
        additional_permissions: Option<AdditionalPermissionProfile>,
    },
    #[cfg(unix)]
    Execve {
        id: String,
        approval_id: String,
        environment_id: String,
        source: GuardianCommandSource,
        program: AbsolutePathBuf,
        argv: Vec<String>,
        command: Vec<String>,
        cwd: AbsolutePathBuf,
        additional_permissions: Option<AdditionalPermissionProfile>,
    },
    ApplyPatch {
        id: String,
        environment_id: String,
        cwd: PathUri,
        files: Vec<PathUri>,
        patch: String,
        #[serde(skip_serializing)]
        changes: Arc<HashMap<PathBuf, FileChange>>,
        permissions_preapproved: bool,
    },
    McpToolCall {
        id: String,
        server: String,
        tool_name: String,
        arguments: Option<serde_json::Value>,
        connector_id: Option<String>,
        connector_name: Option<String>,
        connector_description: Option<String>,
        connected_account_email: Option<String>,
        tool_title: Option<String>,
        tool_description: Option<String>,
        annotations: Option<crate::guardian::GuardianMcpAnnotations>,
        #[serde(skip_serializing)]
        hook_tool_name: HookToolName,
        approval_policy: AskForApproval,
        reviewer: ApprovalsReviewer,
        approval_mode: AppToolApproval,
        allow_session_remember: bool,
        allow_persistent_approval: bool,
    },
    NetworkAccess {
        id: String,
        turn_id: String,
        environment_id: String,
        target: String,
        host: String,
        protocol: NetworkApprovalProtocol,
        port: u16,
        trigger: Option<GuardianNetworkAccessTrigger>,
        #[serde(skip_serializing)]
        hook_command: String,
        #[serde(skip_serializing)]
        hook_run_id: String,
        command: Vec<String>,
        cwd: AbsolutePathBuf,
    },
    RequestPermissions {
        // Permission request fields
    },
}
```

---

### 3. Skills (4)

#### 3.1 Code Review (Orchestrator)
```markdown
# .codex/skills/code-review/SKILL.md

---
name: code-review
description: Run a final code review on a pull request
---

Use subagents to review code using all code-review-* skills other than this orchestrator. One subagent per skill. Pass full skill path to subagents. Use xhigh reasoning.

You must return every single issue from every subagent. You can return an unlimited number of findings.
Use raw Markdown to report findings.
Number findings for ease of reference.
Each finding must include a specific file path and line number.

If the GitHub user running the review is the owner of the pull request add a `code-reviewed` label.
Do not leave GitHub comments unless explicitly asked.
```

#### 3.2 Code Review Breaking Changes
```markdown
# .codex/skills/code-review-breaking-changes/SKILL.md

---
name: code-review-breaking-changes
description: Review code for breaking changes that could affect downstream consumers
---

# Breaking Changes Review

Identify breaking changes including:
- API signature modifications
- Behavior changes that break backward compatibility
- Removed or renamed functions/classes
- Changed return types
- Modified error handling
```

#### 3.3 Code Review Context
```markdown
# .codex/skills/code-review-context/SKILL.md

---
name: code-review-context
description: Review code for context-aware issues and dependencies
---

# Context Review

Analyze code for:
- Missing context or dependencies
- Implicit assumptions
- Environment-specific behavior
- Resource lifecycle issues
```

#### 3.4 Codex PR Body
```markdown
# .codex/skills/codex-pr-body/SKILL.md

---
name: codex-pr-body
description: Update the title and body of one or more pull requests.
---

## Determining the PR(s)

When this skill is invoked, the PR(s) to update may be specified explicitly, but in the common case, the PR(s) to update will be inferred from the branch / commit that the user is currently working on. For ordinary Git usage (i.e., not Sapling as discussed below), you may have to use a combination of `git branch` and `gh pr view <branch> --repo openai/codex --json number --jq '.number'` to determine the PR associated with the current branch / commit.

## PR Body Contents

When invoked, use `gh` to edit the pull request body and title to reflect the contents of the specified PR. Make sure to check the existing pull request body to see if there is key information that should be preserved. For example, NEVER remove an image in the existing pull request body, as the author may have no way to recover it if you remove it.

It is critically important to explain _why_ the change is being made. If the current conversation in which this skill is invoked has discussed the motivation, be sure to capture this in the pull request body.

The body should also explain _what_ changed, but this should appear after the _why_.

Limit discussion to the _net change_ of the commit. It is generally frowned upon to discuss changes that were attempted but later undone in the course of the development of the pull request. When rewriting the pull request body, you may need to eliminate details such as these when they are no longer appropriate / of interest to future readers.

Avoid references to absolute paths on my local disk. When talking about a path that is within the repository, simply use the repo-relative path.

Avoid references to confidential information including but not limited to codenames or OpenAI-internal URLs.

It is generally helpful to discuss how the change was verified. That said, it is unnecessary to mention things that CI checks automatically, e.g., do not include "ran `just fmt`" as part of the test plan. Though identifying the new tests that were purposely introduced to verify the new behavior introduced by the pull request is often appropriate.

Make use of Markdown to format the pull request professionally. Ensure "code things" appear in single backticks when referenced inline. Fenced code blocks are useful when referencing code or showing a shell transcript. Also, make use of GitHub permalinks when citing existing pieces of code that are relevant to the change.

Make sure to reference any relevant pull requests or issues, though there should be no need to reference the pull request in its own PR body.

If there is documentation that should be updated on https://developers.openai.com/codex as a result of this change, please note that in a separate section near the end of the pull request. Omit this section if there is no documentation that needs to be updated.

## Working with Stacks

Sometimes a pull request is composed of a stack of commits that build on one another. In these cases, the PR body should reflect the _net_ change introduced by the stack as a whole, rather than the individual commits that make up the stack.

Similarly, sometimes a user may be using a tool like Sapling to leverage _stacked pull requests_, in which case the `base` of the PR may be the a branch that is the `head` of another PR in the stack rather than `main`. In this case, be sure to discuss only the net change between the `base` and `head` of the PR that is being opened against that stacked base, rather than the changes relative to `main`.

## Sapling

If `.git/sl/store` is present, then this Git repository is governed by Sapling SCM (https://sapling-scm.com).

In Sapling, run the following to see if there is a GitHub pull request associated with the current revision:

```shell
sl log --template '{github_pull_request_url}' -r .
```

Alternatively, you can run `sl sl` to see the current development branch and whether there is a GitHub pull request associated with the current commit. For example, if the output were:

```
  @  cb032b31cf  72 minutes ago  mbolin  #11412
╭─╯  tui: show non-file layer content in /debug-config
│
o  fdd0cd1de9  Today at 20:09  origin/main
│
~
```

- `@` indicates the current commit is `cb032b31cf`
- it is a development branch containing a single commit branched off of `origin/main`
- it is associated with GitHub pull request #11412
```

---

## Evaluation Dimensions

### 1. Role Clarity
- [ ] Clear separation between approval system and skills
- [ ] Each skill has specific trigger conditions
- [ ] Orchestrator skill coordinates subagent skills

### 2. Workflow Completeness
- [ ] Multi-aspect code review (breaking changes, context)
- [ ] PR body generation with Git/GitHub integration
- [ ] Approval workflow for safe execution

### 3. Prompt Consistency
- [ ] Standardized skill format with name and description
- [ ] Clear instructions for PR body content
- [ ] Multi-tool integration patterns

### 4. Tool Modularity
- [ ] ApprovalAction enum covers multiple tool types
- [ ] Sandbox permissions management
- [ ] MCP tool call integration

### 5. Observability
- [ ] Approval request tracking
- [ ] Line-specific findings in code review
- [ ] Git history analysis

### 6. Extensibility
- [ ] Additional code review skills can be added
- [ ] Custom approval actions
- [ ] Sapling SCM integration

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
1. **Code review workflow**: Test orchestrator skill with all sub-skills
2. **PR body generation**: Test with actual pull requests
3. **Approval workflow**: Test various approval actions

### Unit Tests
1. **Approval action parsing**: Verify ApprovalAction enum handling
2. **Skill matching**: Test correct skill activation from descriptions
3. **PR discovery**: Test Git branch to PR mapping

### Integration Tests
1. **GitHub API**: Test `gh` command integration
2. **Sapling SCM**: Test Sapling-specific workflows
3. **Stacked PRs**: Test stacked PR body generation

---

## Notes

- **Apache-2.0 license** allows full quotation and modification
- Open Interpreter emphasizes **safe code execution** with approval system
- Skills focus on **code review and PR workflows**
- The orchestrator pattern enables **multi-agent code review**