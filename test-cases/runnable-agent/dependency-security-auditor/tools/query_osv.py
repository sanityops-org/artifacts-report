#!/usr/bin/env python3
"""
query_osv: Query the OSV (Open Source Vulnerabilities) API for package vulnerabilities.

Queries https://api.osv.dev/v1/query for vulnerability data.
"""

import requests
import time
from typing import Any, Dict, List, Optional

OSV_API_URL = "https://api.osv.dev/v1/query"
MAX_RETRIES = 3
RETRY_DELAY = 1.0  # seconds


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Query OSV API for vulnerabilities affecting a package.

    Args:
        params: {
            "ecosystem": "PyPI" | "npm",
            "package": str,
            "version": str
        }

    Returns:
        {
            "status": "success" | "error",
            "data": {
                "package": str,
                "version": str,
                "vulnerabilities": [
                    {
                        "id": str,
                        "summary": str,
                        "severity": "CRITICAL" | "HIGH" | "MEDIUM" | "LOW",
                        "cvss_score": float,
                        "affected_versions": [str],
                        "fixed_versions": [str]
                    }
                ]
            },
            "error": str | None
        }
    """
    ecosystem = params.get("ecosystem")
    package = params.get("package")
    version = params.get("version")

    if not all([ecosystem, package, version]):
        return {
            "status": "error",
            "error": "Missing required parameters: ecosystem, package, version"
        }

    if ecosystem not in ("PyPI", "npm"):
        return {
            "status": "error",
            "error": f"Unsupported ecosystem: {ecosystem}. Must be 'PyPI' or 'npm'"
        }

    try:
        # Query OSV API with retry logic
        response_data = _query_osv_with_retry(ecosystem, package, version)

        # Parse vulnerabilities
        vulnerabilities = _parse_osv_response(response_data, version)

        return {
            "status": "success",
            "data": {
                "package": package,
                "version": version,
                "vulnerabilities": vulnerabilities
            }
        }

    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "error": f"OSV API timeout after {MAX_RETRIES} retries for {package}"
        }
    except requests.exceptions.ConnectionError:
        return {
            "status": "error",
            "error": "Network error: Cannot reach OSV API. Check internet connection."
        }
    except Exception as e:
        return {
            "status": "error",
            "error": f"OSV API error: {str(e)}"
        }


def _query_osv_with_retry(ecosystem: str, package: str, version: str) -> Dict:
    """Query OSV API with exponential backoff retry."""
    payload = {
        "version": version,
        "package": {
            "name": package,
            "ecosystem": ecosystem
        }
    }

    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(
                OSV_API_URL,
                json=payload,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            last_error = e
            if attempt < MAX_RETRIES - 1:
                # Exponential backoff
                delay = RETRY_DELAY * (2 ** attempt)
                time.sleep(delay)

    raise last_error


def _parse_osv_response(response_data: Dict, query_version: str) -> List[Dict]:
    """Parse OSV API response into standardized vulnerability format."""
    vulnerabilities = []

    vulns = response_data.get("vulns", [])
    if not vulns:
        return vulnerabilities

    for vuln in vulns:
        # Extract CVSS score and severity
        cvss_score = 0.0
        severities = vuln.get("severity", [])
        for sev in severities:
            if sev.get("type") == "CVSS_V3":
                score_value = sev.get("score", 0.0)
                # CVSS score can be a float, a string like "7.5", or a full vector string
                try:
                    if isinstance(score_value, (int, float)):
                        cvss_score = float(score_value)
                    else:
                        # String format - might be "7.5" or a vector string
                        cvss_score = float(str(score_value).split("/")[0])
                except:
                    cvss_score = 0.0
                break

        # Determine severity level
        severity = _map_severity(cvss_score)

        # Extract affected and fixed versions
        affected_versions = []
        fixed_versions = []

        for affected in vuln.get("affected", []):
            for version in affected.get("versions", []):
                affected_versions.append(version)

            for event in affected.get("ranges", []):
                for range_event in event.get("events", []):
                    if "fixed" in range_event:
                        fixed_versions.append(range_event["fixed"])

        vulnerabilities.append({
            "id": vuln.get("id", "UNKNOWN"),
            "summary": vuln.get("summary", "No description available"),
            "severity": severity,
            "cvss_score": cvss_score,
            "affected_versions": affected_versions,
            "fixed_versions": fixed_versions
        })

    # Sort by severity (Critical first)
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    vulnerabilities.sort(key=lambda v: severity_order.get(v["severity"], 4))

    return vulnerabilities


def _map_severity(cvss_score: float) -> str:
    """
    Map CVSS score to severity level.

    CVSS v3.1 scoring:
    - 0.1-3.9: Low
    - 4.0-6.9: Medium
    - 7.0-8.9: High
    - 9.0-10.0: Critical
    """
    if cvss_score >= 9.0:
        return "CRITICAL"
    elif cvss_score >= 7.0:
        return "HIGH"
    elif cvss_score >= 4.0:
        return "MEDIUM"
    else:
        return "LOW"


if __name__ == "__main__":
    # Simple CLI for testing
    import sys
    import json

    if len(sys.argv) >= 4:
        result = execute({
            "ecosystem": sys.argv[1],
            "package": sys.argv[2],
            "version": sys.argv[3]
        })
        print(json.dumps(result, indent=2))
    else:
        print("Usage: python query_osv.py <ecosystem> <package> <version>")
        print("Example: python query_osv.py PyPI requests 2.28.0")