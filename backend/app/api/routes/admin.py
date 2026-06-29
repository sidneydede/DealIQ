"""Routes admin — lecture du journal d'audit (M22)."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.api.pagination import (
    Page,
    Pagination,
    SortParams,
    apply_sql_sort,
    pagination,
    sorting,
)
from app.database import get_db
from app.domain.enums import AuditAction
from app.models.audit import AuditLog
from app.models.user import User
from app.schemas.audit import AuditLogOut

router = APIRouter()

_AUDIT_SORT = {"created_at": AuditLog.created_at, "action": AuditLog.action}


@router.get("/audit", response_model=Page[AuditLogOut])
def read_audit(
    action: AuditAction | None = None,
    object_id: str | None = None,
    sort: SortParams = Depends(sorting),
    page: Pagination = Depends(pagination),
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> Page[AuditLogOut]:
    q = db.query(AuditLog)
    if action:
        q = q.filter(AuditLog.action == action)
    if object_id:
        q = q.filter(AuditLog.object_id == object_id)
    total = q.count()
    q = apply_sql_sort(q, sort, _AUDIT_SORT, default=AuditLog.created_at)
    rows = q.offset(page.offset).limit(page.limit).all()
    return Page.build(rows, total, page)
