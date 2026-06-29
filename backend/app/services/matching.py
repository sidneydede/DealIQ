"""Service de matching (M10) : rapproche une entreprise des investisseurs compatibles."""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.domain import matching
from app.models.company import Company
from app.models.investor import Investor
from app.models.reference import DealType


def _company_context(db: Session, company: Company) -> dict:
    need = company.financing_need
    deal_type = need.deal_type_primary if need else None
    instrument = None
    if deal_type is not None:
        dt = db.query(DealType).filter(DealType.code == deal_type).first()
        if dt and dt.instruments:
            instrument = dt.instruments[0]
    return {
        "country": company.country.value,
        "sector": company.sector,
        "instrument": instrument,
        "deal_type": deal_type.value if deal_type else None,
        "amount": float(need.amount) if need and need.amount is not None else None,
        "stage": company.stage.value if company.stage else None,
    }


def _criteria_context(inv: Investor) -> dict:
    c = inv.criteria
    return {
        "countries": c.countries,
        "sectors": c.sectors,
        "instruments": c.instruments,
        "deal_types": c.deal_types,
        "stages": c.stages,
        "exclusions": c.exclusions,
        "ticket_min": float(c.ticket_min) if c.ticket_min is not None else None,
        "ticket_max": float(c.ticket_max) if c.ticket_max is not None else None,
    }


def match_company(db: Session, company: Company) -> list[dict]:
    """Évalue tous les investisseurs ayant des critères ; trie par fit décroissant.

    Le résultat est une proposition : la validation humaine reste obligatoire (RG-M10-03/04).
    """
    ctx = _company_context(db, company)
    investors = db.query(Investor).filter(Investor.criteria.has()).all()

    results: list[dict] = []
    for inv in investors:
        passes, fit, reasons = matching.evaluate(ctx, _criteria_context(inv))
        results.append({
            "investor_id": inv.id,
            "investor_name": inv.name,
            "investor_type": inv.type,
            "passes_hard_filters": passes,
            "fit_score": fit,
            "reasons": reasons,
        })
    # Compatibles d'abord, triés par score de fit.
    results.sort(key=lambda r: (r["passes_hard_filters"], r["fit_score"]), reverse=True)
    return results
