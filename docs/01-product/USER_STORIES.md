# TradePulse – User Stories

**Version:** 1.1  
**Status:** Updated  
**Last Updated:** 2026-11-13

---

## 1. Purpose

This document describes the user stories for TradePulse, an AI-powered investment portfolio management and paper-trading platform.

The stories define user goals and expected platform capabilities. They will guide development and testing.

## 2. User Roles

### 2.1 ADMIN

A platform administrator responsible for managing the supported asset catalog and future platform administration capabilities.

ADMIN permissions:
- View supported assets.
- Create new assets.
- Update existing asset information.
- Deactivate assets.
- Access future platform administration features.

ADMIN restrictions:
- Cannot create or manage investment portfolios.
- Cannot perform paper trades.
- Cannot access USER portfolio or investment data.

### 2.2 USER

A registered investment user who can manage personal portfolios, simulate trades, review investment performance, and access AI-powered insights.

USER permissions:
- View and search supported assets.
- Create and manage personal portfolios.
- Perform paper trades.
- Review holdings and portfolio performance.
- Access AI-powered investment insights when available.

USER restrictions:
- Cannot create assets.
- Cannot update asset information.
- Cannot deactivate assets.
- Cannot access another user's private portfolio or transaction data.

### 2.3 System

The platform responsible for authentication, authorization, portfolio calculations, market data processing, and AI-assisted analysis.

### 2.4 Role Assignment Rules

- Public registration always creates a USER account.
- Users cannot select or submit their role during registration.
- ADMIN accounts are provisioned manually.
- Role-based permissions are enforced by the backend.

---

## 3. Authentication and User Management

### US-001: User Registration

As a new user, I want to create an account using my name, email, and password so that I can access TradePulse.

**Priority:** MVP

### US-002: User Login

As a registered user, I want to log in using my email and password so that I can securely access my account.

**Priority:** MVP

### US-003: View My Profile

As a logged-in user, I want to view my profile information so that I can verify my account details.

**Priority:** MVP

### US-004: Secure Account Access

As a user, I want my account and personal data protected so that other users cannot access my information.

**Priority:** MVP

### US-030: Assign Default USER Role

As the system, I want every publicly registered account to receive the USER role automatically so that users cannot grant themselves administrative privileges.

**Priority:** MVP

### US-031: Restrict Role Assignment

As the system, I want to prevent users from assigning or changing their own role through public APIs so that role-based access remains secure.

**Priority:** MVP

### US-032: Enforce Role-Based Access

As the system, I want to enforce permissions based on the authenticated user's role so that ADMIN and USER responsibilities remain separate.

**Priority:** MVP

---

## 4. Portfolio Management

**Access:** USER only.

### US-005: Create Portfolio

As a USER, I want to create multiple portfolios so that I can organize different investment strategies.

**Priority:** MVP

### US-006: View Portfolios

As a USER, I want to view all my portfolios so that I can track my investments in one place.

**Priority:** MVP

### US-007: Update Portfolio

As a USER, I want to update my portfolio name and description so that I can keep my portfolio information accurate.

**Priority:** MVP

### US-008: Delete Portfolio

As a USER, I want to delete a portfolio so that I can remove portfolios I no longer need.

**Priority:** MVP

### US-033: Restrict Portfolio Access to USER

As the system, I want to allow only USER accounts to access portfolio management operations so that ADMIN accounts cannot perform investment activities.

**Priority:** MVP

### US-034: Enforce Portfolio Ownership

As a USER, I want to access and manage only my own portfolios so that another user cannot view or modify my portfolio data.

**Priority:** MVP

---

## 5. Asset Management

Asset information is shared across the platform.

Both ADMIN and USER accounts can view supported assets. Only ADMIN accounts can create, update, or deactivate assets.

### US-009: Search Assets

As a USER, I want to search for assets by symbol or name so that I can find the assets I want to track.

**Priority:** MVP

### US-010: View Asset Details

As a USER, I want to view asset information such as symbol, name, and asset type so that I can identify an asset before trading.

**Priority:** MVP

### US-011: Support Multiple Asset Types

As a USER, I want to manage supported asset types such as stocks and cryptocurrencies so that I can organize different investments.

**Priority:** MVP

### US-035: Create Assets

As an ADMIN, I want to create supported assets so that users can access new assets on the platform.

**Priority:** MVP

### US-036: Update Asset Information

As an ADMIN, I want to update existing asset information so that the asset catalog remains accurate.

**Priority:** MVP

### US-037: Deactivate Assets

As an ADMIN, I want to deactivate assets so that unavailable assets cannot be used for new investment activities.

**Priority:** MVP

### US-038: Restrict Asset Management

As the system, I want to restrict asset creation, updating, and deactivation to ADMIN accounts so that USER accounts cannot modify the shared asset catalog.

