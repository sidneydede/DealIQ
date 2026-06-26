"""Calcul du completeness_score et détection du Mode Données Zéro (Module 1).

Implémente le barème exact du cahier des charges (50 pts obligatoires +
50 pts optionnels dont 20 pts répartis sur les réseaux sociaux).
"""

from collections.abc import Iterable

from app.domain.enums import (
    OPTIONAL_FIELD_POINTS,
    REQUIRED_FIELD_POINTS,
    SOCIAL_NETWORK_POINTS,
    DeckStatus,
)
from app.models.deal import Deal, SocialProfile


def _filled(value: str | None) -> bool:
    return value is not None and str(value).strip() != ""


def filled_networks(socials: Iterable[SocialProfile]) -> set[str]:
    """Réseaux pour lesquels au moins un profil non vide est renseigné."""
    return {s.network for s in socials if _filled(s.value)}


def compute_completeness(deal: Deal) -> int:
    """Score de 0 à 100, recalculé à chaque modification de fiche."""
    score = 0

    # Champs obligatoires (50 pts)
    for field, points in REQUIRED_FIELD_POINTS.items():
        if _filled(getattr(deal, field)):
            score += points

    # Champs optionnels hors réseaux (30 pts)
    for field, points in OPTIONAL_FIELD_POINTS.items():
        if _filled(getattr(deal, field)):
            score += points

    # Réseaux sociaux (20 pts répartis)
    present = filled_networks(deal.socials)
    for network, points in SOCIAL_NETWORK_POINTS.items():
        if network.value in present:
            score += points

    return score


def is_data_zero_mode(deal: Deal) -> bool:
    """Mode Données Zéro : les 3 conditions doivent être vraies simultanément.

    - URL site web = vide
    - Deck disponible = non
    - Aucun réseau social renseigné (0 des 5)
    """
    no_website = not _filled(deal.website_url)
    deck_is_no = deal.deck_status == DeckStatus.NON.value
    no_socials = len(filled_networks(deal.socials)) == 0
    return no_website and deck_is_no and no_socials


DATA_ZERO_HINT = (
    "Cherche au moins le @Twitter ou le LinkedIn du fondateur. "
    "C'est souvent la seule donnée publique disponible en CI."
)
