"""add zichtbaarheid to persoon

Revision ID: cef446336358
Revises: b2c3d4e5f6a7
Create Date: 2026-02-22 18:56:06.002178

"""
from typing import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cef446336358'
down_revision: str | Sequence[str] | None = "b2c3d4e5f6a7"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("persoon", sa.Column("zichtbaarheid", sa.String(length=50), nullable=False, server_default='publiek'))


def downgrade() -> None:
    pass
