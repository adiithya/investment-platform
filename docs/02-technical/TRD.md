# TradePulse – Technical Requirements Document (TRD)

**Product:** TradePulse  
**Version:** 1.1  
**Status:** Updated Draft  
**Product Type:** AI-powered investment and paper-trading platform

---

## 1. Technical Overview

TradePulse will use a modular full-stack architecture consisting of a Next.js frontend, Python FastAPI backend, PostgreSQL database, and a provider-independent AI integration layer.

The architecture will prioritize modularity, security, maintainability, testability, and future scalability.

The backend will be responsible for authentication, role-based authorization, business logic, financial calculations, and persistence.

Role-Based Access Control (RBAC) will separate platform administration from investment activities.

## 2. Technology Stack

### 2.1 Frontend

| Technology | Purpose |
|---|---|
| Next.js | Frontend application framework |
| React | Component-based UI |
| TypeScript | Type safety |
| Tailwind CSS | Styling |
| Redux Toolkit | Shared application state where needed |
| React Hook Form | Form management |
| Zod | Frontend schema validation |

### 2.2 Backend

| Technology | Purpose |
|---|---|
| Python 3.12 | Backend programming language |
| FastAPI | REST API framework |
| Pydantic | Request and response validation |
| Pydantic Settings | Environment configuration |
| SQLAlchemy 2.x | ORM and database operations |
| Psycopg 3 | PostgreSQL driver |
| Alembic | Database migrations |
| PyJWT | JWT generation and verification |
| Argon2 | Password hashing |

### 2.3 Database

| Technology | Purpose |
|---|---|
| PostgreSQL | Primary relational database |
| SQLAlchemy ORM | Database abstraction |
| Alembic | Schema versioning |
| pgvector | Future vector storage and similarity search |

### 2.4 AI and Machine Learning

| Technology | Purpose |
|---|---|
| Python provider SDKs | LLM communication |
| LangChain | LLM integrations and retrieval utilities |
| LangGraph | Stateful AI workflows |
| MCP | Standardized tool integration |
| pgvector | Vector similarity search |
| Ollama | Optional local model execution |

AI integrations must support multiple model providers through a common internal interface.

Potential providers include OpenAI, Google Gemini, Anthropic, and locally hosted models.

### 2.5 Background Processing and Infrastructure

| Technology | Purpose |
|---|---|
| Redis | Caching and task coordination |
| Celery | Background task processing |
| Docker | Application containerization |
| Pytest | Backend testing |
| OpenTelemetry | Observability |
| GitHub | Source control and collaboration |

These technologies will be introduced when required rather than installed all at once.

## 3. Application Architecture

The application will be organized into three major areas:

1. Frontend application.
2. Backend API application.
3. AI and data processing capabilities.

The frontend communicates with the backend through REST APIs.

The backend owns:

- Authentication.
- Role-based authorization.
- Business logic.
- Financial calculations.
- Data validation.
- Persistence.
- User-level data isolation.

AI services consume validated application data and approved external information sources.

### 3.1 Authorization Architecture

The backend will enforce authorization using role-based access control.

The initial role model contains two roles:

- ADMIN: Platform administration.
- USER: Investment and portfolio management.

ADMIN and USER responsibilities are strictly separated.

Authorization must be enforced at the API and backend dependency levels. Frontend restrictions alone are not sufficient.

## 4. Backend Architecture

### 4.1 Backend Source Structure

The backend will follow a modular layered architecture.

```text
tradepulse-backend/
│
├── app/
│   ├── api/
│   │   ├── routes/
│   │   └── dependencies.py
│   │
│   ├── constants/
│   │   ├── __init__.py
│   │   └── roles.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   │
│   ├── database/
│   │   ├── base.py
│   │   └── session.py
│   │
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── modules/
│   ├── utils/
│   └── main.py
│
├── migrations/
├── tests/
├── requirements.txt
├── .env.example
└── .gitignore
```

### 4.2 Layer Responsibilities

**API Layer**

- Expose REST endpoints.
- Validate incoming requests.
- Handle HTTP responses.
- Apply authentication and authorization dependencies.

**Schema Layer**

- Validate request payloads.
- Define response structures.
- Enforce data constraints.

**Service Layer**

