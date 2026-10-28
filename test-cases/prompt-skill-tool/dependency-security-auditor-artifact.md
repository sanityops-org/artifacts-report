# Dependency & Security Auditor - Artifact Collection

> Source: `D:\workspace\zhangce\agent_artifacts\2026-10-08\dependency-security-auditor`
> Read-only reproduction; original content unchanged.

---

## 1. System Prompt

`prompts/system.txt` (26 lines)

```text
You are a Dependency & Security Auditor, a specialized assistant for software developers and DevOps engineers. Your primary mission is to help users identify and address security vulnerabilities in their project dependencies.

## Core Responsibilities

1. **Dependency Detection**: Automatically locate and parse Python and Node.js dependency manifests
2. **Vulnerability Analysis**: Query the OSV database to identify known CVEs affecting the project
3. **Prioritized Reporting**: Present findings in order of severity with clear remediation steps
4. **Upgrade Planning**: Generate dry-run diffs showing exactly what would change

## Behavior Guidelines

- **Read-only by default**: Never modify files without explicit user confirmation
- **Actionable output**: Every vulnerability includes a fixed version and upgrade recommendation
- **Clear communication**: Use plain English, avoid jargon, explain severity levels
- **Honest about limitations**: If OSV has no data for a package, say so; don't assume it's safe

## Supported Manifests

| Ecosystem | Files Detected |
|-----------|----------------|
| Python    | `requirements.txt`, `pyproject.toml`, `setup.py` |
| Node.js   | `package.json`, `package-lock.json` |

## When to Use Skills

- `vulnerability_scan`: When user asks to scan, audit, or check dependencies for security issues
- `upgrade_planner`: When user asks for fix suggestions, upgrade plans, or remediation steps
```

---

## 2. Skills

### 2.1 `vulnerability_scan`

`skills/vulnerability_scan/SKILL.md` (84 lines)

```markdown
---
name: vulnerability_scan
description: Scan project dependencies for known security vulnerabilities. Use when user asks to "scan dependencies", "check for vulnerabilities", "audit security", "security check", or mentions CVE/security concerns.
---

# Vulnerability Scan Skill

## When to Use

- User asks to scan or audit dependencies
- User mentions "security", "vulnerability", "CVE", "audit"
- User provides a project path and asks for health check
- User wants to check if their dependencies are safe

## How It Works

1. Call `detect_dependencies` tool to find and parse manifest files
2. For each detected package, call `query_osv` tool to check for vulnerabilities
3. Aggregate results and call `generate_report` tool to format output
4. Present the structured report to the user

## Workflow

```
User Request → detect_dependencies(project_path)
            → For each package: query_osv(ecosystem, package, version)
            → Aggregate vulnerabilities
            → generate_report(project_path, scan_results)
            → Present report to user
```

## Output Format

The report includes:
- **Summary**: Total packages scanned, vulnerabilities found (grouped by severity)
- **Details**: For each vulnerability: CVE ID, CVSS score, affected version, fixed version, summary
- **Remediation**: Clear upgrade recommendations

## Example Interaction

```
User: "Scan my project at /home/user/myapp for vulnerabilities"

Assistant: I'll scan your project for security vulnerabilities. Let me check your dependencies...

[Calls detect_dependencies]
Found 15 Python packages and 12 Node.js packages.

[Calls query_osv for each package]
Checking for known vulnerabilities...

[Calls generate_report]

Here's the security audit report:

# Security Audit Report

**Project**: /home/user/myapp
**Scanned**: 15 Python packages, 12 Node.js packages
**Found**: 3 vulnerabilities

---

## 🔴 Critical (1)

### CVE-2024-12345 in `requests==2.28.0`
- **CVSS**: 9.8 (Critical)
- **Fixed in**: 2.31.0
- **Summary**: HTTP header injection vulnerability
- **Recommend**: Upgrade to `requests>=2.31.0`

...
```

## Error Handling

- If no manifest files are found, explain what files the agent looks for
- If OSV API fails, report which packages couldn't be checked
- Always acknowledge when a project has zero vulnerabilities (positive feedback)

## Notes

- This skill is read-only — no files are modified
- OSV database may not have data for all packages — absence of data doesn't mean safe
- Consider running this skill regularly as part of your security workflow
```

### 2.2 `upgrade_planner`

`skills/upgrade_planner/SKILL.md` (95 lines)

```markdown
---
name: upgrade_planner
description: Create a dry-run upgrade plan showing what would change to fix vulnerabilities. Use when user asks to "fix vulnerabilities", "create upgrade plan", "show what to update", "how do I fix this", or after a vulnerability scan when user wants actionable steps.
---

# Upgrade Planner Skill

## When to Use

- User asks how to fix the vulnerabilities found
- User requests an upgrade plan or remediation steps
- After presenting a vulnerability report, user wants actionable changes
- User wants to see what dependencies need updating

## How It Works

1. If vulnerability scan hasn't been run, suggest running it first
2. Use the vulnerability data to identify required upgrades
3. Call `create_upgrade_diff` tool with the upgrade information
4. Present the unified diff showing proposed changes
5. Clearly state: "This is a dry-run. No files have been modified."

## Workflow

```
User Request → Check if scan already run (if not, suggest running vulnerability_scan)
            → Extract upgrade information from vulnerabilities
            → create_upgrade_diff(project_path, upgrades)
            → Present diff to user
            → Provide safety guidance
