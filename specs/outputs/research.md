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
