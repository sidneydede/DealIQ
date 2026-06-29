"""Schémas Pydantic — programmes sponsorisés (M23)."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums import ProgramStatus


class ProgramCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    sponsor_name: str = Field(min_length=1, max_length=255)
    sponsor_email: str | None = None  # lie un compte sponsor existant
    scope: str | None = None
    deliverables: str | None = None


class ProgramOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    sponsor_name: str
    sponsor_user_id: str | None
    scope: str | None
    deliverables: str | None
    status: ProgramStatus
    created_at: datetime


class MemberAdd(BaseModel):
    company_id: str


class ProgramMemberOut(BaseModel):
    id: str
    company_id: str
    company_name: str | None


class ProgramReport(BaseModel):
    """Reporting d'impact AGRÉGÉ / ANONYMISÉ (RG-M23-02) — aucun nom d'entreprise."""

    cohort_size: int
    by_readiness_category: dict
    by_status: dict
    esg: dict
    deals_total: int
    closings: int
