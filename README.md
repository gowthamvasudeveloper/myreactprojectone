# Expense Management

Full-stack expense app: **FastAPI + MySQL** (`backend/`) and **React + Vite + Tailwind** (`frontend/`).

## Quick start (local)

**Backend**

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

**Frontend**

```bash
cd frontend
npm install
copy .env.example .env
npm run dev
```

From repo root you can also run:

```bash
npm run install:frontend
npm run dev
```

## Docker

```bash
docker compose up -d --build
```

- App UI: http://localhost:3000  
- API docs: http://localhost:8000/docs  
- phpMyAdmin: http://localhost:8080  

## Layout

- `backend/` — API, models, services, Docker image  
- `frontend/` — SPA, nginx image for compose  
- `docker-compose.yml` — mysql, backend, frontend, phpmyadmin  
