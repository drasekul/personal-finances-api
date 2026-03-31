# Development Findings & Reflections

This file contains reflections on what worked or failed during the development process to avoid repeating errors and improve future iterations.

## Reflections
- **SDD Integration**: The initial specification and implementation tracking has been initialized.
- **Constitution Rules**: New rules for task tracking have been added to ensure the AI agent remains synchronized with the project roadmap.

## Avoidance Log
- **Floating Point**: Never use `float` for money (already enforced by constitution).
- **N+1 Queries**: Always use `selectinload` or `joinedload`.
