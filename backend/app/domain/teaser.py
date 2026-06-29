"""Anonymisation des teasers (M11, RG-M11-01) — logique pure et testable.

Aucune donnée ré-identifiante : pas de nom, pas de localisation précise (zone seulement),
chiffres en fourchettes.
"""
from __future__ import annotations

from app.domain.enums import DealTypeCode, Zone

# Fourchettes de CA / montant (FCFA) — jamais de chiffre précis dans un teaser.
_BANDS = [
    (50_000_000, "< 50 M FCFA"),
    (200_000_000, "50 – 200 M FCFA"),
    (1_000_000_000, "200 M – 1 Md FCFA"),
]
_BAND_TOP = "> 1 Md FCFA"

_DEAL_TYPE_LABELS = {
    DealTypeCode.ouverture_capital: "ouverture de capital",
    DealTypeCode.dette_bancaire: "financement par dette bancaire",
    DealTypeCode.dette_privee: "financement par dette privée",
    DealTypeCode.cession_parts: "cession de parts",
    DealTypeCode.ma: "opération de M&A",
    DealTypeCode.hybride: "financement hybride",
    DealTypeCode.partenariat: "partenariat stratégique",
    DealTypeCode.indecis: "opération à préciser",
}

_ZONE_LABELS = {Zone.UEMOA: "Afrique de l'Ouest (UEMOA)", Zone.CEMAC: "Afrique centrale (CEMAC)"}


def band(value: float | None) -> str:
    """Convertit un montant en fourchette (anonymisation)."""
    if value is None:
        return "Non communiqué"
    for ceiling, label in _BANDS:
        if value < ceiling:
            return label
    return _BAND_TOP


def zone_label(zone: Zone) -> str:
    return _ZONE_LABELS.get(zone, zone.value)


def build_title(sector: str, zone: Zone, deal_type: DealTypeCode | None) -> str:
    """Titre anonymisé : secteur + zone + nature d'opération, sans identité."""
    op = (
        _DEAL_TYPE_LABELS.get(deal_type, "opération de financement")
        if deal_type
        else "financement"
    )
    return f"PME du secteur {sector} en {zone_label(zone)} — {op}"
