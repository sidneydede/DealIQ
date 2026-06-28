"""Schéma initial — Lot 0 (users, companies, deal_types, scores, documents, audit_logs).

Migration de bootstrap greenfield : crée l'ensemble du schéma à partir de la metadata
des modèles. Les évolutions ultérieures utiliseront l'autogénération Alembic classique.

Revision ID: 0001_initial
Revises:
Create Date: 2026-06-28
"""
from typing import Sequence, Union

from alembic import op

from app.models import Base

revision: str = "0001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    Base.metadata.create_all(bind=op.get_bind())


def downgrade() -> None:
    Base.metadata.drop_all(bind=op.get_bind())
