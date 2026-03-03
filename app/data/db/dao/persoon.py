from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.data.db.dao.base import BaseDAO
from app.data.db.dao.common import CommonDAO
from app.data.db.models.persoon import Persoon


class PersoonDAO(BaseDAO):
    """
    Data Access Object for Persoon model, providing methods to interact with the database.
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.common = CommonDAO(db=db, db_class=Persoon)

    async def get_by_id(self, persoon_id: int) -> Persoon | None:
        stmt = (
            select(Persoon)
            .options(selectinload(Persoon.organisaties))
            .where(Persoon.id == persoon_id)
        )
        return await self.db.scalar(stmt)

    async def get_by_voornaam(self, voornaam: str) -> Persoon | None:
        result = await self.db.execute(
            select(Persoon).where(Persoon.voornaam == voornaam)
        )
        return result.scalars().first()

    async def save(self, persoon: Persoon) -> Persoon:
        return await self.common.save(orm_object=persoon)
