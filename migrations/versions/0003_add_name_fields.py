"""add first_name and last_name to statements

Revision ID: 0003
Revises: 0002
Create Date: 2026-06-27 13:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0003"
down_revision: Union[str, None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("statements", sa.Column("first_name", sa.String(100), nullable=True))
    op.add_column("statements", sa.Column("last_name", sa.String(100), nullable=True))


def downgrade() -> None:
    op.drop_column("statements", "last_name")
    op.drop_column("statements", "first_name")
