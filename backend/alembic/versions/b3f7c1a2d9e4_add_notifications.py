"""add notifications

Revision ID: b3f7c1a2d9e4
Revises: 06071a6cba37
Create Date: 2026-06-29 16:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'b3f7c1a2d9e4'
down_revision: Union[str, None] = '06071a6cba37'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('notifications',
    sa.Column('recipient_id', sa.String(length=36), nullable=False),
    sa.Column('type', sa.Enum('investor_interest', 'qa_asked', 'qa_answered',
                              'dataroom_access_granted', 'kyc_hit',
                              name='notificationtype', native_enum=False), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('body', sa.String(length=1000), nullable=False),
    sa.Column('link', sa.String(length=255), nullable=True),
    sa.Column('object_type', sa.String(length=80), nullable=True),
    sa.Column('object_id', sa.String(length=36), nullable=True),
    sa.Column('read_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['recipient_id'], ['users.id'], name=op.f('fk_notifications_recipient_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_notifications'))
    )
    op.create_index(op.f('ix_notifications_recipient_id'), 'notifications', ['recipient_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_notifications_recipient_id'), table_name='notifications')
    op.drop_table('notifications')
