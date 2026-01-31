from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.data.db.dao.persoon import PersoonDAO
from app.data.db.models.persoon import Persoon
from app.schemas.persoon import PersoonCreate

from app.exceptions.persoon import PersoonExistsException
from app.services.base import CommonService


class PersoonService:
    def __init__(self, dao: PersoonDAO):
        self.dao = dao
        self.common = CommonService()

    async def get_persoon(self, persoon_id: int) -> Persoon | None:
        return await self.dao.get_by_id(persoon_id)

    async def create_persoon(self, persoon_schema: PersoonCreate, created_by: dict) -> Persoon:
        existing = await self.dao.get_by_voornaam(persoon_schema.voornaam)
        if existing:
            raise PersoonExistsException()
        data = persoon_schema.model_dump()
        self.common.set_system_fields_new_entry(data, created_by=created_by)
        new = Persoon(**data)
        return await self.dao.save(new)
