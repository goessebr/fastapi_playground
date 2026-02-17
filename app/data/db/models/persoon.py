from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from datetime import datetime, timezone

from app.data.db.base import Base
from app.data.db.models.relations import persoon_organisatie


class Persoon(Base):
    __tablename__ = "persoon"
    id = Column(Integer, primary_key=True)
    voornaam = Column(String(length=255), nullable=False, unique=True)
    organisaties = relationship("Organisatie", secondary=persoon_organisatie, back_populates="personen")

    # system fields
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_by = Column(String(length=120), nullable=False, default="ongekend")

    @property
    def systemfields(self) -> dict:
        """Return system fields as a dict so Pydantic (from_attributes) can access them.

        This shape matches the API response schema which nests updated_at and updated_by
        under `systemfields`.
        """
        return {"updated_at": self.updated_at, "updated_by": self.updated_by}
