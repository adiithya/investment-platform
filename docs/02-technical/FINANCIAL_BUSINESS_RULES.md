# TradePulse – Financial Business Rules

**Version:** 1.1  
**Status:** Updated  
**Last Updated:** 2026-11-13

---

## 1. Purpose

This document defines the financial rules and calculations used by TradePulse for portfolio management and simulated trading.

All financial calculations must be performed by the backend using deterministic business logic.

AI components may explain financial results but must never independently calculate, modify, or invent financial records.

The backend must enforce role-based authorization before allowing access to portfolio and trading operations.

## 2. MVP Configuration

| Configuration | Value |
|---|---|
| Supported markets | US stocks and cryptocurrency |
| Default portfolio currency | USD |
| Initial virtual cash | $100,000 per portfolio |
| Transaction fees | Zero |
| Short selling | Not supported |
| Trading type | Paper trading |
| Real-money execution | Not supported |

## 3. User Roles and Financial Access Rules

TradePulse supports two roles: ADMIN and USER.

### 3.1 USER Permissions

A USER can:

1. Create multiple personal portfolios.
2. View their own portfolios.
3. Update their own portfolio information.
4. Delete their own portfolios according to the defined deletion policy.
5. Perform simulated buy and sell transactions within their own portfolios.
6. View their own holdings and transaction history.
7. View their own portfolio valuation and profit/loss.
8. Access AI-powered portfolio insights when available.

### 3.2 ADMIN Permissions

An ADMIN can:

1. View supported assets.
2. Create supported assets.
3. Update existing asset information.
4. Deactivate assets.
5. Access future platform administration capabilities.

An ADMIN cannot:

- Create or manage investment portfolios.
- Perform simulated buy or sell transactions.
- Access USER portfolio balances.
- Access USER holdings or transaction history.
- Access USER-specific portfolio analytics.

### 3.3 Authorization Rules

1. Only authenticated USER accounts can create and manage portfolios.
2. Only authenticated USER accounts can perform paper trades.
3. Every portfolio must belong to exactly one USER.
4. Every portfolio operation must verify ownership.
5. Every transaction must be associated with a portfolio owned by the authenticated USER.
6. ADMIN accounts must not receive automatic access to USER financial data.
7. Role restrictions must be enforced by backend authorization logic.
8. Public registration must always assign the USER role.
9. Users must not be able to assign or change their own role through public APIs.
10. Both ADMIN and USER accounts can view supported assets, but only ADMIN accounts can modify the asset catalog.

## 4. Portfolio Rules

1. A USER can create multiple portfolios.
2. Every portfolio belongs to exactly one USER.
3. Each new portfolio receives an initial virtual cash balance of $100,000.
4. Portfolio cash must never become negative.
5. Portfolio data must be accessible only to its owner.
6. Portfolio currency is USD for the MVP.
7. Portfolio starting cash must be configurable in future versions.
8. ADMIN accounts cannot create or manage portfolios.

## 5. Buy Transaction Rules

When a USER purchases an asset:

1. The authenticated user must have the USER role.
2. The portfolio must belong to the authenticated USER.
3. The asset must be valid and supported.
4. The purchase quantity must be greater than zero.
5. The purchase price must not be negative.
6. The USER must have sufficient virtual cash.
7. The purchase cost is calculated using quantity multiplied by unit price.
8. Transaction fees are zero in the MVP.
9. Portfolio cash decreases by the purchase cost.
10. Holdings quantity increases by the purchased quantity.
11. Average purchase price is recalculated.
12. The transaction is stored in transaction history.

### Formula

Purchase Cost = Quantity × Unit Price

Remaining Cash = Previous Cash − Purchase Cost

### Example

Buy 10 shares at $100 each.

| Description | Amount |
|---|---:|
| Previous cash | $100,000 |
| Quantity | 10 |
| Unit price | $100 |
| Purchase cost | $1,000 |
| Remaining cash | $99,000 |

## 6. Average Purchase Price Rules

The weighted average purchase price is calculated whenever an additional buy transaction occurs.

### Formula

Average Purchase Price = Total Purchase Cost / Total Quantity Purchased

### Example

First purchase:

- 10 shares at $100 = $1,000

Second purchase:

- 10 shares at $120 = $1,200

Combined position:

- Total quantity = 20
- Total cost = $2,200
- Average purchase price = $110

The average purchase price remains unchanged when part of the position is sold under the MVP weighted-average cost method.

## 7. Sell Transaction Rules

