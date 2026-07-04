from fastapi import APIRouter
from fastapi.concurrency import run_in_threadpool
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.database.session import SessionLocal
from app.services.redis_service import check_redis_connection
from app.api.v1.auth import router as auth_router
from app.api.v1.workspaces import router as workspace_router

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "CloudCollab API", "version": settings.API_VERSION}


def _check_db() -> None:
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
    finally:
        db.close()


@router.get("/health/database")
async def health_database() -> dict[str, str]:
    try:
        await run_in_threadpool(_check_db)
        return {"status": "ok", "database": "connected"}
    except SQLAlchemyError as exc:
        return {"status": "error", "database": "disconnected", "detail": str(exc)}


@router.get("/health/redis")
async def health_redis() -> dict[str, str]:
    try:
        ok = await run_in_threadpool(check_redis_connection)
    except Exception as exc:
        return {"status": "error", "redis": "disconnected", "detail": str(exc)}

    if ok:
        return {"status": "ok", "redis": "connected"}
    return {
        "status": "error",
        "redis": "disconnected",
        "detail": f"Unable to connect to Redis at {settings.REDIS_URL}",
    }


@router.get("/system/info")
async def system_info() -> dict[str, object]:
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.API_VERSION,
        "environment": settings.ENVIRONMENT,
        "features_initialized": [
            "FastAPI application",
            "Configuration management",
            "PostgreSQL connection setup",
            "Redis connection setup",
            "Health check routes",
        ],
    }


router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(workspace_router, prefix="/workspaces", tags=["workspaces"])