- Implement business logic.
- Coordinate application operations.
- Perform financial calculations.
- Enforce domain rules.

**Model Layer**

- Define SQLAlchemy ORM entities.
- Define database relationships.
- Map application entities to database tables.

**Database Layer**

- Configure database engine.
- Manage SQLAlchemy sessions.
- Provide database metadata.

**Core Layer**

- Manage configuration.
- Provide security utilities.
- Centralize shared application settings.

**Constants Layer**

- Store shared application constants.
- Centralize role definitions.
- Avoid repeated hardcoded role strings across the application.

## 5. Database Requirements

PostgreSQL will be the primary application database.

SQLAlchemy 2.x will be used for ORM operations.

Alembic will manage database schema changes.

Initial entities are expected to include:

- Users.
- Portfolios.
- Assets.
- Transactions.
- Holdings or derived position data.
- Market price records.

Additional tables will be introduced based on detailed database design.

### 5.1 User Role Data

The users table will contain a role column to support authorization.

| Column | Type | Requirement |
|---|---|---|
| id | INTEGER | Primary key |
| full_name | VARCHAR | User's full name |
| email | VARCHAR | Unique email address |
| password_hash | VARCHAR | Secure password hash |
| role | VARCHAR(20) | Authorization role |
| created_at | TIMESTAMP | Account creation timestamp |

Role configuration:

- Default role: `USER`.
- Allowed roles: `ADMIN`, `USER`.
- Role column must not be nullable.
- A database CHECK constraint must restrict role values.
- Public registration must not accept a role supplied by the client.

### 5.2 Role Constants

Role definitions will be centralized in:

`app/constants/roles.py`

```python
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"
```

Application code must use `UserRole.ADMIN` and `UserRole.USER` instead of repeating string literals.

### 5.3 Data Integrity

- Primary keys must uniquely identify records.
- Foreign keys must maintain relationships.
- User-owned records must be associated with their owners.
- Email addresses must be unique.
- Financial quantities and monetary values must use appropriate decimal precision.
- Transactions must preserve an auditable history.
- Database changes must be managed through migrations.
- User roles must contain only supported values.

Use PostgreSQL `NUMERIC` and Python `Decimal` for financial calculations instead of binary floating-point arithmetic.

## 6. Authentication and Authorization

### 6.1 Authentication

Authentication will use JWT access tokens.

Password storage will use Argon2 hashing.

Requirements:

- Passwords must never be stored in plain text.
- JWT signatures must be verified.
- Token expiration must be enforced.
- Protected endpoints must identify the authenticated user.
- User-owned resources must be checked against the authenticated user.
- Sensitive configuration must be stored in environment variables.

Token refresh and revocation strategies will be designed before introducing long-lived sessions.

### 6.2 Role-Based Access Control

TradePulse will initially support two roles.

**ADMIN**

Responsibilities:

- Create investment assets.
- Update asset information.
- Activate and deactivate assets.
- View the asset catalog.
- Access future platform administration functionality when implemented.

ADMIN accounts will not have portfolio-management or paper-trading permissions.

**USER**

Responsibilities:

- View available assets.
- Create portfolios.
- Retrieve their own portfolios.
- Update their own portfolios.
- Delete their own portfolios.
- Perform future paper-trading activities.
- Access future investment analytics.

USER accounts cannot create, update, or deactivate assets.

### 6.3 Role Assignment

- New registrations must receive the `USER` role automatically.
- Registration schemas must not expose a role field.
- Users must not be able to promote themselves to ADMIN through public APIs.
- Initial ADMIN provisioning will be performed manually through a controlled PostgreSQL database operation.
- Administrative role changes must be restricted to trusted provisioning procedures.

### 6.4 Authorization Implementation

Authorization will use reusable FastAPI dependencies.

The authenticated user will first be identified through:

`get_current_user()`

Role authorization will be handled through:

`require_role()`

The application will expose role-specific dependencies:

- `require_admin`
- `require_user`

Conceptual implementation:

```python
def require_role(required_role: str):
    def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:
        if current_user.role != required_role:
            raise HTTPException(
                status_code=403,
                detail="Insufficient permissions",
            )

        return current_user

    return role_checker
```

Role dependencies:

