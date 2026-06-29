"""Routes investisseurs & critères (M9)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_cabinet
from app.database import get_db
from app.models.investor import Investor
from app.models.user import User
from app.schemas.investor import (
    CriteriaIn,
    CriteriaOut,
    InvestorCreate,
    InvestorOut,
    InvestorUpdate,
)
from app.services import investors as svc

router = APIRouter()


def _load(investor_id: str, db: Session, user: User) -> Investor:
    inv = db.get(Investor, investor_id)
    if inv is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Investisseur introuvable"
        )
    if not svc.can_access(user, inv):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")
    return inv


@router.post("", response_model=InvestorOut, status_code=status.HTTP_201_CREATED)
def create_investor(
    payload: InvestorCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_cabinet),
) -> Investor:
    return svc.create_investor(db, payload)


@router.get("", response_model=list[InvestorOut])
def list_investors(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> list[Investor]:
    return svc.list_for_user(db, user)


@router.get("/me", response_model=InvestorOut)
def my_investor(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> Investor:
    inv = svc.my_investor(db, user)
    if inv is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Aucune fiche investisseur rattachée"
        )
    return inv


@router.get("/{investor_id}", response_model=InvestorOut)
def get_investor(
    investor_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> Investor:
    return _load(investor_id, db, user)


@router.patch("/{investor_id}", response_model=InvestorOut)
def update_investor(
    investor_id: str,
    payload: InvestorUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_cabinet),
) -> Investor:
    inv = db.get(Investor, investor_id)
    if inv is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Investisseur introuvable"
        )
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(inv, field, value)
    db.commit()
    db.refresh(inv)
    return inv


@router.get("/{investor_id}/criteria", response_model=CriteriaOut)
def get_criteria(
    investor_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> CriteriaOut:
    inv = _load(investor_id, db, user)
    if inv.criteria is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Critères non définis")
    return CriteriaOut.model_validate(inv.criteria)


@router.put("/{investor_id}/criteria", response_model=CriteriaOut)
def set_criteria(
    investor_id: str,
    payload: CriteriaIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> CriteriaOut:
    inv = _load(investor_id, db, user)  # cabinet ou investisseur propriétaire (US-M9-03)
    crit = svc.upsert_criteria(db, inv, payload)
    return CriteriaOut.model_validate(crit)
