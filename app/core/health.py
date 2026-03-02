from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from app.infrastructure.database.sqlalchemy import get_engine
from app.core.config import get_settings

settings = get_settings()


async def check_db_async() -> bool:
    """
    Use the async SQLAlchemy engine for runtime readiness/startup checks.
    """
    engine: AsyncEngine = get_engine()
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            val = result.scalar_one_or_none()
            return val == 1
    except Exception:
        return False