When a USER sells an asset:

1. The authenticated user must have the USER role.
2. The portfolio must belong to the authenticated USER.
3. The USER must own the asset in the selected portfolio.
4. The sell quantity must be greater than zero.
5. The sell quantity must not exceed the available holding quantity.
6. The selling price must not be negative.
7. Portfolio cash increases by the sale proceeds.
8. Holdings quantity decreases by the sold quantity.
9. Realized profit or loss is calculated.
10. The transaction is recorded in transaction history.

### Formula

Sale Proceeds = Sell Quantity × Selling Price

Realized P&L = Sale Proceeds − (Sell Quantity × Average Purchase Price)

### Example

- Average purchase price = $110
- Sell quantity = 5
- Selling price = $130

Sale proceeds = 5 × $130 = $650

Cost basis = 5 × $110 = $550

Realized profit = $100

Remaining holding quantity = 15 shares.

## 8. Profit and Loss Rules

TradePulse must distinguish between realized and unrealized profit and loss.

### Realized P&L

Profit or loss from assets that have already been sold.

Realized P&L = Sale Proceeds − Cost Basis of Sold Quantity

### Unrealized P&L

Profit or loss on assets that are still held.

Unrealized P&L = (Current Market Price − Average Purchase Price) × Remaining Quantity

### Example

- Remaining quantity = 15 shares
- Average purchase price = $110
- Current market price = $130

Unrealized P&L = (130 − 110) × 15 = $300

### Total P&L

Total P&L = Realized P&L + Unrealized P&L

The platform must clearly distinguish realized and unrealized values.

## 9. Portfolio Valuation Rules

Portfolio Market Value = Sum of (Holding Quantity × Current Market Price)

Total Portfolio Value = Available Virtual Cash + Portfolio Market Value

The system must use the latest available market prices.

If market prices are unavailable or stale, the platform must communicate that limitation instead of silently treating missing data as a valid current price.

Only the owning USER can access their portfolio valuation.

## 10. Transaction Fee Rules

Transaction fees are zero in the MVP.

The financial calculation layer must be designed so fixed or percentage-based fees can be introduced later without rewriting the trading workflow.

## 11. Short Selling Rules

Short selling is not supported in the MVP.

A USER can sell only an asset quantity already available in their portfolio holdings.

The system must reject sell requests that exceed the available quantity.

## 12. Transaction Consistency

1. Every successful trade must create a transaction record.
2. The transaction and its corresponding cash and holding updates must succeed or fail together.
3. Failed trades must not partially modify portfolio data.
4. Concurrent trade requests must not result in incorrect balances or holdings.
5. Financial calculations must use decimal arithmetic.
6. Transaction history must be retained for auditability.
7. Duplicate trade submissions must be prevented through an idempotency mechanism when implemented.
8. Every trade must be associated with the correct portfolio and authenticated USER.
9. ADMIN accounts must not be able to execute financial transactions.

## 13. Financial Data Precision

- Use PostgreSQL NUMERIC for monetary values and quantities.
- Use Python Decimal for financial calculations.
- Avoid floating-point arithmetic for financial calculations.
- Store timestamps in UTC.
- Define appropriate precision and scale for each monetary and quantity field.

## 14. AI Responsibilities

AI may:

- Explain portfolio performance.
- Summarize realized and unrealized P&L.
- Explain asset allocation.
- Answer questions using verified portfolio data.
- Identify trends based on available market and portfolio information.

AI must not:

- Invent portfolio balances or asset prices.
- Independently calculate authoritative financial metrics.
- Modify holdings or transaction records.
- Execute real-money trades.
- Present generated insights as guaranteed investment advice.
- Access financial information belonging to another USER.
- Bypass backend authentication, authorization, or portfolio ownership checks.

AI-generated explanations must use financial results supplied by the backend.

## 15. Future Enhancements

The following features are outside the initial MVP:

- INR and multi-currency portfolios.
- Configurable transaction fees.
- Short selling.
- Dividends and stock splits.
- Tax calculations.
- Advanced portfolio performance metrics.
- Real brokerage integrations, subject to separate security and authorization design.

## 16. Implementation Principle

The backend financial engine is the single source of truth for all financial calculations.

All portfolio balances, holdings, transaction records, and profit/loss values must be derived from validated business rules.

Only authenticated USER accounts can perform investment activities, and every operation must validate portfolio ownership.

ADMIN permissions are restricted to platform administration and asset catalog management. ADMIN accounts must not access or modify USER investment records.