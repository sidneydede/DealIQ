"""add crm_tasks (US-M20-02)

Revision ID: f1c8b6d4e2a7
Revises: e9a4c2f7b3d1
Create Date: 2026-06-29 19:20:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'f1c8b6d4e2a7'
down_revision: Union[str, None] = 'e9a4c2f7b3d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('crm_tasks',
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('note', sa.Text(), nullable=True),
    sa.Column('due_date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('status', sa.Enum('a_faire', 'fait', name='taskstatus', native_enum=False), nullable=False),
    sa.Column('company_id', sa.String(length=36), nullable=True),
    sa.Column('assignee_id', sa.String(length=36), nullable=True),
    sa.Column('created_by', sa.String(length=36), nullable=True),
    sa.Column('done_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['assignee_id'], ['users.id'], name=op.f('fk_crm_tasks_assignee_id_users')),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], name=op.f('fk_crm_tasks_company_id_companies')),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], name=op.f('fk_crm_tasks_created_by_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_crm_tasks'))
    )
    op.create_index(op.f('ix_crm_tasks_assignee_id'), 'crm_tasks', ['assignee_id'], unique=False)
    op.create_index(op.f('ix_crm_tasks_company_id'), 'crm_tasks', ['company_id'], unique=False)
    op.create_index(op.f('ix_crm_tasks_due_date'), 'crm_tasks', ['due_date'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_crm_tasks_due_date'), table_name='crm_tasks')
    op.drop_index(op.f('ix_crm_tasks_company_id'), table_name='crm_tasks')
    op.drop_index(op.f('ix_crm_tasks_assignee_id'), table_name='crm_tasks')
    op.drop_table('crm_tasks')
