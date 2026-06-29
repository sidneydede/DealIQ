"""Routes mandats & honoraires (M17)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api.deps import load_company, require_cabinet, require_roles
from app.database import get_db
from app.domain.enums import Role
from app.models.mandate import Fee, Mandate
from app.models.user import User
from app.schemas.mandate import (
    ConflictItem,
    FeeCreate,
    FeeOut,
    FeeUpdate,
    MandateCreate,
    MandateOut,
    MandateUpdate,
)
from app.services import mandates as svc

router = APIRouter()

require_governance = require_roles(Role.conformite, Role.senior, Role.admin)


def _ip(request: Request) -> str | None:
    return request.client.host if request.client else None


@router.post("/companies/{company_id}/mandates", response_model=MandateOut, status_code=201)
def create_mandate(
    company_id: str,
    payload: MandateCreate,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_cabinet),
) -> Mandate:
    company = load_company(company_id, db, user)
    return svc.create_mandate(db, company, payload, user, ip=_ip(request))


@router.get("/companies/{company_id}/mandates", response_model=list[MandateOut])
def list_mandates(
    company_id: str, db: Session = Depends(get_db), user: User = Depends(require_cabinet)
) -> list[Mandate]:
    company = load_company(company_id, db, user)
    return svc.list_for_company(db, company)


@router.patch("/mandates/{mandate_id}", response_model=MandateOut)
def update_mandate(
    mandate_id: str,
    payload: MandateUpdate,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_cabinet),
) -> Mandate:
    mandate = db.get(Mandate, mandate_id)
    if mandate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mandat introuvable")
    return svc.update_mandate(db, mandate, payload, user, ip=_ip(request))


@router.post("/mandates/{mandate_id}/fees", response_model=FeeOut, status_code=201)
def add_fee(
    mandate_id: str,
    payload: FeeCreate,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_cabinet),
) -> Fee:
    mandate = db.get(Mandate, mandate_id)
    if mandate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mandat introuvable")
    return svc.add_fee(db, mandate, payload, user, ip=_ip(request))


@router.get("/mandates/{mandate_id}/fees", response_model=list[FeeOut])
def list_fees(
    mandate_id: str, db: Session = Depends(get_db), _: User = Depends(require_cabinet)
) -> list[Fee]:
    mandate = db.get(Mandate, mandate_id)
    if mandate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mandat introuvable")
    return svc.list_fees(db, mandate)


@router.patch("/fees/{fee_id}", response_model=FeeOut)
def update_fee(
    fee_id: str,
    payload: FeeUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_cabinet),
) -> Fee:
    fee = db.get(Fee, fee_id)
    if fee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Honoraire introuvable")
    return svc.update_fee(db, fee, payload.status)


@router.get("/conflicts", response_model=list[ConflictItem])
def conflict_register(
    db: Session = Depends(get_db), _: User = Depends(require_governance)
) -> list[dict]:
    return svc.conflicts(db)
