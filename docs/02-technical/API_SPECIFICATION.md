# TradePulse – API Specification

**Version:** 1.1  
**Status:** Updated API Contract  
**API Style:** REST  
**Data Format:** JSON  
**Backend:** FastAPI  
**Authentication:** JWT Bearer Token

---

## 1. API Overview

TradePulse exposes REST APIs through FastAPI.

The API layer is responsible for:

- User authentication.
- Role-based authorization.
- Portfolio management.
- Asset management.
- Simulated transactions.
- Portfolio analytics.
- Market data retrieval.
- AI assistant interactions.

The backend enforces authentication, role permissions, and resource ownership.

The initial role model contains:

- `ADMIN`: Platform administration and asset catalog management.
- `USER`: Portfolio management and investment activities.

ADMIN and USER responsibilities are strictly separated.

## 2. API Conventions

### 2.1 Base URL

Local development:

```text
http://127.0.0.1:8000
```

### 2.2 API Prefix

```text
/api
```

### 2.3 Content Type

Requests and responses use:

```text
application/json
```

### 2.4 Authentication Header

Protected endpoints require:

```text
Authorization: Bearer <access_token>
```

### 2.5 HTTP Methods

| Method | Purpose |
|---|---|
| GET | Retrieve resources |
| POST | Create resources or execute operations |
| PUT | Replace a resource |
| PATCH | Partially update a resource |
| DELETE | Delete or deactivate a resource when permitted |

### 2.6 Authorization

Protected endpoints require a valid JWT access token.

Role-specific endpoints additionally require the appropriate role.

The backend uses:

- `get_current_user()` to identify the authenticated user.
- `require_role()` to enforce role-based permissions.
- `require_admin` for ADMIN-only operations.
- `require_user` for USER-only operations.

Roles are centrally defined through `UserRole` in `app/constants/roles.py`.

## 3. Standard HTTP Status Codes

| Status | Meaning |
|---|---|
| 200 | Successful request |
| 201 | Resource created |
| 204 | Successful request without response body |
| 400 | Invalid business request |
| 401 | Authentication required or invalid |
| 403 | Authenticated but not authorized |
| 404 | Resource not found or inaccessible |
| 409 | Resource conflict |
| 422 | Request validation failed |
| 429 | Rate limit exceeded |
| 500 | Internal server error |
| 502 | Upstream provider failure |
| 503 | Service temporarily unavailable |

### 3.1 Authentication and Authorization Error Handling

- `401 Unauthorized`: Missing, invalid, or expired authentication token.
- `403 Forbidden`: Authenticated user does not have the required role.
- `404 Not Found`: Requested resource does not exist or is not accessible within the user's ownership scope.

## 4. Authentication APIs

Base path:

`/api/auth`

### 4.1 User Registration

**Endpoint**

`POST /api/auth/register`

**Authentication:** Not required.

**Authorization:** Public endpoint.

**Request**

```json
{
  "full_name": "Adithya",
  "email": "adithya@example.com",
  "password": "StrongPassword123"
}
```

**Successful response**

HTTP 201 Created

```json
{
  "id": 1,
  "full_name": "Adithya",
  "email": "adithya@example.com",
  "role": "USER",
  "created_at": "2026-11-13T10:30:00Z"
}
```

**Validation rules**

- Full name: 2–100 characters.
- Email: Valid email format.
- Password: Minimum 8 characters, maximum 128 characters.
- Email must be unique.
- Role is assigned by the backend.
- Registration must not accept or permit user-controlled role assignment.

**Default role:** `USER`.

**Possible errors**

- 409: Email already registered.
- 422: Invalid request data.

Password hashes must never be included in API responses.

### 4.2 User Login

**Endpoint**

`POST /api/auth/login`

**Authentication:** Not required.

**Request**

```json
{
  "email": "adithya@example.com",
  "password": "StrongPassword123"
}
```

**Successful response**

HTTP 200 OK

```json
{
  "access_token": "<jwt_access_token>",
  "token_type": "bearer"
}
```

**Possible errors**

- 401: Invalid email or password.
- 422: Invalid request data.

The access token is used to authenticate subsequent protected API requests.

### 4.3 Get Current User

**Endpoint**

`GET /api/auth/me`

**Authentication:** Required.

**Authorization:** ADMIN and USER.

**Header**

```text
Authorization: Bearer <access_token>
```

**Successful response**

HTTP 200 OK

```json
{
  "id": 1,
  "full_name": "Adithya",
  "email": "adithya@example.com",
  "role": "USER",
  "created_at": "2026-11-13T10:30:00Z"
}
```

**Possible errors**

- 401: Missing, invalid, or expired token.

## 5. User Management APIs

Base path:

`/api/users`

**Status:** Planned.

Planned endpoints:

| Method | Endpoint | Description | Authorization |
|---|---|---|---|
| GET | `/api/users/me` | Retrieve profile | ADMIN / USER |
| PATCH | `/api/users/me` | Update profile | ADMIN / USER |
| DELETE | `/api/users/me` | Request account deletion | ADMIN / USER |

