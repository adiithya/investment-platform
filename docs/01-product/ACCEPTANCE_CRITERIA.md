# TradePulse – Acceptance Criteria

**Version:** 1.1  
**Status:** Updated  
**Last Updated:** 2026-11-13

---

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
- Every publicly registered account must receive the USER role automatically.

### AC-002: User Login

- Given a registered user provides valid credentials, when they submit login, then the system must return an access token.
- Given the password or email is incorrect, when login is attempted, then the system must return an authentication error.
- The response must not expose the stored password hash.
- The generated access token must have an expiry time.
- Both ADMIN and USER accounts must be able to authenticate successfully using valid credentials.

### AC-003: View My Profile

- Given a user has a valid access token, when they request their profile, then only their own profile information must be returned.
- Given a user does not provide a valid token, when they request their profile, then access must be denied.
- The profile response must include the user's assigned role.
- The response must not expose the password or password hash.

### AC-004: Secure Account Access

- Protected endpoints must require valid authentication.
- A user must not be able to access another user's private data by changing resource IDs.
- Invalid, expired, or malformed tokens must be rejected.
- Role-based authorization must be enforced by the backend.
- Frontend restrictions must not replace backend authorization checks.

---

## 3. Portfolio Management

**Access:** USER only.

### AC-005: Create Portfolio

- Given an authenticated USER provides a valid portfolio name, when they create a portfolio, then the portfolio must be saved and associated with their user ID.
- A portfolio must not be created without a valid name.
- A USER must not be able to create a portfolio for another user.
- An ADMIN must not be able to create a portfolio.
- Portfolio creation must use the configured initial cash balance and base currency.

### AC-006: View Portfolios

- Given a USER has created multiple portfolios, when they request their portfolio list, then only their portfolios must be returned.
- Given a USER has no portfolios, then an empty list must be returned.
- Portfolio data must not include another user's portfolios.
- An ADMIN must not be able to access the portfolio list endpoint.

### AC-007: Update Portfolio

- Given a USER owns a portfolio, when they submit valid updates, then the portfolio information must be updated.
- Given a USER attempts to update another user's portfolio, then the operation must be rejected.
- Invalid portfolio data must return validation errors.
- An ADMIN must not be able to update a portfolio.

### AC-008: Delete Portfolio

- Given a USER owns a portfolio, when they request its deletion, then the system must follow the defined deletion policy.
- A USER must not be able to delete another user's portfolio.
- An ADMIN must not be able to delete a portfolio.
- The system must not leave orphaned transaction or holding records.
- The deletion policy must be finalized before this feature is implemented.

---

## 4. Asset Management

**Access:** Both ADMIN and USER can view assets. Only ADMIN can create, update, or deactivate assets.

### AC-009: Search Assets

- Given supported assets exist, when an authenticated user searches by symbol, then matching assets must be returned.
- When an authenticated user searches by asset name, matching assets must be returned.
- When no asset matches the search, the API must return an empty result.
- Search results must contain only supported and active assets when active-only filtering is applied.
- Both ADMIN and USER must be able to view supported assets.

### AC-010: View Asset Details

- Given a valid asset ID exists, when an authenticated user requests its details, then the asset information must be returned.
- Given an invalid asset ID is provided, then the API must return an appropriate not-found response.
- Both ADMIN and USER must be able to view asset details.

### AC-011: Support Multiple Asset Types

- The system must identify each asset using its supported asset type.
- Assets must have valid symbols and names.
- Unsupported asset types must be rejected.
- The initial supported asset types must include STOCK and CRYPTO.

### AC-030: Create Assets

- Given an authenticated ADMIN provides valid asset information, when the ADMIN submits an asset creation request, then the asset must be saved successfully.
- Asset symbols must be unique.
- Required fields must be validated.
- Unsupported asset types must be rejected.
- A USER attempting to create an asset must receive HTTP 403.
- An unauthenticated request must receive HTTP 401.

### AC-031: Update Asset Information

- Given an authenticated ADMIN requests an update for an existing asset, when valid changes are submitted, then the asset information must be updated.
- Given an invalid asset ID is provided, then the API must return HTTP 404.
- Invalid update data must return validation errors.
- A USER attempting to update an asset must receive HTTP 403.
- An unauthenticated request must receive HTTP 401.

### AC-032: Deactivate Assets

