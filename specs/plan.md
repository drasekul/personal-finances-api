# Technical Plan: Personal Finance API

## Tech Stack

| Layer | Technology | Details |
|---|---|---|
| **Language** | Python 3.12+ | Core language for the backend. |
| **Framework** | FastAPI | Main web framework for high performance. |
| **ORM** | SQLAlchemy 2.0+ | Asynchronous database communication. |
| **Database** | PostgreSQL 15+ | Primary relational database for persistence. |
| **Migration** | Alembic | Version control for database schema changes. |
| **Caching** | Redis 7+ | caching layer for reports and API response performance. |
| **Validation** | Pydantic v2 | Schema definition and data validation. |
| **Security** | passlib + bcrypt / python-jose | Password hashing (bcrypt) and JWT (HS256) management. |
| **Task Queue** | APScheduler | Background jobs for budget threshold checking. |
| **Containerization** | Docker / Docker Compose | reproducible development and deployment environment. |
| **Testing** | Pytest / Pytest-asyncio | Automation testing suite. |

---

## Data Models

### 1. User
- `id`: UUID (Primary Key)
- `email`: String (Unique, Index)
- `hashed_password`: String (Bcrypt)
- `full_name`: String
- `currency`: String (3 chars, e.g., "USD")
- `is_active`: Boolean (Default: True)
- `timestamps`: `created_at`, `updated_at` (Auto-managed)

### 2. Category
- `id`: UUID (Primary Key)
- `user_id`: UUID (ForeignKey to User)
- `name`: String (Name of the category)
- `type`: Enum ("income", "expense")
- `color`: String (Hex color for UI)
- `icon`: String (Icon identifier)
- `is_default`: Boolean (Flag for system-wide defaults)
- **Constraint**: Unique combination of `(user_id, name)`

### 3. Transaction
- `id`: UUID (Primary Key)
- `user_id`: UUID (ForeignKey to User, Indexed)
- `category_id`: UUID (ForeignKey to Category)
- `amount`: Numeric(12, 2)
- `type`: Enum ("income", "expense")
- `description`: String (Optional)
- `date`: Date (Indexed)
- `recurrence`: Enum ("none", "daily", "weekly", "monthly", "yearly")
- `notes`: Text (Optional)
- **Tags**: Many-to-Many relationship via `transaction_tags` table.

### 4. Tag
- `id`: UUID (Primary Key)
- `user_id`: UUID (ForeignKey to User)
- `name`: String
- **Constraint**: Unique combination of `(user_id, name)`

### 5. Budget
- `id`: UUID (Primary Key)
- `user_id`: UUID (ForeignKey to User, Indexed)
- `category_id`: UUID (ForeignKey to Category)
- `amount_limit`: Numeric(12, 2)
- `period`: Enum ("monthly", "annual")
- `month`: Integer (1-12, nullable for annual)
- `year`: Integer
- `alert_threshold`: Integer (Percentage, e.g., 80)
- `alert_sent`: Boolean (Avoid duplicate notifications)
- **Constraint**: Unique combination of `(user_id, category_id, month, year)`

### 6. BudgetAlert
- `id`: UUID (Primary Key)
- `user_id`: UUID (ForeignKey to User, Indexed)
- `budget_id`: UUID (ForeignKey to Budget)
- `message`: String
- `alert_type`: Enum ("warning", "exceeded")
- `is_read`: Boolean (Default: False)
- `read_at`: Timestamp (Nullable)

---

## App Architecture (Hexagonal / Ports and Adapters)

The application follows a **Hexagonal Architecture** (also known as Ports and Adapters) to ensure that the core business logic (Domain) remains decoupled from external technologies (Infrastructure).

### 1. Domain Layer (The Core)
- **Entities**: Pure logic and database models representing business objects.
- **Ports (Interfaces)**: Abstract definitions of what the application needs (e.g., `UserRepository`, `EmailService`).
- **Exceptions**: Domain-specific errors.

### 2. Application Layer (Use Cases)
- **Services/Use Cases**: Orchestrate flow between entities and ports. This layer contains the "How" of the business processes.

### 3. Infrastructure Layer (Adapters)
- **Data Adapters**: Concrete implementations of Domain ports (e.g., `SQLAlchemyUserRepository`).
- **External Adapters**: Clients for third-party services (Redis, AWS S3, etc.).
- **Database**: Session management and migrations.

### 4. Web Layer (Adapters)
- **FastAPI Core**: Routers, dependencies, and middlewares.
- **DTOs (Schemas)**: Pydantic models for request/response validation.

---

## Project Structure

```
app/
├── domain/               # Core business logic
│   ├── entities/         # SQLAlchemy Models (Domain representation)
│   │   ├── __init__.py   # Model registrar for Alembic
│   │   ├── base.py       # BaseEntity with UUID and timestamps
│   │   └── user.py       # User entity
│   ├── ports/            # Abstract Repository/Service interfaces
│   │   └── user_repository.py
│   └── exceptions.py     # Domain-specific exceptions
├── application/          # Use cases & coordination
│   └── use_cases/        # Service logic implementation
│       └── auth.py       # Registration, Login, and Rotation logic
├── infrastructure/       # External tool implementations (Adapters)
│   ├── adapters/         # Implementation of domain ports
│   │   ├── postgres/     # SQLAlchemy repository implementations
│   │   │   └── user_repository.py
│   │   └── redis/        # Caching implementations
│   └── database.py       # Engine and Session setup
├── web/                  # API Layer (FastAPI Adapters)
│   ├── api/              # API Route definitions
│   │   └── v1/           # Versioned API routes (e.g., auth.py)
│   ├── schemas/          # Pydantic DTOs (user.py, auth.py)
│   └── dependencies/     # FastAPI Dependency Injection (auth.py)
├── core/                 # Shared configuration
│   ├── config.py         # App settings (Pydantic Settings)
│   └── security.py       # Passlib and JWT utilities
└── main.py              # Application entry point & router registration
```

---

## FastAPI Best Practices

1.  **Type Hinting Everywhere**: Use Python type hints for all parameters and return types to enable better IDE support and Pydantic validation.
2.  **Dependency Injection (DI)**: Leverage FastAPI's `Depends` for managing database sessions, authentication, and service injection. This facilitates testing through overrides.
3.  **DTOs for Everything**: Never return a database model directly. Always use Pydantic `Response` schemas to filter sensitive data and ensure contract stability.
4.  **Async/Await first**: Strictly use asynchronous libraries and drivers (`asyncpg`, `httpx`) to maintain high concurrency performance.
5.  **Global Exception Handling**: Use `exception_handlers` in the FastAPI app to map domain exceptions to appropriate HTTP status codes.
6.  **Environment Isolation**: Use `pydantic-settings` to manage configuration via `.env` files, ensuring no secrets are hardcoded.
7.  **Pydantic V2**: Utilize the performance and feature improvements of Pydantic V2 for schema validation.
8.  **Automatic Documentation**: Keep `tags`, `summary`, and `description` updated in routers to produce high-quality Swagger/OpenAPI docs.
