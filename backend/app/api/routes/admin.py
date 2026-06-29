"""Routes admin — lecture du journal d'audit (M22)."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.api.pagination import Page, Pagination, pagination
from app.database import get_db
from app.domain.enums import AuditAction
from app.models.audit import AuditLog
from app.models.user import User
from app.schemas.audit import AuditLogOut

router = APIRouter()


@router.get("/audit", response_model=Page[AuditLogOut])
def read_audit(
    action: AuditAction | None = None,
    object_id: str | None = None,
    page: Pagination = Depends(pagination),
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> Page[AuditLogOut]:
    q = db.query(AuditLog).order_by(AuditLog.created_at.desc())
    if action:
        q = q.filter(AuditLog.action == action)
    if object_id:
        q = q.filter(AuditLog.object_id == object_id)
    total = q.count()
    rows = q.offset(page.offset).limit(page.limit).all()
    return Page.build(rows, total, page)
