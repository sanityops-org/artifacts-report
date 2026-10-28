#!/usr/bin/env python3
"""
detect_dependencies: Find and parse Python and Node.js dependency manifest files.

Scans a project directory for requirements.txt, pyproject.toml, setup.py,
package.json, and package-lock.json, extracting package names and versions.
"""

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Python 3.11+ has native tomllib, otherwise use tomli
try:
    import tomllib
except ImportError:
    import tomli as tomllib


# Directories to skip during traversal
SKIP_DIRS = {
    "node_modules", ".venv", "venv", "__pycache__", ".git",
    ".tox", "dist", "build", "*.egg-info"
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Detect and parse dependency manifest files.

    Args:
        params: {
            "project_path": str  # Path to project root directory
        }

    Returns:
        {
            "status": "success" | "error",
            "data": {
                "ecosystems": {
                    "python": {
                        "manifests": ["requirements.txt"],
                        "packages": [{"name": str, "version": str, "source": str}]
                    },
                    "nodejs": {
                        "manifests": ["package.json"],
                        "packages": [{"name": str, "version": str, "source": str}]
                    }
                },
                "total_packages": int
            },
            "error": str | None
        }
    """
    project_path = params.get("project_path")
    if not project_path:
        return {"status": "error", "error": "project_path parameter is required"}

    project_dir = Path(project_path)
    if not project_dir.exists():
        return {"status": "error", "error": f"Path does not exist: {project_path}"}

    ecosystems: Dict[str, Dict[str, Any]] = {}
    total_packages = 0

    # Scan for Python manifests
    python_packages = _scan_python_manifests(project_dir)
    if python_packages["packages"]:
        ecosystems["python"] = {
            "manifests": python_packages["manifests"],
            "packages": python_packages["packages"]
        }
        total_packages += len(python_packages["packages"])

    # Scan for Node.js manifests
    nodejs_packages = _scan_nodejs_manifests(project_dir)
    if nodejs_packages["packages"]:
        ecosystems["nodejs"] = {
            "manifests": nodejs_packages["manifests"],
            "packages": nodejs_packages["packages"]
        }
        total_packages += len(nodejs_packages["packages"])

    if not ecosystems:
        return {
            "status": "error",
            "error": "No dependency manifests found. Looking for: requirements.txt, pyproject.toml, setup.py, package.json, package-lock.json"
        }

    return {
        "status": "success",
        "data": {
            "ecosystems": ecosystems,
            "total_packages": total_packages
        }
    }


def _scan_python_manifests(project_dir: Path) -> Dict[str, Any]:
    """Scan for Python dependency manifests."""
    packages: List[Dict[str, str]] = []
    manifests: List[str] = []

    # Check requirements.txt
    req_file = project_dir / "requirements.txt"
    if req_file.exists():
        manifests.append("requirements.txt")
        packages.extend(_parse_requirements_txt(req_file))

    # Check pyproject.toml
    pyproject_file = project_dir / "pyproject.toml"
    if pyproject_file.exists():
        manifests.append("pyproject.toml")
        packages.extend(_parse_pyproject_toml(pyproject_file))

    # Check setup.py (basic extraction)
    setup_file = project_dir / "setup.py"
    if setup_file.exists():
        manifests.append("setup.py")
        packages.extend(_parse_setup_py(setup_file))

    return {"manifests": manifests, "packages": packages}


def _scan_nodejs_manifests(project_dir: Path) -> Dict[str, Any]:
    """Scan for Node.js dependency manifests."""
    packages: List[Dict[str, str]] = []
    manifests: List[str] = []

    # Prefer package-lock.json for exact versions
    lock_file = project_dir / "package-lock.json"
    pkg_file = project_dir / "package.json"

    if lock_file.exists():
        manifests.append("package-lock.json")
        packages.extend(_parse_package_lock_json(lock_file))
    elif pkg_file.exists():
        manifests.append("package.json")
        packages.extend(_parse_package_json(pkg_file))

    return {"manifests": manifests, "packages": packages}


def _parse_requirements_txt(file_path: Path) -> List[Dict[str, str]]:
    """Parse requirements.txt file."""
    packages = []

    content = file_path.read_text(encoding="utf-8")
    for line in content.splitlines():
        line = line.strip()

        # Skip comments and empty lines
        if not line or line.startswith("#"):
            continue

        # Handle various version specifiers
        # requests==2.28.0 -> name=requests, version=2.28.0
        # requests>=2.28.0 -> name=requests, version=2.28.0 (minimum)
        # requests~=2.28.0 -> name=requests, version=2.28.0

        match = re.match(r"^([a-zA-Z0-9_-]+)\s*(==|>=|<=|~=|!=|>|<)\s*([\d.]+)", line)
        if match:
            name = match.group(1)
            operator = match.group(2)
            version = match.group(3)

            packages.append({
                "name": name,
                "version": version,
                "source": "requirements.txt",
                "specifier": f"{operator}{version}"
            })

    return packages


def _parse_pyproject_toml(file_path: Path) -> List[Dict[str, str]]:
    """Parse pyproject.toml file (PEP 621 format)."""
    packages = []

    try:
        content = file_path.read_text(encoding="utf-8")
        data = tomllib.loads(content)

        # Check for PEP 621 project.dependencies
        project = data.get("project", {})
        deps = project.get("dependencies", [])

        for dep in deps:
            # Parse dependency strings like "requests>=2.28.0"
            match = re.match(r"^([a-zA-Z0-9_-]+)\s*(==|>=|<=|~=|!=|>|<)\s*([\d.]+)", dep)
            if match:
                packages.append({
                    "name": match.group(1),
                    "version": match.group(3),
                    "source": "pyproject.toml",
                    "specifier": f"{match.group(2)}{match.group(3)}"
                })

        # Also check optional-dependencies
        optional_deps = project.get("optional-dependencies", {})
        for group, deps_list in optional_deps.items():
            for dep in deps_list:
                match = re.match(r"^([a-zA-Z0-9_-]+)\s*(==|>=|<=|~=|!=|>|<)\s*([\d.]+)", dep)
                if match:
                    packages.append({
                        "name": match.group(1),
                        "version": match.group(3),
                        "source": f"pyproject.toml[{group}]",
                        "specifier": f"{match.group(2)}{match.group(3)}"
                    })

    except Exception as e:
        # Log error but don't fail the entire scan
        pass

    return packages


def _parse_setup_py(file_path: Path) -> List[Dict[str, str]]:
    """Basic extraction of dependencies from setup.py."""
    packages = []

    # This is a simplified regex-based extraction
    # Real setup.py parsing would require AST analysis
    content = file_path.read_text(encoding="utf-8")

    # Look for install_requires=[...] pattern
    match = re.search(r"install_requires\s*=\s*\[(.*?)\]", content, re.DOTALL)
    if match:
        deps_str = match.group(1)
        # Extract quoted strings
        for dep_match in re.finditer(r"['\"]([^'\"]+)['\"]", deps_str):
            dep = dep_match.group(1)
            # Parse version specifier
            version_match = re.match(r"^([a-zA-Z0-9_-]+)\s*(==|>=|<=|~=|!=|>|<)\s*([\d.]+)", dep)
            if version_match:
                packages.append({
                    "name": version_match.group(1),
                    "version": version_match.group(3),
                    "source": "setup.py",
                    "specifier": f"{version_match.group(2)}{version_match.group(3)}"
                })

    return packages


def _parse_package_json(file_path: Path) -> List[Dict[str, str]]:
    """Parse package.json file."""
    packages = []

    try:
        content = file_path.read_text(encoding="utf-8")
        data = json.loads(content)

        # Check dependencies
        deps = data.get("dependencies", {})
        for name, version in deps.items():
            # Clean version (remove ^, ~, etc.)
            clean_version = re.sub(r"^[^0-9]*", "", version)
            packages.append({
                "name": name,
                "version": clean_version,
                "source": "package.json"
            })

        # Check devDependencies
        dev_deps = data.get("devDependencies", {})
        for name, version in dev_deps.items():
            clean_version = re.sub(r"^[^0-9]*", "", version)
            packages.append({
                "name": name,
                "version": clean_version,
                "source": "package.json"
            })

    except Exception as e:
        pass

    return packages


def _parse_package_lock_json(file_path: Path) -> List[Dict[str, str]]:
    """Parse package-lock.json file for exact versions."""
    packages = []

    try:
        content = file_path.read_text(encoding="utf-8")
        data = json.loads(content)

        # npm 7+ format: packages section
        packages_section = data.get("packages", {})
        for pkg_path, pkg_data in packages_section.items():
            # Skip the root package (empty string key)
            if not pkg_path:
                continue

            # Extract package name from path
            name = pkg_data.get("name") or pkg_path.split("node_modules/")[-1]
            version = pkg_data.get("version", "")

            if name and version:
                packages.append({
                    "name": name,
                    "version": version,
                    "source": "package-lock.json"
                })

        # Legacy format (npm 6): dependencies section
        if not packages_section:
            deps_section = data.get("dependencies", {})
            for name, pkg_data in deps_section.items():
                version = pkg_data.get("version", "")
                if version:
                    packages.append({
                        "name": name,
                        "version": version,
                        "source": "package-lock.json"
                    })

    except Exception as e:
        pass

    return packages


if __name__ == "__main__":
    # Simple CLI for testing
    import sys
    if len(sys.argv) > 1:
        result = execute({"project_path": sys.argv[1]})
        print(json.dumps(result, indent=2))
    else:
        print("Usage: python detect_dependencies.py <project_path>")