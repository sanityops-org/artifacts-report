#!/usr/bin/env python3
"""Initialization check script."""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent

REQUIRED_DIRS = [
    "prompts",
    "tools",
    "skills",
    "models",
    "apis",
    "data",
    "scripts",
    "tests"
]

REQUIRED_DATA_FILES = [
    "facilities.json",
    "equipment.json",
    "consumption_patterns.json",
    "efficiency_measures.json",
    "renewable_options.json"
]


def main():
    issues = []

    print("Energy Management Assistant - Initialization Check")
    print("=" * 50)

    # Check directories
    print("\nChecking directories...")
    for dir_name in REQUIRED_DIRS:
        dir_path = project_root / dir_name
        if dir_path.is_dir():
            print(f"  ✓ {dir_name}/")
        else:
            print(f"  ✗ {dir_name}/ (missing)")
            issues.append(f"Missing directory: {dir_name}")

    # Check data files
    print("\nChecking data files...")
    data_dir = project_root / "data"
    for file_name in REQUIRED_DATA_FILES:
        file_path = data_dir / file_name
        if file_path.is_file():
            print(f"  ✓ data/{file_name}")
        else:
            print(f"  ✗ data/{file_name} (missing)")
            issues.append(f"Missing data file: {file_name}")

    # Check system prompt
    print("\nChecking prompts...")
    system_prompt = project_root / "prompts" / "system.txt"
    if system_prompt.is_file():
        print(f"  ✓ prompts/system.txt")
    else:
        print(f"  ✗ prompts/system.txt (missing)")
        issues.append("Missing system prompt")

    # Check tools
    print("\nChecking tools...")
    tools_dir = project_root / "tools"
    if tools_dir.is_dir():
        tool_files = list(tools_dir.glob("energy_*.py"))
        print(f"  Found {len(tool_files)} tool(s)")
        for tf in tool_files:
            print(f"    - {tf.name}")
    else:
        issues.append("Tools directory missing")

    # Summary
    print("\n" + "=" * 50)
    if issues:
        print(f"❌ {len(issues)} issue(s) found:")
        for issue in issues:
            print(f"   - {issue}")
        sys.exit(1)
    else:
        print("✅ All checks passed. Agent is ready to run.")
        print("\nNext steps:")
        print("  1. Copy .env.example to .env and configure LLM_API_KEY")
        print("  2. Run: python scripts/run.py")


if __name__ == "__main__":
    main()