# 🛠️ Backend-Architektur & Dokumentation

Dieses Backend basiert auf **Python (FastAPI)** und folgt einer Drei-Schichten-Architektur (_Layered Architecture_ / _Modular Monolith_). Die strikte Trennung von API-Endpunkten, Geschäftslogik und Datenbankzugriffen sorgt für hohe Stabilität, einfache Wartbarkeit und ermöglicht automatisierte Tests.

---

## 📁 Ordnerstruktur

```
backend/
├── app/
│   ├── main.py              # Startpunkt der Anwendung (FastAPI App, CORS, Router)
│   │
│   ├── api/                 # A) API-SCHICHT (Routing, Request/Response & Auth)
│   │   ├── deps.py          # Gemeinsame Dependencies (DB-Session, Rollenprüfung)
│   │   └── v1/              # API-Version 1
│   │       ├── users.py     # Endpunkte für User (/users/...)
│   │       ├── products.py  # Endpunkte für Produkte (/products/...)
│   │       └── transactions.py # Endpunkte für Transaktionen & Kasse
│   │
│   ├── services/            # B) LOGIKSCHICHT (Geschäftslogik & Transaktionen)
│   │   ├── checkout.py      # Bezahlvorgang, Guthabenprüfung, Stornierung
│   │   └── nfc.py           # Validierung & Mapping von NFC-Karten
│   │
│   ├── models/              # C) DATENBANK-TABELLEN (SQLAlchemy / SQLModel)
│   │   ├── user.py          # ORM-Model: Users-Tabelle
│   │   ├── product.py       # ORM-Model: Products-Tabelle
│   │   └── transaction.py   # ORM-Model: Transactions-Tabelle
│   │
│   ├── schemas/             # D) DATENVALIDIERUNG & DTOs (Pydantic)
│   │   ├── checkout.py      # Request/Response-Formate für Kassen-Requests
│   │   ├── user.py          # Request/Response-Formate für User-Daten
│   │   └── product.py       # Request/Response-Formate für Produkte
│   │
│   └── db/                  # E) DATENBANK-VERBINDUNG
│       ├── session.py       # DB-Engine Setup & SessionLocal (PostgreSQL)
│       └── init_db.py       # Initialisierung / Seeding (z.B. Admin-User anlegen)
│
├── .env                     # Umgebungsvariablen (DB-Zugangsdaten, Secrets)
└── requirements.txt         # Python-Abhängigkeiten

```

---

## 🔍 Wofür sind die Ordner & Dateien da?

### 1. `app/main.py`

Der Haupteinstiegspunkt. Hier wird die `FastAPI()`-Instanz erzeugt, Middleware (wie CORS für den iPad-Zugriff) konfiguriert und die API-Router aus `api/v1/` eingebunden.

### 2. `app/api/` (API-Schicht)

Nimmt HTTP-Requests vom Frontend (iPad-Kasse / Web-Admin) entgegen.

- **`deps.py`**: Enthält Hilfsfunktionen, die per Dependency Injection (`Depends`) in Routen geladen werden – z. B. das Bereitstellen einer Datenbank-Session pro Request oder das Prüfen von Benutzerrollen.
- **`v1/*.py`**: Die einzelnen Endpunkte. **Wichtig:** Hier wird keine komplexe Logik geschrieben! Die Routen nehmen Daten entgegen, rufen Funktionen aus `services/` auf und liefern das Ergebnis zurück.

### 3. `app/services/` (Logikschicht – _Herzstück_)

Enthält die reine Geschäftslogik (Business Logic).

- **`checkout.py`**: Verarbeitet den Kassen-Checkout. Liest das Guthaben aus, prüft `guthaben >= kaufbetrag`, zieht das Geld ab, schreibt das Protokoll in die Datenbank und stellt sicher, dass alles atomar (ACID) geschieht.
- **`nfc.py`**: Logik zur schnellen Zuordnung einer gescannten NFC-UID zu einer `user_id`.

