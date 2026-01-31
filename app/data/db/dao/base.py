import datetime
from zoneinfo import ZoneInfo

from app.data.db.base import Base as ORMBase
from datetime import datetime

from sqlalchemy.ext.asyncio.session import AsyncSession


class BaseDAO:
    def __init__(self, db: AsyncSession):
        self.db = db

    def set_db_system_fields(self, orm_object: ORMBase) -> None:
        orm_object.updated_at = datetime.now(ZoneInfo("Europe/Brussels"))
        orm_object.updated_by = getattr(orm_object, "updated_by", None) or "ongekend"
