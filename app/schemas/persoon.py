# File: app/schemas/user.py
from pydantic import BaseModel
from pydantic import Field
from datetime import datetime


class PersoonBase(BaseModel):
    voornaam: str = Field(max_length=120)


class PersoonCreate(PersoonBase):
    pass


class SystemFields(BaseModel):
    updated_at: datetime
    updated_by: str


class PersoonResponse(PersoonBase):
    id: int
    systemfields: SystemFields
