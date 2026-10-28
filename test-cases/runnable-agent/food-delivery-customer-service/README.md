# Intelligent customer service of takeaway platform

## Industry
Takeaway/Catering

## Function description
Intelligent customer service for takeaway platform customers supports two major scenarios: order processing (ordering/inquiry/order reminder/modification/cancellation) and refund after-sales (apply for refund/inquiry refund/transfer manual work orders). Embedded in the takeaway platform App, customers complete self-service operations through natural language dialogue.

## List of skills
- order_management：Place an order, inquire about the order, urge the order, modify the order, cancel the order
- after_sale：Apply for a refund, check the progress of the refund, and transfer the manual work order

## Date of creation
2026-09-04

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
cd test-cases/runnable-agent/food-delivery-customer-service
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/run.py
```