- Given an authenticated ADMIN requests deactivation of an existing asset, when the request is processed, then the asset must be marked inactive.
- Deactivation must not physically delete the asset record.
- Deactivated assets must not appear in active-only asset results.
- A USER attempting to deactivate an asset must receive HTTP 403.
- An unauthenticated request must receive HTTP 401.

### AC-033: Restrict Asset Management to ADMIN

- Only ADMIN accounts must be allowed to create assets.
- Only ADMIN accounts must be allowed to update assets.
- Only ADMIN accounts must be allowed to deactivate assets.
- USER accounts must not be able to bypass restrictions by directly calling APIs.
- Both ADMIN and USER accounts must be allowed to view supported assets.

---

## 5. Paper Trading

**Access:** USER only.

### AC-012: Simulate Buy Transaction

- Given a USER owns a portfolio and selects a valid asset, when they submit a valid buy transaction, then the transaction must be recorded.
- The transaction must include quantity, unit price, fees, and calculated total amount.
- Quantity must be greater than zero.
- Unit price must not be negative.
- Fees must not be negative.
- The transaction and corresponding holding update must succeed or fail together.
- The transaction must be marked as a simulated trade and must not trigger real-money execution.
- An ADMIN must not be allowed to perform a buy transaction.

### AC-013: Simulate Sell Transaction

- Given a USER has sufficient holdings, when they submit a valid sell transaction, then the transaction must be recorded and holdings must be reduced.
- The sell quantity must be greater than zero.
- A USER must not be able to sell more than the available holding quantity.
- A failed sell transaction must not change the holding quantity.
- The transaction and holding update must be committed atomically.
- An ADMIN must not be allowed to perform a sell transaction.

### AC-014: View Transaction History

- Given a portfolio contains transactions, when a USER requests its transaction history, then the system must return the transactions belonging to that portfolio.
- Transaction history must support appropriate pagination.
- Transactions must be displayed with their type, asset, quantity, price, fees, total, and execution time.
- Users must not be able to view another user's transaction history.
- ADMIN accounts must not be allowed to access USER transaction history.

### AC-015: Prevent Invalid Trades

- The system must reject zero or negative quantities.
- The system must reject invalid prices and fees.
- The system must reject selling more quantity than the USER holds.
- Duplicate submissions must not create duplicate transactions when an idempotency mechanism is implemented.
- All financial calculations must use precise decimal arithmetic rather than floating-point arithmetic.
- Only USER accounts must be allowed to execute paper trades.

---

## 6. Holdings and Portfolio Analytics

**Access:** USER only.

### AC-016: View Current Holdings

- Given a portfolio has completed buy and sell transactions, when the USER requests holdings, then the system must return the current position for each asset.
- Holdings must reflect successfully completed transactions only.
- Fully sold assets must not appear as active positive-quantity holdings.
- The sum of transaction effects must reconcile with the holding quantity.
- A USER must not be able to view another user's holdings.
- ADMIN accounts must not be able to access USER holdings.

### AC-017: View Portfolio Value

- Given holdings and valid price data are available, when the USER requests portfolio value, then the system must calculate the total using holding quantities and applicable prices.
- If price data is unavailable, the system must clearly indicate that valuation cannot be fully calculated.
- The valuation must identify the currency used.
- A USER must only be able to view portfolio values belonging to their own portfolios.

### AC-018: View Profit and Loss

- The system must calculate profit and loss using defined cost-basis and valuation rules.
- Realized and unrealized profit and loss must be distinguishable.
- The calculation must use consistent currency and decimal precision.
- Results must be traceable to holdings, transactions, and price data.
- A USER must only be able to view profit and loss for their own portfolios.

### AC-019: View Asset Allocation

- The system must calculate allocation using the value of each holding relative to total portfolio value.
- Allocation percentages must be based on the same valuation timestamp and currency basis.
- The displayed allocation must reconcile to the portfolio total, subject to rounding.
- A USER must only be able to view allocation for their own portfolios.

---

## 7. Market Data

**Access:** USER-facing functionality.

### AC-020: View Latest Asset Prices

- Given valid price data is available, when a USER requests an asset price, then the latest available price must be returned.
- The response must include the asset, price, currency, provider, and price timestamp where available.
- The system must indicate when price data is unavailable or stale.

### AC-021: View Historical Prices

- Given historical price records exist, when a USER requests prices for a date range, then matching records must be returned in chronological order.
- Invalid date ranges must be rejected.
- The response must identify the currency and timestamps associated with the prices.

