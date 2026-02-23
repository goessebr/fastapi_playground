from typing import Annotated
from typing import Any

from pydantic import BaseModel
from pydantic import Discriminator
from pydantic import Field
from pydantic import ConfigDict
from typing import List

from pydantic import Tag
from pydantic import field_validator

from app.enums import ZichtbaarheidEnum
from app.schemas.common import SystemFields
from app.schemas.organisatie import OrganisatieSummary, OrganisatieRef


class PersoonBase(BaseModel):
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


def _discriminator_key(data: Any) -> str:
    return "persoon_anoniem"  # todo afhankelijk van de rechten persoon_volledig tonen
    # role = _get_role().value
    # if isinstance(data, dict):
    #     premie_type = data.get("type", "")
    #     existing = current_premie.get()
    #     if existing and existing.id == 2:
    #         role = "owner"
    # else:
    #     premie_type = getattr(data, "type", "")
    #     if hasattr(data, "id") and data.id == 2:
    #         role = "owner"
    # return f"{role}_{premie_type}"


PersoonResponse = Annotated[
    Annotated[PersoonResponseFull, Tag("persoon_volledig")]
    | Annotated[PersoonResponseAnoniem, Tag("persoon_anoniem")],
    Discriminator(_discriminator_key),
]
