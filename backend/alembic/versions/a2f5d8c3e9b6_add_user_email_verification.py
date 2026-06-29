"""add user email verification (US-M1-02)

Revision ID: a2f5d8c3e9b6
Revises: f1c8b6d4e2a7
Create Date: 2026-06-29 19:50:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'a2f5d8c3e9b6'
down_revision: Union[str, None] = 'f1c8b6d4e2a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'users',
        sa.Column('email_verified', sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column('users', sa.Column('email_otp', sa.String(length=6), nullable=True))
    op.add_column('users', sa.Column('email_otp_expires', sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'email_otp_expires')
    op.drop_column('users', 'email_otp')
    op.drop_column('users', 'email_verified')
