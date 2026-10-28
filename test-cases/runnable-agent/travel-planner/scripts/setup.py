#!/usr/bin/env python3
"""
Travel Planner Agent - Setup Script
"""

import os
import sys
from pathlib import Path

def check_file(path: Path, description: str) -> bool:
    """Check if file exists"""
    if path.exists():
        print(f"✓ {description}: {path}")
        return True
    else:
        print(f"✗ {description}: {path} (MISSING)")
        return False

def check_directory(path: Path, description: str) -> bool:
    """Check if directory exists"""
    if path.exists() and path.is_dir():
        print(f"✓ {description}: {path}")
        return True
    else:
        print(f"✗ {description}: {path} (MISSING)")
        return False

def main():
    print("=" * 60)
    print("Travel Planner Agent - Setup Check")
    print("=" * 60)
    print()

    project_root = Path(__file__).parent.parent
    all_ok = True

    # Check directories
    print("Checking directories:")
    all_ok &= check_directory(project_root / "prompts", "Prompts directory")
    all_ok &= check_directory(project_root / "models", "Models directory")
    all_ok &= check_directory(project_root / "apis", "APIs directory")
    all_ok &= check_directory(project_root / "data", "Data directory")
    all_ok &= check_directory(project_root / "skills", "Skills directory")
    all_ok &= check_directory(project_root / "tools", "Tools directory")
    print()

    # Check configuration files
    print("Checking configuration files:")
    all_ok &= check_file(project_root / "requirements.txt", "Requirements file")
    all_ok &= check_file(project_root / ".env.example", "Environment example")
    all_ok &= check_file(project_root / "README.md", "README file")
    print()

    # Check data files
    print("Checking data files:")
    all_ok &= check_file(project_root / "data" / "destinations.json", "Destinations data")
    all_ok &= check_file(project_root / "data" / "attractions.json", "Attractions data")
    all_ok &= check_file(project_root / "data" / "accommodations.json", "Accommodations data")
    print()

    # Check system prompt
    print("Checking system prompt:")
    all_ok &= check_file(project_root / "prompts" / "system.txt", "System prompt")
    print()

    # Check tools
    print("Checking tools:")
    tools = [
        "destination_search.py",
        "destination_details.py",
        "attraction_list.py",
        "attraction_details.py",
        "accommodation_search.py",
        "accommodation_details.py",
        "itinerary_create.py",
        "itinerary_details.py",
        "budget_estimate.py",
    ]
    for tool in tools:
        all_ok &= check_file(project_root / "tools" / tool, f"Tool: {tool}")
    print()

    # Check skills
    print("Checking skills:")
    skills = ["destination_search", "itinerary_planning", "accommodation_search"]
    for skill in skills:
        skill_dir = project_root / "skills" / skill
        all_ok &= check_directory(skill_dir, f"Skill: {skill}")
        all_ok &= check_file(skill_dir / "SKILL.md", f"  SKILL.md")
        all_ok &= check_file(skill_dir / "handler.py", f"  handler.py")
    print()

    # Summary
    print("=" * 60)
    if all_ok:
        print("✓ All checks passed!")
        print("\nNext steps:")
        print("1. Copy .env.example to .env and add your LLM API key")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Run the agent: python scripts/run.py")
    else:
        print("✗ Some checks failed. Please fix the issues above.")
        sys.exit(1)
    print("=" * 60)

if __name__ == "__main__":
    main()
