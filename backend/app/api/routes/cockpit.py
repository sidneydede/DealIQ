"""Routes cockpit cabinet & pipeline (M20)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import require_cabinet
from app.database import get_db
from app.domain.enums import CompanyStatus, DealTypeCode
from app.models.quote import QuoteRequest
from app.models.user import User
from app.schemas.cockpit import CockpitItem, QuoteStatusUpdate
from app.schemas.offer import QuoteOut
from app.services import cockpit as svc

router = APIRouter()

_QUOTE_STATUSES = {"nouveau", "traite"}


@router.get("/cockpit/companies", response_model=list[CockpitItem])
def cockpit_companies(
    status_filter: CompanyStatus | None = None,
    deal_type: DealTypeCode | None = None,
    only: str | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(require_cabinet),
) -> list[dict]:
    return svc.cockpit_items(db, status=status_filter, deal_type=deal_type, only=only)


@router.get("/cockpit/pipeline")
def cockpit_pipeline(
    db: Session = Depends(get_db), _: User = Depends(require_cabinet)
) -> dict[str, int]:
    return svc.pipeline_counts(db)


@router.patch("/quote-requests/{quote_id}/status", response_model=QuoteOut)
def update_quote_status(
    quote_id: str,
    payload: QuoteStatusUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_cabinet),
) -> QuoteRequest:
    if payload.status not in _QUOTE_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Statut invalide"
        )
    quote = db.get(QuoteRequest, quote_id)
    if quote is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Demande introuvable")
    quote.status = payload.status
    db.commit()
    db.refresh(quote)
    return quote
