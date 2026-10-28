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