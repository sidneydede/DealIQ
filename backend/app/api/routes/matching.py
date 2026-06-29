"""Route matching (M10)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import load_company, require_cabinet
from app.database import get_db
from app.domain.enums import CompanyStatus
from app.models.user import User
from app.schemas.investor import MatchResult
from app.services import matching as svc

router = APIRouter()


@router.get("/companies/{company_id}/matches", response_model=list[MatchResult])
def company_matches(
    company_id: str,
    include_non_eligible: bool = False,
    db: Session = Depends(get_db),
    user: User = Depends(require_cabinet),
) -> list[dict]:
    company = load_company(company_id, db, user)
    # RG-M10-03 : un dossier non « investor-ready » n'est jamais proposé.
    if company.status != CompanyStatus.investor_ready:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Le dossier doit être « investor-ready » avant tout matching.",
        )
    results = svc.match_company(db, company)
    if not include_non_eligible:
        results = [r for r in results if r["passes_hard_filters"]]
    return results
