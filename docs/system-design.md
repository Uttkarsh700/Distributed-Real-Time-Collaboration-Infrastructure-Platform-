# System Design

## Services

| Service | Responsibility |
|---|---|
| Frontend | Dashboard, editor, logs, metrics, and collaboration UI |
| FastAPI API | REST endpoints, authentication foundation, workspace and project operations |
| FastAPI WebSocket layer | Live collaboration and realtime status delivery |
| PostgreSQL | Durable storage for users, workspaces, projects, jobs, and audit records |
| Redis | Pub/sub, transient state, and Celery broker support |
| Celery Worker | Background processing for deployment simulation and long-running tasks |

---

## Data Flow

1. The frontend sends standard requests to the FastAPI API.
2. The API validates the request and reads or writes data in PostgreSQL.
3. For async work, the API submits a job to Celery through Redis.
4. The worker processes the job and publishes progress updates.
5. The frontend receives those updates through the realtime channel.

---

## Realtime Flow

- Clients connect to the WebSocket endpoint after authentication.
- Collaboration events and presence updates are broadcast through Redis pub/sub.
- The WebSocket layer relays those messages to all interested clients.
- The UI updates in near real time without refreshing the page.

---

## Deployment Flow

- A user triggers a deployment from a project screen.
- The API creates a deployment job record and sends the task to Celery.
- The worker simulates Docker-based deployment activity in this prototype stage.
- Status changes are emitted as the job progresses.
- The frontend renders the deployment result and history for the project.

---

## Logging Flow

- The worker produces log and status events while the job runs.
- Those events are written or relayed through Redis pub/sub.
- The WebSocket layer forwards the stream to connected clients.
- The frontend shows the logs in a live panel next to the project.

---

## Scaling Plan

**Current prototype:**
- Single backend service
- One Celery worker
- Single PostgreSQL instance
- Single Redis instance

**Growth path:**
- Split realtime workloads from REST workloads if traffic grows.
- Scale Celery workers horizontally for more concurrent jobs.
- Add read replicas or partitioned storage when history data grows significantly.
- Introduce dedicated observability and notification services only when the platform needs them.
