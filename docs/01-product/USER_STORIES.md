# TradePulse – User Stories

## 1. Purpose

This document describes the user stories for TradePulse, an AI-powered investment portfolio management and paper-trading platform.

The stories define user goals and expected platform capabilities. They will guide development and testing.

## 2. User Roles

### Registered User
A person who creates an account and uses TradePulse to manage portfolios, simulate trades, review investment performance, and access AI-powered insights.

### System
The platform responsible for authentication, portfolio calculations, market data processing, and AI-assisted analysis.

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

## 4. Portfolio Management

### US-005: Create Portfolio
As a user, I want to create multiple portfolios so that I can organize different investment strategies.

**Priority:** MVP

### US-006: View Portfolios
As a user, I want to view all my portfolios so that I can track my investments in one place.

**Priority:** MVP

### US-007: Update Portfolio
As a user, I want to update my portfolio name and description so that I can keep my portfolio information accurate.

**Priority:** MVP

### US-008: Delete Portfolio
As a user, I want to delete a portfolio so that I can remove portfolios I no longer need.

**Priority:** MVP

## 5. Asset Management

### US-009: Search Assets
As a user, I want to search for assets by symbol or name so that I can find the assets I want to track.

**Priority:** MVP

### US-010: View Asset Details
As a user, I want to view asset information such as symbol, name, and asset type so that I can identify an asset before trading.

**Priority:** MVP

### US-011: Support Multiple Asset Types
As a user, I want to manage supported asset types such as stocks and cryptocurrencies so that I can organize different investments.

**Priority:** MVP

## 6. Paper Trading

### US-012: Simulate Buy Transaction
As a user, I want to simulate buying an asset using virtual funds so that I can practice investment decisions without risking real money.

**Priority:** MVP

### US-013: Simulate Sell Transaction
As a user, I want to simulate selling assets from my holdings so that I can track the results of my investment decisions.

**Priority:** MVP

### US-014: View Transaction History
As a user, I want to view my completed buy and sell transactions so that I can review my trading activity.

**Priority:** MVP

### US-015: Prevent Invalid Trades
As a user, I want the platform to validate trade quantities and available holdings so that invalid transactions are prevented.

**Priority:** MVP

## 7. Holdings and Portfolio Analytics

### US-016: View Current Holdings
As a user, I want to see the assets I currently hold in each portfolio so that I can understand my investment positions.

**Priority:** MVP

### US-017: View Portfolio Value
As a user, I want to see the total value of my portfolio so that I can understand its current worth.

**Priority:** MVP

### US-018: View Profit and Loss
As a user, I want to view profit and loss for my holdings and portfolio so that I can evaluate investment performance.

**Priority:** MVP

### US-019: View Asset Allocation
As a user, I want to see how my portfolio is distributed across different assets so that I can understand my investment allocation.

**Priority:** MVP

## 8. Market Data

### US-020: View Latest Asset Prices
As a user, I want to view the latest available prices for supported assets so that I can make informed paper-trading decisions.

**Priority:** Post-MVP

### US-021: View Historical Prices
As a user, I want to view historical asset prices so that I can understand price movements over time.

**Priority:** Post-MVP

## 9. AI Investment Assistant

### US-022: Ask Investment Questions
As a user, I want to ask the AI assistant questions about my portfolio so that I can better understand my investment data.

**Priority:** Post-MVP

### US-023: Receive Portfolio Insights
As a user, I want AI-generated insights based on my portfolio data so that I can identify important trends and risks.

**Priority:** Post-MVP

### US-024: Understand Profit and Loss
As a user, I want the AI assistant to explain my portfolio's profit and loss so that I can understand the factors affecting performance.

**Priority:** Post-MVP

### US-025: Ask Questions About Investment Documents
As a user, I want to ask questions about uploaded investment documents and research so that I can retrieve relevant information.

**Priority:** Post-MVP

### US-026: Receive Explainable AI Responses
As a user, I want AI responses to distinguish verified portfolio data from AI-generated explanations so that I can understand the reliability of the information.

**Priority:** Post-MVP

## 10. Security and Reliability

### US-027: Protect User Data
As a user, I want my portfolio and transaction data accessible only to me so that my financial information remains private.

**Priority:** MVP

### US-028: Maintain Transaction Accuracy
As a user, I want every successful paper trade to update my holdings and transaction history consistently so that my portfolio data remains accurate.

**Priority:** MVP

### US-029: Handle System Errors
As a user, I want clear error messages when an operation fails so that I understand what happened and can take appropriate action.

**Priority:** MVP

## 11. Scope Notes

- MVP functionality will be implemented before advanced AI features.
- All trades are simulated using virtual funds.
- No real-money transactions or brokerage execution are included.
- Financial calculations must be performed by backend business logic, not generated by an LLM.
- AI insights must be based on available platform data and clearly communicate limitations.
- Post-MVP stories will be implemented after the core portfolio and paper-trading workflows are stable.