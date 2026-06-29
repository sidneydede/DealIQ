"""Route mini-rapport readiness (M6) + export PDF serveur."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, load_company
from app.database import get_db
from app.domain.enums import Role
from app.models.company import Company
from app.models.user import User
from app.schemas.report import ReportOut
from app.services import pdf as pdf_svc
from app.services import report as svc

router = APIRouter()


def _load_for_report(company_id: str, db: Session, user: User) -> Company:
    if user.role == Role.investisseur:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")
    company = load_company(company_id, db, user)
    if company.financing_need is None or company.financing_need.deal_type_primary is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sélectionnez d'abord un type de deal",
        )
    return company


@router.get("/companies/{company_id}/report", response_model=ReportOut)
def get_report(
    company_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> dict:
    company = _load_for_report(company_id, db, user)
    return svc.build(db, company, user)


@router.get("/companies/{company_id}/report.pdf")
def get_report_pdf(
    company_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> Response:
    company = _load_for_report(company_id, db, user)
    data = svc.build(db, company, user)
    content = pdf_svc.report_pdf(data)
    filename = f"rapport-readiness-{company_id[:8]}.pdf"
    return Response(
        content=content,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
