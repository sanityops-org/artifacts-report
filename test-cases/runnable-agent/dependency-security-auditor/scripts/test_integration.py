#!/usr/bin/env python3
"""Integration test for Dependency & Security Auditor."""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "tools"))

import detect_dependencies
import query_osv
import generate_report
import create_upgrade_diff


def test_python_project():
    """Test scanning a Python project."""
    print("Testing Python project scan...")

    # Detect dependencies
    result = detect_dependencies.execute({
        "project_path": str(project_root / "data/sample_projects/python_vulnerable")
    })
    print(f"  Found {result['data']['total_packages']} packages")

    # Query OSV for each package
    vulnerabilities = []
    for pkg in result["data"]["ecosystems"]["python"]["packages"]:
        print(f"  Checking {pkg['name']} {pkg['version']}...")
        osv_result = query_osv.execute({
            "ecosystem": "PyPI",
            "package": pkg["name"],
            "version": pkg["version"]
        })
        if osv_result["status"] == "success" and osv_result["data"]["vulnerabilities"]:
            vulnerabilities.append({
                "package": pkg["name"],
                "version": pkg["version"],
                "vulnerabilities": osv_result["data"]["vulnerabilities"]
            })

    # Generate report
    if vulnerabilities:
        report_result = generate_report.execute({
            "project_path": "python_vulnerable",
            "scan_results": {
                "ecosystems": result["data"]["ecosystems"],
                "vulnerabilities": vulnerabilities
            }
        })
        print("\n" + report_result["data"]["report"])
    else:
        print("  No vulnerabilities found (or OSV API not reachable)")

    return vulnerabilities


def test_nodejs_project():
    """Test scanning a Node.js project."""
    print("\nTesting Node.js project scan...")

    result = detect_dependencies.execute({
        "project_path": str(project_root / "data/sample_projects/nodejs_vulnerable")
    })
    print(f"  Found {result['data']['total_packages']} packages")

    vulnerabilities = []
    for pkg in result["data"]["ecosystems"]["nodejs"]["packages"]:
        print(f"  Checking {pkg['name']} {pkg['version']}...")
        osv_result = query_osv.execute({
            "ecosystem": "npm",
            "package": pkg["name"],
            "version": pkg["version"]
        })
        if osv_result["status"] == "success" and osv_result["data"]["vulnerabilities"]:
            vulnerabilities.append({
                "package": pkg["name"],
                "version": pkg["version"],
                "vulnerabilities": osv_result["data"]["vulnerabilities"]
            })

    if vulnerabilities:
        report_result = generate_report.execute({
            "project_path": "nodejs_vulnerable",
            "scan_results": {
                "ecosystems": result["data"]["ecosystems"],
                "vulnerabilities": vulnerabilities
            }
        })
        print("\n" + report_result["data"]["report"])
    else:
        print("  No vulnerabilities found (or OSV API not reachable)")

    return vulnerabilities


if __name__ == "__main__":
    print("=" * 60)
    print("  Integration Test: Dependency & Security Auditor")
    print("=" * 60)
    print()

    try:
        py_vulns = test_python_project()
        js_vulns = test_nodejs_project()

        print("\n" + "=" * 60)
        print("  Integration test completed successfully!")
        print(f"  Python vulnerabilities: {len(py_vulns)}")
        print(f"  Node.js vulnerabilities: {len(js_vulns)}")
        print("=" * 60)
    except Exception as e:
        print(f"\nError during integration test: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)