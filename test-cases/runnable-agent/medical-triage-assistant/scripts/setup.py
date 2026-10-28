#!/usr/bin/env python3
"""Medical Guidance Assistant - Environmental and Data Checking Script.

Check whether the required directories and data files are complete, and check whether the data can be loaded by the model.
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore

REQUIRED_DIRS = [
    "prompts",
    "models",
    "apis",
    "data",
    "skills/triage",
    "skills/registration",
    "tools",
    "scripts",
]

REQUIRED_DATA_FILES = [
    "departments.json",
    "doctors.json",
    "slots.json",
    "red_flag_rules.json",
    "symptom_department_map.json",
    "appointments.json",
]


def check_dirs() -> list[str]:
    """Check the required directory and return the missing items."""
    missing = []
    print("Check the required catalog:")
    for name in REQUIRED_DIRS:
        path = project_root / name
        if path.is_dir():
            print(f"  [OK]   {name}")
        else:
            print(f"  [Shortcoming] {name}")
            missing.append(name)
    return missing


def check_data_files() -> list[str]:
    """Check the required data files and do a loading check on the modelable data."""
    missing = []
    print()
    print("Check the required data files:")
    data_dir = project_root / "data"
    for name in REQUIRED_DATA_FILES:
        path = data_dir / name
        if path.is_file():
            print(f"  [OK]   data/{name}")
        else:
            print(f"  [Shortcoming] data/{name}")
            missing.append(name)
    return missing


def check_data_loadable() -> list[str]:
    """Try to load the data and return the error description."""
    errors = []
    print()
    print("Verification data can be loaded:")
    store = DataStore(data_dir=project_root / "data")
    loaders = [
        ("Departments and offices", store.load_departments),
        ("Doctor", store.load_doctors),
        ("Number source", store.load_slots),
        ("Registration record", store.load_appointments),
        ("Red flag rules", store.load_red_flag_rules),
        ("Symptom mapping", store.load_symptom_map),
    ]
    for label, loader in loaders:
        try:
            print(f"  [OK]   {label}: {len(loader())} Twig")
        except Exception as e:
            print(f"  [Be defeated] {label}: {e}")
            errors.append(f"{label}: {e}")
    return errors


def main() -> int:
    """Perform the inspection and output the summary"""
    print("=" * 50)
    print("  Medical Guidance Assistant - Environmental Inspection")
    print("=" * 50)
    print()
    missing_dirs = check_dirs()
    missing_files = check_data_files()
    data_errors = check_data_loadable()

    print()
    print("=" * 50)
    if not missing_dirs and not missing_files and not data_errors:
        print("Check passed: the directory, data file and data loading are all normal.")
        return 0

    print("The inspection failed.:")
    for name in missing_dirs:
        print(f"  Missing directory: {name}")
    for name in missing_files:
        print(f"  Missing data files: data/{name}")
    for message in data_errors:
        print(f"  Data loading error: {message}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
