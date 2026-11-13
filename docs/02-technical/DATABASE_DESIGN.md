# TradePulse – Database Design

**Version:** 1.0  
**Status:** Initial Design  
**Database:** PostgreSQL 17  
**ORM:** SQLAlchemy 2.0  
**Migration Tool:** Alembic

---

## 1. Database Overview

PostgreSQL is the primary relational database for TradePulse.

SQLAlchemy ORM 2.0 will be used to define entities, relationships, and database operations. Alembic will manage schema migrations.

The database must support:

- User accounts and authentication.
- Multiple portfolios per user.
- Supported investment assets.
- Simulated buy and sell transactions.
- Portfolio holdings and cash balances.
- Historical market prices.
- Portfolio analytics.
- Future AI research and assistant functionality.

## 2. Database Design Principles

1. Use normalized relational structures where appropriate.
2. Use primary keys for entity identification.
3. Use foreign keys to maintain referential integrity.
4. Enforce unique constraints for business-critical fields.
5. Use `NUMERIC` for monetary values and quantities.
6. Use timezone-aware timestamps.
7. Maintain an auditable transaction history.
8. Associate private financial records with their owners.
9. Use database migrations for schema changes.
10. Avoid storing redundant calculated values unless there is a clear performance requirement.

## 3. Entity Relationship Overview

The initial database will contain the following core entities:

- users
- portfolios
- assets
- transactions
- holdings
- market_prices

### Entity Relationships

```mermaid
erDiagram
    USERS ||--o{ PORTFOLIOS : owns
    PORTFOLIOS ||--o{ TRANSACTIONS : contains
    ASSETS ||--o{ TRANSACTIONS : references
    PORTFOLIOS ||--o{ HOLDINGS : contains
    ASSETS ||--o{ HOLDINGS : represents
    ASSETS ||--o{ MARKET_PRICES : has

    USERS {
        int id PK
        varchar full_name
        varchar email UK
        varchar password_hash
        timestamptz created_at
    }

    PORTFOLIOS {
        int id PK
        int user_id FK
        varchar name
        text description
        varchar base_currency
        timestamptz created_at
        timestamptz updated_at
    }

    ASSETS {
        int id PK
        varchar symbol
        varchar name
        varchar asset_type
        varchar provider_asset_id
        varchar quote_currency
        boolean is_active
        timestamptz created_at
    }

    TRANSACTIONS {
        int id PK
        int portfolio_id FK
        int asset_id FK
        varchar transaction_type
        numeric quantity
        numeric unit_price
        numeric fees
        numeric total_amount
        varchar status
        timestamptz executed_at
        timestamptz created_at
    }

    HOLDINGS {
        int id PK
        int portfolio_id FK
        int asset_id FK
        numeric quantity
        numeric average_buy_price
        timestamptz updated_at
    }

    MARKET_PRICES {
        int id PK
        int asset_id FK
        numeric price
        varchar quote_currency
        varchar provider
        timestamptz price_timestamp
        timestamptz created_at
    }
```

## 4. Table Definitions

### 4.1 users

Stores user account information.

| Column | PostgreSQL Type | Constraints |
|---|---|---|
| id | INTEGER | Primary key |
| full_name | VARCHAR(100) | NOT NULL |
| email | VARCHAR(255) | NOT NULL, UNIQUE |
| password_hash | VARCHAR(255) | NOT NULL |
| created_at | TIMESTAMPTZ | NOT NULL, default NOW() |

Current implementation status: Implemented.

### 4.2 portfolios

Stores portfolios created by users.

| Column | PostgreSQL Type | Constraints |
|---|---|---|
| id | BIGINT | Primary key |
| user_id | INTEGER | Foreign key to users.id |
| name | VARCHAR(100) | NOT NULL |
| description | TEXT | Nullable |
| base_currency | VARCHAR(10) | NOT NULL |
| created_at | TIMESTAMPTZ | NOT NULL |
| updated_at | TIMESTAMPTZ | NOT NULL |

Business rules:

- A user can create multiple portfolios.
- Every portfolio belongs to exactly one user.
- A user cannot access another user's portfolio.
- Portfolio names should be validated.
- Base currency determines the currency used for portfolio-level reporting.

### 4.3 assets

Stores supported investment assets.

| Column | PostgreSQL Type | Constraints |
|---|---|---|
| id | BIGINT | Primary key |
| symbol | VARCHAR(30) | NOT NULL |
| name | VARCHAR(150) | NOT NULL |
| asset_type | VARCHAR(30) | NOT NULL |
| provider_asset_id | VARCHAR(150) | Nullable |
| quote_currency | VARCHAR(10) | NOT NULL |
| is_active | BOOLEAN | NOT NULL |
| created_at | TIMESTAMPTZ | NOT NULL |

Initial asset categories:

- CRYPTO
- STOCK
- ETF

Business rules:

- Symbols and provider identifiers must be handled according to the selected market-data provider.
- Asset records should not be deleted if referenced by historical transactions.
- Inactive assets must not be available for new transactions.

### 4.4 transactions

Stores simulated trading activity.

| Column | PostgreSQL Type | Constraints |
|---|---|---|
| id | BIGINT | Primary key |
| portfolio_id | BIGINT | Foreign key |
| asset_id | BIGINT | Foreign key |
| transaction_type | VARCHAR(10) | NOT NULL |
| quantity | NUMERIC(28,10) | NOT NULL |
| unit_price | NUMERIC(28,10) | NOT NULL |
| fees | NUMERIC(28,10) | NOT NULL |
| total_amount | NUMERIC(28,10) | NOT NULL |
| status | VARCHAR(20) | NOT NULL |
| executed_at | TIMESTAMPTZ | NOT NULL |
| created_at | TIMESTAMPTZ | NOT NULL |