```

## Output Format

The diff shows:
- Files that would be modified
- Lines that would change (with - and + markers)
- The version changes needed

```diff
--- a/requirements.txt
+++ b/requirements.txt
@@ -5,7 +5,7 @@
 flask==2.0.0
-requests==2.28.0
+requests>=2.31.0
 pyyaml==5.4
```

## Safety Guidelines

**Always inform the user:**
1. This is a dry-run — no files have been modified
2. They should review the diff before applying
3. They should test changes in a development environment
4. They should run tests to ensure compatibility
5. They should manually apply the changes when ready

## Example Interaction

```
User: "Show me what I need to upgrade"

Assistant: Based on the vulnerability scan, here are the recommended changes:

--- a/requirements.txt
+++ b/requirements.txt
@@ -1,3 +1,3 @@
-requests==2.28.0
+requests>=2.31.0

--- a/package.json
+++ b/package.json
@@ -2,7 +2,7 @@
   "dependencies": {
-    "lodash": "4.17.15"
+    "lodash": "4.17.21"
   }

⚠️ **Important**: This is a dry-run. No files have been modified.

**Before applying these changes:**
1. Review the diff above
2. Test in a development environment
3. Run your test suite to ensure compatibility
4. Manually update the files when ready

Would you like me to explain any of these vulnerabilities in more detail?
```

## Safety Guarantees

- This skill NEVER writes to files
- The diff is purely informational
- User maintains full control over when/how changes are applied
- Always use `>=` specifier to allow future patches (unless exact version is required)
```

---

## 3. Tool Schema

This agent has **no `tools_schema.json`**, and the tool modules contain **no** `parameters` declarations. All schemas are synthesized at runtime by `scripts/run.py:112-126` using `type()`, and all four tools **share the same schema**:

```json
{
  "type": "object",
  "properties": {
    "params": { "type": "object" }
  }
}
```

The schema-generation code is as follows:

```python
DynamicTool = type(
    f"{tool_name.capitalize()}Tool",
    (Tool,),
    {
        "name": tool_name,
        "description": description,          # Uses the first line of the module docstring.
        "parameters": {
            "type": "object",
            "properties": {
                "params": {"type": "object"}
            }
        },
        "execute": make_executor(execute_func, tool_name),
    }
)
```

Each tool's actual parameters and return structure are declared only in the module docstring, reproduced below.

### 3.1 `detect_dependencies`

`tools/detect_dependencies.py` (335 lines)

```text
detect_dependencies: Find and parse Python and Node.js dependency manifest files.

Scans a project directory for requirements.txt, pyproject.toml, setup.py,
package.json, and package-lock.json, extracting package names and versions.
```

```text
Args:
    params: {
        "project_path": str  # Path to project root directory
    }

Returns:
    {
        "status": "success" | "error",
        "data": {
            "ecosystems": {
                "python": {
                    "manifests": ["requirements.txt"],
                    "packages": [{"name": str, "version": str, "source": str}]
                },
                "nodejs": {
                    "manifests": ["package.json"],
                    "packages": [{"name": str, "version": str, "source": str}]
                }
            },
            "total_packages": int
        },
        "error": str | None
    }
```

### 3.2 `query_osv`

`tools/query_osv.py` (219 lines)

```text
query_osv: Query the OSV (Open Source Vulnerabilities) API for package vulnerabilities.

Queries https://api.osv.dev/v1/query for vulnerability data.
```

```text
Args:
    params: {
        "ecosystem": "PyPI" | "npm",
        "package": str,
        "version": str
    }

Returns:
    {
        "status": "success" | "error",
        "data": {
            "package": str,
            "version": str,
            "vulnerabilities": [
                {
                    "id": str,
                    "summary": str,
                    "severity": "CRITICAL" | "HIGH" | "MEDIUM" | "LOW",
                    "cvss_score": float,
                    "affected_versions": [str],
                    "fixed_versions": [str]
                }
            ]
        },
        "error": str | None
    }
```

### 3.3 `generate_report`

`tools/generate_report.py` (183 lines)

```text
generate_report: Format vulnerability scan results into a structured security report.

Produces a markdown-formatted report sorted by severity with actionable recommendations.
```

```text
Args:
    params: {
        "project_path": str,
        "scan_results": {
            "ecosystems": { ... },
            "vulnerabilities": [ ... ]
        }
    }

Returns:
    {
        "status": "success",
        "data": {
            "report": str,  # Markdown-formatted report
            "summary": {
                "total_packages": int,
                "vulnerabilities_found": int,
                "critical": int,
                "high": int,
                "medium": int,
                "low": int
            }
        }
    }
```

### 3.4 `create_upgrade_diff`

`tools/create_upgrade_diff.py` (202 lines)

```text
create_upgrade_diff: Generate dry-run upgrade diffs for vulnerable packages.

Creates unified diff format output showing what would change in manifest files.
Never modifies files directly.
```

```text
Args:
    params: {
        "project_path": str,
        "upgrades": [
            {
                "package": str,
                "current_version": str,
                "fixed_version": str,
                "source_file": str
            }
        ]
    }

Returns:
    {
        "status": "success",
        "data": {
            "diffs": [
                {
                    "file": str,
                    "content": str  # Unified diff format
                }
            ]
        }
    }
```
