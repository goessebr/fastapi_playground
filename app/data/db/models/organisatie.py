from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship

from datetime import datetime, timezone

from app.data.db.base import Base
from app.data.db.models.relations import persoon_organisatie


class Organisatie(Base):
    __tablename__ = "organisatie"
    id = Column(Integer, primary_key=True)
    naam = Column(String(length=255), nullable=False, unique=True)
    personen = relationship("Persoon", secondary=persoon_organisatie, back_populates="organisaties")

    # system fields
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_by = Column(String(length=120), nullable=False, default="ongekend")

    def __repr__(self) -> str:  # pragma: no cover - trivial
        return f"Organisatie(id={self.id!r}, naam={self.naam!r})"
