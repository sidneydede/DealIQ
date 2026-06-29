"""add user mfa_secret

Revision ID: c5d1e8a3f6b2
Revises: b3f7c1a2d9e4
Create Date: 2026-06-29 17:30:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c5d1e8a3f6b2'
down_revision: Union[str, None] = 'b3f7c1a2d9e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('mfa_secret', sa.String(length=64), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'mfa_secret')
