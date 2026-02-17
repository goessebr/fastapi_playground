"""add organisatie and persoon_organisatie

Revision ID: b2c3d4e5f6a7
Revises: 3e8dc1d54bf6
Create Date: 2026-02-01 12:00:00.000000

"""
from typing import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b2c3d4e5f6a7"
down_revision: str | Sequence[str] | None = "3e8dc1d54bf6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema: add organisatie table and persoon_organisatie association table."""
    op.create_table(
        "organisatie",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("naam", sa.String(length=255), nullable=False, unique=True),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("TIMEZONE('Europe/Brussels', now())")),
        sa.Column("updated_by", sa.String(length=120), nullable=False),
    )

    op.create_table(
        "persoon_organisatie",
        sa.Column("persoon_id", sa.Integer(), sa.ForeignKey("persoon.id", ondelete="CASCADE"), primary_key=True, nullable=False),
        sa.Column("organisatie_id", sa.Integer(), sa.ForeignKey("organisatie.id", ondelete="CASCADE"), primary_key=True, nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema: drop association and organisatie tables."""
    op.drop_table("persoon_organisatie")
    op.drop_table("organisatie")

