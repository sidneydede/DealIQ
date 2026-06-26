from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.config import settings
from app.database import get_db
from app.domain.enrichment import (
    FALLBACK_TABLE,
    FALLBACK_TOTAL_MESSAGE,
    PREREQUISITE_MESSAGE,
    ProposalStatus,
    RunStatus,
)
from app.models.deal import Deal
from app.models.enrichment import EnrichmentProposal, EnrichmentRun
from app.models.user import User
from app.schemas.enrichment import (
    EnrichResult,
    EnrichStatus,
    ProposalModify,
    ProposalOut,
    RunOut,
)
from app.services.enrichment.orchestrator import (
    PrerequisiteNotMet,
    RateLimited,
    minutes_until_next,
    prerequisite_met,
    run_enrichment,
)
from app.services.enrichment.validation import (
    ProposalAlreadyResolved,
    resolve_proposal,
)

router = APIRouter(tags=["enrichment"])


def _deal_or_404(db: Session, deal_id: int) -> Deal:
    deal = db.get(Deal, deal_id)
    if deal is None:
        raise HTTPException(status_code=404, detail="Fiche introuvable.")
    return deal


def _proposal_or_404(db: Session, proposal_id: int) -> EnrichmentProposal:
    p = db.get(EnrichmentProposal, proposal_id)
    if p is None:
        raise HTTPException(status_code=404, detail="Proposition introuvable.")
    return p


@router.get("/enrichment/fallbacks")
def fallbacks(_: User = Depends(get_current_user)) -> list[dict]:
    """Table documentaire des fallbacks (source / condition / comportement / label)."""
    return FALLBACK_TABLE


@router.get("/deals/{deal_id}/enrich/status", response_model=EnrichStatus)
def enrich_status(
    deal_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> EnrichStatus:
    deal = _deal_or_404(db, deal_id)
    pre = prerequisite_met(deal)
    remaining = minutes_until_next(db, deal_id)
    return EnrichStatus(
        prerequisite_met=pre,
        minutes_until_next=remaining,
        can_run=pre and remaining == 0,
    )


@router.post("/deals/{deal_id}/enrich", response_model=EnrichResult)
def enrich(
    deal_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> EnrichResult:
    deal = _deal_or_404(db, deal_id)
    try:
        run = run_enrichment(db, deal, mode=settings.enrichment_mode)
    except PrerequisiteNotMet:
        raise HTTPException(status_code=400, detail=PREREQUISITE_MESSAGE) from None
    except RateLimited as exc:
        raise HTTPException(
            status_code=429,
            detail=f"Prochain enrichissement disponible dans {exc.minutes_remaining} minutes.",
        ) from None

    proposals = list(
        db.execute(
            select(EnrichmentProposal)
            .where(EnrichmentProposal.run_id == run.id)
            .order_by(EnrichmentProposal.id)
        )
        .scalars()
        .all()
    )
    message = FALLBACK_TOTAL_MESSAGE if run.status == RunStatus.NO_SOURCE else None
    return EnrichResult(
        run=RunOut.model_validate(run),
        proposals=[ProposalOut.model_validate(p) for p in proposals],
        message=message,
    )


@router.get("/deals/{deal_id}/enrich/runs", response_model=list[RunOut])
def list_runs(
    deal_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[EnrichmentRun]:
    _deal_or_404(db, deal_id)
    return list(
        db.execute(
            select(EnrichmentRun)
            .where(EnrichmentRun.deal_id == deal_id)
            .order_by(EnrichmentRun.started_at.desc())
        )
        .scalars()
        .all()
    )


@router.get("/deals/{deal_id}/proposals", response_model=list[ProposalOut])
def list_proposals(
    deal_id: int,
    status_filter: str | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[EnrichmentProposal]:
    _deal_or_404(db, deal_id)
    stmt = select(EnrichmentProposal).where(EnrichmentProposal.deal_id == deal_id)
    if status_filter:
        stmt = stmt.where(EnrichmentProposal.status == status_filter)
    return list(db.execute(stmt.order_by(EnrichmentProposal.id)).scalars().all())


def _resolve(
    db: Session,
    proposal_id: int,
    action: ProposalStatus,
    new_value: str | None = None,
) -> EnrichmentProposal:
    proposal = _proposal_or_404(db, proposal_id)
    deal = _deal_or_404(db, proposal.deal_id)
    try:
        return resolve_proposal(db, deal, proposal, action, new_value)
    except ProposalAlreadyResolved:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Proposition déjà traitée.",
        ) from None


@router.post("/proposals/{proposal_id}/accept", response_model=ProposalOut)
def accept_proposal(
    proposal_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> EnrichmentProposal:
    return _resolve(db, proposal_id, ProposalStatus.ACCEPTED)


@router.post("/proposals/{proposal_id}/modify", response_model=ProposalOut)
def modify_proposal(
    proposal_id: int,
    payload: ProposalModify,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> EnrichmentProposal:
    return _resolve(db, proposal_id, ProposalStatus.MODIFIED, payload.value)


@router.post("/proposals/{proposal_id}/reject", response_model=ProposalOut)
def reject_proposal(
    proposal_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> EnrichmentProposal:
    return _resolve(db, proposal_id, ProposalStatus.REJECTED)
