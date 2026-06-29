"""Routes cockpit cabinet & pipeline (M20)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.api.deps import require_cabinet
from app.api.pagination import Page, Pagination, pagination
from app.database import get_db
from app.domain.enums import CompanyStatus, Country, DealTypeCode
from app.models.quote import QuoteRequest
from app.models.user import User
from app.schemas.cockpit import CockpitItem, QuoteStatusUpdate
from app.schemas.offer import QuoteOut
from app.services import cockpit as svc
from app.services import csv_export

router = APIRouter()

_QUOTE_STATUSES = {"nouveau", "traite"}

_COCKPIT_CSV_COLUMNS = [
    ("name", "Entreprise"),
    ("country", "Pays"),
    ("sector", "Secteur"),
    ("status", "Statut"),
    ("deal_type_primary", "Type de deal"),
    ("readiness_category", "Readiness"),
    ("score_total", "Score"),
    ("quote_requests", "Devis"),
    ("days_open", "Ancienneté (j)"),
    ("sla_breach", "SLA dépassé"),
]


@router.get("/cockpit/companies", response_model=Page[CockpitItem])
def cockpit_companies(
    status_filter: CompanyStatus | None = None,
    deal_type: DealTypeCode | None = None,
    country: Country | None = None,
    only: str | None = None,
    q: str | None = None,
    page: Pagination = Depends(pagination),
    db: Session = Depends(get_db),
    _: User = Depends(require_cabinet),
) -> Page[CockpitItem]:
    items, total = svc.cockpit_items(
        db, status=status_filter, deal_type=deal_type, country=country, only=only,
        q=q, limit=page.limit, offset=page.offset,
    )
    return Page.build(items, total, page)


@router.get("/cockpit/companies.csv")
def cockpit_companies_csv(
    status_filter: CompanyStatus | None = None,
    deal_type: DealTypeCode | None = None,
    country: Country | None = None,
    only: str | None = None,
    q: str | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(require_cabinet),
) -> Response:
    # Export complet (mêmes filtres que la liste, sans pagination).
    items, _total = svc.cockpit_items(
        db, status=status_filter, deal_type=deal_type, country=country, only=only, q=q, limit=None
    )
    content = csv_export.to_csv(items, _COCKPIT_CSV_COLUMNS)
    return Response(
        content=content,
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="dealflow.csv"'},
    )


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