All endpoints require authentication.

Account deletion must follow the data-retention and transaction-history policies.

Role modification must not be exposed through ordinary user profile-update operations.

Future administrative user-management APIs must require ADMIN authorization.

## 6. Portfolio Management APIs

Base path:

`/api/portfolios`

**Authentication:** Required.

**Authorization:** USER only.

ADMIN accounts cannot access portfolio-management operations under the initial role-separation policy.

All portfolio operations must enforce ownership validation.

### 6.1 Create Portfolio

`POST /api/portfolios`

**Authorization:** USER.

**Request**

```json
{
  "name": "My Crypto Portfolio",
  "description": "Long-term crypto paper trading"
}
```

**Successful response**

HTTP 201 Created

```json
{
  "id": 1,
  "user_id": 2,
  "name": "My Crypto Portfolio",
  "description": "Long-term crypto paper trading",
  "base_currency": "USD",
  "initial_cash_balance": "100000.00",
  "cash_balance": "100000.00",
  "created_at": "2026-11-13T10:30:00Z",
  "updated_at": "2026-11-13T10:30:00Z"
}
```

The initial virtual cash balance is $100,000 USD.

The backend initializes portfolio currency and cash balances according to the configured portfolio defaults.

### 6.2 Get User Portfolios

`GET /api/portfolios`

**Authorization:** USER.

Returns portfolios belonging only to the authenticated user.

### 6.3 Get Portfolio by ID

`GET /api/portfolios/{portfolio_id}`

**Authorization:** USER.

Returns portfolio details after verifying ownership.

If the portfolio belongs to another user, the API must return 404.

### 6.4 Update Portfolio

`PATCH /api/portfolios/{portfolio_id}`

**Authorization:** USER.

**Request**

```json
{
  "name": "Updated Portfolio Name",
  "description": "Updated description"
}
```

The API must verify portfolio ownership before applying updates.

### 6.5 Delete Portfolio

`DELETE /api/portfolios/{portfolio_id}`

**Authorization:** USER.

Deletion must follow transaction-history and retention rules.

The API must verify ownership before deletion.

### 6.6 Portfolio Authorization Rules

- USER can create and manage portfolios.
- USER can access only their own portfolios.
- ADMIN cannot access portfolio APIs under the initial role-separation policy.
- Unauthenticated requests must return 401.
- Authenticated ADMIN requests must return 403.
- Cross-user portfolio access must return 404.

## 7. Asset Management APIs

Base path:

`/api/assets`

**Authentication:** Required.

Asset records are shared platform resources.

### 7.1 List Assets

`GET /api/assets`

**Authorization:** ADMIN and USER.

Returns supported assets.

**Query parameters**

| Parameter | Type | Description |
|---|---|---|
| asset_type | string | Filter by STOCK or CRYPTO |
| active_only | boolean | Filter active assets; defaults to true |

Example:

```text
GET /api/assets?asset_type=STOCK
```

Example:

```text
GET /api/assets?asset_type=CRYPTO&active_only=true
```

### 7.2 Get Asset by ID

`GET /api/assets/{asset_id}`

**Authorization:** ADMIN and USER.

Returns asset details.

Possible errors:

- 404: Asset not found.
- 401: Authentication required.

### 7.3 Create Asset

`POST /api/assets`

**Authorization:** ADMIN only.

**Request**

```json
{
  "symbol": "AAPL",
  "name": "Apple Inc.",
  "asset_type": "STOCK",
  "exchange": "NASDAQ",
  "currency": "USD"
}
```

**Successful response**

HTTP 201 Created

```json
{
  "id": 1,
  "symbol": "AAPL",
  "name": "Apple Inc.",
  "asset_type": "STOCK",
  "exchange": "NASDAQ",
  "currency": "USD",
  "is_active": true,
  "created_at": "2026-11-13T10:30:00Z",
  "updated_at": "2026-11-13T10:30:00Z"
}
```

**Validation rules**

- Symbol must not be empty.
- Name must not be empty.
- Asset type must be STOCK or CRYPTO.
- Symbol must be unique.
- Currency must contain three characters.

**Possible errors**

- 401: Missing or invalid token.
- 403: User does not have ADMIN permissions.
- 409: Asset symbol already exists.
- 422: Invalid request data.

### 7.4 Update Asset

`PATCH /api/assets/{asset_id}`

**Authorization:** ADMIN only.

**Request**

```json
{
  "name": "Apple Inc.",
  "exchange": "NASDAQ",
  "currency": "USD",
  "is_active": true
}
```

Only supplied fields are updated.

Possible errors:

- 401: Authentication required.
- 403: ADMIN access required.
- 404: Asset not found.
- 422: Invalid request data.

### 7.5 Deactivate Asset

`DELETE /api/assets/{asset_id}`

**Authorization:** ADMIN only.

Asset deletion uses a soft-delete approach.

The backend updates:

```text
is_active = false
```

The database record is retained to preserve historical references and future transaction integrity.

