from pathlib import Path

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.router import api_router
from app.core.config import get_settings
from app.core.health import check_db_async
from app.core.logging import configure_logging, get_logger
from app.exceptions.common import NotFoundException
from app.exceptions.handlers import not_found_handler
from app.exceptions.handlers import register_exception_handlers
from app.infrastructure.database.sqlalchemy import dispose_engine
from app.web.router import html_router

settings = get_settings()
LOG = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    configure_logging(settings.DEBUG)
    LOG.info("Starting application: %s", settings.PROJECT_NAME)
    try:
        ready = await check_db_async()
        if not ready:
            LOG.warning("Database readiness check failed during startup")
    except Exception:
        LOG.exception("Exception while running startup checks")
    yield
    # shutdown / teardown
    LOG.info("Shutting down application")
    try:
        await dispose_engine()
    except Exception:
        LOG.exception("Error while disposing database engine")


app: FastAPI = FastAPI(
    title=settings.PROJECT_NAME, debug=settings.DEBUG, lifespan=lifespan
)

register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.DEBUG else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# serve the simple frontend at /frontend using absolute path resolved from project root
project_root = Path(__file__).resolve().parents[1]
frontend_path = project_root.joinpath(settings.FRONTEND_DIR)
if frontend_path.exists():
    app.mount(
        "/frontend",
        StaticFiles(directory=str(frontend_path), html=True),
        name="frontend",
    )
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(api_router, prefix="")
app.include_router(html_router)
