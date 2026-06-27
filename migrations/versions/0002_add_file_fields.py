"""add file fields to statements

Revision ID: 0002
Revises: 0001
Create Date: 2026-06-27 12:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("statements", sa.Column("file_id", sa.String(200), nullable=True))
    op.add_column("statements", sa.Column("file_type", sa.String(20), nullable=True))


def downgrade() -> None:
    op.drop_column("statements", "file_type")
    op.drop_column("statements", "file_id")
