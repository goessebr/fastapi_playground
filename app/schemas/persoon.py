from pydantic import BaseModel
from pydantic import Field
from pydantic import ConfigDict
from typing import List

from pydantic import field_validator

from app.enums import ZichtbaarheidEnum
from app.schemas.common import SystemFields
from app.schemas.organisatie import OrganisatieSummary, OrganisatieRef


class PersoonBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    voornaam: str = Field(max_length=120)


class PersoonCreate(PersoonBase):
    organisaties: List[OrganisatieRef] | None = None
    zichtbaarheid: ZichtbaarheidEnum = ZichtbaarheidEnum.publiek

    @field_validator("organisaties")
    @classmethod
    def validate_organisaties(cls, value):
        if value is None:
            return value
        ids = [getattr(ref, "id") for ref in value]
        duplicates = set([oid for oid in ids if ids.count(oid) > 1])
        if duplicates:
            raise ValueError(
                f"Duplicate organisatie ids are not allowed. Duplicates: {sorted(duplicates)}"
            )
        return value


class PersoonResponseBase(PersoonBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    zichtbaarheid: ZichtbaarheidEnum


class PersoonResponseFull(PersoonResponseBase):
    systemfields: SystemFields
    organisaties: List[OrganisatieSummary] | None = None


class PersoonResponseAnoniem(PersoonResponseBase):
    @field_validator("voornaam", mode="before")
    @classmethod
    def set_voornaam_anoniem(cls, value):
        return "Anoniem"


PersoonResponse = PersoonResponseFull | PersoonResponseAnoniem
