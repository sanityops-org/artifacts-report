# Dependency & Security Auditor

## Industry
Software Development

## Description
A specialized agent that scans Python and Node.js project dependencies for known security vulnerabilities using the OSV (Open Source Vulnerabilities) database. The agent produces prioritized security reports and generates dry-run upgrade diffs — it never modifies files without explicit user action.

## Key Features
- **Dual Ecosystem Support**: Scans Python (requirements.txt, pyproject.toml, setup.py) and Node.js (package.json, package-lock.json)
- **OSV Integration**: Uses Google's free OSV API — no authentication required
- **Prioritized Reports**: Vulnerabilities sorted by severity (Critical → High → Medium → Low)
- **Dry-Run Diffs**: Shows exactly what would change, user retains full control

## Skills
- `vulnerability_scan`: Scan dependencies for security vulnerabilities
- `upgrade_planner`: Create dry-run upgrade plans

## Created
2026-10-08

## Version
v1.0.0

## Author
agent_artifacts

## Requirements
- Python 3.11+
- `requests` library

## Usage

```bash
# Install dependencies
pip install requests tomli

# Run the agent
python scripts/run.py
```

## Example

```
User: Scan /home/user/myproject for vulnerabilities
Agent: [Produces security report with CVE details and upgrade recommendations]

User: Show me what I need to upgrade
Agent: [Generates dry-run diff showing version changes]
```

## Run From This Repository

From the repository root:

```bash
cd test-cases/runnable-agent/dependency-security-auditor
python3 -m venv .venv
source .venv/bin/activate
python -m pip install requests tomli
python scripts/run.py
```
