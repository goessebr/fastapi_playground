"""initinal

Revision ID: 3e8dc1d54bf6
Revises: 
Create Date: 2026-01-20 21:01:04.675672

"""
from typing import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3e8dc1d54bf6'
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema: create persoon table."""
    op.create_table(
        "persoon",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("voornaam", sa.String(length=255), nullable=False, unique=True),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("TIMEZONE('Europe/Brussels', now())")),
        sa.Column("updated_by", sa.String(length=255), nullable=False),
    )
    # op.create_table(
    #     "persoon_statussen",
    #     sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
    #     sa.Column("persoon_id", sa.Integer(), sa.ForeignKey("persoon.id"), nullable=False),
    #     sa.Column("naam", sa.String(length=255), nullable=False, unique=True),
    #     sa.Column("updated_at", sa.DateTime(), nullable=False),
    # )


def downgrade() -> None:
    """Downgrade schema: drop persoon table."""
    op.drop_table("persoon")