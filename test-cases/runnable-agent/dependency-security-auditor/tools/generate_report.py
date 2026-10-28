#!/usr/bin/env python3
"""
generate_report: Format vulnerability scan results into a structured security report.

Produces a markdown-formatted report sorted by severity with actionable recommendations.
"""

from typing import Any, Dict, List
from collections import defaultdict


# Severity icons and colors
SEVERITY_ICONS = {
    "CRITICAL": "🔴",
    "HIGH": "🟠",
    "MEDIUM": "🟡",
    "LOW": "🟢"
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a formatted security audit report.

    Args:
        params: {
            "project_path": str,
            "scan_results": {
                "ecosystems": { ... },
                "vulnerabilities": [ ... ]
            }
        }

    Returns:
        {
            "status": "success",
            "data": {
                "report": str,  # Markdown-formatted report
                "summary": {
                    "total_packages": int,
                    "vulnerabilities_found": int,
                    "critical": int,
                    "high": int,
                    "medium": int,
                    "low": int
                }
            }
        }
    """
    project_path = params.get("project_path", "Unknown")
    scan_results = params.get("scan_results", {})

    if not scan_results:
        return {
            "status": "error",
            "error": "No scan results provided"
        }

    # Count packages
    ecosystems = scan_results.get("ecosystems", {})
    total_packages = 0
    python_packages = 0
    nodejs_packages = 0

    if "python" in ecosystems:
        python_packages = len(ecosystems["python"].get("packages", []))
        total_packages += python_packages

    if "nodejs" in ecosystems:
        nodejs_packages = len(ecosystems["nodejs"].get("packages", []))
        total_packages += nodejs_packages

    # Process vulnerabilities
    vulnerabilities = scan_results.get("vulnerabilities", [])

    # Group by severity
    by_severity = defaultdict(list)
    severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}

    for pkg_vulns in vulnerabilities:
        for vuln in pkg_vulns.get("vulnerabilities", []):
            severity = vuln.get("severity", "LOW")
            by_severity[severity].append({
                **vuln,
                "package": pkg_vulns.get("package"),
                "version": pkg_vulns.get("version")
            })
            severity_counts[severity] += 1

    total_vulnerabilities = sum(severity_counts.values())

    # Generate report
    report_lines = []

    # Header
    report_lines.append("# Security Audit Report")
    report_lines.append("")
    report_lines.append(f"**Project**: {project_path}")
    report_lines.append(f"**Scanned**: {python_packages} Python packages, {nodejs_packages} Node.js packages")
    report_lines.append(f"**Found**: {total_vulnerabilities} vulnerabilities")
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")

    # No vulnerabilities case
    if total_vulnerabilities == 0:
        report_lines.append(f"✓ All {total_packages} dependencies are clean. No known vulnerabilities detected.")
        return {
            "status": "success",
            "data": {
                "report": "\n".join(report_lines),
                "summary": {
                    "total_packages": total_packages,
                    "vulnerabilities_found": 0,
                    "critical": 0,
                    "high": 0,
                    "medium": 0,
                    "low": 0,
                    **severity_counts
                }
            }
        }

    # Vulnerabilities by severity (sorted Critical -> Low)
    severity_order = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]

    for severity in severity_order:
        vulns = by_severity.get(severity, [])
        if not vulns:
            continue

        icon = SEVERITY_ICONS.get(severity, "⚪")
        report_lines.append(f"## {icon} {severity.title()} ({len(vulns)})")
        report_lines.append("")

        for vuln in vulns:
            report_lines.append(f"### {vuln['id']} in `{vuln['package']}=={vuln['version']}`")
            report_lines.append(f"- **CVSS**: {vuln.get('cvss_score', 'N/A')} ({severity})")

            fixed_versions = vuln.get("fixed_versions", [])
            if fixed_versions:
                report_lines.append(f"- **Fixed in**: {', '.join(fixed_versions)}")

            report_lines.append(f"- **Summary**: {vuln.get('summary', 'No description available')}")

            # Recommendation
            if fixed_versions:
                recommended_version = min(fixed_versions)  # Lowest safe version
                report_lines.append(f"- **Recommend**: Upgrade to `{vuln['package']}>={recommended_version}`")

            report_lines.append("")

        report_lines.append("---")
        report_lines.append("")

    return {
        "status": "success",
        "data": {
            "report": "\n".join(report_lines),
            "summary": {
                "total_packages": total_packages,
                "vulnerabilities_found": total_vulnerabilities,
                "critical": severity_counts["CRITICAL"],
                "high": severity_counts["HIGH"],
                "medium": severity_counts["MEDIUM"],
                "low": severity_counts["LOW"],
                **severity_counts
            }
        }
    }


if __name__ == "__main__":
    # CLI for testing
    import sys
    import json

    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            scan_results = json.load(f)
        result = execute({"project_path": "/test", "scan_results": scan_results})
        print(result["data"]["report"])
    else:
        print("Usage: python generate_report.py <scan_results.json>")