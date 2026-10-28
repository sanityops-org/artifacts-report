#!/usr/bin/env python3
"""
Weather Assistant - Setup verification script
"""

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

    print("=" * 50)
    print("  Weather Assistant Setup Check")
    print("=" * 50)
    print()

    print("[1] Checking required directories...")
    dirs_ok = True
    dirs_ok &= check_directory("prompts", project_root / "prompts")
    dirs_ok &= check_directory("models", project_root / "models")
    dirs_ok &= check_directory("apis", project_root / "apis")
    dirs_ok &= check_directory("data", project_root / "data")
    dirs_ok &= check_directory("skills", project_root / "skills")
    dirs_ok &= check_directory("tools", project_root / "tools")
    dirs_ok &= check_directory("scripts", project_root / "scripts")

    print("\n[2] Checking required data files...")
    data_ok = True
    data_ok &= check_file("locations.json", project_root / "data" / "locations.json")
    data_ok &= check_file("current_conditions.json", project_root / "data" / "current_conditions.json")
    data_ok &= check_file("forecasts.json", project_root / "data" / "forecasts.json")
    data_ok &= check_file("alerts.json", project_root / "data" / "alerts.json")

    print("\n[3] Checking system prompt...")
    prompt_ok = check_file("system.txt", project_root / "prompts" / "system.txt")

    print("\n" + "=" * 50)
    if dirs_ok and data_ok and prompt_ok:
        print("  ✓ All checks passed")
        print("\nYou can now run:")
        print("  python scripts/run.py")
    else:
        print("  ✗ Some checks failed")
        print("\nPlease ensure all required files are in place.")
    print("=" * 50)


if __name__ == "__main__":
    main()
