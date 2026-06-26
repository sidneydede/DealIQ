"""Énumérations et barèmes métier (Module 1 — Sourcing manuel).

Valeurs alignées sur le cahier des charges. Stockées en base sous forme de
chaînes (String) ; la validation des valeurs autorisées est faite côté Pydantic.
"""

from enum import StrEnum


class Stage(StrEnum):
    """Stade de la startup."""

    IDEE = "idee"
    MVP = "mvp"
    TRACTION = "traction"
    SCALE = "scale"


class DeckStatus(StrEnum):
    """Disponibilité du deck."""

    OUI = "oui"
    NON = "non"
    EN_ATTENTE = "en_attente"


class DealSource(StrEnum):
    """Canal d'où provient le deal."""

    EVENT = "event"
    WHATSAPP = "whatsapp"
    RECOMMENDATION = "recommendation"
    COLD_INBOUND = "cold_inbound"
    AUTRE = "autre"


class SocialNetwork(StrEnum):
    """Réseaux sociaux gérés (un champ URL/handle par réseau)."""

    X_TWITTER = "x_twitter"
    LINKEDIN_COMPANY = "linkedin_company"
    LINKEDIN_FOUNDER = "linkedin_founder"
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"


# ── Barème du completeness_score (cf. CDC) ───────────────────────────────────
# Champs obligatoires : 50 pts
REQUIRED_FIELD_POINTS = {
    "name": 15,
    "sector": 10,
    "stage": 10,
    "country": 15,
}

# Champs optionnels hors réseaux sociaux : 30 pts
OPTIONAL_FIELD_POINTS = {
    "founders": 10,
    "description": 5,
    "deal_source": 5,
    "website_url": 5,
    "deck_status": 5,
}

# Réseaux sociaux : 20 pts répartis
SOCIAL_NETWORK_POINTS = {
    SocialNetwork.X_TWITTER: 6,
    SocialNetwork.LINKEDIN_COMPANY: 5,
    SocialNetwork.LINKEDIN_FOUNDER: 5,
    SocialNetwork.FACEBOOK: 2,
    SocialNetwork.INSTAGRAM: 2,
}

assert sum(REQUIRED_FIELD_POINTS.values()) == 50
assert (
    sum(OPTIONAL_FIELD_POINTS.values()) + sum(SOCIAL_NETWORK_POINTS.values()) == 50
)


def score_band(score: int) -> str:
    """Interprétation textuelle du score (cf. CDC)."""
    if score <= 30:
        return "Fiche très incomplète — enrichissement quasi-impossible"
    if score <= 60:
        return "Fiche partielle — enrichissement limité"
    if score <= 85:
        return "Fiche correcte — enrichissement possible"
    return "Fiche complète"