---

## 8. AI Investment Assistant

**Access:** USER-facing functionality.

### AC-022: Ask Investment Questions

- Given a USER is authenticated, when they submit a supported question, then the AI assistant must return a response.
- The assistant must use only data the authenticated USER is authorized to access.
- Unsupported or ambiguous questions must be handled clearly.
- AI responses must not be presented as guaranteed investment advice.
- ADMIN accounts must not access USER-specific AI portfolio analysis.

### AC-023: Receive Portfolio Insights

- AI insights must be grounded in the USER's available portfolio data.
- The system must not invent holdings, prices, or performance figures.
- Where data is missing, the assistant must disclose the limitation.
- Financial metrics shown in an insight must come from backend calculations.
- The assistant must not access another USER's portfolio data.

### AC-024: Understand Profit and Loss

- Given portfolio performance data is available, when a USER asks for an explanation, then the assistant must explain the relevant figures using the supplied calculation results.
- The explanation must distinguish realized and unrealized profit and loss when both are available.
- The assistant must not change financial records.

### AC-025: Ask Questions About Investment Documents

- Given a USER has uploaded a supported document, when they ask a question about its contents, then the assistant must retrieve relevant document information.
- Responses should identify supporting document references when available.
- The assistant must not treat unrelated documents as evidence for the answer.
- Users must not retrieve documents belonging to other users.

### AC-026: Receive Explainable AI Responses

- AI responses must distinguish source-backed information from generated explanations.
- The assistant must communicate uncertainty when the available information is insufficient.
- The assistant must not execute trades or modify portfolio records without an explicitly designed and authorized workflow.

---

## 9. Security and Reliability

### AC-027: Protect User Data

- All private resources must be associated with an authenticated user.
- Database queries must enforce ownership checks.
- Passwords must be securely hashed.
- Sensitive credentials and tokens must not be written to application logs.
- ADMIN accounts must not be granted automatic access to USER portfolio or transaction data.
- USER accounts must not be able to access ADMIN-only asset management operations.

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

### AC-034: Enforce Role-Based Access

- Every protected endpoint must verify the authenticated user's role where role restrictions apply.
- A USER attempting to access an ADMIN-only operation must receive HTTP 403.
- An ADMIN attempting to access USER-only portfolio or trading operations must receive HTTP 403.
- Requests without valid authentication must receive HTTP 401.
- Role restrictions must be enforced by the backend, not only by the frontend.

### AC-035: Prevent Unauthorized Role Assignment

- Public registration requests must not accept a role field.
- Every newly registered account must receive the USER role.
- A USER must not be able to promote their own account to ADMIN through an API request.
- Only the authorized administrative provisioning process may create or promote ADMIN accounts.

### AC-036: Enforce Portfolio Ownership

- Every portfolio operation must verify that the authenticated USER owns the requested portfolio.
- Changing a portfolio ID must not allow access to another USER's portfolio.
- Unauthorized access to another USER's portfolio must not expose its data.
- The API must return the defined not-found response for resources outside the USER's ownership scope.

### AC-037: Enforce Asset Management Permissions

- ADMIN accounts must be allowed to create, update, and deactivate assets.
- USER accounts must be denied access to asset creation, update, and deactivation operations.
- Both ADMIN and USER accounts must be able to access permitted asset read operations.
- Permission checks must apply to direct API requests as well as frontend interactions.

---

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

For role-restricted functionality, testing must include the permitted role, the prohibited role, and unauthenticated access.

---

## 11. Implementation Status

| Feature | Status |
|---|---|
| User registration | Implemented |
| User login | Implemented |
| JWT authentication | Implemented |
| Protected profile endpoint | Implemented |
| User role field and database constraint | Implemented |
| Default USER role during registration | Implemented in code |
| Role authorization dependencies | Implemented in code; final API verification pending |
| Portfolio model and CRUD APIs | Implemented |
| Portfolio ownership validation | Implemented |
| USER-only portfolio authorization | Final verification pending |
| Asset model and database migration | Implemented |
| Asset schemas and service layer | Implemented |
| Asset CRUD route implementation | Implemented; final RBAC verification pending |
| ADMIN-only asset management | Final verification pending |
| Paper trading | Planned |
| Holdings and analytics | Planned |
| Market data integration | Planned |
| AI assistant and RAG | Planned |

This status should be updated as features are implemented and verified.