```python
require_admin = require_role(UserRole.ADMIN.value)
require_user = require_role(UserRole.USER.value)
```

The implementation must use the centralized `UserRole` constants.

### 6.5 Authorization Matrix

| Operation | ADMIN | USER |
|---|---|---|
| View assets | Allowed | Allowed |
| Create assets | Allowed | Forbidden |
| Update assets | Allowed | Forbidden |
| Deactivate assets | Allowed | Forbidden |
| Create portfolios | Forbidden | Allowed |
| View own portfolios | Forbidden | Allowed |
| Update own portfolios | Forbidden | Allowed |
| Delete own portfolios | Forbidden | Allowed |
| Manage another user's portfolio | Forbidden | Forbidden |
| Paper trading | Forbidden | Allowed |

The ADMIN role is intended for platform administration only. It must not automatically grant investment-user permissions.

### 6.6 HTTP Authorization Responses

The backend must distinguish authentication failures from authorization failures.

| Status code | Meaning |
|---|---|
| 401 Unauthorized | Missing, invalid, or expired authentication token |
| 403 Forbidden | Authenticated user lacks the required role |
| 404 Not Found | Requested resource does not exist or is not accessible under the user's ownership scope |

## 7. API Requirements

REST APIs will use JSON request and response bodies.

### 7.1 API Conventions

- Appropriate HTTP methods.
- Standard HTTP status codes.
- Consistent error response structures.
- Request validation using Pydantic.
- Pagination for collection endpoints.
- Authentication dependencies for protected endpoints.
- Role authorization dependencies for restricted endpoints.
- API documentation through OpenAPI and Swagger UI.

### 7.2 Initial API Groups

- Authentication.
- User management.
- Portfolio management.
- Asset management.
- Transactions.
- Market data.
- Portfolio analytics.
- AI assistant.

### 7.3 API Authorization Requirements

**Authentication APIs**

- Registration.
- Login.
- Current-user information.

Registration must always assign the default USER role.

**Portfolio APIs**

- Accessible only to USER accounts.
- Every portfolio operation must enforce ownership validation.
- Users must not access another user's portfolio by changing the portfolio ID.

**Asset APIs**

- GET operations: available to authenticated ADMIN and USER accounts.
- POST operations: ADMIN only.
- PATCH operations: ADMIN only.
- DELETE/deactivation operations: ADMIN only.

Asset deactivation should use a soft-delete approach by setting `is_active = false`, preserving asset references for future transaction history.

**Future APIs**

Transactions, analytics, and AI assistant endpoints will follow the USER authorization policy unless a specific feature requires a different permission model.

## 8. Financial Calculation Requirements

Financial calculations must be deterministic and independently testable.

The backend must calculate:

- Cash balances.
- Asset quantities.
- Average purchase price.
- Transaction totals.
- Realized profit/loss.
- Unrealized profit/loss.
- Portfolio valuation.
- Asset allocation.

The calculation engine must use validated transaction and market-price data.

LLMs must not be responsible for authoritative financial calculations.

## 9. Market Data Integration

Market data will be accessed through a provider abstraction.

The architecture should support multiple market-data providers without requiring changes to portfolio business logic.

Requirements:

- Normalize provider responses.
- Validate prices and timestamps.
- Handle unavailable data.
- Track price timestamps and source information.
- Cache suitable responses.
- Distinguish delayed, stale, and unavailable prices.

## 10. AI Integration Requirements

AI functionality must be separated from core financial business logic.

### 10.1 Provider Abstraction

Create a common interface for model providers.

Business logic should not directly depend on a specific LLM vendor.

### 10.2 AI Assistant

The assistant should access approved tools and user-authorized data.

AI operations must respect the authenticated user's permissions and data ownership.

### 10.3 RAG

RAG will support document ingestion, chunking, embedding generation, vector storage, retrieval, and grounded answer generation.

### 10.4 AI Agents

LangGraph may orchestrate stateful workflows and multi-step tool execution.

### 10.5 Safety Requirements

- Enforce user-level access controls.
- Validate tool inputs and outputs.
- Restrict tools to approved operations.
- Do not permit autonomous real-money trading.
- Clearly identify uncertainty and data freshness.
- Preserve source references for retrieved information where available.
- Prevent AI tools from accessing data outside the user's authorization scope.
- Prevent AI agents from bypassing backend role authorization.