Transaction types:

- BUY
- SELL

Initial status:

- EXECUTED

Additional statuses may be introduced if order simulation requires pending, rejected, or cancelled states.

Business rules:

- Quantity must be greater than zero.
- Unit price must be greater than zero.
- Fees must be non-negative.
- SELL quantity cannot exceed available holdings.
- BUY transactions must respect the available simulated cash balance.
- Every executed transaction must be recorded.
- Transaction records should be immutable through ordinary user operations.
- Duplicate requests must not create duplicate transactions.

The `total_amount` calculation must follow a documented convention. Initially:

BUY total = quantity × unit_price + fees

SELL proceeds = quantity × unit_price − fees

The system must retain enough information to reproduce transaction calculations.

### 4.5 holdings

Stores the current position of an asset in a portfolio.

| Column | PostgreSQL Type | Constraints |
|---|---|---|
| id | BIGINT | Primary key |
| portfolio_id | BIGINT | Foreign key |
| asset_id | BIGINT | Foreign key |
| quantity | NUMERIC(28,10) | NOT NULL |
| average_buy_price | NUMERIC(28,10) | NOT NULL |
| updated_at | TIMESTAMPTZ | NOT NULL |

Constraints:

- Unique combination of portfolio_id and asset_id.
- Quantity cannot be negative.
- Zero-quantity positions should be handled consistently.

Holdings are derived from executed transactions and maintained as a transactional position projection. Transaction history remains the source of truth.

Portfolio transactions and corresponding holdings updates must occur within a database transaction.

### 4.6 market_prices

Stores market price observations.

| Column | PostgreSQL Type | Constraints |
|---|---|---|
| id | BIGINT | Primary key |
| asset_id | BIGINT | Foreign key |
| price | NUMERIC(28,10) | NOT NULL |
| quote_currency | VARCHAR(10) | NOT NULL |
| provider | VARCHAR(100) | NOT NULL |
| price_timestamp | TIMESTAMPTZ | NOT NULL |
| created_at | TIMESTAMPTZ | NOT NULL |

Business rules:

- Price must be greater than zero.
- Provider information must be preserved.
- Price timestamps must be stored in UTC.
- Historical prices should not be overwritten by new observations.
- The application must identify stale or unavailable market prices.

## 5. Database Relationships

### User to Portfolio

One user can own multiple portfolios.

Relationship:

users.id → portfolios.user_id

### Portfolio to Transactions

One portfolio can contain multiple transactions.

Relationship:

portfolios.id → transactions.portfolio_id

### Asset to Transactions

One asset can appear in multiple transactions.

Relationship:

assets.id → transactions.asset_id

### Portfolio to Holdings

One portfolio can contain multiple asset holdings.

Relationship:

portfolios.id → holdings.portfolio_id

### Asset to Market Prices

One asset can have multiple historical price records.

Relationship:

assets.id → market_prices.asset_id

## 6. Financial Data Handling

Financial values must use Python `Decimal` and PostgreSQL `NUMERIC`.

Do not use binary floating-point values for authoritative monetary calculations.

The application must distinguish:

- Asset quantity.
- Unit price.
- Transaction fees.
- Transaction amount.
- Cash balance.
- Realized profit/loss.
- Unrealized profit/loss.
- Portfolio valuation.

Currency conversions must use explicit exchange-rate data and documented conversion timestamps.

## 7. Indexing Strategy

Initial indexes:

| Table | Index | Purpose |
|---|---|---|
| users | Unique email | User lookup |
| portfolios | user_id | Retrieve user portfolios |
| assets | symbol | Asset lookup |
| transactions | portfolio_id | Transaction history |
| transactions | asset_id | Asset transaction history |
| holdings | portfolio_id, asset_id | Unique portfolio position |
| market_prices | asset_id, price_timestamp | Historical price retrieval |

Indexes will be reviewed based on actual query patterns and performance measurements.

## 8. Data Integrity and Deletion

- User-owned data must be protected by authorization checks.
- Historical transactions should not be casually deleted.
- Referenced assets should generally be deactivated rather than removed.
- Portfolio deletion must follow a defined policy for associated transactions and holdings.
- Database constraints must enforce important integrity rules.

## 9. Future Database Extensions

Potential future entities:

- refresh_tokens
- portfolio_snapshots
- watchlists
- alerts
- price_alerts
- ai_conversations
- ai_messages
- documents
- document_chunks
- embeddings
- ai_tool_executions

These tables will be added only when their corresponding functionality is designed.

## 10. Migration Strategy

Alembic will manage all schema changes.

Rules:

1. Every schema change requires a migration.
2. Review autogenerated migrations before applying them.
3. Never modify an already-applied migration as a normal schema update.
4. Test migrations before production deployment.
5. Preserve data during schema evolution.

## 11. Current Implementation Status

Implemented:

- users table.
- SQLAlchemy ORM foundation.
- Alembic migration infrastructure.

Planned:

- portfolios.
- assets.
- transactions.
- holdings.
- market_prices.

---

**Document Owner:** TradePulse Development  
**Last Updated:** 2026-11-13