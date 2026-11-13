# TradePulse – API Specification

**Version:** 1.0  
**Status:** Initial API Contract  
**API Style:** REST  
**Data Format:** JSON  
**Backend:** FastAPI  
**Authentication:** JWT Bearer Token

---

## 1. API Overview

TradePulse exposes REST APIs through FastAPI.

The API layer is responsible for:

- User authentication.
- Portfolio management.
- Asset management.
- Simulated transactions.
- Portfolio analytics.
- Market data retrieval.
- AI assistant interactions.

## 2. API Conventions

### Base URL

Local development:

`http://127.0.0.1:8000`

### API Prefix

`/api`

### Content Type

Requests and responses use:

`application/json`

### Authentication Header

Protected endpoints require:

`Authorization: Bearer <access_token>`

### HTTP Methods

| Method | Purpose |
|---|---|
| GET | Retrieve resources |
| POST | Create resources or execute operations |
| PUT | Replace a resource |
| PATCH | Partially update a resource |
| DELETE | Delete a resource when permitted |

## 3. Standard HTTP Status Codes

| Status | Meaning |
|---|---|
| 200 | Successful request |
| 201 | Resource created |
| 204 | Successful request without response body |
| 400 | Invalid business request |
| 401 | Authentication required or invalid |
| 403 | Authenticated but not authorized |
| 404 | Resource not found |
| 409 | Resource conflict |
| 422 | Request validation failed |
| 429 | Rate limit exceeded |
| 500 | Internal server error |
| 502 | Upstream provider failure |
| 503 | Service temporarily unavailable |

## 4. Authentication APIs

Base path:

`/api/auth`

### 4.1 User Registration

**Endpoint**

`POST /api/auth/register`

Authentication: Not required.

Request:

```json
{
  "full_name": "Adithya",
  "email": "adithya@example.com",
  "password": "StrongPassword123"
}
```

Successful response:

HTTP 201 Created

```json
{
  "id": 1,
  "full_name": "Adithya",
  "email": "adithya@example.com",
  "created_at": "2026-11-13T10:30:00Z"
}
```

Validation rules:

- Full name: 2–100 characters.
- Email: Valid email format.
- Password: Minimum 8 characters, maximum 128 characters.
- Email must be unique.

Possible errors:

- 409: Email already registered.
- 422: Invalid request data.

Password hashes must never be included in API responses.

### 4.2 User Login

**Endpoint**

`POST /api/auth/login`

Authentication: Not required.

Request:

```json
{
  "email": "adithya@example.com",
  "password": "StrongPassword123"
}
```

Successful response:

HTTP 200 OK

```json
{
  "access_token": "<jwt_access_token>",
  "token_type": "bearer"
}
```

Possible errors:

- 401: Invalid email or password.
- 422: Invalid request data.

### 4.3 Get Current User

**Endpoint**

`GET /api/auth/me`

Authentication: Required.

Header:

`Authorization: Bearer <access_token>`

Successful response:

HTTP 200 OK

```json
{
  "id": 1,
  "full_name": "Adithya",
  "email": "adithya@example.com",
  "created_at": "2026-11-13T10:30:00Z"
}
```

Possible errors:

- 401: Missing, invalid, or expired token.

## 5. User Management APIs

Base path:

`/api/users`

Planned endpoints:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/users/me` | Retrieve profile |
| PATCH | `/api/users/me` | Update profile |
| DELETE | `/api/users/me` | Request account deletion |

All endpoints require authentication.

Account deletion must follow the data-retention and transaction-history policies.

## 6. Portfolio Management APIs

Base path:

`/api/portfolios`

All portfolio endpoints require authentication.

### 6.1 Create Portfolio

`POST /api/portfolios`

Request:

```json
{
  "name": "My Crypto Portfolio",
  "description": "Long-term crypto paper trading",
  "base_currency": "USD"
}
```

Successful response:

HTTP 201 Created

```json
{
  "id": 1,
  "name": "My Crypto Portfolio",
  "description": "Long-term crypto paper trading",
  "base_currency": "USD",
  "created_at": "2026-11-13T10:30:00Z"
}
```

### 6.2 Get User Portfolios

`GET /api/portfolios`

Returns portfolios belonging to the authenticated user.

### 6.3 Get Portfolio by ID

`GET /api/portfolios/{portfolio_id}`

Returns portfolio details after verifying ownership.

### 6.4 Update Portfolio

`PATCH /api/portfolios/{portfolio_id}`

Request:

```json
{
  "name": "Updated Portfolio Name",
  "description": "Updated description"
}
```

### 6.5 Delete Portfolio

`DELETE /api/portfolios/{portfolio_id}`

Deletion must follow transaction-history and retention rules.

## 7. Asset Management APIs

Base path:

`/api/assets`

Planned endpoints:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/assets` | List supported assets |
| GET | `/api/assets/{asset_id}` | Get asset details |
| GET | `/api/assets/search` | Search assets |
| GET | `/api/assets/{asset_id}/prices` | Retrieve historical prices |

Query parameters may include:

- asset_type
- symbol
- search
- page
- page_size
- start_date
- end_date

