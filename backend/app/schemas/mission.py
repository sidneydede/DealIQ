"""Schémas Pydantic — espace mission (M8)."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.domain.enums import DeliverableKind, DeliverableStatus, MissionStatus, Role


class MissionTaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    label: str
    position: int
    done: bool


class TaskToggle(BaseModel):
    done: bool


class DeliverableCreate(BaseModel):
    kind: DeliverableKind
    note: str | None = None


class DeliverableUpdate(BaseModel):
    status: DeliverableStatus | None = None
    note: str | None = None


class DeliverableOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    kind: DeliverableKind
    version: int
    status: DeliverableStatus
    note: str | None


class MissionReviewOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    role: Role
    reviewer_id: str | None
    note: str | None
    created_at: datetime


class MissionDetailOut(BaseModel):
    id: str
    company_id: str
    status: MissionStatus
    owner_id: str | None
    tasks: list[MissionTaskOut]
    deliverables: list[DeliverableOut]
    reviews: list[MissionReviewOut]
    can_promote: bool
    blockers: list[str]
