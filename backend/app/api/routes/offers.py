"""Routes offres & demande de devis/RDV (M7)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, load_company, require_cabinet
from app.database import get_db
from app.domain.offers import ANTI_PAY_TO_PLAY, offers_for
from app.models.quote import QuoteRequest
from app.models.user import User
from app.schemas.offer import OffersResponse, QuoteCreate, QuoteOut

router = APIRouter()


@router.get("/meta/offers", response_model=OffersResponse, tags=["meta"])
def list_offers(deal_type: str | None = None) -> OffersResponse:
    # Le filtrage par type de deal pourra restreindre/ordonner les offres ultérieurement.
    _ = deal_type
    return OffersResponse(offers=offers_for(), anti_pay_to_play=ANTI_PAY_TO_PLAY)


@router.post(
    "/companies/{company_id}/quote-request",
    response_model=QuoteOut,
    status_code=status.HTTP_201_CREATED,
)
def request_quote(
    company_id: str,
    payload: QuoteCreate,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> QuoteRequest:
    company = load_company(company_id, db, user)
    deal_type = company.financing_need.deal_type_primary if company.financing_need else None
    quote = QuoteRequest(
        company_id=company.id,
        requested_by=user.id,
        offer_key=payload.offer_key,
        deal_type=deal_type,
        message=payload.message,
        contact_phone=payload.contact_phone,
    )
    db.add(quote)
    db.commit()
    db.refresh(quote)
    return quote


@router.get("/companies/{company_id}/quote-requests", response_model=list[QuoteOut])
def list_quote_requests(
    company_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[QuoteRequest]:
    company = load_company(company_id, db, user)
    return (
        db.query(QuoteRequest)
        .filter(QuoteRequest.company_id == company.id)
        .order_by(QuoteRequest.created_at.desc())
        .all()
    )


@router.get("/quote-requests", response_model=list[QuoteOut])
def all_quote_requests(
    db: Session = Depends(get_db), _: User = Depends(require_cabinet)
) -> list[QuoteRequest]:
    """Toutes les demandes de devis — vue cabinet (pilotage conversion)."""
    return db.query(QuoteRequest).order_by(QuoteRequest.created_at.desc()).all()
