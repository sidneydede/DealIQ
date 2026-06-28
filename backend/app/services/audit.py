"""Service d'audit (M22). Journalise les actions sensibles de façon append-only."""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.domain.enums import AuditAction
from app.models.audit import AuditLog
from app.models.user import User


def record(
    db: Session,
    action: AuditAction,
    *,
    actor: User | None = None,
    actor_email: str | None = None,
    object_type: str | None = None,
    object_id: str | None = None,
    meta: dict | None = None,
    ip_address: str | None = None,
    commit: bool = True,
) -> AuditLog:
    """Crée une entrée d'audit. Ne modifie jamais une entrée existante (inaltérable)."""
    entry = AuditLog(
        actor_id=actor.id if actor else None,
        actor_email=actor_email or (actor.email if actor else None),
        action=action,
        object_type=object_type,
        object_id=object_id,
        meta=meta or {},
        ip_address=ip_address,
    )
    db.add(entry)
    if commit:
        db.commit()
    return entry
