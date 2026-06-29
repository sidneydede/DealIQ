"""Routes pipeline deal (M16) — outil cabinet."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api.deps import require_cabinet
from app.api.pagination import Page, Pagination, pagination
from app.database import get_db
from app.domain import deal as domain
from app.domain.enums import DealStage, DealTypeCode
from app.models.deal import Deal, DealMilestone
from app.models.teaser import Interaction
from app.models.user import User
from app.schemas.deal import (
    DealDetailOut,
    DealOut,
    MilestoneOut,
    MilestoneToggle,
    StageUpdate,
)
from app.services import deals as svc

router = APIRouter()


def _ip(request: Request) -> str | None:
    return request.client.host if request.client else None


@router.post("/interactions/{interaction_id}/deal", response_model=DealOut, status_code=201)
def create_deal(
    interaction_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(require_cabinet),
) -> dict:
    interaction = db.get(Interaction, interaction_id)
    if interaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Mise en relation introuvable"
        )
    deal = svc.create_from_interaction(db, interaction, user)
    return svc.to_dict(db, deal)


@router.get("/deals", response_model=Page[DealOut])
def list_deals(
    stage: DealStage | None = None,
    deal_type: DealTypeCode | None = None,
    page: Pagination = Depends(pagination),
    db: Session = Depends(get_db),
    _: User = Depends(require_cabinet),
) -> Page[DealOut]:
    items, total = svc.list_deals(
        db, stage=stage, deal_type=deal_type.value if deal_type else None,
        limit=page.limit, offset=page.offset,
    )
    return Page.build(items, total, page)


@router.get("/deals/meta/milestones/{deal_type}", response_model=list[str], tags=["meta"])
def milestones_template(deal_type: DealTypeCode) -> list[str]:
    return domain.milestones_for(deal_type)


@router.get("/deals/{deal_id}", response_model=DealDetailOut)
def get_deal(
    deal_id: str, db: Session = Depends(get_db), _: User = Depends(require_cabinet)
) -> dict:
    deal = db.get(Deal, deal_id)
    if deal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deal introuvable")
    return svc.detail(db, deal)


@router.patch("/deals/{deal_id}/stage", response_model=DealOut)
def advance_stage(
    deal_id: str,
    payload: StageUpdate,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_cabinet),
) -> dict:
    deal = db.get(Deal, deal_id)
    if deal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deal introuvable")
    svc.advance_stage(db, deal, payload.stage, payload.note, user, ip=_ip(request))
    return svc.to_dict(db, deal)


@router.patch("/deal-milestones/{milestone_id}", response_model=MilestoneOut)
def toggle_milestone(
    milestone_id: str,
    payload: MilestoneToggle,
    db: Session = Depends(get_db),
    _: User = Depends(require_cabinet),
) -> DealMilestone:
    milestone = db.get(DealMilestone, milestone_id)
    if milestone is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jalon introuvable")
    return svc.toggle_milestone(db, milestone, payload.done)
