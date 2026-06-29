"""Schéma Pydantic — lecture du journal d'audit (M22)."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.domain.enums import AuditAction


class AuditLogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    actor_id: str | None
    actor_email: str | None
    action: AuditAction
    object_type: str | None
    object_id: str | None
    meta: dict
    ip_address: str | None
    created_at: datetime
