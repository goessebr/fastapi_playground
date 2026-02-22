from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict


class SystemFields(BaseModel):
    updated_at: datetime
    updated_by: str
