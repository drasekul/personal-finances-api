# Personal Finance API

A robust, secure, and performant REST API for managing personal finances, built with **FastAPI** and following **Spec-Driven Development (SDD)** and **Hexagonal Architecture** principles.

---

## 🚀 Overview

The **Personal Finance API** is designed to provide users with a complete toolkit for financial organization. It allows recording transactions, managing custom categories, setting spending limits with automated alerts, and generating insightful financial reports.

### Key Features
- **Stateless Auth**: Secure JWT-based authentication with Refresh Token rotation.
- **Hexagonal Architecture**: Core business logic strictly decoupled from infrastructure and external providers.
- **Budgeting & Alerts**: Monthly and annual budget tracking with automated threshold notifications via APScheduler.
- **Financial Analytics**: Monthly summaries, category-wise breakdowns, and spending trend analysis.
- **Redis Caching**: Optimized performance for expensive report aggregations.
- **Data Export**: Export transaction history in JSON or CSV formats.

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| **Framework** | [FastAPI](https://fastapi.tiangolo.com/) |
| **Database** | [PostgreSQL](https://www.postgresql.org/) + [SQLAlchemy 2.0](https://www.sqlalchemy.org/) (Async) |
| **Migrations** | [Alembic](https://alembic.sqlalchemy.org/) |
| **Caching** | [Redis](https://redis.io/) |
| **Validation** | [Pydantic V2](https://docs.pydantic.dev/) |
| **Jobs** | [APScheduler](https://apscheduler.readthedocs.io/) |
| **Container** | [Docker](https://www.docker.com/) + [Docker Compose](https://docs.docker.com/compose/) |

---

## 📐 Architecture & Standards

This project uses **Hexagonal Architecture (Ports and Adapters)** to maintain a clean separation of concerns:
- **`domain/`**: Entities and abstract ports (interfaces).
- **`application/`**: Use cases and business orchestration.
- **`infrastructure/`**: Concrete adapters for DB (Postgres) and Caching (Redis).
- **`web/`**: FastAPI routers and schemas.

### Coding Constitution
Strict adherence to project principles:
- **Async mandatory**: All I/O is asynchronous.
- **Financial Integrity**: Using `Decimal` and `NUMERIC(12, 2)` for zero floating-point errors.
- **DTOs Only**: Database models are never exposed directly to the client.

---

## 📄 Documentation (SDD)

This project is built using a **Specification-Driven Development** approach. All detailed documentation is located in the **[specs/](specs/)** directory:

1.  **[spec.md](specs/spec.md)**: Product objectives and detailed use cases.
2.  **[plan.md](specs/plan.md)**: Technical architecture, directory structure, and best practices.
3.  **[tasks.md](specs/tasks.md)**: Development roadmap and status tracking.
4.  **[constitution.md](specs/constitution.md)**: Immutable project principles and coding style.

---

## 🚦 Getting Started (Draft)

1.  Clone the repository.
2.  Setup environment variables (`.env`).
3.  Launch the services: `docker compose up -d`.
4.  Run migrations: `alembic upgrade head`.
5.  Access the API at `http://localhost:8000/docs`.
