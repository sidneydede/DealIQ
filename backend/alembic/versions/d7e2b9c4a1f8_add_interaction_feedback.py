"""add interaction feedback / next_step (US-M10-04)

Revision ID: d7e2b9c4a1f8
Revises: c5d1e8a3f6b2
Create Date: 2026-06-29 18:30:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'd7e2b9c4a1f8'
down_revision: Union[str, None] = 'c5d1e8a3f6b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('interactions', sa.Column('feedback', sa.Text(), nullable=True))
    op.add_column('interactions', sa.Column('next_step', sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column('interactions', 'next_step')
    op.drop_column('interactions', 'feedback')
