# Development Findings & Reflections

This file contains reflections on what worked or failed during the development process to avoid repeating errors and improve future iterations.

## Reflections
- **SDD Integration**: The initial specification and implementation tracking has been initialized.
- **Constitution Rules**: New rules for task tracking have been added to ensure the AI agent remains synchronized with the project roadmap.

## Avoidance Log
- **Floating Point**: Never use `float` for money (already enforced by constitution).
- **N+1 Queries**: Always use `selectinload` or `joinedload`.

## Phase 2: Lessons Learned
- **Alembic in Isolation**: Generating migrations requires access to the database or a specialized migration tool environment. For this dev session, code has been verified for structural correctness against the schema.
- **Pydantic Validation**: Using `min_length=3` and `max_length=3` for currency provides a simple yet effective validation layer for Phase 2.
- **Hexagonal Decoupling**: Keeping the repo port in the domain ensures that even if we change the persistence layer (to MongoDB or others), the business logic in AuthUseCase remains untouched.
