#!/usr/bin/env python3
"""Tests for detect_dependencies tool."""

import unittest
import tempfile
import os
from pathlib import Path

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from detect_dependencies import execute


class TestDetectDependencies(unittest.TestCase):
    """Test cases for dependency detection."""

    def test_detect_requirements_txt(self):
        """Test parsing requirements.txt file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            req_file = Path(tmpdir) / "requirements.txt"
            req_file.write_text("requests==2.28.0\nflask==2.0.0\n")

            result = execute({"project_path": tmpdir})

            self.assertEqual(result["status"], "success")
            self.assertIn("python", result["data"]["ecosystems"])
            packages = result["data"]["ecosystems"]["python"]["packages"]
            self.assertEqual(len(packages), 2)
            self.assertEqual(packages[0]["name"], "requests")
            self.assertEqual(packages[0]["version"], "2.28.0")

    def test_detect_package_json(self):
        """Test parsing package.json file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            pkg_file = Path(tmpdir) / "package.json"
            pkg_file.write_text('{"dependencies": {"lodash": "4.17.15", "express": "4.18.0"}}')

            result = execute({"project_path": tmpdir})

            self.assertEqual(result["status"], "success")
            self.assertIn("nodejs", result["data"]["ecosystems"])
            packages = result["data"]["ecosystems"]["nodejs"]["packages"]
            self.assertEqual(len(packages), 2)
            self.assertEqual(packages[0]["name"], "lodash")

    def test_no_manifests_found(self):
        """Test error handling when no manifests exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = execute({"project_path": tmpdir})

            self.assertEqual(result["status"], "error")
            self.assertIn("No dependency manifests found", result["error"])

    def test_requirements_with_version_operators(self):
        """Test parsing requirements with various version specifiers."""
        with tempfile.TemporaryDirectory() as tmpdir:
            req_file = Path(tmpdir) / "requirements.txt"
            req_file.write_text("requests>=2.28.0\nflask==2.0.0\npyyaml~=5.4\n")

            result = execute({"project_path": tmpdir})

            self.assertEqual(result["status"], "success")
            packages = result["data"]["ecosystems"]["python"]["packages"]
            # Should extract pinned version from ==
            flask = next((p for p in packages if p["name"] == "flask"), None)
            self.assertIsNotNone(flask)
            self.assertEqual(flask["version"], "2.0.0")
            # >= should still be recorded
            requests = next((p for p in packages if p["name"] == "requests"), None)
            self.assertIsNotNone(requests)

    def test_ignore_directories(self):
        """Test that common directories are ignored."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create node_modules and venv directories
            node_modules = Path(tmpdir) / "node_modules" / "some_package"
            node_modules.mkdir(parents=True)
            (node_modules / "package.json").write_text('{"name": "some_package"}')

            venv = Path(tmpdir) / ".venv"
            venv.mkdir()

            # Create actual project package.json
            pkg_file = Path(tmpdir) / "package.json"
            pkg_file.write_text('{"dependencies": {"lodash": "4.17.15"}}')

            result = execute({"project_path": tmpdir})

            # Should only find the root package.json
            self.assertEqual(result["status"], "success")
            packages = result["data"]["ecosystems"]["nodejs"]["packages"]
            self.assertEqual(len(packages), 1)


if __name__ == "__main__":
    unittest.main()