### 4. `app/models/` (Datenbank-Tabellen)

Definiert die Struktur der PostgreSQL-Tabellen als Python-Klassen mit SQLAlchemy/SQLModel.

- Hier liegen die tatsächlichen DB-Spalten (z. B. `balance_cents`, `nfc_uid`, `school_id`).

### 5. `app/schemas/` (Pydantic DTOs)

Sichert den Datenaustausch nach außen ab.

- Definiert exakt, wie JSON-Daten vom iPad ankommen müssen und was die API zurückgibt.
- Verhindert, dass fehlerhafte Datentypen an die Logikschicht oder Datenbank übergeben werden.

### 6. `app/db/` (DB-Setup)

Verwaltet die Verbindung zu PostgreSQL.

- **`session.py`**: Verbindet sich über den `DATABASE_URL`-String aus `.env` mit der Datenbank und stellt die DB-Sessions bereit.

---

## ⚡ Wichtige Entwicklungs-Richtlinien

### 1. Geldbeträge immer in Cents speichern (`INTEGER`)

- **Keine `FLOAT`-Werte für Geld!** Fließkommazahlen führen zu Rundungsfehlern (`2.9900000000000002 €`).
- In der Datenbank und im Backend wird ausschließlich in Ganzzahlen (Cents) gerechnet:
- `10,50 €` $\rightarrow$ `1050`
- `3,00 €` $\rightarrow$ `300`

- Die Umrechnung in Euro erfolgt erst im Frontend bei der Anzeige.

### 2. Datenbank-Transaktionen & Race-Conditions

Guthaben-Abbuchungen in `services/checkout.py` **müssen** innerhalb einer expliziten SQL-Transaktion mit Row-Level Locking stattfinden:

```python
# Verhindert zeitgleiche Doppelabwendungs-Versuche
user = db.query(User).filter(User.id == user_id).with_for_update().first()

```

### 3. Multi-Tenancy (Vorbereitung für weitere Schulen)

Jede Kern-Tabelle (`users`, `products`, `transactions`) enthält das Feld **`school_id`**. Im MVP hat dieses überall den gleichen Wert (z. B. `"schule-1"`). Bei einer späteren Expansion kann die API die Daten dadurch sauber trennen.

---

## 📋 Entwicklungs-Fortschritt (Dateien-Checkliste)

- [x] `requirements.txt` (Abhängigkeiten definiert)
- [x] `.env` (Datenbank-Zugangsdaten)
- [x] `app/db/session.py` (PostgreSQL-Verbindung & `get_db` Dependency)
- [x] `app/db/init_db.py` (Skript zum Erstellen der DB-Tabellen & Demo-Seeding)
- [x] `app/models/user.py` (ORM-Model: Benutzer, Guthaben in Cents, NFC-UID)
- [x] `app/models/product.py` (ORM-Model: Produkte & Cent-Preise)
- [x] `app/models/transaction.py` (ORM-Model: Transaktions-Historie)
- [ ] `app/schemas/user.py` (Pydantic-Models für User-Anfragen & -Antworten)
- [ ] `app/schemas/product.py` (Pydantic-Models für Produkte)
- [ ] `app/schemas/checkout.py` (Pydantic-Models für den Kassen-Warenkorb)
- [ ] `app/services/nfc.py` (Schnelle NFC-UID zu User-ID Auflösung)
- [ ] `app/services/checkout.py` (Kassen-Abbuchung mit Guthabenprüfung & ACID-Lock)
- [ ] `app/api/deps.py` (Dependencies für DB-Session & einfache Rollenprüfung)
- [ ] `app/api/v1/users.py` (Routen für User-Suche & Guthaben)
- [ ] `app/api/v1/products.py` (Routen für Produktliste & Bearbeitung)
- [ ] `app/api/v1/transactions.py` (Routen für Checkout & Storno)
- [ ] `app/main.py` (FastAPI Einstiegspunkt mit CORS-Support fürs iPad)
