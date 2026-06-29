"""Routes admin — configuration & simulation du scoring (M5, calibrage)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import require_admin, require_cabinet
from app.database import get_db
from app.domain.enums import CompanyStage, DealTypeCode
from app.models.company import Company
from app.models.reference import DealType
from app.models.user import User
from app.schemas.scoring import (
    ScoringConfigOut,
    ScoringConfigUpdate,
    SimulateIn,
    SimulateOut,
)
from app.services import scoring as svc

router = APIRouter()


def _config_out(db: Session, config) -> dict:
    deal_type_weights = {
        dt.code.value: dt.scoring_weights
        for dt in db.query(DealType).all()
        if dt.scoring_weights
    }
    return {
        "id": config.id,
        "version": config.version,
        "base_weights": config.base_weights,
        "caps": config.caps,
        "thresholds": config.thresholds,
        "confidence": config.confidence,
        "active": config.active,
        "deal_type_weights": deal_type_weights,
    }


@router.get("/admin/scoring/config", response_model=ScoringConfigOut)
def get_config(db: Session = Depends(get_db), user: User = Depends(require_admin)) -> dict:
    return _config_out(db, svc.get_or_create_config(db, user))


@router.put("/admin/scoring/config", response_model=ScoringConfigOut)
def update_config(
    payload: ScoringConfigUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_admin),
) -> dict:
    config = svc.get_or_create_config(db, user)
    config = svc.update_config(db, config, payload, user)
    return _config_out(db, config)


@router.post("/admin/scoring/simulate", response_model=SimulateOut)
def simulate(
    payload: SimulateIn,
    db: Session = Depends(get_db),
    _: User = Depends(require_cabinet),  # cabinet + admin peuvent simuler/calibrer
) -> dict:
    company = None
    if payload.company_id:
        company = db.get(Company, payload.company_id)
        if company is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Entreprise introuvable"
            )
    deal_type = DealTypeCode(payload.deal_type) if payload.deal_type else None
    stage = CompanyStage(payload.stage) if payload.stage else None
    return svc.simulate(
        db,
        company=company,
        deal_type=deal_type,
        signals=payload.signals,
        has_verified_financials=payload.has_verified_financials,
        verified_fraction=payload.verified_fraction,
        need_complete=payload.need_complete,
        stage=stage,
        config_override=payload.config_override,
    )
