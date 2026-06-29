"""add company_history (US-M2-03)

Revision ID: e9a4c2f7b3d1
Revises: d7e2b9c4a1f8
Create Date: 2026-06-29 18:50:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'e9a4c2f7b3d1'
down_revision: Union[str, None] = 'd7e2b9c4a1f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('company_history',
    sa.Column('company_id', sa.String(length=36), nullable=False),
    sa.Column('field', sa.String(length=60), nullable=False),
    sa.Column('old_value', sa.String(length=500), nullable=True),
    sa.Column('new_value', sa.String(length=500), nullable=True),
    sa.Column('changed_by', sa.String(length=36), nullable=True),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['changed_by'], ['users.id'], name=op.f('fk_company_history_changed_by_users')),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], name=op.f('fk_company_history_company_id_companies')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_company_history'))
    )
    op.create_index(op.f('ix_company_history_company_id'), 'company_history', ['company_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_company_history_company_id'), table_name='company_history')
    op.drop_table('company_history')
