# Backend (FastAPI) - Expense Management API

## What this is
- A production-oriented FastAPI backend, designed with clean architecture:
  controller (routes) → service → repository → database.

## How to run locally (Windows / PowerShell)

1. Create a virtual environment (recommended):

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file:
- Copy `.env.example` to `.env`
- Update `DATABASE_URL` and `JWT_SECRET_KEY`

4. Run the API:

```bash
uvicorn app.main:app --reload --port 8000
```

5. Verify:
- Open Swagger UI at `http://localhost:8000/docs`
- Health check: `GET http://localhost:8000/api/v1/health`

## Notes
- Models, auth, and business modules will be added step-by-step next.

## Run with Docker Compose

1. From project root, copy Docker env file:

```bash
copy .env.docker.example .env
```

2. Build and start all services:

```bash
docker compose up --build
```

3. Access services:
- Frontend: `http://localhost:3000`
- Backend API docs: `http://localhost:8000/docs`
- Backend health: `http://localhost:8000/api/v1/health`

4. Stop services:

```bash
docker compose down
```
