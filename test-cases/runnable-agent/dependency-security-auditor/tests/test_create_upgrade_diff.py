#!/usr/bin/env python3
"""Tests for create_upgrade_diff tool."""

import unittest
import tempfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from create_upgrade_diff import execute


class TestCreateUpgradeDiff(unittest.TestCase):
    """Test cases for upgrade diff generation."""

    def test_create_diff_requirements_txt(self):
        """Test creating diff for requirements.txt."""
        with tempfile.TemporaryDirectory() as tmpdir:
            req_file = Path(tmpdir) / "requirements.txt"
            req_file.write_text("requests==2.28.0\nflask==2.0.0\n")

            upgrades = [
                {
                    "package": "requests",
                    "current_version": "2.28.0",
                    "fixed_version": "2.31.0",
                    "source_file": "requirements.txt"
                }
            ]

            result = execute({
                "project_path": tmpdir,
                "upgrades": upgrades
            })

            self.assertEqual(result["status"], "success")
            diffs = result["data"]["diffs"]
            self.assertEqual(len(diffs), 1)

            diff_content = diffs[0]["content"]
            self.assertIn("-requests==2.28.0", diff_content)
            self.assertIn("+requests>=2.31.0", diff_content)

    def test_create_diff_package_json(self):
        """Test creating diff for package.json."""
        with tempfile.TemporaryDirectory() as tmpdir:
            pkg_file = Path(tmpdir) / "package.json"
            pkg_file.write_text('{"dependencies": {"lodash": "4.17.15"}}')

            upgrades = [
                {
                    "package": "lodash",
                    "current_version": "4.17.15",
                    "fixed_version": "4.17.21",
                    "source_file": "package.json"
                }
            ]

            result = execute({
                "project_path": tmpdir,
                "upgrades": upgrades
            })

            self.assertEqual(result["status"], "success")
            diff_content = result["data"]["diffs"][0]["content"]
            self.assertIn('"lodash"', diff_content)

    def test_no_upgrades_needed(self):
        """Test handling when no upgrades are provided."""
        result = execute({
            "project_path": "/test",
            "upgrades": []
        })

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"]["diffs"], [])

    def test_preserves_file_formatting(self):
        """Test that diff preserves other lines in file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            req_file = Path(tmpdir) / "requirements.txt"
            original = "flask==2.0.0\nrequests==2.28.0\npyyaml==5.4\n"
            req_file.write_text(original)

            upgrades = [
                {
                    "package": "requests",
                    "current_version": "2.28.0",
                    "fixed_version": "2.31.0",
                    "source_file": "requirements.txt"
                }
            ]

            result = execute({
                "project_path": tmpdir,
                "upgrades": upgrades
            })

            diff_content = result["data"]["diffs"][0]["content"]
            # Other lines should be preserved
            self.assertIn("flask==2.0.0", diff_content)
            self.assertIn("pyyaml==5.4", diff_content)


if __name__ == "__main__":
    unittest.main()