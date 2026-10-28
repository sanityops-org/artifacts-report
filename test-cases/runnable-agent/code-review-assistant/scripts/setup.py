#!/usr/bin/env python3
"""
Agent Initialize the script

Set up the Agent running environment, install dependencies, and verify the configuration.
"""

import sys
import os
import subprocess
from pathlib import Path

# Project root directory
project_root = Path(__file__).parent.parent


def check_python_version():
    """Check the Python version"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"Error: Python 3.8+ is required, the current version {version.major}.{version.minor}")
        return False
    print(f"✓ Python Version check passed: {version.major}.{version.minor}.{version.micro}")
    return True


def install_dependencies():
    """Installation dependency"""
    requirements_file = project_root / "requirements.txt"

    if not requirements_file.exists():
        print(f"Error: Dependent file does not exist: {requirements_file}")
        return False

    print(f"Dependencies are being installed...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
            check=True,
            capture_output=False
        )
        print("✓ Depend on the completion of installation")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Dependent installation failed: {e}")
        return False


def check_sanityops_agent():
    """Check whether sanityops_agent is installed"""
    try:
        import sanityops_agent
        print(f"✓ sanityops_agent Installed")
        return True
    except ImportError:
        print(f"✗ sanityops_agent Not installed")
        print(f"  Please run: pip install sanityops_agent ")
        return False


def validate_config():
    """Verify the configuration file"""
    config_file = project_root / "agent.yaml"

    if not config_file.exists():
        print(f"✗ The configuration file does not exist.: {config_file}")
        return False

    try:
        import yaml
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)

        required_keys = ['name', 'version', 'description']
        for key in required_keys:
            if key not in config:
                print(f"✗ The configuration file lacks the necessary fields.: {key}")
                return False

        print(f"✓ Configuration file verification passed")
        print(f"  Agent Name: {config['name']}")
        print(f"  Edition: {config['version']}")
        return True
    except Exception as e:
        print(f"✗ Configuration file verification failed: {e}")
        return False


def check_skills():
    """Check the skill configuration"""
    skills_dir = project_root / "skills"

    if not skills_dir.exists():
        print(f"✗ The skill catalog does not exist.: {skills_dir}")
        return False

    skill_count = 0
    for skill_path in skills_dir.iterdir():
        if skill_path.is_dir():
            skill_yaml = skill_path / "skill.yaml"
            handler_py = skill_path / "handler.py"

            if skill_yaml.exists() and handler_py.exists():
                skill_count += 1
                print(f"✓ Skill verification passed: {skill_path.name}")
            else:
                print(f"✗ Incomplete skill configuration: {skill_path.name}")

    if skill_count == 0:
        print(f"✗ No effective skills were found.")
        return False

    return True


def make_scripts_executable():
    """Set script execution permissions"""
    scripts_dir = project_root / "scripts"
    skills_dir = project_root / "skills"

    executable_count = 0
    for script_dir in [scripts_dir, skills_dir]:
        if not script_dir.exists():
            continue

        for py_file in script_dir.rglob("*.py"):
            try:
                os.chmod(py_file, 0o755)
                executable_count += 1
            except Exception as e:
                print(f"Warning: Unable to set permissions {py_file}: {e}")

    print(f"✓ The executable permissions of {executable_count} scripts have been set")
    return True


def main():
    """Main entrance"""
    print("=" * 60)
    print("Code Review Assistant - Initialization")
    print("=" * 60)
    print()

    all_passed = True

    # 1. Check the Python version
    if not check_python_version():
        all_passed = False
    print()

    # 2. Installation dependency
    if not install_dependencies():
        all_passed = False
    print()

    # 3. Examine sanityops_agent
    if not check_sanityops_agent():
        all_passed = False
    print()

    # 4. Verify the configuration
    if not validate_config():
        all_passed = False
    print()

    # 5. Check the skills
    if not check_skills():
        all_passed = False
    print()

    # 6. Set permissions
    make_scripts_executable()
    print()

    # Sum up
    print("=" * 60)
    if all_passed:
        print("✓ Initialization completed!")
        print()
        print("Operation mode:")
        print(f"  python {project_root}/scripts/run.py")
    else:
        print("✗ Initialization failed, please fix the above problem.")
        return 1
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
