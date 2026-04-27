# Deduckly

Deduckly  is a mobile-first application designed to help gig economy workers track mileage, expenses, and tax deductions.

Drivers working with platforms like DoorDash, Uber, Lyft, Instacart, and Spark often struggle to keep accurate records for tax deductions. Deduckly simplifies this process by providing automated mileage tracking, receipt scanning, and real-time financial insights.

The goal of Deduckly  is to remove the complexity of bookkeeping for independent contractors while helping users maximize their tax deductions.

---

# Core Features

### Mileage Tracking

Drivers can start and stop trip tracking directly from the mobile app. GPS tracking calculates miles driven and logs trips for tax deduction purposes.

### Expense Tracking

Users can add and categorize expenses such as fuel, maintenance, supplies, parking, and other deductible costs.

### Receipt Scanning

Receipts can be scanned using the mobile camera. The system extracts key data such as vendor, total, and date.

### Financial Dashboard

Users can quickly view:

* Total miles driven
* Total income
* Total expenses
* Estimated deductions
* Estimated tax liability

### Tax Estimation

Deduckly  provides a running estimate of taxes owed based on recorded income, mileage deductions, and expenses.

### Subscription Model

Deduckly  operates using a freemium model.

**Free Tier**

* Basic mileage tracking
* Manual expense tracking
* Limited receipt scans
* Basic financial dashboard

**Premium**

* Unlimited mileage tracking
* Unlimited receipt scanning
* Automatic expense categorization
* Advanced tax estimation
* Exportable tax reports

Premium subscriptions are managed through **Apple In-App Purchases (StoreKit)**.

---

# Security

Deduckly  includes secure authentication and optional Two-Factor Authentication (2FA).

Supported authentication methods:

* Email and password login
* OAuth providers
* Time-based One-Time Password (TOTP) 2FA

Security features include:

* JWT authentication
* OAuth login support
* TOTP-based two-factor authentication
* Secure password hashing
* Encrypted API communication

---

# Tech Stack

### Backend

* FastAPI
* PostgreSQL
* SQLAlchemy
* Alembic migrations
* Redis (background jobs)

### Mobile App

* React Native
* Expo

### Cloud Infrastructure

* AWS / GCP compatible deployment
* Object storage for receipt uploads

### Payments

* Apple In-App Purchases (StoreKit)

---

# Architecture

Deduckly  uses a client-server architecture.

The mobile application acts as a client that communicates with a centralized API built with FastAPI.

This architecture allows the backend to support additional clients in the future, such as:

* Web dashboards
* Admin analytics tools
* Third-party integrations

---

# Roadmap

## Phase 1 – Planning

* Define product requirements
* Design database schema
* Define API structure
* Setup project repositories

## Phase 2 – Backend Foundation

* Setup FastAPI project
* Implement authentication system
* Create core database models
* Build API endpoints

## Phase 3 – Mobile App

* Create React Native app
* Implement login and onboarding
* Build dashboard UI
* Implement trip tracking

## Phase 4 – Expense & Receipt System

* Add expense management
* Implement receipt scanning
* Integrate OCR for receipt parsing

## Phase 5 – Subscription System

* Configure Apple In-App Purchases
* Implement free vs premium feature access
* Validate purchases with backend

## Phase 6 – Security

* Add Two-Factor Authentication
* Improve API security
* Rate limiting and monitoring

## Phase 7 – Background Mileage Tracking

* Automatic trip detection
* Background GPS tracking

## Phase 8 – Reports & Exports

* Tax summary reports
* CSV export
* CPA-ready reports

## Phase 9 – Testing

* Backend unit tests
* API integration tests
* Mobile testing

## Phase 10 – Beta Release

* TestFlight beta
* Early user feedback
* Bug fixes and performance improvements

## Phase 11 – Launch

* Public App Store release
* Initial marketing push
* User acquisition

---

# Target Users

Deduckly  is designed for independent workers including:

* DoorDash drivers
* Uber and Lyft drivers
* Instacart shoppers
* Spark drivers
* Freelancers and independent contractors

---

# Long-Term Vision

Future versions of Deduckly  may include:

* Automated income imports from gig platforms
* AI-powered expense categorization
* CPA-ready tax reporting
* Web dashboard access
* Accounting software integrations

---

# License

MIT License
