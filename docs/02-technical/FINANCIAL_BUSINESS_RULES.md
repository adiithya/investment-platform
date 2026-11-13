# TradePulse – Financial Business Rules

## 1. Purpose

This document defines the financial rules and calculations used by TradePulse for portfolio management and simulated trading.

All financial calculations must be performed by the backend using deterministic business logic.

AI components may explain financial results but must never independently calculate, modify, or invent financial records.

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

## 3. Portfolio Rules

1. A registered user can create multiple portfolios.
2. Every portfolio belongs to exactly one user.
3. Each new portfolio receives an initial virtual cash balance of $100,000.
4. Portfolio cash must never become negative.
5. Portfolio data must be accessible only to its owner.
6. Portfolio currency is USD for the MVP.
7. Portfolio starting cash must be configurable in future versions.

## 4. Buy Transaction Rules

When a user purchases an asset:

1. The asset must be valid and supported.
2. The purchase quantity must be greater than zero.
3. The purchase price must not be negative.
4. The user must have sufficient virtual cash.
5. The purchase cost is calculated using quantity multiplied by unit price.
6. Transaction fees are zero in the MVP.
7. Portfolio cash decreases by the purchase cost.
8. Holdings quantity increases by the purchased quantity.
9. Average purchase price is recalculated.
10. The transaction is stored in transaction history.

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

## 5. Average Purchase Price Rules

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

## 6. Sell Transaction Rules

When a user sells an asset:

1. The user must own the asset.
2. The sell quantity must be greater than zero.
3. The sell quantity must not exceed the available holding quantity.
4. The selling price must not be negative.
5. Portfolio cash increases by the sale proceeds.
6. Holdings quantity decreases by the sold quantity.
7. Realized profit or loss is calculated.
8. The transaction is recorded in transaction history.

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

## 7. Profit and Loss Rules

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

## 8. Portfolio Valuation Rules

Portfolio Market Value = Sum of (Holding Quantity × Current Market Price)

Total Portfolio Value = Available Virtual Cash + Portfolio Market Value

The system must use the latest available market prices.

If market prices are unavailable or stale, the platform must communicate that limitation instead of silently treating missing data as a valid current price.

## 9. Transaction Fee Rules

Transaction fees are zero in the MVP.

The financial calculation layer must be designed so fixed or percentage-based fees can be introduced later without rewriting the trading workflow.

## 10. Short Selling Rules

Short selling is not supported in the MVP.

A user can sell only an asset quantity already available in their portfolio holdings.

The system must reject sell requests that exceed the available quantity.

## 11. Transaction Consistency

1. Every successful trade must create a transaction record.
2. The transaction and its corresponding cash and holding updates must succeed or fail together.
3. Failed trades must not partially modify portfolio data.
4. Concurrent trade requests must not result in incorrect balances or holdings.
5. Financial calculations must use decimal arithmetic.
6. Transaction history must be retained for auditability.
7. Duplicate trade submissions must be prevented through an idempotency mechanism when implemented.

## 12. Financial Data Precision

- Use PostgreSQL NUMERIC for monetary values and quantities.
- Use Python Decimal for financial calculations.
- Avoid floating-point arithmetic for financial calculations.
- Store timestamps in UTC.
- Define appropriate precision and scale for each monetary and quantity field.

## 13. AI Responsibilities

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

## 14. Future Enhancements

The following features are outside the initial MVP:

- INR and multi-currency portfolios.
- Configurable transaction fees.
- Short selling.
- Dividends and stock splits.
- Tax calculations.
- Advanced portfolio performance metrics.
- Real brokerage integrations, subject to separate security and authorization design.

## 15. Implementation Principle

The backend financial engine is the single source of truth for all financial calculations.

All portfolio balances, holdings, transaction records, and profit/loss values must be derived from validated business rules.