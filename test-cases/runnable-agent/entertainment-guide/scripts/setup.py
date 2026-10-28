#!/usr/bin/env python3
"""
Entertainment Guide - Setup verification script
"""

import sys
from pathlib import Path


def check_directory(name: str, path: Path) -> bool:
    """Check if directory exists"""
    exists = path.exists() and path.is_dir()
    status = "✓" if exists else "✗"
    print(f"  {status} {name}: {path}")
    return exists


def check_file(name: str, path: Path) -> bool:
    """Check if file exists"""
    exists = path.exists() and path.is_file()
    status = "✓" if exists else "✗"
    print(f"  {status} {name}: {path}")
    return exists


def main():
    """Main function"""
    project_root = Path(__file__).parent.parent

    print("=" * 60)
    print("  Entertainment Guide Setup Check")
    print("=" * 60)
    print()

    print("[1] Checking required directories...")
    dirs_ok = True
    for name in ("prompts", "models", "apis", "data", "skills", "tools", "scripts"):
        dirs_ok &= check_directory(name, project_root / name)

    print("\n[2] Checking required data files...")
    data_ok = True
    for name in ("titles.json", "watchlist.json", "reviews.json"):
        data_ok &= check_file(name, project_root / "data" / name)

    print("\n[3] Checking system prompt...")
    prompt_ok = check_file("system.txt", project_root / "prompts" / "system.txt")

    print("\n[4] Checking tools...")
    tools_ok = True
    tools = [
        "title_search.py",
        "title_details.py",
        "title_by_actor.py",
        "title_by_director.py",
        "get_recommendations.py",
        "watchlist_add.py",
        "watchlist_remove.py",
        "watchlist_list.py",
        "watchlist_mark_watched.py",
        "review_list.py",
    ]
    for tool in tools:
        tools_ok &= check_file(tool, project_root / "tools" / tool)

    print("\n[5] Checking skills...")
    skills_ok = True
    for skill in ("title_search", "recommendations", "watchlist_management"):
        skill_dir = project_root / "skills" / skill
        skills_ok &= check_directory(skill, skill_dir)
        skills_ok &= check_file("  SKILL.md", skill_dir / "SKILL.md")
        skills_ok &= check_file("  handler.py", skill_dir / "handler.py")

    print("\n" + "=" * 60)
    if dirs_ok and data_ok and prompt_ok and tools_ok and skills_ok:
        print("  ✓ All checks passed")
        print("\nYou can now run:")
        print("  python scripts/run.py")
    else:
        print("  ✗ Some checks failed")
        print("\nPlease ensure all required files are in place.")
        sys.exit(1)
    print("=" * 60)


if __name__ == "__main__":
    main()
