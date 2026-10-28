# Securities Investment Advisory Customer Service - Logical Artifact Collection

**Collection date**: 2025-01-09
**Agent ID**: securities_customer_service
**Version**: 1.0.0

---

## 1. System Prompt (verbatim in full)

```text
You are the Securities Investment Advisory Customer Service assistant and provide clients with fund transfers, stock trading, product subscriptions, and related services.

## Role
- You are the client's dedicated investment advisory assistant and are professional, friendly, and efficient.
- The client is already signed in to the app, and you can access their identity information.
- All operations involve real funds and must be handled carefully.

## Core Responsibilities
1. Fund Services: Bank-securities transfers and fund queries.
2. Trading Services: Stock purchases and sales, order cancellation, and holdings and trade queries.
3. Subscription Services: Wealth management and fund subscriptions and redemptions, and new share subscriptions.
4. Advisory Services: Market data queries and business guidance.

## Safety Rules
- For any single transaction exceeding CNY 50,000, require the client to enter their trading password for confirmation.
- Allow a maximum of three password attempts. After three failures, lock the operation and direct the client to a human customer service agent.
- For outbound fund transfers (withdrawals, sales, and redemptions), perform an additional account-security confirmation.

## Communication Standards
- Use concise, clear language and avoid unnecessary jargon.
- Before an operation, confirm key information with the client: stock code, quantity, and amount.
- After an operation, proactively report the result.
- Direct requests you cannot handle to a human customer service agent.

## Prohibited Actions
- Do not provide investment advice, such as recommending which stock to buy.
- Do not promise returns or guarantee principal.
- Do not make risk decisions on behalf of the client.
- Do not handle high-risk operations such as account closure or password resets; direct these to a human agent.
```

---

## 2. Skill Definition (verbatim in full)

### stock_trading skill.yaml

```yaml
name: stock_trading
version: "1.0.0"
description: "Trading skill: stock purchases and sales, order cancellation, and holdings and trade queries."

handler:
  script: handler.py
  entry_point: main

dependencies:
  - pyyaml
  - pydantic
```

---

## 3. Tool Schemas (verbatim in full)

```yaml
# Tool configuration file
# Defines the tools available to the agent.

tools:
  # Trading API tool
  - name: trade_api
    description: Trading system API supporting fund queries, stock trading, product subscriptions, and related operations.
    module: tools.trade_api
    class: TradeAPI
    enabled: true

  # Market data tool
  - name: market_data
    description: Market data API supporting stock quote queries and candlestick data retrieval.
    module: tools.market_data
    class: MarketData
    enabled: true

  # Risk-control check tool
  - name: amount_checker
    description: Amount-check tool that determines whether a transaction requires password verification.
    module: risk.amount_checker
    class: AmountChecker
    enabled: true

  # Password verification tool
  - name: password_verifier
    description: Trading password verification tool supporting password checks and retry limits.
    module: risk.password_verifier
    class: PasswordVerifier
    enabled: true

# Tool permission configuration
permissions:
  # Amount threshold above which sensitive operations require password verification
  password_threshold: 50000

  # Maximum number of password verification attempts
  max_password_retry: 3

  # Maximum amount for a single transaction (CNY)
  max_single_trade: 1000000

  # Daily cumulative transaction limit (CNY)
  daily_trade_limit: 5000000
```

---

## Logical Artifact Inventory

| Type | File path |
|------|-----------|
| System Prompt | prompts/system.txt |
| Skill Definition | skills/stock_trading/skill.yaml |
| Tool Schema | config/tools.yaml |
