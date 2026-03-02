from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import all models here so Alembic's autogenerate can see them.
# e.g. from app.data.db.models import user  # noqa: F401