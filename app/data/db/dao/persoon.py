
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession


from app.data.db.dao.base import BaseDAO
from app.data.db.models.persoon import Persoon

class PersoonDAO(BaseDAO):
    def __init__(self, db: AsyncSession):
        self.db = db
        super().__init__(self.db)

    async def get_by_id(self, persoon_id: int) -> Persoon | None:
        result = await self.db.execute(
            select(Persoon).where(Persoon.id == persoon_id)
        )
        return result.scalars().first()

    async def get_by_voornaam(self, voornaam: str) -> Persoon | None:
        result = await self.db.execute(
            select(Persoon).where(Persoon.voornaam == voornaam)
        )
        return result.scalars().first()

    async def save(self, persoon: Persoon) -> Persoon:
        self.set_db_system_fields(persoon)  # naar sqlalchemy event listeners?
        self.db.add(persoon)
        await self.db.flush()
        await self.db.refresh(persoon)
        return persoon
