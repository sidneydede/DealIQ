"""Routes ESG / impact (M19)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, load_company, require_cabinet
from app.database import get_db
from app.models.user import User
from app.schemas.esg import EsgExport, EsgIn, EsgOut, RequiredUpdate
from app.services import esg as svc

router = APIRouter()


@router.put("/companies/{company_id}/esg", response_model=EsgOut)
def upsert_esg(
    company_id: str,
    payload: EsgIn,
    db: Session = Depends(get_db),
    user: User = Depends(require_cabinet),
) -> dict:
    company = load_company(company_id, db, user)
    profile = svc.upsert(db, company, payload)
    return svc.to_out(profile)


@router.get("/companies/{company_id}/esg", response_model=EsgOut)
def get_esg(
    company_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> dict:
    company = load_company(company_id, db, user)  # propriétaire ou cabinet
    profile = svc.get(db, company)
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profil ESG non renseigné"
        )
    return svc.to_out(profile)


@router.patch("/companies/{company_id}/esg/required", response_model=EsgOut)
def set_required(
    company_id: str,
    payload: RequiredUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_cabinet),
) -> dict:
    company = load_company(company_id, db, user)
    profile = svc.get(db, company) or svc.upsert(db, company, EsgIn())
    profile = svc.set_required(db, profile, payload.esg_required)
    return svc.to_out(profile)


@router.get("/companies/{company_id}/esg/export", response_model=EsgExport)
def export_esg(
    company_id: str, db: Session = Depends(get_db), user: User = Depends(require_cabinet)
) -> dict:
    company = load_company(company_id, db, user)
    profile = svc.get(db, company)
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profil ESG non renseigné"
        )
    return svc.export(db, company, profile)
