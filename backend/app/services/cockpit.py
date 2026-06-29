"""Cockpit cabinet (M20 léger) : file de dossiers enrichie + pipeline par statut."""
from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.domain.enums import CompanyStatus, Country, DealTypeCode, ReadinessCategory
from app.models.company import Company
from app.models.quote import QuoteRequest

# Seuil SLA indicatif : un dossier en brouillon non traité au-delà de N jours est signalé.
SLA_DAYS = 2


def _days_open(company: Company) -> int:
    created = company.created_at
    if created.tzinfo is None:
        created = created.replace(tzinfo=UTC)
    return (datetime.now(UTC) - created).days


def cockpit_items(
    db: Session,
    *,
    status: CompanyStatus | None = None,
    deal_type: DealTypeCode | None = None,
    country: Country | None = None,
    only: str | None = None,
    q: str | None = None,
    limit: int | None = None,
    offset: int = 0,
) -> tuple[list[dict], int]:
    """File de dossiers pour le cabinet, filtrable + recherche + pagination.

    Renvoie (page d'items, total filtré). Les filtres dérivés (investor-ready, SLA)
    dépendent du score/ancienneté : on filtre en mémoire puis on pagine.
    """
    companies = db.query(Company).order_by(Company.created_at.desc()).all()

    # nombre de demandes de devis par entreprise (un seul passage)
    quote_counts: dict[str, int] = {}
    for (cid,) in db.query(QuoteRequest.company_id).all():
        quote_counts[cid] = quote_counts.get(cid, 0) + 1

    needle = q.strip().lower() if q else None

    items: list[dict] = []
    for c in companies:
        need = c.financing_need
        dtype = need.deal_type_primary if need else None
        score = c.score
        days = _days_open(c)
        sla_breach = c.status == CompanyStatus.brouillon and days > SLA_DAYS

        if status and c.status != status:
            continue
        if deal_type and dtype != deal_type:
            continue
        if country and c.country != country:
            continue
        if only == "a_traiter" and c.status != CompanyStatus.brouillon:
            continue
        if only == "investor_ready" and (
            not score or score.category != ReadinessCategory.investor_ready
        ):
            continue
        if only == "sla" and not sla_breach:
            continue
        if needle and needle not in c.name.lower() and needle not in (c.sector or "").lower():
            continue

        items.append({
            "company_id": c.id,
            "name": c.name,
            "country": c.country,
            "sector": c.sector,
            "status": c.status,
            "deal_type_primary": dtype,
            "readiness_category": score.category if score else None,
            "score_total": score.total if score else None,
            "quote_requests": quote_counts.get(c.id, 0),
            "days_open": days,
            "sla_breach": sla_breach,
        })

    total = len(items)
    if limit is None:
        return items, total
    return items[offset : offset + limit], total


def pipeline_counts(db: Session) -> dict[str, int]:
    """Répartition des dossiers par statut (pipeline commercial)."""
    counts = {s.value: 0 for s in CompanyStatus}
    for (st,) in db.query(Company.status).all():
        counts[st.value if hasattr(st, "value") else st] += 1
    return counts
