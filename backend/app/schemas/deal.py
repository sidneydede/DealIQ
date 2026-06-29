"""Schémas Pydantic — pipeline deal (M16)."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums import DealStage, DealTypeCode


class DealOut(BaseModel):
    id: str
    company_id: str
    company_name: str | None = None
    investor_id: str
    investor_name: str | None = None
    interaction_id: str | None
    deal_type: DealTypeCode | None
    stage: DealStage
    owner_id: str | None
    created_at: datetime


class StageUpdate(BaseModel):
    stage: DealStage
    note: str | None = Field(default=None, max_length=2000)


class MilestoneOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    label: str
    position: int
    done: bool


class MilestoneToggle(BaseModel):
    done: bool


class StageHistoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    old_stage: DealStage | None
    new_stage: DealStage
    actor_id: str | None
    note: str | None
    created_at: datetime


class DealDetailOut(DealOut):
    milestones: list[MilestoneOut] = []
    history: list[StageHistoryOut] = []
