"""Schémas Pydantic — KYC/KYB/AML (M15)."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums import KycCheckType, KycStatus, KycSubjectType


class KycRunRequest(BaseModel):
    subject_type: KycSubjectType
    subject_id: str
    check_type: KycCheckType


class KycStatusUpdate(BaseModel):
    status: KycStatus
    notes: str | None = Field(default=None, max_length=2000)


class KycCheckOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    subject_type: KycSubjectType
    subject_id: str
    subject_label: str | None
    check_type: KycCheckType
    status: KycStatus
    provider: str | None
    result: dict
    notes: str | None
    checked_by: str | None
    created_at: datetime
