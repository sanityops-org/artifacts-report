#!/usr/bin/env python3
"""
Expense Compliance Auditor - Environment self-check

Verifies the convention-based layout this repository relies on. There are no
configuration files to validate: the directories and files checked here are
exactly what the SDK discovers on its own.
"""

import os
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent
MIN_PYTHON = (3, 11)

REQUIRED_TOOLS = (
    "parse_expenses.py",
    "get_policy.py",
    "audit_expenses.py",
    "detect_duplicates.py",
    "generate_report.py",
)
REQUIRED_SKILLS = ("expense_audit", "policy_management", "audit_report")
REQUIRED_SAMPLE_DATA = (
    "clean_batch.csv",
    "violations_batch.csv",
    "duplicates_batch.json",
)
FORBIDDEN_CONFIG_FILES = ("agent.yaml", "agent.yml", "tools.yaml", "policy.yaml", "policy.json")


def check_python_version() -> bool:
    """Require the Python version the agent targets."""
    current = sys.version_info[:2]
    if current < MIN_PYTHON:
        print(f"FAIL: Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+ required, running {current[0]}.{current[1]}")
        return False
    print(f"OK: Python {current[0]}.{current[1]}")
    return True


def check_system_prompt() -> bool:
    """Confirm prompts/system.txt exists and is non-empty."""
    prompt_file = PROJECT_ROOT / "prompts" / "system.txt"
    if not prompt_file.exists():
        print(f"FAIL: missing {prompt_file.relative_to(PROJECT_ROOT)}")
        return False
    if not prompt_file.read_text(encoding="utf-8").strip():
        print("FAIL: prompts/system.txt is empty")
        return False
    print("OK: prompts/system.txt")
    return True


def check_tools() -> bool:
    """Confirm every tool module exists and exposes execute()."""
    passed = True
    for tool_name in REQUIRED_TOOLS:
        tool_path = PROJECT_ROOT / "tools" / tool_name
        if not tool_path.exists():
            print(f"FAIL: missing tools/{tool_name}")
            passed = False
            continue
        if "def execute(" not in tool_path.read_text(encoding="utf-8"):
            print(f"FAIL: tools/{tool_name} has no execute() function")
            passed = False
    if passed:
        print(f"OK: {len(REQUIRED_TOOLS)} tools")
    return passed


def check_skills() -> bool:
    """Confirm every skill folder has a SKILL.md with frontmatter."""
    passed = True
    for skill_name in REQUIRED_SKILLS:
        skill_file = PROJECT_ROOT / "skills" / skill_name / "SKILL.md"
        if not skill_file.exists():
            print(f"FAIL: missing skills/{skill_name}/SKILL.md")
            passed = False
            continue
        text = skill_file.read_text(encoding="utf-8")
        if not text.startswith("---") or "name:" not in text or "description:" not in text:
            print(f"FAIL: skills/{skill_name}/SKILL.md is missing frontmatter")
            passed = False
    if passed:
        print(f"OK: {len(REQUIRED_SKILLS)} skills")
    return passed


def check_sample_data() -> bool:
    """Confirm the sample batches are present."""
    passed = True
    for filename in REQUIRED_SAMPLE_DATA:
        data_file = PROJECT_ROOT / "data" / "sample_expenses" / filename
        if not data_file.exists():
            print(f"FAIL: missing data/sample_expenses/{filename}")
            passed = False
    if passed:
        print(f"OK: {len(REQUIRED_SAMPLE_DATA)} sample batches")
    return passed


def check_no_config_files() -> bool:
    """Confirm the convention has not been broken by a config file."""
    found = [name for name in FORBIDDEN_CONFIG_FILES if (PROJECT_ROOT / name).exists()]
    if found:
        print(f"FAIL: configuration files are not part of this repository's convention: {', '.join(found)}")
        return False
    print("OK: no configuration files (convention over configuration)")
    return True


def check_framework() -> bool:
    """Report whether the sanityops_agent framework is importable."""
    try:
        import sanityops_agent  # noqa: F401
    except ImportError:
        print("WARN: sanityops_agent not installed; scripts/run.py will not start")
        print("      pip install sanityops_agent --index-url <your index url>")
        return True
    print("OK: sanityops_agent")
    return True


def make_scripts_executable() -> None:
    """Mark every Python file in scripts/ and tools/ executable."""
    count = 0
    for directory in (PROJECT_ROOT / "scripts", PROJECT_ROOT / "tools"):
        if not directory.exists():
            continue
        for python_file in directory.rglob("*.py"):
            try:
                os.chmod(python_file, 0o755)
                count += 1
            except OSError:
                pass
    print(f"OK: marked {count} scripts executable")


def main() -> int:
    """Run every check and report the result."""
    print("=" * 60)
    print("  Expense Compliance Auditor - Environment Check")
    print("=" * 60)
    print()

    results = [
        check_python_version(),
        check_system_prompt(),
        check_tools(),
        check_skills(),
        check_sample_data(),
        check_no_config_files(),
        check_framework(),
    ]

    print()
    make_scripts_executable()
    print()

    print("=" * 60)
    if all(results):
        print("Environment check passed.")
        print()
        print("Run the agent with:")
        print(f"  python {PROJECT_ROOT / 'scripts' / 'run.py'}")
        print("=" * 60)
        return 0

    print("Environment check failed. Fix the FAIL lines above.")
    print("=" * 60)
    return 1


if __name__ == "__main__":
    sys.exit(main())