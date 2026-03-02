from pydantic import BaseModel, Field, ConfigDict

from app.schemas.common import SystemFields


class OrganisatieBase(BaseModel):
    naam: str = Field(max_length=255)


class OrganisatieCreate(OrganisatieBase):
    pass


class OrganisatieRef(BaseModel):
    id: int


class OrganisatieSummary(OrganisatieBase, OrganisatieRef):
    pass


class OrganisatieResponse(OrganisatieBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    systemfields: SystemFields
