# Architecture

CloudCollab is organized as a set of focused services around a shared collaboration and deployment workflow.

```mermaid
flowchart LR
    FE[Frontend]
    API[FastAPI API]
    WS[FastAPI WebSocket]
    PG[(PostgreSQL)]
    REDIS[(Redis Pub/Sub)]
    WORKER[Celery Worker]
    SIM[Docker Deployment Simulator]
    FE_LOGS[Logs / Status / Metrics UI]

    FE --> API --> PG
    FE --> WS --> REDIS
    API --> WORKER
    WORKER --> SIM
    SIM --> REDIS
    REDIS --> WS
    WS --> FE
    REDIS --> FE_LOGS
```

## Reading The Diagram

- The frontend talks to the FastAPI API for normal application requests.
- The API persists project and workspace data in PostgreSQL.
- The frontend connects to FastAPI WebSockets for collaboration and live updates.
- Redis acts as the pub/sub layer that moves realtime events between the backend and UI.
- FastAPI sends deployment work to Celery workers.
- The worker runs a Docker-based deployment simulator in this prototype phase.
- Status and log events are published back through Redis and WebSockets so the frontend can show them live.