**Priority:** MVP

### US-039: Allow Shared Asset Visibility

As the system, I want both ADMIN and USER accounts to view supported assets so that asset information is consistently available across the platform.

**Priority:** MVP

---

## 6. Paper Trading

**Access:** USER only.

### US-012: Simulate Buy Transaction

As a USER, I want to simulate buying an asset using virtual funds so that I can practice investment decisions without risking real money.

**Priority:** MVP

### US-013: Simulate Sell Transaction

As a USER, I want to simulate selling assets from my holdings so that I can track the results of my investment decisions.

**Priority:** MVP

### US-014: View Transaction History

As a USER, I want to view my completed buy and sell transactions so that I can review my trading activity.

**Priority:** MVP

### US-015: Prevent Invalid Trades

As a USER, I want the platform to validate trade quantities and available holdings so that invalid transactions are prevented.

**Priority:** MVP

### US-040: Restrict Paper Trading to USER

As the system, I want to allow only USER accounts to perform paper-trading operations so that ADMIN accounts cannot execute investment transactions.

**Priority:** MVP

---

## 7. Holdings and Portfolio Analytics

**Access:** USER only.

### US-016: View Current Holdings

As a USER, I want to see the assets I currently hold in each portfolio so that I can understand my investment positions.

**Priority:** MVP

### US-017: View Portfolio Value

As a USER, I want to see the total value of my portfolio so that I can understand its current worth.

**Priority:** MVP

### US-018: View Profit and Loss

As a USER, I want to view profit and loss for my holdings and portfolio so that I can evaluate investment performance.

**Priority:** MVP

### US-019: View Asset Allocation

As a USER, I want to see how my portfolio is distributed across different assets so that I can understand my investment allocation.

**Priority:** MVP

---

## 8. Market Data

**Access:** USER-facing functionality.

### US-020: View Latest Asset Prices

As a USER, I want to view the latest available prices for supported assets so that I can make informed paper-trading decisions.

**Priority:** Post-MVP

### US-021: View Historical Prices

As a USER, I want to view historical asset prices so that I can understand price movements over time.

**Priority:** Post-MVP

---

## 9. AI Investment Assistant

**Access:** USER-facing functionality.

### US-022: Ask Investment Questions

As a USER, I want to ask the AI assistant questions about my portfolio so that I can better understand my investment data.

**Priority:** Post-MVP

### US-023: Receive Portfolio Insights

As a USER, I want AI-generated insights based on my portfolio data so that I can identify important trends and risks.

**Priority:** Post-MVP

### US-024: Understand Profit and Loss

As a USER, I want the AI assistant to explain my portfolio's profit and loss so that I can understand the factors affecting performance.

**Priority:** Post-MVP

### US-025: Ask Questions About Investment Documents

As a USER, I want to ask questions about uploaded investment documents and research so that I can retrieve relevant information.

**Priority:** Post-MVP

### US-026: Receive Explainable AI Responses

As a USER, I want AI responses to distinguish verified portfolio data from AI-generated explanations so that I can understand the reliability of the information.

**Priority:** Post-MVP

---

## 10. Security and Reliability

### US-027: Protect User Data

As a USER, I want my portfolio and transaction data accessible only to me so that my financial information remains private.

**Priority:** MVP

### US-028: Maintain Transaction Accuracy

As a USER, I want every successful paper trade to update my holdings and transaction history consistently so that my portfolio data remains accurate.

**Priority:** MVP

### US-029: Handle System Errors

As a user, I want clear error messages when an operation fails so that I understand what happened and can take appropriate action.

**Priority:** MVP

### US-041: Prevent Unauthorized Operations

As the system, I want to reject operations attempted by authenticated users who do not have the required role so that restricted functionality cannot be accessed.

**Priority:** MVP

### US-042: Protect Private Resource Access

As the system, I want to verify portfolio ownership before returning or modifying private portfolio resources so that users cannot access another user's data by changing resource identifiers.

**Priority:** MVP

---

## 11. Scope Notes

- MVP functionality will be implemented before advanced AI features.
- All trades are simulated using virtual funds.
- No real-money transactions or brokerage execution are included.
- Financial calculations must be performed by backend business logic, not generated by an LLM.
- AI insights must be based on available platform data and clearly communicate limitations.
- Post-MVP stories will be implemented after the core portfolio and paper-trading workflows are stable.
- ADMIN is responsible for asset catalog management and future platform administration.
- USER is responsible for personal portfolio management and investment activities.
- Both ADMIN and USER can view supported assets.
- Public registration always assigns the USER role.
- Backend authorization must enforce all role restrictions.
- ADMIN accounts cannot access portfolio management or paper-trading functionality.
- USER accounts cannot modify the shared asset catalog.