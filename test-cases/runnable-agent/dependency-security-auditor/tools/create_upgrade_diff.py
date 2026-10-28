#!/usr/bin/env python3
"""
create_upgrade_diff: Generate dry-run upgrade diffs for vulnerable packages.

Creates unified diff format output showing what would change in manifest files.
Never modifies files directly.
"""

import json
import re
from pathlib import Path
from typing import Any, Dict, List


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a dry-run diff for upgrading vulnerable packages.

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
    """
    project_path = params.get("project_path")
    upgrades = params.get("upgrades", [])

    if not project_path:
        return {"status": "error", "error": "project_path parameter is required"}

    if not upgrades:
        return {
            "status": "success",
            "data": {
                "diffs": [],
                "message": "No upgrades needed."
            }
        }

    # Group upgrades by source file
    upgrades_by_file: Dict[str, List[Dict]] = {}
    for upgrade in upgrades:
        source_file = upgrade.get("source_file", "unknown")
        if source_file not in upgrades_by_file:
            upgrades_by_file[source_file] = []
        upgrades_by_file[source_file].append(upgrade)

    diffs = []

    for source_file, file_upgrades in upgrades_by_file.items():
        file_path = Path(project_path) / source_file

        if not file_path.exists():
            continue

        # Read original content
        original_content = file_path.read_text(encoding="utf-8")
        original_lines = original_content.splitlines(keepends=True)

        # Create modified content
        modified_lines = _apply_upgrades(original_lines, file_upgrades, source_file)

        # Generate unified diff
        diff_content = _create_unified_diff(
            original_lines,
            modified_lines,
            source_file
        )

        diffs.append({
            "file": source_file,
            "content": diff_content
        })

    return {
        "status": "success",
        "data": {
            "diffs": diffs,
            "note": "This is a dry-run. No files have been modified."
        }
    }


def _apply_upgrades(
    original_lines: List[str],
    upgrades: List[Dict],
    source_file: str
) -> List[str]:
    """Apply upgrades to file lines, returning modified lines."""
    modified_lines = original_lines.copy()

    for upgrade in upgrades:
        package = upgrade["package"]
        current_version = upgrade["current_version"]
        fixed_version = upgrade["fixed_version"]

        for i, line in enumerate(modified_lines):
            if source_file == "requirements.txt":
                # Match package==version or package>=version etc.
                pattern = rf"^{package}\s*(==|>=|<=|~=)\s*{re.escape(current_version)}"
                if re.search(pattern, line, re.IGNORECASE):
                    # Replace with >= specifier to allow future patches
                    modified_lines[i] = re.sub(
                        rf"^{package}\s*(==|>=|<=|~=)\s*{re.escape(current_version)}",
                        f"{package}>={fixed_version}",
                        line,
                        flags=re.IGNORECASE
                    )

            elif source_file == "package.json":
                # Match "package": "version"
                pattern = rf'"{package}"\s*:\s*"{re.escape(current_version)}"'
                if re.search(pattern, line):
                    modified_lines[i] = re.sub(
                        rf'"{package}"\s*:\s*"{re.escape(current_version)}"',
                        f'"{package}": "{fixed_version}"',
                        line
                    )

            elif source_file == "pyproject.toml":
                # Match package with version specifier
                pattern = rf'{package}\s*(==|>=|<=|~=)\s*{re.escape(current_version)}'
                if re.search(pattern, line):
                    modified_lines[i] = re.sub(
                        rf'{package}\s*(==|>=|<=|~=)\s*{re.escape(current_version)}',
                        f"{package}>={fixed_version}",
                        line
                    )

    return modified_lines


def _create_unified_diff(
    original_lines: List[str],
    modified_lines: List[str],
    filename: str
) -> str:
    """Create a unified diff string."""
    diff_lines = []

    # Diff header
    diff_lines.append(f"--- a/{filename}")
    diff_lines.append(f"+++ b/{filename}")

    # Find changes
    # Simple approach: find lines that changed
    original_set = set(enumerate(original_lines))
    modified_set = set(enumerate(modified_lines))

    # Build diff hunks
    # For simplicity, we'll output a minimal diff showing changed lines
    for i, (orig, mod) in enumerate(zip(original_lines, modified_lines)):
        if orig != mod:
            # Found a change - output context around it
            start = max(0, i - 2)
            end = min(len(original_lines), i + 3)

            diff_lines.append(f"@@ -{start + 1},{end - start} +{start + 1},{end - start} @@")

            for j in range(start, end):
                if j < len(original_lines):
                    if original_lines[j] != modified_lines[j]:
                        diff_lines.append(f"-{original_lines[j].rstrip()}")
                        diff_lines.append(f"+{modified_lines[j].rstrip()}")
                    else:
                        diff_lines.append(f" {original_lines[j].rstrip()}")

    return "\n".join(diff_lines)


if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            params = json.load(f)
        result = execute(params)
        for diff in result["data"]["diffs"]:
            print(f"=== {diff['file']} ===")
            print(diff["content"])
    else:
        print("Usage: python create_upgrade_diff.py <params.json>")