**Successful response**

HTTP 204 No Content.

Possible errors:

- 401: Authentication required.
- 403: ADMIN access required.
- 404: Asset not found.
- 400: Asset is already inactive.

### 7.6 Asset Authorization Matrix

| Operation | ADMIN | USER |
|---|---|---|
| List assets | Allowed | Allowed |
| Get asset details | Allowed | Allowed |
| Create asset | Allowed | 403 |
| Update asset | Allowed | 403 |
| Deactivate asset | Allowed | 403 |

## 8. Paper Trading APIs

Base path:

`/api/portfolios/{portfolio_id}/transactions`

**Status:** Planned.

**Authentication:** Required.

**Authorization:** USER only.

All transaction endpoints require portfolio ownership validation.

### 8.1 Execute Simulated Buy

`POST /api/portfolios/{portfolio_id}/transactions/buy`

**Request**

```json
{
  "asset_id": 1,
  "quantity": "0.5",
  "order_type": "MARKET"
}
```

**Successful response**

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

**Request**

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

**Authorization:** USER with portfolio ownership validation.

## 9. Holdings APIs

Base path:

`/api/portfolios/{portfolio_id}/holdings`

**Status:** Planned.

**Authorization:** USER with portfolio ownership validation.

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

**Status:** Planned.

**Authorization:** USER with portfolio ownership validation.

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

**Status:** Planned.

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

**Status:** Planned.

All user-specific assistant operations require authentication and USER authorization.

### 12.1 Ask AI Assistant

`POST /api/ai/chat`

**Request**

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

AI operations must not bypass role authorization or portfolio ownership validation.

## 13. Error Response Format

The API should use consistent error responses.

Example:

```json
{
  "detail": "Portfolio not found"
}
```

Authorization error example:

```json
{
  "detail": "USER access required"
}
```

Validation errors may use FastAPI's structured validation response.

Sensitive internal exceptions, credentials, SQL statements, and stack traces must not be exposed to API clients.

## 14. Authorization Requirements

1. Private endpoints must require authentication.
2. Every portfolio operation must verify USER authorization and ownership.
3. ADMIN accounts must not access portfolio-management endpoints.
4. Transactions must be associated with authorized portfolios.
5. Asset catalog read operations must be available to authenticated ADMIN and USER accounts.
6. Asset creation, updating, and deactivation must require ADMIN authorization.
7. Public registration must always assign the USER role.
8. Users must not be able to assign themselves ADMIN through public APIs.
9. AI tools must access only data authorized for the current user.
10. Users must not retrieve another user's private resources by changing resource IDs.
11. Role authorization must be enforced in the backend.
12. Missing or invalid authentication must return 401.
13. Insufficient role permissions must return 403.

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
- Role-based authorization.
- Cross-user resource access.
- Duplicate operations.
- Database failures.
- External provider failures.
- Pagination and filtering.

Swagger UI will be used during development.

Pytest will support automated API and integration tests.

### 16.1 RBAC Test Scenarios

| Scenario | Expected Result |
|---|---|
| Register a new account | USER assigned |
| Attempt to register with ADMIN role | Must not grant ADMIN |
| ADMIN views assets | 200 |
| USER views assets | 200 |
| ADMIN creates an asset | 201 |
| USER creates an asset | 403 |
| ADMIN updates an asset | 200 |
| USER updates an asset | 403 |
| ADMIN deactivates an asset | 204 |
| USER deactivates an asset | 403 |
| ADMIN accesses portfolio APIs | 403 |
| USER accesses own portfolio | Allowed |
| USER accesses another user's portfolio | 404 |
| Unauthenticated protected request | 401 |

## 17. Implementation Status

The following status reflects the development progress established during the current implementation workflow.

| API / Feature | Status |
|---|---|
| POST `/api/auth/register` | Implemented |
| POST `/api/auth/login` | Implemented |
| GET `/api/auth/me` | Implemented |
| Role assignment during registration | Implemented |
| Role returned in user response | Implemented |
| Portfolio CRUD APIs | Implemented and tested |
| Portfolio ownership validation | Implemented and tested |
| USER-only portfolio authorization | Implemented in code; final RBAC verification pending |
| Asset database model and migration | Implemented |
| Asset schemas and service layer | Implemented |
| Asset GET APIs | Implemented in route design; final verification pending |
| Asset POST API | Implemented in route design; ADMIN authorization verification pending |
| Asset PATCH API | Implemented in route design; ADMIN authorization verification pending |
| Asset DELETE/deactivation API | Implemented in route design; ADMIN authorization verification pending |
| User profile management | Planned |
| Paper-trading APIs | Planned |
| Holdings APIs | Planned |
| Analytics APIs | Planned |
| Market-data APIs | Planned |
| AI assistant APIs | Planned |

Endpoint definitions in this document are API contracts. Implementation status must be updated after the corresponding endpoints and authorization tests are verified.

---

**Document Owner:** TradePulse Development  
**Last Updated:** 2026-11-13