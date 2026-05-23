# Backend

The backend is the FastAPI service responsible for the platform's core application logic.

## Responsibilities

- REST APIs for workspaces, projects, and deployment actions
- Authentication and JWT-based access control foundation
- WebSocket endpoints for realtime collaboration and status updates
- Database access through PostgreSQL
- Deployment trigger orchestration
- Logs and metrics APIs for the frontend

## Current State

This stage contains only the backend foundation. The application is intentionally minimal and does not yet include database models, auth flows, realtime logic, or worker integration.

## Backend Setup - Step 2

### Create a virtual environment

```bash
cd backend
python -m venv venv
```

### Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

macOS / Linux:

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run PostgreSQL and Redis

```bash
cd ../infra
docker compose up -d
```

### Run the backend

```bash
cd ../backend
uvicorn app.main:app --reload --port 8000
```

### Health check endpoints

- http://localhost:8000/
- http://localhost:8000/health
- http://localhost:8000/health/database
- http://localhost:8000/health/redis
- http://localhost:8000/system/info
- http://localhost:8000/docs

## Authentication Setup - Step 4

The backend now includes a basic JWT authentication system for local development.

Endpoints

- Register: `POST /api/v1/auth/register`
- Login: `POST /api/v1/auth/login` (form data: `username`, `password`)
- Current user: `GET /api/v1/auth/me` (requires `Authorization: Bearer <token>`)

Quick test commands:

Start backend:

```bash
uvicorn app.main:app --reload --port 8000
```

Register user:

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
	-H "Content-Type: application/json" \
	-d "{\"email\":\"test@cloudcollab.dev\",\"full_name\":\"Test User\",\"password\":\"password123\"}"
```

Login user:

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
	-H "Content-Type: application/x-www-form-urlencoded" \
	-d "username=test@cloudcollab.dev&password=password123"
```

Get current user (replace YOUR_ACCESS_TOKEN):

```bash
curl -X GET http://localhost:8000/api/v1/auth/me \
	-H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Swagger docs can also be used to test login at `http://localhost:8000/docs`.

## Database Setup - Step 3

This step adds the first SQLAlchemy schema, Alembic migrations, and a simple local seed script.

### Table overview

- `users` stores accounts, profile data, and verification flags.
- `workspaces` stores team spaces and their owners.
- `workspace_members` stores workspace membership and roles (`owner`, `admin`, `developer`, `viewer`).
- `projects` stores project-level configuration and environment metadata.
- `project_files` stores collaborative files and versioned content.
- `deployments` stores deployment runs and their status (`pending`, `building`, `testing`, `deploying`, `running`, `failed`, `cancelled`).
- `deployment_logs` stores streaming log lines for each deployment using levels (`info`, `warning`, `error`, `success`).
- `audit_logs` stores action history across workspaces and projects.

### Migrations and seed data

1. Start infra:

```bash
cd infra
docker compose up -d
```

2. Install dependencies:

```bash
cd backend
pip install -r requirements.txt
```

3. Run migrations:

```bash
alembic upgrade head
```

4. Seed demo data:

```bash
python ../scripts/seed_db.py
```

5. Check health:

```bash
http://localhost:8000/health/database
```
