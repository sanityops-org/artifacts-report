#!/usr/bin/env python3
"""
Freight Logistics Assistant - Initialization Check Script

Verifies required directories and mock data files exist.
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent


def check_directories() -> bool:
    """Check required directories exist"""
    required_dirs = [
        "prompts",
        "tools",
        "skills",
        "data",
        "models",
        "apis",
        "scripts",
    ]

    all_exist = True
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        if dir_path.exists():
            print(f"  ✓ {dir_name}/")
        else:
            print(f"  ✗ {dir_name}/ (missing)")
            all_exist = False

    return all_exist


def check_data_files() -> bool:
    """Check required mock data files exist"""
    data_dir = project_root / "data"
    required_files = [
        "shipments.json",
        "routes.json",
        "carriers.json",
        "pricing_rules.json",
        "cargo_types.json",
    ]

    all_exist = True
    for file_name in required_files:
        file_path = data_dir / file_name
        if file_path.exists():
            print(f"  ✓ data/{file_name}")
        else:
            print(f"  ✗ data/{file_name} (missing)")
            all_exist = False

    return all_exist


def check_skills() -> bool:
    """Check skill directories have SKILL.md"""
    skills_dir = project_root / "skills"
    skill_dirs = ["shipment_tracking", "route_planning", "freight_quotation"]

    all_exist = True
    for skill_name in skill_dirs:
        skill_path = skills_dir / skill_name / "SKILL.md"
        if skill_path.exists():
            print(f"  ✓ skills/{skill_name}/SKILL.md")
        else:
            print(f"  ✗ skills/{skill_name}/SKILL.md (missing)")
            all_exist = False

    return all_exist


def main():
    """Run all checks"""
    print("=" * 50)
    print("  Freight Logistics Assistant - Setup Check")
    print("=" * 50)
    print()

    print("[1] Checking directories...")
    dirs_ok = check_directories()

    print("\n[2] Checking data files...")
    data_ok = check_data_files()

    print("\n[3] Checking skills...")
    skills_ok = check_skills()

    print()
    print("=" * 50)
    if dirs_ok and data_ok and skills_ok:
        print("  ✓ All checks passed!")
        print()
        print("  Next steps:")
        print("  1. Copy .env.example to .env")
        print("  2. Configure LLM_API_KEY in .env")
        print("  3. Run: python scripts/run.py")
    else:
        print("  ✗ Some checks failed. Please fix missing items.")
        sys.exit(1)
    print("=" * 50)


if __name__ == "__main__":
    main()