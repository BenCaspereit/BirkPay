# 💳 BirkPay

> **A lightweight digital payment system for school-based economic simulations.**

[![Status](https://img.shields.io/badge/Status-In%20Development-orange?style=for-the-badge)](https://github.com/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Vue.js](https://img.shields.io/badge/Vue.js-4FC08D?style=for-the-badge&logo=vuedotjs&logoColor=white)](https://vuejs.org/)
[![ESP32](https://img.shields.io/badge/Hardware-ESP32-E7352C?style=for-the-badge&logo=espressif&logoColor=white)](https://www.espressif.com/)

---

## 📖 Overview

**BirkPay** is a digital payment system designed for a school-based economic simulation.

The project digitizes the fictional currency (_Birklinge_) used in the simulation, allowing participants to receive salaries and pay for goods and services using digital balances.

Built with **Vue.js**, **FastAPI**, and **PostgreSQL**, BirkPay combines a web-based frontend with a REST API and persistent data storage to manage users, payments, salaries, and transaction history.

The project also includes a hardware component: an **ESP32-based NFC reader** designed to enable contactless identification at supported terminals.

BirkPay is developed independently as a personal hobby project, combining full-stack software development, database design, API development, automated testing, and embedded hardware integration.

---

## 🖥️ Application Preview

BirkPay provides dedicated interfaces for point-of-sale operations, banking, and system administration.

### Point of Sale (POS)

![BirkPay POS interface](pos.png)

### Bank

![BirkPay Bank interface](bank.png)

### Admin Dashboard

![BirkPay Admin Dashboard](adminPortal.png)

---

## 🏗️ Architecture

BirkPay follows a client-server architecture. The Vue.js frontend communicates with a FastAPI backend, which handles application logic and interacts with the PostgreSQL database.

The planned NFC integration extends this architecture with an ESP32-based reader connected to the client device.

```text
┌─────────────────────────┐
│      NFC Reader         │
│                         │
│  NFC Module + ESP32     │
└────────────┬────────────┘
             │
             │ Bluetooth / Serial*
             ▼
┌─────────────────────────┐
│      Client Device      │
│          Vue.js         │
│                         │
│   POS · Bank · Admin    │
└────────────┬────────────┘
             │
             │ HTTPS / LAN
             ▼
┌─────────────────────────┐
│     FastAPI Backend     │
│                         │
│  Authentication         │
│  Role-Based Access      │
│  Payment Processing     │
│  Salary Processing      │
│  Transaction Services   │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│       PostgreSQL        │
│                         │
│    Persistent Storage   │
└─────────────────────────┘
```

_The exact communication method between the ESP32 and the client depends on the final hardware implementation. NFC integration and end-to-end testing are still in development._

### Communication Flow

1. The NFC reader detects a supported NFC card or tag.
2. The ESP32 processes the reader interaction and communicates with the client.
3. The Vue.js application sends relevant requests to the FastAPI backend.
4. The backend handles the required business logic and database operations.
5. PostgreSQL stores the application's persistent data.

---

## ⚡ Backend

The backend is built with **Python 3.12** and **FastAPI**, with PostgreSQL serving as the database.

### Responsibilities

- REST API endpoints for users, products, and transactions
- Role-based access control
- Payment and checkout processing
- Salary-related operations
- Database interactions and persistence
- Transaction recording and history
- NFC-related services

The backend provides the core business logic and data layer for the BirkPay application.

---

## 🖥️ Frontend

The frontend is built with **Vue.js** and provides separate interfaces for the main workflows of the simulation.

| Interface              | Purpose                                        |
| ---------------------- | ---------------------------------------------- |
| 💳 **POS**             | Process payments at points of sale.            |
| 🏦 **Bank**            | Support banking and salary-related operations. |
| 🛠️ **Admin Dashboard** | Manage and monitor the system.                 |

The POS and bank interfaces are implemented. The admin dashboard is undergoing final adjustments, while further frontend-backend integration remains part of the development process.

---

## 🔐 Roles & Permissions

BirkPay uses role-based access control (RBAC) to separate responsibilities within the simulated economy.

| Role           | Responsibilities                                    |
| -------------- | --------------------------------------------------- |
| 👤 **User**    | Participate in the simulation and make payments.    |
| 🧾 **Cashier** | Process payments at points of sale.                 |
| 🏦 **Banker**  | Handle salaries and other money-related operations. |
| 🛠️ **Admin**   | Manage and monitor the application.                 |

Each role represents a distinct set of responsibilities within the system.

---

## 💸 Payments & Transactions

BirkPay supports the transaction workflows required for the simulated economy.

### Payments

Participants can use their digital balances to pay for goods and services, such as food at the school cafeteria.

### Salary Processing

The system supports salary-related operations based on participants' simulated professions.

### Transaction History

Transactions include relevant information such as:

- **Transaction ID** — A unique identifier for the transaction.
- **Amount** — The amount transferred.
- **Details** — Information about the transaction.
- **Timestamp** — When the transaction occurred.

This information provides a record of financial activity within the simulation.

---

## 🧪 Testing

BirkPay uses **pytest** for automated testing.

The current test suite covers API endpoints and selected service-level functionality.

| Test Area           |  Tests |
| ------------------- | -----: |
| `api/products`      |      5 |
| `api/transaction`   |      4 |
| `api/users`         |      7 |
| `services/checkout` |      4 |
| `services/nfc`      |      5 |
| **Total**           | **25** |

The current test suite contains **25 tests** across API and service modules.

---

## 🛠️ Tech Stack

| Component              | Technology         |
| ---------------------- | ------------------ |
| **Language**           | Python 3.12        |
| **Backend Framework**  | FastAPI            |
| **Database**           | PostgreSQL         |
| **API Architecture**   | REST               |
| **Frontend Framework** | Vue.js             |
| **Hardware**           | ESP32 + NFC reader |
| **Testing Framework**  | pytest             |

---

## 🗺️ Roadmap

### ✅ Completed

- [x] Core backend implementation
- [x] REST API for users
- [x] REST API for products
- [x] REST API for transactions
- [x] Database integration for users
- [x] Database integration for products
- [x] Database integration for transactions
- [x] POS interface
- [x] Bank interface
- [x] Initial automated test suite

### 🚧 In Progress

- [ ] Final adjustments to the admin dashboard
- [ ] Frontend-backend integration
- [ ] Middleware implementation
- [ ] ESP32 and NFC reader assembly
- [ ] NFC firmware development

### 📌 Planned

- [ ] Complete end-to-end NFC integration
- [ ] Test the complete payment workflow with the NFC hardware
- [ ] Improve NFC security
- [ ] Add additional payment options
- [ ] Conduct a real-world test during the next school simulation, if development is completed in time

---

## 🧭 Next Milestone

The next major milestone is to prepare BirkPay for use during the upcoming school economic simulation.

The goal is to test the application in a real usage scenario, including payment workflows and, if ready, NFC-based identification.

If the system is not ready for deployment in time, the simulation can still serve as an opportunity to explore the concept of digital currency and payment systems together with students involved in the banking role.

This provides a practical way to evaluate the idea, gather feedback, and identify improvements for future development.

---

## 🎯 Project Goals

BirkPay aims to provide a simple, maintainable, and extensible digital payment infrastructure for school-based economic simulations.

The project combines full-stack development, database design, API development, automated testing, and embedded hardware integration in a practical application.

By replacing physical currency with digital transactions, BirkPay explores how a small, self-contained digital economy can be managed through a centralized software system.

---

_Developed independently as a personal software and hardware project._
