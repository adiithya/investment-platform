# TradePulse – Acceptance Criteria

## 1. Purpose

This document defines the conditions that must be satisfied before a TradePulse feature can be considered complete.

Acceptance criteria will be used during development, functional testing, and API testing.

## 2. Authentication and User Management

### AC-001: User Registration

- Given a user provides valid name, email, and password, when they submit registration, then a new account must be created.
- Given an email is already registered, when the user attempts registration with that email, then the system must reject the request with an appropriate duplicate-email error.
- Given required fields are missing or invalid, when registration is submitted, then validation errors must be returned.
- The password must never be stored as plain text.
- The registration response must not expose the password or password hash.

### AC-002: User Login

- Given a registered user provides valid credentials, when they submit login, then the system must return an access token.
- Given the password or email is incorrect, when login is attempted, then the system must return an authentication error.
- The response must not expose the stored password hash.
- The generated access token must have an expiry time.

### AC-003: View My Profile

- Given a user has a valid access token, when they request their profile, then only their own profile information must be returned.
- Given a user does not provide a valid token, when they request their profile, then access must be denied.

### AC-004: Secure Account Access

- Protected endpoints must require valid authentication.
- A user must not be able to access another user's private data by changing resource IDs.
- Invalid, expired, or malformed tokens must be rejected.

## 3. Portfolio Management

### AC-005: Create Portfolio

- Given an authenticated user provides a valid portfolio name, when they create a portfolio, then the portfolio must be saved and associated with their user ID.
- A portfolio must not be created without a valid name.
- A user must not be able to create a portfolio for another user.

### AC-006: View Portfolios

- Given a user has created multiple portfolios, when they request their portfolio list, then only their portfolios must be returned.
- Given a user has no portfolios, then an empty list must be returned.
- Portfolio data must not include another user's portfolios.

### AC-007: Update Portfolio

- Given a user owns a portfolio, when they submit valid updates, then the portfolio information must be updated.
- Given a user attempts to update another user's portfolio, then the operation must be rejected.
- Invalid portfolio data must return validation errors.

### AC-008: Delete Portfolio

- Given a user owns a portfolio, when they request its deletion, then the system must follow the defined deletion policy.
- A user must not be able to delete another user's portfolio.
- The system must not leave orphaned transaction or holding records.
- The deletion policy must be finalized before this feature is implemented.

## 4. Asset Management

### AC-009: Search Assets

- Given supported assets exist, when a user searches by symbol, then matching assets must be returned.
- When a user searches by asset name, matching assets must be returned.
- When no asset matches the search, the API must return an empty result.
- Search results must contain only supported and active assets.

### AC-010: View Asset Details

- Given a valid asset ID exists, when a user requests its details, then the asset information must be returned.
- Given an invalid asset ID is provided, then the API must return an appropriate not-found response.

### AC-011: Support Multiple Asset Types

- The system must identify each asset using its supported asset type.
- Assets must have valid symbols and names.
- Unsupported asset types must be rejected.

## 5. Paper Trading

### AC-012: Simulate Buy Transaction

- Given a user owns a portfolio and selects a valid asset, when they submit a valid buy transaction, then the transaction must be recorded.
- The transaction must include quantity, unit price, fees, and calculated total amount.
- Quantity must be greater than zero.
- Unit price must not be negative.
- Fees must not be negative.
- The transaction and corresponding holding update must succeed or fail together.
- The transaction must be marked as a simulated trade and must not trigger real-money execution.

### AC-013: Simulate Sell Transaction

- Given a user has sufficient holdings, when they submit a valid sell transaction, then the transaction must be recorded and holdings must be reduced.
- The sell quantity must be greater than zero.
- A user must not be able to sell more than the available holding quantity.
- A failed sell transaction must not change the holding quantity.
- The transaction and holding update must be committed atomically.

### AC-014: View Transaction History

- Given a portfolio contains transactions, when a user requests its transaction history, then the system must return the transactions belonging to that portfolio.
- Transaction history must support appropriate pagination.
- Transactions must be displayed with their type, asset, quantity, price, fees, total, and execution time.
- Users must not be able to view another user's transaction history.

### AC-015: Prevent Invalid Trades

- The system must reject zero or negative quantities.
- The system must reject invalid prices and fees.
- The system must reject selling more quantity than the user holds.
- Duplicate submissions must not create duplicate transactions when an idempotency mechanism is implemented.
- All financial calculations must use precise decimal arithmetic rather than floating-point arithmetic.

## 6. Holdings and Portfolio Analytics

### AC-016: View Current Holdings

