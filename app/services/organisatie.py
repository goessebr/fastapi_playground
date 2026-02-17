from app.data.db.dao.organisatie import OrganisatieDAO
from app.data.db.models.organisatie import Organisatie
from app.exceptions.organisatie import OrganisatieExistsException
from app.schemas.organisatie import OrganisatieCreate

from app.services.base import CommonService


class OrganisatieService:
    def __init__(self, common_service: CommonService, dao: OrganisatieDAO):
        self.common_service = common_service
        self.dao = dao

    async def get_organisatie(self, organisatie_id: int) -> Organisatie | None:
        return await self.dao.get_by_id(organisatie_id)

    async def create_organisatie(
        self, organisatie_schema: OrganisatieCreate, created_by: dict
    ) -> Organisatie:
        existing = await self.dao.get_by_naam(organisatie_schema.naam)
        if existing:
            raise OrganisatieExistsException()
        data = organisatie_schema.model_dump()
        self.common_service.set_system_fields_new_entry(data, created_by=created_by)
        new = Organisatie(**data)
        return await self.dao.save(new)
