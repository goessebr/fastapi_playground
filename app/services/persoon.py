from sqlalchemy.ext.asyncio import AsyncSession

from app.data.db.dao.persoon import PersoonDAO
from app.data.db.dao.organisatie import OrganisatieDAO
from app.data.db.models.persoon import Persoon
from app.schemas.persoon import PersoonCreate

from app.exceptions.persoon import PersoonExistsException
from app.services.base import CommonService


class PersoonService:
    def __init__(self, common_service: CommonService, dao: PersoonDAO, org_dao: OrganisatieDAO):
        self.common_service = common_service
        self.dao = dao
        self.org_dao = org_dao

    async def get_persoon(self, persoon_id: int) -> Persoon | None:
        return await self.dao.get_by_id(persoon_id)

    async def create_persoon(self, persoon_schema: PersoonCreate, created_by: dict) -> Persoon:
        existing = await self.dao.get_by_voornaam(persoon_schema.voornaam)
        if existing:
            raise PersoonExistsException()
        data = persoon_schema.model_dump()
        org_refs = data.pop("organisaties", None)
        organisaties = []
        if org_refs:
            ids = [getattr(ref, "id") for ref in org_refs]
            organisaties = await self.org_dao.get_by_ids(ids)
            # ensure all provided ids exist
            if len(organisaties) != len(ids):
                missing = set(ids) - {o.id for o in organisaties}
                raise ValueError(f"Organisaties not found for ids: {sorted(missing)}")
        self.common_service.set_system_fields_new_entry(data, created_by=created_by)
        new = Persoon(**data)
        if organisaties:
            new.organisaties = organisaties

        return await self.dao.save(new)
