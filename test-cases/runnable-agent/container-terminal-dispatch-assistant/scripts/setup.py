#!/usr/bin/env python3
"""
Container Terminal Dispatch Assistant - Initialization Script

Check whether the data file exists to ensure that the system can operate normally.
"""

import os
import sys

# Project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Required data files
REQUIRED_DATA_FILES = [
    "data/vessels.json",
    "data/berths.json",
    "data/yard_blocks.json",
    "data/containers.json",
    "data/equipment.json",
    "data/tasks.json",
    "data/gate_channels.json",
    "data/appointments.json",
]

# Required catalogs
REQUIRED_DIRS = [
    "data",
    "models",
    "skills",
    "skills/berth_scheduling",
    "skills/yard_scheduling",
    "skills/equipment_scheduling",
    "skills/gate_scheduling",
    "simulator",
    "prompts",
    "scripts",
    "apis",
    "tools",
]


def check_directories() -> tuple:
    """
    Check whether the required directory exists

    Returns:
        tuple: (Existing directory list, missing directory list)
    """
    existing = []
    missing = []

    for dir_path in REQUIRED_DIRS:
        full_path = os.path.join(PROJECT_ROOT, dir_path)
        if os.path.isdir(full_path):
            existing.append(dir_path)
        else:
            missing.append(dir_path)

    return existing, missing


def check_data_files() -> tuple:
    """
    Check whether the data file exists

    Returns:
        tuple: (List of existing files, list of missing files)
    """
    existing = []
    missing = []

    for file_path in REQUIRED_DATA_FILES:
        full_path = os.path.join(PROJECT_ROOT, file_path)
        if os.path.isfile(full_path):
            existing.append(file_path)
        else:
            missing.append(file_path)

    return existing, missing


def main():
    """Main function"""
    print("=" * 50)
    print("  Container Terminal Dispatch Assistant - System Inspection")
    print("=" * 50)
    print()

    # Check the catalog
    print("[1] Check the directory structure...")
    existing_dirs, missing_dirs = check_directories()

    if existing_dirs:
        print(f"    {Len(existing_dirs)} directories found:")
        for d in existing_dirs:
            print(f"      ✓ {d}")

    if missing_dirs:
        print(f"    Missing {len(missing_dirs)} directories:")
        for d in missing_dirs:
            print(f"      ✗ {d}")

    print()

    # Check the data files
    print("[2] Check the data files...")
    existing_files, missing_files = check_data_files()

    if existing_files:
        print(f"    {Len(existing_files)} data files have been found:")
        for f in existing_files:
            print(f"      ✓ {f}")

    if missing_files:
        print(f"    Missing {len(missing_files)} data files:")
        for f in missing_files:
            print(f"      ✗ {f}")

    print()

    # Summary of inspection results
    print("[3] Summary of inspection results...")
    if not missing_dirs and not missing_files:
        print("    ✓ The system check has passed, and all the required files and directories are ready.")
        return 0
    else:
        if missing_dirs:
            print(f"    ✗ Missing {len(missing_dirs)} directories")
        if missing_files:
            print(f"    ✗ Missing {len(missing_files)} data files")
        print()
        print("    Please run the data generation script or check the integrity of the project first.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
