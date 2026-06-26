"""Logique métier des fiches deal : création, mise à jour, historique.

Chaque modification de champ est tracée (DealChangeLog) et le completeness_score
est recalculé puis horodaté à chaque enregistrement.
"""

from sqlalchemy.orm import Session

from app.models.deal import Deal, DealChangeLog, SocialProfile
from app.services.completeness import compute_completeness

# Champs scalaires de la fiche suivis dans l'historique
SCALAR_FIELDS = [
    "name",
    "sector",
    "stage",
    "country",
    "founders",
    "description",
    "deal_source",
    "deal_source_other",
    "website_url",
    "deck_status",
    "what_i_know",
]


def _log(deal: Deal, field: str, old, new) -> None:
    deal.changes.append(
        DealChangeLog(
            field=field,
            old_value=None if old is None else str(old),
            new_value=None if new is None else str(new),
        )
    )


def _social_pairs(socials: list[SocialProfile]) -> set[tuple[str, str]]:
    return {(s.network, s.value) for s in socials}


def create_deal(db: Session, *, fields: dict, socials: list[dict]) -> Deal:
    deal = Deal(**{k: fields.get(k) for k in SCALAR_FIELDS if k in fields})
    deal.socials = [
        SocialProfile(network=s["network"], value=s["value"]) for s in socials
    ]
    deal.completeness_score = compute_completeness(deal)
    db.add(deal)
    db.commit()
    db.refresh(deal)
    return deal


def update_deal(
    db: Session,
    deal: Deal,
    *,
    fields: dict,
    socials: list[dict] | None,
) -> Deal:
    """Met à jour les champs fournis uniquement (semantique PATCH).

    `socials=None` -> profils inchangés. `socials=[]` -> tous supprimés.
    """
    # Champs scalaires
    for field in SCALAR_FIELDS:
        if field not in fields:
            continue
        old = getattr(deal, field)
        new = fields[field]
        if old != new:
            setattr(deal, field, new)
            _log(deal, field, old, new)

    # Réseaux sociaux (remplacement complet si fourni)
    if socials is not None:
        current = _social_pairs(deal.socials)
        incoming = {(s["network"], s["value"]) for s in socials}
        for network, value in current - incoming:
            _log(deal, f"social:{network}", value, None)
        for network, value in incoming - current:
            _log(deal, f"social:{network}", None, value)
        deal.socials = [
            SocialProfile(network=n, value=v) for n, v in incoming
        ]

    # Recalcul + horodatage du score
    old_score = deal.completeness_score
    new_score = compute_completeness(deal)
    if new_score != old_score:
        deal.completeness_score = new_score
        _log(deal, "completeness_score", old_score, new_score)

    db.commit()
    db.refresh(deal)
    return deal
