"""Grille de readiness (M5, Annexe C) — logique pure, testable et traçable.

Sortie = 4 catégories + indice de confiance + gating documentaire. Le score chiffré
n'est JAMAIS exposé à l'investisseur (RG-M5-04) ; l'entrepreneur ne voit que la
catégorie et ses gaps.
"""
from __future__ import annotations

from app.domain.enums import CompanyStage, DealTypeCode, ReadinessCategory

GRID_VERSION = "annexe-c-1.0"

# Dimensions et pondérations par défaut (Annexe C). La somme des dimensions positives = 1.0 ;
# le malus de risque est appliqué séparément (jusqu'à -15 %).
DEFAULT_WEIGHTS: dict[str, float] = {
    "traction": 0.20,
    "profitabilite_cashflow": 0.20,
    "qualite_info_financiere": 0.15,
    "clarte_besoin": 0.10,
    "gouvernance": 0.10,
    "qualite_documentaire": 0.10,
    "scalabilite_marche": 0.05,
    "esg": 0.05,
}

# Dimensions subjectives plafonnées (RG-M5-02).
CAPPED_DIMENSIONS = {"scalabilite_marche": 0.6, "esg": 0.6}

# Seuils de catégorisation (paramétrables via ScoringConfig — calibrage métier).
DEFAULT_THRESHOLDS: dict[str, float] = {
    "investor_ready_min": 70.0,  # score mini pour investor-ready (si pièces vérifiées)
    "early_precoce_max": 45.0,   # sous ce score, un dossier early = trop précoce
    "precoce_floor": 30.0,       # plancher absolu trop précoce
}

# Paramètres de l'indice de confiance.
DEFAULT_CONFIDENCE: dict[str, float] = {"base": 0.3, "doc": 0.5, "need": 0.2}

# Libellés de gaps par dimension (pour le mini-rapport M6).
GAP_LABELS: dict[str, str] = {
    "traction": "Traction commerciale à étayer (factures, contrats, historique de ventes).",
    "profitabilite_cashflow": "Rentabilité / cash-flow à démontrer (comptes, relevés).",
    "qualite_info_financiere": (
        "Information financière à fiabiliser (états certifiés / expert-comptable)."
    ),
    "clarte_besoin": "Besoin de financement à clarifier (montant, usage, horizon).",
    "gouvernance": "Gouvernance / actionnariat à documenter (RCCM, statuts, cap table).",
    "qualite_documentaire": "Dossier documentaire incomplet (pièces requises manquantes).",
    "scalabilite_marche": "Potentiel de marché à argumenter.",
    "esg": "Dimensions ESG / impact à renseigner.",
}


def normalize_weights(weights: dict[str, float] | None) -> dict[str, float]:
    """Renvoie des pondérations normalisées (somme = 1) sur les dimensions connues."""
    raw = {d: float((weights or {}).get(d, DEFAULT_WEIGHTS[d])) for d in DEFAULT_WEIGHTS}
    total = sum(raw.values()) or 1.0
    return {d: v / total for d, v in raw.items()}


def apply_caps(signals: dict[str, float], caps: dict[str, float] | None = None) -> dict[str, float]:
    caps = caps if caps is not None else CAPPED_DIMENSIONS
    capped = dict(signals)
    for dim, ceiling in caps.items():
        if dim in capped:
            capped[dim] = min(capped[dim], ceiling)
    return capped


def weighted_total(
    signals: dict[str, float], weights: dict[str, float], risk_malus: float
) -> float:
    """Score 0..100. risk_malus dans [0, 0.15] retranché du total."""
    base = sum(signals.get(d, 0.0) * w for d, w in weights.items())
    base = max(0.0, base - max(0.0, min(risk_malus, 0.15)))
    return round(base * 100, 1)


def map_category(
    total: float,
    *,
    stage: CompanyStage | None,
    deal_type: DealTypeCode | None,
    has_verified_financials: bool,
    thresholds: dict[str, float] | None = None,
) -> ReadinessCategory:
    """Mappe un score en catégorie, avec gating documentaire et orientation par instrument."""
    th = {**DEFAULT_THRESHOLDS, **(thresholds or {})}
    early = stage in (CompanyStage.idee, CompanyStage.amorcage)

    if early and total < th["early_precoce_max"]:
        return ReadinessCategory.trop_precoce
    if total < th["precoce_floor"]:
        return ReadinessCategory.trop_precoce

    # Gating documentaire (RG-M5-01) : pas d'investor-ready sans pièces financières vérifiées.
    if total >= th["investor_ready_min"] and has_verified_financials and not early:
        return ReadinessCategory.investor_ready

    # Orientation dette quand l'opération vise un instrument de dette.
    if deal_type in (DealTypeCode.dette_bancaire, DealTypeCode.dette_privee):
        return ReadinessCategory.plutot_dette_banque

    return ReadinessCategory.a_preparer


def confidence_index(
    doc_verified_fraction: float, need_complete: bool, params: dict[str, float] | None = None
) -> float:
    """Indice de confiance 0..1 selon la part de données vérifiées (RG-M5-03)."""
    p = {**DEFAULT_CONFIDENCE, **(params or {})}
    frac = max(0.0, min(doc_verified_fraction, 1.0))
    value = p["base"] + p["doc"] * frac + (p["need"] if need_complete else 0.0)
    return round(min(value, 1.0), 2)


def derive_gaps(signals: dict[str, float], threshold: float = 0.5, limit: int = 5) -> list[str]:
    """Liste de 3-5 blocages prioritaires : dimensions sous le seuil, triées par criticité."""
    weak = sorted(
        ((d, v) for d, v in signals.items() if v < threshold and d in GAP_LABELS),
        key=lambda kv: kv[1],
    )
    return [GAP_LABELS[d] for d, _ in weak[:limit]]
