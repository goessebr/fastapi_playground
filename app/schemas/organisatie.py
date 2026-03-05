from pydantic import BaseModel, Field, ConfigDict

from app.schemas.common import SystemFields


class OrganisatieBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    naam: str = Field(max_length=255)


class OrganisatieCreate(OrganisatieBase):
    pass


class OrganisatieRef(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int


class OrganisatieSummary(OrganisatieBase, OrganisatieRef):
    pass


class OrganisatieResponse(OrganisatieBase):
    id: int
    systemfields: SystemFields
