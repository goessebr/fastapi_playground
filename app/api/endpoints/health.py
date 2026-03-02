from time import time
from fastapi import APIRouter, Response, status
from app.core.health import check_db_async
from app.core.config import get_settings

router = APIRouter()
_start_time = time()
settings = get_settings()

"""
When to use each:
- use /live and /ready for orchestration/probes
- use /health for monitoring and debugging.
"""

@router.get("/live")
async def live():
    """
    Liveness probe: very cheap, only indicates process is alive.
    """
    return {"status": "alive"}


@router.get("/ready")
async def ready(response: Response):
    """
    Readiness probe: checks dependencies required to serve traffic.
    Returns 200 when all required checks pass, 503 otherwise.
    """
    db_ok = await check_db_async()
    # todo add redis, ES, storage, skos, queues, other applications
    ready_ok = db_ok  # add other checks (cache, queues) as needed
    if not ready_ok:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "unready", "checks": {"db": db_ok}}
    return {"status": "ready", "checks": {"db": db_ok}}


@router.get("/health")
async def health(response: Response):
    """
    Aggregate health endpoint for humans and dashboards.
    """
    db_ok = await check_db_async()
    overall = "ok" if db_ok else "unhealthy"
    if not db_ok:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return {
        "status": overall,
        "version": settings.APP_VERSION,
        "uptime_seconds": int(time() - _start_time),
        "checks": {"db": db_ok},
    }


@router.get("/health/db")
async def health_db(response: Response):
    db_ok = await check_db_async()
    if not db_ok:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return {"component": "db", "ok": db_ok}

# capture at import time (cheap and stable)
_version_info = {
    "version": settings.APP_VERSION,
    "branch": getattr(settings, "GIT_BRANCH", settings.GIT_BRANCH),
    "commit": getattr(settings, "GIT_COMMIT", settings.GIT_COMMIT),
    "built_at": getattr(settings, "BUILD_TIME", settings.BUILD_TIME),
}

@router.get("/version")
async def version():
    """
    Simple version/meta endpoint suitable for dashboards and CI.
    Keep sensitive details behind auth or internal network if needed.
    """
    return _version_info