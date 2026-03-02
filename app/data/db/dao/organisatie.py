from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.db.dao.base import BaseDAO
from app.data.db.dao.common import CommonDAO
from app.data.db.models.organisatie import Organisatie


class OrganisatieDAO(BaseDAO):
    """
    Data Access Object for Organisatie model, providing methods to interact with the database.
    """
    def __init__(self, db: AsyncSession):
        self.db = db
        self.common = CommonDAO(db=db, db_class=Organisatie)

    async def get_by_id(self, organisatie_id: int) -> Organisatie | None:
        return await self.common.get_by_id(object_id=organisatie_id)

    async def get_by_naam(self, naam: str) -> Organisatie | None:
        result = await self.db.execute(
            select(Organisatie).where(Organisatie.naam == naam)
        )
        return result.scalars().first()

    async def save(self, organisatie: Organisatie) -> Organisatie:
        return await self.common.save(orm_object=organisatie)

    async def get_by_ids(self, ids: List[int]) -> List[Organisatie]:
        if not ids:
            return []
        stmt = select(Organisatie).where(Organisatie.id.in_(ids))
        result = await self.db.execute(stmt)
        return result.scalars().all()
