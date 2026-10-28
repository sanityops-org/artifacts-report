#!/usr/bin/env python3
"""Tests for generate_report tool."""

import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from generate_report import execute


class TestGenerateReport(unittest.TestCase):
    """Test cases for report generation."""

    def test_generate_report_with_vulnerabilities(self):
        """Test report generation with vulnerabilities."""
        scan_results = {
            "ecosystems": {
                "python": {
                    "packages": [{"name": "requests", "version": "2.28.0"}]
                }
            },
            "vulnerabilities": [
                {
                    "package": "requests",
                    "version": "2.28.0",
                    "vulnerabilities": [
                        {
                            "id": "CVE-2024-12345",
                            "summary": "Test vulnerability",
                            "severity": "HIGH",
                            "cvss_score": 7.5,
                            "fixed_versions": ["2.31.0"]
                        }
                    ]
                }
            ]
        }

        result = execute({
            "project_path": "/test/project",
            "scan_results": scan_results
        })

        self.assertEqual(result["status"], "success")
        self.assertIn("report", result["data"])
        self.assertIn("summary", result["data"])

        # Check report content
        report = result["data"]["report"]
        self.assertIn("Security Audit Report", report)
        self.assertIn("requests", report)
        self.assertIn("HIGH", report)

        # Check summary
        summary = result["data"]["summary"]
        self.assertEqual(summary["total_packages"], 1)
        self.assertEqual(summary["vulnerabilities_found"], 1)
        self.assertEqual(summary["high"], 1)

    def test_generate_report_no_vulnerabilities(self):
        """Test report generation with no vulnerabilities."""
        scan_results = {
            "ecosystems": {
                "python": {
                    "packages": [{"name": "requests", "version": "2.31.0"}]
                }
            },
            "vulnerabilities": []
        }

        result = execute({
            "project_path": "/test/project",
            "scan_results": scan_results
        })

        self.assertEqual(result["status"], "success")
        report = result["data"]["report"]
        self.assertIn("No known vulnerabilities detected", report)

    def test_severity_sorting(self):
        """Test that vulnerabilities are sorted by severity."""
        scan_results = {
            "ecosystems": {},
            "vulnerabilities": [
                {
                    "package": "pkg-low",
                    "version": "1.0.0",
                    "vulnerabilities": [
                        {"id": "LOW-1", "severity": "LOW", "cvss_score": 2.0, "summary": "Low", "fixed_versions": []}
                    ]
                },
                {
                    "package": "pkg-critical",
                    "version": "1.0.0",
                    "vulnerabilities": [
                        {"id": "CRIT-1", "severity": "CRITICAL", "cvss_score": 9.5, "summary": "Critical", "fixed_versions": []}
                    ]
                },
                {
                    "package": "pkg-high",
                    "version": "1.0.0",
                    "vulnerabilities": [
                        {"id": "HIGH-1", "severity": "HIGH", "cvss_score": 7.5, "summary": "High", "fixed_versions": []}
                    ]
                }
            ]
        }

        result = execute({
            "project_path": "/test",
            "scan_results": scan_results
        })

        report = result["data"]["report"]
        # Critical should appear before High
        critical_pos = report.find("CRITICAL")
        high_pos = report.find("HIGH")
        # Check that Critical section header comes before High section header
        # (Both words appear in multiple places, so we check section headers)
        self.assertLess(
            report.find("🔴 Critical"),
            report.find("🟠 High")
        )


if __name__ == "__main__":
    unittest.main()