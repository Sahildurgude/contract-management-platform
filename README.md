Contract Management Platform

A full-stack Contract Management Platform built to demonstrate backend-first system design, strict lifecycle enforcement, and clean API-driven workflows.

The primary focus of this project is correctness, state control, and workflow enforcement, rather than visual UI polish.

This application is fully deployed to demonstrate end-to-end full-stack development, cloud deployment, and frontend–backend integration.

🔗 Live Deployment

Frontend (Vercel):
https://contract-management-platform-three.vercel.app

Backend API (Render):
https://contract-management-platform-h7fb.onrender.com

API Health Check:
https://contract-management-platform-h7fb.onrender.com/health

⚠️ Note: The backend is hosted on Render’s free tier, so the first request may take ~20–30 seconds due to cold start.

🚀 Features
1. Blueprint Management

Blueprints act as reusable contract templates.

Each blueprint contains configurable fields

Supported field types:

Text

Date

Signature

Checkbox

Every field stores:

Field type

Label

Position (x, y)

Blueprints are persisted in the database and serve as the source of truth for contract creation.

2. Contract Creation

Contracts are created from existing blueprints

At creation time, all blueprint fields are copied into the contract

This ensures contracts remain immutable even if a blueprint changes later

Contract data and field values are stored independently of blueprints

3. Contract Lifecycle Management

Each contract follows a strict, backend-enforced lifecycle:

CREATED → APPROVED → SENT → SIGNED → LOCKED
        ↘ REVOKED
SENT    ↘ REVOKED

Lifecycle Rules

Lifecycle transitions are validated on the backend

Invalid transitions are rejected via API

Locked contracts are immutable

Revoked contracts cannot move forward

Frontend reflects only allowed actions and cannot bypass backend rules

Lifecycle enforcement is implemented as a backend state machine.

4. Contract Listing & Dashboard

Contracts are listed via a dashboard UI

Current lifecycle state is clearly displayed

Lifecycle actions are rendered dynamically based on current state

Contracts can be grouped by:

Active

Pending

Signed

🏗 Architecture Overview
Frontend (React + TypeScript, Vite, Vercel)
        |
        | REST APIs
        v
Backend (FastAPI, Render)
        |
        | SQLAlchemy ORM
        v
SQLite Database

⚙️ Tech Stack
Backend

Python

FastAPI

SQLAlchemy ORM

SQLite

Pydantic (validation)

Frontend

React

TypeScript

React Router

Vite

🧩 Data Model
Blueprint

id

name

created_at

fields

Contract

id

name

blueprint_id

state

created_at

fields

Blueprint fields are copied into contract fields at creation time to preserve historical correctness.

Note: The terms state and status are used interchangeably to represent the contract lifecycle state.

🔒 Lifecycle Enforcement

Lifecycle rules are enforced entirely on the backend.

Allowed transitions:

CREATED → APPROVED, REVOKED

APPROVED → SENT

SENT → SIGNED, REVOKED

SIGNED → LOCKED

Any invalid transition results in a 400-level API error.

📡 API Summary
Blueprint APIs

POST /blueprints — Create blueprint

GET /blueprints — List blueprints

GET /blueprints/{id} — Retrieve blueprint

Contract APIs

POST /contracts — Create contract from blueprint

GET /contracts — List contracts

GET /contracts?group=active|pending|signed — Grouped listing

POST /contracts/{id}/transition — Perform lifecycle transition

🛠 Local Development Setup (Optional)
Backend
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload


Backend runs at:
http://127.0.0.1:8000

Swagger docs:
http://127.0.0.1:8000/docs

Frontend
cd frontend
npm install
npm run dev


Frontend runs at:
http://localhost:5173

🧠 Assumptions & Trade-offs

Authentication intentionally omitted

SQLite used for simplicity and fast setup

UI prioritizes clarity over visual polish

No background jobs or async workers

Database starts empty; data is created via application workflows

🔮 Possible Enhancements

Role-based access control

Contract value editing UI

Lifecycle timeline visualization

Audit logs

Dockerized setup

Automated tests

✅ Project Status

Blueprint management ✔

Contract creation ✔

Lifecycle enforcement ✔

Dashboard & grouping ✔

Frontend–backend integration ✔

Cloud deployment ✔

Documentation ✔

👤 Author

Sahil
