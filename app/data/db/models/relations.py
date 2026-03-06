from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey

from app.data.db.base import Base


# association table for many-to-many relation between persoon and organisatie
persoon_organisatie = Table(
    "persoon_organisatie",
    Base.metadata,
    Column("persoon_id", Integer, ForeignKey("persoon.id", ondelete="CASCADE"), primary_key=True),
    Column("organisatie_id", Integer, ForeignKey("organisatie.id", ondelete="CASCADE"), primary_key=True),
)
