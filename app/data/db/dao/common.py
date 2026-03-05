import datetime
from typing import Callable
from typing import Iterable
from typing import List
from zoneinfo import ZoneInfo
from datetime import datetime

from typing import TypeVar, Generic, Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")

class CommonDAO(Generic[ModelType]):
    """
    Provides shared async DAO utilities in a generic way so this module
    does not import concrete models (avoids circular imports).
    """
    def __init__(self, db: AsyncSession, db_class: Type[ModelType]):
        self.db = db
        self.db_class = db_class

    def set_db_system_fields(self, orm_object: ModelType) -> None:
        # set/override system fields as needed; tolerant if attributes absent
        if hasattr(orm_object, "updated_at"):
            setattr(orm_object, "updated_at", datetime.now(ZoneInfo("Europe/Brussels")))
        if not getattr(orm_object, "updated_by", None):
            # set default only if not already set
            try:
                setattr(orm_object, "updated_by", "ongekend")
            except Exception:
                # ignore if object doesn't allow attribute assignment
                pass

    async def get_by_id(self, object_id: int) -> ModelType | None:
        result = await self.db.execute(
            select(self.db_class).where(self.db_class.id == object_id)
        )
        return result.scalars().first()

    async def save(self, orm_object: ModelType, attribute_names: Iterable[str] | None = None) -> ModelType:
        self.set_db_system_fields(orm_object)
        self.db.add(orm_object)
        await self.db.flush()
        await self.db.refresh(orm_object, attribute_names=attribute_names)
        return orm_object