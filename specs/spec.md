# Application Specification: Personal Finance API

## Principal Objective
The primary objective of this project is to build a robust, secure, and performant REST API for personal finance management. The system will enable users to track their income and expenses, set monthly and annual budgets by category, and receive automated alerts when spending approaches or exceeds predefined limits. Additionally, users will have access to detailed financial reports and the ability to export their data.

---

## Use Cases

### 1. User Management & Authentication
- **Register**: Create a new account with email, password, full name, and preferred currency.
- **Login**: Securely authenticate using email and password to receive a JWT (Access + Refresh tokens).
- **Profile**: View and update user profile information (except email).
- **Refresh Token**: Obtain a new access token using a valid refresh token (token rotation).

### 2. Category Management
- **Default Categories**: Use system-provided categories (e.g., Food, Transport, Rent).
- **Custom Categories**: Create, update, and delete personalized categories for both income and expenses.
- **Categorization**: Ensure every transaction is linked to a valid category.

### 3. Transaction Tracking
- **Record Transactions**: Create, update, and delete income and expense records with date, amount, description, tags, and category.
- **Filtering & Search**: List and filter transactions by date range, type, category, tags, and amount.
- **Pagination**: Browse transaction history using cursor-based pagination for efficiency.

### 4. Tagging System
- **Custom Tags**: Create and manage tags to further organize transactions (e.g., #urgent, #vacation).
- **Multiple Tags**: Assign multiple tags to a single transaction.

### 5. Budgeting & Limits
- **Set Budgets**: Define spending limits by category for specific months or years.
- **Real-time Tracking**: Monitor budget progress automatically as transactions are recorded.
- **Budget status**: Visualize whether a budget is "OK", at a "Warning" level, or "Exceeded".

### 6. Automated Alerts
- **Threshold Warnings**: Receive system alerts when spending reaches a defined percentage (e.g., 80%) of a budget.
- **Limit Exceeded**: Receive alerts when a budget limit is reached or surpassed.
- **Manage Alerts**: List, read, and mark alerts as read/unread.

### 7. Financial Reporting & Analytics
- **Summary**: Monthly/Annual overview of total income, expenses, and net balance.
- **Breakdown**: Categorized spending analysis with percentages.
- **Trends**: Historical trend analysis (income vs. expenses) over the last 6-12 months.
- **Data Export**: Export transaction history in CSV or JSON formats for external use.

---

## Acceptance Criteria for High Quality

### 1. Reliability & Data Integrity
- **Precise Financials**: All monetary amounts must use the `NUMERIC(12, 2)` format in the database and `Decimal` in Pydantic/Python to avoid floating-point errors.
- **Atomic Operations**: Use database transactions and proper async handling to ensure no data loss or corruption.
- **Soft Deletes/Validations**: Prevent deletion of categories that have active transactions.

### 2. Performance
- **Async Architecture**: Fully asynchronous implementation using FastAPI and SQLAlchemy (asyncpg).
- **Caching**: Report endpoints must leverage Redis caching to minimize expensive database queries.
- **Efficient Pagination**: Large datasets must be handled via optimized cursor-based pagination.

### 3. Security
- **Stateless Auth**: Robust JWT implementation with short-lived access tokens and secure refresh token rotation.
- **Ownership Enforcement**: Every request must strictly validate that the user is the owner of the resource being accessed/modified.
- **Encrypted Secrets**: Passwords must be hashed using `bcrypt`. No sensitive data (e.g., hashed passwords, internal IDs) should ever be exposed in responses.

### 4. Maintainability & Standards
- **Testing**: Minimum global test coverage of 75%, with critical security and business logic modules at 80%+.
- **Clean Code**: Strict adherence to the project's Coding Constitution (naming conventions, folder structure, etc.).
- **Automatic Documentation**: Fully compliant OpenAPI (Swagger) documentation for all endpoints.
- **Dockerized**: The entire application and its dependencies (Postgres, Redis) must be deployable via Docker and Docker Compose.
