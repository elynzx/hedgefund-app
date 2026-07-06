<p align="center">
  <img src=".github/assets/hedgehog-logo.png" alt="HedgeFund mascot a friendly hedgehog" width="110"/>
</p>

<h1 align="center">HedgeFund App</h1>

<p align="center">
  A personal finance tracker to take control of your income, expenses, and savings goals without the overwhelm.
  <br/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Flask-3.1-000000?style=flat-square&logo=flask"/>
  <img src="https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat-square&logo=postgresql&logoColor=white"/>
  <img src="https://img.shields.io/badge/JWT-Auth-F5A623?style=flat-square&logo=jsonwebtokens&logoColor=white"/>
  <img src="https://img.shields.io/badge/Pydantic-v2-E92063?style=flat-square&logo=pydantic&logoColor=white"/>
  <img src="https://img.shields.io/badge/Swagger-Docs-85EA2D?style=flat-square&logo=swagger&logoColor=black"/>
</p>

---

## What is HedgeFund?

HedgeFund is a **REST API-powered personal finance tracker** that helps you log income and expenses, manage bank accounts and credit cards, and understand your spending at a glance guided by the 50/30/20 budgeting rule.

Built as an academic project using Flask, SQLAlchemy, and PostgreSQL, with JWT authentication, Pydantic validation, and Swagger documentation.

> **Multi-currency support** — set your currency (PEN, USD, EUR) once in your profile; every amount displays with the right symbol automatically.


## Key features

| Feature | Description |
|---|---|
| JWT Authentication | Secure register & login with bcrypt-hashed passwords |
| Bank accounts | Track balances across multiple accounts simultaneously |
| Credit cards | Monitor debt, credit limit, and available credit in real time |
| Transactions | Log income, expenses, transfers, and card payments |
| Categories | Organize spending by type: needs, wants, obligations |
| Monthly summary | Total income, expenses, balance, and 50/30/20 progress |
| Atomic balance updates | Every transaction updates balances and card debt instantly |
| Multi-currency | Choose PEN, USD, EUR from your profile |



## Tech stack

| Layer | Technology |
|---|---|
| Framework | Flask 3.1 + Flask-RESTful 0.3.10 |
| ORM | SQLAlchemy 3.1 — `Mapped` / `mapped_column` style |
| Database | PostgreSQL 16 |
| Auth | Flask-JWT-Extended 4.7 + bcrypt 4.3 |
| Validation | Pydantic v2 with `EmailStr` |
| Migrations | Flask-Migrate 4.0 (Alembic) |
| API docs | Flasgger 0.9 (Swagger UI at `/apidocs`) |
| Frontend | HTML + CSS templates (Jinja2) |
| Config | python-dotenv + cryptography (Fernet) |



## Getting started

### Prerequisites

- Python 3.11+
- PostgreSQL 16+
- pip

### 1. Clone the repository

```bash
git clone https://github.com/your-username/hedgefund-app.git
cd hedgefund-app
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root folder:

```env
DATABASE_URL=postgresql://your_user:your_password@localhost:5432/hedgefund_db
JWT_SECRET_KEY=your_jwt_secret
SECRET_KEY=your_flask_secret
FERNET_KEY=your_fernet_key
```

> **Generate a Fernet key:**
> ```bash
> python key_generator.py
> ```

### 5. Set up the database
Create the database in PostgreSQL and apply the existing database migrations to build your local schema:

```bash
# Create the database in psql
CREATE DATABASE hedgefund_db;

# Run migrations
flask db upgrade
```

### 6. Seed default categories
Run the custom Flask CLI command to automatically feed the system with the standard financial categories required by the 50/30/20 budgeting rules:

```bash
flask shell
>>> flask seed-categories
```

### 7. Run the development server

```bash
python run.py
```

| URL | Description |
|---|---|
| `http://localhost:5000` | App / frontend |
| `http://localhost:5000/apidocs` | Swagger UI |



