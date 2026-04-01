# Project Constitution: Personal Finance API

## 1. Core Principles

### 1.1 Inmutable Implementation
All core features and architectural decisions defined in the specification (`spec.md`) and plan (`plan.md`) are mandatory. Any deviation must be explicitly justified and approved.

### 1.2 Performance First
- **Async mandatory**: All I/O operations (database, cache, file system) **MUST** be implemented using `async/await`.
- **Optimization**: No "N+1" queries. Use `selectinload` or `joinedload` for relationship loading.
- **Caching**: The `ReportService` **MUST** utilize Redis for caching to avoid redundant heavy aggregations.

### 1.3 Strict Financial Accuracy
- **No Floating Point**: Never use `float` for monetary values. Always use `Decimal` (Python) and `NUMERIC(12, 2)` (PostgreSQL).
- **Rounding**: Rounding (if necessary) must follow the "banker's rounding" (round to nearest even) or a consistent business-defined rounding strategy to prevent sum errors.

### 1.4 Architectural Integrity (Hexagonal)
- **Domain Isolation**: Core logic in `domain/` must have **ZERO** dependencies on `infrastructure/` or `web/`. It should only interact with ports (interfaces).
- **Dependency Inversion**: Use interfaces in the domain that infrastructure adapters must implement.
- **Single Source of Truth**: Business rules must live exclusively in the Application layer (Use Cases) and Domain entities.

---

## 2. Security Standards

### 2.1 Zero-Knowledge Architecture
- **Salted Hashing**: passwords must be hashed using `bcrypt` via Passlib.
- **No sensitive exposure**: Under no circumstances shall `hashed_password` or internal system secrets be returned to the client or logged in plain text.

### 2.2 Granular Authorization
- **Strict Ownership**: Every service method and API endpoint **MUST** verify that the authenticated user owns the resource they are attempting to access.
- **Fail Closed**: If ownership cannot be verified, the application must default to a `403 Forbidden` or `404 Not Found`.

### 2.3 JWT Lifecycle
- **Access/Refresh Rotation**: Always use short-lived access tokens (30min) and require a secondary refresh token for renewal.
- **Statelessness**: The API must remain stateless. Do not rely on server-side session cookies.

---

## 3. Coding Style & Conventions

### 3.1 Naming
- **Database Tables**: `snake_case`, pluralized (e.g., `transactions`).
- **SQLAlchemy Models**: `PascalCase`, singular (e.g., `Transaction`).
- **Pydantic Schemas**: `PascalCase` with role suffixes (`TransactionCreate`, `TransactionResponse`).
- **API Endpoints**: `kebab-case` (e.g., `/api/v1/budget-alerts`).
- **Environment Variables**: `SCREAMING_SNAKE_CASE`.

### 3.2 FastAPI Best Practices
- **Type Hinting**: All parameters and return types must be explicitly typed.
- **Dependency Injection**: Use `Depends` for all service/repository injection at the router level.
- **DTOs mandatory**: Every endpoint **MUST** return a Pydantic schema (Response Model). Database entities should never be exposed directly in responses.

### 3.3 Error Handling
- **Consistent Response**: All errors must return a JSON object with a `detail` message: `{"detail": "Error message"}`.
- **Validation**: Use Pydantic's built-in validation (e.g., `min_length`, `max_length`, `le`, `ge`).
- **Domain Exception Handling**: Raise `DomainException` in business logic (Application Layer). In `main.py`, these MUST be globally handled and mapped to `HTTP 400` or higher to protect internal stack traces.
- **Entity Identification**: Use `EntityNotFoundException` (mapped to `HTTP 404`) when a resource is missing.

---

## 4. Responsibility & Maintenance

### 4.1 Documentation
- **API Doc**: All endpoints must be decorated with relevant tags and summary descriptions for Swagger clarity.
- **Task Tracking**: Every time changes are applied, the associated tasks in `tasks.md` MUST be checked and marked as completed.
- **Changelog**: All major task completions should be documented or reflected in the `tasks.md` progress.

### 4.2 Testing Integrity
- **Mandatory Suite**: No feature is considered "Done" until it has associated integration tests in `/tests`.
- **Coverage**: Maintain a minimum of 80% code coverage. Critical modules (Auth, Finance calculations) must strive for 100%.
