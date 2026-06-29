"""Routes DD OHADA/SYSCOHADA (M18)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api.deps import load_company, require_cabinet
from app.database import get_db
from app.models.user import User
from app.schemas.dd import DdAnalysisOut, ImportIn, ImportOut
from app.services import dd as svc

router = APIRouter()


def _ip(request: Request) -> str | None:
    return request.client.host if request.client else None


@router.post("/companies/{company_id}/syscohada", response_model=ImportOut, status_code=201)
def import_balance(
    company_id: str,
    payload: ImportIn,
    db: Session = Depends(get_db),
    user: User = Depends(require_cabinet),
):
    company = load_company(company_id, db, user)
    return svc.import_balance(db, company, payload, user)


@router.get("/companies/{company_id}/syscohada", response_model=ImportOut)
def get_import(
    company_id: str, db: Session = Depends(get_db), user: User = Depends(require_cabinet)
):
    company = load_company(company_id, db, user)
    imp = svc.latest_import(db, company)
    if imp is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune balance importée")
    return imp


@router.post("/companies/{company_id}/dd/compute", response_model=DdAnalysisOut)
def compute_dd(
    company_id: str,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_cabinet),
):
    company = load_company(company_id, db, user)
    try:
        return svc.compute(db, company, user, ip=_ip(request))
    except svc.DdError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e


@router.get("/companies/{company_id}/dd", response_model=DdAnalysisOut)
def get_dd(
    company_id: str, db: Session = Depends(get_db), user: User = Depends(require_cabinet)
):
    company = load_company(company_id, db, user)
    analysis = svc.latest_analysis(db, company)
    if analysis is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune DD calculée")
    return analysis
