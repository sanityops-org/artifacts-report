# Securities investment customer service

## Industry
Securities/Finance

## Function description
The investment customer service intelligence for securities customers supports fund transfer, stock trading, product subscription and other types of business processing. Embedded in the securities app, customers can complete self-service operations through natural language dialogue.

## List of skills
- fund_operation：Bank certificate transfer, fund inquiry
- stock_trading：Stock trading, order withdrawal, position/transaction inquiry
- product_purchase：Financial management/fund subscription and redemption, new stock subscription
- inquiry：Market inquiry, business guidelines

## Date of creation
2026-09-03

## Edition
v1.0.0

## Author
Agent Artifacts Team

## Operation mode

**Precondition**: Make sure that the `sanityops_agent` framework has been installed

```bash
# Installation dependency
pip install -r requirements.txt

# Start up Agent
python scripts/run.py
```

## Run From This Repository

From the repository root:

```bash
cd test-cases/runnable-agent/securities-customer-service
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/run.py
```
