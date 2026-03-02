from typing import AsyncGenerator
from typing import AsyncIterator
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.sqlalchemy import get_sessionmaker

MUTATING_METHODS = {"POST", "PUT", "PATCH", "DELETE"}

async def get_db(request: Request) -> AsyncGenerator[AsyncSession, None]:
    async with get_sessionmaker()() as session:
        try:
            yield session
            if request.method in MUTATING_METHODS:
                await session.commit()
            else:
                await session.rollback()
        except Exception:
            await session.rollback()
            raise


async def get_db_without_request() -> AsyncIterator[AsyncSession]:
    """Dependency that yields a database session and closes it afterwards.
    Gebruik deze voor taken die op de achtergrond worden uitgevoerd zonder HTTP-request context"""
    async with get_sessionmaker()() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
