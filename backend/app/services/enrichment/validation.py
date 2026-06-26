"""Validation des propositions (champ par champ) et signal d'activité.

Règle d'or : aucun champ de la fiche n'est écrasé automatiquement. L'analyste
accepte / modifie / rejette chaque proposition individuellement.
"""

from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.domain.enrichment import ACTIVITY_STALE_DAYS, ProposalStatus
from app.models.deal import Deal
from app.models.enrichment import EnrichmentProposal
from app.services.deals import update_deal
from app.services.enrichment.base import WRITABLE_FIELDS


class ProposalAlreadyResolved(Exception):
    pass


class FieldNotWritable(Exception):
    pass


def _apply_value(db: Session, deal: Deal, field: str, value: str | None) -> None:
    if field not in WRITABLE_FIELDS:
        raise FieldNotWritable(field)
    # Réutilise la logique deals : log d'historique + recalcul du score
    update_deal(db, deal, fields={field: value}, socials=None)


def resolve_proposal(
    db: Session,
    deal: Deal,
    proposal: EnrichmentProposal,
    action: ProposalStatus,
    new_value: str | None = None,
) -> EnrichmentProposal:
    if proposal.status != ProposalStatus.PENDING:
        raise ProposalAlreadyResolved()

    if action == ProposalStatus.ACCEPTED:
        _apply_value(db, deal, proposal.field, proposal.suggested_value)
    elif action == ProposalStatus.MODIFIED:
        _apply_value(db, deal, proposal.field, new_value)
    # REJECTED : aucune écriture sur la fiche

    proposal.status = action
    db.commit()
    db.refresh(proposal)
    return proposal


def activity_banner(deal: Deal) -> dict | None:
    """Bandeau « Dernière activité publique » — grisé si > 90 jours."""
    if not deal.last_activity_at:
        return None
    at = deal.last_activity_at
    if at.tzinfo is None:
        at = at.replace(tzinfo=UTC)
    age_days = (datetime.now(UTC) - at).days
    return {
        "network": deal.last_activity_network,
        "last_activity_at": deal.last_activity_at,
        "stale": age_days > ACTIVITY_STALE_DAYS,
    }
