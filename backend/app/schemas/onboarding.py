"""Schémas Pydantic — onboarding / questionnaire (M3)."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class QuestionOut(BaseModel):
    id: str
    label: str
    type: str
    options: list[str]
    required: bool


class OnboardingSave(BaseModel):
    """Autosave partiel : réponses + étape courante."""

    answers: dict = Field(default_factory=dict)
    current_step: int = 0


class ConsentIn(BaseModel):
    consent_text: str = Field(min_length=3, max_length=2000)


class GatingResult(BaseModel):
    eligible: bool
    route: str  # pipeline | nurturing | orientation_cabinet
    reasons: list[str]


class OnboardingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    company_id: str
    answers: dict
    current_step: int
    completed: bool
    consent_given: bool
    consent_at: datetime | None
    gating_route: str | None