## API endpoints

All routes except `/auth/*` require:
```
Authorization: Bearer <your_jwt_token>
```

### Auth

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/auth/register` | Create a new user account |
| `POST` | `/auth/login` | Login and receive a JWT token |

### Bank accounts

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/accounts` | List all active accounts |
| `POST` | `/accounts` | Create a new bank account |
| `PUT` | `/accounts/<id>` | Update account name or type |
| `DELETE` | `/accounts/<id>` | Deactivate an account (soft delete) |

### Credit cards

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/cards` | List cards with real-time available credit |
| `POST` | `/cards` | Register a new credit card |
| `PUT` | `/cards/<id>` | Update card details |
| `DELETE` | `/cards/<id>` | Deactivate a card |

### Transactions

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/transactions` | List transactions — filter by `date`, `type`, `category` |
| `POST` | `/transactions` | Create transaction + update balances atomically |
| `DELETE` | `/transactions/<id>` | Delete and reverse the balance change |

### Profile

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/profile` | Get profile (income, currency, fixed expenses) |
| `PUT` | `/profile` | Update income, currency, or fixed expense targets |

### Summary

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/summary` | Monthly income, expenses, balance + 50/30/20 breakdown |



## Project structure

Following the pattern established in class — resources, services, schemas, and models as separate layers:

```
hedgefund-app/
├── run.py                        # Entry point
├── config.py                     # App configuration class
├── db.py                         # SQLAlchemy instance
├── key_generator.py              # Fernet key generator utility
├── requirements.txt
├── .env                          # Environment variables (not committed)
├── .gitignore
├── app/
│   ├── __init__.py               # App factory — registers extensions & resources
│   ├── router.py                 # Flask-RESTful API route registration
│   ├── models/                   # SQLAlchemy ORM models
│   ├── schemas/                  # Pydantic v2 validation schemas
│   ├── resources/                # Flask-RESTful resources (HTTP layer)
│   │   ├── auth_resource.py
│   │   ├── bank_account_resource.py
│   │   ├── credit_card_resource.py
│   │   ├── transaction_resource.py
│   │   ├── user_resource.py
│   │   └── summary_resource.py
│   ├── services/                 # Business logic layer
│   └── utils/
│       ├── __init__.py
│       ├── security.py            # hash_password, verify_password, CryptoHelper
│       └── seed.py                # seed_categories   
└── migrations/                   # Alembic — auto-generated, do not edit manually
    └── versions/
```


## How transactions work (business logic)

When `POST /transactions` is called, `transaction_service` executes everything in a single atomic operation:

```
income        → + amount to destination account
expense       → - amount from origin account (or + debt to credit card)
transfer      → - from origin account  /  + to destination account
card payment  → - from origin account  /  - debt from credit card
```

If anything fails, SQLAlchemy rolls back the entire operation, no partial state is ever saved.


## The 50/30/20 rule

HedgeFund uses your fixed monthly income (set in your profile) to calculate recommended spending limits and show your progress each month:

```
Your income: USD 7,400
─────────────────────────────────
 Needs     50%  →  USD 3,700   (rent, utilities, groceries)
 Wants     30%  →  USD 2,220   (dining out, entertainment)
 Savings   20%  →  USD 1,480   (savings goals, debt payments)
```

The `/summary` endpoint returns actual vs. recommended amounts so the frontend can display progress bars for each category.


## Multi-currency support

Set your currency once during registration or from your profile settings:

| Code | Symbol | Currency |
|---|---|---|
| PEN | S/ | Peruvian Sol |
| USD | $ | US Dollar |
| EUR | € | Euro |

Amounts are stored as plain `NUMERIC` — no conversion is applied. The currency symbol is used for display only.


## License

Developed as an academic project. Open for educational use.


<p align="center">Build with ♡ by <a href="https://github.com/elynzx">@elynzx</a> · <a href="https://linkedin.com/in/evelynpascualc">LinkedIn</a></p>