## 11. Testing Requirements

### 11.1 Unit Testing

- Service logic.
- Financial calculations.
- Validation rules.
- Security utilities.
- Role authorization logic.

### 11.2 Integration Testing

- Database operations.
- API endpoints.
- Authentication flows.
- Transaction workflows.
- Role-based access control.
- Portfolio ownership enforcement.

### 11.3 API Testing

- Request validation.
- Response schemas.
- Error handling.
- Authorization.
- ADMIN versus USER access.
- Unauthorized requests.
- Cross-user resource access.

### 11.4 RBAC Test Scenarios

| Scenario | Expected Result |
|---|---|
| Register a new account | Role assigned as USER |
| Attempt to register with ADMIN role | Must not grant ADMIN access |
| ADMIN creates an asset | Allowed |
| USER creates an asset | 403 Forbidden |
| ADMIN updates an asset | Allowed |
| USER updates an asset | 403 Forbidden |
| ADMIN deactivates an asset | Allowed |
| USER deactivates an asset | 403 Forbidden |
| ADMIN accesses portfolio APIs | 403 Forbidden |
| USER accesses own portfolio | Allowed |
| USER accesses another user's portfolio | 404 Not Found |
| Unauthenticated request to protected endpoint | 401 Unauthorized |

### 11.5 AI Testing

- Retrieval relevance.
- Grounded responses.
- Tool execution validation.
- Access-control enforcement.
- Hallucination and failure scenarios.

Pytest will be used for backend testing.

## 12. Security Requirements

- Environment-based secrets.
- Secure password hashing.
- JWT validation.
- Authorization at resource level.
- Role-based API access control.
- Input validation.
- Database transaction management.
- No sensitive data in logs.
- Dependency management and vulnerability reviews.
- Appropriate CORS configuration.
- Rate limiting for sensitive endpoints before production.
- Protection against unauthorized role assignment.
- Ownership validation for user-owned resources.
- Administrative provisioning through a controlled process.

## 13. Development and Deployment

Development will initially use local environments.

The backend will run using Uvicorn.

The frontend will run using the Next.js development server.

PostgreSQL will provide local persistence.

Docker-based deployment will be introduced after the core application structure stabilizes.

Database schema changes must be managed through Alembic migrations.

## 14. Technical Constraints

- The initial product is paper trading only.
- Third-party market data may have rate limits and availability constraints.
- LLM services may introduce latency and usage costs.
- Local LLM performance depends on available hardware.
- AI features must not compromise financial data correctness.
- The initial authorization model supports ADMIN and USER roles.
- ADMIN and USER responsibilities are strictly separated.
- Public registration cannot create administrative accounts.
- Future role expansion must preserve existing authorization boundaries.

## 15. Technical Implementation Phases

1. Backend foundation and authentication.
2. Database design and portfolio APIs.
3. Asset management and RBAC.
4. Paper-trading engine.
5. Market-data integration.
6. Portfolio analytics.
7. AI provider abstraction.
8. AI assistant and RAG.
9. AI agent workflows.
10. Testing, optimization, and deployment.

## 16. Implementation Status

The following reflects the development progress established during the current implementation workflow.

| Component | Status |
|---|---|
| FastAPI backend foundation | Implemented |
| JWT authentication | Implemented |
| Argon2 password hashing | Implemented |
| User database model | Implemented |
| Portfolio database model and migration | Implemented |
| Portfolio CRUD APIs | Implemented and tested |
| Portfolio ownership validation | Implemented and tested |
| Asset database model and migration | Implemented |
| Asset schemas and service layer | Implemented |
| RBAC role column and migration | Implemented |
| Centralized UserRole enum | Implemented |
| Manual initial admin provisioning | Performed |
| Reusable role authorization dependency | Implemented |
| Complete ADMIN/USER API permission testing | Pending confirmation |
| Paper-trading engine | Planned |
| Market-data integration | Planned |
| Portfolio analytics | Planned |
| AI assistant and RAG | Planned |
| AI agent workflows | Planned |

Implementation status must be updated as features are completed and verified.

---

**Document Owner:** TradePulse Development  
**Last Updated:** 2026-11-13