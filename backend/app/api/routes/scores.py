"""Routes readiness score (M5)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api.deps import CABINET_ROLES, get_current_user, load_company
from app.database import get_db
from app.domain import scoring
from app.domain.enums import Role
from app.models.user import User
from app.schemas.score import ScoreEntrepreneurOut, ScoreFullOut
from app.services import scoring as svc

router = APIRouter()


def _ip(request: Request) -> str | None:
    return request.client.host if request.client else None


def _view(score, user: User):
    """Renvoie la vue adaptée au rôle (RG-M5-04)."""
    gaps = scoring.derive_gaps(score.subscores or {})
    if user.role in CABINET_ROLES:
        return ScoreFullOut(
            total=score.total,
            category=score.category,
            confidence=score.confidence,
            grid_version=score.grid_version,
            deal_type_applied=score.deal_type_applied,
            subscores=score.subscores or {},
            gaps=gaps,
        )
    # entrepreneur : catégorie + gaps, jamais le score chiffré
    return ScoreEntrepreneurOut(
        category=score.category, confidence=score.confidence, gaps=gaps
    )


@router.post("/companies/{company_id}/score")
def compute_score(
    company_id: str,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if user.role == Role.investisseur:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")
    company = load_company(company_id, db, user)
    score = svc.compute(db, company, user, ip=_ip(request))
    return _view(score, user)


@router.get("/companies/{company_id}/score")
def get_score(
    company_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    if user.role == Role.investisseur:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")
    company = load_company(company_id, db, user)
    if company.score is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Score non encore calculé"
        )
    return _view(company.score, user)
