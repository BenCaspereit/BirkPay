# Project Code Conventions

## Across the Project
* Indentation: 4 Spaces (Python) / 2 oder 4 Spaces (Frontend via Prettier)

## Git Commit Prefixes
| Prefix      | Meaning / Area of Application                        | Example                                     |
| :---------- | :--------------------------------------------------- | :------------------------------------------ |
| `feat:`     | Feature – A new feature or function                  | `feat: add user authentication API`         |
| `fix:`      | Bug Fix – A bug has been fixed                       | `fix: resolve CORS error in backend`        |
| `refactor:` | Refactoring – Code restructured without logic change | `refactor: clean up legacy code with ruff`  |
| `docs:`     | Documentation – Changes to docs or comments          | `docs: add setup guide to README`           |
| `chore:`    | Routine task – Build system, .gitignore, packages    | `chore: update .gitignore and dependencies` |
| `style:`    | Style/Formatting – Purely cosmetic changes           | `style: fix indentations in CSS`            |
| `test:`     | Tests – Adding or revising tests                     | `test: add unit tests for payment endpoint` |
## Git Branch Prefixes 
| **Prefix**      | **Meaning**                                          | **Example**                                  |
| --------------- | ---------------------------------------------------- | -------------------------------------------- |
| **`feature/`**  | Feature – A new feature or function                  | `feature/user-page` oder `feature/dark-mode` |
| **`fix/`**      | Bug Fix – A bug has been fixed                       | `fix/header-padding`                         |
| **`refactor/`** | Refactoring – Code restructured without logic change | `refactor/api-cleanup`                       |
| **`docs/`**     | Documentation – Changes to docs or comments          | `docs/update-readme`                         |
| **`hotfix/`**   | Critical error in the live system                    | `hotfix/crash-on-launch`                     |

## Backend (Python / FastAPI)
* **Code Formatting:** Ruff (Linting, Formatting & Import Sorting)
* **Name Conventions:**
  * `snake_case` for variables, functions, and methods
  * `PascalCase` for classes and Pydantic models
  * `UPPER_CASE` for global constants

## Frontend (Vue.js)
* **Tools:** ESLint + Prettier
* **Name Conventions:**
  * `PascalCase` for component files (`UserProfile.vue`) and usage
  * `camelCase` for JS/TS variables, functions, and props
* **Color Convention (`/frontend/src/assets/css/main.css`):**
  * Use CSS Custom Properties (`--color-primary`, `--color-bg-main`) instead of hardcoded hex codes.

## Database (PostgreSQL)
* **Name Conventions:**
  * `snake_case` for tables, columns, and foreign keys
  * Plural nouns for table names (`users`, `orders`)
* **SQL Style:**
  * SQL keywords in UPPERCASE (e.g., `SELECT`, `FROM`, `WHERE`)
