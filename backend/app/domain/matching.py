"""Logique de matching (M10) — filtres durs + score de fit. Pur et testable.

Le moteur PROPOSE, le consultant DISPOSE : aucune mise en relation automatique (RG-M10-04).
"""
from __future__ import annotations


def evaluate(company: dict, criteria: dict) -> tuple[bool, float, list[str]]:
    """Renvoie (passe_filtres_durs, score_fit_0..1, raisons).

    company : {country, sector, instrument, deal_type, amount, stage}
    criteria: {countries[], sectors[], instruments[], deal_types[], stages[],
               exclusions[], ticket_min, ticket_max}
    """
    reasons: list[str] = []

    def _in(value, allowed) -> bool:
        return (not allowed) or (value in allowed)

    # --- Filtres durs (bloquants, RG-M10-01) ---
    hard_ok = True
    if not _in(company.get("deal_type"), criteria.get("deal_types")):
        reasons.append("Type de deal non couvert")
        hard_ok = False
    if not _in(company.get("country"), criteria.get("countries")):
        reasons.append("Pays hors cible")
        hard_ok = False
    if not _in(company.get("sector"), criteria.get("sectors")):
        reasons.append("Secteur hors cible")
        hard_ok = False
    if not _in(company.get("instrument"), criteria.get("instruments")):
        reasons.append("Instrument non couvert")
        hard_ok = False
    if company.get("stage") and not _in(company.get("stage"), criteria.get("stages")):
        reasons.append("Stade hors cible")
        hard_ok = False

    exclusions = criteria.get("exclusions") or []
    if company.get("sector") in exclusions or company.get("country") in exclusions:
        reasons.append("Exclusion explicite")
        hard_ok = False

    amount = company.get("amount")
    tmin, tmax = criteria.get("ticket_min"), criteria.get("ticket_max")
    if amount is not None:
        if tmin is not None and amount < tmin:
            reasons.append("Ticket sous le minimum")
            hard_ok = False
        if tmax is not None and amount > tmax:
            reasons.append("Ticket au-dessus du maximum")
            hard_ok = False

    if not hard_ok:
        return False, 0.0, reasons

    # --- Score de fit (RG-M10-02), uniquement si les filtres durs passent ---
    fit = 0.5
    if criteria.get("sectors") and company.get("sector") in criteria["sectors"]:
        fit += 0.2
        reasons.append("Secteur dans la thèse")
    if amount is not None and tmin is not None and tmax is not None and tmax > tmin:
        # Ticket centré dans la fourchette → meilleur fit.
        center = (tmin + tmax) / 2
        span = (tmax - tmin) / 2
        closeness = max(0.0, 1 - abs(amount - center) / span)
        fit += 0.2 * closeness
        reasons.append("Ticket dans la fourchette")
    if criteria.get("deal_types") and company.get("deal_type") in criteria["deal_types"]:
        fit += 0.1
        reasons.append("Type de deal explicitement traité")

    return True, round(min(fit, 1.0), 3), reasons
