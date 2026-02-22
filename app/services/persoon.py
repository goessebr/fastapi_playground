from app.data.db.dao.persoon import PersoonDAO
from app.data.db.dao.organisatie import OrganisatieDAO
from app.data.db.models import Organisatie
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

    async def create_persoon(
        self, persoon_schema: PersoonCreate, created_by: dict
    ) -> Persoon:
        existing = await self.dao.get_by_voornaam(persoon_schema.voornaam)
        if existing:
            raise PersoonExistsException()

        organisaties_orm: list[Organisatie] = []
        if persoon_schema.organisaties:
            ids = [getattr(org, "id") for org in persoon_schema.organisaties]
            organisaties_orm = await self.org_dao.get_by_ids(ids)
            if len(organisaties_orm) != len(ids):
                missing = set(ids) - {o.id for o in organisaties_orm}
                raise ValueError(f"Organisaties not found for ids: {sorted(missing)}")

        data = persoon_schema.model_dump()
        # verwijder eventuele dicts zodat SQLAlchemy geen dicts probeert toe te voegen aan de relatie
        data.pop("organisaties", None)

        self.common_service.set_system_fields_new_entry(data, created_by=created_by)
        new = Persoon(**data)
        new.organisaties = organisaties_orm

        return await self.dao.save(new)
