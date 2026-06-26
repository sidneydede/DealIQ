from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProposalOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    run_id: int
    field: str
    suggested_value: str | None
    source: str
    confidence: str
    label: str | None
    status: str
    collected_at: datetime


class RunOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    deal_id: int
    status: str
    started_at: datetime
    finished_at: datetime | None
    summary: str | None


class EnrichResult(BaseModel):
    """Réponse au déclenchement d'Agent A."""

    run: RunOut
    proposals: list[ProposalOut]
    message: str | None = None  # fallback total le cas échéant


class EnrichStatus(BaseModel):
    prerequisite_met: bool
    minutes_until_next: int
    can_run: bool


class ProposalModify(BaseModel):
    value: str = Field(min_length=1)


class ActivityBanner(BaseModel):
    network: str | None
    last_activity_at: datetime | None
    stale: bool
