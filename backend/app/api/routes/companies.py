"""Routes entreprise (M2) et type de deal (M24)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_cabinet
from app.database import get_db
from app.domain.enums import DealTypeChangeSource, Role
from app.models.company import Company
from app.models.user import User
from app.schemas.company import (
    CompanyCreate,
    CompanyCreateResult,
    CompanyOut,
    CompanyStatusUpdate,
    CompanyUpdate,
    DealTypeHistoryOut,
    DealTypeRequalify,
    DealTypeSelect,
    FinancingNeedOut,
)
from app.services import companies as svc

router = APIRouter()


def _ip(request: Request) -> str | None:
    return request.client.host if request.client else None


def _load(company_id: str, db: Session, user: User) -> Company:
    company = db.get(Company, company_id)
    if company is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entreprise introuvable")
    if not svc.can_access(user, company):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")
    return company


@router.post("", response_model=CompanyCreateResult, status_code=status.HTTP_201_CREATED)
def create_company(
    payload: CompanyCreate,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> CompanyCreateResult:
    company, duplicates = svc.create_company(db, payload, user, ip=_ip(request))
    return CompanyCreateResult(
        company=CompanyOut.model_validate(company), duplicate_warnings=duplicates
    )


@router.get("", response_model=list[CompanyOut])
def list_companies(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> list[Company]:
    return svc.list_for_user(db, user)


@router.get("/{company_id}", response_model=CompanyOut)
def get_company(
    company_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> Company:
    return _load(company_id, db, user)


@router.patch("/{company_id}", response_model=CompanyOut)
def update_company(
    company_id: str,
    payload: CompanyUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Company:
    company = _load(company_id, db, user)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(company, field, value)
    db.commit()
    db.refresh(company)
    return company


@router.patch("/{company_id}/status", response_model=CompanyOut)
def update_status(
    company_id: str,
    payload: CompanyStatusUpdate,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_cabinet),
) -> Company:
    company = _load(company_id, db, user)
    return svc.change_status(db, company, payload.status, user, ip=_ip(request))


# --- M24 : type de deal ---
@router.post("/{company_id}/deal-type", response_model=FinancingNeedOut)
def set_deal_type(
    company_id: str,
    payload: DealTypeSelect,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> FinancingNeedOut:
    company = _load(company_id, db, user)
    source = (
        DealTypeChangeSource.cabinet
        if user.role in {Role.analyste, Role.senior, Role.admin}
        else DealTypeChangeSource.entrepreneur
    )
    need = svc.change_deal_type(
        db, company,
        primary=payload.deal_type_primary,
        secondary=payload.deal_type_secondary,
        source=source,
        actor=user,
        amount=payload.amount,
        use_of_funds=payload.use_of_funds,
        horizon=payload.horizon,
        ip=_ip(request),
    )
    return FinancingNeedOut.model_validate(need)


@router.post("/{company_id}/deal-type/requalify", response_model=FinancingNeedOut)
def requalify_deal_type(
    company_id: str,
    payload: DealTypeRequalify,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_cabinet),
) -> FinancingNeedOut:
    """Requalification réservée au cabinet (RG-M24-04), motif obligatoire."""
    company = _load(company_id, db, user)
    need = svc.change_deal_type(
        db, company,
        primary=payload.deal_type_primary,
        secondary=payload.deal_type_secondary,
        source=DealTypeChangeSource.cabinet,
        actor=user,
        motif=payload.motif,
        ip=_ip(request),
    )
    return FinancingNeedOut.model_validate(need)


@router.get("/{company_id}/deal-type/history", response_model=list[DealTypeHistoryOut])
def deal_type_history(
    company_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> list:
    company = _load(company_id, db, user)
    return svc.history(db, company)
