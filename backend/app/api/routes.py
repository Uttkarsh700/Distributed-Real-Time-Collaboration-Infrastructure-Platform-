from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.database.session import SessionLocal
from app.services.redis_service import check_redis_connection

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "CloudCollab API", "version": settings.API_VERSION}


@router.get("/health/database")
async def health_database() -> dict[str, str]:
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except SQLAlchemyError as exc:
        return {"status": "error", "database": "disconnected", "detail": str(exc)}
    except Exception as exc:
        return {"status": "error", "database": "disconnected", "detail": str(exc)}
    finally:
        db.close()


@router.get("/health/redis")
async def health_redis() -> dict[str, str]:
    if check_redis_connection():
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
