"""Routes KYC/KYB/AML (M15) — réservées à la conformité."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.database import get_db
from app.domain.enums import KycStatus, KycSubjectType, Role
from app.models.kyc import KycCheck
from app.models.user import User
from app.schemas.kyc import KycCheckOut, KycRunRequest, KycStatusUpdate
from app.services import kyc as svc

router = APIRouter()

require_conformite = require_roles(Role.conformite, Role.admin)


def _ip(request: Request) -> str | None:
    return request.client.host if request.client else None


@router.post("/kyc/checks", response_model=KycCheckOut, status_code=status.HTTP_201_CREATED)
def run_check(
    payload: KycRunRequest,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_conformite),
) -> KycCheck:
    return svc.run_check(
        db, payload.subject_type, payload.subject_id, payload.check_type, user, ip=_ip(request)
    )


@router.get("/kyc/checks", response_model=list[KycCheckOut])
def list_checks(
    subject_type: KycSubjectType | None = None,
    subject_id: str | None = None,
    status_filter: KycStatus | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(require_conformite),
) -> list[KycCheck]:
    return svc.list_checks(
        db, subject_type=subject_type, subject_id=subject_id, status=status_filter
    )


@router.patch("/kyc/checks/{check_id}", response_model=KycCheckOut)
def update_check(
    check_id: str,
    payload: KycStatusUpdate,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_conformite),
) -> KycCheck:
    check = db.get(KycCheck, check_id)
    if check is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contrôle introuvable")
    return svc.update_status(db, check, payload.status, payload.notes, user, ip=_ip(request))


@router.get("/kyc/subjects/{subject_type}/{subject_id}/cleared")
def subject_cleared(
    subject_type: KycSubjectType,
    subject_id: str,
    db: Session = Depends(get_db),
    _: User = Depends(require_conformite),
) -> dict:
    return {"cleared": svc.is_cleared(db, subject_type, subject_id)}
