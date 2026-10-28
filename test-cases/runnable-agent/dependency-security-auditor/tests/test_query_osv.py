#!/usr/bin/env python3
"""Tests for query_osv tool."""

import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from query_osv import execute, _map_severity


class TestQueryOSV(unittest.TestCase):
    """Test cases for OSV API queries."""

    @patch("query_osv.requests.post")
    def test_query_pypi_package_with_vulnerability(self, mock_post):
        """Test querying a vulnerable Python package."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "vulns": [
                {
                    "id": "GHSA-xxxx-xxxx-xxxx",
                    "summary": "Test vulnerability",
                    "severity": [{"type": "CVSS_V3", "score": 7.5}],
                    "affected": [
                        {
                            "versions": ["2.28.0"],
                            "ranges": [{"type": "ECOSYSTEM", "events": [{"fixed": "2.31.0"}]}]
                        }
                    ]
                }
            ]
        }
        mock_post.return_value = mock_response

        result = execute({
            "ecosystem": "PyPI",
            "package": "requests",
            "version": "2.28.0"
        })

        self.assertEqual(result["status"], "success")
        self.assertEqual(len(result["data"]["vulnerabilities"]), 1)
        vuln = result["data"]["vulnerabilities"][0]
        self.assertEqual(vuln["id"], "GHSA-xxxx-xxxx-xxxx")
        self.assertEqual(vuln["severity"], "HIGH")

    @patch("query_osv.requests.post")
    def test_query_package_no_vulnerabilities(self, mock_post):
        """Test querying a package with no vulnerabilities."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}  # No vulns key
        mock_post.return_value = mock_response

        result = execute({
            "ecosystem": "npm",
            "package": "safe-package",
            "version": "1.0.0"
        })

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"]["vulnerabilities"], [])

    @patch("query_osv.requests.post")
    def test_api_error_handling(self, mock_post):
        """Test handling of API errors."""
        mock_post.side_effect = Exception("Network error")

        result = execute({
            "ecosystem": "PyPI",
            "package": "requests",
            "version": "2.28.0"
        })

        self.assertEqual(result["status"], "error")
        self.assertIn("Network error", result["error"])

    def test_map_severity_critical(self):
        """Test CVSS score to severity mapping."""
        self.assertEqual(_map_severity(9.8), "CRITICAL")
        self.assertEqual(_map_severity(10.0), "CRITICAL")

    def test_map_severity_high(self):
        """Test high severity mapping."""
        self.assertEqual(_map_severity(7.5), "HIGH")
        self.assertEqual(_map_severity(8.9), "HIGH")

    def test_map_severity_medium(self):
        """Test medium severity mapping."""
        self.assertEqual(_map_severity(5.0), "MEDIUM")
        self.assertEqual(_map_severity(6.9), "MEDIUM")

    def test_map_severity_low(self):
        """Test low severity mapping."""
        self.assertEqual(_map_severity(2.0), "LOW")
        self.assertEqual(_map_severity(3.9), "LOW")


if __name__ == "__main__":
    unittest.main()