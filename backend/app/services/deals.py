"""Service pipeline deal (M16)."""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.domain import deal as domain
from app.domain.enums import AuditAction, DealStage, InteractionStatus
from app.models.company import Company
from app.models.deal import Deal, DealMilestone, DealStageHistory
from app.models.investor import Investor
from app.models.teaser import Interaction
from app.models.user import User
from app.services import audit

# Étape initiale dérivée de l'avancement de la mise en relation.
_STAGE_FROM_INTERACTION = {
    InteractionStatus.interesse: DealStage.interesse,
    InteractionStatus.nda_envoye: DealStage.nda,
    InteractionStatus.nda_signe: DealStage.data_room,
}


def create_from_interaction(db: Session, interaction: Interaction, actor: User) -> Deal:
    existing = db.query(Deal).filter(Deal.interaction_id == interaction.id).first()
    if existing:
        return existing

    company = db.get(Company, interaction.company_id)
    deal_type = (
        company.financing_need.deal_type_primary
        if company and company.financing_need
        else None
    )
    stage = _STAGE_FROM_INTERACTION.get(interaction.status, DealStage.interesse)

    deal = Deal(
        company_id=interaction.company_id,
        investor_id=interaction.investor_id,
        interaction_id=interaction.id,
        deal_type=deal_type,
        stage=stage,
        owner_id=actor.id,
    )
    db.add(deal)
    db.flush()

    for pos, label in enumerate(domain.milestones_for(deal_type)):
        db.add(DealMilestone(deal_id=deal.id, label=label, position=pos))
    db.add(DealStageHistory(deal_id=deal.id, old_stage=None, new_stage=stage, actor_id=actor.id))

    db.commit()
    db.refresh(deal)
    audit.record(
        db, AuditAction.deal_created, actor=actor, object_type="Deal", object_id=deal.id,
        meta={"company_id": deal.company_id, "investor_id": deal.investor_id},
    )
    return deal


def advance_stage(
    db: Session, deal: Deal, new_stage: DealStage, note: str | None, actor: User,
    ip: str | None = None,
) -> Deal:
    old = deal.stage
    deal.stage = new_stage
    db.add(DealStageHistory(
        deal_id=deal.id, old_stage=old, new_stage=new_stage, actor_id=actor.id, note=note,
    ))
    db.commit()
    db.refresh(deal)
    audit.record(
        db, AuditAction.deal_stage_changed, actor=actor, object_type="Deal", object_id=deal.id,
        meta={"old": old.value, "new": new_stage.value, "note": note}, ip_address=ip,
    )
    return deal


def to_dict(db: Session, deal: Deal) -> dict:
    company = db.get(Company, deal.company_id)
    investor = db.get(Investor, deal.investor_id)
    return {
        "id": deal.id,
        "company_id": deal.company_id,
        "company_name": company.name if company else None,
        "investor_id": deal.investor_id,
        "investor_name": investor.name if investor else None,
        "interaction_id": deal.interaction_id,
        "deal_type": deal.deal_type,
        "stage": deal.stage,
        "owner_id": deal.owner_id,
        "created_at": deal.created_at,
    }


def list_deals(
    db: Session,
    *,
    stage: DealStage | None = None,
    deal_type: str | None = None,
    limit: int | None = None,
    offset: int = 0,
) -> tuple[list[dict], int]:
    q = db.query(Deal).order_by(Deal.created_at.desc())
    if stage:
        q = q.filter(Deal.stage == stage)
    if deal_type:
        q = q.filter(Deal.deal_type == deal_type)
    total = q.count()
    if limit is not None:
        q = q.offset(offset).limit(limit)
    return [to_dict(db, d) for d in q.all()], total


def detail(db: Session, deal: Deal) -> dict:
    data = to_dict(db, deal)
    data["milestones"] = (
        db.query(DealMilestone)
        .filter(DealMilestone.deal_id == deal.id)
        .order_by(DealMilestone.position)
        .all()
    )
    data["history"] = (
        db.query(DealStageHistory)
        .filter(DealStageHistory.deal_id == deal.id)
        .order_by(DealStageHistory.created_at.desc())
        .all()
    )
    return data


def toggle_milestone(db: Session, milestone: DealMilestone, done: bool) -> DealMilestone:
    milestone.done = done
    db.commit()
    db.refresh(milestone)
    return milestone


def stage_counts(db: Session) -> dict[str, int]:
    counts = {s.value: 0 for s in DealStage}
    for (st,) in db.query(Deal.stage).all():
        counts[st.value if hasattr(st, "value") else st] += 1
    return counts