- Given a portfolio has completed buy and sell transactions, when the user requests holdings, then the system must return the current position for each asset.
- Holdings must reflect successfully completed transactions only.
- Fully sold assets must not appear as active positive-quantity holdings.
- The sum of transaction effects must reconcile with the holding quantity.

### AC-017: View Portfolio Value

- Given holdings and valid price data are available, when the user requests portfolio value, then the system must calculate the total using holding quantities and applicable prices.
- If price data is unavailable, the system must clearly indicate that valuation cannot be fully calculated.
- The valuation must identify the currency used.

### AC-018: View Profit and Loss

- The system must calculate profit and loss using defined cost-basis and valuation rules.
- Realized and unrealized profit and loss must be distinguishable.
- The calculation must use consistent currency and decimal precision.
- Results must be traceable to holdings, transactions, and price data.

### AC-019: View Asset Allocation

- The system must calculate allocation using the value of each holding relative to total portfolio value.
- Allocation percentages must be based on the same valuation timestamp and currency basis.
- The displayed allocation must reconcile to the portfolio total, subject to rounding.

## 7. Market Data

### AC-020: View Latest Asset Prices

- Given valid price data is available, when a user requests an asset price, then the latest available price must be returned.
- The response must include the asset, price, currency, provider, and price timestamp where available.
- The system must indicate when price data is unavailable or stale.

### AC-021: View Historical Prices

- Given historical price records exist, when a user requests prices for a date range, then matching records must be returned in chronological order.
- Invalid date ranges must be rejected.
- The response must identify the currency and timestamps associated with the prices.

## 8. AI Investment Assistant

### AC-022: Ask Investment Questions

- Given a user is authenticated, when they submit a supported question, then the AI assistant must return a response.
- The assistant must use only data the authenticated user is authorized to access.
- Unsupported or ambiguous questions must be handled clearly.
- AI responses must not be presented as guaranteed investment advice.

### AC-023: Receive Portfolio Insights

- AI insights must be grounded in the user's available portfolio data.
- The system must not invent holdings, prices, or performance figures.
- Where data is missing, the assistant must disclose the limitation.
- Financial metrics shown in an insight must come from backend calculations.

### AC-024: Understand Profit and Loss

- Given portfolio performance data is available, when a user asks for an explanation, then the assistant must explain the relevant figures using the supplied calculation results.
- The explanation must distinguish realized and unrealized profit and loss when both are available.
- The assistant must not change financial records.

### AC-025: Ask Questions About Investment Documents

- Given a user has uploaded a supported document, when they ask a question about its contents, then the assistant must retrieve relevant document information.
- Responses should identify supporting document references when available.
- The assistant must not treat unrelated documents as evidence for the answer.
- Users must not retrieve documents belonging to other users.

### AC-026: Receive Explainable AI Responses

- AI responses must distinguish source-backed information from generated explanations.
- The assistant must communicate uncertainty when the available information is insufficient.
- The assistant must not execute trades or modify portfolio records without an explicitly designed and authorized workflow.

## 9. Security and Reliability

### AC-027: Protect User Data

- All private resources must be associated with an authenticated user.
- Database queries must enforce ownership checks.
- Passwords must be securely hashed.
- Sensitive credentials and tokens must not be written to application logs.

### AC-028: Maintain Transaction Accuracy

- Every successful trade must update the transaction ledger and holdings consistently.
- Failed transactions must not partially update financial records.
- Concurrent trade requests must not produce incorrect holdings.
- Financial calculations must use decimal precision.

### AC-029: Handle System Errors

- The API must return appropriate HTTP status codes.
- Error responses must provide useful messages without exposing internal stack traces or secrets.
- Unexpected failures must be logged for debugging.
- The application must remain usable when an individual operation fails.

## 10. Definition of Done

A feature can be considered complete when:

1. The implementation satisfies its acceptance criteria.
2. Input validation is implemented.
3. Authentication and authorization are verified where required.
4. Relevant unit tests pass.
5. Relevant API or integration tests pass.
6. Error scenarios are tested.
7. API documentation is updated.
8. No sensitive information is exposed in responses or logs.
9. The implementation is reviewed and committed to the repository.

## 11. Implementation Status

| Feature | Status |
|---|---|
| User registration | Implemented |
| User login | Implemented |
| JWT authentication | Implemented |
| Protected profile endpoint | Implemented |
| Portfolio management | Planned |
| Asset management | Planned |
| Paper trading | Planned |
| Holdings and analytics | Planned |
| Market data integration | Planned |
| AI assistant and RAG | Planned |

This status should be updated as features are implemented and verified.