# Tech Stack

## Frontend: TypeScript, React/Next.js, Tailwind CSS, shadcn/ui
TypeScript adds type safety for a product that will grow across many screens and states. React and Next.js provide a practical app framework for dashboards, authenticated views, and server-friendly rendering. Tailwind CSS and shadcn/ui help move quickly while keeping the UI consistent and production-friendly.

## Editor: Monaco Editor
Monaco is the code editor experience used in VS Code, which makes it a strong fit for editing infrastructure files, manifests, and config content directly in the browser.

## Collaboration: Yjs
Yjs provides real-time shared document state. It is a good fit for collaborative editing because it handles concurrent updates and can scale to multiple clients with a clear sync model.

## Backend: FastAPI
FastAPI is a strong choice for a modern Python backend because it is fast, typed, and good for building REST APIs plus realtime endpoints around the same application layer.

## Realtime: FastAPI WebSockets
WebSockets provide the live communication channel needed for collaboration awareness, deployment status, and log streaming.

## Database: PostgreSQL
PostgreSQL is the primary system of record for users, workspaces, projects, deployment history, and audit data.

## Cache / PubSub / Queue Broker: Redis
Redis supports realtime event distribution, shared state helpers, and background job coordination.

## Background Jobs: Celery + Redis
Celery is a proven background job system for deployment simulations, asynchronous tasks, and longer-running workflow steps.

## Runtime / Infra: Docker + Docker Compose
Docker keeps the platform environment reproducible, and Docker Compose makes local development and infrastructure dependencies easy to start.

## Auth: JWT
JWT is a practical foundation for API authentication in a prototype that needs stateless token-based access.

## CI/CD: GitHub Actions
GitHub Actions is a natural fit for automated checks, builds, and future deployment pipelines.
