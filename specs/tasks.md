# Development Tasks: Personal Finance API

## Phase 1: Foundation & Setup
- [x] Initialize project structure following the **Hexagonal Architecture** directory tree.
- [x] Setup Pydantic configuration (`app/core/config.py`) for environment variables.
- [x] Configure SQLAlchemy async engine and base session management (`app/infrastructure/database.py`).
- [x] Setup Alembic for migrations, including the `env.py` async configuration.
- [x] Define base entities and common domain exceptions (`app/domain/entities/base.py`).
- [x] Configure Dockerfile and docker-compose.yml for local development.

## Phase 2: User Authentication & Security
- [ ] Implement `User` entity and initial migration.
- [ ] Create hashing and JWT utilities in `app/core/security.py`.
- [ ] Define `UserRepository` port and its Postgres adapter implementation.
- [ ] Build `AuthUseCase` in the application layer.
- [ ] Implement Web adapters: Auth schemas and FastAPI routers.
- [ ] Setup `get_current_user` dependency.

## Phase 3: Categories & Tagging
- [ ] Implement `Category` and `Tag` entities.
- [ ] Create repository ports and adapters for Category/Tag.
- [ ] Implement logic for seeding default categories in `CategoryUseCase`.
- [ ] Build CRUD Web adapters (schemas + routers) for categories and tags.

## Phase 4: Transaction Management
- [ ] Implement `Transaction` entity and tag association.
- [ ] Define `TransactionRepository` port and Postgres implementation (with filters).
- [ ] Build `TransactionUseCase` ensuring business rule: type matches category.
- [ ] Implement Transaction Web adapters (filtering, pagination, CRUD).

## Phase 5: Budgeting System
- [ ] Implement `Budget` and `BudgetAlert` entities.
- [ ] Create `BudgetRepository` and its adapter.
- [ ] Implement `BudgetUseCase` for real-time progress calculations.
- [ ] Build Budget Web adapters and enforce "expense-only" rules.

## Phase 6: Reporting & Analytics
- [ ] Implement Redis adapter in `app/infrastructure/adapters/redis`.
- [ ] Build `ReportUseCase` with caching logic.
- [ ] Implement specialized queries for summaries, category breakdowns, and trends.
- [ ] Develop data export adapters (CSV/JSON).
- [ ] Implement Report Web adapters.

## Phase 7: Background Alerts
- [ ] Implement `BudgetCheckerTask` as a background use case.
- [ ] Setup `APScheduler` in `app/main.py` to trigger the daily alert job.
- [ ] Build `AlertUseCase` for managing notification visibility.
- [ ] Implement Alert Web adapters for user interaction.

## Phase 8: Testing & Refinement
- [ ] Setup `pytest` with database and adapter mocks/fixtures.
- [ ] Write integration tests for Hexagonal layers (Web -> Application -> Port).
- [ ] Perform coverage analysis (target 75%+).
- [ ] Final documentation update and code cleanup.
