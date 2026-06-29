"""Route mini-rapport readiness (M6)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, load_company
from app.database import get_db
from app.domain.enums import Role
from app.models.user import User
from app.schemas.report import ReportOut
from app.services import report as svc

router = APIRouter()


@router.get("/companies/{company_id}/report", response_model=ReportOut)
def get_report(
    company_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> dict:
    if user.role == Role.investisseur:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")
    company = load_company(company_id, db, user)
    if company.financing_need is None or company.financing_need.deal_type_primary is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sélectionnez d'abord un type de deal",
        )
    return svc.build(db, company, user)
