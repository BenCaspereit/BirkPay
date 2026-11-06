# BirkPay – Backend Structure

## Directory Tree

```text
Backend/
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── deps.py
│   │   └── v1/
│   │       ├── users.py
│   │       ├── products.py
│   │       └── transactions.py
│   ├── db/
│   │   ├── session.py
│   │   └── init_db.py
│   ├── models/
│   │   ├── user.py
│   │   ├── product.py
│   │   └── transaction.py
│   ├── schemas/
│   │   ├── user.py
│   │   ├── product.py
│   │   └── checkout.py
│   └── services/
│       ├── checkout_integration.py
│       ├── checkout_operations.py
│       ├── checkout.py
│       ├── nfc.py
│       ├── nfc_integration.py
│       └── nfc_operations.py
├── tests/
│   ├── api/
│   │   ├── test_products.py
│   │   ├── test_transactions.py
│   │   └── test_users.py
│   ├── services/
│   │   ├── test_checkout.py
│   │   └── test_nfc.py
│   ├── conftest.py
│   └── test_checkout_operations.py
├── requirements.txt
└── README_BACKEND.md
```

## Architecture and Responsibilities

The backend is a layered FastAPI monolith, but it does not consistently follow a Controller-Service-Repository pattern:

| Layer | Implementation | Responsibility |
|---|---|---|
| HTTP/API | `app/api/v1/*.py` | FastAPI routes, status codes, Pydantic request/response models; many CRUD handlers query SQLAlchemy directly |
| Dependencies | `app/api/deps.py` | Database session, NFC-header identity, and role checks |
| Services | `app/services/` | NFC and checkout logic; the checkout service orchestrates database access and operations functions |
| Persistence | `app/models/`, `app/db/` | SQLAlchemy tables, engine, and session lifecycle |
| DTOs/validation | `app/schemas/` | Pydantic validation and API representations |
| Tests | `tests/` | API, service, and operations tests; fixtures override the DB dependency and use in-memory SQLite |

There is no separate repository layer. `products.py` and `users.py` perform most queries and updates directly. `transactions.py` delegates checkout to `CheckoutService` in `checkout_integration.py`.

### Services Actually Wired to Routes

- User NFC lookup and card assignment use `NFCService` from `nfc.py`.
- Checkout uses `CheckoutService` from `checkout_integration.py` and helper functions from `checkout_operations.py`.
- `checkout.py` and `nfc_integration.py` contain alternative/older implementations, but current API routers do not import them.

Before changing a service, check the route imports: service classes with similar names in parallel files are not necessarily on the active request path.

## Request Data Flow

1. `app/main.py` creates the FastAPI app, configures CORS, and mounts the three routers under `/api/v1`.
2. FastAPI validates path, query, and JSON data using type annotations and Pydantic schemas.
3. `Depends(get_db)` opens a SQLAlchemy session for each request and closes it afterward.
4. Protected endpoints resolve `RoleChecker`. It reads `X-NFC-Key`, looks up `User.nfc_uid`, and compares `user.role` to the allowed role list.
5. The route or service reads or updates SQLAlchemy models. Checkout loads the user with `with_for_update()`, sums active product prices in cents, checks the balance, debits the account, and creates a `PURCHASE` transaction.
6. Changes are persisted with `commit()`; response models serialize ORM data.

`main.py` calls `init_db()` at application startup, creating known tables with `Base.metadata.create_all()`. `seed_demo_data()` is defined separately and runs when the module is invoked directly, not during normal FastAPI startup.

## Persistence Model

| Table | Main fields | Purpose |
|---|---|---|
| `users` | `id`, `school_id`, `nfc_uid`, `name`, `balance_cents`, `role`, `created_at` | Accounts and NFC assignment |
| `products` | `id`, `school_id`, `name`, `price_cents`, `is_active`, `created_at` | Products for sale; API deletion deactivates rather than physically deleting |
| `transactions` | `id`, `school_id`, `user_id`, `amount_cents`, `type`, `created_by_user_id`, `created_at` | Deposit and purchase history |

Money is stored as integer cents. `transactions.user_id` and `created_by_user_id` reference `users.id`. ORM models use SQLAlchemy `Column` declarations; no migration tool is listed in the dependencies.

## Runtime and Dependencies

- FastAPI ≥ 0.110, Uvicorn, SQLAlchemy ≥ 2, Pydantic ≥ 2, `pydantic-settings`, `python-dotenv`, `psycopg2-binary`.
- `app/db/session.py` reads `DATABASE_URL` from the environment after `load_dotenv()` and creates the engine at import time. PostgreSQL is supported via the driver; test fixtures use `sqlite:///:memory:`.
- Local entry point in `main.py`: Uvicorn on `0.0.0.0:8000`; OpenAPI/Swagger at `/docs`, ReDoc at `/redoc`.
- CORS in `main.py` allows `allow_origins=["*"]`, all methods, and all headers.

## REST Interfaces

All business routes use the `/api/v1` prefix. For role-protected operations, `X-NFC-Key` is interpreted as the NFC UID of the calling user.

| Method and path | Purpose | Access declared by route |
|---|---|---|
| `GET /` | Health status | Public |
| `GET /api/v1/users/` | List users (`skip`, `limit`) | Public |
| `GET /api/v1/users/by-nfc/{nfc_uid}` | Look up a user by card UID | Public |
| `POST /api/v1/users/` | Create a user | `admin` |
| `POST /api/v1/users/{user_id}/deposit?amount_cents=…` | Add funds and create a `DEPOSIT` transaction | `admin`, `cashier` |
| `PUT /api/v1/users/{user_id}/nfc?nfc_uid=…` | Assign an NFC card | `admin`, `cashier` |
| `GET /api/v1/products/` | List products (`only_active`, defaults to `true`) | Public |
| `GET /api/v1/products/{product_id}` | Get product details | Public |
| `POST /api/v1/products/` | Create a product | `admin` |
| `PUT /api/v1/products/{product_id}` | Update product fields | `admin` |
| `DELETE /api/v1/products/{product_id}` | Deactivate a product | `admin` |
| `POST /api/v1/transactions/checkout` | Checkout with `nfc_uid`, `items`, and optional `cashier_user_id` | `cashier`, `admin` |
| `GET /api/v1/transactions/user/{user_id}?limit=…` | Transaction history (limit 1–100, default 20) | Public |

Checkout request items contain `product_id` and `quantity > 0`. The response and transaction history use Pydantic schemas from `schemas/checkout.py`.

## Conventions and Change Notes

- Python: `snake_case` for functions/variables, `PascalCase` for classes/schemas; project conventions specify Ruff for linting, formatting, and import sorting.
- Add request/response formats in `schemas/`, persistence fields in `models/`; when adding endpoints, observe the router prefix and `main.py` registration.
- Use integer cents rather than `float` for monetary values; balance updates require an appropriate database transaction.
- NFC UID is also used as the identifier in the `X-NFC-Key` authentication mechanism; current authentication is not token- or password-based.
- `README_BACKEND.md` contains planned or differing structure descriptions. Route imports and source code take precedence for actual wiring.
