# BirkPay – Project Structure

## Purpose and Architecture Boundary

BirkPay is a school payment system for balances, products, transactions, and planned NFC use. The codebase is split into a Python backend and a Nuxt frontend. The backend exposes a REST API; in the inspected state, the frontend is primarily a UI prototype and does not communicate with that API.

## Repository Overview

```text
Birkpay/
├── Backend/
│   ├── app/                  # FastAPI application; see 02-backend-structure.md
│   ├── tests/                # API, service, and operations tests
│   ├── requirements.txt      # Python dependencies
│   └── README_BACKEND.md     # Backend overview; partly outdated
├── Frontend/
│   ├── app/                  # Nuxt application; see 03-frontend-structure.md
│   ├── public/               # Static files served directly
│   ├── nuxt.config.ts        # Nuxt modules, CSS, and Vite configuration
│   └── package.json          # JavaScript dependencies and scripts
├── docs/
│   ├── assets/images/        # Screenshots for project and user documentation
│   ├── Admin Handbook.md
│   ├── Conventions.md        # Naming, formatting, and Git conventions
│   ├── Tech Overview.md      # Existing technical overview
│   ├── User Manuals.md
│   └── architecture/         # These architecture documents
├── Issues/                   # Project issues (contains subdirectories)
├── Template/                 # Project template (directory exists)
├── schema.drawio             # Database schema draft
├── ReadMe.md                 # Project purpose, architecture, and status
└── .gitignore                # Ignores environment files, caches, build output, etc.
```

`Backend/old/` contains legacy files and is excluded by `.gitignore`. `Backend/` also contains `api_keys.env`; environment files are ignored and should not be included in documentation or version control. No container or deployment manifests were found in the inspected project file list.

## Main Modules and Communication

| Module | Responsibility | Connection |
|---|---|---|
| `Frontend` | Nuxt/Vue interfaces for admin, POS, and banking | No backend HTTP requests were found in the current source |
| `Backend` | FastAPI endpoints, business logic, and SQLAlchemy access | Configurable database connection via `DATABASE_URL` |
| Database | Users, products, and transactions | SQLAlchemy models; application expects `DATABASE_URL`, tests use in-memory SQLite |
| NFC hardware | Project README describes ESP32/NFC as a planned extension | Communication method and end-to-end integration are not implemented in code |

The intended path is client → HTTP(S)/LAN → FastAPI → SQLAlchemy → database. Backend endpoints for users, products, and transactions exist, while the inspected frontend uses static or local sample data. The architecture description in the project README represents the target state, not an already working integration.

## Technology Stack (Code as Implemented)

| Area | Technologies |
|---|---|
| Backend | Python, FastAPI, Uvicorn, Pydantic 2, SQLAlchemy 2, `python-dotenv`, `psycopg2-binary` |
| Frontend | Nuxt 4, Vue 3, TypeScript (alongside Vue files without explicit TypeScript), Vue Router via Nuxt |
| UI/CSS | Nuxt UI, Nuxt Icon, Tailwind CSS 4, `@tailwindcss/vite`, PostCSS |
| Database | SQLAlchemy engine configured by `DATABASE_URL`; PostgreSQL driver dependency; in-memory SQLite for tests |
| Tests | pytest, FastAPI `TestClient`, SQLAlchemy test database |

`package.json` defines `dev`, `build`, `generate`, and `preview`; it contains neither Pinia nor an API client library. Nuxt generates page routes from `Frontend/app/pages/`. Backend and frontend dependencies are managed separately.

## Shared Data and Design Conventions

- The backend represents monetary values as integer cents (`balance_cents`, `price_cents`, `amount_cents`); checkout debits are stored as negative transaction amounts.
- Database/Python names generally use `snake_case`; Python classes and Vue components use `PascalCase`; frontend variables use `camelCase`.
- Core models include `school_id` (default `schule-1`) as a tenant field in preparation for multi-tenancy. Consistent tenant filtering is not apparent across all endpoints.
- The project uses a layered structure but has no repository layer: some API routes access SQLAlchemy directly.
- Detailed module and API information: [Backend Structure](./02-backend-structure.md) and [Frontend Structure](./03-frontend-structure.md).
