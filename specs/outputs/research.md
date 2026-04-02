# Research Findings

This file contains documentations of findings regarding existing patterns and architectures in the codebase.

## Codebase Patterns
- **Hexagonal Architecture**: The project follows a hexagonal structure with `domain`, `application`, `infrastructure`, and `web` directories.
- **Async Implementation**: The use of `async/await` is mandatory for all I/O operations.
- **SQLAlchemy 2.0**: The ORM uses async sessions and modern mapping patterns.

## Infrastructure Patterns
- **PostgreSQL**: Used for primary data storage with `NUMERIC(12, 2)` for financials.
- **Redis**: Used for reporting summaries caching.
- **APScheduler**: Used for daily budget checking jobs.

## Phase 2: Implementation Details
- **User Entity**: Implemented in `app/domain/entities/user.py` with fields: email, hashed_password, full_name, currency (3-char), and is_active.
- **Security Context**: `app/core/security.py` provides Bcrypt hashing and JWT (HS256) token generation/decoding.
- **Dependency Flow**: The `AuthRouter` depends on `AuthUseCase`, which depends on `UserRepository`. The `SQLAlchemyUserRepository` implementation handles the actual DB interaction.

## Phase 3: Implementation Details
- **Category Entity**: Implemented in `app/domain/entities/category.py` with fields: name, type (income/expense), icon, color, is_default, and user_id (optional).
- **Tag Entity**: Implemented in `app/domain/entities/tag.py` with fields: name, color, and user_id (owned by user).
- **User Preference**: `app/domain/entities/user_category_preference.py` manages the per-user enabled/disabled status of system-wide default categories.
- **Category Seeding**: `CategoryUseCase` includes logic to seed 15+ standard financial categories (Food, Salary, etc.) if they don't already exist.
- **API Coverage**: Full CRUD for Tags and Categories, plus a `/toggle-default` endpoint for managing system category visibility.