## 8. Paper Trading APIs

Base path:

`/api/portfolios/{portfolio_id}/transactions`

All transaction endpoints require authentication and portfolio ownership validation.

### 8.1 Execute Simulated Buy

`POST /api/portfolios/{portfolio_id}/transactions/buy`

Request:

```json
{
  "asset_id": 1,
  "quantity": "0.5",
  "order_type": "MARKET"
}
```

Successful response:

HTTP 201 Created

```json
{
  "id": 101,
  "portfolio_id": 1,
  "asset_id": 1,
  "transaction_type": "BUY",
  "quantity": "0.5",
  "unit_price": "65000.00",
  "fees": "10.00",
  "total_amount": "32510.00",
  "status": "EXECUTED"
}
```

The execution price must come from an approved price source or explicitly defined simulation pricing rule.

### 8.2 Execute Simulated Sell

`POST /api/portfolios/{portfolio_id}/transactions/sell`

Request:

```json
{
  "asset_id": 1,
  "quantity": "0.25",
  "order_type": "MARKET"
}
```

The service must validate available holdings and calculate net proceeds.

### 8.3 Retrieve Transactions

`GET /api/portfolios/{portfolio_id}/transactions`

Supports pagination and optional filters:

- asset_id
- transaction_type
- start_date
- end_date
- page
- page_size

## 9. Holdings APIs

Base path:

`/api/portfolios/{portfolio_id}/holdings`

Planned endpoints:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/portfolios/{portfolio_id}/holdings` | Retrieve all holdings |
| GET | `/api/portfolios/{portfolio_id}/holdings/{asset_id}` | Retrieve a specific holding |

Holdings responses may include:

- Asset details.
- Quantity.
- Average purchase price.
- Current market price.
- Current valuation.
- Unrealized profit/loss.

Financial calculations must be performed by backend services.

## 10. Portfolio Analytics APIs

Base path:

`/api/portfolios/{portfolio_id}/analytics`

Planned endpoints:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/summary` | Portfolio summary |
| GET | `/allocation` | Asset allocation |
| GET | `/performance` | Portfolio performance |
| GET | `/profit-loss` | Profit/loss breakdown |
| GET | `/history` | Historical portfolio valuation |

Responses must identify the valuation timestamp and relevant currency.

## 11. Market Data APIs

Base path:

`/api/market`

Planned endpoints:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/prices/{asset_id}` | Latest available price |
| GET | `/prices/{asset_id}/history` | Historical prices |
| GET | `/assets/search` | Search market assets |

Market data responses should include:

- Asset identifier.
- Price.
- Quote currency.
- Provider.
- Price timestamp.
- Data freshness information where available.

## 12. AI Assistant APIs

Base path:

`/api/ai`

All user-specific assistant operations require authentication.

### 12.1 Ask AI Assistant

`POST /api/ai/chat`

Request:

```json
{
  "message": "Explain my portfolio performance",
  "portfolio_id": 1,
  "conversation_id": null
}
```

Potential response:

```json
{
  "conversation_id": "conversation-id",
  "message": "Your portfolio performance summary...",
  "sources": []
}
```

AI responses must use authorized portfolio data and clearly distinguish facts, calculations, and generated explanations.

### 12.2 Retrieve Conversation History

`GET /api/ai/conversations`

Returns conversations belonging to the authenticated user.

### 12.3 Retrieve Conversation Messages

`GET /api/ai/conversations/{conversation_id}/messages`

Returns authorized conversation history.

## 13. Error Response Format

The API should use consistent error responses.

Example:

```json
{
  "detail": "Portfolio not found"
}
```

Validation errors may use FastAPI's structured validation response.

Sensitive internal exceptions, credentials, SQL statements, and stack traces must not be exposed to API clients.

## 14. Authorization Requirements

1. Private endpoints must require authentication.
2. Every portfolio operation must verify ownership.
3. Transactions must be associated with authorized portfolios.
4. AI tools must access only data authorized for the current user.
5. Users must not be able to retrieve another user's private resources by changing resource IDs.

## 15. API Versioning

The initial development API will use the `/api` prefix.

Future external or production API versioning may use:

`/api/v1`

A versioning strategy must be introduced before a stable public API is released.

## 16. API Testing

API testing will cover:

- Successful requests.
- Missing authentication.
- Invalid authentication.
- Invalid request data.
- Unauthorized resource access.
- Duplicate operations.
- Database failures.
- External provider failures.
- Pagination and filtering.

Swagger UI will be used during development.

Pytest will support automated API and integration tests.

## 17. Implementation Status

Currently implemented:

- POST `/api/auth/register`
- POST `/api/auth/login`
- GET `/api/auth/me`

Planned:

- User profile management.
- Portfolio APIs.
- Asset APIs.
- Paper-trading APIs.
- Holdings APIs.
- Analytics APIs.
- Market-data APIs.
- AI assistant APIs.

Endpoint definitions in this document are initial contracts. Their implementation must follow the relevant module requirements and acceptance criteria.

---

**Document Owner:** TradePulse Development  
**Last Updated:** 2026-11-13