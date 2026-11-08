# BirkPay – Frontend Structure

## Directory Tree

```text
Frontend/
├── app/
│   ├── app.vue
│   ├── assets/css/main.css
│   ├── components/
│   │   ├── User/LogInComponent.vue
│   │   ├── bank/accountcard.vue
│   │   ├── bank/depositcard.vue
│   │   ├── bank/transhistory.vue
│   │   ├── layout/AppNavbar.vue
│   │   ├── layout/AppSidebar.vue
│   │   ├── pos/CartSummary.vue
│   │   ├── pos/PaymentModal.vue
│   │   └── pos/ProductGrid.vue
│   ├── layouts/
│   │   ├── default.vue
│   │   ├── bank.vue
│   │   ├── bank/bank.vue
│   │   ├── pos/pos.vue
│   │   ├── pos/products.vue
│   │   └── pos/sales.vue
│   ├── modules/pos/components/CkeckoutCart.vue
│   ├── modules/pos/components/ProductGrid.vue
│   └── pages/
│       ├── index.vue
│       ├── adminPortal/
│       │   ├── index.vue
│       │   ├── admin/reports.vue
│       │   ├── admin/users.vue
│       │   ├── bank/cash.vue
│       │   ├── bank/index.vue
│       │   ├── pos/index.vue
│       │   ├── pos/products.vue
│       │   └── pos/sales.vue
│       ├── bank/index.vue
│       ├── pos/index.vue
│       ├── pos/pos.vue
│       ├── pos/products.vue
│       └── pos/sales.vue
├── public/robots.txt
├── nuxt.config.ts
├── package.json
└── postcss.config.js
```

## Framework and Configuration

| Area | Implementation |
|---|---|
| App framework | Nuxt 4, Vue 3; `app/app.vue` renders `NuxtLayout` and `NuxtPage` |
| Pages/routing | Nuxt file-based routing from `app/pages/`; Nuxt uses Vue Router |
| Components | Vue single-file components (`.vue`), Composition API (`<script setup>`) |
| Styling | Tailwind CSS 4 via `@tailwindcss/vite`; `@nuxtjs/tailwindcss` is also installed as a Nuxt module |
| UI/icons | Nuxt UI and Nuxt Icon |
| Internationalization | `@nuxtjs/i18n` is installed and enabled as a module; no local translation files or additional i18n configuration were found in the inspected `app/` tree |
| State management | Local Vue refs and computed properties; no Pinia/Vuex in `package.json` |

`nuxt.config.ts` loads `~/assets/css/main.css`, registers `@nuxt/icon`, `@nuxt/ui`, and `@nuxtjs/i18n`, enables Vite Tailwind, and binds the dev server to `0.0.0.0:3000`. The Nuxt compatibility date is `2026-10-05`.

## UI Organization

| Path | Responsibility |
|---|---|
| `app/pages/` | Route pages grouped into admin portal, banking, and POS |
| `app/layouts/` | Page shells for default, banking, and POS |
| `app/components/layout/` | Shared navigation and sidebar |
| `app/components/pos/` | Reusable POS components: product grid, cart summary, payment modal |
| `app/components/bank/` | Account, deposit, and transaction-history views |
| `app/components/User/` | Login component |
| `app/modules/pos/components/` | Additional POS components; some overlap functionally with `components/pos/` |
| `app/assets/css/main.css` | Tailwind/Nuxt UI imports, palette, and global CSS variables |

The home page `pages/index.vue` redirects to `/adminPortal`. `pages/bank/index.vue` disables the default layout and renders the bank view directly. The `adminPortal/` route has dedicated admin, bank, and POS subpages.

## State and Component Contracts

- State is held locally in pages or components using `ref()`/`computed()`; there is no centralized store.
- Components receive data through props and report actions to parents through typed `defineEmits()` events (for example, `ProductGrid` emits category selection and cart actions).
- Some UI is split into components; other pages contain their own UI/business logic. `components/pos/` and `modules/pos/components/` are parallel locations and should be checked for reusable components before adding more.
- File names do not consistently follow `PascalCase` (for example, `accountcard.vue`, `depositcard.vue`, `transhistory.vue`); preserve exact import paths.
- Project conventions specify `PascalCase` for components and `camelCase` for variables/functions. Prefer CSS variables from `main.css`.

## Backend Integration: Current State

The POS layout keeps its product catalogue and cart locally, but payment now waits for a keyboard-wedge NFC scan and submits the scanned UID and cart items through `server/api/pos/checkout.post.ts` to `POST /api/v1/transactions/checkout`. The server route supplies `X-NFC-Key` from private runtime configuration; successful completion depends on the backend response. Backend API contracts are described in [Backend Structure](./02-backend-structure.md).

Configure `NUXT_BACKEND_BASE_URL` with the backend origin and `NUXT_CASHIER_NFC_UID` with the UID of an authorized cashier/admin card. Both values are private server runtime configuration. Payment simulation is disabled by default; set `NUXT_PUBLIC_PAYMENT_SIMULATION=true` only when intentionally testing the UI without a card or backend checkout.

## Dependencies and Scripts

- Runtime: `nuxt`, `vue`, `vue-router`, `typescript`.
- UI: `@nuxt/ui`, `@nuxt/icon`, Tailwind CSS/PostCSS.
- Other installed features: Nuxt i18n and Tiptap editor extensions; no concrete use of the Tiptap dependencies is apparent in the inspected `app/` tree.
- Scripts: `npm run dev`, `npm run build`, `npm run generate`, `npm run preview`; no test or lint script is defined in `package.json`.
- Project `docs/Conventions.md` mentions ESLint/Prettier, but these tools are not configured in the current frontend scripts or dependencies.
